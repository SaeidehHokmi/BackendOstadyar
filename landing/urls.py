from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from .views import RegisterView, CourseViewSet, UserViewSet, CourseContentViewSet, AssignmentViewSet, HomeworkUploadViewSet, CourseGradeViewSet, \
    RegistrationCourseViewSet, OfficeHoursViewSet, ChatMessageViewSet, HomeworkDeadlineViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import include, path

router = DefaultRouter()

router.register(r'courses', CourseViewSet)
router.register(r'users', UserViewSet)
router.register(r'course-contents', CourseContentViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'homework-uploads', HomeworkUploadViewSet)
router.register(r'course-grade', CourseGradeViewSet)
router.register(r'registrations-course', RegistrationCourseViewSet)
router.register(r'office-hours', OfficeHoursViewSet)
router.register(r'chat-messages', ChatMessageViewSet)
router.register(r'homework-deadlines', HomeworkDeadlineViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
