from rest_framework.response import Response
from rest_framework import status


from component.models import Aggravator
from component.api.serializers import AggravatorSerializer



def create(request):
	user = request.user
	data = request.data
	data['user'] = user.pk
	serializer = AggravatorSerializer(data=data)

	data = {}
	if serializer.is_valid():
		aggravator = serializer.save()
		data['response'] = "success"
		return Response(data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_all(request):
	user = request.user
	try:
		aggravator = Aggravator.objects.filter(user=user)
	except Aggravator.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	
	serializer = AggravatorSerializer(aggravator, many=True)
	return Response(serializer.data)


def retrieve(request, pk):
	try:
		aggravator = Aggravator.objects.get(id=pk)
	except Aggravator.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	user = request.user
	if aggravator.user != user:
		return Response({'response':"You don't have permission to get that."}, status=status.HTTP_401_UNAUTHORIZED) 

	
	serializer = AggravatorSerializer(aggravator)
	return Response(serializer.data)


def update(request, pk):
	try:
		aggravator = Aggravator.objects.get(id=pk)
	except Aggravator.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	user = request.user
	if aggravator.user != user:
		return Response({'response':"You don't have permission to edit that."}, status=status.HTTP_401_UNAUTHORIZED) 

	serializer = AggravatorSerializer(aggravator, data=request.data, partial=True)
	if serializer.is_valid():
		aggravator = serializer.save()
		return Response(serializer.data)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def delete(request, pk):
	try:
		aggravator = Aggravator.objects.get(id=pk)
	except Aggravator.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	user = request.user
	if aggravator.user != user:
		return Response({'response':"You don't have permission to delete that."}, status=status.HTTP_401_UNAUTHORIZED) 


	operation = aggravator.delete()
	data = {}
	if operation:
		data['response'] = "success"
	return Response(data=data, status = status.HTTP_200_OK)