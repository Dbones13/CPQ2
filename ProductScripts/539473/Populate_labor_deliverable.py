import datetime
def sortRow(cont,rank,new_row_index):
    sort_needed = True
    if new_row_index == 0:
        return
    while sort_needed == True:
        Trace.Write("rank of previous row: {0}, new_row_index: {1}".format(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value, new_row_index))
        if int(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value) > int(rank):
            cont.MoveRowUp(new_row_index, False)
            new_row_index -= 1
        else:
            sort_needed = False

Product.ExecuteRulesOnce = True #This is to improve performance. We keep triggering product rules execution with each change to each container cell. Sets back to False at end of script.
salesArea = TagParserQuote.ParseString('<* QuoteProperty (Sales Area) *>')
marketCode = TagParserQuote.ParseString('<* MCODE *>')
#salesOrg = marketCode.partition('_')[0]
#Updated logic for Defect 29879
#currency = marketCode.partition('_')[2]
salesOrg = Quote.GetCustomField('Sales Area').Content
currency = Quote.GetCustomField('Currency').Content
query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
#query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))

current_year = datetime.datetime.now().year
if Quote:
    if Quote.GetCustomField('EGAP_Contract_Start_Date').Content != "": #If there is a Contract Start Date in the quote:
        c_start_date = Quote.GetCustomField('EGAP_Contract_Start_Date').Content
        contract_start = int("20"+c_start_date[-2:])
        if contract_start > current_year+3: #Maxes out at 3 years in the future. Can't go beyond that.
            contract_start = current_year+3
    else:
        contract_start = current_year
else:
    contract_start = current_year
gesLocation = Product.Attr('C300_GES_Location').GetValue()

laborAddi = Product.GetContainerByName('ESDC_Labor_Additional_Cust_Deliverables_con').Rows

for row1 in laborAddi:
    #Trace.Write(row1['UpdatedYear'])
    if row1.GetColumnByName('Execution Country').Value == "" and salesArea != "":
        row1['Execution Country'] = query.Execution_County
    if row1.GetColumnByName('Execution Year').Value == "":
        row1["Execution Year"] = str(contract_start)
    if gesLocation == "None" or gesLocation == '':
        row1["FO Eng % Split"] = '100'
        row1["GES Eng % Split"] = '0'
    row1.Calculate()

Product.ExecuteRulesOnce = False

Product.Attr('isProductLoaded').AssignValue('True')

#for x in rows_to_delete:
#    laborCont.DeleteRow(x)