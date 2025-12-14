from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ваше имя',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Email',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Телефон (необязательно)',
                'pattern': '^\+?[1-9]\d{1,14}$'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Ваше сообщение...',
                'required': True,
                'minlength': 10
            }),
        }
        labels = {
            'name': 'Имя',
            'email': 'Электронная почта',
            'phone': 'Телефон',
            'message': 'Сообщение',
        }
        help_texts = {
            'phone': 'Формат: +7XXXXXXXXXX',
            'message': 'Минимальная длина сообщения - 10 символов',
        }
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Сообщение должно содержать минимум 10 символов')
        return message
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.replace('+', '').isdigit():
            raise forms.ValidationError('Номер телефона должен содержать только цифры и знак +')
        return phone