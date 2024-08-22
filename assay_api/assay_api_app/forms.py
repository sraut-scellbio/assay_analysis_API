from django import forms

class FormCountFluo(forms.Form):
    image = forms.ImageField()

class FormCountLabelfree(forms.Form):
    image = forms.ImageField()

class FormClono(forms.Form):
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
    w1_d1_lf = forms.FileField(label="Label-free Images: ")
    w1_d1_fluo = forms.FileField(label="Fluorescent Images: ")

    w2_d1_lf = forms.FileField(label="Label-free Images: ")
    w2_d1_fluo = forms.FileField(label="Fluorescent Images: ")

    w3_d1_lf = forms.FileField(label="Label-free Images: ")
    w3_d1_fluo = forms.FileField(label="Fluorescent Images: ")

    w4_d1_lf = forms.FileField(label="Label-free Images: ")
    w4_d1_fluo = forms.FileField(label="Fluorescent Images: ")

    w1_dn_lf = forms.FileField(label="Label-free Images: ")
    w1_dn_fluo = forms.FileField(label="Fluorescent Images: ")

    w2_dn_lf = forms.FileField(label="Label-free Images: ")
    w2_dn_fluo = forms.FileField(label="Fluorescent Images: ")

    w3_dn_lf = forms.FileField(label="Label-free Images: ")
    w3_dn_fluo = forms.FileField(label="Fluorescent Images: ")

    w4_dn_lf = forms.FileField(label="Label-free Images: ")
    w4_dn_fluo = forms.FileField(label="Fluorescent Images: ")

    saving_folder_name = forms.CharField(max_length=264, label="Save folder as: ")


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
    w1_d1_lf = forms.FileField(label="Label-free Images: ")
    w2_d1_lf = forms.FileField(label="Label-free Images: ")
    w3_d1_lf = forms.FileField(label="Label-free Images: ")
    w4_d1_lf = forms.FileField(label="Label-free Images: ")
    w1_dn_lf = forms.FileField(label="Label-free Images: ")
    w2_dn_lf = forms.FileField(label="Label-free Images: ")
    w3_dn_lf = forms.FileField(label="Label-free Images: ")
    w4_dn_lf = forms.FileField(label="Label-free Images: ")

    saving_folder_name = forms.CharField(max_length=264, label="Save folder as: ")
