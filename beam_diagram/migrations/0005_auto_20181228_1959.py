# Generated by Django 2.1.1 on 2018-12-28 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beam_diagram', '0004_auto_20181224_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beamsupport',
            name='support',
            field=models.CharField(choices=[('ROLLER SUPPORT', 'ROLLER SUPPORT'), ('PIN SUPPORT', 'PIN SUPPORT'), ('FIXED SUPPORT', 'FIXED SUPPORT'), ('FREE SUPPORT', 'FREE SUPPORT')], default='PIN SUPPORT', max_length=20),
        ),
        migrations.AlterField(
            model_name='pointload',
            name='point_load_distance',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
