# Generated by Django 2.1.1 on 2019-01-03 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(blank=True, max_length=220, null=True)),
                ('address', models.CharField(blank=True, max_length=220, null=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('views_count', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-time_stamp'],
            },
        ),
        migrations.CreateModel(
            name='SolveBeamCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(blank=True, max_length=220, null=True)),
                ('address', models.CharField(blank=True, max_length=220, null=True)),
                ('user', models.CharField(db_index=True, max_length=150)),
                ('time_stamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('views_count', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-time_stamp'],
            },
        ),
    ]
