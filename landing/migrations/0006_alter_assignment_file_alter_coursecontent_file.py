# Generated by Django 5.1 on 2024-09-01 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0005_assignment_coursecontent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='file',
            field=models.FileField(upload_to='media/assignment/'),
        ),
        migrations.AlterField(
            model_name='coursecontent',
            name='file',
            field=models.FileField(upload_to='media/course_contents/'),
        ),
    ]
