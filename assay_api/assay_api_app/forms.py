from django import forms
from django.core import validators
from assay_api_app.models import *

class FormCountFluo(forms.ModelForm):
    class Meta:
        model = ModelCountFluo
        fields = ['name', 'cell_line', 'magnification', 'image']
        labels = {
            'name': 'Enter your name ',
            'cell_line': 'Enter cell-line name ',
            'magnification': 'Magnification',
            'image': 'Upload image ',
        }


class FormCountLabelFree(forms.ModelForm):
    class Meta:
        model = ModelCountLabelFree
        fields = ['name', 'cell_line', 'magnification', 'image']
        labels = {
            'name': 'Enter your name ',
            'cell_line': 'Enter cell-line name ',
            'magnification': 'Magnification',
            'image': 'Upload image ',
        }


class FormClono(forms.ModelForm):
    class Meta:
        model = ModelClono
        fields = [
            'name',
            'cell_line',
            'magnification',
            'num_wells',
            'analysis_type',
            'w1_d1_lf',
            'w1_d1_fluo',
            'w2_d1_lf',
            'w2_d1_fluo',
            'w3_d1_lf',
            'w3_d1_fluo',
            'w4_d1_lf',
            'w4_d1_fluo',
            'w1_dn_lf',
            'w1_dn_fluo',
            'w2_dn_lf',
            'w2_dn_fluo',
            'w3_dn_lf',
            'w3_dn_fluo',
            'w4_dn_lf',
            'w4_dn_fluo'
        ]

        labels = {
            'name': 'Enter your name',
            'cell_line': 'Enter cell-line name',
            'magnification': 'Magnification',
            'num_wells': 'Choose number of wells',
            'analysis_type': 'Choose analysis type',
            'w1_d1_lf': 'Label-free Images',
            'w1_d1_fluo': 'Fluorescent Images',
            'w2_d1_lf': 'Label-free Images',
            'w2_d1_fluo': 'Fluorescent Images',
            'w3_d1_lf': 'Label-free Images',
            'w3_d1_fluo': 'Fluorescent Images',
            'w4_d1_lf': 'Label-free Images',
            'w4_d1_fluo': 'Fluorescent Images',
            'w1_dn_lf': 'Label-free Images',
            'w1_dn_fluo': 'Fluorescent Images',
            'w2_dn_lf': 'Label-free Images',
            'w2_dn_fluo': 'Fluorescent Images',
            'w3_dn_lf': 'Label-free Images',
            'w3_dn_fluo': 'Fluorescent Images',
            'w4_dn_lf': 'Label-free Images',
            'w4_dn_fluo': 'Fluorescent Images'
        }


class FormClonoLabelFree(forms.ModelForm):
    class Meta:
        model = ModelClonoLabelFree
        fields = [
            'name',
            'cell_line',
            'magnification',
            'num_wells',
            'analysis_type',
            'w1_d1_lf',
            'w2_d1_lf',
            'w3_d1_lf',
            'w4_d1_lf',
            'w1_dn_lf',
            'w2_dn_lf',
            'w3_dn_lf',
            'w4_dn_lf'
        ]

        labels = {
            'name': 'Enter your name',
            'cell_line': 'Enter cell-line name',
            'magnification': 'Magnification',
            'num_wells': 'Choose number of wells',
            'analysis_type': 'Choose analysis type',
            'w1_d1_lf': '',
            'w2_d1_lf': '',
            'w3_d1_lf': '',
            'w4_d1_lf': '',
            'w1_dn_lf': '',
            'w2_dn_lf': '',
            'w3_dn_lf': '',
            'w4_dn_lf': ''
        }


class FormMigration(forms.ModelForm):
    class Meta:
        model = ModelMigration
        fields = [
            'name',
            'cell_line',
            'num_wells',
            'w1_d1_fluo',
            'w2_d1_fluo',
            'w3_d1_fluo',
            'w4_d1_fluo'
        ]

        labels = {
            'name': 'Enter your name',
            'cell_line': 'Enter cell-line name',
            'num_wells': 'Choose number of wells',
            'w1_d1_fluo': 'Well A ',
            'w2_d1_fluo': 'Well B ',
            'w3_d1_fluo': 'Well C ',
            'w4_d1_fluo': 'Well D ',
        }


class FormDormancy(forms.ModelForm):
    class Meta:
        model = ModelDormancy
        fields = [
            'name',
            'cell_line',
            'magnification',
            'num_wells',
            'analysis_type',
            'w1_d1_fluo',
            'w2_d1_fluo',
            'w3_d1_fluo',
            'w4_d1_fluo',
            'w1_dn_fluo',
            'w2_dn_fluo',
            'w3_dn_fluo',
            'w4_dn_fluo'
        ]

        labels = {
            'name': 'Enter your name',
            'cell_line': 'Enter cell-line name',
            'magnification': 'Magnification',
            'num_wells': 'Choose number of wells',
            'analysis_type': 'Choose analysis type',
            'w1_d1_fluo': '',
            'w2_d1_fluo': '',
            'w3_d1_fluo': '',
            'w4_d1_fluo': '',
            'w1_dn_fluo': '',
            'w2_dn_fluo': '',
            'w3_dn_fluo': '',
            'w4_dn_fluo': ''
        }


class FormDormancyLabelFree(forms.ModelForm):
    class Meta:
        model = ModelDormancyLabelFree
        fields = [
            'name',
            'cell_line',
            'magnification',
            'num_wells',
            'analysis_type',
            'w1_d1_lf',
            'w2_d1_lf',
            'w3_d1_lf',
            'w4_d1_lf',
            'w1_dn_lf',
            'w2_dn_lf',
            'w3_dn_lf',
            'w4_dn_lf'
        ]

        labels = {
            'name': 'Enter your name',
            'cell_line': 'Enter cell-line name',
            'magnification': 'Magnification',
            'num_wells': 'Choose number of wells',
            'analysis_type': 'Choose analysis type',
            'w1_d1_lf': '',
            'w2_d1_lf': '',
            'w3_d1_lf': '',
            'w4_d1_lf': '',
            'w1_dn_lf': '',
            'w2_dn_lf': '',
            'w3_dn_lf': '',
            'w4_dn_lf': ''
        }
