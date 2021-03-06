# Generated by Django 3.1.5 on 2022-02-01 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import thumbnails.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectApproval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('centralized_data_id', models.IntegerField()),
                ('campaign_id', models.CharField(blank=True, max_length=50, null=True)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(blank=True, max_length=250, null=True)),
                ('mobile', models.CharField(max_length=20)),
                ('name', models.CharField(blank=True, max_length=500)),
                ('approval_status', models.IntegerField()),
                ('active', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Created on')),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Updated on')),
            ],
            options={
                'permissions': [('view_own_connectapproval', 'Can view own connect approval')],
            },
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.TextField()),
                ('mrn_no', models.CharField(blank=True, max_length=15, null=True)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(blank=True, max_length=250, null=True)),
                ('nick_name', models.CharField(blank=True, max_length=250, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile-pic-connection')),
                ('profile_pic_icon', thumbnails.fields.ImageField(blank=True, null=True, upload_to='profile-pic-icon-connection')),
                ('mobile', models.CharField(max_length=20)),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('alt_mobile_1', models.CharField(blank=True, max_length=50, null=True)),
                ('alt_mobile_2', models.CharField(blank=True, max_length=50, null=True)),
                ('alt_email_1', models.CharField(blank=True, max_length=200, null=True)),
                ('alt_email_2', models.CharField(blank=True, max_length=200, null=True)),
                ('home_address', models.TextField(blank=True, null=True)),
                ('company_address', models.TextField(blank=True, null=True)),
                ('company_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('company_pincode', models.CharField(blank=True, max_length=25, null=True)),
                ('home_pincode', models.CharField(blank=True, max_length=25, null=True)),
                ('status', models.IntegerField(default=1)),
                ('dob', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=15, null=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('mobile_verified', models.BooleanField(default=False)),
                ('favourite', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True, null=True)),
                ('cop', models.CharField(blank=True, max_length=50, null=True)),
                ('voter', models.CharField(blank=True, max_length=50, null=True)),
                ('booth_no', models.CharField(blank=True, max_length=50, null=True)),
                ('active', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Created on')),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Updated on')),
            ],
            options={
                'permissions': [('view_own_connection', 'Can view own connection')],
            },
        ),
        migrations.CreateModel(
            name='ConnectionTemp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.TextField()),
                ('mrn_no', models.CharField(blank=True, max_length=15)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile-pic-connectiontemp')),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.CharField(blank=True, max_length=200)),
                ('company_name', models.CharField(blank=True, max_length=100)),
                ('alt_mobile_1', models.CharField(blank=True, max_length=50)),
                ('alt_mobile_2', models.CharField(blank=True, max_length=50)),
                ('alt_email_1', models.CharField(blank=True, max_length=200)),
                ('alt_email_2', models.CharField(blank=True, max_length=200)),
                ('home_address', models.TextField(blank=True)),
                ('company_address', models.TextField(blank=True)),
                ('company_phone', models.CharField(blank=True, max_length=15)),
                ('status', models.IntegerField(default=1)),
                ('dob', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=8, null=True, verbose_name='Gender')),
                ('about', models.TextField(blank=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('mobile_verified', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('region', models.TextField(blank=True)),
                ('cop', models.CharField(blank=True, max_length=50)),
                ('voter', models.CharField(blank=True, max_length=50)),
                ('booth_no', models.CharField(blank=True, max_length=50)),
                ('active', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Created on')),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Updated on')),
            ],
            options={
                'permissions': [('view_own_connectiontemp', 'Can view own connection temp')],
            },
        ),
        migrations.CreateModel(
            name='WassengerCronData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_list', models.TextField(blank=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('auth_key', models.TextField(blank=True, null=True)),
                ('device_id', models.TextField(blank=True, null=True)),
                ('product_id', models.TextField(blank=True, null=True)),
                ('response', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Created on')),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Updated on')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wassengercrondata_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wassengercrondata_updated_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wassengercrondata', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('view_own_wassengercrondata', 'Can view own wassengercrondata')],
            },
        ),
        migrations.CreateModel(
            name='MeetingRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_notes', models.TextField(blank=True)),
                ('meeting_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('action_items', models.TextField(blank=True)),
                ('attendees', models.TextField(blank=True)),
                ('next_action_date', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Created on')),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Updated on')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetingrecord_created_by', to=settings.AUTH_USER_MODEL)),
                ('meeting_connection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='konnect.connection')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetingrecord_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('view_own_meetingrecord', 'Can view own meeting record')],
            },
        ),
    ]
