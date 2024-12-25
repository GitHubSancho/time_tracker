# tracker/forms.py
from django import forms
from .models import TimeRecord
from datetime import datetime
from .models import User, InviteCode
from django.core.exceptions import ValidationError
import re


class TimeRecordForm(forms.ModelForm):

    class Meta:
        model = TimeRecord
        fields = [
            'start_datetime', 'end_datetime', 'project', 'category', 'notes'
        ]
        labels = {
            'project': '项目',
            'category': '分类',
            'start_datetime': '开始时间',
            'end_datetime': '结束时间',
            'notes': '备注',
        }
        widgets = {
            'start_datetime':
                forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime':
                forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(TimeRecordForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:  # 如果是新建记录
            self.initial['start_datetime'] = datetime.now().strftime(
                '%Y-%m-%dT%H:%M')
            self.initial['end_datetime'] = datetime.now().strftime(
                '%Y-%m-%dT%H:%M')
        self.fields['notes'].required = False  # 明确设置 notes 字段为非必填


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='密码',
                                widget=forms.PasswordInput,
                                help_text='密码长度必须在8到20位之间，且包含至少一个字母和一个数字。')
    password2 = forms.CharField(label='确认密码',
                                widget=forms.PasswordInput,
                                help_text='请再次输入密码。')
    invite_code = forms.CharField(label='邀请码', help_text='请输入有效的邀请码。')

    class Meta:
        model = User
        fields = ('username', 'invite_code')
        labels = {
            'username': '用户名',
        }
        help_texts = {
            'username': '用户名必须以字母开头，只能包含字母和数字，且长度在6到10位之间。',
        }

    def clean_invite_code(self):
        invite_code = self.cleaned_data.get('invite_code')
        try:
            invite = InviteCode.objects.get(code=invite_code, uses_left__gt=0)
            invite.uses_left -= 1
            invite.save()
        except InviteCode.DoesNotExist:
            raise ValidationError('邀请码无效或已使用完毕。')
        return invite_code

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[A-Za-z][A-Za-z0-9]{5,9}$', username):
            raise ValidationError('用户名必须以字母开头，只能包含字母和数字，且长度在6到10位之间。')
        if User.objects.filter(username=username).exists():
            raise ValidationError('该用户名已存在，请选择其他用户名。')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8 or len(password1) > 20:
            raise ValidationError('密码长度必须在8到20位之间。')
        if not any(char.isdigit() for char in password1):
            raise ValidationError('密码必须包含至少一个数字。')
        if not any(char.isalpha() for char in password1):
            raise ValidationError('密码必须包含至少一个字母。')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('两次输入的密码不一致。')
        return password2
