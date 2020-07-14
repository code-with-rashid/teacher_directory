from django.views.generic import DetailView
from django_filters.views import FilterView

from directory.filters import TeacherListFilter
from directory.models import Teacher


class TeacherListView(FilterView):
    model = Teacher
    template_name = 'teachers.html'
    filterset_class = TeacherListFilter


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'teacher_detail.html'
