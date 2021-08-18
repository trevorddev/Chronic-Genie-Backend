# from django import forms
# from django.contrib.auth import (
#     authenticate, get_user_model, password_validation,
# )
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext, gettext_lazy as _

# class SetPasswordForm(forms.Form):
#     """
#     A form that lets a user change set their password without entering the old
#     password
#     """
#     error_messages = {
#         'password_mismatch': _('The two password fields didn’t match.'),
#     }
#     new_password1 = forms.CharField(
#         label=_("New password"),
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#         strip=False,
#         help_text=password_validation.password_validators_help_text_html(),
#     )
#     new_password2 = forms.CharField(
#         label=_("New password confirmation"),
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#     )

#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super().__init__(*args, **kwargs)

#     def clean_new_password2(self):
#         password1 = self.cleaned_data.get('new_password1')
#         password2 = self.cleaned_data.get('new_password2')
#         if password1 and password2:
#             if password1 != password2:
#                 raise ValidationError(
#                     self.error_messages['password_mismatch'],
#                     code='password_mismatch',
#                 )
#         password_validation.validate_password(password2, self.user)
#         return password2

#     def save(self, commit=True):
#         password = self.cleaned_data["new_password1"]
#         self.user.set_password(password)
#         if commit:
#             self.user.save()
#         return self.user



import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
 
from django.contrib.auth import (
    password_validation,
)

class SetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    # new_password2 = forms.CharField(
    #     label=_("New password confirmation"),
    #     strip=False,
    #     widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    # )

    # def clean_data(self):
    #     print("heieh")
    #     password1 = self.cleaned_data.get('new_password1')
    #     password2 = self.cleaned_data.get('new_password2')
    #     if password1 and password2:
    #         if password1 != password2:
    #             raise ValidationError(
    #                 self.error_messages['password_mismatch'],
    #                 code='password_mismatch',
    #             )
    #     password_validation.validate_password(password2, self.user)
    #     return password2