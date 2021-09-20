from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render

from rest_framework import status
import json, math

from sql_utils import query_ReturnRow
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
	endDate = request_body['endDate'] if "endDate" in request_body and request_body["endDate"] else ""

	if not startDate or not endDate:
			return Response(data={"Response": "startDate or endDate not provided"}, status = status.HTTP_400_BAD_REQUEST)

	result = {}
	try:
		records = daily_report.objects.filter(user=user, date__range=(startDate, endDate)).values()
		
	except Exception as ex:
		print(str(ex))
		return Response(data={}, status = status.HTTP_200_OK)

	for record in records:
		date = str(record["date"])
		result[date] = record


		# get foods for a specific date
		foodss = daily_report_food.objects.filter(
													daily_report_id= record["id"], 
													food_id__selected=True,
													food_id__user = user).select_related('food_id')
		
		if foodss:
			result[date]["foods"] = []
			for food in foodss:
				temp = food.food_id.__dict__
				temp.pop('_state', None)
				result[date]["foods"].append(temp)


		# get aggravators for a specific date
		aggravatorss = daily_report_aggravator.objects.filter(
													daily_report_id= record["id"], 
													aggravator_id__selected=True,
													aggravator_id__user = user).select_related('aggravator_id')
		
		if aggravatorss:
			result[date]["aggravators"] = []
			for aggravator in aggravatorss:
				temp = aggravator.aggravator_id.__dict__
				temp.pop('_state', None)
				result[date]["aggravators"].append(temp)


		# get symptoms for a specific date
		symptomss = daily_report_symptom.objects.filter(
													daily_report_id= record["id"], 
													symptom_id__selected=True,
													symptom_id__user = user).select_related('symptom_id')
		
		if symptomss:
			result[date]["symptoms"] = []
			for symptom in symptomss:
				temp = symptom.symptom_id.__dict__
				temp.pop('_state', None)
				result[date]["symptoms"].append(temp)


		# get comorbiditys for a specific date
		comorbidityss = daily_report_comorbidity.objects.filter(
													daily_report_id= record["id"], 
													comorbidity_id__selected=True,
													comorbidity_id__user = user).select_related('comorbidity_id')
		
		if comorbidityss:
			result[date]["comorbidities"] = []
			for comorbidity in comorbidityss:
				temp = comorbidity.comorbidity_id.__dict__
				temp.pop('_state', None)
				result[date]["comorbidities"].append(temp)

		# get flare medications for a specific date
		flareMedicationss = daily_report_flare_medication.objects.filter(
													daily_report_id= record["id"], 
													flare_medication_id__selected=True,
													flare_medication_id__user = user).select_related('flare_medication_id')
		

		
		if flareMedicationss:
			result[date]["flareMedications"] = []
			for flareMedications in flareMedicationss:
				temp = flareMedications.flare_medication_id.__dict__
				temp.pop('_state', None)
				temp["pills"] = flareMedications.pills
				result[date]["flareMedications"].append(temp)
		
		
	return Response(data=result, status = status.HTTP_200_OK)
@api_view(['GET','POST'])
@permission_classes(())
def customized_search(request):
	
	if request.method == 'GET':
		return render(request, 'admin/filter.html', {"message": "Token Expires, try to generate token again"})
	
	request_body = json.loads(request.body)

	filters = request_body['filters'] if "filters" in request_body and request_body["filters"] else {}
	page_number = request_body["page_number"] if "page_number" in request_body and request_body["page_number"] else 1 
	page_size = request_body["page_size"] if "page_size" in request_body and request_body["page_size"] else 1 
	
	if not filters:
		return Response(data={"Response": {}}, status = status.HTTP_200_OK)
   
	limit = (page_number - 1) * page_size


	selected_symptoms = filters['selected_symptoms'] if "selected_symptoms" in filters and filters["selected_symptoms"] else []
	recorded_symptoms = filters['recorded_symptoms'] if "recorded_symptoms" in filters and filters["recorded_symptoms"] else {}
	medical_conditions = filters['medical_conditions'] if "medical_conditions" in filters and filters["medical_conditions"] else []

	master_query = []
	if selected_symptoms:
		sub_query = '''
						select ua.id, ua.email, ua.first_name, ua.date_of_birth, ua.gender from user_account ua 
						join component_symptom cs on (cs.user_id = ua.id)
						where cs.selected = TRUE and ({})
					'''
		conditions = []
		for symptom in selected_symptoms:
			conditions.append("cs.name like '%{}%'".format(symptom))
		
		sub_query = sub_query.format(" or ".join(conditions))
	
		master_query.append(sub_query)

	if recorded_symptoms:
		symptoms = recorded_symptoms['symptoms'] if "symptoms" in recorded_symptoms and recorded_symptoms["symptoms"] else []
		start_date = recorded_symptoms['start_date'] if "start_date" in recorded_symptoms and recorded_symptoms["start_date"] else ""
		end_date = recorded_symptoms['end_date'] if "end_date" in recorded_symptoms and recorded_symptoms["end_date"] else ""

		if symptoms or start_date or end_date:
			sub_query = '''
							select ua.id, ua.email, ua.first_name, ua.date_of_birth, ua.gender from user_account ua 
							join stats_daily_report sdr on (sdr.user_id = ua.id)
							join stats_daily_report_symptom sdrs on (sdrs.daily_report_id_id = sdr.id)
							join component_symptom cs on (cs.id = sdrs.symptom_id_id)
							where 1=1
						'''
			conditions = []

			if symptoms:
				for symptom in symptoms:
					conditions.append("cs.name like '%{}%'".format(symptom))
				
				sub_query += " and (" + " or ".join(conditions) + ")"

			if start_date and end_date:
				sub_query += f" and (sdr.date BETWEEN '{start_date}' and '{end_date}')"
			master_query.append(sub_query)
	
	if medical_conditions:
		sub_query = '''
						select ua.id, ua.email, ua.first_name, ua.date_of_birth, ua.gender from user_account ua 
						where 1 = 1 and ({})
					'''
		conditions = []
		for mc in medical_conditions:
			conditions.append("ua.medical_conditions like '%{}%'".format(mc))
		
		sub_query = sub_query.format(" or ".join(conditions))
	
		master_query.append(sub_query)


	sql = (" Union ").join(master_query)

	if not sql:
		response = {
			"total_pages": 0,
			"page_number": 0,
			"page_size": 0,
			"result": {}
		}
		return Response(data=response, status=status.HTTP_200_OK)

	
	filtered_query = f'''
			SELECT * FROM
				( 
					{sql}
				)
			query
			LIMIT {page_size} offset {limit}	
			'''
	
	print(filtered_query)
	result = query_ReturnRow(filtered_query, None, False, True)

	total_query = f'''
			SELECT count(*) as total FROM
				( 
					{sql}
				)
			query
			'''
	
	total_count = query_ReturnRow(total_query, None, False, True)[0]["total"]

	response = {
		"total_pages": math.ceil(total_count / page_size),
		"page_number": page_number,
		"page_size": page_size,
		"result": result
	}

	return Response(data=response, status=status.HTTP_200_OK)

