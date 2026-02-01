import datetime
#PS_Labor_Container_Populate
def isFloat(val):
	if val is not None and val != '':
		try:
			float(val)
			return True
		except:
			return False
	return False

def get_calculated_hrs(Product, attr_name):
    attr = filter(lambda a : a.Name == attr_name, Product.Attributes)
    val = 0
    if attr:
        val = Product.Attr(attr[0].Name).GetValue()
    return val
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
isR2Qquote = Quote.GetCustomField("isR2QRequest").Content
if isR2Qquote:
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
#process_type = Product.Attr('Exp_Project_Categorization').GetValue()
process_type = 'None'
if Product.GetContainerByName("CE_Project_Questions_Cont").Rows.Count > 0:
    process_type = Product.GetContainerByName("CE_Project_Questions_Cont").Rows[0].GetColumnByName("Project Categorization").DisplayValue
gesLocation = 'None'
if Product.GetContainerByName('Labor_Details_New/Expansion_Cont').Rows.Count > 0:
    gesLocation = Product.GetContainerByName('Labor_Details_New/Expansion_Cont').Rows[0].GetColumnByName('GES_Location').Value
if process_type == "Hardware only Project":
    disallow_lst.append("PCA Internal Kickoff Meeting")
    disallow_lst.append("PCA Project Control Workbook")
    disallow_lst.append("PCA Project Financial Report")
    disallow_lst.append("PCA Gate 1 Review")
    disallow_lst.append("PCA Project Control Plan")
    disallow_lst.append("PCA External Kickoff Meeting")
    disallow_lst.append("PCA Deliverable Control Index")
    disallow_lst.append("PCA Work Breakdown Structure")
    disallow_lst.append("PCA Acceptance Protocol")
    disallow_lst.append("PCA Gate 4 Review")
#process_type1 = Product.GetContainerByName("CE_Project_Questions_Cont").Rows[0].GetColumnByName("Project Categorization").DisplayValue
if process_type == "Small Project":
    disallow_lst.append("PCA Gate 1 Review")
    disallow_lst.append("PCA External Kickoff Meeting")
    disallow_lst.append("PCA Deliverable Control Index")
    disallow_lst.append("PCA Acceptance Protocol")
    disallow_lst.append("PCA Gate 4 Review")
'''process_type = Product.Attr('Exp_Project_Categorization').GetValue()
if process_type != "Hardware only Project":
    disallow_lst.append("PCA Financial System Setup")
    disallow_lst.append("PCA Project Balanced Scorecard")
    disallow_lst.append("PCA Project Schedule")
    disallow_lst.append("PCA Progress Measurement")
    disallow_lst.append("PCA Financial Close Out")
    disallow_lst.append("PCA Project Close Out Report")
process_type1 = Product.Attr('Exp_Project_Categorization').GetValue()
if process_type1 != "Small Project":
    disallow_lst.append("PCA Financial System Setup")
    disallow_lst.append("PCA Internal Kickoff Meeting")
    disallow_lst.append("PCA Project Control Workbook")
    disallow_lst.append("PCA Project Financial Report")
    disallow_lst.append("PCA Project Balanced Scorecard")
    disallow_lst.append("PCA Project Control Plan")
    disallow_lst.append("PCA Project Schedule")
    disallow_lst.append("PCA Progress Measurement")
    disallow_lst.append("PCA Work Breakdown Structure")
    disallow_lst.append("PCA Financial Close Out")
    disallow_lst.append("PCA Project Financial Report")
    disallow_lst.append("PCA Project Close Out Report")'''

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

laborCont = Product.GetContainerByName('Labor_Container')
tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from NEW_EXPANSION_LABOR_DELIVERABLE_2')

current_deliverables = []
rows_to_delete = []
for row in laborCont.Rows:
    current_deliverables.append(row.GetColumnByName('Deliverable').Value)

for row in tableLabor:
    if row.Deliverable not in disallow_lst and row.Deliverable not in current_deliverables:
        new_row = laborCont.AddNewRow(False)
        new_row["Deliverable"] = row.Deliverable
        if Quote.GetCustomField("R2QFlag").Content == "Yes":
            new_row["Execution Year"] = Quote.GetCustomField('R2Q_PRJT_Execution_Year').Content
        else:
            new_row["Execution Year"] = str(contract_start)
        new_row["Rank"] = str(row.Rank)
        sortRow(laborCont,row.Rank,new_row.RowIndex)
        if salesArea == "":
            new_row.GetColumnByName('Execution Country').Value = ""
        else:
            new_row.GetColumnByName('Execution Country').Value = query.Execution_County

        new_row["Productivity"]= row.Productivity

        #if row.Calculated_Hrs.isnumeric():
        if isFloat(row.Calculated_Hrs):
            new_row["Calculated Hrs"] = row.Calculated_Hrs
        else:
            new_row["Calculated Hrs"] = get_calculated_hrs(Product, row.Calculated_Hrs)
        if row.FO_Eng_1_NoGES  and row.FO_Eng_1_NoGES !='None':
            new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
            new_row['FO Eng 1']=row.FO_Eng_1_NoGES
        else:
            new_row.GetColumnByName('FO Eng 1').SetAttributeValue('None')
        if row.FO_Eng_2_NoGES and row.FO_Eng_2_NoGES !='None':
            new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
            new_row['FO Eng 2']=row.FO_Eng_2_NoGES
        else:
            new_row.GetColumnByName('FO Eng 2').SetAttributeValue('None')
        new_row.SetColumnValue('GES Location', gesLocation)
        new_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocation)
        if gesLocation == "None" or gesLocation == '':
            new_row["GES Eng % Split"]= row.GES_Eng_1_No
            new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
            new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
        else:
            new_row["GES Eng % Split"]= row.GES_Eng
            new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
            new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
            new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES PM-BO-'+gesLocation)
        new_row.ApplyProductChanges()
        new_row.Calculate()
    elif row.Deliverable in disallow_lst and row.Deliverable in current_deliverables:
        for cont_row in laborCont.Rows:
            if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                rows_to_delete.append(cont_row.RowIndex)
                break
    elif row.Deliverable in current_deliverables:
        for cont_row in laborCont.Rows:
            if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                applyChanges = 0
                if cont_row['GES Location'] != gesLocation:
                    cont_row.SetColumnValue('GES Location', gesLocation)
                    cont_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocation)
                    if gesLocation == "None" or gesLocation == '':
                        cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('None')
                    else:
                        cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES PM-BO-'+gesLocation)
                    applyChanges = 1
                if not row.Calculated_Hrs.isnumeric():
                    cont_row["Calculated Hrs"] = get_calculated_hrs(Product, row.Calculated_Hrs)
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