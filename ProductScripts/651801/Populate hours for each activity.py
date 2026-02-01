from GS_Populate_Labour_WTW import populateWTW
from GS_CyberProductModule import CyberProduct
import math

def get_value(attr_name, default='0'):
	value = Product.Attr(attr_name).GetValue()
	return int(value) if value else int(default)

def assign_value_if_edit_hours(row, attr_name):
	if row['Edit Hours'] not in ('', '0'):
		Product.Attr(attr_name).AssignValue(row['Edit Hours'])

def calculate_hours(row, var_factors, number_of_smx_units, number_of_years_of_contract):
	previous_value = row['Hours']
	if row['Identifier'] == 'A1':
		if number_of_smx_units > 0 or number_of_years_of_contract > 0:
			row['Hours'] = str(var_factors['Var_Initial_Comm_Config_Factor'] * get_value('Initial Communication Configuration'))
		else:
			row['Hours'] = '0'
	elif row['Identifier'] == 'A2':
		sum_of_ST_RT = get_value('Number of SMX System RT') + get_value('Number of SMX System ST')
		row['Hours'] = '8' if sum_of_ST_RT <= 6 else str(((sum_of_ST_RT - 6) * var_factors['Var_Setup_Config_Factor']) + 8)
	elif row['Identifier'] == 'A3':
		solution_familiarization_value = get_value('Solution Familiarization', 4)
		row['Hours'] = str(solution_familiarization_value if solution_familiarization_value > 0 else 4)
	elif row['Identifier'] == 'A4':
		if number_of_smx_units > 0 or number_of_years_of_contract > 0:
			row['Hours'] = str(get_value('Travel Time'))
		else:
			row['Hours'] = '0'

	if Product.Attr('calculate_value_set').GetValue() == "True" or row['Edit Hours'] == '':
		row['Edit Hours'] = row['Hours']

	return row['Hours']

def calculate_cyber_coord_hours(a1_hours, a2_hours, a3_hours):
	cybert_coord_per = math.ceil((float(a1_hours) + float(a2_hours) + float(a3_hours))*0.10)
	return max(8, min(cybert_coord_per, 40))

# Main logic
if (Product.Attr('R2QRequest').GetValue() == 'Yes' and Quote.GetCustomField("R2Q_Save").Content == "Submit") or Product.Attr('R2QRequest').GetValue() != 'Yes':
	activity_container = Product.GetContainerByName('Activities')
	number_of_smx_units = sum(get_value(attr) for attr in ['Number of SMX System RT', 'Number of SMX System ST', 'Number of System MI'])
	number_of_years_of_contract = get_value('Number of Years of Contract')

	# Assign values from activity container
	for row in activity_container.Rows:
		if row['Identifier'] in ['A3', 'A5', 'A4']:
			assign_value_if_edit_hours(row, 'Solution Familiarization' if row['Identifier'] == 'A3' 
									else 'Cybert Coordination Pct' if row['Identifier'] == 'A5' 
									else 'Travel Time')

	if number_of_smx_units == 0:
		activity_container.Rows.Clear()

	if activity_container.Rows.Count > 0:
		product_variables = SqlHelper.GetList("SELECT Variable, Value FROM CT_Product_Variables WHERE Product = 'SMX'")
		var_factors = {var.Variable: int(var.Value) for var in product_variables}
		a1_hours = a2_hours = a3_hours = a4_hours = 0
		a5_index = -1

		for row_index, row in enumerate(activity_container.Rows):
			row['Productivity'] = '1'
			hours = calculate_hours(row, var_factors, number_of_smx_units, number_of_years_of_contract)
			if row['Identifier'] == 'A1':
				a1_hours = hours
			elif row['Identifier'] == 'A2':
				a2_hours = hours
			elif row['Identifier'] == 'A3':
				a3_hours = hours
			elif row['Identifier'] == 'A4':
				a4_hours = hours
			elif row['Identifier'] == 'A5':
				a5_index = row_index

			row.Calculate()

		cyber_coord_hrs = calculate_cyber_coord_hours(a1_hours, a2_hours, a3_hours)
		previous_value = activity_container.Rows[a5_index]['Hours']
		activity_container.Rows[a5_index]['Hours'] = str(cyber_coord_hrs)
		if Product.Attr('calculate_value_set').GetValue() == "True" or activity_container.Rows[a5_index]['Edit Hours'] == '':
			activity_container.Rows[a5_index]['Edit Hours'] = activity_container.Rows[a5_index]['Hours']

		cyber = CyberProduct(Quote, Product, TagParserQuote)
		cyber.populateActivityListPricing('Activities')
		populateWTW(['Activities'], Product, Quote)