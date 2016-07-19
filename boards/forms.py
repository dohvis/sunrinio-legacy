from django import forms
from django.db import models
from .models import Post

class PostWriteForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
    def __init__(self, *args, **kwargs):
        super(PostWriteForm, self).__init__(*args, **kwargs)
        self.fields['title'].error_messages = {'required': '제목을 입력해주세요.'}
        self.fields['content'].error_messages = {'required': '내용을 입력해주세요.'}
