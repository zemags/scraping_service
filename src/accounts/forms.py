from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from scraping.models import Language, City

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))  # attrs={'class': 'form-control'}) for form creating
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))  # dots show while user write password

    def clean(self, *args, **kwargs):
        #default method clean in eaach form exist to check all data from form
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password')

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('User not found.')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Incorrect password.')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('User offline.')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(label='Input email', widget=forms.EmailInput(
        attrs={'class': 'form-control'}))  # attrs={'class': 'form-control'}) for form creating
    password = forms.CharField(label='Input password', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))  # dots show while user write password
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))  # dots show while user write password


    class Meta:
        model = User
        fields = ('email', )

    def clean_password2(self):
        # all methods starts with 'clean' always called
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Passwords didn\'t match')
        return data['password2']


class UserUpdateForm(forms.Form):
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

    send_email = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='Get mail from service.')

    class Meta:
        model = User
        fields = ('city', 'language', 'send_email',)