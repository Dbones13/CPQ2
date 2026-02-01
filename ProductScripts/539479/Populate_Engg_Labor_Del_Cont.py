# C300_Labor_Base_Details populate
labor_base_cont = Product.GetContainerByName('C300_Labor_Base_Details')
if labor_base_cont.Rows.Count == 0:
    base_details = SqlHelper.GetList("Select * from PLC_UOC_ATTRIBUTE_MINMAX where Product = '{0}' and Container_Name ='{1}' ".format('ControlEdge UOC System', 'UOC_Labor_Base_Details'))
    for value in base_details:
        base_row = labor_base_cont.AddNewRow(False)
        base_row['Labor_Deliverable'] = value.Cont_ColumnName
        base_row['Less_Than_IO'] = str(value.Min)
        base_row['Greater_Than_IO'] = str(value.Max)
        base_row['Base_Values'] = str(value.Min + value.Max)

# PS_Experion_HS_Engineering_Labor_Container_Populate
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
    salesArea = marketCode = ""
    if Quote:
        salesArea = Quote.GetCustomField('Sales Area').Content
        marketCode = Quote.SelectedMarket.MarketCode
        salesOrg = Quote.GetCustomField('Sales Area').Content
        currency = Quote.GetCustomField('Currency').Content
        query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
        #query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))


    disallow_lst = []
    C300_Process_Type = Product.Attr('C300_Process_Type').GetValue()
    if C300_Process_Type == "None" or C300_Process_Type == "Continuous" or C300_Process_Type == "Continuous + Interlock" or C300_Process_Type == "Continuous + Sequence" or C300_Process_Type == "Continuous + Interlock + Sequence":
        disallow_lst.append("C300 Batch Design Workshop")
        disallow_lst.append("C300 Batch Protocols")
        disallow_lst.append("C300 Batch Application Configuration")
    if C300_Process_Type != "Batch-Pharma":
        disallow_lst.append("C300 Pharma QA Documentation")
        disallow_lst.append("C300 Pre-Test (Batch-Pharma)")
        disallow_lst.append("C300 Pharma Project Quality Management")

    Labor_Site_Activities = Product.Attr('Labor_Site_Activities').GetValue()
    if Labor_Site_Activities != "Yes":
        disallow_lst.append("C300 Site Installation")
        disallow_lst.append("C300 Site Acceptance Test & Sign off")

    Labor_Custom_Scope = Product.Attr('Labor_Custom_Scope').GetValue()
    if Labor_Custom_Scope != "Yes":
        disallow_lst.append("C300 Customer Training")

    Labor_Operation_Manual_Scope = Product.Attr('Labor_Operation_Manual_Scope').GetValue()
    if Labor_Operation_Manual_Scope != "Yes":
        disallow_lst.append("C300 Operation Manual")
    if Product.Attr('New_Expansion').GetValue() == 'Expansion':
        if Product.Attr('CE_Cutover').GetValue() != 'Yes':
            disallow_lst.append("C300 Cut Over Procedure ")
    else:
        disallow_lst.append("C300 Cut Over Procedure ")

    current_year = DateTime().Now.Year
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

    laborCont = Product.GetContainerByName('C300_Engineering_Labor_Container')
    Booking_LOB = TagParserQuote.ParseString('<* QuoteProperty (Booking LOB) *>')

    tableLabor = SqlHelper.GetList("select Deliverable,GES_Eng_NoGES,GES_Eng_GES,FO_Eng_1_NoGES,FO_Eng_1_GES,FO1_Eng_NoGES,FO1_Eng_GES,FO_Eng_2_NoGES,FO_Eng_2_GES,FO2_Eng_NoGES,FO2_Eng_GES,Rank,Execution_Country from C300_ENGINEERING_DELIVERABLES WHERE LOB ='"+str(Booking_LOB)+"'")
    '''if Booking_LOB != 'LSS':
        not_allowed = ['SVC-PMGT-ST','SVC-ECON-ST','SVC-ESSS-ST','SVC-EAPS-ST','SVC-EST1-ST','SVC-PMGT-ST-NC','SVC-ECON-ST-NC','SVC-ESSS-ST-NC','SVC-EAPS-ST-NC','SVC-EST1-ST-NC']'''
    gesLocation = Product.Attr("C300_GES_Location").GetValue()
    gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
    gesLocationVC = gesMapping.get(gesLocation)


    current_deliverables = []
    rows_to_delete = []
    for row in laborCont.Rows:
        current_deliverables.append(row.GetColumnByName('Deliverable').Value)

    for row in tableLabor:
        if row.Deliverable not in disallow_lst and row.Deliverable not in current_deliverables:
            new_row = laborCont.AddNewRow(False)
            new_row["Deliverable"] = row.Deliverable
            if gesLocation == 'None' or gesLocation == '': 
                new_row.GetColumnByName('FO Eng 1').ReferencingAttribute.SelectDisplayValue(row.FO_Eng_1_NoGES)
                new_row.GetColumnByName('FO Eng 2').ReferencingAttribute.SelectDisplayValue(row.FO_Eng_2_NoGES)           
                new_row['FO Eng 1']=row.FO_Eng_1_NoGES
                new_row['FO Eng 2']=row.FO_Eng_2_NoGES
            else:
                new_row.GetColumnByName('FO Eng 1').ReferencingAttribute.SelectDisplayValue(row.FO_Eng_1_GES)
                new_row.GetColumnByName('FO Eng 2').ReferencingAttribute.SelectDisplayValue(row.FO_Eng_2_GES)
                new_row['FO Eng 1']=row.FO_Eng_1_GES
                new_row['FO Eng 2']=row.FO_Eng_2_GES
            '''if Booking_LOB != 'LSS':
                new_row.Product.DisallowAttrValues('C300_FO_ENG_1', *not_allowed)
                new_row.Product.DisallowAttrValues('C300_FO_ENG_2', *not_allowed)'''
            if Quote.GetCustomField('R2QFlag').Content == "Yes":
                new_row["Execution Year"] = str(Quote.GetCustomField('R2Q_PRJT_Execution_Year').Content)
            else:
                new_row["Execution Year"] = str(contract_start)
            new_row["Rank"] = str(row.Rank)
            sortRow(laborCont,row.Rank,new_row.RowIndex)
            if salesArea == "":
                new_row.GetColumnByName('Execution Country').Value = ""
            else:
                new_row.GetColumnByName('Execution Country').Value = query.Execution_County
            new_row.SetColumnValue('GES Location', gesLocationVC)
            new_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
            Trace.Write('gesLocation: '+str(gesLocation))
            if gesLocation == "None" or gesLocation == '':
                new_row["GES Eng % Split"]= row.GES_Eng_NoGES
                # new_row["FO Eng 1"]= row.FO_Eng_1
                new_row["FO Eng 1 % Split"]= row.FO1_Eng_NoGES
                # new_row["FO Eng 2"]= row.FO_Eng_2
                new_row["FO Eng 2 % Split"]= row.FO2_Eng_NoGES
            else:
                new_row["GES Eng % Split"]= row.GES_Eng_GES
                # new_row["FO Eng 1"]= row.FO_Eng_1
                new_row["FO Eng 1 % Split"]= row.FO1_Eng_GES
                new_row["FO Eng 2 % Split"]= row.FO2_Eng_GES
                if row.Deliverable in ["C300 User Requirement Specification", "C300 Engineering Plan", "C300 Customer Training", "C300 Procure Materials & Services"]:
                    new_row['GES Eng'] = ''
                else:
                    if Booking_LOB == 'LSS':
                        new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('LSS GES Eng-BO-'+gesLocationVC)
                    else:
                        new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
            new_row.ApplyProductChanges()
            new_row.Calculate()
            #sortRow(laborCont,row.Rank,new_row.RowIndex)
        elif row.Deliverable in disallow_lst and row.Deliverable in current_deliverables:
            for cont_row in laborCont.Rows:
                if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                    rows_to_delete.append(cont_row.RowIndex)
        elif row.Deliverable in current_deliverables:
            for cont_row in laborCont.Rows:
                if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                    applyChanges = 0
                    if cont_row['GES Location'] != gesLocationVC:
                        cont_row.SetColumnValue('GES Location', gesLocationVC)
                        cont_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
                        if gesLocation == "None" or gesLocation == '':
                            cont_row['GES Eng'] = ''
                        else:
                            if row.Deliverable in ["C300 User Requirement Specification", "C300 Engineering Plan", "C300 Customer Training", "C300 Procure Materials & Services"]:
                                cont_row['GES Eng'] = ''
                            else:
                                if Booking_LOB == 'LSS':
                                    cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('LSS GES Eng-BO-'+gesLocationVC)
                                else:
                                    cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
                        applyChanges = 1
                    if applyChanges:
                        cont_row.ApplyProductChanges()
                        cont_row.Calculate()
                    break
    laborCont.Calculate()
    rows_to_delete.sort(reverse=True)

    laborAddi = Product.GetContainerByName('C300_Additional_Custom_Deliverables_Container').Rows
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
        if row1['GES Location'] != gesLocationVC:
            row1['GES Location'] = gesLocationVC
            row1.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
            if Booking_LOB == 'LSS':
                row1.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('LSS GES Eng-BO-'+gesLocationVC)
            else:
                row1.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
        row1.ApplyProductChanges()
        row1.Calculate()
    Product.GetContainerByName('C300_Additional_Custom_Deliverables_Container').Calculate()

    Product.ExecuteRulesOnce = False
    Product.Attr('isProductLoaded').AssignValue('True')

    for x in rows_to_delete:
        laborCont.DeleteRow(x)