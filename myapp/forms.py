from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import Post, Comment, Rate


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


class CommentForm(forms.ModelForm):
    author_name = forms.CharField(
        max_length=100, required=False, label="Imię (opcjonalnie)"
    )

    class Meta:
        model = Comment
        fields = ["text", "author_name"]
        labels = {"text": "Treść komentarza"}


class RateForm(forms.ModelForm):
    score = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        label="Ocena",
    )

    class Meta:
        model = Rate
        fields = ["score"]
        labels = {"text": "Ocena"}


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Stare hasło"),
        widget=forms.PasswordInput,
    )
    new_password1 = forms.CharField(
        label=_("Nowe hasło"),
        widget=forms.PasswordInput,
    )
    new_password2 = forms.CharField(
        label=_("Potwierdzenie nowego hasła"), widget=forms.PasswordInput
    )

    class Meta:
        fields = ("old_password", "new_password1", "new_password2")


class CustomUserChangeForm(UserChangeForm):
    password = None
    username = forms.CharField(label=_("Nazwa użytkownika"))
    first_name = forms.CharField(label=_("Imię"))
    last_name = forms.CharField(label=_("Nazwisko"))
    email = forms.CharField(label=_("Email"))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
