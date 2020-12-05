import logging
import os
import traceback
from collections import OrderedDict
from copy import deepcopy

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.transaction import TransactionManagementError
from django.utils.encoding import force_str
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from import_export.results import RowResult
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from project.settings import STATICFILES_DIRS
from .models import Subject, Teacher

logger = logging.getLogger(__name__)


class TeacherResource(resources.ModelResource):
    subjects_taught = fields.Field(
        attribute='subjects_taught',
        widget=ManyToManyWidget(model=Subject, separator=',', field='name'),
    )

    class Meta:
        model = Teacher
        fields = (
            'id', 'first_name', 'last_name', 'profile_picture',
            'email_address', 'phone_number', 'room_number'
        )
        export_order = (
            'id', 'first_name', 'last_name', 'profile_picture',
            'email_address', 'phone_number', 'room_number', 'subjects_taught'
        )

    def before_import_row(self, row, row_number=None, **kwargs):
        images_dir = STATICFILES_DIRS[0] + '/images'
        image_list = []
        for file in os.listdir(images_dir):
            image_list.append(file)

        new_row = OrderedDict()
        for item in row.items():
            old_key = item[0]
            new_key = str(old_key).lower().replace(' ', '_')
            if str(item[0]).lower().replace(' ', '_') in self._meta.export_order:
                new_row[new_key] = item[1]
            else:
                new_row[old_key] = item[1]
        row = new_row

        if str(row['profile_picture']).strip():
            if row['profile_picture'] in image_list:
                row['profile_picture'] = "/static/images/%s" % row['profile_picture']
        else:
            row['profile_picture'] = "/static/images/21167.JPG"
        return row

    def get_field_names(self):
        names = []
        for field in self.get_fields():
            names.append(self.get_field_name(field))
        return names

    def import_row(self, row, instance_loader, using_transactions=True, dry_run=False, raise_errors=False, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        skip_diff = self._meta.skip_diff
        row_result = self.get_row_result_class()()
        original = None
        try:
            row = self.before_import_row(row, **kwargs)
            instance, new = self.get_or_init_instance(instance_loader, row)
            self.after_import_instance(instance, new, **kwargs)
            if new:
                row_result.import_type = RowResult.IMPORT_TYPE_NEW
            else:
                row_result.import_type = RowResult.IMPORT_TYPE_UPDATE
            row_result.new_record = new
            if not skip_diff:
                original = deepcopy(instance)
                diff = self.get_diff_class()(self, original, new)
            if self.for_delete(row, instance):
                if new:
                    row_result.import_type = RowResult.IMPORT_TYPE_SKIP
                    if not skip_diff:
                        diff.compare_with(self, None, dry_run)
                else:
                    row_result.import_type = RowResult.IMPORT_TYPE_DELETE
                    self.delete_instance(instance, using_transactions, dry_run)
                    if not skip_diff:
                        diff.compare_with(self, None, dry_run)
            else:
                import_validation_errors = {}
                try:
                    self.import_obj(instance, row, dry_run)
                except ValidationError as e:
                    # Validation errors from import_obj() are passed on to
                    # validate_instance(), where they can be combined with model
                    # instance validation errors if necessary
                    import_validation_errors = e.update_error_dict(import_validation_errors)
                if self.skip_row(instance, original):
                    row_result.import_type = RowResult.IMPORT_TYPE_SKIP
                else:
                    self.validate_instance(instance, import_validation_errors)
                    self.save_instance(instance, using_transactions, dry_run)
                    self.save_m2m(instance, row, using_transactions, dry_run)
                    # Add object info to RowResult for LogEntry
                    row_result.object_id = instance.pk
                    row_result.object_repr = force_str(instance)
                if not skip_diff:
                    diff.compare_with(self, instance, dry_run)

            if not skip_diff:
                row_result.diff = diff.as_html()
            self.after_import_row(row, row_result, **kwargs)

        except ValidationError as e:
            row_result.import_type = RowResult.IMPORT_TYPE_INVALID
            row_result.validation_error = e
        except Exception as e:
            row_result.import_type = RowResult.IMPORT_TYPE_ERROR
            # There is no point logging a transaction error for each row
            # when only the original error is likely to be relevant
            if not isinstance(e, TransactionManagementError):
                logger.debug(e, exc_info=e)
            tb_info = traceback.format_exc()
            row_result.errors.append(self.get_error_result_class()(e, tb_info, row))

        if self._meta.use_bulk:
            # persist a batch of rows
            # because this is a batch, any exceptions are logged and not associated
            # with a specific row
            if len(self.create_instances) == self._meta.batch_size:
                self.bulk_create(using_transactions, dry_run, raise_errors, batch_size=self._meta.batch_size)
            if len(self.update_instances) == self._meta.batch_size:
                self.bulk_update(using_transactions, dry_run, raise_errors, batch_size=self._meta.batch_size)
            if len(self.delete_instances) == self._meta.batch_size:
                self.bulk_delete(using_transactions, dry_run, raise_errors)

        if row_result.import_type == resources.RowResult.IMPORT_TYPE_ERROR:
            row_result.diff = [
                row.get(name, '') for name in self.get_field_names()
            ]

            # Add a column with the error message
            row_result.diff.append(
                "Errors: {}".format(
                    [err.error for err in row_result.errors]
                )
            )
            # clear errors and mark the record to skip
            row_result.errors = []
            row_result.import_type = resources.RowResult.IMPORT_TYPE_SKIP

        return row_result

    def get_export_headers(self):
        """Custom `get_export_headers` method.
        Replaces header names with `verbose_name` of model fields.
        """
        headers = []
        for field in self.get_fields():
            model_fields = self.Meta.model._meta.get_fields()
            header = next((
                str(x.verbose_name.title()) for x in model_fields
                if x.name == field.column_name
            ), field.column_name)
            headers.append(header)
        return headers


class TeacherAdmin(ImportExportModelAdmin):
    resource_class = TeacherResource


admin.site.register(Subject)
admin.site.register(Teacher, TeacherAdmin)
