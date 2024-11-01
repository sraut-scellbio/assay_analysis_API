# Generated by Django 4.1 on 2024-10-21 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assay_api_app', '0012_alter_modelclono_analysis_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelclono',
            name='magnification',
            field=models.CharField(choices=[('4', '4x'), ('10', '10x'), ('20', '20x'), ('50', '50x')], default='10x', max_length=10),
        ),
        migrations.AddField(
            model_name='modelclonolabelfree',
            name='magnification',
            field=models.CharField(choices=[('4', '4x'), ('10', '10x'), ('20', '20x'), ('50', '50x')], default='10x', max_length=10),
        ),
        migrations.AddField(
            model_name='modeldormancy',
            name='magnification',
            field=models.CharField(choices=[('4', '4x'), ('10', '10x'), ('20', '20x'), ('50', '50x')], default='10x', max_length=10),
        ),
        migrations.AddField(
            model_name='modeldormancylabelfree',
            name='magnification',
            field=models.CharField(choices=[('4', '4x'), ('10', '10x'), ('20', '20x'), ('50', '50x')], default='10x', max_length=10),
        ),
    ]
