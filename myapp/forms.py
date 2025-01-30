from django import forms
from django.contrib.auth.models import User
from .models import Post


class RegisterForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło")
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Potwierdź hasło"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirm"]
        labels = {
            "username": "Nazwa użytkownika",
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Hasła się nie zgadzają!")
        return cleaned_data


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        labels = {
            "title": "Tytuł",
            "content": "Treść",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "n.p. Wycieczka",
                    "class": "form-control",
                }
            ),
            "content": forms.TextInput(
                attrs={
                    "placeholder": "n.p. Co robiłeś na wycieczce?",
                    "class": "form-control",
                }
            ),
        }
