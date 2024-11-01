# Generated by Django 4.1 on 2024-10-29 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assay_api_app', '0013_modelclono_magnification_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelclono',
            name='magnification',
            field=models.CharField(choices=[('4', '4x'), ('10', '10x'), ('20', '20x')], default='10x', max_length=10),
        ),
        migrations.AlterField(
            model_name='modelclonolabelfree',
            name='magnification',
            field=models.CharField(choices=[('4', '4x'), ('10', '10x'), ('20', '20x')], default='10x', max_length=10),
        ),
        migrations.AlterField(
            model_name='modelcountfluo',
            name='magnification',
            field=models.CharField(choices=[('4', '4x'), ('10', '10x'), ('20', '20x')], default='10x', max_length=10),
        ),
        migrations.AlterField(
            model_name='modelcountlabelfree',
            name='magnification',
            field=models.CharField(choices=[('4', '4x'), ('10', '10x'), ('20', '20x')], default='10x', max_length=10),
        ),
        migrations.AlterField(
            model_name='modeldormancy',
            name='magnification',
            field=models.CharField(choices=[('4', '4x'), ('10', '10x'), ('20', '20x')], default='10x', max_length=10),
        ),
        migrations.AlterField(
            model_name='modeldormancylabelfree',
            name='magnification',
            field=models.CharField(choices=[('4', '4x'), ('10', '10x'), ('20', '20x')], default='10x', max_length=10),
        ),
    ]