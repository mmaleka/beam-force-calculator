# Generated by Django 2.1.1 on 2018-12-24 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beam_diagram', '0003_auto_20181224_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beamsupport',
            name='support',
            field=models.CharField(choices=[('ROLLER SUPPORT', 'ROLLER SUPPORT'), ('PIN SUPPORT', 'PIN SUPPORT'), ('FIXED SUPPORT', 'FIXED SUPPORT')], default='PIN SUPPORT', max_length=20),
        ),
    ]