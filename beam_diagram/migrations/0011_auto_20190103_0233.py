# Generated by Django 2.1.1 on 2019-01-03 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beam_diagram', '0010_auto_20190102_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beamsupport',
            name='beamLength',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='beam_support', to='beam_diagram.Beamlength'),
        ),
        migrations.AlterField(
            model_name='distributedload',
            name='beamLength',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='distributed_load', to='beam_diagram.Beamlength'),
        ),
        migrations.AlterField(
            model_name='momentload',
            name='beamLength',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='moment_load', to='beam_diagram.Beamlength'),
        ),
        migrations.AlterField(
            model_name='pointload',
            name='beamLength',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='point_load', to='beam_diagram.Beamlength'),
        ),
    ]
