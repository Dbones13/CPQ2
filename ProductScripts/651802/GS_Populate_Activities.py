import System
from System import DateTime
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from GS_GetPriceFromCPS import getPrice
import GS_UTILITY_CONTAINER_SORT as con


def getContainer(con):
	return Product.GetContainerByName(con)
activities_cont = getContainer('Activities')

def getExecutionCountry():
	salesOrg = Quote.GetCustomField('Sales Area').Content
	currency = Quote.GetCustomField('Currency').Content
	Execution_County = ''
	query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
	if query is not None:
		Execution_County = query.Execution_County
	return Execution_County,salesOrg, currency

def addRowsforActivities(activities_cont, partNumber, activity, identifier, activity_type, rank, Product):
	excecutionCountry,salesOrg, currency = getExecutionCountry()
	currentYear = DateTime.Now.Year
	addNewRow = activities_cont.AddNewRow(False)
	addNewRow['PartNumber'] = partNumber
	addNewRow['Activity'] = activity
	addNewRow['Identifier'] = identifier
	addNewRow['Activity_Type'] = activity_type
	addNewRow["Error_Message"] = 'True'
	addNewRow["Rank"] = rank
	if addNewRow["Identifier"] not in ['Total','On-Site','Off-Site']:
		addNewRow["Execution Country"] = str(excecutionCountry)
		addNewRow['Execution_Year'] =  str(currentYear)
		addNewRow["Currency"] = currency
		addNewRow["CostCurrency"] = Product.ParseString("<* TABLE ( SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = '<* TABLE ( SELECT Cost_Currency_Code FROM HPS_Labor_Cost_Data WHERE Sales_Org = '{}' AND Part_Number = '{}' ) *>' AND To_Currency = '{}' ) *>".format(str(salesOrg),partNumber,currency))
	addNewRow.Calculate()
	con.sortRow(activities_cont,addNewRow['Rank'],addNewRow.RowIndex)

def populateActivityListPricing():
	priceDict = dict()
	activities_list = [row['PartNumber'] for row in activities_cont.Rows if row['PartNumber']!='']
	list_set = set(activities_list)
	PriceData = getPrice(Quote,priceDict,list_set,TagParserQuote)
	for r in activities_cont.Rows:
		if r['Identifier'] not in ['Total','On-Site','Off-Site'] and r['Edit Hours'] not in ['','0.0','0']:
			r["List_Price"] = str((PriceData.get(r['PartNumber'],'')))

def populate_activities(activities_cont, product_name, conditions, Product):
	base_query = "SELECT PartNumber, Activity, Identifier, Activity_Type, Rank FROM CT_ACTIVITIES WHERE Product = '"+product_name+"'"
	filters = []
	
	for condition in conditions:
		if condition['value']:
			filter_condition = condition['filter']
			if filter_condition:
				filters.append(filter_condition)
	
	if filters:
		base_query += ' AND ' + ' AND '.join(filters)
	activity_list = SqlHelper.GetList(base_query)
	exist_identifier = {row['Identifier']:row.RowIndex for row in activities_cont.Rows if row['Identifier']!=''}
	for item in activity_list:
		if item.Identifier not in exist_identifier:
			addRowsforActivities(activities_cont, item.PartNumber, item.Activity, item.Identifier, item.Activity_Type, item.Rank, Product)

def conditionsMap(product_name, Product):
	conditions_map = {
		'PCN Hardening': [
			{'value': product_name == 'PCN Hardening' and Product.Attr('FAT Document Verification and Execution').GetValue() == 'Yes' and Product.Attr('FDS & DDS Documentation Required').GetValue() == 'Yes',
			 'filter': None},
			{'value': product_name == 'PCN Hardening' and Product.Attr('FAT Document Verification and Execution').GetValue() == 'Yes' and Product.Attr('FDS & DDS Documentation Required').GetValue() == '',
			 'filter': "Identifier <> 'A8'"},
			{'value': product_name == 'PCN Hardening' and Product.Attr('FDS & DDS Documentation Required').GetValue() == 'Yes' and Product.Attr('FAT Document Verification and Execution').GetValue() == '',
			 'filter': "Identifier <> 'A7'"},
			{'value': product_name == 'PCN Hardening',
			 'filter': None}
		],
		'MSS': [
			{'value': product_name == 'MSS' and Product.Attr('Patching and Anti-Virus Required').GetValue() == 'Yes' and Product.Attr('Repository Server Required').GetValue() == 'Yes' and Product.Attr('SAT Document Verification and Execution').GetValue() == 'Yes' and Product.Attr('FAT Document Verification and Execution').GetValue() == 'Yes' and Product.Attr('FDS & DDS Documentation Required').GetValue() == 'Yes' and Product.Attr('Microsoft Updates Install').GetValue() == 'Yes' and Product.Attr('Onsite Support Implementation Services').GetValue() == 'Yes',
			 'filter': None},
			{'value': product_name == 'MSS' and Product.Attr('Patching and Anti-Virus Required').GetValue() == '' and Product.Attr('Repository Server Required').GetValue() == '' and Product.Attr('SAT Document Verification and Execution').GetValue() == '' and Product.Attr('FAT Document Verification and Execution').GetValue() == '' and Product.Attr('FDS & DDS Documentation Required').GetValue() == '' and Product.Attr('Microsoft Updates Install').GetValue() == '' and Product.Attr('Onsite Support Implementation Services').GetValue() == '',
			 'filter': "Identifier NOT IN ('A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14')"}
		],
		'Cyber App Control': [
			{'value': product_name == 'Cyber App Control' and Product.Attr('FDS & DDS Documentation Required').GetValue() == 'Yes' and Product.Attr('FAT Document Verification and Execution').GetValue() == 'Yes' and Product.Attr('SAT Document Verification and Execution').GetValue() == 'Yes',
			 'filter': None},
			{'value': product_name == 'Cyber App Control' and Product.Attr('FDS & DDS Documentation Required').GetValue() == '' and Product.Attr('FAT Document Verification and Execution').GetValue() == '' and Product.Attr('SAT Document Verification and Execution').GetValue() == '',
			 'filter': "Identifier NOT IN ('A7', 'A8', 'A9')"},
			{'value': product_name == 'Cyber App Control' and Product.Attr('FDS & DDS Documentation Required').GetValue() == 'Yes' and Product.Attr('FAT Document Verification and Execution').GetValue() == '' and Product.Attr('SAT Document Verification and Execution').GetValue() == '',
			 'filter': "Identifier NOT IN ('A8', 'A9')"},
			{'value': product_name == 'Cyber App Control' and Product.Attr('FDS & DDS Documentation Required').GetValue() == '' and Product.Attr('FAT Document Verification and Execution').GetValue() == 'Yes' and Product.Attr('SAT Document Verification and Execution').GetValue() == '',
			 'filter': "Identifier NOT IN ('A7', 'A9')"},
			{'value': product_name == 'Cyber App Control' and Product.Attr('FDS & DDS Documentation Required').GetValue() == '' and Product.Attr('FAT Document Verification and Execution').GetValue() == '' and Product.Attr('SAT Document Verification and Execution').GetValue() == 'Yes',
			 'filter': "Identifier NOT IN ('A7', 'A8')"},
			{'value': product_name == 'Cyber App Control' and Product.Attr('FDS & DDS Documentation Required').GetValue() == 'Yes' and Product.Attr('FAT Document Verification and Execution').GetValue() == 'Yes' and Product.Attr('SAT Document Verification and Execution').GetValue() == '',
			 'filter': "Identifier <> 'A9'"},
			{'value': product_name == 'Cyber App Control' and Product.Attr('FDS & DDS Documentation Required').GetValue() == '' and Product.Attr('FAT Document Verification and Execution').GetValue() == 'Yes' and Product.Attr('SAT Document Verification and Execution').GetValue() == 'Yes',
			 'filter': "Identifier <> 'A7'"},
			{'value': product_name == 'Cyber App Control' and Product.Attr('FDS & DDS Documentation Required').GetValue() == 'Yes' and Product.Attr('FAT Document Verification and Execution').GetValue() == '' and Product.Attr('SAT Document Verification and Execution').GetValue() == 'Yes',
			 'filter': "Identifier <> 'A8'"},
			{'value': product_name == 'Cyber App Control',
			 'filter': None}
		],
		'SMX': [
			{'value': product_name == 'SMX',
			 'filter': None}
		],
		'Assessments': [
			{'value': product_name == 'Assessments' and Product.Attr('Assessment Type').GetValue() == 'Cyber',
			 'filter': "Derived !='N'"},
			{'value': product_name == 'Assessments' and Product.Attr('Assessment Type').GetValue() != 'Cyber',
			 'filter': "Derived !='C'"}
		]
	}
	return conditions_map

if (Product.Attr('R2QRequest').GetValue() == 'Yes' and Quote.GetCustomField("R2Q_Save").Content == "Submit") or Product.Attr('R2QRequest').GetValue() != 'Yes' or Product.PartNumber == 'CYBER_APP_CNTRL':

	activities_cont = getContainer('Activities')

	part_number_list = SqlHelper.GetList('SELECT Part_Number FROM CT_CYBER_PRICINGLISTTYPE')
	part_list = [i.Part_Number for i in part_number_list]
	part_list_str = ','.join(part_list)

	# Define the list of items
	items = """[IN](<*CTX( Product.PartNumber )*>, {})""".format(part_list_str)
	Quote.GetCustomField('CF_CYBER_DEFINE_PRICELIST').Content = items

	Quote.GetCustomField('CF_CYBER_DEFINE_PRICELIST_CPS').Content = str(part_list)

	if Product.PartNumber == 'CYBER_APP_CNTRL':
		cyber_app_servers = 0
		validated_stations = 0
		non_validated_stations = 0
		validated_servers = 0
		non_validated_servers = 0
		migrations = 0
		Total = 0
		for row in Product.GetContainerByName('Network Level Container').Rows:
			cyber_app_servers += int(row['Number of Cyber App Control Servers']) if row['Number of Cyber App Control Servers'] != '' else 0
			validated_stations += int(row['Validated Stations']) if row['Validated Stations'] != '' else 0
			non_validated_stations += int(row['Non‐Validated Stations']) if row['Non‐Validated Stations'] != '' else 0
			validated_servers += int(row['Validated Servers']) if row['Validated Servers'] != '' else 0
			non_validated_servers += int(row['Non‐Validated Servers']) if row['Non‐Validated Servers'] != '' else 0
			migrations += int(row['MIGRATIONS ONLY - Existing Server & Station Clients']) if row['MIGRATIONS ONLY - Existing Server & Station Clients'] != '' else 0
		Total = cyber_app_servers + validated_stations + non_validated_stations + non_validated_stations + validated_servers + non_validated_servers + migrations

	product_name = Product.Name
	conditions = conditionsMap(product_name,Product)
	if product_name in conditions:
		if (Product.PartNumber == 'SMX' and Product.Attr('Include Services').GetValue() == 'Yes') or (Product.PartNumber == 'MSS' and Product.Attr('Onsite Support Implementation Services').GetValue() == 'Yes') or (Product.PartNumber == 'CYBER_APP_CNTRL' and Total>0) or Product.PartNumber not in ['SMX','MSS','CYBER_APP_CNTRL']:
			populate_activities(activities_cont, product_name, conditions[product_name],Product)