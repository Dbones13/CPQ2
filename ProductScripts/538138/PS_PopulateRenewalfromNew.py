if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
	Exchange_Rate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content else 1
	ScriptExecutor.Execute('PS_OPB_Popup_Message')
	summary_cont = Product.GetContainerByName("SC_Labor_Summary_Container")
	comparision_cont = Product.GetContainerByName('ComparisonSummary')
	Country = Quote.GetCustomField('Opportunity Tab Booking Country').Content
	if summary_cont.Rows.Count:
		for row in summary_cont.Rows:
			row.Product.Attr('SC_Renewal_check').AssignValue('0')
			row.Product.Attr('SC_Labor_Product_Type').AssignValue('0')
			row.Product.AllowAttr('SC_Labor_Contigency_Cost')
			row.Product.AllowAttr('SC_Labor_Pricing_Escalation_Based')
			row.Product.AllowAttr('SC_Labor_PY_Deliverables_Hours')
			row.GetColumnByName('PY_Service_Product').ReferencingAttribute.SelectDisplayValue(row['Service_Product'],False)
			row['PY_Service_Product'] = row['Service_Product']
			workhrs_query = SqlHelper.GetFirst("select Work_Hour from CT_SC_LABOR_RESOURCETYPE where Country = '{}' and Type = '{}'".format(Country,row['Resource_Type'].split(',')[-1].Trim()))
			row.GetColumnByName('PY_Entitlement').ReferencingAttribute.SelectDisplayValue(row['Entitlement'],False)
			row['PY_Entitlement'] = row['Entitlement']
			row.GetColumnByName('PY_Related_Module').ReferencingAttribute.SelectDisplayValue(row['Related Module'],False)
			row['PY_Related_Module'] = row['Related Module']
			row['PY_Resource_Type'] = row['Resource_Type']
			row.Product.Attr('SC_Labor_PY_ResourceType').AssignValue(row['PY_Resource_Type'])
			row['PY_Deliverables_Hours'] = row['Deliverable_Hours'] if row['Deliverable_Hours'] else '0'
			row.Product.Attr('SC_Labor_PY_Deliverables_Hours').AssignValue(row['PY_Deliverables_Hours'])
			row['Scope_Reduction_Quantity'] = '0'
			row['Scope_Addition_Quantity'] = '0'
			#row.Product.Attr('SC_Labor_PY_CustomerLP').AssignValue(row['Customer_List_Price'])
			#row['PY_UnitPrice'] = str((float(row['Honeywell_List_Price_Hidden']) / float(row['PY_Deliverables_Hours'])) * Exchange_Rate) if row['Honeywell_List_Price_Hidden'] else '0'
			#row['PY_ListPrice'] = str(float(row['Honeywell_List_Price_Hidden']) * Exchange_Rate) if row['Honeywell_List_Price_Hidden'] else '0'
			row['PY_Total_Expenses'] = str(float(row['Other_Expenses']) * Exchange_Rate) if row['Other_Expenses'] else '0'
			row['PY_Contigency_Cost'] = str(float(row['Contigency_Cost']) * Exchange_Rate) if row['Contigency_Cost'] else '0'
			if row.Product.Attr('SC_Labor_Resource_Type').GetValue() == "A360 Contract Management" or row.Product.Attr('SC_Labor_Resource_Type').GetValue() == "Service Contract Management":
				row.Product.Attr('SC_Labor_Pricing_Escalation_Based').SelectValue('No')
			if workhrs_query is not None:
				py_listprice = str(float(row['PY_UnitPrice']) * float(workhrs_query.Work_Hour))
				row.Product.Attr('SC_Labor_PY_CustomerLP').AssignValue(py_listprice)
			if row['PY_Contigency_Cost'] == "":
				row['PY_Total_Cost_Price'] = str(float(row['PY_Deliverables_Hours']) * round(float(row['BurdenRate']),2) * Exchange_Rate)
			else:
				row['PY_Total_Cost_Price'] = str(float(row['PY_Deliverables_Hours']) * round(float(row['BurdenRate']),2) * Exchange_Rate + float(row['PY_Contigency_Cost']))
			if row['Contigency_Cost'] == "":
				row['Final_Total_Cost_Price'] = str(float(row['Renewal_Year_Deliverables_Hours']) * round(float(row['BurdenRate']),2))
			else:
				row['Final_Total_Cost_Price'] = str(float(row['Renewal_Year_Deliverables_Hours']) * round(float(row['BurdenRate']),2) + float(row['Contigency_Cost']))
			if float(row['PY_Deliverables_Hours']) > float(row['Renewal_Year_Deliverables_Hours']):
				row['Scope_Reduction_Quantity'] = str(float(row['Renewal_Year_Deliverables_Hours']) - float(row['PY_Deliverables_Hours']))
				row['Scope_Addition_Quantity'] = '0'
				row['Comments'] = 'Scope Reduction'
			elif float(row['PY_Deliverables_Hours']) < float(row['Renewal_Year_Deliverables_Hours']):
				row['Scope_Addition_Quantity'] = str(float(row['Renewal_Year_Deliverables_Hours']) - float(row['PY_Deliverables_Hours']))
				row['Scope_Reduction_Quantity'] = '0'
				row['Comments'] = 'Scope Addition'
			else:
				row['Comments'] = 'No Scope Change'
				row['Scope_Addition_Quantity'] = '0'
				row['Scope_Reduction_Quantity'] = '0'
			row.Calculate()
			compDict = {}
			if comparision_cont.Rows.Count:
				for comp_row in comparision_cont.Rows:
					compDict[comp_row["Service_Product"]] = comp_row["PY_Discount_SFDC"] if comp_row["PY_Discount_SFDC"] else '0'
					py_discount = float(compDict.get(row['PY_Service_Product'],0))
					row["PY_Discount"] = str(py_discount * 100)
					row["PY_SellPrice"] = str(float(row['PY_ListPrice']) - (float(row['PY_ListPrice']) * py_discount))
					if row['PY_Service_Product'] == comp_row['Service_Product']:
						comp_row['Configured_PY_List_Price'] = str((float(row["PY_ListPrice"]) if row["PY_ListPrice"] else 0) + (float(row['PY_Total_Expenses']) if row['PY_Total_Expenses'] else 0))
						comp_row['Configured_PY_Sell_Price'] = str((float(row["PY_SellPrice"]) if row["PY_SellPrice"] else 0) + (float(row['PY_Total_Expenses']) if row['PY_Total_Expenses'] else 0))
						comp_row.Calculate()
	summary_cont.Calculate()
	delta = SqlHelper.GetFirst("select Value from SC_HARDCODE_VALUES where Name = 'Comparison Summary Delta Allowance (%)'")
	deltaFactor = eval(delta.Value)/100 if delta is not None else 0
	Product.Attr('SC_Labor_Popup_Msg').AssignValue('False')
	for row in comparision_cont.Rows:
		row['List_Price_Delta'] = row['List_Price_Delta'] if row['List_Price_Delta'] != '' else '0'
		row['Sell_Price_Delta'] = row['Sell_Price_Delta'] if row['Sell_Price_Delta'] != '' else '0'
		row['PY_List_Price_SFDC'] = row['PY_List_Price_SFDC'] if row['PY_List_Price_SFDC'] else '0'
		row['PY_Sell_Price_SFDC'] = row['PY_Sell_Price_SFDC'] if row['PY_Sell_Price_SFDC'] else '0'
		if abs(float(row['List_Price_Delta'])) > (deltaFactor*float(row['PY_List_Price_SFDC'])) or abs(float(row['Sell_Price_Delta'])) > (deltaFactor*float(row['PY_Sell_Price_SFDC'])):
			Product.Attr('SC_Labor_Popup_Msg').AssignValue('True')
	for row in summary_cont.Rows:
		if row['PY_Service_Product'] == "":
			row['PY_Total_Cost_Price'] = '0'

	sp_dict = {}
	if summary_cont.Rows.Count:
		for laborrow in summary_cont.Rows:
			laborrow['PY_ListPrice'] = laborrow['PY_ListPrice'] if laborrow['PY_ListPrice'] != "" else '0'
			laborrow['PY_SellPrice'] = laborrow['PY_SellPrice'] if laborrow['PY_SellPrice'] != "" else '0'
			if laborrow['PY_Service_Product'] not in sp_dict.keys():
				sp_dict[laborrow['PY_Service_Product']] = [str(float(laborrow['PY_ListPrice']) + (float(laborrow['PY_Total_Expenses']) if laborrow['PY_Total_Expenses'] else 0)),str(float(laborrow['PY_SellPrice']) + (float(laborrow['PY_Total_Expenses']) if laborrow['PY_Total_Expenses'] else 0))]
			else:
				lp = str(float(laborrow['PY_ListPrice']) + (float(laborrow['PY_Total_Expenses']) if laborrow['PY_Total_Expenses'] else 0) + float(sp_dict.get(laborrow['PY_Service_Product'])[0]))
				sp = str(float(laborrow['PY_SellPrice']) + (float(laborrow['PY_Total_Expenses']) if laborrow['PY_Total_Expenses'] else 0) + float(sp_dict.get(laborrow['PY_Service_Product'])[1]))
				sp_dict[laborrow['PY_Service_Product']] = [lp,sp]

	if comparision_cont.Rows.Count:
		for compRow in comparision_cont.Rows:
			if compRow["Service_Product"] in sp_dict.keys():
				compRow["Configured_PY_List_Price"] = sp_dict[compRow["Service_Product"]][0]
				compRow["Configured_PY_Sell_Price"] = sp_dict[compRow["Service_Product"]][1]
			compRow.Calculate()
		comparision_cont.Calculate()

	Product.Attr('SC_Renewal_check').AssignValue('1')