import datetime

def sortRow(cont,rank,new_row_index):
    sort_needed = True
    if new_row_index == 0:
        return
    while sort_needed == True:
        #Trace.Write("rank of previous row: {0}, new_row_index: {1}".format(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value, new_row_index))
        if int(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value) > int(rank):
            cont.MoveRowUp(new_row_index, False)
            new_row_index -= 1
        else:
            sort_needed = False

scope = Product.Attr('CE_Scope_Choices').GetValue()
if scope == 'HW/SW + LABOR':

    Product.ExecuteRulesOnce = True #This is to improve performance. We keep triggering product rules execution with each change to each container cell. Sets back to False at end of script.
    #salesArea = Quote.GetCustomField('Sales Area').Content
    #marketCode = Quote.SelectedMarket.MarketCode
    #salesOrg = marketCode.partition('_')[0]
    #Updated logic for Defect 29879
    #currency = marketCode.partition('_')[2]
    salesOrg = Quote.GetCustomField('Sales Area').Content
    currency = Quote.GetCustomField('Currency').Content
    query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
    #query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))

    disallow_lst = []
    process_type1 = Product.Attr('Labor_Site_Activities').GetValue()
    if process_type1 != "Yes":
        disallow_lst.append("DVM Site Acceptance Test")
    process_type2 = Product.Attr('Labor_Operation_Manual_Scope').GetValue()
    if process_type2 != "Yes":
        disallow_lst.append("DVM Operations Manual for Industrial Security")
    process_type3 = Product.Attr('Labor_Custom_Scope').GetValue()
    if process_type3 != "Yes":
        disallow_lst.append("DVM Customer Training")
    process_type4 = Product.Attr('Is Site Survey Required').GetValue()
    if process_type4 != "Yes":
        disallow_lst.append("DVM Site Survey Report")
    #Trace.Write('disallow_lst:'+str(disallow_lst))

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

    laborCont = Product.GetContainerByName('DVM_Engineering_Labor_Container')
    tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from DVM_ENGINEERING_LABOR')
    gesLocation = Product.Attr("DVM_GES_Location").GetValue()

    current_deliverables = []
    rows_to_delete = []
    for row in laborCont.Rows:
        current_deliverables.append(row.GetColumnByName('Deliverable').Value)

    for row in tableLabor:
        if row.Deliverable not in disallow_lst and row.Deliverable not in current_deliverables:
            new_row = laborCont.AddNewRow(False)
            new_row["Deliverable"] = row.Deliverable
            new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
            new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
            new_row['FO Eng 1']=row.FO_Eng_1_NoGES
            new_row['FO Eng 2']=row.FO_Eng_2_NoGES
            new_row["Execution Year"] = str(contract_start)
            new_row["Rank"] = str(row.Rank)
            sortRow(laborCont,row.Rank,new_row.RowIndex)
            if not query:
                new_row.GetColumnByName('Execution Country').Value = ""
            else:
                new_row.GetColumnByName('Execution Country').Value = query.Execution_County

            #Trace.Write('gesLocation: '+str(gesLocation))
            #Trace.Write('BSKR3::'+str(new_row["Deliverable"])+'::'+str(new_row.GetColumnByName('Execution Country').Value))
            new_row["Productivity"]= '1'
            #new_row["Calculated Hrs"]= row.Calculated_Hrs
            if gesLocation == "None" or gesLocation == '':
                new_row["GES Eng % Split"]= row.GES_Eng_1_No
                new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
                new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
                new_row['GES Eng'] = ''
            else:
                new_row["GES Eng % Split"]= row.GES_Eng
                new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
                new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES

            new_row.Calculate()
            #sortRow(laborCont,row.Rank,new_row.RowIndex)
        elif row.Deliverable in disallow_lst and row.Deliverable in current_deliverables:
            for cont_row in laborCont.Rows:
                if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                    rows_to_delete.append(cont_row.RowIndex)
    laborCont.Calculate()
    #Trace.Write('Total deliverables:'+str(laborCont.Rows.Count))
    rows_to_delete.sort(reverse=True)
    laborAddi = Product.GetContainerByName('DVM_Additional_Labour_Container').Rows

    for row1 in laborAddi:

        if row1.GetColumnByName('Execution Country').Value == "" and query:
            row1['Execution Country'] = query.Execution_County
        if row1.GetColumnByName('Execution Year').Value == "":
            row1["Execution Year"] = str(contract_start)
        if gesLocation == "None" or gesLocation == '':
            row1["FO Eng % Split"] = '100'
            row1["GES Eng % Split"] = '0'

    Product.ExecuteRulesOnce = False

    Product.Attr('isProductLoaded').AssignValue('True')

    for x in rows_to_delete:
        laborCont.DeleteRow(x)