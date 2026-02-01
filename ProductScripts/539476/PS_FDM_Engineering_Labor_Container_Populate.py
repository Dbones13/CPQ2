import datetime
def sortRow(cont,rank,new_row_index):
    sort_needed = True
    if new_row_index == 0:
        return
    while sort_needed == True:
        if int(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value) > int(rank):
            cont.MoveRowUp(new_row_index, False)
            new_row_index -= 1
        else:
            sort_needed = False
scope = Product.Attr('CE_Scope_Choices').GetValue()
if scope == 'HW/SW + LABOR':
    Product.ExecuteRulesOnce = True #This is to improve performance. We keep triggering product rules execution with each change to each container cell. Sets back to False at end of script.
    salesArea = Quote.GetCustomField('Sales Area').Content
    marketCode = Quote.SelectedMarket.MarketCode
    #salesOrg = marketCode.partition('_')[0]
    #Updated logic for Defect 29879
    #currency = marketCode.partition('_')[2]
    currency = Quote.GetCustomField('Currency').Content
    query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesArea,currency))



    disallow_lst = [] 
    if Product.Attr("Labor_Site_Activities").GetValue() != 'Yes':
        disallow_lst.append("FDM Commissioning")
        disallow_lst.append("FDM Site Acceptance Test & Sign Off")

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

    laborCont = Product.GetContainerByName('FDM Engineering Labor Container')
    tableLabor = SqlHelper.GetList('select Deliverable,GES_Eng_NoGES,GES_Eng_GES,FO_Eng_1_NoGES,FO_Eng_1_GES,FO1_Eng_NoGES,FO1_Eng_GES,FO_Eng_2_NoGES,FO_Eng_2_GES,FO2_Eng_NoGES,FO2_Eng_GES,Rank,Execution_Country from FDM_ENGINEERING_DELIVERABLES')
    nonr2q  = Quote.GetCustomField('R2QFlag').Content
    gesLocation = Product.Attr("FDM_GES_Location").GetValue()
    gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
    if gesLocation == '' and nonr2q:
        gesLocation = Quote.GetGlobal('ExGesLocation')
        gesLocationVC = gesLocation  # already mapped code like 'IN'
    else:
        gesLocationVC = gesMapping.get(gesLocation, 'None')

    current_deliverables = []
    rows_to_delete = []
    for row in laborCont.Rows:
        current_deliverables.append(row.GetColumnByName('Deliverable').Value)

    for row in tableLabor:
        if row.Deliverable not in disallow_lst and row.Deliverable not in current_deliverables:
            new_row = laborCont.AddNewRow(False)
            new_row["Deliverable"] = row.Deliverable
            if gesLocation == 'None' or gesLocation == '':
                new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
                new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
                new_row["FO Eng 1"]=row.FO_Eng_1_NoGES
                new_row["FO Eng 2"]=row.FO_Eng_2_NoGES
            else:
                Trace.Write('Inside GES-->')
                new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_GES)
                new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_GES)
                new_row["FO Eng 1"]=row.FO_Eng_1_GES
                new_row["FO Eng 2"]=row.FO_Eng_2_GES

            if Quote.GetCustomField('R2QFlag').Content == "Yes":
                new_row["Execution Year"] = Quote.GetCustomField('R2Q_PRJT_Execution_Year').Content
            else:
                new_row["Execution Year"] = str(contract_start)
            new_row["Rank"] = str(row.Rank)
            sortRow(laborCont,row.Rank,new_row.RowIndex)
            if salesArea == "":
                new_row.GetColumnByName('Execution Country').Value = ""
            else:
                new_row.GetColumnByName('Execution Country').Value = query.Execution_County

            if gesLocation == "None" or gesLocation == '':
                new_row["GES Eng % Split"]= row.GES_Eng_NoGES
                new_row["FO Eng 1 % Split"]= row.FO1_Eng_NoGES
                new_row["FO Eng 2 % Split"]= row.FO2_Eng_NoGES
            else:
                new_row["GES Eng % Split"]= row.GES_Eng_GES
                new_row["FO Eng 1 % Split"]= row.FO1_Eng_GES
                new_row["FO Eng 2 % Split"]= row.FO2_Eng_GES
                new_row['GES Eng'] = str('SYS GES Eng-BO-' + gesLocationVC)
                new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
            new_row.ApplyProductChanges()
            new_row.Calculate()
        elif row.Deliverable in disallow_lst and row.Deliverable in current_deliverables:
            for cont_row in laborCont.Rows:
                if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                    rows_to_delete.append(cont_row.RowIndex)
    laborCont.Calculate()
    rows_to_delete.sort(reverse=True)
    laborAddi = Product.GetContainerByName('FDM Additional Custom Deliverables').Rows

    for row1 in laborAddi:
        if row1.GetColumnByName('Execution Country').Value == "" and salesArea != "":
            row1['Execution Country'] = query.Execution_County
        if row1.GetColumnByName('Execution Year').Value == "":
            if Quote.GetCustomField('R2QFlag').Content == "Yes":
                row1["Execution Year"] = Quote.GetCustomField('R2Q_PRJT_Execution_Year').Content
            else:
                row1["Execution Year"] = str(contract_start)
        if gesLocation == "None" or gesLocation == '':
            row1["FO Eng % Split"] = '100'
            row1["GES Eng % Split"] = '0'
        if row1['Ges Location'] != gesLocationVC:
            row1['Ges Location'] = gesLocationVC
            row1.GetColumnByName('Ges Location').ReferencingAttribute.AssignValue(gesLocationVC)
            row1.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
        row1.Calculate()

    Product.ExecuteRulesOnce = False

    Product.Attr('isProductLoaded').AssignValue('True')

    for x in rows_to_delete:
        laborCont.DeleteRow(x)