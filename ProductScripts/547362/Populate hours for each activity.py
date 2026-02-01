import math
from GS_Populate_Labour_WTW import populateWTW
from GS_CyberProductModule import CyberProduct
activity_container = Product.GetContainerByName('Activities')
network_level_container = Product.GetContainerByName('Network Level Container')
product_variables = SqlHelper.GetList("Select Variable, Value from CT_Product_Variables where Product = 'Cyber App Control'")
#declare and initialize product variables

var_pre_site_tech_prep_hrs = 0
var_fds_dds_documentation_hrs = 0
var_fat_report_hrs = 0
var_sat_fat_hrs = 0
var_sat_hrs = 0
var_customer_acceptance_familiarization_new_hrs = 0
var_customer_acceptance_familiarization_expansion_hrs = 0
var_cyber_coordination_pct = 0
var_serverinstalconfig_new_factor = 0
var_serverinstalconfig_expansion_factor = 0
var_protectedstasetupconfig_new_factor = 0
var_protectedstasetupconfig_expansion_factor = 0
var_protectedservsetupconfig_new_factor = 0
var_protectedservsetupconfig_expansion_factor = 0
var_expanssvrstnconfig_factor = 0
var_awlspecialpolicies_new_factor = 0
var_awlspecialpolicies_expansion_factor = 0

#read values for product variables from table

for product_variable in product_variables:
	if product_variable.Variable == 'Var_Pre_Site_Tech_Prep_Hrs':
		var_pre_site_tech_prep_hrs = float(product_variable.Value)
	elif product_variable.Variable == 'Var_FDS_DDS_Documentation_Hrs':
		var_fds_dds_documentation_hrs = float(product_variable.Value)
	elif product_variable.Variable == 'Var_FAT_Report_Hrs':
		var_fat_report_hrs  = float(product_variable.Value)
	elif product_variable.Variable == 'Var_SAT_FAT_Hrs':
		var_sat_fat_hrs  = float(product_variable.Value)
	elif product_variable.Variable == 'Var_SAT_Hrs':
		var_sat_hrs  = float(product_variable.Value)
	elif product_variable.Variable == 'Var_Customer_Acceptance_Familiarization_New_Hrs':
		var_customer_acceptance_familiarization_new_hrs  = float(product_variable.Value)
	elif product_variable.Variable == 'Var_Customer_Acceptance_Familiarization_Expansion_Hrs':
		var_customer_acceptance_familiarization_expansion_hrs  = float(product_variable.Value)
	elif product_variable.Variable == 'Var_Cyber_Coordination_Pct':
		var_cyber_coordination_pct  = float(product_variable.Value)
	elif product_variable.Variable == 'Var_ServerInstalConfig_New_Factor':
		var_serverinstalconfig_new_factor  = float(product_variable.Value)
	elif product_variable.Variable == 'Var_ServerInstalConfig_Expansion_Factor':
		var_serverinstalconfig_expansion_factor  = float(product_variable.Value)
	elif product_variable.Variable == 'Var_ProtectedStaSetupConfig_New_Factor':
		var_protectedstasetupconfig_new_factor  = float(product_variable.Value)
	elif product_variable.Variable == 'Var_ProtectedStaSetupConfig_Expansion_Factor':
		var_protectedstasetupconfig_expansion_factor  = float(product_variable.Value)
	elif product_variable.Variable == 'Var_ProtectedServSetupConfig_New_Factor':
		var_protectedservsetupconfig_new_factor  = float(product_variable.Value)
	elif product_variable.Variable == 'Var_ProtectedServSetupConfig_Expansion_Factor':
		var_protectedservsetupconfig_expansion_factor  = float(product_variable.Value)
	elif product_variable.Variable == 'Var_ExpansSvrStnConfig_Factor':
		var_expanssvrstnconfig_factor  = float(product_variable.Value)
	elif product_variable.Variable == 'Var_AWLSpecialPolicies_New_Factor':
		var_awlspecialpolicies_new_factor  = float(product_variable.Value)
	elif product_variable.Variable == 'Var_AWLSpecialPolicies_Expansion_Factor':
		var_awlspecialpolicies_expansion_factor  = float(product_variable.Value)

#declare and initialize Network Level variables

number_of_cyber_app_control_servers_L3_0 = 0
validated_stations_L3_0 = 0
validated_servers_L3_0 = 0
non_validated_stations_L3_0 = 0
non_validated_servers_L3_0 = 0
migrations_only_existing_server_and_station_clients_L3_0 = 0

number_of_cyber_app_control_servers_L3_5 = 0
validated_stations_L3_5 = 0
validated_servers_L3_5 = 0
non_validated_stations_L3_5 = 0
non_validated_servers_L3_5 = 0
migrations_only_existing_server_and_station_clients_L3_5 = 0

#read values for Network Level variables from respective container

for row in network_level_container.Rows:
	if row['Network Level'] == 'L3.0 Network':
		if row['Number of Cyber App Control Servers'] != '':
			number_of_cyber_app_control_servers_L3_0 = float(row['Number of Cyber App Control Servers'])
		if row['Validated Stations'] != '':
			validated_stations_L3_0 = float(row['Validated Stations'])
		if row['Validated Servers'] != '':
			validated_servers_L3_0 = float(row['Validated Servers'])
		if row['Non‐Validated Stations'] != '':
			non_validated_stations_L3_0 = float(row['Non‐Validated Stations'])
		if row['Non‐Validated Servers'] != '':
			non_validated_servers_L3_0 = float(row['Non‐Validated Servers'])
		if row['MIGRATIONS ONLY - Existing Server & Station Clients'] != '':
			migrations_only_existing_server_and_station_clients_L3_0 = float(row['MIGRATIONS ONLY - Existing Server & Station Clients'])
	elif row['Network Level'] == 'L3.5 Network':
		if row['Number of Cyber App Control Servers'] != '':
			number_of_cyber_app_control_servers_L3_5 = float(row['Number of Cyber App Control Servers'])
		if row['Validated Stations'] != '':
			validated_stations_L3_5 = float(row['Validated Stations'])
		if row['Validated Servers'] != '':
			validated_servers_L3_5 = float(row['Validated Servers'])
		if row['Non‐Validated Stations'] != '':
			non_validated_stations_L3_5 = float(row['Non‐Validated Stations'])
		if row['Non‐Validated Servers'] != '':
			non_validated_servers_L3_5 = float(row['Non‐Validated Servers'])
		if row['MIGRATIONS ONLY - Existing Server & Station Clients'] != '':
			migrations_only_existing_server_and_station_clients_L3_5 = float(row['MIGRATIONS ONLY - Existing Server & Station Clients'])

#declare and initialize activity hour variables, indices

a1_hours = 0
a2_hours = 0
a3_hours = 0
a4_hours = 0
a5_hours = 0
a6_hours = 0
a7_hours = 0
a8_hours = 0
a9_hours = 0
a10_hours = 0
a12_index = -1
row_index = -1

#declare and assign attribute variables 

attr_general_value = Product.Attr('General').GetValue()
attr_fat_report_required_value = Product.Attr('FAT Document Verification and Execution').GetValue()
attr_sat_report_required_value = Product.Attr('SAT Document Verification and Execution').GetValue()
attr_fds_dds_documentation_required_value = Product.Attr('FDS & DDS Documentation Required').GetValue()
attr_travel_time_value = Product.Attr('Travel Time').GetValue()

#calculate activity hours
if activity_container.Rows.Count>0:
	for row in activity_container.Rows:
		row_index = row_index + 1

		if row['Identifier'] == 'A1':
			row['Hours'] = str(int(var_pre_site_tech_prep_hrs))
			a1_hours = float(row['Hours'])
		elif row['Identifier'] == 'A2':
			if attr_general_value == 'New':
				row['Hours'] = str(int(math.ceil(var_serverinstalconfig_new_factor * (number_of_cyber_app_control_servers_L3_0 + number_of_cyber_app_control_servers_L3_5))))
			elif attr_general_value == 'Expansion':
				row['Hours'] = str(var_serverinstalconfig_expansion_factor * (number_of_cyber_app_control_servers_L3_0 + number_of_cyber_app_control_servers_L3_5))
			a2_hours = float(row['Hours'])
		elif row['Identifier'] == 'A3':
			sum_stations_servers_L3_0 = validated_stations_L3_0 + non_validated_stations_L3_0
			sum_stations_servers_L3_5 = validated_stations_L3_5 + non_validated_stations_L3_5

			if attr_general_value == 'New':
				row['Hours'] = str(int(math.ceil(var_protectedstasetupconfig_new_factor * (sum_stations_servers_L3_0 + sum_stations_servers_L3_5))))
			elif attr_general_value == 'Expansion':
				row['Hours'] = str(var_protectedstasetupconfig_expansion_factor * (sum_stations_servers_L3_0 + sum_stations_servers_L3_5))
			a3_hours = float(row['Hours'])
		elif row['Identifier'] == 'A4':
			sum_stations_servers_L3_0 = validated_servers_L3_0 + non_validated_servers_L3_0
			sum_stations_servers_L3_5 = validated_servers_L3_5 + non_validated_servers_L3_5

			if attr_general_value == 'New':
				row['Hours'] = str(int(math.ceil(var_protectedservsetupconfig_new_factor * (sum_stations_servers_L3_0 + sum_stations_servers_L3_5))))
			elif attr_general_value == 'Expansion':
				row['Hours'] = str(var_protectedservsetupconfig_expansion_factor * (sum_stations_servers_L3_0 + sum_stations_servers_L3_5))
			a4_hours = float(row['Hours'])
		elif row['Identifier'] == 'A5':
			row['Hours'] = str(int(math.ceil(var_expanssvrstnconfig_factor * (migrations_only_existing_server_and_station_clients_L3_0 + migrations_only_existing_server_and_station_clients_L3_5))))
			a5_hours = float(row['Hours'])
		elif row['Identifier'] == 'A6':
			sum_stations_servers_L3_0 = non_validated_stations_L3_0 + non_validated_servers_L3_0
			sum_stations_servers_L3_5 = non_validated_stations_L3_5 + non_validated_servers_L3_5

			if attr_general_value == 'New':
				row['Hours'] = str(int(math.ceil(var_awlspecialpolicies_new_factor * (sum_stations_servers_L3_0 + sum_stations_servers_L3_5))))
			elif attr_general_value == 'Expansion':
				row['Hours'] = str(var_awlspecialpolicies_expansion_factor * (sum_stations_servers_L3_0 + sum_stations_servers_L3_5))
			a6_hours = float(row['Hours'])
		elif row['Identifier'] == 'A7':
			if attr_fds_dds_documentation_required_value == 'Yes':
				row['Hours'] = str(int(var_fds_dds_documentation_hrs))
			else:
				row['Hours'] = '0'
			a7_hours = float(row['Hours'])
		elif row['Identifier'] == 'A8':
			if attr_fat_report_required_value == 'Yes':
				row['Hours'] = str(int(var_fat_report_hrs))
			else:
				row['Hours'] = '0'
			a8_hours = float(row['Hours'])
		elif row['Identifier'] == 'A9':
			if attr_sat_report_required_value == 'Yes' and attr_fat_report_required_value == 'Yes':
				row['Hours'] = str(int(var_sat_fat_hrs))
			elif attr_sat_report_required_value == 'Yes':
				row['Hours'] = str(int(var_sat_hrs))
			else:
				row['Hours'] = '0'
			a9_hours = float(row['Hours'])
		elif row['Identifier'] == 'A10':
			if attr_general_value == 'New':
				row['Hours'] = str(int(var_customer_acceptance_familiarization_new_hrs))
			elif attr_general_value == 'Expansion':
				row['Hours'] = str(var_customer_acceptance_familiarization_expansion_hrs)
			a10_hours = float(row['Hours'])
		elif row['Identifier'] == 'A11':
			row['Hours'] = str(int(attr_travel_time_value))
			a11_hours = float(row['Hours'])
		elif row['Identifier'] == 'A12':
			a12_index = row_index
		if Product.Attr('calculate_value_set').GetValue() == "True" or row['Edit Hours'] == '':
			row['Edit Hours'] = row['Hours']
		row.Calculate()

	#Calculate A12 hours outside for loop

	total_hours = a1_hours + a2_hours + a3_hours + a4_hours + a5_hours + a6_hours + a8_hours + a9_hours + a10_hours
	cybert_coord_per = math.ceil((total_hours)*0.10)
	if cybert_coord_per <= 8:
		cyber_coord_hrs = 8
	elif cybert_coord_per >= 40:
		cyber_coord_hrs = 40
	else:
		cyber_coord_hrs = cybert_coord_per

	previous_value = activity_container.Rows[a12_index]['Hours']
	activity_container.Rows[a12_index]['Hours'] = str(int(math.ceil(cyber_coord_hrs)))
	if Product.Attr('calculate_value_set').GetValue() == "True" or activity_container.Rows[a12_index]['Edit Hours'] == '':
		activity_container.Rows[a12_index]['Edit Hours'] = activity_container.Rows[a12_index]['Hours']
	cyber = CyberProduct(Quote, Product, TagParserQuote)
	cyber.populateActivityListPricing('Activities')
	populateWTW(['Activities'], Product, Quote)