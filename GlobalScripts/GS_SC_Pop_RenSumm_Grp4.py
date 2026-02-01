#SESP, Enabled Services and Hardware Refresh
def get_training_match(Quote):
	scopechg = primpact= pylist= cylist = 0
	training_match = {}
	for item in Quote.MainItems:
		if item.PartNumber == "Year-1":
			for child in item.Children:
				for subchild in child.Children:
					escal_dis = []
					if subchild.PartNumber == "Training Match":
						scopechg = str(subchild.QI_SC_Scope_Change.Value)
						primpact = str(subchild.QI_SC_Price_Impact.Value)
						pylist = str(subchild.QI_SC_Previous_Year_List_Price.Value)
						cylist = str(subchild.ListPrice)
						escal_dis.extend([scopechg,primpact,pylist,cylist])
						training_match[subchild.PartNumber] = escal_dis
			return training_match
def fn_load_QuoteTable_Grp4(Quote,v_mod_name,item,v_child_dict,ProRatedFactor,ExchangeRateFactor = 1):

	if v_mod_name  == "SESP":
		platform_dict=v_child_dict
		training_match = get_training_match(Quote)
		Honeywell_List_Price = 0
		renewal_summary = Quote.QuoteTables["Renewal_Summary"]
		renewal_summary.Rows.Clear()
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		SC_Service_Product = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Service_Product'), '')
		if SC_Product_Type == "Renewal":
			comp_cont = item.SelectedAttributes.GetContainerByName('ComparisonSummary')
			PY_Sell_Price_SFDC = 0
			PY_List_Price_SFDC = 0
			if comp_cont.Rows.Count:
				for row in comp_cont.Rows:
					PY_Sell_Price_SFDC = row['PY_Sell_Price_SFDC'] if row['PY_Sell_Price_SFDC'] else '0'
					PY_List_Price_SFDC = row['PY_List_Price_SFDC'] if row['PY_List_Price_SFDC'] else '0'
					PY_Training_Match_SFDC = row['PY_Training_Match_SFDC'] if row['PY_Training_Match_SFDC'] else '0'
			cont = item.SelectedAttributes.GetContainerByName("SC_SESP Models Hidden")#SC_SESP Models_Renewal_Hidden
			SC_Pricing_Escalation = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Pricing_Escalation'), 'False')
			SC_ScopeRemoval = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_ScopeRemoval'), 'False')
			SC_ScopeRemoval_flag = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SESP_SC_ScopeRemoval_Flag'), 'False')
			if training_match:
				qt_row = renewal_summary.AddNewRow()
				qt_row['Platform'] = "Training Match Price_813"
				qt_row['SESP_Model'] = "TRNGMATCH"
				qt_row['Previous_Year_Quantity'] = 1 if PY_Training_Match_SFDC != "0" else 0
				qt_row['Renewal_Quantity']  = 1 if training_match["Training Match"][3] != "0" else 0
				try:
					qt_row['Previous_Year_Unit_Price'] = training_match["Training Match"][2]
					qt_row['Previous_Year_List_Price'] = training_match["Training Match"][2]
					qt_row['Final_List_Price'] = training_match["Training Match"][3]
					qt_row['Scope_Change'] = training_match["Training Match"][0]
					qt_row['Price_Impact'] = training_match["Training Match"][1]
				except:
					qt_row['Previous_Year_Unit_Price'] = 0
					qt_row['Previous_Year_List_Price'] = 0
					qt_row['Final_List_Price'] = 0
					qt_row['Scope_Change'] = 0
					qt_row['Price_Impact'] = 0
				qt_row['Final_Sell_Price'] = float(qt_row['Final_List_Price'])
				qt_row['Previous_Year_Sell_Price'] = float(qt_row['Previous_Year_List_Price'])
				qt_row['Comments'] = 'No Scope Change'
				if qt_row['Renewal_Quantity'] < qt_row['Previous_Year_Quantity']:
					qt_row['Comments'] = 'Scope Reduction'
				elif qt_row['Renewal_Quantity'] > qt_row['Previous_Year_Quantity']:
					qt_row['Comments'] = 'Scope Addition'
				for col in ['Asset_Validation_Line_Item_Number','MSID','System_Name','System_Number','Descrption']:
					qt_row[col] = ""
				for col in ['Honeywell_List_Price_Per_Unit','Escalation','Escalation_Value','Scope_Addition_Quantity','Scope_Addition_Price','Total_Discount','Scope_Reduction_Quantity','Scope_Reduction_Price','Last_Year_Discount','Total_Discount_Price']:
					qt_row[col] = "0"
				renewal_summary.Save()
			if SC_ScopeRemoval_flag == '1':
				if comp_cont.Rows.Count:
					for cs_row in comp_cont.Rows:
						qt_row = renewal_summary.AddNewRow()
						qt_row['Asset_Validation_Line_Item_Number'] = ""
						qt_row['MSID'] = cs_row['Service_Product']
						qt_row['System_Name'] = ""
						qt_row['System_Number'] = ""
						qt_row['Platform'] = ""
						qt_row['SESP_Model'] = ""
						qt_row['Descrption'] = "Scope Removed"
						qt_row['Previous_Year_Quantity'] = 1
						qt_row['Previous_Year_Unit_Price'] = float(cs_row['PY_List_Price_SFDC']) * ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Previous_Year_List_Price'] = float(cs_row['PY_List_Price_SFDC']) * ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Scope_Reduction_Quantity'] = 1
						qt_row['Scope_Reduction_Price'] = (-1)*(float(cs_row['PY_List_Price_SFDC']) * ProRatedFactor) if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Last_Year_Discount'] = float(cs_row['PY_Discount_SFDC'])*100 if cs_row['PY_Discount_SFDC'] else 0
						qt_row['Previous_Year_Sell_Price'] = float(cs_row['PY_Sell_Price_SFDC']) * ProRatedFactor if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Scope_Change'] = str(round(-float(cs_row['PY_Sell_Price_SFDC'])* ProRatedFactor,2)) if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Comments'] = "Scope Reduction"
						for col in ['Renewal_Quantity','Scope_Addition_Quantity','Honeywell_List_Price_Per_Unit','Honeywell_List_Price','Escalation','Total_Discount','Scope_Addition_Price','Escalation_Value','Final_List_Price','Total_Discount_Price','Final_Sell_Price','Price_Impact']:
							qt_row[col] = 0
					renewal_summary.Save()
			else:
				if cont.Rows.Count:
					for ct_row in cont.Rows:
						SR = SA = 0
						qt_row = renewal_summary.AddNewRow()
						qt_row['Asset_Validation_Line_Item_Number'] = ct_row['Asset Validation Line Item Number']
						qt_row['MSID'] = ct_row['MSID']
						qt_row['System_Name'] = ct_row['System_Name']
						qt_row['System_Number'] = ct_row['System_Number']
						qt_row['Platform'] = ct_row['Platform']
						qt_row['SESP_Model'] = ct_row['Model#']
						qt_row['Descrption'] = ct_row['Description']
						qt_row['Previous_Year_Quantity'] = ct_row['Qty'] if ct_row['Qty']!='' else 0
						qt_row['Renewal_Quantity'] = ct_row['Renewal Quantity'] if ct_row['Renewal Quantity']!='' else 0
						qt_row['Scope_Addition_Quantity'] =	 ct_row['Scope Addition Quantity']	if ct_row['Scope Addition Quantity']!='' else 0
						if ct_row['Previous Year Unit Price'] is not None:
							qt_row['Previous_Year_Unit_Price'] = float(ct_row['Previous Year Unit Price']) * ProRatedFactor if ct_row['Previous Year Unit Price'] != "" else 0
						qt_row['Previous_Year_List_Price'] = float(ct_row['Previous Year List Price']) * ProRatedFactor if ct_row['Previous Year List Price'] != "" else 0
						Trace.Write('hey'+str(ct_row['Honeywell List Price Per Unit']))
						qt_row['Honeywell_List_Price_Per_Unit'] = float(ct_row['Honeywell List Price Per Unit']) * ProRatedFactor
						if qt_row["Honeywell_List_Price_Per_Unit"] not in ['', 0] and qt_row["Renewal_Quantity"] not in ['', 0]:
							qt_row['Honeywell_List_Price'] = str(float(qt_row['Honeywell_List_Price_Per_Unit']) * float(qt_row['Renewal_Quantity']))
						else:
							qt_row['Honeywell_List_Price'] = 0

						try:
							qt_row['Escalation'] = platform_dict[ct_row['Platform']][0]
							qt_row['Total_Discount'] = platform_dict[ct_row['Platform']][1]
						except:
							qt_row['Escalation'] = 0
							qt_row['Total_Discount'] = 0
						if float(PY_List_Price_SFDC):
							qt_row['Last_Year_Discount'] = ((1 - (float(PY_Sell_Price_SFDC)/float(PY_List_Price_SFDC)))*100)
						Honeywell_List_Price = float(ct_row['Honeywell List Price Per Unit']) * float(ct_row['Renewal Quantity'])  * ProRatedFactor
						qt_row['Scope_Reduction_Quantity'] = ct_row['Scope Reduction Quantity']
						if qt_row['Previous_Year_Quantity'] != 0:
							qt_row['Scope_Reduction_Price'] = (qt_row['Scope_Reduction_Quantity'] * (qt_row['Previous_Year_List_Price']/qt_row['Previous_Year_Quantity']))
						else:
							qt_row['Scope_Reduction_Price'] = 0
						qt_row['Scope_Addition_Price'] = (qt_row['Scope_Addition_Quantity'] * qt_row['Honeywell_List_Price_Per_Unit'])
						if SC_Pricing_Escalation == "No":
							qt_row['Escalation_Value'] = 0
							qt_row['Final_List_Price'] = Honeywell_List_Price
						elif SC_Pricing_Escalation == "Yes":
							if qt_row['Renewal_Quantity'] <= 0:
								qt_row['Escalation_Value'] = 0
							elif qt_row['Renewal_Quantity'] > qt_row['Previous_Year_Quantity']:
								qt_row['Escalation_Value'] = ((qt_row['Escalation']) / 100 * qt_row['Previous_Year_Quantity'] * qt_row['Previous_Year_Unit_Price'])
							else:
								qt_row['Escalation_Value'] = ((qt_row['Escalation']) / 100 * qt_row['Renewal_Quantity'] * qt_row['Previous_Year_Unit_Price'])
							qt_row['Final_List_Price'] = (qt_row['Previous_Year_List_Price'] + qt_row['Scope_Reduction_Price'] + qt_row['Escalation_Value'] + qt_row['Scope_Addition_Price'])*ExchangeRateFactor
						qt_row['Previous_Year_Sell_Price'] = (qt_row['Previous_Year_List_Price'] - ((qt_row['Last_Year_Discount'] * qt_row['Previous_Year_List_Price']) / 100))
						qt_row['Total_Discount_Price'] = (qt_row['Final_List_Price'] * (qt_row['Total_Discount']/100))
						qt_row['Final_Sell_Price'] = (qt_row['Final_List_Price'] - qt_row['Total_Discount_Price'])
						if qt_row['Previous_Year_List_Price'] != 0:
							SR = qt_row['Scope_Reduction_Price'] * (qt_row['Previous_Year_Sell_Price'] / qt_row['Previous_Year_List_Price'])
						if qt_row['Final_List_Price'] != 0:
							SA =  qt_row['Scope_Addition_Price'] * (qt_row['Final_Sell_Price']/qt_row['Final_List_Price'])
						if SC_Service_Product == SC_ScopeRemoval:
							qt_row['Scope_Change'] = (-1) * qt_row['Previous_Year_Sell_Price']
						else:
							qt_row['Scope_Change'] = SA + SR
						qt_row['Price_Impact'] = qt_row['Final_Sell_Price'] - (qt_row['Scope_Change'] + qt_row['Previous_Year_Sell_Price'])
						qt_row['Comments'] = ct_row['Comments']
					renewal_summary.Save()
		elif SC_Product_Type == "New":
			cont = item.SelectedAttributes.GetContainerByName("SC_SESP Models Hidden")
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					qt_row = renewal_summary.AddNewRow()
					qt_row['MSID'] = ct_row['MSID']
					qt_row['System_Name'] = ct_row['System_Name']
					qt_row['System_Number'] = ct_row['System_Number']
					qt_row['Platform'] = ct_row['Platform']
					qt_row['SESP_Model'] = ct_row['Model#']
					qt_row['Descrption'] = ct_row['Description']
					qt_row['Previous_Year_Quantity'] = 0
					qt_row['Renewal_Quantity'] = ct_row['Qty'] if ct_row['Qty']!='' else 0
					qt_row['Previous_Year_List_Price'] = 0
					qt_row['Honeywell_List_Price_Per_Unit'] = float(ct_row['Price']) * ProRatedFactor
					qt_row['Honeywell_List_Price'] = str(float(qt_row['Honeywell_List_Price_Per_Unit']) * float(qt_row['Renewal_Quantity']) * ProRatedFactor)
					qt_row['Escalation'] = 0
					qt_row['Last_Year_Discount'] = 0
					qt_row['Escalation_Value'] = 0
					qt_row['Scope_Reduction_Quantity'] = 0
					qt_row['Scope_Reduction_Price'] = 0
					qt_row['Scope_Change'] = 0
					try:
						qt_row['Total_Discount'] = platform_dict[ct_row['Platform']][1]
					except:
						qt_row['Total_Discount'] = 0

					if int(qt_row['Renewal_Quantity']) > int(qt_row['Previous_Year_Quantity']):
						qt_row['Scope_Addition_Quantity'] = float(qt_row['Renewal_Quantity']) - int(qt_row['Previous_Year_Quantity'])
					else:
						qt_row['Scope_Addition_Quantity'] = 0

					qt_row['Scope_Addition_Price'] = (qt_row['Scope_Addition_Quantity'] * qt_row['Honeywell_List_Price_Per_Unit'])

					qt_row['Final_List_Price'] = (qt_row['Previous_Year_List_Price'] + qt_row['Scope_Reduction_Price'] + qt_row['Escalation_Value'] + qt_row['Scope_Addition_Price'])
					qt_row['Previous_Year_Sell_Price'] = 0
					qt_row['Total_Discount_Price'] = (qt_row['Final_List_Price'] * (qt_row['Total_Discount']/100))
					qt_row['Final_Sell_Price'] = (qt_row['Final_List_Price'] - qt_row['Total_Discount_Price'])
					qt_row['Scope_Change'] = qt_row['Final_Sell_Price']
					qt_row['Price_Impact'] = 0
					qt_row['Comments'] = "Scope Addition"
				renewal_summary.Save()
	if v_mod_name in ['Enabled Services', 'SESP']:
		es_child_dict=v_child_dict
		es_renewal_summary = Quote.QuoteTables["SC_ES_Renewal_Summary"]
		es_renewal_summary.Rows.Clear()
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		Service_Product = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'EnabledService_Entitlement'), 'NA')
		if SC_Product_Type == "Renewal" and Service_Product != 'NA':
			cont = item.SelectedAttributes.GetContainerByName("ES_Asset_Summary")
			SC_Pricing_Escalation = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Pricing_Escalation'),"None")
			comp_cont = item.SelectedAttributes.GetContainerByName('ESComparisonSummary')
			PY_Sell_Price_SFDC = 0
			PY_List_Price_SFDC = 0
			PY_Service_Product = ''
			if comp_cont.Rows.Count:
				for row in comp_cont.Rows:
					PY_Sell_Price_SFDC = row['PY_Sell_Price_SFDC'] if row['PY_Sell_Price_SFDC'] else '0'
					PY_List_Price_SFDC = row['PY_List_Price_SFDC'] if row['PY_List_Price_SFDC'] else '0'
					PY_Service_Product = row['Service_Product']
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					qt_row = es_renewal_summary.AddNewRow()
					qt_row['Service_Product'] = Service_Product
					qt_row['No_MSID_PY'] = ct_row['No_MSID_PY'] if ct_row['No_MSID_PY'] != "" else 0
					qt_row['No_MSID_CY'] = ct_row['No_MSID_CY'] if ct_row['No_MSID_CY'] != "" else 0
					qt_row['PY_List_Price'] = float(ct_row['PY_List_Price']) * ProRatedFactor if ct_row['PY_List_Price'] != "" else 0
					qt_row['CY_List_Price'] = float(ct_row['CY_List_Price']) * ProRatedFactor if ct_row['CY_List_Price'] != "" else 0
					qt_row['Scope_Reduction_Price'] = 0
					if float(ct_row['CY_List_Price']) < float(ct_row['PY_List_Price']):
						qt_row['Scope_Reduction_Price'] = (float(ct_row['CY_List_Price']) - float(ct_row['PY_List_Price']))  * ProRatedFactor
					qt_row['Scope_Addition_Price'] = 0
					if float(ct_row['CY_List_Price']) > float(ct_row['PY_List_Price']):
						qt_row['Scope_Addition_Price'] = (float(ct_row['CY_List_Price']) - float(ct_row['PY_List_Price'])) * ProRatedFactor
					try:
						part_number = es_child_dict.keys()[0]
						qt_row['Escalation_Percentage'] = float(es_child_dict[part_number][0])
						qt_row['Total_Discount_Percentage'] = float(es_child_dict[part_number][1])
						#qt_row['Last_Year_Discount_Percentage'] = float(es_child_dict[part_number][2])
					except:
						qt_row['Escalation_Percentage'] = 0
						qt_row['Total_Discount_Percentage'] = 0
						qt_row['Last_Year_Discount_Percentage'] = 0
					if float(PY_List_Price_SFDC):
						qt_row['Last_Year_Discount_Percentage'] = str((1 - (float(PY_Sell_Price_SFDC)/float(PY_List_Price_SFDC)))*100)
					if SC_Pricing_Escalation == "No":
						qt_row['Escalation_Value'] = 0
						qt_row['Final_List_Price'] = (qt_row['CY_List_Price'])  * ProRatedFactor
					else:
						qt_row['Escalation_Value'] = ((qt_row['Escalation_Percentage'] / 100.0) * (qt_row['PY_List_Price'] - qt_row['Scope_Reduction_Price']))
						qt_row['Final_List_Price'] = (qt_row['PY_List_Price'] + qt_row['Scope_Reduction_Price'] + qt_row['Scope_Addition_Price'] + qt_row['Escalation_Value'])
					qt_row['Total_Discount_Price'] = (qt_row['Final_List_Price'] * (qt_row['Total_Discount_Percentage']/100.0))
					qt_row['PY_Sell_Price'] = (qt_row['PY_List_Price'] * ( 1 - (qt_row['Last_Year_Discount_Percentage']/ 100.0)))
					qt_row['Final_Sell_Price'] = (qt_row['Final_List_Price'] - qt_row['Total_Discount_Price']) 
					if qt_row['CY_List_Price'] == 0:
						qt_row['Scope_Change_Price'] =(-1) * qt_row['PY_Sell_Price']
					else:
						if qt_row['PY_List_Price'] == 0:
							qt_row['Scope_Change_Price'] =	qt_row['Scope_Addition_Price'] * (qt_row['Final_Sell_Price'] / qt_row['Final_List_Price'])
						else:
							qt_row['Scope_Change_Price'] =	qt_row['Scope_Addition_Price'] * (qt_row['Final_Sell_Price'] / qt_row['Final_List_Price']) + qt_row['Scope_Reduction_Price'] * (qt_row['PY_Sell_Price']/qt_row['PY_List_Price'])
					qt_row['Price_Impact'] = qt_row['Final_Sell_Price'] - (qt_row['Scope_Change_Price'] + qt_row['PY_Sell_Price'])
					qt_row['Comment'] = 'No Scope Change'
					if qt_row['Scope_Change_Price'] < 0:
						qt_row['Comment'] = 'Scope Reduction'
					elif qt_row['Scope_Change_Price'] > 0:
						qt_row['Comment'] = 'Scope Addition'
				if PY_Service_Product != '' and PY_Service_Product != Service_Product:
					PY_List_Price = float(PY_List_Price_SFDC)
					PY_Sell_Price = float(PY_Sell_Price_SFDC)
					py_asset_detail_cont = item.SelectedAttributes.GetContainerByName('ES_PY_Asset_Details')
					qt_row = es_renewal_summary.AddNewRow()
					qt_row['Service_Product'] = PY_Service_Product
					qt_row['No_MSID_PY'] = py_asset_detail_cont.Rows.Count
					qt_row['No_MSID_CY'] = "0"
					qt_row['PY_List_Price'] = PY_List_Price  * ProRatedFactor
					qt_row['PY_Sell_Price'] = PY_Sell_Price  * ProRatedFactor
					qt_row['Scope_Reduction_Price'] = (-1) * PY_List_Price  * ProRatedFactor
					qt_row['Scope_Change_Price'] = (-1) * PY_Sell_Price  * ProRatedFactor
					for col in ['CY_List_Price',  'Scope_Addition_Price', 'Escalation_Percentage','Total_Discount_Percentage', 'Last_Year_Discount_Percentage', 'Final_List_Price', 'Final_Sell_Price']:
						qt_row[col] = 0
					qt_row['Comment'] = 'Scope Reduction'
		elif SC_Product_Type == "New":
			contName = ''
			ct = 0
			if item.PartNumber == 'Enabled Services':
				contName = 'Asset_details_ServiceProd'
			elif item.PartNumber == 'SESP' and	Service_Product != 'NA':
				contName = 'Asset_details_ServiceProd_ReadOnly'
			if contName != '':
				cont = item.SelectedAttributes.GetContainerByName(contName)
				ct = cont.Rows.Count
			if ct:
				cy_list_price = 0
				for r in cont.Rows:
					cy_list_price += float(r['List Price'])
				qt_row = es_renewal_summary.AddNewRow()
				qt_row['Service_Product'] = Service_Product
				qt_row['No_MSID_PY'] = 0
				qt_row['No_MSID_CY'] = ct
				qt_row['PY_List_Price'] = 0
				qt_row['CY_List_Price'] = cy_list_price  * ProRatedFactor
				qt_row['Scope_Reduction_Price'] = 0
				qt_row['Scope_Addition_Price'] = float(qt_row['CY_List_Price']) * ProRatedFactor
				qt_row['Escalation_Percentage'] = 0
				qt_row['Last_Year_Discount_Percentage'] = 0
				try:
					part_number = es_child_dict.keys()[0]
					qt_row['Total_Discount_Percentage'] = float(es_child_dict[part_number][1])
				except:
					qt_row['Total_Discount_Percentage'] = 0
				qt_row['Escalation_Value'] = 0
				qt_row['Final_List_Price'] = float(qt_row['CY_List_Price'])
				qt_row['Total_Discount_Price'] = (qt_row['Final_List_Price'] * (qt_row['Total_Discount_Percentage']/100.0))
				qt_row['PY_Sell_Price'] = 0
				qt_row['Final_Sell_Price'] = (qt_row['Final_List_Price'] - qt_row['Total_Discount_Price'])
				qt_row['Scope_Change_Price'] =	qt_row['Final_Sell_Price']
				qt_row['Price_Impact'] = 0
				qt_row['Comment'] = 'No Scope Change'
				if qt_row['Scope_Change_Price'] < 0:
					qt_row['Comment'] = 'Scope Reduction'
				elif qt_row['Scope_Change_Price'] > 0:
					qt_row['Comment'] = 'Scope Addition'
		es_renewal_summary.Save()
	if v_mod_name == "Hardware Refresh":
		hr_child_dict=v_child_dict
		hr_renewal_summary = Quote.QuoteTables["Hardware_Refresh_Renewal_Summary"]
		hr_renewal_summary.Rows.Clear()
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		SC_Pricing_Escalation = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Pricing_Escalation'), '')
		if SC_Product_Type == "Renewal":
			cont = item.SelectedAttributes.GetContainerByName("SC_ModelsHiddenSS_HR_RWL")
			compCont = item.SelectedAttributes.GetContainerByName("ComparisonSummary")
			if compCont.Rows.Count:
				for cs_row in compCont.Rows:
					if cs_row.IsSelected == True and not cont:
						qt_row = hr_renewal_summary.AddNewRow()
						qt_row["Asset"]=''
						qt_row["Model"] = cs_row['Service_Product'] 
						qt_row["Description"] = "Scope Removed"
						qt_row["PreviousYearQuantity"]= 1
						qt_row['PreviousYearUnitPrice'] = float(cs_row['PY_List_Price_SFDC'])* ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['PreviousYearListPrice'] = float(cs_row['PY_List_Price_SFDC']) * ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['ScopeReductionQuantity'] = -1
						qt_row['ScopeReductionPrice'] = ((-1)*float(cs_row['PY_List_Price_SFDC']))* ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['LastYearDiscountPer'] = (float(cs_row['PY_Discount_SFDC'])*100) if cs_row['PY_Discount_SFDC'] else 0
						qt_row['PreviousYearSellPrice'] = float(cs_row['PY_Sell_Price_SFDC']) * ProRatedFactor if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['ScopeChange'] = str((round(-float(cs_row['PY_Sell_Price_SFDC']),2))* ProRatedFactor) if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Previous_Year_Cost_Price'] = str(round((1-float(cs_row['Booked_Margin'])/100) *float(cs_row["PY_Sell_Price_SFDC"]),2)* ProRatedFactor) if cs_row["PY_Sell_Price_SFDC"] else "0"
						qt_row['Previous_Year_Unit_Cost_Price']=str(round(float(qt_row['Previous_Year_Cost_Price']),2))
						qt_row['Comments'] = "Scope Reduction"
						for col in ['RenewalQuantity','HoneywellListPricePerUnit','Current_Year_List_Price','ScopeAdditionQuantity','ScopeAdditionPrice','EscalationPercentage','TotalDiscountPer','EscalationValue','FinalListPrice','TotalDiscountPrice','FinalSellPrice','PriceImpact','Current_Year_Unit_Cost_Price','MarginPercentage','Current_Year_Cost_Price']:
							qt_row[col] = 0
			if cont:
				if cont.Rows.Count:
					for ct_row in cont.Rows:
						qt_row = hr_renewal_summary.AddNewRow()
						qt_row["Asset"] = ct_row["Asset"]
						qt_row["Model"] = ct_row["Model"]
						qt_row["Description"] = ct_row["Description"]
						qt_row["PreviousYearQuantity"] = ct_row["PreviousYearQuantity"]
						qt_row["RenewalQuantity"] = ct_row["RenewalQuantity"]
						qt_row["PreviousYearUnitPrice"] = float(ct_row["PreviousYearUnitPrice"])* ProRatedFactor
						qt_row["PreviousYearListPrice"] = float(ct_row["PreviousYearListPrice"])* ProRatedFactor
						qt_row["HoneywellListPricePerUnit"] = float(ct_row["HoneywellListPricePerUnit"])* ProRatedFactor
						qt_row["ScopeReductionQuantity"] = ct_row["ScopeReductionQuantity"]
						qt_row["ScopeReductionPrice"] =  float(ct_row["ScopeReductionPrice"])* ProRatedFactor
						try:
							EscalationPercentage = hr_child_dict['Hardware Refresh'][0] if hr_child_dict['Hardware Refresh'][0] else 0.00
						except:
							EscalationPercentage=0.00
						qt_row["EscalationPercentage"] = str(round(float(EscalationPercentage),2))
						if ct_row["Comments"] in ["Scope Reduction","No Scope Change"]:
							EscalationValue = round((float(float(EscalationPercentage)/100) * int(float(ct_row["RenewalQuantity"])) * (float(ct_row["PreviousYearUnitPrice"]))* ProRatedFactor),2)
						else:
							EscalationValue = round((float(float(EscalationPercentage)/100) * int(float(ct_row["PreviousYearQuantity"])) * (float(ct_row["PreviousYearUnitPrice"]))* ProRatedFactor),2)
						qt_row["EscalationValue"] = str(EscalationValue)
						qt_row["ScopeAdditionQuantity"] = ct_row["ScopeAdditionQuantity"]
						ScopeReductionPrice = float(ct_row["ScopeReductionPrice"])* ProRatedFactor
						ScopeAdditionPrice = float(ct_row["ScopeAdditionPrice"])* ProRatedFactor
						FinalListPrice = round(((float(ct_row["PreviousYearListPrice"])* ProRatedFactor) + EscalationValue + ScopeReductionPrice + ScopeAdditionPrice),2)
						qt_row["FinalListPrice"] = str(FinalListPrice)
						if SC_Pricing_Escalation=="No":
							qt_row["EscalationValue"] = '0'
							FinalListPrice = round(float(ct_row['Sc_CurrentYearListPrice_HR_RWL']),2)* ProRatedFactor
						qt_row["FinalListPrice"] = FinalListPrice
						LastYearDiscountPer = str(float(ct_row['LastYearDiscountPer']))
						qt_row["LastYearDiscountPer"] = str(LastYearDiscountPer)
						try:
							TotalDiscountPer = hr_child_dict['Hardware Refresh'][1] if hr_child_dict['Hardware Refresh'][1] else 0.00
						except:
							TotalDiscountPer=0.00
						qt_row["TotalDiscountPer"] = str(round(float(TotalDiscountPer),2))
						TotalDiscountPrice = round(float(qt_row["FinalListPrice"]) * (float(TotalDiscountPer)/100),2)
						qt_row["TotalDiscountPrice"] = str(TotalDiscountPrice)
						PreviousYearSellPrice = float(ct_row["PreviousYearSellPrice"])* ProRatedFactor
						qt_row["PreviousYearSellPrice"] = (PreviousYearSellPrice-(PreviousYearSellPrice  % 0.01)) if LastYearDiscountPer!="0.0" else qt_row["PreviousYearListPrice"]
						FinalSellPrice = round(float(qt_row["FinalListPrice"])* (1-(float(TotalDiscountPer)/100)),2)
						Trace.Write("FinalSellPrice : "+str(FinalSellPrice))
						qt_row["FinalSellPrice"] = str(FinalSellPrice)
						ScopeChange = 0
						if float(qt_row["FinalListPrice"]) != 0 and float(ct_row["PreviousYearListPrice"]) != 0:
							ScopeChange = round((ScopeReductionPrice * (PreviousYearSellPrice/(float(ct_row["PreviousYearListPrice"])* ProRatedFactor))) + (ScopeAdditionPrice*(FinalSellPrice/float(qt_row["FinalListPrice"]))),2)
						if qt_row['RenewalQuantity'] == '0':
							ScopeChange =round((-1) * float(qt_row['PreviousYearSellPrice']),2)
							Trace.Write("Lahu>>>>>>>>>>>>>>>>>>>: "+str(qt_row['PreviousYearSellPrice']))
						qt_row["ScopeChange"] = str(ScopeChange)
						PriceImpact = round(FinalSellPrice - (ScopeChange + PreviousYearSellPrice),2)
						qt_row["PriceImpact"] = str(PriceImpact)
						qt_row["Comments"] = ct_row["Comments"]
						qt_row["ScopeAdditionPrice"] = float(ct_row["ScopeAdditionPrice"])* ProRatedFactor
						qt_row['Previous_Year_Unit_Cost_Price'] = str(float(ct_row['PreviousYearUnitCostPrice'])* ProRatedFactor)
						qt_row['Previous_Year_Cost_Price'] = str(float(ct_row['PreviousYearCostPrice'])* ProRatedFactor)
						qt_row['Current_Year_List_Price'] = str(float(ct_row['Sc_CurrentYearListPrice_HR_RWL'])* ProRatedFactor)
						qt_row['Current_Year_Unit_Cost_Price'] = str(float(ct_row['SC_CurrentYearUnitCostPrice_HR_RWL'])* ProRatedFactor)
						qt_row['Current_Year_Cost_Price'] = str(float(ct_row['SC_CurrentYearCostPrice_HR_RWL'])* ProRatedFactor)
						if FinalSellPrice != 0:
							qt_row['MarginPercentage'] = str(round((1-(float(qt_row['Current_Year_Cost_Price']) / FinalSellPrice))*100,2))
							Trace.Write(str(round((1-(float(qt_row['Current_Year_Cost_Price']) / FinalSellPrice))*100,2)))
						else:
							qt_row['MarginPercentage'] ="0.0"
				hr_renewal_summary.Save()
		elif SC_Product_Type == 'New':
			cont = item.SelectedAttributes.GetContainerByName("HWOS_Model Scope_3party")
			#hr_renewal_summary.GetColumnByName('Asset').AccessLevel = hr_renewal_summary.AccessLevel.Hidden
			for i in cont.Rows:
				qt_row = hr_renewal_summary.AddNewRow()
				qt_row["Asset"] = i['Asset']
				qt_row["Current_Year_Unit_Cost_Price"] = float(i['Unit Cost'])* ProRatedFactor
				qt_row["HoneywellListPricePerUnit"] = float(i['Unit List Price'])* ProRatedFactor
				qt_row["RenewalQuantity"] = i['Quantity']
				qt_row["Description"] = i['Description']
				qt_row["Model"] = i['3rd Party Model']
				qt_row["PreviousYearQuantity"] = 0
				qt_row["PreviousYearUnitPrice"] = 0
				qt_row["PreviousYearListPrice"] = 0
				qt_row['Previous_Year_Unit_Cost_Price'] = 0
				qt_row['Previous_Year_Cost_Price'] = 0
				qt_row["ScopeReductionQuantity"] = 0
				qt_row["ScopeReductionPrice"] = 0
				qt_row["LastYearDiscountPer"] = 0
				qt_row["PreviousYearSellPrice"] = 0
				try:
					EscalationPercentage = float(hr_child_dict['Hardware Refresh'][0]) if hr_child_dict['Hardware Refresh'][0] else 0.00
				except:
					EscalationPercentage = 0.00
				qt_row["EscalationPercentage"] = str(round(float(EscalationPercentage),2))
				qt_row["PriceImpact"] = 0
				EscalationValue = float(float(EscalationPercentage)/100) * int(float(qt_row["RenewalQuantity"])) * float(qt_row["HoneywellListPricePerUnit"])
				qt_row["EscalationValue"] = str(EscalationValue)
				FinalListPrice = (float(i['List Price'])* ProRatedFactor) + EscalationValue
				qt_row["FinalListPrice"] = str(FinalListPrice)
				try:
					TotalDiscountPer = float(hr_child_dict['Hardware Refresh'][1]) if hr_child_dict['Hardware Refresh'][1] else 0.00
				except:
					TotalDiscountPer =0.00
				qt_row["TotalDiscountPer"] = str(round(float(TotalDiscountPer),2))
				qt_row['Current_Year_Cost_Price'] = str(float(qt_row["Current_Year_Unit_Cost_Price"]) * float(qt_row["RenewalQuantity"]))
				TotalDiscountPrice = FinalListPrice * (float(TotalDiscountPer)/100)
				qt_row["TotalDiscountPrice"] = str(TotalDiscountPrice)
				qt_row['Current_Year_List_Price'] = str(float(qt_row["HoneywellListPricePerUnit"]) * float(qt_row["RenewalQuantity"]))
				FinalSellPrice = str(float(qt_row["FinalListPrice"]) * (1-(float(TotalDiscountPer)/100)))
				qt_row["FinalSellPrice"] = str(FinalSellPrice)
				qt_row["ScopeAdditionQuantity"] = qt_row["RenewalQuantity"]
				qt_row["ScopeAdditionPrice"] = float(qt_row["ScopeAdditionQuantity"]) * float(qt_row["HoneywellListPricePerUnit"])
				if qt_row["FinalSellPrice"] != 0:
					qt_row['MarginPercentage'] = round((1 - (qt_row['Current_Year_Cost_Price']/qt_row['FinalSellPrice'])) * 100,2)
				qt_row["Comments"] = "Scope Addition"
				qt_row["ScopeChange"] = qt_row["FinalSellPrice"]
			hr_renewal_summary.Save()