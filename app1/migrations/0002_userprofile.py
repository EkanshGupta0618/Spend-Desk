# Generated by Django 5.1.4 on 2024-12-13 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('profile_pic', models.ImageField(null=True, upload_to='Media/user_profile')),
                ('password', models.CharField(max_length=25)),
                ('otp', models.CharField(default='000000', max_length=25)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
    ]
