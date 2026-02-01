import datetime
#PS_HMI_Engineering_Labor_Container_Populate
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

if Product.Attr('Is HMI Engineering in Scope?').GetValue() == "Yes" and Product.Attr('CE_Scope_Choices').GetValue() == 'HW/SW + LABOR':
	Product.ExecuteRulesOnce = True #This is to improve performance. We keep triggering product rules execution with each change to each container cell. Sets back to False at end of script.
	#salesArea = TagParserQuote.ParseString('<* QuoteProperty (Sales Area) *>')
	#marketCode = TagParserQuote.ParseString('<* MCODE *>')
	#salesOrg = marketCode.partition('_')[0]
	#Updated logic for Defect 29879
	#currency = marketCode.partition('_')[2]
	salesOrg = Quote.GetCustomField('Sales Area').Content
	currency = Quote.GetCustomField('Currency').Content
	query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
	
	disallow_lst = [] 
	process_type = Product.Attr('Labor_Site_Activities').GetValue()
	if process_type != "Yes":
		disallow_lst.append("HMI SAT & Sign Off")
	process_type1 = Product.Attr('Labor_Operation_Manual_Scope').GetValue()
	if process_type1 != "Yes":
		disallow_lst.append("HMI Operation Manual")
	process_type2 = Product.Attr('Labor_Custom_Scope').GetValue()
	if process_type2 != "Yes":
		disallow_lst.append("HMI Customer Training")
	if Product.Attr('New_Expansion').GetValue() == 'Expansion':
		if Product.Attr('CE_Cutover').GetValue() != 'Yes':
			disallow_lst.append("HMI Cut Over Procedure")
	else:
		disallow_lst.append("HMI Cut Over Procedure")

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


	laborCont = Product.GetContainerByName('HMI_Engineering_Labor_Container')
	tableLabor = SqlHelper.GetList('select Top 1000 Deliverable,Productivity,GES_Eng_1_No,FO_Eng_1_GES_Loc,FO_Eng_2_GES_Loc,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from HMI_ENGINEERING_LABOR_CONTAINER Order By CAST(Rank AS int)')
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
			if not query:
				new_row.GetColumnByName('Execution Country').Value = ""
			else:
				new_row.GetColumnByName('Execution Country').Value = query.Execution_County
			new_row["Productivity"]= row.Productivity
			new_row["Calculated Hrs"]= row.Calculated_Hrs
			new_row.SetColumnValue('GES Location', gesLocationVC)
			new_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
			if gesLocation == "None" or gesLocation == '':
				if row.FO_Eng_1_NoGES:
					new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
					new_row['FO Eng 1']=row.FO_Eng_1_NoGES
					Log.Write("--FO eng 1-"+str(new_row['FO Eng 1'])+"-row-"+str(row.FO_Eng_1_NoGES))
				else:
					new_row.GetColumnByName('FO Eng 1').SetAttributeValue('None')
					new_row['FO Eng 1']='None'
				if row.FO_Eng_2_NoGES:
					new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
					new_row['FO Eng 2']=row.FO_Eng_2_NoGES
					Log.Write("--FO eng 2-"+str(new_row['FO Eng 2'])+"-row-"+str(row.FO_Eng_2_NoGES))
				else:
					new_row.GetColumnByName('FO Eng 2').SetAttributeValue('None')
					new_row['FO Eng 2']='None'

				new_row["GES Eng % Split"]= row.GES_Eng_1_No
				new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
				new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
				new_row['GES Eng'] = ''
				if row.Deliverable in ['HMI Engineering Plan', 'HMI Customer Training']:
					new_row['GES Eng'] = ''
				else:
					new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES HMI Eng-BO-'+gesLocationVC)
			else:
				if row.FO_Eng_1_GES_Loc:
					new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_GES_Loc)
					new_row['FO Eng 1']=row.FO_Eng_1_GES_Loc
					Log.Write("--FO eng 1-"+str(new_row['FO Eng 1'])+"-row-"+str(row.FO_Eng_1_GES_Loc))
				else:
					new_row.GetColumnByName('FO Eng 1').SetAttributeValue('None')
					new_row['FO Eng 1']='None'
				if row.FO_Eng_2_GES_Loc:
					new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_GES_Loc)
					new_row['FO Eng 2']=row.FO_Eng_2_GES_Loc
					Log.Write("--FO eng 2-"+str(new_row['FO Eng 2'])+"-row-"+str(row.FO_Eng_2_GES_Loc))
				else:
					new_row.GetColumnByName('FO Eng 2').SetAttributeValue('None')
					new_row['FO Eng 2']='None'
				new_row["GES Eng % Split"]= row.GES_Eng
				new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
				new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
				if row.Deliverable in ['HMI Operator Interface Workshop', 'HMI Engineering Plan', 'HMI Customer Training']:
					new_row['GES Eng'] = ''
				else:
					new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES HMI Eng-BO-'+gesLocationVC)
			new_row.ApplyProductChanges()
			new_row.Calculate()
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
							if row.Deliverable in ['HMI Operator Interface Workshop', 'HMI Engineering Plan', 'HMI Customer Training']:
								cont_row['GES Eng'] = ''
							else:
								cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES HMI Eng-BO-'+gesLocationVC)
						applyChanges = 1
					if applyChanges:
						cont_row.ApplyProductChanges()
						cont_row.Calculate()
					break
	rows_to_delete.sort(reverse=True)
	Product.ExecuteRulesOnce = False
	Product.Attr('isProductLoaded').AssignValue('True')

	for x in rows_to_delete:
		laborCont.DeleteRow(x)
	laborCont.Calculate()