# Generated by Django 5.1 on 2024-09-01 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0006_alter_assignment_file_alter_coursecontent_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='file',
            field=models.FileField(upload_to='assignment/'),
        ),
        migrations.AlterField(
            model_name='coursecontent',
            name='file',
            field=models.FileField(upload_to='course_contents/'),
        ),
    ]
