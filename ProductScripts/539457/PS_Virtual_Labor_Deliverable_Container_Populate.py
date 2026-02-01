import datetime
# Virtualization_Labor_Deliverable_Container_Populate
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
if Product.Name == "Virtualization System" and scope == 'HW/SW + LABOR':
	Product.ExecuteRulesOnce = True #This is to improve performance. We keep triggering product rules execution with each change to each container cell. Sets back to False at end of script.
	salesArea = TagParserQuote.ParseString('<* QuoteProperty (Sales Area) *>')
	marketCode = TagParserQuote.ParseString('<* MCODE *>')
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

	laborCont = Product.GetContainerByName('Virtualization_Labor_Deliverable')
	tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from TABLE_VIRTUALIZATION_LABOR_DELIVERABLE')
	gesLocation = Product.Attr('Virtualization_Ges_Location').GetValue()

	current_deliverables = []
	rows_to_delete = []
	for row in laborCont.Rows:
		current_deliverables.append(row.GetColumnByName('Deliverable').Value)
					
	Product.ExecuteRulesOnce = True
	Product.Attr('isProductLoaded').AssignValue('False')
	for row in tableLabor:
		if  row.Deliverable not in current_deliverables:
			new_row = laborCont.AddNewRow(True)
			new_row["Deliverable"] = row.Deliverable
			new_row["Execution Year"] = str(contract_start)
			new_row["Rank"] = str(row.Rank)
			if salesArea == "":
				new_row.GetColumnByName('Execution Country').Value = ""
			else:
				new_row.GetColumnByName('Execution Country').Value = query.Execution_County

			if gesLocation == "None" or gesLocation == '':
				new_row["GES Eng % Split"]= row.GES_Eng_1_No
				new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
				new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
				new_row["Productivity"]= row.Productivity
				new_row["Calculated Hrs"]= row.Calculated_Hrs if row.Calculated_Hrs.isnumeric() else '0'
				new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
				new_row['FO Eng 1']=row.FO_Eng_1_NoGES
				new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
				new_row['FO Eng 2']=row.FO_Eng_2_NoGES
			else:
				new_row["GES Eng % Split"]= row.GES_Eng
				new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
				new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
				new_row["Productivity"]= row.Productivity
				new_row["Calculated Hrs"]= row.Calculated_Hrs if row.Calculated_Hrs.isnumeric() else '0'
				new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
				new_row['FO Eng 1']=row.FO_Eng_1_NoGES
				new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
				new_row['FO Eng 2']=row.FO_Eng_2_NoGES
			sortRow(laborCont,row.Rank,new_row.RowIndex)

	laborCont.Calculate()
	rows_to_delete.sort(reverse=True)
	

	laborAddi = Product.GetContainerByName('Virtualization_Additional_Custom_Deliverables').Rows

	for row1 in laborAddi:
		#Trace.Write(row1['UpdatedYear'])
		if row1.GetColumnByName('Execution Country').Value == "" and salesArea != "":
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