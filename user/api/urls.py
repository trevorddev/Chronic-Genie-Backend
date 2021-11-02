from django.urls import path
from user.api.views import(
	registration_view,
	ObtainAuthTokenView,
	Logout,
    SetNewPasswordAPIView, 
    # VerifyEmail, 
    PasswordTokenCheckAPI, 
    RequestPasswordResetEmail,
    passwordResetView,
    account_properties_view,
    update_account_view,
    email_unsubscribe_view,
    email_resubscribe_view,
    AccountRetrieve,
    email_check,
    change_password,
)

from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
app_name = 'account'

urlpatterns = [
	path('register', registration_view, name="register"),
    path('email_check', email_check, name="email check"),
    path('login', ObtainAuthTokenView.as_view(), name="login"), # -> see user/api/views.py for response and url info
	path('logout', Logout.as_view(), name="logout"),
    path('properties', account_properties_view, name="properties"),
    path('properties/update', update_account_view, name="update"),

    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('reset/', passwordResetView,
         name='password-reset'),
    path('unsubscribe/<token>/', email_unsubscribe_view, name='unsubscribe-email'),
    path('resubscribe/<token>/', email_resubscribe_view, name='resubscribe-email'),

    path('', AccountRetrieve.as_view(), name="accounts-retrieve-API"),
    path('change_password/', change_password, name='change-password'),
]