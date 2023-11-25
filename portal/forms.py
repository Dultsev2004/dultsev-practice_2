from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Application, Category


class RegistrationUserForm(UserCreationForm):
    username = forms.CharField(label='Введите логин', widget=forms.TextInput)
    email = forms.EmailField(label='Введите Email', widget=forms.EmailInput)
    password1 = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Введите повтор пароля', widget=forms.PasswordInput)
    consent = forms.BooleanField(label='Согласие на обработку данных', widget=forms.CheckboxInput, )

    class Meta:
        model = CustomUser
        fields = ('full_name', 'username', 'email', 'password1', 'password2', 'consent')

    def true_passwords(self):
        value = self.cleaned_data
        if value['password1'] != value['password2']:
            raise forms.ValidationError("Пароли не совпадают!")
        return value['password2']


class ApplicationForm(forms.ModelForm):
    def clean_image(self):
        image = self.cleaned_data.get("image")
        image_types = ['.jpg', '.jpeg', '.png', '.bpm']

        for image_type in image_types:
            if image_type in str(image) and image.size <= 2097152:
                return image

        raise forms.ValidationError(
            "Допустимый формат изображений: jpg, jpeg, png, bmp и размер не более 2МБ"
        )

    class Meta:
        model = Application
        fields = ('title', 'description', 'category', 'image',)


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class ApplicationDoneForm(forms.ModelForm):
    image_created = forms.ImageField(label='Созданный дизайн', required=True)

    class Meta:
        model = Application
        fields = ('image_created',)


class ApplicationInWorkForm(forms.ModelForm):
    comment = forms.CharField(label='Комментарий', widget=forms.Textarea, required=True)

    class Meta:
        model = Application
        fields = ('comment',)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title', 'description', )