from django import forms

from scraping.models import City, Language, Vacancy


class FindForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),# dropdown menu for user choice
        to_field_name='slug',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City'
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(), # dropdown menu for user choice
        to_field_name='slug',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Language'
    )


class VacancyForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),# dropdown menu for user choice
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City'
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(), # dropdown menu for user choice
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Language'
    )

    url = forms.CharField(
        label='URL',
        widget=forms.URLInput(attrs={'class': 'form-control'}),
    )

    title = forms.CharField(
        label='Vacancy title',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    company = forms.CharField(
        label='Company',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    description = forms.CharField(
        label='Vacancy description',
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Vacancy
        fields = '__all__'  # pass all fields from db table to html form

