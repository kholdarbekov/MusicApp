from django import forms
from .models import Chart


class ChartForm(forms.ModelForm):
    class Meta:
        model = Chart
        fields = '__all__'

    def clean(self):
        cleaned_data = self.cleaned_data
        musics = cleaned_data['musics']
        max_music = cleaned_data['number_of_songs']
        current_number = musics.count()
        if current_number > max_music:
            raise forms.ValidationError('This chart can contain only %d number of musics, but you are trying to add %d' % (max_music, current_number))
        return cleaned_data
