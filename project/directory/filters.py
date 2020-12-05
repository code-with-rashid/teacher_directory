from django_filters import FilterSet, CharFilter

from directory.models import Teacher


class TeacherListFilter(FilterSet):
    last_name_starts = CharFilter(method='filter_last_name_starts')
    subject = CharFilter(method='filter_subjects_taught')
    class Meta:
        model = Teacher
        fields = ['last_name_starts', 'subject']

    def filter_last_name_starts(self, queryset, name, value):
        value = str(value).strip()
        if len(value) > 1:
            return queryset.none()
        return queryset.filter(last_name__startswith=value)

    def filter_subjects_taught(self, queryset, name, value):
        return queryset.filter(subjects_taught__name__iexact=value).distinct()