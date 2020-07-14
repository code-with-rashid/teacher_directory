import os

from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin


# Register your models here.
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from project.settings import STATICFILES_DIRS
from .models import Subject, Teacher


class TeacherResource(resources.ModelResource):
    subjects = fields.Field(
        attribute='subjects',
        widget=ManyToManyWidget(model=Subject, separator=',', field='name'),
    )

    class Meta:
        model = Teacher
        fields = (
            'id', 'first_name', 'last_name', 'profile_picture',
            'email', 'phone', 'room_no'
        )

    def before_import_row(self, row, row_number=None, **kwargs):
        data = super(TeacherResource, self).before_import_row(row, row_number=None, **kwargs)
        images_dir = STATICFILES_DIRS[0] + '/images'
        image_list = []
        for file in os.listdir(images_dir):
            image_list.append(file)

        if str(row['profile_picture']).strip():
            if row['profile_picture'] in image_list:
                row['profile_picture'] = "/static/images/%s" % row['profile_picture']
        else:
            row['profile_picture'] = "/static/images/21167.JPG"
        return data



class TeacherAdmin(ImportExportModelAdmin):
    resource_class = TeacherResource

admin.site.register(Subject)
admin.site.register(Teacher, TeacherAdmin)
