
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from component.models import AppSettings, Food
from component.api.serializers import FoodSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getAppSettings(request):
	
	user = request.user

	appsettings = AppSettings.objects.last()
	response = appsettings.__dict__

	# removing unwanted field
	del response["_state"]

	# get selected foods
	selectedFoods = Food.objects.filter(user=user, selected=True).values()

	response["food"] = selectedFoods
	# print(response)

	return Response(data=response, status = status.HTTP_200_OK)

# class FoodCreateRetrieve(generics.ListCreateAPIView):
    
# 	queryset = Food.objects.all()
# 	serializer_class = FoodSerializer

# 	def get_queryset(self):
# 		user = self.request.user
# 		return Food.objects.filter(user=user)

# 	def perform_create(self, serializer):
# 		serializer.save(user=self.request.user, )

# 	def perform_update(self, serializer):
# 		serializer.save(user=self.request.user)



# class FoodAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Food.objects.all()
#     serializer_class = FoodSerializer


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def api_list_create_food_view(request):
	
	user = request.user
	
	if request.method == 'GET':
		try:
			food = Food.objects.filter(user=user)
		except Food.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		serializer = FoodSerializer(food, many=True)
		return Response(serializer.data)

	if request.method == 'POST':

		data = request.data
		data['user'] = user.pk
		serializer = FoodSerializer(data=data)

		data = {}
		if serializer.is_valid():
			food = serializer.save()
			data['response'] = "success"
			return Response(data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FoodRetrieveAll(generics.ListAPIView):
    
	queryset = Food.objects.all()
	serializer_class = FoodSerializer

	def get_queryset(self):
		user = self.request.user
		return Food.objects.filter(user=user)



@api_view(['GET', 'PUT', 'DELETE' ])
@permission_classes((IsAuthenticated, ))
def api_detail_update_delete_food_view(request, pk):

	try:
		food = Food.objects.get(id=pk)
	except Food.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	user = request.user
	if food.user != user:
		return Response({'response':"You don't have permission to edit that."}, status=status.HTTP_401_UNAUTHORIZED) 

	if request.method == 'GET':
		serializer = FoodSerializer(food)
		return Response(serializer.data)

	if request.method == 'PUT':
		serializer = FoodSerializer(food, data=request.data, partial=True)
		if serializer.is_valid():
			food = serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	if request.method == 'DELETE':
		operation = food.delete()
		data = {}
		if operation:
			data['response'] = "success"
		return Response(data=data, status = status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# def api_create_food_view(request):
# 	print("here")
# 	if request.method == 'POST':

# 		data = request.data
# 		data['user'] = request.user.pk
# 		serializer = FoodSerializer(data=data)

# 		data = {}
# 		if serializer.is_valid():
# 			food = serializer.save()
# 			data['response'] = "success"
# 			return Response(data, status=status.HTTP_201_CREATED)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




