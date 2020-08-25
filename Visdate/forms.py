from django import forms

class accurateUploadForm(forms.Form):
    values = forms.IntegerField(required=True)
    axis = forms.ChoiceField(choices=[(1,"x"),(2,"y"),(3,"x")])

