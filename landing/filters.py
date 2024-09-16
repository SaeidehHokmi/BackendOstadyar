import django_filters
from .models import CourseContent, HomeworkUpload, CourseGrade, RegistrationCourse, OfficeHours
import django_filters
from .models import Assignment
from rest_framework.permissions import BasePermission


class CourseContentFilter(django_filters.FilterSet):
    class Meta:
        model = CourseContent
        fields = {
            'course__id': ['exact'],
            'teacher__id': ['exact'],
            'course__title': ['exact', 'icontains'],
        }


class AssignmentFilter(django_filters.FilterSet):
    class Meta:
        model = Assignment
        fields = {
            'course__id': ['exact'],
            'teacher__id': ['exact'],
            'title': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'uploaded_at': ['exact', 'gte', 'lte'],
            'course__title': ['exact', 'icontains']
        }


class HomeworkUploadFilter(django_filters.FilterSet):
    class Meta:
        model = HomeworkUpload
        fields = {
            'student': ['exact'],
            'course': ['exact'],
            'title': ['exact', 'icontains'],
            'uploaded_at': ['exact', 'gte', 'lte'],
        }


class CourseGradeFilter(django_filters.FilterSet):
    class Meta:
        model = CourseGrade
        fields = {
            'student': ['exact'],
            'course': ['exact'],
            'grade': ['exact', 'gte', 'lte'],
            'graded_at': ['exact', 'gte', 'lte'],
        }


class RegistrationCourseFilter(django_filters.FilterSet):
    student = django_filters.NumberFilter(field_name='student', lookup_expr='exact')
    course = django_filters.NumberFilter(field_name='course', lookup_expr='exact')
    status = django_filters.BooleanFilter(field_name='status', lookup_expr='exact')

    class Meta:
        model = RegistrationCourse
        fields = ['student', 'course', 'status']


class OfficeHoursFilter(django_filters.FilterSet):
    teacher = django_filters.NumberFilter(field_name='teacher', lookup_expr='exact')
    day_of_week = django_filters.CharFilter(field_name='day_of_week', lookup_expr='exact')
    start_time = django_filters.TimeFilter(field_name='start_time', lookup_expr='gte')
    end_time = django_filters.TimeFilter(field_name='end_time', lookup_expr='lte')

    class Meta:
        model = OfficeHours
        fields = ['teacher', 'day_of_week', 'start_time', 'end_time']


