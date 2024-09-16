from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
import jdatetime
from rest_framework.exceptions import ValidationError
from datetime import datetime  


class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('ostad', 'Ostad'),
        ('daneshjo', 'Daneshjo'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='daneshjo')

    def __str__(self):
        return f"{self.user_type}"


class Course(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='course_image/', blank=True, null=True)

    def __str__(self):
        return self.title


class CourseContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_contents')
    file = models.FileField(upload_to='course_contents/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignment')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_assignment')
    file = models.FileField(upload_to='assignment/')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class HomeworkDeadline(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='homework_deadline')
    deadline = jmodels.jDateTimeField()

    def __str__(self):
        return f"Deadline for {self.course.name}: {self.deadline}"


class HomeworkUpload(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homework_uploads')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='homework_uploads')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='homework_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        course_deadline = self.course.homework_deadline.deadline
        if jdatetime.datetime.now() > course_deadline:
            raise ValidationError("شما نمی‌توانید بعد از مهلت تعیین‌شده، تکلیف ارسال کنید.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.student.username}"


# is homework grade.
class AssignmentGrade(models.Model):
    assignment = models.ForeignKey('HomeworkUpload', on_delete=models.CASCADE, related_name='grades')
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignment_grades')
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True, null=True)
    graded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.professor.username} graded {self.assignment.title} with {self.grade}"


class CourseGrade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_grades')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='course_grades')
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_grades_given')
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    graded_at = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} received {self.grade} for {self.course.title}"


class RegistrationCourse(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations_course')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations_course')
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {'Enrolled' if self.status else 'Not Enrolled'}"


class OfficeHours(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=60)
    date = jmodels.jDateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.teacher.username} - {self.day_of_week} ({self.start_time} to {self.end_time})"

    def duration(self):
        # محاسبه زمان حضور در یک روز به دقیقه
        start = datetime.combine(self.date, self.start_time)  # ترکیب تاریخ و زمان شروع
        end = datetime.combine(self.date, self.end_time)      # ترکیب تاریخ و زمان پایان
        return (end - start).total_seconds() / 3600  # تبدیل زمان به ساعت
    
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"
