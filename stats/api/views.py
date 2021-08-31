from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import json

from stats.models import (
	daily_report,
	daily_report_food,
	daily_report_aggravator,
	daily_report_symptom,
	daily_report_comorbidity,
	daily_report_flare_medication
)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_daily_report(request):

	user = request.user

	request_body = json.loads(request.body)

	for date, record in request_body.items():
		
		date = record['date']
		rating = record['rating']
		notes = record['notes']

		
		

		# deleting existing particular date records
		daily_report.objects.filter(user=user, date=date).delete()

		# adding general records

		general_record = daily_report(
			user=user,
			date=date,
			rating=rating,
			notes=notes,
		)

		general_record.save()
		
		print(general_record.id)

		# adding food in daily_report_food
		if "foods" in record and record["foods"]:
			for food in record["foods"]:
				food_id = food["id"]

				## https://stackoverflow.com/questions/4195242/django-model-object-with-foreign-key-creation
				daily_report_food.objects.create(daily_report_id_id=general_record.id, food_id_id=food_id)


		# adding aggravator in daily_report_aggravator
		if "aggravators" in record and record["aggravators"]:
			for aggravator in record["aggravators"]:
				aggravator_id = aggravator["id"]
				
				## https://stackoverflow.com/questions/4195242/django-model-object-with-foreign-key-creation
				daily_report_aggravator.objects.create(daily_report_id_id=general_record.id, aggravator_id_id=aggravator_id)


		# adding symptom in daily_report_symptom
		if "symptoms" in record and record["symptoms"]:
			for symptom in record["symptoms"]:
				symptom_id = symptom["id"]
				
				## https://stackoverflow.com/questions/4195242/django-model-object-with-foreign-key-creation
				daily_report_symptom.objects.create(daily_report_id_id=general_record.id, symptom_id_id=symptom_id)


		# adding comorbidity in daily_report_comorbidity
		if "comorbidities" in record and record["comorbidities"]:
			for comorbidity in record["comorbidities"]:
				comorbidity_id = comorbidity["id"]

				## https://stackoverflow.com/questions/4195242/django-model-object-with-foreign-key-creation
				daily_report_comorbidity.objects.create(daily_report_id_id=general_record.id, comorbidity_id_id=comorbidity_id)


		# adding flare medication in daily_report_flare_medication
		if "flareMedications" in record and record["flareMedications"]:
			for flareMedication in record["flareMedications"]:
				flare_medication_id = flareMedication["id"]
				pills = flareMedication.pop("pills", None)
			
				## https://stackoverflow.com/questions/4195242/django-model-object-with-foreign-key-creation
				daily_report_flare_medication.objects.create(daily_report_id_id=general_record.id,
															flare_medication_id_id=flare_medication_id,
															pills=pills)



				


	return Response(data={}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def get_daily_report(request):

	user = request.user

	request_body = json.loads(request.body)

	startDate = request_body['startDate'] if "startDate" in request_body and request_body["startDate"] else ""
	endDate = request_body['endDate'] if "endDate" in request_body and request_body["startDate"] else ""

	if not startDate or not endDate:
			return Response(data={"Response": "startDate or endDate not provided"}, status = status.HTTP_400_BAD_REQUEST)

	result = {}
	try:
		record = daily_report.objects.filter(user=user, date=startDate).values()[0]
		print(record)
		result[startDate] = record
	except Exception as ex:
		return Response(data={}, status = status.HTTP_200_OK)

	# get foods for a specific date
	foodss = daily_report_food.objects.filter(
												daily_report_id= record["id"], 
												food_id__selected=True,
												food_id__user = user).select_related('food_id')
	
	if foodss:
		result[startDate]["foods"] = []
		for food in foodss:
			temp = food.food_id.__dict__
			temp.pop('_state', None)
			result[startDate]["foods"].append(temp)


	# get aggravators for a specific date
	aggravatorss = daily_report_aggravator.objects.filter(
												daily_report_id= record["id"], 
												aggravator_id__selected=True,
												aggravator_id__user = user).select_related('aggravator_id')
	
	if aggravatorss:
		result[startDate]["aggravators"] = []
		for aggravator in aggravatorss:
			temp = aggravator.aggravator_id.__dict__
			temp.pop('_state', None)
			result[startDate]["aggravators"].append(temp)


	# get symptoms for a specific date
	symptomss = daily_report_symptom.objects.filter(
												daily_report_id= record["id"], 
												symptom_id__selected=True,
												symptom_id__user = user).select_related('symptom_id')
	
	if symptomss:
		result[startDate]["symptoms"] = []
		for symptom in symptomss:
			temp = symptom.symptom_id.__dict__
			temp.pop('_state', None)
			result[startDate]["symptoms"].append(temp)


	# get comorbiditys for a specific date
	comorbidityss = daily_report_comorbidity.objects.filter(
												daily_report_id= record["id"], 
												comorbidity_id__selected=True,
												comorbidity_id__user = user).select_related('comorbidity_id')
	
	if comorbidityss:
		result[startDate]["comorbidities"] = []
		for comorbidity in comorbidityss:
			temp = comorbidity.comorbidity_id.__dict__
			temp.pop('_state', None)
			result[startDate]["comorbidities"].append(temp)

	# get flare medications for a specific date
	flareMedicationss = daily_report_flare_medication.objects.filter(
												daily_report_id= record["id"], 
												flare_medication_id__selected=True,
												flare_medication_id__user = user).select_related('flare_medication_id')
	

	
	if flareMedicationss:
		result[startDate]["flareMedications"] = []
		for flareMedications in flareMedicationss:
			temp = flareMedications.flare_medication_id.__dict__
			temp.pop('_state', None)
			temp["pills"] = flareMedications.pills
			result[startDate]["flareMedications"].append(temp)
	
	
	return Response(data=result, status = status.HTTP_200_OK)

