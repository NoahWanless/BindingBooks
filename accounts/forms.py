from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    favorite_authors = forms.CharField(
        required=False,
        help_text="Enter authors separated by commas.",
        widget=forms.TextInput(attrs={"placeholder": "Tolkien, Sanderson"})
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "favorite_genre",
            "favorite_authors",
            "user_bio",
            "profile_image",
        )

    def clean_favorite_authors(self):
        raw = self.cleaned_data.get("favorite_authors", "")
        if not raw.strip():
            return []
        return [a.strip() for a in raw.split(",")]


class UserUpdateForm(forms.ModelForm):
    favorite_authors = forms.CharField(
        required=False,
        help_text="Enter authors separated by commas.",
        widget=forms.TextInput(attrs={"placeholder": "Tolkien, Sanderson"})
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "favorite_genre",
            "favorite_authors",
            "user_bio",
            "profile_image",
        )

    def clean_favorite_authors(self):
        raw = self.cleaned_data.get("favorite_authors", "")
        if not raw.strip():
            return []
        return [a.strip() for a in raw.split(",")]


class ProfileEditForm(forms.ModelForm):
    favorite_authors = forms.CharField(
        required=False,
        help_text="Enter authors separated by commas.",
        widget=forms.TextInput(attrs={"placeholder": "Tolkien, Sanderson"})
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "favorite_genre",
            "favorite_authors",
            "user_bio",
            "profile_image",
        )

    def clean_favorite_authors(self):
        raw = self.cleaned_data.get("favorite_authors", "")
        if not raw.strip():
            return []
        return [a.strip() for a in raw.split(",")]