import datetime
#PS_System_Interface_Labor_Container_Populate
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
systemInterface = 'No'
if scope == 'HW/SW + LABOR':
    attrList = ['Is Fieldbus Interface in Scope?', 'Is Modbus Interface in Scope?', 'Is Profibus Interface in Scope?', 'Is EtherNet IP Interface in Scope?', 'Is OPC Interface in Scope?', 'Is HART Interface in Scope?', 'Is Terminal Server Interface in Scope?', 'Is DeviceNet Interface in Scope?']
    for attr in attrList:
        val = Product.Attr(attr).GetValue()
        if val == 'Yes':
            systemInterface = 'Yes'
            break
if systemInterface == 'Yes':
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

    disallow_lst = []
    process_type = Product.Attr('Is Fieldbus Interface in Scope?').GetValue()
    if process_type != "Yes":
        disallow_lst.append("SII Function Design Specification -Fieldbus")
        disallow_lst.append("SII Detail Design Specification -Fieldbus")
        disallow_lst.append("SII Test Procedure -Fieldbus")
    process_type1 = Product.Attr('Is Modbus Interface in Scope?').GetValue()
    if process_type1 != "Yes":
        disallow_lst.append("SII Function Design Specification -Modbus")
        disallow_lst.append("SII Detail Design Specification -Modbus")
        disallow_lst.append("SII I/F Configuration Settings -Modbus")
        disallow_lst.append("SII Test Procedure -Modbus")
        disallow_lst.append("SII Pre-FAT - Modbus")
        disallow_lst.append("SII FAT and Sign Off-Modbus")
    process_type2 = Product.Attr('Is Profibus Interface in Scope?').GetValue()
    if process_type2 != "Yes":
        disallow_lst.append("SII Function Design Specification -Profibus")
        disallow_lst.append("SII Detail Design Specification -Profibus")
        disallow_lst.append("SII I/F Configuration Settings -Profibus")
        disallow_lst.append("SII Test Procedure -Profibus")
        disallow_lst.append("SII Pre-FAT - Profibus")
        disallow_lst.append("SII FAT and Sign Off-Profibus")
    process_type3 = Product.Attr('Is EtherNet IP Interface in Scope?').GetValue()
    if process_type3 != "Yes":
        disallow_lst.append("SII Function Design Specification -EtherNet IP")
        disallow_lst.append("SII Detail Design Specification -EtherNet IP")
        disallow_lst.append("SII I/F Configuration Settings -EtherNet IP")
        disallow_lst.append("SII Test Procedure -EtherNet IP")
        disallow_lst.append("SII Pre-FAT - EtherNet IP")
        disallow_lst.append("SII FAT and Sign Off-EtherNet IP")
    process_type4 = Product.Attr('Is OPC Interface in Scope?').GetValue()
    if process_type4 != "Yes":
        disallow_lst.append("SII OPC Self Test")
        disallow_lst.append("SII Function Design Specification -OPC")
        disallow_lst.append("SII Detail Design Specification -OPC")
        disallow_lst.append("SII I/F Configuration Settings -OPC")
        disallow_lst.append("SII Test Procedure -OPC")
        disallow_lst.append("SII Pre-FAT - OPC")
        disallow_lst.append("SII FAT and Sign Off-OPC")
    process_type5 = Product.Attr('Is HART Interface in Scope?').GetValue()
    if process_type5 != "Yes":
        disallow_lst.append("SII Function Design Specification -HART")
        disallow_lst.append("SII Detail Design Specification -HART")
        disallow_lst.append("SII I/F Configuration Settings-HART")
        disallow_lst.append("SII Test Procedure -HART")
        disallow_lst.append("SII Pre-FAT - HART")
        disallow_lst.append("SII FAT and Sign Off-HART")
    process_type6 = Product.Attr('Is Terminal Server Interface in Scope?').GetValue()
    if process_type6 != "Yes":
        disallow_lst.append("SII Function Design Specification -Terminal Svr")
        disallow_lst.append("SII Detail Design Specification -Terminal Svr")
        disallow_lst.append("SII I/F Configuration Settings-Terminal Svr")
        disallow_lst.append("SII Test Procedure -Terminal Svr")
        disallow_lst.append("SII Pre-FAT - Terminal Svr")
        disallow_lst.append("SII FAT and Sign Off -Terminal Svr")
    process_type7 = Product.Attr('Is DeviceNet Interface in Scope?').GetValue()
    if process_type7 != "Yes":
        disallow_lst.append("SII Function Design Specification -Devicenet")
    process_type8 = Product.Attr('Labor_Site_Activities').GetValue()
    if process_type8 != "Yes":
        disallow_lst.append("SII Site Installation")
        disallow_lst.append("SII Site Acceptance Test and Sign Off")
    process_type9 = Product.Attr('Labor_Operation_Manual_Scope').GetValue()
    if process_type9 != "Yes":
        disallow_lst.append("SII Operation Manual for System Interface")
    process_type10 = Product.Attr('Labor_Custom_Scope').GetValue()
    if process_type10 != "Yes":
        disallow_lst.append("SII Customer Training for System Interface")
    process_type11 = Product.Attr('Is Site Survey Required').GetValue()
    if process_type11 != "Yes":
        disallow_lst.append("SII Site Survey Report")

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

    laborCont = Product.GetContainerByName('System_Interface_Engineering_Labor_Container')
    tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from System_Interface_Labor')
    gesLocation = TagParserProduct.ParseString(Product.Attr("Experion_HS_Ges_Location_Labour").GetValue())
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

            if row.FO_Eng_1_NoGES:
                new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
                new_row['FO Eng 1']=row.FO_Eng_1_NoGES
            else:
                new_row.GetColumnByName('FO Eng 1').SetAttributeValue('None')
                new_row['FO Eng 1']='None'
            if row.FO_Eng_2_NoGES:
                new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
                new_row['FO Eng 2']=row.FO_Eng_2_NoGES
            else:
                new_row.GetColumnByName('FO Eng 2').SetAttributeValue('None')
                new_row['FO Eng 2']='None'
            new_row["Productivity"]= row.Productivity
            new_row["Calculated Hrs"]= row.Calculated_Hrs
            new_row.SetColumnValue('GES Location', gesLocationVC)
            new_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
            if gesLocation == "None" or gesLocation == '':
                new_row["GES Eng % Split"]= row.GES_Eng_1_No
                new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
                new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
                new_row['GES Eng'] = ''
            else:
                new_row["GES Eng % Split"]= row.GES_Eng
                new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
                new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
                new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
                new_row['GES Eng']= 'SYS GES Eng-BO-'+gesLocationVC
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
                            cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
                            cont_row['GES Eng'] = 'SYS GES Eng-BO-'+gesLocationVC
                        applyChanges = 1
                    if applyChanges:
                        cont_row.ApplyProductChanges()
                        cont_row.Calculate()
                    break
    laborCont.Calculate()
    rows_to_delete.sort(reverse=True)
    Product.ExecuteRulesOnce = False
    Product.Attr('isProductLoaded').AssignValue('True')

    for x in rows_to_delete:
        laborCont.DeleteRow(x)