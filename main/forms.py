from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User , Course , StatusUpdate , Feedback

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'real_name', 'email', 'photo','is_student','is_teacher', 'user_type', 'password1', 'password2']
    
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description','pdf']

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = StatusUpdate
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Update your status...'}),
        }
        labels = {
            'text': '',
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class CoursePDFUploadForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['pdf']  # Only the PDF field