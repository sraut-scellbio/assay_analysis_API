# Generated by Django 4.1 on 2024-10-18 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay_api_app', '0009_modeldormancylabelfree_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modeldormancylabelfree',
            old_name='w1_d1_fluo',
            new_name='w1_d1_lf',
        ),
        migrations.RenameField(
            model_name='modeldormancylabelfree',
            old_name='w1_dn_fluo',
            new_name='w1_dn_lf',
        ),
        migrations.RenameField(
            model_name='modeldormancylabelfree',
            old_name='w2_d1_fluo',
            new_name='w2_d1_lf',
        ),
        migrations.RenameField(
            model_name='modeldormancylabelfree',
            old_name='w2_dn_fluo',
            new_name='w2_dn_lf',
        ),
        migrations.RenameField(
            model_name='modeldormancylabelfree',
            old_name='w3_d1_fluo',
            new_name='w3_d1_lf',
        ),
        migrations.RenameField(
            model_name='modeldormancylabelfree',
            old_name='w3_dn_fluo',
            new_name='w3_dn_lf',
        ),
        migrations.RenameField(
            model_name='modeldormancylabelfree',
            old_name='w4_d1_fluo',
            new_name='w4_d1_lf',
        ),
        migrations.RenameField(
            model_name='modeldormancylabelfree',
            old_name='w4_dn_fluo',
            new_name='w4_dn_lf',
        ),
    ]