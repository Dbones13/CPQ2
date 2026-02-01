import math
from GS_Populate_Labour_WTW import populateWTW
from GS_CyberProductModule import CyberProduct

activity_container = Product.GetContainerByName('Activities')
activity_analysis_factors = SqlHelper.GetList("Select Top 1000 Assessment_Hours, Analysis_Factor, Identifier from CT_Activity_Analysis_Factors where Product = 'Assessments' order by Identifier, Sequence")
product_variables = SqlHelper.GetList("Select Variable, Value from CT_Product_Variables where Product = 'Assessments'")

#declare and initialize product variables

var_network_travel_time_hrs = 0
var_network_cyber_coordination_pct = 0
var_cyber_internal_peer_review_hrs = 0
var_cyber_customer_review_hrs = 0
var_cyber_travel_time_hrs = 0

#read values for product variables from table

for product_variable in product_variables:
	if product_variable.Variable == 'Var_Network_Travel_Time_Hrs':
		var_network_travel_time_hrs = float(product_variable.Value)
	elif product_variable.Variable == 'Var_Network_Cyber_Coordination_Pct':
		 var_network_cyber_coordination_pct = float(product_variable.Value)/100
	elif product_variable.Variable == 'Var_Cyber_Internal_Peer_Review_Hrs':
		var_cyber_internal_peer_review_hrs  = float(product_variable.Value)
	elif product_variable.Variable == 'Var_Cyber_Customer_Review_Hrs':
		var_cyber_customer_review_hrs  = float(product_variable.Value)
	elif product_variable.Variable == 'Var_Cyber_Travel_Time_Hrs':
		var_cyber_travel_time_hrs  = float(product_variable.Value)

#declare and initialize activity hour variables, indices

a1_hours = 0
a2_hours = 0
a3_hours = 0
a5_hours = 0
a6_hours = 0
a7_hours = 0
a8_hours = 0
a9_hours = 0
a10_hours = 0
a4_index = 0
a11_index = -1
row_index = -1
index = 0
cybert_coord_per = 0

#declare and assign attribute variables
attr_assessment_type_value = Product.Attr('Assessment Type').GetValue()
attr_remote_instrumentation_enclosures_rie_value = float(Product.Attr('Remote Instrumentation Enclosures (RIE)').GetValue())
attr_control_rooms_value = float(Product.Attr('Control Rooms').GetValue())
attr_dcs_or_fte_communities_value = float(Product.Attr('DCS or FTE Communities').GetValue())
attr_switches_and_routers_value = float(Product.Attr('Switches and Routers').GetValue())
attr_controllers_and_plcs_value = float(Product.Attr('Controllers and PLCs').GetValue())
attr_pcs_and_servers_value = float(Product.Attr("PC's and Servers").GetValue())
attr_firewalls_redundant_pair_value = 0

if Product.Attr('Firewalls (redundant pair)').GetValue()!='':
	attr_firewalls_redundant_pair_value = float(Product.Attr('Firewalls (redundant pair)').GetValue())

afive_hrs = int(math.ceil((attr_control_rooms_value * 2) + (attr_remote_instrumentation_enclosures_rie_value * 0.25) + (attr_dcs_or_fte_communities_value * 1) + (attr_switches_and_routers_value * 0.5) + (attr_controllers_and_plcs_value * 0.25) + (attr_pcs_and_servers_value * 0.5) + (attr_firewalls_redundant_pair_value * 2)))

aone_hrs = int(math.ceil((attr_control_rooms_value * 2) + (attr_remote_instrumentation_enclosures_rie_value * 0.25) + (attr_dcs_or_fte_communities_value * 1) + (attr_switches_and_routers_value * 0.5) + (attr_controllers_and_plcs_value * 0.25) + (attr_pcs_and_servers_value * 0.5)))

if (Product.Attr('R2QRequest').GetValue() == 'Yes' and Quote.GetCustomField("R2Q_Save").Content == "Submit") or Product.Attr('R2QRequest').GetValue() != 'Yes':
#calculate activity hours
	for row in activity_container.Rows:
		row_index = row_index + 1
		analysis_factor = 0
		previous_value = row['Hours']

		if row['Identifier'] == 'A1':
			row['Hours'] = str(aone_hrs)
			a1_hours = float(row['Hours'])
		elif row['Identifier'] == 'A2':
			for activity_analysis_factor in activity_analysis_factors:
				if activity_analysis_factor.Identifier == 'A2':
					if aone_hrs >= activity_analysis_factor.Assessment_Hours:
						analysis_factor = activity_analysis_factor.Analysis_Factor
					else:
						break
			row['Hours'] = str(int(math.ceil(aone_hrs * analysis_factor)))
			a2_hours = float(row['Hours'])
		elif row['Identifier'] == 'A3':
			row['Hours'] = str(int(var_network_travel_time_hrs))
			a3_hours = float(row['Hours'])
		elif row['Identifier'] == 'A4':
			a4_index = row_index
		elif row['Identifier'] == 'A5':
			row['Hours'] = str(afive_hrs)
			a5_hours = float(row['Hours'])
		elif row['Identifier'] == 'A6':
			for activity_analysis_factor in activity_analysis_factors:
				if activity_analysis_factor.Identifier == 'A6':
					if afive_hrs >= activity_analysis_factor.Assessment_Hours:
						analysis_factor = activity_analysis_factor.Analysis_Factor
					else:
						break
			row['Hours'] = str(int(math.ceil(afive_hrs * analysis_factor)))
			a6_hours = float(row['Hours'])
		elif row['Identifier'] == 'A7':
			for activity_analysis_factor in activity_analysis_factors:
				if activity_analysis_factor.Identifier == 'A7':
					if afive_hrs >= activity_analysis_factor.Assessment_Hours:
						analysis_factor = activity_analysis_factor.Analysis_Factor
					else:   
						break
			row['Hours'] = str(int(analysis_factor))
			a7_hours = float(row['Hours'])
		elif row['Identifier'] == 'A8':
			row['Hours'] = str(int(var_cyber_internal_peer_review_hrs))
			a8_hours = float(row['Hours'])
		elif row['Identifier'] == 'A9':
			row['Hours'] = str(int(var_cyber_customer_review_hrs))
			a9_hours = float(row['Hours'])
		elif row['Identifier'] == 'A10':
			row['Hours'] = str(int(var_cyber_travel_time_hrs))
			a10_hours = float(row['Hours'])
		elif row['Identifier'] == 'A11':
			a11_index = row_index

		if Product.Attr('calculate_value_set').GetValue() == "True" or row['Edit Hours'] == '':
			row['Edit Hours'] = row['Hours']

		row.Calculate()

	#Calculate A11 hours outside for loop
	if a4_index == 3 and attr_assessment_type_value == 'Network':
		cybert_coord_per = math.ceil((a1_hours + a2_hours)*0.10)
		index = 3
	if a11_index > -1:
		cybert_coord_per = math.ceil((a5_hours + a6_hours + a7_hours + a8_hours + a9_hours)*0.10)
		index = a11_index
	if index!=0:
		row = activity_container.Rows[index]
		if cybert_coord_per <= 8:
			cyber_coord_hrs = 8
		elif cybert_coord_per >= 40:
			cyber_coord_hrs = 40
		else:
			cyber_coord_hrs = cybert_coord_per
		previous_value = row['Hours']
		row['Hours'] = str(int(math.ceil(cyber_coord_hrs)))
		if Product.Attr('calculate_value_set').GetValue() == "True" or row['Edit Hours'] == '':
			row['Edit Hours'] = row['Hours']
	cyber = CyberProduct(Quote, Product, TagParserQuote)
	cyber.populateActivityListPricing('Activities')
	populateWTW(['Activities'], Product, Quote)