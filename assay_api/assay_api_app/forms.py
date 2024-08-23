from django import forms
from django.core import validators

def check_for_z(value):
    if value[0].lower == 'z':
        raise forms.ValidationError("Cannot Start with Z.")

class FormCountFluo(forms.Form):
    image = forms.ImageField()

    def clean(self):
        all_clean_data = super.clean()


class FormCountLabelfree(forms.Form):
    image = forms.ImageField()

    def clean(self):
        all_clean_data = super.clean()


class FormClono(forms.Form):
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

    name = forms.CharField(max_length=264, label="Enter your name: ",              validators=[check_for_z])
    num_wells = forms.ChoiceField(label="Choose number of wells: ", choices=WELL_CHOICES)
    analysis_type = forms.ChoiceField(label="Choose analysis type: ", choices=ANALYSIS_CHOICES)

    # folder upload fields
    w1_d1_lf = forms.FileField(label="Label-free Images: ", disabled=True)
    w1_d1_fluo = forms.FileField(label="Fluorescent Images: ", disabled=True)

    w2_d1_lf = forms.FileField(label="Label-free Images: ", disabled=True)
    w2_d1_fluo = forms.FileField(label="Fluorescent Images: ", disabled=True)

    w3_d1_lf = forms.FileField(label="Label-free Images: ", disabled=True)
    w3_d1_fluo = forms.FileField(label="Fluorescent Images: ", disabled=True)

    w4_d1_lf = forms.FileField(label="Label-free Images: ", disabled=True)
    w4_d1_fluo = forms.FileField(label="Fluorescent Images: ", disabled=True)

    w1_dn_lf = forms.FileField(label="Label-free Images: ", disabled=True)
    w1_dn_fluo = forms.FileField(label="Fluorescent Images: ", disabled=True)

    w2_dn_lf = forms.FileField(label="Label-free Images: ", disabled=True)
    w2_dn_fluo = forms.FileField(label="Fluorescent Images: ", disabled=True)

    w3_dn_lf = forms.FileField(label="Label-free Images: ", disabled=True)
    w3_dn_fluo = forms.FileField(label="Fluorescent Images: ", disabled=True)

    w4_dn_lf = forms.FileField(label="Label-free Images: ", disabled=True)
    w4_dn_fluo = forms.FileField(label="Fluorescent Images: ", disabled=True)

    saving_folder_name = forms.CharField(max_length=264, label="Save folder as: ")

    def clean(self):
        all_clean_data = super.clean()


class FormClonoLabelfree(forms.Form):
    WELL_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
    ]

    ANALYSIS_CHOICES = [
        (1, "Single Day"),
        (2, "Multi Day")
    ]

    name = forms.CharField(max_length=264, label="Enter your name: ")
    num_wells = forms.ChoiceField(label="Choose number of wells: ", choices=WELL_CHOICES)
    analysis_type = forms.ChoiceField(label="Choose analysis type: ", choices=ANALYSIS_CHOICES)

    # folder upload fields
    w1_d1_lf = forms.FileField(label="Label-free Images: ", disabled=True)
    w2_d1_lf = forms.FileField(label="Label-free Images: ", disabled=True)
    w3_d1_lf = forms.FileField(label="Label-free Images: ", disabled=True)
    w4_d1_lf = forms.FileField(label="Label-free Images: ", disabled=True)
    w1_dn_lf = forms.FileField(label="Label-free Images: ", disabled=True)
    w2_dn_lf = forms.FileField(label="Label-free Images: ", disabled=True)
    w3_dn_lf = forms.FileField(label="Label-free Images: ", disabled=True)
    w4_dn_lf = forms.FileField(label="Label-free Images: ", disabled=True)

    saving_folder_name = forms.CharField(max_length=264, label="Save folder as: ")

    def clean(self):
        all_clean_data = super.clean()
