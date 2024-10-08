# Generated by Django 4.1 on 2024-08-29 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assay_api_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelclono',
            name='w1_d1_fluo',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis'),
        ),
        migrations.AlterField(
            model_name='modelclono',
            name='w1_d1_lf',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis'),
        ),
        migrations.AlterField(
            model_name='modelclono',
            name='w1_dn_fluo',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis'),
        ),
        migrations.AlterField(
            model_name='modelclono',
            name='w1_dn_lf',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis'),
        ),
        migrations.AlterField(
            model_name='modelclono',
            name='w2_d1_fluo',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis'),
        ),
        migrations.AlterField(
            model_name='modelclono',
            name='w2_d1_lf',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis'),
        ),
        migrations.AlterField(
            model_name='modelclono',
            name='w2_dn_fluo',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis'),
        ),
        migrations.AlterField(
            model_name='modelclono',
            name='w2_dn_lf',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis'),
        ),
        migrations.AlterField(
            model_name='modelclono',
            name='w3_d1_fluo',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis'),
        ),
        migrations.AlterField(
            model_name='modelclono',
            name='w3_d1_lf',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis'),
        ),
        migrations.AlterField(
            model_name='modelclono',
            name='w3_dn_fluo',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis'),
        ),
        migrations.AlterField(
            model_name='modelclono',
            name='w3_dn_lf',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis'),
        ),
        migrations.AlterField(
            model_name='modelclono',
            name='w4_d1_fluo',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis'),
        ),
        migrations.AlterField(
            model_name='modelclono',
            name='w4_d1_lf',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis'),
        ),
        migrations.AlterField(
            model_name='modelclono',
            name='w4_dn_fluo',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis'),
        ),
        migrations.AlterField(
            model_name='modelclono',
            name='w4_dn_lf',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis'),
        ),
        migrations.AlterField(
            model_name='modelclonolabelfree',
            name='w1_d1_lf',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis_labelfree'),
        ),
        migrations.AlterField(
            model_name='modelclonolabelfree',
            name='w1_dn_lf',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis_labelfree'),
        ),
        migrations.AlterField(
            model_name='modelclonolabelfree',
            name='w2_d1_lf',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis_labelfree'),
        ),
        migrations.AlterField(
            model_name='modelclonolabelfree',
            name='w2_dn_lf',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis_labelfree'),
        ),
        migrations.AlterField(
            model_name='modelclonolabelfree',
            name='w3_d1_lf',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis_labelfree'),
        ),
        migrations.AlterField(
            model_name='modelclonolabelfree',
            name='w3_dn_lf',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis_labelfree'),
        ),
        migrations.AlterField(
            model_name='modelclonolabelfree',
            name='w4_d1_lf',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis_labelfree'),
        ),
        migrations.AlterField(
            model_name='modelclonolabelfree',
            name='w4_dn_lf',
            field=models.FileField(blank=True, null=True, upload_to='downloads/clono_analysis_labelfree'),
        ),
        migrations.AlterField(
            model_name='modelcountfluo',
            name='image',
            field=models.ImageField(upload_to='downloads/count_fluo'),
        ),
        migrations.AlterField(
            model_name='modelcountlabelfree',
            name='image',
            field=models.ImageField(upload_to='downloads/count_labelfree'),
        ),
    ]
