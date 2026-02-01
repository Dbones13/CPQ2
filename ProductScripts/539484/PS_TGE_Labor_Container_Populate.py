import datetime
#PS_Tank_Gauging_Engineering_Labor_Container_Populate
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

def update_location_GESValues(gesLocationVC,row):
    eng_values = ['HPS_GES_P350B_CN','HPS_GES_P350F_CN','HPS_GES_P350B_IN','HPS_GES_P350F_IN']
    allow_eng_values = [val for val in eng_values if str(gesLocationVC) in val]
    disallow_eng_values = [val for val in eng_values if str(gesLocationVC) not in val]
    row.Product.AllowAttrValues('TGE_Labor_GES_Eng',*allow_eng_values)
    row.Product.DisallowAttrValues('TGE_Labor_GES_Eng',*disallow_eng_values)

Product.ExecuteRulesOnce = True #This is to improve performance. We keep triggering product rules execution with each change to each container cell. Sets back to False at end of script.
salesArea = Quote.GetCustomField('Sales Area').Content
marketCode = Quote.SelectedMarket.MarketCode
#salesOrg = marketCode.partition('_')[0]
#Updated logic for Defect 29879
#currency = marketCode.partition('_')[2]
currency = Quote.GetCustomField('Currency').Content
query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesArea,currency))
#query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesArea))

disallow_lst = [] 
'''MS_ASE_attr_value = Product.Attr('MSASE_Analyser_System_Part_of_Metering_Package').GetValue()
if MS_ASE_attr_value != "No":
    disallow_lst.append("MS Progress Meeting with Client (at Client Location)")
MS_ASE_attr_value = Product.Attr('MSASE_Analyser_System_Part_of_Metering_Package').GetValue()
if MS_ASE_attr_value != "No":
    disallow_lst.append("MS Progress Meeting with Client (at Home Location)")
MS_ASE_attr_value = Product.Attr('MSASE_Analyser_System_Part_of_Metering_Package').GetValue()
if MS_ASE_attr_value != "No":
    disallow_lst.append("MS Project Meetings (Internal)")'''
    
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


laborCont = Product.GetContainerByName('TGE_Engineering_Labor_Container')
tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from Tank_Gauging_Engineering_LABOR_CUSTOM_TABLE')
gesLocation = Product.Attr("TGE_GES Location").GetValue()
#gesMapping = {'GES China':'CN','None':'None'}
#CXCPQ-83970
gesMapping = {'GES China':'CN','GES India':'IN','None':'None'}
gesLocationVC = gesMapping.get(gesLocation)

current_deliverables = []
rows_to_delete = []
for row in laborCont.Rows:
    current_deliverables.append(row.GetColumnByName('Deliverable').Value)
    update_location_GESValues(gesLocationVC,row)

for row in tableLabor:
    if row.Deliverable not in disallow_lst and row.Deliverable not in current_deliverables:
        new_row = laborCont.AddNewRow(False)
        new_row["Deliverable"] = row.Deliverable
        new_row["Execution Year"] = str(contract_start)
        new_row["Rank"] = str(row.Rank)
        #sortRow(laborCont,row.Rank,new_row.RowIndex)
        if salesArea == "":
            new_row.GetColumnByName('Execution Country').Value = ""
        else:
            new_row.GetColumnByName('Execution Country').Value = query.Execution_County

        if row.FO_Eng_1_NoGES:
            new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
            new_row['FO Eng 1']=row.FO_Eng_1_NoGES
        else:
            new_row.GetColumnByName('FO Eng 1').SetAttributeValue('None')
        if row.FO_Eng_2_NoGES:
            new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
            new_row['FO Eng 2']=row.FO_Eng_2_NoGES
        else:
            new_row.GetColumnByName('FO Eng 2').SetAttributeValue('None')
        new_row["Productivity"]= row.Productivity
        new_row["Calculated Hrs"]= row.Calculated_Hrs
        new_row.SetColumnValue('GES Location', gesLocationVC)
        new_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
        if gesLocation == "None" or gesLocation == '':
            new_row["GES Eng % Split"]= row.GES_Eng_1_No
            new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
            new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
            new_row['GES Eng'].GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('')
        else:
            new_row["GES Eng % Split"]= row.GES_Eng
            new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
            new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
            new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
            new_row['GES Eng']='SYS GES Eng-BO-'+gesLocationVC
            update_location_GESValues(gesLocationVC,new_row)
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
                    cont_row.SetColumnValue('GES Location', gesLocationVC)
                    cont_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
                    if gesLocation == "None" or gesLocation == '':
                        cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('')
                    else:
                        cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
                        cont_row['GES Eng']=('SYS GES Eng-BO-'+gesLocationVC)
                    update_location_GESValues(gesLocationVC,cont_row)
                    applyChanges = 1
                if applyChanges:
                    cont_row.ApplyProductChanges()
                    cont_row.Calculate()
                break
laborCont.Calculate()
rows_to_delete.sort(reverse=True)
laborAddi = Product.GetContainerByName('TGE_Additional_Labour_Container').Rows

for row1 in laborAddi:
    #Trace.Write(row1['UpdatedYear'])
    if row1.GetColumnByName('Execution Country').Value == "" and salesArea != "":
        row1['Execution Country'] = query.Execution_County
    if row1.GetColumnByName('Execution Year').Value == "":
        row1["Execution Year"] = str(contract_start)
    if gesLocation == "None" or gesLocation == '':
        row1["FO Eng % Split"] = '100'
        row1["GES Eng % Split"] = '0'
    elif row1["GES Eng % Split"] == '0' or row1["GES Eng % Split"] == '':
        row1["FO Eng % Split"] = '100'
    if row1['GES Location'] != gesLocationVC:
        row1['GES Location'] = gesLocationVC
        row1.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
        row1.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
        row1['GES Eng']=('SYS GES Eng-BO-'+gesLocationVC)
    attr_values  = row1.Product.Attr('TGE_ADDI_Labor_GES_Eng').Values		
    add_eng_values = []
    for val in attr_values:
        add_eng_values.append(val.ValueCode)
    Trace.Write('-addneg values--'+str(add_eng_values))
    allow_add_values =  [val for val in add_eng_values if str(gesLocationVC) in val]
    disallow_add_values =  [val for val in add_eng_values if str(gesLocationVC) not in val]
    row1.Product.AllowAttrValues('TGE_ADDI_Labor_GES_Eng',*allow_add_values)
    row1.Product.DisallowAttrValues('TGE_ADDI_Labor_GES_Eng',*disallow_add_values)
    row1.Product.ApplyRules()
    row1.ApplyProductChanges()
    row1.Calculate()
Product.GetContainerByName('TGE_Additional_Labour_Container').Calculate()
Product.ExecuteRulesOnce = False

Product.Attr('isProductLoaded').AssignValue('True')

for x in rows_to_delete:
    laborCont.DeleteRow(x)