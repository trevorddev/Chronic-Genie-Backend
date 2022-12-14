
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from component.models import (
	Aggravator, 
	Comorbidity, 
	DailyMedication, 
	FlareMedication, 
	Food, 
	Symptom,
)

from adminPanel.models import (
    AppSettings
)
from .modules import (
    food_crud, 
    aggravator_crud, 
    symptom_crud, 
    comorbidity_crud, 
    dailyMedication_crud, 
    flareMedication_crud,
)

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

	selectedAggravators = Aggravator.objects.filter(user=user, selected=True).values()
	response["aggravator"] = selectedAggravators

	selectedSymptoms = Symptom.objects.filter(user=user, selected=True).values()
	response["symptom"] = selectedSymptoms

	selectedComorbiditys = Comorbidity.objects.filter(user=user, selected=True).values()
	response["comorbidity"] = selectedComorbiditys

	selectedFlareMedication = FlareMedication.objects.filter(user=user, selected=True).values()
	response["flareMedication"] = selectedFlareMedication

	selectedDailyMedication = DailyMedication.objects.filter(user=user, selected=True).values()
	response["dailyMedication"] = selectedDailyMedication


	# print(response)

	return Response(data=response, status = status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT'])
@permission_classes((IsAuthenticated, ))
def ListCreateView(request, component):
	
    if component == "food":
        if request.method == 'POST':
            return food_crud.create(request)
	
        if request.method == 'GET':
            return food_crud.get_all(request)

        # bulk update
        if request.method == 'PUT':  
            records = request.data
            for record in records:
                request._full_data = record
                try:
                    pk = record["id"]
                except:
                    food_crud.create(request)
                    continue
                response = food_crud.update(request, pk)
                if response.status_code == 404:
                    # if record not found then create it
                    food_crud.create(request)
            return Response(records, status=status.HTTP_200_OK) 

    if component == "aggravator":
        if request.method == 'POST':
            return aggravator_crud.create(request)
	
        if request.method == 'GET':
            return aggravator_crud.get_all(request)

        # bulk update
        if request.method == 'PUT':  
            records = request.data
            for record in records:
                request._full_data = record
                try:
                    pk = record["id"]
                except:
                    aggravator_crud.create(request)
                    continue
                response = aggravator_crud.update(request, pk)
                if response.status_code == 404:
                    # if record not found then create it
                    aggravator_crud.create(request)
            return Response(records, status=status.HTTP_200_OK) 
    
    if component == "symptom":
        if request.method == 'POST':
            return symptom_crud.create(request)
	
        if request.method == 'GET':
            return symptom_crud.get_all(request)

        # bulk update
        if request.method == 'PUT':  
            records = request.data
            for record in records:
                request._full_data = record
                try:
                    pk = record["id"]
                except:
                    symptom_crud.create(request)
                    continue
                response = symptom_crud.update(request, pk)
                if response.status_code == 404:
                    # if record not found then create it
                    symptom_crud.create(request)
            return Response(records, status=status.HTTP_200_OK)

    if component == "comorbidity":
        if request.method == 'POST':
            return comorbidity_crud.create(request)
	
        if request.method == 'GET':
            return comorbidity_crud.get_all(request)
        
        # bulk update
        if request.method == 'PUT':  
            records = request.data
            for record in records:
                request._full_data = record
                try:
                    pk = record["id"]
                except:
                    comorbidity_crud.create(request)
                    continue
                response = comorbidity_crud.update(request, pk)
                if response.status_code == 404:
                    # if record not found then create it
                    comorbidity_crud.create(request)
            return Response(records, status=status.HTTP_200_OK)


    if component == "dailyMedication":
        if request.method == 'POST':
            return dailyMedication_crud.create(request)
	
        if request.method == 'GET':
            return dailyMedication_crud.get_all(request)

        # bulk update
        if request.method == 'PUT':  
            records = request.data
            for record in records:
                request._full_data = record
                try:
                    pk = record["id"]
                except:
                    dailyMedication_crud.create(request)
                    continue
                response = dailyMedication_crud.update(request, pk)
                if response.status_code == 404:
                    # if record not found then create it
                    dailyMedication_crud.create(request)
            return Response(records, status=status.HTTP_200_OK)

    if component == "flareMedication":
        if request.method == 'POST':
            return flareMedication_crud.create(request)
	
        if request.method == 'GET':
            return flareMedication_crud.get_all(request)

        # bulk update
        if request.method == 'PUT':  
            records = request.data
            for record in records:
                request._full_data = record
                try:
                    pk = record["id"]
                except:
                    flareMedication_crud.create(request)
                    continue
                response = flareMedication_crud.update(request, pk)
                if response.status_code == 404:
                    # if record not found then create it
                    flareMedication_crud.create(request)
            return Response(records, status=status.HTTP_200_OK)
	
@api_view(['GET', 'PUT', 'DELETE' ])
@permission_classes((IsAuthenticated, ))
def RetrieveUpdateDestroyView(request, component, pk):

    if component == "food":
        if request.method == 'GET':
            return food_crud.retrieve(request, pk)
	
        if request.method == 'PUT':
            return food_crud.update(request, pk)

        if request.method == 'DELETE':
            return food_crud.delete(request, pk)


    if component == "aggravator":
        if request.method == 'GET':
            return aggravator_crud.retrieve(request, pk)
	
        if request.method == 'PUT':
            return aggravator_crud.update(request, pk)

        if request.method == 'DELETE':
            return aggravator_crud.delete(request, pk)


    if component == "symptom":
        if request.method == 'GET':
            return symptom_crud.retrieve(request, pk)
	
        if request.method == 'PUT':
            return symptom_crud.update(request, pk)

        if request.method == 'DELETE':
            return symptom_crud.delete(request, pk)


    if component == "comorbidity":
        if request.method == 'GET':
            return comorbidity_crud.retrieve(request, pk)
	
        if request.method == 'PUT':
            return comorbidity_crud.update(request, pk)

        if request.method == 'DELETE':
            return comorbidity_crud.delete(request, pk)


    if component == "dailyMedication":
        if request.method == 'GET':
            return dailyMedication_crud.retrieve(request, pk)
	
        if request.method == 'PUT':
            return dailyMedication_crud.update(request, pk)

        if request.method == 'DELETE':
            return dailyMedication_crud.delete(request, pk)


    if component == "flareMedication":
        if request.method == 'GET':
            return flareMedication_crud.retrieve(request, pk)
	
        if request.method == 'PUT':
            return flareMedication_crud.update(request, pk)

        if request.method == 'DELETE':
            return flareMedication_crud.delete(request, pk)





