import os
from django.db import models
from django.forms import ModelForm

WELL_CHOICES = [
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
]

ANALYSIS_CHOICES = [
    ("Single Day", "Single Day"),
    ("Multi Day", "Multi Day")
]

class ModelCountFluo(models.Model):

    name = models.CharField(max_length=264)
    cell_line = models.CharField(max_length=264)
    image = models.ImageField(upload_to='downloads/count_fluo')
    def __str__(self):
        return self.name

class ModelCountLabelFree(models.Model):
    name = models.CharField(max_length=264)
    cell_line = models.CharField(max_length=264)
    image = models.ImageField(upload_to='downloads/count_labelfree')
    def __str__(self):
        return self.name

class ModelClono(models.Model):
    name = models.CharField(max_length=264)
    cell_line = models.CharField(max_length=264)
    num_wells = models.IntegerField(choices=WELL_CHOICES)
    analysis_type = models.CharField(max_length=50, choices=ANALYSIS_CHOICES)

    w1_d1_lf = models.FileField(upload_to='downloads/clono_analysis', blank=True, null=True)
    w1_d1_fluo = models.FileField(upload_to='downloads/clono_analysis', blank=True, null=True)
    w2_d1_lf = models.FileField(upload_to='downloads/clono_analysis', blank=True, null=True)
    w2_d1_fluo = models.FileField(upload_to='downloads/clono_analysis', blank=True, null=True)
    w3_d1_lf = models.FileField(upload_to='downloads/clono_analysis', blank=True, null=True)
    w3_d1_fluo = models.FileField(upload_to='downloads/clono_analysis', blank=True, null=True)
    w4_d1_lf = models.FileField(upload_to='downloads/clono_analysis', blank=True, null=True)
    w4_d1_fluo = models.FileField(upload_to='downloads/clono_analysis', blank=True, null=True)
    w1_dn_lf = models.FileField(upload_to='downloads/clono_analysis', blank=True, null=True)
    w1_dn_fluo = models.FileField(upload_to='downloads/clono_analysis', blank=True, null=True)
    w2_dn_lf = models.FileField(upload_to='downloads/clono_analysis', blank=True, null=True)
    w2_dn_fluo = models.FileField(upload_to='downloads/clono_analysis', blank=True, null=True)
    w3_dn_lf = models.FileField(upload_to='downloads/clono_analysis', blank=True, null=True)
    w3_dn_fluo = models.FileField(upload_to='downloads/clono_analysis', blank=True, null=True)
    w4_dn_lf = models.FileField(upload_to='downloads/clono_analysis', blank=True, null=True)
    w4_dn_fluo = models.FileField(upload_to='downloads/clono_analysis', blank=True, null=True)

    def __str__(self):
        return self.name

class ModelClonoLabelFree(models.Model):
    name = models.CharField(max_length=264)
    cell_line = models.CharField(max_length=264)
    num_wells = models.IntegerField(choices=WELL_CHOICES)
    analysis_type = models.CharField(max_length=50, choices=ANALYSIS_CHOICES)
    w1_d1_lf = models.FileField(upload_to='downloads/clono_analysis_labelfree', blank=True, null=True)
    w2_d1_lf = models.FileField(upload_to='downloads/clono_analysis_labelfree', blank=True, null=True)
    w3_d1_lf = models.FileField(upload_to='downloads/clono_analysis_labelfree', blank=True, null=True)
    w4_d1_lf = models.FileField(upload_to='downloads/clono_analysis_labelfree', blank=True, null=True)
    w1_dn_lf = models.FileField(upload_to='downloads/clono_analysis_labelfree', blank=True, null=True)
    w2_dn_lf = models.FileField(upload_to='downloads/clono_analysis_labelfree', blank=True, null=True)
    w3_dn_lf = models.FileField(upload_to='downloads/clono_analysis_labelfree', blank=True, null=True)
    w4_dn_lf = models.FileField(upload_to='downloads/clono_analysis_labelfree', blank=True, null=True)

    def __str__(self):
        return self.name
