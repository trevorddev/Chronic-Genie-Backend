from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
import datetime
from datetime import datetime, timedelta, date

from rest_framework import status
import json, math, time, csv

from sql_utils import query_ReturnRow
from stats.models import (
	daily_report,
	daily_report_food,
	daily_report_aggravator,
	daily_report_symptom,
	daily_report_comorbidity,
	daily_report_flare_medication,
	daily_report_daily_medication
)

def month_converter(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months[month-1]

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_daily_report(request):

	user = request.user

	request_body = json.loads(request.body)

	for date, record in request_body.items():
		
		# deleting existing particular date records
		daily_report.objects.filter(user=user, date=date).delete()
		if not record:
			continue

		date = record['date']
		rating = record['rating']
		notes = record['notes']


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
				rating = symptom.pop("rating", 0)
				times = symptom.pop("times", [])
				if type(times) is not list:
					times = []

				## https://stackoverflow.com/questions/4195242/django-model-object-with-foreign-key-creation
				daily_report_symptom.objects.create(daily_report_id_id=general_record.id, 
													symptom_id_id=symptom_id,
													rating=rating,
													times=json.dumps(times))


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


		# adding flare medication in daily_report_daily_medication
		if "dailyMedications" in record and record["dailyMedications"]:
			for dailyMedication in record["dailyMedications"]:
				daily_medication_id = dailyMedication["id"]
				times = dailyMedication.pop("times", [])
				if type(times) is not list:
					times = []
				## https://stackoverflow.com/questions/4195242/django-model-object-with-foreign-key-creation
				daily_report_daily_medication.objects.create(daily_report_id_id=general_record.id,
															daily_medication_id_id=daily_medication_id,
															times=json.dumps(times))



				


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
		records = daily_report.objects.filter(user=user, date__range=(startDate, endDate)).order_by('date').values()
		
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
				temp["rating"] = symptom.rating
				try:
					temp["times"] = json.loads(symptom.times)
				except:
					temp["times"] = []
				
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
		
		# get daily medications for a specific date
		dailyMedicationss = daily_report_daily_medication.objects.filter(
													daily_report_id= record["id"], 
													daily_medication_id__selected=True,
													daily_medication_id__user = user).select_related('daily_medication_id')
		

		
		if dailyMedicationss:
			result[date]["dailyMedications"] = []
			for dailyMedications in dailyMedicationss:
				temp = dailyMedications.daily_medication_id.__dict__
				temp.pop('_state', None)
				temp["times"] = json.loads(dailyMedications.times)
				try:
					temp["times"] = temp["times"] = json.loads(dailyMedications.times)
				except:
					temp["times"] = []
				result[date]["dailyMedications"].append(temp)
		
		
	return Response(data=result, status = status.HTTP_200_OK)
@api_view(['GET','POST'])
@permission_classes(())
def customized_search(request):
	
	if request.method == 'GET':
		return render(request, 'filter.html', {})
	
	request_body = json.loads(request.body)

	filters = request_body['filters'] if "filters" in request_body and request_body["filters"] else {}
	page_number = request_body["page_number"] if "page_number" in request_body and request_body["page_number"] else 1 
	page_size = request_body["page_size"] if "page_size" in request_body and request_body["page_size"] else 1 
	
	page_size = 1000

	is_export = request_body["is_export"] if "is_export" in request_body else False

	if not filters:
		return Response(data={"Response": {}}, status = status.HTTP_200_OK)
   
	limit = (page_number - 1) * page_size


	selected_symptoms = filters['selected_symptoms'] if "selected_symptoms" in filters and filters["selected_symptoms"] else []
	recorded_symptoms = filters['recorded_symptoms'] if "recorded_symptoms" in filters and filters["recorded_symptoms"] else {}
	medical_conditions = filters['medical_conditions'] if "medical_conditions" in filters and filters["medical_conditions"] else []
	daily_medication = filters['daily_medications'] if "daily_medications" in filters and filters["daily_medications"] else {}
	
	master_query = []
	# master_query_cond = []

	if selected_symptoms:
		sub_query = '''
						select 1 from user_account ua 
						join component_symptom cs on (cs.user_id = ua.id)
						where ua.id = m.id and cs.selected = TRUE and ({})
					'''
		conditions = []
		for symptom in selected_symptoms:
			conditions.append("cs.name like '%{}%'".format(symptom))
		
		sub_query = sub_query.format(" and ".join(conditions))
		# master_query_cond.append(" cs.selected = TRUE ")
		# master_query_cond.append(" (" + " or ".join(conditions) + ")")
		master_query.append(" EXISTS ( " + sub_query + " ) ")

	if recorded_symptoms:
		symptoms = recorded_symptoms['symptoms'] if "symptoms" in recorded_symptoms and recorded_symptoms["symptoms"] else []
		start_date = recorded_symptoms['start_date'] if "start_date" in recorded_symptoms and recorded_symptoms["start_date"] else ""
		end_date = recorded_symptoms['end_date'] if "end_date" in recorded_symptoms and recorded_symptoms["end_date"] else ""

		if symptoms:
			sub_query = '''
							select 1 from user_account ua 
							join stats_daily_report sdr on (sdr.user_id = ua.id)
							join stats_daily_report_symptom sdrs on (sdrs.daily_report_id_id = sdr.id)
							join component_symptom cs on (cs.id = sdrs.symptom_id_id)
							where ua.id = m.id and 1=1
						'''
			conditions = []

			if symptoms:
				for symptom in symptoms:
					conditions.append("cs.name like '%{}%'".format(symptom))
				
				sub_query += " and (" + " and ".join(conditions) + ")"
				# master_query_cond.append(" (" + " or ".join(conditions) + ")")

			if start_date and end_date:
				sub_query += f" and (sdr.date BETWEEN '{start_date}' and '{end_date}')"
				# master_query_cond.append(f" (sdr.date BETWEEN '{start_date}' and '{end_date}')")
			master_query.append(" EXISTS ( " + sub_query + " ) ")

	if daily_medication:
		medicines = daily_medication['medicines'] if "medicines" in daily_medication and daily_medication["medicines"] else []
		start_date = daily_medication['start_date'] if "start_date" in daily_medication and daily_medication["start_date"] else ""
		end_date = daily_medication['end_date'] if "end_date" in daily_medication and daily_medication["end_date"] else ""

		if medicines:
			sub_query = '''
							select 1 from user_account ua 
							join component_dailymedication cd on (cd.user_id = ua.id)
							where ua.id = m.id and cd.selected = TRUE and 1=1
						'''
			conditions = []

			
			for medicine in medicines:
				conditions.append("cd.name like '%{}%'".format(medicine))
			
			sub_query += " and (" + " and ".join(conditions) + ")"

			if start_date:
				sub_query += f" and (cd.startDate = '{start_date}')"
			
			if end_date:
				sub_query += f" and (cd.endDate = '{end_date}')"

			master_query.append(" EXISTS ( " + sub_query + " ) ")
	
	if medical_conditions:
		sub_query = '''
						select 1 from user_account ua 
						where ua.id = m.id and 1 = 1 and ({})
					'''
		conditions = []
		for mc in medical_conditions:
			conditions.append("ua.medical_conditions like '%{}%'".format(mc))
		
		sub_query = sub_query.format(" and ".join(conditions))
		# master_query_cond.append(" (" + " or ".join(conditions) + ")")
	
		master_query.append(" EXISTS ( " + sub_query + " ) ")

	# if master_query_cond:
	# 	print("here")
	# 	print(" and ".join(master_query_cond))
	sql = (" AND ").join(master_query)

	if not sql:
		sql = " EXISTS ( select ua.id, ua.email, ua.first_name, ua.date_of_birth, ua.gender, ua.date_joined, ua.last_login from user_account ua  ) "
		
	if is_export:
		pass
	
	filtered_query = f'''
			SELECT m.id, m.email, m.first_name, m.date_of_birth, m.gender, m.date_joined, m.last_login
    		FROM user_account m
			WHERE
				{sql}
				
			'''
	
	if not is_export:
		filtered_query += f'LIMIT {page_size} offset {limit}'

	print(filtered_query)
	result = query_ReturnRow(filtered_query, None, False, True)

	if is_export:
		pass
		response = HttpResponse(content_type='application/force-downloa')
		response['Content-Disposition'] = 'attachment; filename=user_dashboard.csv'
		writer = csv.writer(response)

		
		writer.writerow(["Email", "First Name", "D.O.B", "Gender", "Date Joined", "Last Login"])
		for s in result:
			writer.writerow([s['email'], s['first_name'], s['date_of_birth'], s['gender'], s['date_joined'], s['last_login']])
		return response

	filter_count_query = f'''
			SELECT count(*) as total FROM user_account m
			WHERE
				{sql}
			'''
	
	filter_count = query_ReturnRow(filter_count_query, None, False, True)[0]["total"]


	total_count_query = f'''
			select count(*) as total from user_account ua
			'''
	
	total_count = query_ReturnRow(total_count_query, None, False, True)[0]["total"]


	response = {
		"page_number": page_number,
		"page_size": page_size,
		"total_count": total_count,
		"filter_count": filter_count,
		"total_pages": math.ceil(filter_count / page_size),
		"result": result
	}

	return Response(data=response, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes(())
def user_dashboard(request):
	
	if request.method == 'GET':
		return render(request, 'user_summary_dashboard.html', {})
	


@api_view(['POST'])
@permission_classes(())
def users_summary(request):

	ini_date_for_now = datetime.now().date()

	one_week_before_date = (ini_date_for_now + timedelta(days = -7)).strftime("%Y-%m-%d")
	one_month_before_date = (ini_date_for_now + timedelta(days = -30)).strftime("%Y-%m-%d")
	one_year_before_date = (ini_date_for_now + timedelta(days = -365)).strftime("%Y-%m-%d")
	five_year_before_date = (ini_date_for_now + timedelta(days = -1825)).strftime("%Y-%m-%d")  
	
	## getting total count
	query = f'''
			SELECT count(*) as count from user_account ua 
	'''

	total_count = query_ReturnRow(query, None, False, True)[0]["count"]

	## getting count of users in last 7 days
	query = f'''
			SELECT DATE(date_joined) as date, count(*) as count from user_account ua 
			where (DATE(date_joined) > "{one_week_before_date}" and DATE(date_joined) <= "{ini_date_for_now}")
			GROUP BY date_joined
			order by date
	'''
	weekly_result = query_ReturnRow(query, None, False, True)

	
	## getting count of users in last 30 days
	query = f'''
			SELECT DATE(date_joined) as date, count(*) as count from user_account ua 
			where (DATE(date_joined) > "{one_month_before_date}" and DATE(date_joined) <= "{ini_date_for_now}")
			GROUP BY date_joined
			order by date
	'''
	monthly_result = query_ReturnRow(query, None, False, True)

	## getting count of users in last 12 months
	query = f'''
			SELECT YEAR(date_joined) as y, MONTH(date_joined) as m, count(*) as count from user_account ua  
			where (DATE(date_joined) > "{one_year_before_date}" and DATE(date_joined) <= "{ini_date_for_now}")
			GROUP BY Year(date_joined), MONTH(date_joined)
			order by y, m
	'''
	yearly_result = query_ReturnRow(query, None, False, True)


	## getting count of users in last 5 years
	query = f'''
			SELECT YEAR(date_joined) as y, count(*) as count from user_account ua  
			where (DATE(date_joined) > "{five_year_before_date}" and DATE(date_joined) <= "{ini_date_for_now}")
			GROUP BY Year(date_joined)
			order by y
	'''
	five_year_result = query_ReturnRow(query, None, False, True)


	# add date which is not returned by query, setting count to 0 for that date
	modified_weekly_result = []
	base = date.today()
	date_list = [base -timedelta(days=x) for x in range(7)]
	for _date in date_list[::-1]:
		record_found = False
		for i in weekly_result:
			if _date == i['date']:
				modified_weekly_result.append(i)
				record_found = True
				break
		if not record_found:
			modified_weekly_result.append(
				{
					"date": _date,
					"count": 0
				}
			)


	# add date which is not returned by query, setting count to 0 for that date
	modified_monthly_result = []
	base = date.today()
	date_list = [base -timedelta(days=x) for x in range(30)]
	for _date in date_list[::-1]:
		record_found = False
		for i in monthly_result:
			if _date == i['date']:
				modified_monthly_result.append(i)
				record_found = True
				break
		if not record_found:
			modified_monthly_result.append(
				{
					"date": _date,
					"count": 0
				}
			)
	
	# get list of last 12 months
	now = time.localtime()
	last_12_months = [time.localtime(time.mktime((now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)))[:2] for n in range(12)]
	# add date which is not returned by query, setting count to 0 for that date
	modified_yearly_result = []
	for y, m in last_12_months[::-1]:
		record_found = False
		for i in yearly_result:
			if y == i['y'] and m == i['m']:
				modified_yearly_result.append({
						'date': month_converter(m) + ' ' + str(y),
						'count': i['count']
					}
				)
				record_found = True
				break
		if not record_found:
			modified_yearly_result.append({
						'date': month_converter(m) + ' ' + str(y),
						'count': 0
					}
			)


	# get list of last 5 years
	now = time.localtime()
	last_5_years = [time.localtime(time.mktime((now.tm_year - n, 1, 1, 0, 0, 0, 0, 0, 0)))[:1] for n in range(5)]
	# add date which is not returned by query, setting count to 0 for that date
	modified_five_year_result = []
	for y, in last_5_years[::-1]:
		record_found = False
		for i in five_year_result:
			if y == i['y']:
				modified_five_year_result.append({
						'date': str(y),
						'count': i['count']
					}
				)
				record_found = True
				break
		if not record_found:
			modified_five_year_result.append({
						'date': str(y),
						'count': 0
					}
			)
	response = {
		"Total": total_count,
		"weekly_count": sum(item['count'] for item in modified_weekly_result),
		"monthly_count": sum(item['count'] for item in modified_monthly_result),
		"yearly_count": sum(item['count'] for item in modified_yearly_result),
		"all_count": sum(item['count'] for item in modified_five_year_result), 
		"Weekly": modified_weekly_result,
		"Monthly": modified_monthly_result,
		"Yearly": modified_yearly_result,
		"all": modified_five_year_result
	}


	return Response(data=response, status=status.HTTP_200_OK)

