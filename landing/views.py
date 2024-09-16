from django.contrib.auth.models import User
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import AssignmentFilter, CourseContentFilter, HomeworkUploadFilter, CourseGradeFilter, RegistrationCourseFilter, OfficeHoursFilter
from .models import Profile, Course, CourseContent, Assignment, HomeworkUpload, CourseGrade, RegistrationCourse, OfficeHours, ChatMessage, HomeworkDeadline
from rest_framework import viewsets

from .permissions import AllowGETForAnonymous
from .serializers import CourseSerializer, UserSerializer, CourseContentSerializer, AssignmentSerializer, HomeworkUploadSerializer, CourseGradeSerializer, RegistrationSerializer, \
    OfficeHoursSerializer, ChatMessageSerializer, HomeworkDeadlineSerializer
from rest_framework.exceptions import PermissionDenied


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Get the data from the request
        username = request.data.get('username')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        user_type = request.data.get('user_type')  # Get user_type from request

        # Debugging print statement
        print(f"Received data - Username: {username}, Password: {password}, User Type: {user_type}")

        # Validate the inputs
        if not username:
            return Response({"error": "Username must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if user_type not in dict(Profile.USER_TYPE_CHOICES):
            return Response({"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(username=username, password=password)

        Profile.objects.create(user=user, user_type=user_type)

        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CourseContentViewSet(viewsets.ModelViewSet):
    queryset = CourseContent.objects.all()
    serializer_class = CourseContentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseContentFilter

    def get_queryset(self):
        user = self.request.user
        if user.profile.user_type == 'daneshjo':
            return CourseContent.objects.all()
        elif user.profile.user_type == 'ostad':
            return CourseContent.objects.filter(teacher=user)
        return CourseContent.objects.none()

    def perform_create(self, serializer):
        if self.request.user.profile.user_type != 'ostad':
            raise PermissionDenied("Only users with 'ostad' role can upload course contents.")

        serializer.save(teacher=self.request.user)


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AssignmentFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.profile.user_type == 'daneshjo':
            return Assignment.objects.all()
        elif user.profile.user_type == 'ostad':
            return Assignment.objects.filter(teacher=user)
        return Assignment.objects.none()

    def perform_create(self, serializer):
        if self.request.user.profile.user_type != 'ostad':
            raise PermissionDenied("Only users with 'ostad' role can upload assignments.")

        serializer.save(teacher=self.request.user)


class HomeworkDeadlineViewSet(viewsets.ModelViewSet):
    queryset = HomeworkDeadline.objects.all()
    serializer_class = HomeworkDeadlineSerializer


class HomeworkUploadViewSet(viewsets.ModelViewSet):
    queryset = HomeworkUpload.objects.all()
    serializer_class = HomeworkUploadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HomeworkUploadFilter

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class CourseGradeViewSet(viewsets.ModelViewSet):
    queryset = CourseGrade.objects.all()
    serializer_class = CourseGradeSerializer
    permission_classes = [AllowGETForAnonymous]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseGradeFilter

    def perform_create(self, serializer):
        serializer.save(professor=self.request.user)


class RegistrationCourseViewSet(viewsets.ModelViewSet):
    queryset = RegistrationCourse.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowGETForAnonymous]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RegistrationCourseFilter

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class OfficeHoursViewSet(viewsets.ModelViewSet):
    queryset = OfficeHours.objects.all()
    serializer_class = OfficeHoursSerializer
    permission_classes = [AllowGETForAnonymous]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfficeHoursFilter

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)
    
    @action(detail=False, methods=['get'])
    def total_hours(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date and end_date:
            office_hours = OfficeHours.objects.filter(
                teacher=request.user,
                date__range=[start_date, end_date]
            )
            total_duration = sum([oh.duration() for oh in office_hours])
            return Response({"total_hours": total_duration})
        return Response({"error": "Please provide start_date and end_date."}, status=400)

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [AllowGETForAnonymous]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sender', 'receiver']

    def get_queryset(self):
        queryset = super().get_queryset()
        user1 = self.request.query_params.get('user1')
        user2 = self.request.query_params.get('user2')

        if user1 and user2:
            # Retrieve all messages between user1 and user2 in both directions
            queryset = queryset.filter(
                Q(sender=user1, receiver=user2) |
                Q(sender=user2, receiver=user1)
            ).order_by('timestamp')

        return queryset
