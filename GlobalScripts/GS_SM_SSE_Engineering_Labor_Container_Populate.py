#GS_SM_SSE_Engineering_Labor_Container_Populate
import datetime
from GS_Exp_Ent_Sys_Add_To_Quote import sortRow
scope = Product.Attr('CE_Scope_Choices').GetValue()
if scope == 'HW/SW + LABOR':
	##Product.ExecuteRulesOnce = True #This is to improve performance. We keep triggering product rules execution with each change to each container cell. Sets back to False at end of script.
	salesArea = Quote.GetCustomField('Sales Area').Content
	marketCode = Quote.SelectedMarket.MarketCode
	salesOrg = Quote.GetCustomField('Sales Area').Content
	#Updated logic for Defect 29879
	currency = Quote.GetCustomField('Currency').Content
	query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
	#query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))

	disallow_lst = []
	process_type = Product.Attr('Labor_Site_Activities').GetValue()
	if process_type != "Yes":
		disallow_lst.append("SSE Site Installation-Base")
		disallow_lst.append("SSE Site Installation")
		disallow_lst.append("SSE SAT and Sign Off")
		disallow_lst.append("SSE Close Out Report")
	process_type1 = Product.Attr('Labor_Operation_Manual_Scope').GetValue()
	if process_type1 != "Yes":
		disallow_lst.append("SSE Operation Manual for Safety System")
	process_type2 = Product.Attr('Labor_Custom_Scope').GetValue()
	if process_type2 != "Yes":
		disallow_lst.append("SSE Customer Training for Safety System")
	if Product.Attr('New_Expansion').GetValue() == 'Expansion':
		if Product.Attr('CE_Cutover').GetValue() != 'Yes':
			disallow_lst.append("SSE Cut Over Procedure")
	else:
		disallow_lst.append("SSE Cut Over Procedure")
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
	laborCont=''
	gesLocation = ''
	gesMapping = {'GESIndia':'IN','GESChina':'CN','GESRomania':'RO','GESUzbekistan':'UZ','None':'None'}
	if Product.GetContainerByName('SM_Labor_Cont').Rows.Count > 0:
		gesLocation = Product.GetContainerByName('SM_Labor_Cont').Rows[0].GetColumnByName('GES_Location').Value
		if (not gesLocation or gesLocation == 'None') and Quote.GetCustomField("R2QFlag").Content and Quote.GetGlobal('ExGesLocation'):
			gesLocation = gesMapping.keys()[gesMapping.values().index(Quote.GetGlobal('ExGesLocation'))]

	gesLocationVC = gesMapping.get(gesLocation)
	gesEmptyDel = ['SSE User Requirement Specification', 'SSE Engineering Plan', 'SSE Customer Training for Safety System', 'SSE Close Out Report', 'SSE Procure Material & Services']

	if Product.Attr('SM_Product_Name').GetValue() == Product.Name:
		laborCont = Product.GetContainerByName('SM_SSE_Engineering_Labor_Container')
		tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from SAFETY_MANAGER_LABOR_SSE_ENGINEERING_LABOR')
		#gesLocation = Product.GetContainerByName('SM_Labor_Cont').Rows[0].GetColumnByName('GES_Location').Value
		Trace.Write("Prabhat"+str(gesLocation))

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
				if gesLocation == "None" or gesLocation == '':
					new_row["GES Eng % Split"]= row.GES_Eng_1_No
					# new_row["FO Eng 1"]= row.FO_Eng_1
					new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
					# new_row["FO Eng 2"]= row.FO_Eng_2
					new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
					new_row["Productivity"]= row.Productivity
					new_row["Calculated Hrs"]= row.Calculated_Hrs
					new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
					new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
					new_row["FO Eng 1"]= row.FO_Eng_1_NoGES
					new_row["FO Eng 2"]= row.FO_Eng_2_NoGES
				else:
					new_row["GES Eng % Split"]= row.GES_Eng
					# new_row["FO Eng 1"]= row.FO_Eng_1
					new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
					new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
					new_row["Productivity"]= row.Productivity
					new_row["Calculated Hrs"]= row.Calculated_Hrs
					new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
					new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
					new_row["FO Eng 1"]= row.FO_Eng_1_NoGES
					new_row["FO Eng 2"]= row.FO_Eng_2_NoGES
					if row.Deliverable in gesEmptyDel:
						new_row['GES Eng'] = ''
					else:
						new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
						new_row["GES Eng"]= 'SYS GES Eng-BO-'+gesLocationVC
				new_row.Calculate()
			elif row.Deliverable in disallow_lst and row.Deliverable in current_deliverables:
				for cont_row in laborCont.Rows:
					if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
						rows_to_delete.append(cont_row.RowIndex)
						break
		laborCont.Calculate()
		rows_to_delete.sort(reverse=True)
	laborCont1 = Product.GetContainerByName('SM Safety System - ESD/FGS/BMS/HIPPS Container')
	tableLabor1 = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from SAFETY_MANAGER_LABOR_SSE_ENGINEERING_LABOR_TWO')
	#gesLocation = Product.GetContainerByName('SM_Labor_Cont').Rows[0].GetColumnByName('GES_Location').Value
	#Trace.Write("Prabhat"+str(gesLocation))

	current_deliverables1 = []
	rows_to_delete1 = []
	for row in laborCont1.Rows:
		current_deliverables1.append(row.GetColumnByName('Deliverable').Value)

	for row in tableLabor1:
		if row.Deliverable not in disallow_lst and row.Deliverable not in current_deliverables1:
			new_row = laborCont1.AddNewRow(False)
			new_row["Deliverable"] = row.Deliverable
			new_row["Execution Year"] = str(contract_start)
			new_row["Rank"] = str(row.Rank)
			sortRow(laborCont1,row.Rank,new_row.RowIndex)
			if salesArea == "":
				new_row.GetColumnByName('Execution Country').Value = ""
			else:
				new_row.GetColumnByName('Execution Country').Value = query.Execution_County

			Trace.Write('gesLocation: '+str(gesLocation))
			if gesLocation == "None" or gesLocation == '':
				Trace.Write('gesLocation inside if : '+str(gesLocation))
				new_row["GES Eng % Split"]= row.GES_Eng_1_No
				# new_row["FO Eng 1"]= row.FO_Eng_1
				new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
				# new_row["FO Eng 2"]= row.FO_Eng_2
				new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
				new_row["Productivity"]= row.Productivity
				new_row["Calculated Hrs"]= row.Calculated_Hrs
				new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
				new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
				new_row["FO Eng 1"]= row.FO_Eng_1_NoGES
				new_row["FO Eng 2"]= row.FO_Eng_2_NoGES
			else:
				new_row["GES Eng % Split"]= row.GES_Eng
				Trace.Write('gesLocation inside else : '+str(gesLocation))
				# new_row["FO Eng 1"]= row.FO_Eng_1
				new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
				new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
				new_row["Productivity"]= row.Productivity
				new_row["Calculated Hrs"]= row.Calculated_Hrs
				new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
				new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
				new_row["FO Eng 1"]= row.FO_Eng_1_NoGES
				new_row["FO Eng 2"]= row.FO_Eng_2_NoGES
				if row.Deliverable in gesEmptyDel:
					new_row['GES Eng'] = ''
				else:
					new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
					new_row["GES Eng"]= 'SYS GES Eng-BO-'+gesLocationVC
			new_row.Calculate()
		elif row.Deliverable in disallow_lst and row.Deliverable in current_deliverables1:
			for cont_row in laborCont1.Rows:
				if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
					rows_to_delete1.append(cont_row.RowIndex)
					break
	laborCont1.Calculate()
	rows_to_delete1.sort(reverse=True)

	laborAddi = Product.GetContainerByName('SM_Additional_Custom_Deliverables_Labor_Container').Rows

	for row1 in laborAddi:
		#Trace.Write(row1['UpdatedYear'])
		if row1.GetColumnByName('Execution Country').Value == "" and salesArea != "":
			row1['Execution Country'] = query.Execution_County
		if row1.GetColumnByName('Execution Year').Value == "":
			row1["Execution Year"] = str(contract_start)
		if gesLocation == "None" or gesLocation == '':
			row1["FO Eng % Split"] = '100'
			row1["GES Eng % Split"] = '0'

	##Product.ExecuteRulesOnce = False

	Product.Attr('isProductLoaded').AssignValue('True')

	if Product.Attr('SM_Product_Name').GetValue() == Product.Name:
		for x in rows_to_delete:
			laborCont.DeleteRow(x)
	for x in rows_to_delete1:
		laborCont1.DeleteRow(x)