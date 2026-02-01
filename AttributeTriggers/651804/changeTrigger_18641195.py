import GS_UTILITY_CONTAINER_SORT as con
from System import DateTime

def getExecutionCountry():
	salesOrg = Quote.GetCustomField('Sales Area').Content
	currency = Quote.GetCustomField('Currency').Content
	query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
	if query is not None:
		Execution_County = query.Execution_County
	return Execution_County,salesOrg,currency

excecutionCountry,salesOrg,currency = getExecutionCountry()
currentYear = DateTime.Now.Year

activity = Product.GetContainerByName('Activities')
if Product.Attr('FAT Document Verification and Execution').GetValue() == '':
	for row in activity.Rows:
		if row['Identifier'] == 'A7':
			activity.DeleteRow(row.RowIndex)
			break
else:
	item = SqlHelper.GetFirst("Select PartNumber, Activity,Identifier,Activity_Type,Rank FROM CT_ACTIVITIES where Product = 'PCN Hardening' and Identifier = 'A7'")
	newRow = activity.AddNewRow(item.PartNumber,False)
	newRow['PartNumber'] = item.PartNumber
	newRow['Activity'] = item.Activity
	newRow['Identifier'] = item.Identifier
	newRow['Activity_Type'] = item.Activity_Type
	newRow["Error_Message"] = 'True'
	newRow["Execution Country"] = str(excecutionCountry)
	newRow['Execution_Year'] =  str(currentYear)
	newRow['Rank'] =  item.Rank
	newRow["Currency"] = str(currency)
	newRow["CostCurrency"] = Product.ParseString("<* TABLE ( SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = '<* TABLE ( SELECT Cost_Currency_Code FROM HPS_Labor_Cost_Data WHERE Sales_Org = '{}' AND Part_Number = '{}' ) *>' AND To_Currency = '{}' ) *>".format(str(salesOrg),item.PartNumber,str(currency)))
	newRow.Calculate()
	con.sortRow(activity,item.Rank,newRow.RowIndex)