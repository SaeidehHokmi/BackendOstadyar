import jdatetime
from django_jalali.serializers.serializerfield import JDateField

from .models import Course, User, CourseGrade, RegistrationCourse, OfficeHours, ChatMessage, HomeworkDeadline
from rest_framework import serializers
from .models import CourseContent, Assignment
from .models import HomeworkUpload


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'teacher', 'title', 'description', 'file']

    def validate_teacher(self, value):
        if not value.profile.user_type == 'ostad':
            raise serializers.ValidationError("User must be a teacher.")
        return value


class CourseContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseContent
        fields = ['id', 'course', 'file', 'description']


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'course', 'file', 'description', 'uploaded_at']


class HomeworkUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkUpload
        fields = ['id', 'student', 'course', 'title', 'description', 'file', 'uploaded_at']

    def validate(self, data):
        course = data['course']
        if course.homework_deadline.deadline < jdatetime.datetime.now():
            raise serializers.ValidationError("شما نمی‌توانید بعد از مهلت تعیین‌شده، تکلیف ارسال کنید.")
        return data


class HomeworkDeadlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkDeadline
        fields = ['id', 'course', 'deadline']


class CourseGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseGrade
        fields = ['id', 'student', 'course', 'professor', 'grade', 'graded_at']
        read_only_fields = ['graded_at']


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationCourse
        fields = ['id', 'student', 'course', 'status']


class OfficeHoursSerializer(serializers.ModelSerializer):
    date = JDateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    start_time = serializers.TimeField(format="%H:%M", input_formats=["%H:%M"])
    end_time = serializers.TimeField(format="%H:%M", input_formats=["%H:%M"])

    class Meta:
        model = OfficeHours
        fields = ['id', 'teacher', 'date', 'start_time', 'end_time']


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver', 'file', 'message', 'timestamp']

    def validate(self, data):
        if data['sender'] == data['receiver']:
            raise serializers.ValidationError("Sender and receiver cannot be the same user.")
        return data
