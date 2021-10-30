from rest_framework import serializers
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed
import json

from user.models import Account


# class LoginSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Account
# 		fields = ['email', 'password',]

# 		extra_kwargs = {'password': {'write_only': True}}

# 	def validate(self, data):
# 		password = data.get('password')
# 		email = data.get('email')


class RegistrationSerializer(serializers.ModelSerializer):

	password2 				= serializers.CharField(style={'input_type': 'password'}, write_only=True)
	main_conditions         = serializers.ListField(allow_empty=True)
	medical_conditions      = serializers.ListField(allow_empty=True)
	
	class Meta:
		model = Account
		fields = ['email', 'first_name', 'date_of_birth', 'gender', 'password', 'password2', 'race', 'didOnboarding', 'main_conditions', 'medical_conditions', "privacy_preference"]
		extra_kwargs = {
				'password': {'write_only': True},
                'didOnboarding': {'required': False, 'default': False},
		}	


	def	save(self):

		account = Account(
					email=self.validated_data['email'],
					first_name=self.validated_data['first_name'],
                    date_of_birth=self.validated_data['date_of_birth'],
                    gender=self.validated_data['gender'],
                    race=self.validated_data['race'],
                    didOnboarding=self.validated_data['didOnboarding'],
					main_conditions=json.dumps(self.validated_data['main_conditions']),
					medical_conditions=json.dumps(self.validated_data['medical_conditions']),
					privacy_preference=self.validated_data['privacy_preference']
				)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		account.set_password(password)
		account.save()
		return account


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']



class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)





class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class AccountPropertiesSerializer(serializers.ModelSerializer):

	main_conditions         = serializers.ListField(allow_empty=True)
	medical_conditions      = serializers.ListField(allow_empty=True)

	class Meta:
		model = Account
		extra_kwargs = {'password': {'write_only': True, "allow_blank": True, "required": False, "default": ""}}
		fields = ['pk', 'email', 'password', 'first_name', 'date_of_birth', 'gender', 'race', 'main_conditions', 'medical_conditions', 'privacy_preference', 'didOnboarding']


	def to_representation(self, instance):
		"""Convert string to array """
		ret = super().to_representation(instance)

		ret['main_conditions'] = json.loads(instance.main_conditions)
		ret['medical_conditions'] = json.loads(instance.medical_conditions)
		return ret

	def create(self, validated_data):
		user = super().create(validated_data)
		user.set_password(validated_data['password'])
		user.save()
		return user

	def update(self, instance, validated_data):

		# removing password because we need to check whether is is empty or not and save the hash password
		password = validated_data.pop("password")

		# removing main_conditions and medical_conditions because we need to convert to convert array to string first
		validated_data["main_conditions"] = json.dumps(validated_data["main_conditions"])
		validated_data["medical_conditions"] = json.dumps(validated_data["medical_conditions"])

		user = super().update(instance, validated_data)
		try:
			if password:
				# saving hash password
				user.set_password(password)
				user.save()
		except KeyError:
			pass
		return user


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        
        fields = '__all__'