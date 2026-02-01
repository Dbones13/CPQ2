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
scope = Product.Attr('CE_Scope_Choices').GetValue()
if scope == 'HW/SW + LABOR':
    Product.ExecuteRulesOnce = True #This is to improve performance. We keep triggering product rules execution with each change to each container cell. Sets back to False at end of script.
    salesArea = TagParserQuote.ParseString('<* QuoteProperty (Sales Area) *>')
    marketCode = TagParserQuote.ParseString('<* MCODE *>')
    #salesOrg = marketCode.partition('_')[0]
    #currency = marketCode.partition('_')[2]
    salesOrg = Quote.GetCustomField('Sales Area').Content
    currency = Quote.GetCustomField('Currency').Content
    query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))

    disallow_lst = [] 

    truck = Product.ParseString('<* IsSelected(Terminal_Mode_of_Transport.Truck loading/unloading) *>')
    rail = Product.ParseString('<* IsSelected(Terminal_Mode_of_Transport.Rail Wagon loading/unloading) *>')
    pipe = Product.ParseString('<* IsSelected(Terminal_Mode_of_Transport.Pipeline loading/unloading) *>')
    marine = Product.ParseString('<* IsSelected(Terminal_Mode_of_Transport.Marine loading/unloading) *>')

    if truck == '0':
        disallow_lst.extend(["TM Entry Gate Workflow","TM Reporting Office Workflow","TM Weigh Bridge (IN) Workflow","TM Bay Que Workflow","TM Weigh Bridge (OUT) Workflow","TM BoL Office Workflow","TM Exit Gate Workflow","TM PC DET Workflow","TM Mercury Terminal Workflow"])

    if rail == '0':
        disallow_lst.append("TM Rail CEPS")

    if marine == '0':
        disallow_lst.append("TM Marine CEPS")

    Load_List = ["Loading/Dispatch","Unloading/Receipt"]
    cont0 = Product.GetContainerByName('Terminal_Workflow_Scope')
    for row in cont0.Rows:
        if row["Truck Road"] == "" and row["Element"] not in Load_List:
            disallow_lst.append("TM "+row["Element"]+" Workflow")

    cont = Product.GetContainerByName('Terminal_Devices_Scope')
    for row in cont.Rows:
        if row["Truck Road"] == "" and row["Rail Wagon"] == "" and row["Pipeline"] == "" and row["Marine"] == "":
            disallow_lst.append("TM "+row["Element"]+" Devices")

    if Product.Attr("Labor_Site_Activities").GetValue() != 'Yes':
        disallow_lst.append("TM Site Acceptance Test")

    if Product.Attr("Terminal_SAP_ERP_BSI_Interface_required?").GetValue() != 'Yes':
        disallow_lst.extend(["TM BSI FDS Creation","TM BSI FDS Internal Review","TM Business System Interface"])

    if Product.Attr("Labor_Custom_Scope").GetValue() != 'Yes':
        disallow_lst.append("TM Training Manual")

    if Product.Attr("Terminal_Web_Portal_required?").GetValue() != 'Yes':
        disallow_lst.append("TM Web Portal Interface Configuration")

    if Product.Attr("Terminal_to_be_integrated_at_Enterprise_level").GetValue() < 1:
        disallow_lst.extend(["TM Enterprise Client Configuration","TM Enterprise Documentation"])

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

    laborCont = Product.GetContainerByName('Terminal Engineering Labor Container')
    tableLabor = SqlHelper.GetList('select Deliverable,GES_Eng_NoGES,GES_Eng_GES,FO_Eng_1_NoGES,FO_Eng_1_GES,FO1_Eng,FO_Eng_2,FO2_Eng,Rank,Execution_Country from TERMINAL_ENGINEERING_DELIVERABLES')
    gesLocation = Product.Attr("Terminal_Ges_Location_Labour").GetValue()


    current_deliverables = []
    rows_to_delete = []
    for row in laborCont.Rows:
        current_deliverables.append(row.GetColumnByName('Deliverable').Value)

    for row in tableLabor:
        if row.Deliverable not in disallow_lst and row.Deliverable not in current_deliverables:
            new_row = laborCont.AddNewRow(False)
            new_row["Deliverable"] = row.Deliverable
            new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO1_Eng)
            new_row['FO Eng 1']=row.FO1_Eng
            new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO2_Eng)
            new_row['FO Eng 2']=row.FO2_Eng
            new_row["Execution Year"] = str(contract_start)
            new_row["Rank"] = str(row.Rank)
            sortRow(laborCont,row.Rank,new_row.RowIndex)
            if salesArea == "":
                new_row.GetColumnByName('Execution Country').Value = ""
            else:
                new_row.GetColumnByName('Execution Country').Value = query.Execution_County

            Trace.Write('gesLocation: '+str(gesLocation))
            new_row["FO Eng 2 % Split"]= row.FO_Eng_2
            if gesLocation == "None" or gesLocation == '':
                new_row["GES Eng % Split"]= row.GES_Eng_NoGES
                new_row["FO Eng 1 % Split"]= row.FO_Eng_1_NoGES
            else:
                new_row["GES Eng % Split"]= row.GES_Eng_GES
                new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
            new_row.Product.ApplyRules()
            new_row.Calculate()
        elif row.Deliverable in disallow_lst and row.Deliverable in current_deliverables:
            for cont_row in laborCont.Rows:
                if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                    rows_to_delete.append(cont_row.RowIndex)
    laborCont.Calculate()
    for row in laborCont.Rows:
        if Product.Attr('isProductLoaded').GetValue() != "True":
            row["GES Eng % Split"]= "100"
            row["FO Eng 1 % Split"]= "0"
    rows_to_delete.sort(reverse=True)
    laborAddi = Product.GetContainerByName('Terminal Additional Custom Deliverables').Rows

    for row1 in laborAddi:
        #Trace.Write(row1['UpdatedYear'])
        if row1.GetColumnByName('Execution Country').Value == "" and salesArea != "":
            row1['Execution Country'] = query.Execution_County
        if row1.GetColumnByName('Execution Year').Value == "":
            row1["Execution Year"] = str(contract_start)
        if gesLocation == "None" or gesLocation == '':
            row1["FO Eng % Split"] = '100'
            row1["GES Eng % Split"] = '0'
        row1["Deliverable Name"] = "Commissioning"

    Product.ExecuteRulesOnce = False

    Product.Attr('isProductLoaded').AssignValue('True')

    for x in rows_to_delete:
        laborCont.DeleteRow(x)