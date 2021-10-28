from user.models import Account
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from user.api.serializers import RegistrationSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, AccountPropertiesSerializer
from rest_framework.authtoken.models import Token
from rest_framework import generics
from django.shortcuts import render
from cryptography.fernet import Fernet
from django.conf import settings
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.http import HttpResponsePermanentRedirect
import os
from user.api.reset_password_form import SetPasswordForm

from component.models import (
	Food,
	Aggravator,
	Symptom,
	Comorbidity,
	DailyMedication,
	FlareMedication
)

from adminPanel.models import (
	Food as appFood,
	Aggravator as appAggravator,
	Symptom as appSymptom,
	Comorbidity as appComorbidity,
	DailyMedication as appDailyMedication,
	FlareMedication as appFlareMedication,
	MarketingEmail,
)

class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):

	if request.method == 'POST':
		serializer = RegistrationSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['first_name'] = account.first_name
			data['date_of_birth'] = account.date_of_birth
			data['gender'] = account.gender
			token = Token.objects.get(user=account).key
			data['token'] = token

			# add default app settings to user settings
			add_app_settings_to_user(account)

			# add email to marketing email db
			add_user_to_narketing_email_list(account)
		else:
			data = serializer.errors
		return Response(data)


class ObtainAuthTokenView(APIView):

	authentication_classes = []
	permission_classes = []

	def post(self, request):
		context = {}

		email = request.POST.get('username')
		password = request.POST.get('password')
		account = authenticate(email=email, password=password)
		if account:
			try:
				token = Token.objects.get(user=account)
			except Token.DoesNotExist:
				token = Token.objects.create(user=account)
			context['response'] = 'Successfully authenticated.'
			context['pk'] = account.pk
			context['email'] = email.lower()
			context['token'] = token.key
		else:
			context['response'] = 'Error'
			context['error_message'] = 'Invalid credentials'

		return Response(context)


class Logout(APIView):

	def get(self, request, format=None):
		# simply delete the token to force a login
		request.user.auth_token.delete()
		return Response(status=status.HTTP_200_OK)



class RequestPasswordResetEmail(generics.GenericAPIView):

	authentication_classes = []
	permission_classes = []
	serializer_class = ResetPasswordEmailRequestSerializer

	def post(self, request):
		serializer = self.serializer_class(data=request.data)

		email = request.data.get('email', '')

		if Account.objects.filter(email=email).exists():
			user = Account.objects.get(email=email)
			uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
			token = PasswordResetTokenGenerator().make_token(user)
			current_site = get_current_site(
				request=request).domain
			relativeLink = reverse(
				'account:password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

			# redirect_url = request.data.get('redirect_url', '')

			redirect_url = 'http://'+ current_site + '/api/account/reset'

			absurl = 'http://'+current_site + relativeLink
			email_body = 'Hello, \n Use link below to reset your password  \n' + \
				absurl+"?redirect_url="+redirect_url
			data = {'email_body': email_body, 'to_email': user.email,
					'email_subject': 'Reset your passsword'}
			Util.send_email(data)
		return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)



class PasswordTokenCheckAPI(generics.GenericAPIView):

	authentication_classes = []
	permission_classes = []

	serializer_class = SetNewPasswordSerializer

	def get(self, request, uidb64, token):

		redirect_url = request.GET.get('redirect_url')

		try:
			id = smart_str(urlsafe_base64_decode(uidb64))
			user = Account.objects.get(id=id)

			if not PasswordResetTokenGenerator().check_token(user, token):
				if len(redirect_url) > 3:
				    return CustomRedirect(redirect_url+'?token_valid=False')
				else:
				    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

			if redirect_url and len(redirect_url) > 3:
				return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
			else:
				return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

		except DjangoUnicodeDecodeError as identifier:
			try:
				# if not PasswordResetTokenGenerator().check_token(user):	
					return CustomRedirect(redirect_url+'?token_valid=False')
					
			except UnboundLocalError as e:
				return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)



class SetNewPasswordAPIView(generics.GenericAPIView):

	authentication_classes = []
	permission_classes = []

	serializer_class = SetNewPasswordSerializer

	def patch(self, request):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)



def passwordResetView(request):

	try:
		uidb64 = request.GET.get('uidb64', '')
		token = request.GET.get('token', '')
		id = force_str(urlsafe_base64_decode(uidb64))
		user = Account.objects.get(id=id)

		if not PasswordResetTokenGenerator().check_token(user, token):
			# raise AuthenticationFailed('The reset link is invalid', 401)
			return render(request, 'password_reset_error.html', {"message": "Token Expires, try to generate token again"})

		# If this is a POST request then process the Form data
		if request.method == 'POST':
			

			
			# Create a form instance and populate it with data from the request (binding):
			form = SetPasswordForm(request.POST)

			# Check if the form is valid:
			if form.is_valid():
				# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
				
				password = form.cleaned_data['new_password1']
				
				user.set_password(password)
				user.save()

				# redirect to a new URL:
				return render(request, 'password_reset_complete.html')

		# If this is a GET (or any other method) create the default form.
		else:
			form = SetPasswordForm()

		context = {
			'form': form,
		}

		return render(request, 'password_reset.html', context)
	except Exception as ex:
		return render(request, 'password_reset_error.html', {"message": "Token Expires, try to generate token again"})


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def account_properties_view(request):

	try:
		account = request.user
	except Account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = AccountPropertiesSerializer(account)
		return Response(serializer.data)



@api_view(['PUT',])
@permission_classes((IsAuthenticated, ))
def update_account_view(request):

	try:
		account = request.user
	except Account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
		
	if request.method == 'PUT':
		serializer = AccountPropertiesSerializer(account, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = 'Account update success'
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def email_unsubscribe_view(request, token):
	try:
		print(token)
		encMessage = urlsafe_base64_decode(token)

		print("encrypted string: ", encMessage)

		fernet = Fernet(settings.FERNET_KEY)
		decMessage = fernet.decrypt(encMessage).decode()

		print("decrypted string: ", decMessage)

		relativeLink = reverse('account:resubscribe-email', kwargs={'token': token})
		return render(request, 'sub_unsub_.html', {"text": "unsubscribed", "link_text": "Resubscribe", "link_url": relativeLink})
	except Exception as ex:
		print(str(ex))
		return render(request, 'admin/500.html')


def email_resubscribe_view(request, token):
	try:
		print(token)
		encMessage = urlsafe_base64_decode(token)

		print("encrypted string: ", encMessage)

		fernet = Fernet(settings.FERNET_KEY)
		decMessage = fernet.decrypt(encMessage).decode()

		print("decrypted string: ", decMessage)

		relativeLink = reverse('account:unsubscribe-email', kwargs={'token': token})

		return render(request, 'sub_unsub_.html', {"text": "re-subscribed", "link_text": "Unsubscribe", "link_url": relativeLink})
	except Exception as ex:
		print(str(ex))
		return render(request, 'admin/500.html')


def add_app_settings_to_user(user):


	## add default foods to user settings
	app_foods = appFood.objects.filter(enabled=True).values()
	for data in app_foods:
		del data["id"]
		del data["enabled"]
		data["user"] = user
		data["userCreated"] = False
	
		Food(**data).save()


	## add default aggravator to user settings
	app_aggravators = appAggravator.objects.filter(enabled=True).values()
	for data in app_aggravators:
		del data["id"]
		del data["enabled"]
		data["user"] = user
		data["userCreated"] = False
	
		Aggravator(**data).save()


	## add default symptoms to user settings
	app_symptoms = appSymptom.objects.filter(enabled=True).values()
	for data in app_symptoms:
		del data["id"]
		del data["enabled"]
		data["user"] = user
		data["userCreated"] = False
	
		Symptom(**data).save()


	## add default comorbidities to user settings
	app_comorbidities = appComorbidity.objects.filter(enabled=True).values()
	for data in app_comorbidities:
		del data["id"]
		del data["enabled"]
		data["user"] = user
		data["userCreated"] = False
	
		Comorbidity(**data).save()


	## add default dailyMedications to user settings
	app_daily_medications = appDailyMedication.objects.filter(enabled=True).values()
	for data in app_daily_medications:
		del data["id"]
		del data["enabled"]
		data["user"] = user
		data["userCreated"] = False
	
		DailyMedication(**data).save()


	## add default flareMedications to user settings
	app_flare_medications = appFlareMedication.objects.filter(enabled=True).values()
	for data in app_flare_medications:
		del data["id"]
		del data["enabled"]
		data["user"] = user
		data["userCreated"] = False
	
		FlareMedication(**data).save()

def add_user_to_narketing_email_list(user):
	try:
		MarketingEmail(email=user.email).save()
	except Exception as ex:
		print(ex)