# Generated by Django 5.2.1 on 2025-05-28 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_delete_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='phone',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, default='Hi There! I am using Task Manager', max_length=500),
            preserve_default=False,
        ),
    ]
