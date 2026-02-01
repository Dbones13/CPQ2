import datetime
Product.ExecuteRulesOnce = True #This is to improve performance. We keep triggering product rules execution with each change to each container cell. Sets back to False at end of script.
current_year = datetime.datetime.now().year
query = SqlHelper.GetFirst("SELECT Service_Team FROM MIQ_BCOUNTRY_SERVICETEAM_MAPPING WHERE Booking_Country = '{}' ".format(str(Quote.GetCustomField("Booking Country").Content)))
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

laborCont = Product.GetContainerByName('MIQ Engineering Labor Container')
for row in laborCont.Rows:
    row["Execution Year"] = str(contract_start)
laborCont.Calculate()

laborAddi = Product.GetContainerByName('MIQ Additional Custom Deliverables').Rows
for row1 in laborAddi:
    if row1.GetColumnByName('Execution Year').Value == "":
        row1["Execution Year"] = str(contract_start)
    if row1.GetColumnByName('Execution Country').Value == "" and query is not None:
        row1["Execution Country"] = str(query.Service_Team)

Product.ExecuteRulesOnce = False