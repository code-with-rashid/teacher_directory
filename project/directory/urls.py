from django.urls import path

from directory.views import TeacherListView, TeacherDetailView

urlpatterns = [
    path('teacher/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
    path('teachers/', TeacherListView.as_view(), name='teacher-list'),
]
