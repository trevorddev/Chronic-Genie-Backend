from rest_framework.response import Response
from rest_framework import status


from component.models import FlareMedication
from component.api.serializers import FlareMedicationSerializer



def create(request):
	user = request.user
	data = request.data
	data['user'] = user.pk
	serializer = FlareMedicationSerializer(data=data)

	data = {}
	if serializer.is_valid():
		flareMedication = serializer.save()
		data['response'] = "success"
		return Response(data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_all(request):
	user = request.user
	try:
		flareMedication = FlareMedication.objects.filter(user=user)
	except FlareMedication.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	
	serializer = FlareMedicationSerializer(flareMedication, many=True)
	return Response(serializer.data)


def retrieve(request, pk):
	try:
		flareMedication = FlareMedication.objects.get(id=pk)
	except FlareMedication.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	user = request.user
	if flareMedication.user != user:
		return Response({'response':"You don't have permission to get that."}, status=status.HTTP_401_UNAUTHORIZED) 

	
	serializer = FlareMedicationSerializer(flareMedication)
	return Response(serializer.data)


def update(request, pk):
	try:
		flareMedication = FlareMedication.objects.get(id=pk)
	except FlareMedication.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	user = request.user
	if flareMedication.user != user:
		return Response({'response':"You don't have permission to edit that."}, status=status.HTTP_401_UNAUTHORIZED) 

	serializer = FlareMedicationSerializer(flareMedication, data=request.data, partial=True)
	if serializer.is_valid():
		flareMedication = serializer.save()
		return Response(serializer.data)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def delete(request, pk):
	try:
		flareMedication = FlareMedication.objects.get(id=pk)
	except FlareMedication.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	user = request.user
	if flareMedication.user != user:
		return Response({'response':"You don't have permission to delete that."}, status=status.HTTP_401_UNAUTHORIZED) 


	operation = flareMedication.delete()
	data = {}
	if operation:
		data['response'] = "success"
	return Response(data=data, status = status.HTTP_200_OK)