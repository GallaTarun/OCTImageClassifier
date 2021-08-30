from django import forms


class InputForm(forms.Form):
    image_path = forms.CharField(required=True,max_length=100,widget=forms.TextInput
                           (attrs={'placeholder':'Enter OCT image path here'}))