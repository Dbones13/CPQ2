import datetime
#PS_HMI_Engineering_Labor_Container_Populate
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
    # salesOrg = marketCode.partition('_')[0]
    #Updated logic for Defect 29879
    # currency = marketCode.partition('_')[2]
    salesOrg = Quote.GetCustomField('Sales Area').Content
    currency = Quote.GetCustomField('Currency').Content
    query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
    #query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))


    disallow_lst = []
    if Product.Attr("PSW_Only_HAZOP_Scope").GetValue() == "No":
        disallow_lst.append("PSW HAZOP Session and Report")
    if Product.Attr("PSW_Only_LOPA_Scope").GetValue() == "No":
        disallow_lst.append("PSW LOPA Session and Report")
    if Product.Attr("PSW_Only_SIL_Verification_Calculation_Scope").GetValue() == "No":
        disallow_lst.append("PSW SIL Verification Calculation Report")
    if Product.Attr("Only Safety Requirement Specification (SRS) Scope").GetValue() == "No":
        disallow_lst.append("PSW Safety Requirement Specification (SRS) Document")
    if Product.Attr("PSW_Only_Functional_Test_Procedure_(FTP)_Scope").GetValue() == "No":
        disallow_lst.append("PSW Functional Test Procedure (FTP) Document")
    if Product.Attr("PSW_HAZOP+LOPA+SIL_Ver_calcs+SRS+FTP_Scope").GetValue() == "No":
        disallow_lst.append("PSW HAZOP, LOPA, SIL Ver Calcs, SRS, FTP")
    if Product.Attr("PSW_LOPA+SIL_Ver_calcs+SRS+FTP_Scope").GetValue() == "No":
        disallow_lst.append("PSW LOPA, SIL Ver Calcs, SRS, FTP")
    if Product.Attr("PSW_LOPA+SIL_Ver_calcs+SRS_Scope").GetValue() == "No":
        disallow_lst.append("PSW LOPA, SIL Ver Calcs, SRS")
    if Product.Attr("PSW_SIL_Ver_calcs+SRS+FTP_Scope").GetValue() == "No":
        disallow_lst.append("PSW SIL Ver Calcs, SRS, FTP")
    if Product.Attr("PSW_SIL_Ver_calcs+SRS_Scope").GetValue() == "No":
        disallow_lst.append("PSW SIL Ver Calcs, SRS")
    if Product.Attr("PSW_HAZOP_Import_Scope").GetValue() == "No":
        disallow_lst.append("PSW HAZOP Import")
    if Product.Attr("PSW_LOPA_Import_Scope").GetValue() == "No":
        disallow_lst.append("PSW LOPA Import")
    if Product.Attr("PSW_SIL_Calculation_Import_Scope").GetValue() == "No":
        disallow_lst.append("PSW SIL Calculations Import")
    if Product.Attr("PSW_SRS_Import_in_Scope").GetValue() == "No":
        disallow_lst.append("PSW SRS Import")
    if Product.Attr("PSW_FTP_Template_Import_Scope").GetValue() == "No":
        disallow_lst.append("PSW FTP Template Import")


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


    laborCont = Product.GetContainerByName('PSW_Labor_Container')
    #tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from Fire_and_Gas_Consultancy_Service_Labor_custom_table')
    tableLabor = SqlHelper.GetList('select * from Process_Safety_Workbench_Engineering_Custom_Table')
    gesLocation = Product.Attr("PSW_GES_Location").GetValue()
    gesMapping = {'GES India':'IN','None':'None','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','GES Egypt':'EG' }
    gesLocationVC = gesMapping.get(gesLocation)

    current_deliverables = []
    rows_to_delete = []
    for row in laborCont.Rows:
        current_deliverables.append(row.GetColumnByName('Deliverable').Value)

    for row in tableLabor:
        if row.Deliverable not in disallow_lst and row.Deliverable not in current_deliverables:
            new_row = laborCont.AddNewRow(False)
            new_row["Deliverable"] = row.Deliverable
            new_row["Execution Year"] = str(contract_start)
            new_row["Rank"] = str(row.Rank)
            sortRow(laborCont,row.Rank,new_row.RowIndex)
            if salesArea == "":
                new_row.GetColumnByName('Execution Country').Value = ""
            else:
                new_row.GetColumnByName('Execution Country').Value = query.Execution_County

            Trace.Write('gesLocation: '+str(gesLocation))
            if row.FO_Eng_1:
                new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1)
                new_row['FO Eng 1']=row.FO_Eng_1
            else:
                new_row.GetColumnByName('FO Eng 1').SetAttributeValue('None')
            if row.FO_Eng_2:
                new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2)
                new_row['FO Eng 2']=row.FO_Eng_2
            else:
                new_row.GetColumnByName('FO Eng 2').SetAttributeValue('None')
            new_row["Productivity"]= row.Productivity
            new_row["Calculated Hrs"]= row.Calculated_Hrs if row.Calculated_Hrs.isnumeric() else '0'
            new_row.SetColumnValue('GES Location', gesLocationVC)
            new_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
            if gesLocation == "None" or gesLocation == '':
                Log.Write("None condition")
                new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('')
                new_row["FO Eng 1 % Split"] =  row.FO_Eng_1_Split_GES_None
                new_row["FO Eng 2 % Split"] = row.FO_Eng_2_Split_GES_None
                new_row["GES Eng % Split"] = "0"
                new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_Ges_None)
                new_row['FO Eng 1'] = row.FO_Eng_1_Ges_None
                new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2)
                new_row['FO Eng 2'] = row.FO_Eng_2
            else:
                Log.Write("Not None condition")
                new_row["GES Eng % Split"] = row.GES_Eng_Split
                new_row["FO Eng 1 % Split"] = row.FO_Eng_1_GES
                new_row["FO Eng 2 % Split"] = row.FO_Eng_2_GES
                #new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue(row.GES_Eng)
                new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1)
                #new_row['FO Eng 1'] = row.FO_Eng_1
                new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2)
                #new_row['FO Eng 2'] = row.FO_Eng_2
                new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
            new_row.ApplyProductChanges()
            new_row.Calculate()
            sortRow(laborCont,row.Rank,new_row.RowIndex)
        elif row.Deliverable in disallow_lst and row.Deliverable in current_deliverables:
            for cont_row in laborCont.Rows:
                if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                    rows_to_delete.append(cont_row.RowIndex)
        elif row.Deliverable in current_deliverables:
            for cont_row in laborCont.Rows:
                if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                    applyChanges = 0
                    if cont_row['GES Location'] != gesLocationVC:
                        updateEngSplit = False
                        if cont_row['GES Location'] == "None":
                            updateEngSplit = True
                        cont_row.SetColumnValue('GES Location', gesLocationVC)
                        cont_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
                        if gesLocation == "None" or gesLocation == '':
                            cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('')
                            cont_row["FO Eng 1 % Split"] =  row.FO_Eng_1_Split_GES_None
                            cont_row["FO Eng 2 % Split"] = row.FO_Eng_2_Split_GES_None
                            cont_row["GES Eng % Split"] = "0"
                            cont_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_Ges_None)
                            cont_row['FO Eng 1'] = row.FO_Eng_1_Ges_None
                            cont_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2)
                            cont_row['FO Eng 2'] = row.FO_Eng_2
                        else:
                            if updateEngSplit:
                                cont_row["FO Eng 1 % Split"] = row.FO_Eng_1_GES
                                cont_row["FO Eng 2 % Split"] = row.FO_Eng_2_GES
                                cont_row["GES Eng % Split"] = row.GES_Eng_Split
                            #cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue(row.GES_Eng)
                            cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
                            cont_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1)
                            cont_row['FO Eng 1'] = row.FO_Eng_1
                            cont_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2)
                            cont_row['FO Eng 2'] = row.FO_Eng_2
                        applyChanges = 1
                    if applyChanges:
                        cont_row.ApplyProductChanges()
                        cont_row.Calculate()
                    break
    laborCont.Calculate()
    rows_to_delete.sort(reverse=True)
    laborAddi = Product.GetContainerByName('PSW_Additional_Labor_Container').Rows

    for row1 in laborAddi:
        #Trace.Write(row1['UpdatedYear'])
        if row1.GetColumnByName('Execution Country').Value == "" and salesArea != "":
            row1['Execution Country'] = query.Execution_County
        if row1.GetColumnByName('Execution Year').Value == "":
            row1["Execution Year"] = str(contract_start)
        if gesLocation == "None" or gesLocation == '':
            row1["FO Eng % Split"] = '100'
            row1["GES Eng % Split"] = '0'
        elif row1["GES Eng % Split"] == '0':
            row1["FO Eng % Split"] = '100'
        if row1['GES Location'] != gesLocationVC:
            row1['GES Location'] = gesLocationVC
            row1.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
            row1.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocation)
        row1.ApplyProductChanges()
        row1.Calculate()
    Product.GetContainerByName('PSW_Additional_Labor_Container').Calculate()
    Product.ExecuteRulesOnce = False

    Product.Attr('isProductLoaded').AssignValue('True')

    for x in rows_to_delete:
        laborCont.DeleteRow(x)