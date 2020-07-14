from django_filters import FilterSet, CharFilter

from directory.models import Teacher


class TeacherListFilter(FilterSet):
    last_name_starts = CharFilter(method='filter_last_name_starts')
    subject = CharFilter(method='filter_subject')
    class Meta:
        model = Teacher
        fields = ['last_name_starts', 'subject']

    def filter_last_name_starts(self, queryset, name, value):
        value = str(value).strip()
        if len(value) > 1:
            return queryset.none()
        return queryset.filter(last_name__startswith=value)

    def filter_subject(self, queryset, name, value):
        return queryset.filter(subjects__name=value).distinct()