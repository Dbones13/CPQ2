from GS_Populate_Labour_WTW import populateWTW
from System import DateTime
import GS_UTILITY_CONTAINER_SORT as con

activities_cont = Product.GetContainerByName('Activities')

def getExecutionCountry():
    salesOrg = Quote.GetCustomField('Sales Area').Content
    currency = Quote.GetCustomField('Currency').Content
    query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
    if query is not None:
        Execution_County = query.Execution_County
    return Execution_County,salesOrg,currency

excecutionCountry,salesOrg,currency = getExecutionCountry()
currentYear = DateTime.Now.Year

def addRowsforActivities(activities_cont, partNumber, activity, identifier, Activity_Type,rank):
    addNewRow = activities_cont.AddNewRow(False)
    addNewRow['PartNumber'] = partNumber
    addNewRow['Activity'] = activity
    addNewRow['Identifier'] = identifier
    addNewRow['Activity_Type'] = Activity_Type
    addNewRow["Error_Message"] = 'True'
    addNewRow["Execution Country"] = str(excecutionCountry)
    addNewRow['Execution_Year'] =  str(currentYear)
    addNewRow['Rank'] =  str(rank)
    addNewRow["Currency"] = str(currency)
    addNewRow["CostCurrency"] = Product.ParseString("<* TABLE ( SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = '<* TABLE ( SELECT Cost_Currency_Code FROM HPS_Labor_Cost_Data WHERE Sales_Org = '{}' AND Part_Number = '{}' ) *>' AND To_Currency = '{}' ) *>".format(str(salesOrg),partNumber,str(currency)))
    addNewRow.Calculate()
    con.sortRow(activities_cont,rank,addNewRow.RowIndex)

def populateAssessmentsActivities():
    if Product.Attr('Assessment Type').GetValue() == 'Cyber':
        activity = SqlHelper.GetList("SELECT top 1000 PartNumber, Activity, Identifier,Activity_Type,Rank FROM CT_ACTIVITIES where Product = 'Assessments' and Derived !='N'")
        for item in activity:
            addRowsforActivities(activities_cont, item.PartNumber, item.Activity, item.Identifier, item.Activity_Type, item.Rank)
    else:
        activity = SqlHelper.GetList("SELECT top 1000 PartNumber, Activity,Derived,Identifier, Activity_Type,Rank FROM CT_ACTIVITIES where Product = 'Assessments' and Derived !='C'")
        for item in activity:
            addRowsforActivities(activities_cont, item.PartNumber, item.Activity, item.Identifier, item.Activity_Type, item.Rank)
    populateWTW(['Activities'], Product, Quote)
activities_cont.Rows.Clear()
populateAssessmentsActivities()

if Product.Attr('Assessment Type').GetValue() == "Cyber":
    Product.AllowAttr('Firewalls (redundant pair)')
    Product.Attr('Firewalls (redundant pair)').AssignValue('0')
else:
    Product.DisallowAttr('Firewalls (redundant pair)')