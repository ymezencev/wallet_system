# Generated by Django 3.1.6 on 2021-02-02 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=11, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
