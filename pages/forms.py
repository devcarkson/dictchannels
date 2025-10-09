from django import forms
from .models import ContactSubmission, NewsletterSubscription, QuoteSubmission, ServiceInquiry, Student

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['fname', 'email', 'phone', 'subject', 'message']
        widgets = {
            'fname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Phone',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 5,
                'required': True
            }),
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control border-0',
                'placeholder': 'Enter Your Email',
                'required': True
            }),
        }

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
        }

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'required': True
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'required': True
        })
    )

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Use email as username
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class QuoteForm(forms.ModelForm):
    class Meta:
        model = QuoteSubmission
        fields = ['name', 'phone', 'email', 'service', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'Your Name',
                'style': 'height: 55px;',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'Your Mobile Number',
                'style': 'height: 55px;',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'Your Email',
                'style': 'height: 55px;',
                'required': True
            }),
            'service': forms.Select(attrs={
                'class': 'form-select bg-light border-0',
                'style': 'height: 55px;',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'Project Details/Message',
                'rows': 3,
                'required': True
            }),
        }

class ServiceInquiryForm(forms.ModelForm):
    class Meta:
        model = ServiceInquiry
        fields = ['name', 'phone', 'email', 'service', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'Your Name',
                'style': 'height: 55px;',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'Your Mobile Number',
                'style': 'height: 55px;',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'Your Email',
                'style': 'height: 55px;',
                'required': True
            }),
            'service': forms.Select(attrs={
                'class': 'form-select bg-light border-0',
                'style': 'height: 55px;',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'Message',
                'rows': 3,
                'required': True
            }),
        }