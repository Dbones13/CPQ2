#CBM, Parts Management, and Hardware Warranty
def fn_load_QuoteTable_Grp2(Quote,v_mod_name,item,v_child_dict,ProRatedFactor):
	if v_mod_name == "Condition Based Maintenance":
		CBM_child_dict=v_child_dict
		CBM_Renewal_Summary = Quote.QuoteTables["CBM_Renewal_Summary"]
		CBM_Renewal_Summary.Rows.Clear()
		Trace.Write("true")
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		SC_Pricing_Escalation = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Pricing_Escalation'), '')
		Trace.Write(SC_Product_Type)
		if SC_Product_Type == "Renewal":
			cont = item.SelectedAttributes.GetContainerByName("CBM_Models_Cont")
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					qt_row = CBM_Renewal_Summary.AddNewRow()
					if ct_row['CY_ListPrice'] == "":
						qt_row['Honeywell_List_Price_Per_Unit'] = 0
					else:
						qt_row['Honeywell_List_Price_Per_Unit'] = float(ct_row['CY_ListPrice'])*ProRatedFactor
					qt_row['Service_Product'] = ct_row['Service Product']
					qt_row['Product_Family'] = ct_row['Product Family']
					qt_row['Previous_Year_List_Price'] = float(ct_row['PY_ListPrice'])*ProRatedFactor if ct_row['PY_ListPrice'] != "" else 0
					if qt_row['Previous_Year_List_Price'] == "":
						qt_row['Previous_Year_List_Price'] = 0
					if qt_row['Previous_Year_List_Price'] > qt_row['Honeywell_List_Price_Per_Unit']:
						qt_row['Scope_Reduction_Price'] = qt_row['Honeywell_List_Price_Per_Unit'] - qt_row['Previous_Year_List_Price']
					elif qt_row['Previous_Year_List_Price'] < qt_row['Honeywell_List_Price_Per_Unit']:
						qt_row['Scope_Addition_Price'] =  qt_row['Honeywell_List_Price_Per_Unit'] - qt_row['Previous_Year_List_Price']
					try:
						Trace.Write(str(CBM_child_dict))
						qt_row['Escalation_'] = float(CBM_child_dict["Condition Based Maintenance"][0])
						qt_row['Total_Discount_'] = float(CBM_child_dict["Condition Based Maintenance"][1])
						Trace.Write("discount " + str (qt_row['Total_Discount_']))
						#qt_row['Last_Year_Discount_'] = float(CBM_child_dict["Condition Based Maintenance"][2])
						#Trace.Write("LY Discount " + str (float(CBM_child_dict["Condition Based Maintenance"][2])))
						qt_row['Last_Year_Discount_'] = float(ct_row['LY_Discount'])
					except :
						qt_row['Escalation_'] = 0
						qt_row['Total_Discount_'] = 0
						qt_row['Last_Year_Discount_'] = 0
					qt_row['Escalation_Value'] = qt_row['Escalation_'] * ((qt_row['Previous_Year_List_Price'] + qt_row['Scope_Reduction_Price'])/100) #adjusted Escalation value formula on 07/18/2023
					if SC_Pricing_Escalation == "No":
						qt_row['Escalation_Value'] = 0
					qt_row['Final_List_Price'] = qt_row['Previous_Year_List_Price']+qt_row['Escalation_Value']+qt_row['Scope_Reduction_Price']+qt_row['Scope_Addition_Price']
					if SC_Pricing_Escalation == "No":
						qt_row['Final_List_Price'] = qt_row['Honeywell_List_Price_Per_Unit']
					#qt_row['Previous_Year_Sell_Price'] = qt_row['Previous_Year_List_Price'] - ((qt_row['Previous_Year_List_Price']/100) * qt_row['Last_Year_Discount_'])
					qt_row['Previous_Year_Sell_Price'] = float(ct_row['PY_SellPrice'])*ProRatedFactor if ct_row['PY_SellPrice'] != '' else 0
					qt_row['Total_Discount_Price'] = qt_row['Total_Discount_'] * (qt_row['Final_List_Price']/100)
					qt_row['Final_Sell_Price'] = qt_row['Final_List_Price']	 - qt_row['Total_Discount_Price']
					if qt_row['Previous_Year_List_Price'] and qt_row['Final_List_Price']:
						qt_row['Scope_Change'] = (qt_row['Scope_Reduction_Price'] * (qt_row['Previous_Year_Sell_Price']/qt_row['Previous_Year_List_Price'])) + (qt_row['Scope_Addition_Price'] * (qt_row['Final_Sell_Price']/qt_row['Final_List_Price']))
					elif qt_row['Previous_Year_List_Price'] and qt_row['Final_List_Price'] == 0:
						qt_row['Scope_Change'] = (qt_row['Scope_Reduction_Price'] * (qt_row['Previous_Year_Sell_Price']/qt_row['Previous_Year_List_Price']))
					elif qt_row['Previous_Year_List_Price'] == 0 and qt_row['Final_List_Price']:
						qt_row['Scope_Change'] = (qt_row['Scope_Addition_Price'] * (qt_row['Final_Sell_Price']/qt_row['Final_List_Price']))
					else:
						qt_row['Scope_Change'] = qt_row['Final_Sell_Price']
					qt_row['Price_Impact'] = qt_row['Final_Sell_Price'] - (qt_row['Scope_Change']+qt_row['Previous_Year_Sell_Price'])
					qt_row['Comment'] = ct_row['Comments']
				CBM_Renewal_Summary.Save()
		elif SC_Product_Type == "New":
			cont = item.SelectedAttributes.GetContainerByName("CBM_Models_Cont")
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					qt_row = CBM_Renewal_Summary.AddNewRow()
					qt_row['Service_Product'] = ct_row['Service Product']
					qt_row['Product_Family'] = ct_row['Product Family']
					qt_row['Previous_Year_List_Price'] = 0
					qt_row['Honeywell_List_Price_Per_Unit'] = ct_row['List Price']*ProRatedFactor if ct_row['List Price'] != "" else 0
					qt_row['Scope_Reduction_Price'] = 0
					qt_row['Scope_Addition_Price'] =  qt_row['Honeywell_List_Price_Per_Unit'] - qt_row['Previous_Year_List_Price']
					try:
						if ct_row['Service Product'] in CBM_child_dict.keys():
							qt_row['Total_Discount_'] = CBM_child_dict[ct_row['Service Product']][1]
					except:
						qt_row['Total_Discount_'] = 0
					qt_row['Escalation_Value'] = 0
					qt_row['Escalation_'] = 0
					qt_row['Final_List_Price'] = qt_row['Previous_Year_List_Price']+qt_row['Escalation_Value']+qt_row['Scope_Reduction_Price']+qt_row['Scope_Addition_Price']
					qt_row['Previous_Year_Sell_Price'] = 0
					qt_row['Total_Discount_Price'] = qt_row['Total_Discount_'] * (qt_row['Final_List_Price']/100)
					qt_row['Final_Sell_Price'] = qt_row['Final_List_Price']	 - qt_row['Total_Discount_Price']
					qt_row['Scope_Change'] = qt_row['Final_Sell_Price']
					qt_row['Price_Impact'] = qt_row['Final_Sell_Price'] - (qt_row['Scope_Change']+qt_row['Previous_Year_Sell_Price'])
					qt_row['Comment'] = "Scope Addition"
				CBM_Renewal_Summary.Save()
	if v_mod_name == "Parts Management":
		partManagement_child_dict=v_child_dict
		partsManagement_renewal_summary = Quote.QuoteTables["SC_Parts_Management_Summary"]
		partsManagement_renewal_summary.Rows.Clear()
		partsReplacement_renewal_summary = Quote.QuoteTables["SC_Parts_Replacement_Summary"]
		partsReplacement_renewal_summary.Rows.Clear()
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		if SC_Product_Type == "Renewal":
			p1p2cont = item.SelectedAttributes.GetContainerByName("SC_P1P2_Parts_List_Summary")
			replacementcont = item.SelectedAttributes.GetContainerByName("SC_P1P2_Parts_Replacement_Summary")
			SC_Pricing_Escalation_PM = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Pricing_Escalation'),'NA')
			compCont = item.SelectedAttributes.GetContainerByName("ComparisonSummary")
			scope_removed = []
			if compCont.Rows.Count:
				for cs_row in compCont.Rows:
					if cs_row.IsSelected == True:
						scope_removed.append(cs_row['Service_Product'])
						if cs_row['Service_Product'] == "Parts Replacement":
							qt_row_pr = partsReplacement_renewal_summary.AddNewRow()
							qt_row_pr['Service_Product'] = cs_row['Service_Product']
							qt_row_pr['Pricing_Method'] = "Scope Removed"
							qt_row_pr['PY_Ext_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
							qt_row_pr['PY_List_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
							qt_row_pr['PY_Total_Discount'] = float(cs_row['PY_Discount_SFDC'])*100 if cs_row['PY_Discount_SFDC'] else 0
							qt_row_pr['PY_Sell_Price'] = float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor if cs_row['PY_Sell_Price_SFDC'] else 0
							qt_row_pr['Scope_Change'] = str(round(-float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor,2)) if cs_row['PY_Sell_Price_SFDC'] else 0
							qt_row_pr['Comment'] = "Scope Reduction"
							for col in ['Fee_Percentage','Total_Discount','CY_Ext_Price','_CY_List_Price','CY_Sell_Price','Price_Impact']:
								qt_row_pr[col] = 0
							partsReplacement_renewal_summary.Save()
						else:
							qt_row_pm = partsManagement_renewal_summary.AddNewRow()
							qt_row_pm['Service_Product'] = cs_row['Service_Product']
							qt_row_pm['PY_Quantity'] = 1
							qt_row_pm['PY_Ext_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
							qt_row_pm['PY_Ext_holding_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
							qt_row_pm['Last_Year_Discount'] = float(cs_row['PY_Discount_SFDC'])*100 if cs_row['PY_Discount_SFDC'] else 0
							qt_row_pm['Scope_Reduction_Quantity'] = -1
							qt_row_pm['Scope_Reduction_Price'] = (-1)*float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
							qt_row_pm['Previous_Year_Sell_Price'] =	 float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor if cs_row['PY_Sell_Price_SFDC'] else 0
							qt_row_pm['PY_Total_Cost_Price'] = str(round((1-float(cs_row['Booked_Margin'])/100) *float(cs_row["PY_Sell_Price_SFDC"])*ProRatedFactor,2)) if cs_row["PY_Sell_Price_SFDC"] else "0"
							qt_row_pm['Scope_Change'] = str(round(-float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor,2)) if cs_row['PY_Sell_Price_SFDC'] else 0
							qt_row_pm['Comments'] = "Scope Reduction"
							for col in ['Holding_Percentage','CY_Quantity','CY_Ext_Price','CY_Ext_holding_Price','PY_Contigency_Cost','CY_Contigency_Cost','Escalation','Total_Discount','Scope_Addition_Quantity','Escalation_Value','Scope_Addition_Price','Final_List_Price','Total_Discount_Price','Final_Sell_Price','Final_Total_Cost_Price','Price_Impact','Margin']:
								qt_row_pm[col] = 0
							partsManagement_renewal_summary.Save()
			try:
				if replacementcont.Rows.Count:
					for ct_row_pr in replacementcont.Rows:
						if ct_row_pr['Service_Product'] not in scope_removed:
							qt_row_pr = partsReplacement_renewal_summary.AddNewRow()
							qt_row_pr['Service_Product'] = ct_row_pr['Service_Product']
							qt_row_pr['Pricing_Method'] = ct_row_pr['Pricing_Method']
							qt_row_pr['Fee_Percentage'] = ct_row_pr['Fee_Percentage']
							qt_row_pr['PY_Ext_Price'] = float(ct_row_pr['PY_ExtPrice'])*ProRatedFactor if ct_row_pr['PY_ExtPrice'] else 0
							qt_row_pr['PY_List_Price'] = float(ct_row_pr['PY_ListPrice'])*ProRatedFactor if ct_row_pr['PY_ListPrice'] else 0
							try:
								qt_row_pr['Total_Discount'] = partManagement_child_dict[ct_row_pr['Service_Product']][1]
							except:
								qt_row_pr['Total_Discount'] = 0
							qt_row_pr['PY_Total_Discount'] = ct_row_pr['PY_Discount'] if ct_row_pr['PY_Discount'] else 0
							qt_row_pr['PY_Sell_Price'] = qt_row_pr['PY_List_Price'] * (1 - (qt_row_pr['PY_Total_Discount']/100))
							qt_row_pr['CY_Ext_Price'] = float(ct_row_pr['CY_ExtPrice'])*ProRatedFactor if ct_row_pr['CY_ExtPrice'] else 0
							qt_row_pr['_CY_List_Price'] = float(ct_row_pr['CY_ListPrice'])*ProRatedFactor if ct_row_pr['CY_ListPrice'] else 0
							qt_row_pr['CY_Sell_Price'] = qt_row_pr['_CY_List_Price'] * (1 - (qt_row_pr['Total_Discount']/100))
							qt_row_pr['Scope_Change'] = float(ct_row_pr['Scope_Change'])*ProRatedFactor if ct_row_pr['Scope_Change'] else 0
							qt_row_pr['Price_Impact'] = qt_row_pr['CY_Sell_Price'] - (qt_row_pr['Scope_Change'] + qt_row_pr['PY_Sell_Price'])
							qt_row_pr['Comment'] = ct_row_pr['Comments']
					partsReplacement_renewal_summary.Save()
			except:
				pass
			try:
				if p1p2cont.Rows.Count:
					for ct_row_pm in p1p2cont.Rows:
						if ct_row_pm['Service_Product'] not in scope_removed:
							qt_row_pm = partsManagement_renewal_summary.AddNewRow()
							qt_row_pm['Service_Product'] = ct_row_pm['Service_Product']
							qt_row_pm['Holding_Percentage'] = ct_row_pm['Holding_Percentage']
							qt_row_pm['PY_Quantity'] = ct_row_pm['PY_Quantity'] if ct_row_pm['PY_Quantity'] else 0
							qt_row_pm['PY_Ext_Price'] = float(ct_row_pm['PY_ExtPrice'])*ProRatedFactor if ct_row_pm['PY_ExtPrice'] else 0
							qt_row_pm['PY_Ext_holding_Price'] = float(ct_row_pm['PY_ExtHoldingPrice'])*ProRatedFactor if ct_row_pm['PY_ExtHoldingPrice'] else 0
							qt_row_pm['CY_Quantity'] = ct_row_pm['CY_Quantity'] if ct_row_pm['CY_Quantity'] else 0
							qt_row_pm['CY_Ext_Price'] = float(ct_row_pm['CY_ExtPrice'])*ProRatedFactor if ct_row_pm['CY_ExtPrice'] else 0
							qt_row_pm['CY_Ext_holding_Price'] = float(ct_row_pm['CY_ExtHoldingPrice'])*ProRatedFactor if ct_row_pm['CY_ExtHoldingPrice'] else 0
							qt_row_pm['PY_Contigency_Cost'] = float(ct_row_pm['PY_ContigencyCost'])*ProRatedFactor if ct_row_pm['PY_ContigencyCost'] else 0
							qt_row_pm['CY_Contigency_Cost'] = float(ct_row_pm['CY_ContigencyCost'])*ProRatedFactor if ct_row_pm['CY_ContigencyCost'] else 0
							try:
								qt_row_pm['Escalation'] = partManagement_child_dict[ct_row_pm['Service_Product']][0]
								qt_row_pm['Total_Discount'] = partManagement_child_dict[ct_row_pm['Service_Product']][1]
							except:
								qt_row_pm['Escalation'] = 0
								qt_row_pm['Total_Discount'] = 0
							qt_row_pm['Last_Year_Discount'] = ct_row_pm['PY_Discount'] if ct_row_pm['PY_Discount'] else 0
							qt_row_pm['Scope_Reduction_Quantity'] = qt_row_pm['CY_Quantity'] - qt_row_pm['PY_Quantity'] if qt_row_pm['CY_Quantity'] < qt_row_pm['PY_Quantity'] else 0
							qt_row_pm['Scope_Addition_Quantity'] = qt_row_pm['CY_Quantity'] - qt_row_pm['PY_Quantity'] if qt_row_pm['CY_Quantity'] > qt_row_pm['PY_Quantity'] else 0

							if qt_row_pm['PY_Quantity'] > 0:
								qt_row_pm['Escalation_Value'] = (qt_row_pm['Escalation']/100) * qt_row_pm['PY_Ext_holding_Price'] if qt_row_pm['CY_Quantity'] > qt_row_pm['PY_Quantity'] else (qt_row_pm['Escalation']/100) * (qt_row_pm['PY_Ext_holding_Price']*qt_row_pm['CY_Quantity']/qt_row_pm['PY_Quantity'])

							qt_row_pm['Scope_Reduction_Price'] = qt_row_pm['Scope_Reduction_Quantity'] * (qt_row_pm['PY_Ext_holding_Price']/qt_row_pm['PY_Quantity']) if qt_row_pm['PY_Quantity'] != 0 else 0
							qt_row_pm['Scope_Addition_Price'] = qt_row_pm['Scope_Addition_Quantity'] * (qt_row_pm['CY_Ext_holding_Price']/qt_row_pm['CY_Quantity']) if qt_row_pm['CY_Quantity'] != 0 else 0
							qt_row_pm['Escalation_Value'] = qt_row_pm['Escalation_Value'] if SC_Pricing_Escalation_PM == "Yes" else 0
							qt_row_pm['Final_List_Price'] = qt_row_pm['PY_Ext_holding_Price'] + qt_row_pm['Scope_Reduction_Price'] + qt_row_pm['Escalation_Value'] + qt_row_pm['Scope_Addition_Price'] if SC_Pricing_Escalation_PM == "Yes" else qt_row_pm['CY_Ext_holding_Price']
							qt_row_pm['Total_Discount_Price'] =	 qt_row_pm['Final_List_Price'] * (qt_row_pm['Total_Discount']/100)
							qt_row_pm['Previous_Year_Sell_Price'] =	 float(ct_row_pm['PY_SellPrice'])*ProRatedFactor if ct_row_pm['PY_SellPrice'] else 0
							qt_row_pm['Final_Sell_Price'] = qt_row_pm['Final_List_Price'] - qt_row_pm['Total_Discount_Price']
							qt_row_pm['PY_Total_Cost_Price'] = float(ct_row_pm['PY_TotalCost'])*ProRatedFactor if ct_row_pm['PY_TotalCost'] else 0
							qt_row_pm['Final_Total_Cost_Price'] = float(ct_row_pm['CY_TotalCost'])*ProRatedFactor*(1+(qt_row_pm['Escalation']/100)) if ct_row_pm['CY_TotalCost'] else 0
							Reduction_val=qt_row_pm['Scope_Reduction_Price'] * (qt_row_pm['Previous_Year_Sell_Price'] / qt_row_pm['PY_Ext_holding_Price']) if qt_row_pm['PY_Ext_holding_Price'] not in (0,'0','',0.00,'0.00','0.0',0.0) else 0
							Addition_val = qt_row_pm['Scope_Addition_Price'] * (qt_row_pm['Final_Sell_Price']/qt_row_pm['Final_List_Price']) if qt_row_pm['Final_List_Price'] not in (0,'0','',0.00,'0.00','0.0',0.0) else 0
							qt_row_pm['Scope_Change'] = Reduction_val + Addition_val
							qt_row_pm['Price_Impact'] = qt_row_pm['Final_Sell_Price'] - (qt_row_pm['Scope_Change'] + qt_row_pm['Previous_Year_Sell_Price'])
							qt_row_pm['Margin'] = (1 - qt_row_pm['Final_Total_Cost_Price']/qt_row_pm['Final_Sell_Price'])*100 if qt_row_pm['Final_Sell_Price'] not in (0,'0','',0.00,'0.00','0.0',0.0) else 1
							qt_row_pm['Comments'] = ct_row_pm['Comments']
					partsManagement_renewal_summary.Save()
			except:
				pass
		elif SC_Product_Type == "New":
			p1p2cont = item.SelectedAttributes.GetContainerByName("SC_P1P2_Parts_List_Summary")
			replacementcont = item.SelectedAttributes.GetContainerByName("SC_P1P2_Parts_Replacement_Summary")
			try:
				if replacementcont.Rows.Count:
					for ct_row_pr in replacementcont.Rows:
						qt_row_pr = partsReplacement_renewal_summary.AddNewRow()
						for col in ['PY_Ext_Price','PY_List_Price','PY_Total_Discount','PY_Sell_Price','Price_Impact']:
							qt_row_pr[col] = 0
						qt_row_pr['Service_Product'] = ct_row_pr['Service_Product']
						qt_row_pr['Pricing_Method'] = ct_row_pr['Pricing_Method']
						qt_row_pr['Fee_Percentage'] = ct_row_pr['Fee_Percentage']
						qt_row_pr['CY_Ext_Price'] = float(ct_row_pr['Parts_Ext_Price'])*ProRatedFactor if ct_row_pr['Parts_Ext_Price'] else 0
						qt_row_pr['_CY_List_Price'] = float(ct_row_pr['List_Price'])*ProRatedFactor if ct_row_pr['List_Price'] else 0
						try:
							qt_row_pr['Total_Discount'] = partManagement_child_dict[ct_row_pr['Service_Product']][1]
						except:
							qt_row_pr['Total_Discount'] = 0
						qt_row_pr['CY_Sell_Price'] = qt_row_pr['_CY_List_Price'] * (1 - (qt_row_pr['Total_Discount']/100))
						qt_row_pr['Scope_Change'] = qt_row_pr['CY_Sell_Price']
						qt_row_pr['Comment'] = "Scope Addition"
					partsReplacement_renewal_summary.Save()
			except:
				pass
			try:
				if p1p2cont.Rows.Count:
					for ct_row_pm in p1p2cont.Rows:
						qt_row_pm = partsManagement_renewal_summary.AddNewRow()
						for col in ['PY_Quantity','PY_Ext_Price','PY_Ext_holding_Price','PY_Contigency_Cost','CY_Contigency_Cost','Scope_Reduction_Quantity','Scope_Reduction_Price','Escalation','Escalation_Value','Last_Year_Discount','Previous_Year_Sell_Price','PY_Total_Cost_Price','Price_Impact']:
							qt_row_pm[col] = 0
						qt_row_pm['Service_Product'] = ct_row_pm['Service_Product']
						qt_row_pm['Holding_Percentage'] = float(ct_row_pm['Holding_Percentage'])
						qt_row_pm['CY_Quantity'] = ct_row_pm['Qty'] if ct_row_pm['Qty'] else 0
						qt_row_pm['CY_Ext_Price'] = float(ct_row_pm['Ext_Price'])*ProRatedFactor if ct_row_pm['Ext_Price'] else 0
						qt_row_pm['CY_Ext_holding_Price'] = float(ct_row_pm['Ext_Holding_Price'])*ProRatedFactor if ct_row_pm['Ext_Holding_Price'] else 0
						try:
							qt_row_pm['Total_Discount'] = partManagement_child_dict[ct_row_pm['Service_Product']][1]
						except:
							qt_row_pm['Total_Discount'] = 0
						qt_row_pm['Scope_Addition_Quantity'] = ct_row_pm['Qty'] if ct_row_pm['Qty'] else 0
						qt_row_pm['Scope_Addition_Price'] = float(ct_row_pm['Ext_Holding_Price'])*ProRatedFactor if ct_row_pm['Ext_Holding_Price'] else 0
						qt_row_pm['Final_List_Price'] = qt_row_pm['PY_Ext_holding_Price'] + qt_row_pm['Scope_Reduction_Price'] + qt_row_pm['Escalation_Value'] + qt_row_pm['Scope_Addition_Price']
						qt_row_pm['Total_Discount_Price'] = qt_row_pm['Final_List_Price'] * (qt_row_pm['Total_Discount']/100)
						qt_row_pm['Final_Sell_Price'] = qt_row_pm['Final_List_Price'] - qt_row_pm['Total_Discount_Price']
						qt_row_pm['Final_Total_Cost_Price'] = float(ct_row_pm['CY_TotalCost'])*ProRatedFactor*(1+(qt_row_pm['Escalation']/100)) if ct_row_pm['CY_TotalCost'] else 0
						qt_row_pm['Scope_Change'] = qt_row_pm['Final_Sell_Price']
						qt_row_pm['Margin'] = (1 - qt_row_pm['Final_Total_Cost_Price']/qt_row_pm['Final_Sell_Price'])*100
						qt_row_pm['Comments'] = "Scope Addition"
					partsManagement_renewal_summary.Save()
			except:
				pass
	if v_mod_name == "Hardware Warranty":
		hw_child_dict=v_child_dict
		hw_renewal_summary = Quote.QuoteTables["Hardware_Warranty_Renewal_Summary"]
		hw_renewal_summary.Rows.Clear()
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		SC_Pricing_Escalation = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Pricing_Escalation'), '')
		if SC_Product_Type == "Renewal":
			cont = item.SelectedAttributes.GetContainerByName("SC_ModelsHiddenSS_HR_RWL")
			compCont = item.SelectedAttributes.GetContainerByName("ComparisonSummary")
			if compCont.Rows.Count:
				for cs_row in compCont.Rows:
					if (cs_row.IsSelected == True and not cont) or (cs_row.IsSelected == True and cs_row['Service_Product'] not in ['Hardware Warranty']):
						qt_row = hw_renewal_summary.AddNewRow()
						qt_row["Asset"]=''
						qt_row["Model"] = cs_row['Service_Product'] 
						qt_row["Description"] = "Scope Removed"
						qt_row["PreviousYearQuantity"]= 1
						qt_row['PreviousYearUnitPrice'] = float(cs_row['PY_List_Price_SFDC'])* ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['PreviousYearListPrice'] = float(cs_row['PY_List_Price_SFDC'])* ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['ScopeReductionQuantity'] = -1
						qt_row['ScopeReductionPrice'] = ((-1)*float(cs_row['PY_List_Price_SFDC']))* ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['LastYearDiscountPer'] = (float(cs_row['PY_Discount_SFDC'])*100) if cs_row['PY_Discount_SFDC'] else 0
						qt_row['PreviousYearSellPrice'] = float(cs_row['PY_Sell_Price_SFDC'])* ProRatedFactor if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['ScopeChange'] = str((round(-float(cs_row['PY_Sell_Price_SFDC']),2))* ProRatedFactor) if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Previous_Year_Cost_Price'] = str(round((1-float(cs_row['Booked_Margin'])/100) *float(cs_row["PY_Sell_Price_SFDC"]),2)* ProRatedFactor) if cs_row["PY_Sell_Price_SFDC"] else "0"
						qt_row['Previous_Year_Unit_Cost_Price']=str(round(float(qt_row['Previous_Year_Cost_Price']),2)* ProRatedFactor)
						qt_row['Comments'] = "Scope Reduction"
						for col in ['RenewalQuantity','HoneywellListPricePerUnit','Current_Year_List_Price','ScopeAdditionQuantity','ScopeAdditionPrice','EscalationPercentage','TotalDiscountPer','EscalationValue','FinalListPrice','TotalDiscountPrice','FinalSellPrice','PriceImpact','Current_Year_Unit_Cost_Price','MarginPercentage','Current_Year_Cost_Price']:
							qt_row[col] = 0
			if cont:
				if cont.Rows.Count:
					for ct_row in cont.Rows:
						qt_row = hw_renewal_summary.AddNewRow()
						qt_row["Asset"] = ct_row["Asset"]
						qt_row["Model"] = ct_row["Model"]
						qt_row["Description"] = ct_row["Description"]
						qt_row["PreviousYearQuantity"] = ct_row["PreviousYearQuantity"]
						qt_row["RenewalQuantity"] = ct_row["RenewalQuantity"]
						qt_row["PreviousYearUnitPrice"] = float(ct_row["PreviousYearUnitPrice"])* ProRatedFactor
						qt_row["PreviousYearListPrice"] = float(ct_row["PreviousYearListPrice"])* ProRatedFactor
						qt_row["HoneywellListPricePerUnit"] = float(ct_row["HoneywellListPricePerUnit"])* ProRatedFactor
						qt_row["ScopeReductionQuantity"] = ct_row["ScopeReductionQuantity"]
						qt_row["ScopeReductionPrice"] = float(ct_row["ScopeReductionPrice"])* ProRatedFactor
						try:
							EscalationPercentage = hw_child_dict['Hardware Warranty'][0] if hw_child_dict['Hardware Warranty'][0] else 0.00
						except:
							EscalationPercentage = 0.00
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
						LastYearDiscountPer = str(ct_row['LastYearDiscountPer'])
						qt_row["LastYearDiscountPer"] = str(LastYearDiscountPer)
						try:
							TotalDiscountPer = hw_child_dict['Hardware Warranty'][1] if hw_child_dict['Hardware Warranty'][1] else 0.00
						except:
							TotalDiscountPer = 0.00
						qt_row["TotalDiscountPer"] = str(round(float(TotalDiscountPer),2))
						TotalDiscountPrice = round(float(qt_row["FinalListPrice"]) * (float(TotalDiscountPer)/100),2)
						qt_row["TotalDiscountPrice"] = str(TotalDiscountPrice)
						PreviousYearSellPrice = float(ct_row["PreviousYearSellPrice"])* ProRatedFactor
						qt_row["PreviousYearSellPrice"] = (PreviousYearSellPrice-(PreviousYearSellPrice	 % 0.01)) if LastYearDiscountPer!="0.0" else qt_row["PreviousYearListPrice"]
						FinalSellPrice = round(float(qt_row["FinalListPrice"]) * (1-(float(TotalDiscountPer)/100)),2)
														  
						qt_row["FinalSellPrice"] = str(FinalSellPrice)
						ScopeChange = 0
						if float(qt_row["FinalListPrice"]) != 0 and float(ct_row["PreviousYearListPrice"]) != 0:
							ScopeChange = round((ScopeReductionPrice * (PreviousYearSellPrice/(float(ct_row["PreviousYearListPrice"])* ProRatedFactor))) + (ScopeAdditionPrice*(FinalSellPrice/float(qt_row["FinalListPrice"]))),2)
						if qt_row['RenewalQuantity'] == '0':
							ScopeChange =round((-1) * float(qt_row['PreviousYearSellPrice']),2)
																					
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
							Trace.Write("MarginPercentage {} MarginPercentage1 {} per {} div  {}".format(float(ct_row['SC_CurrentYearCostPrice_HR_RWL']),FinalSellPrice,qt_row['MarginPercentage'],str(round(float(qt_row['Current_Year_Cost_Price']) / FinalSellPrice,2))))
						else:
							qt_row['MarginPercentage'] ="0.0"
				hw_renewal_summary.Save()
		elif SC_Product_Type == "New":
			cont = item.SelectedAttributes.GetContainerByName("HWOS_Model Scope_3party_ScopeSummary")
			#hw_renewal_summary.GetColumnByName('Asset').AccessLevel = hw_renewal_summary.AccessLevel.Hidden
			for i in cont.Rows:
				qt_row = hw_renewal_summary.AddNewRow()
				qt_row["Asset"] = i['Asset']
				qt_row["Model"] = i['3rd Party Model']
				qt_row["Description"] = i['Description']
				qt_row["RenewalQuantity"] = i['Quantity']
				qt_row["Description"] = i['Description']
				qt_row["HoneywellListPricePerUnit"] = str((float(i['List Price']) / float(qt_row["RenewalQuantity"]))* ProRatedFactor)
				qt_row["Current_Year_Unit_Cost_Price"] = str((float(i['Ext Cost']) / float(qt_row["RenewalQuantity"]))* ProRatedFactor)
				qt_row["Current_Year_List_Price"] = float(i['List Price'])* ProRatedFactor
				qt_row["Current_Year_Cost_Price"] = float(i['Ext Cost'])* ProRatedFactor
				qt_row["PreviousYearQuantity"] = 0
				qt_row["PreviousYearUnitPrice"] = 0
				qt_row["PreviousYearListPrice"] = 0
				qt_row['Previous_Year_Unit_Cost_Price'] = 0
				qt_row['Previous_Year_Cost_Price'] = 0
				qt_row["ScopeReductionQuantity"] = 0
				qt_row["ScopeReductionPrice"] = 0
				qt_row["LastYearDiscountPer"] = 0
				qt_row["PreviousYearSellPrice"] = 0
				qt_row["EscalationPercentage"] = 0
				qt_row["PriceImpact"] = 0
				qt_row["Comments"] = "Scope Addition"
				EscalationValue = 0
				qt_row["EscalationValue"] = str(EscalationValue)
				try:
					TotalDiscountPer = hw_child_dict['Hardware Warranty'][1] if hw_child_dict['Hardware Warranty'][1] else 0.00
				except:
					TotalDiscountPer = 0.00
				qt_row["TotalDiscountPer"] = str(round(float(TotalDiscountPer),2))
				if qt_row["RenewalQuantity"] > qt_row["PreviousYearQuantity"]:
					qt_row["ScopeAdditionQuantity"] = qt_row["RenewalQuantity"]
				else:
					qt_row["ScopeAdditionQuantity"] = qt_row["RenewalQuantity"]
				qt_row["ScopeAdditionPrice"] = float(i['Quantity']) * float(qt_row["HoneywellListPricePerUnit"])
				qt_row["FinalListPrice"] = qt_row["ScopeAdditionPrice"]
				TotalDiscountPrice = str(float(qt_row["FinalListPrice"]) * (float(TotalDiscountPer)/100))
				qt_row["TotalDiscountPrice"] = str(TotalDiscountPrice)
				qt_row["FinalSellPrice"] = float(qt_row["FinalListPrice"]) - float(qt_row["TotalDiscountPrice"])
				qt_row["ScopeChange"] = qt_row["FinalSellPrice"]
				if qt_row["FinalSellPrice"] != 0:
					qt_row['MarginPercentage'] = str(round((1 - (qt_row['Current_Year_Cost_Price']/qt_row['FinalSellPrice'])) * 100,2))
			hw_renewal_summary.Save()
		elif SC_Product_Type == 'New':
			cont = item.SelectedAttributes.GetContainerByName("HWOS_Model Scope_3party")
			for i in cont.Rows:
				qt_row = hw_renewal_summary.AddNewRow()
				qt_row["HoneywellListPricePerUnit"] = i['Unit List Price']
				qt_row["RenewalQuantity"] = i['Quantity']
				qt_row["Description"] = i['Description']
				qt_row["Model"] = i['3rd Party Model']
				qt_row['Current_Year_List_Price'] =	 float(i['List Price'])* ProRatedFactor

				try:
					EscalationPercentage = hw_child_dict['Hardware Warranty'][0] if hw_child_dict['Hardware Warranty'][0] else 0.00
				except:
					EscalationPercentage = 0.00
				qt_row["EscalationPercentage"] = str(round(float(EscalationPercentage),2))
				
				EscalationValue = float(float(EscalationPercentage)/100) * int(float(qt_row["RenewalQuantity"])) * float(qt_row["HoneywellListPricePerUnit"])
				qt_row["EscalationValue"] = str(EscalationValue)

				FinalListPrice = (float(i['List Price'])* ProRatedFactor) + EscalationValue
				qt_row["FinalListPrice"] = str(FinalListPrice)

				TotalDiscountPer = hw_child_dict['Hardware Warranty'][1] if hw_child_dict['Hardware Warranty'][1] else 0.00
				qt_row["TotalDiscountPer"] = str(round(float(TotalDiscountPer),2))

				TotalDiscountPrice = FinalListPrice * (float(TotalDiscountPer)/100)
				qt_row["TotalDiscountPrice"] = str(TotalDiscountPrice)

				FinalSellPrice = FinalListPrice * (1-(float(TotalDiscountPer)/100))
				qt_row["FinalSellPrice"] = str(FinalSellPrice)

				if FinalSellPrice != 0:
					qt_row['MarginPercentage'] = str((round(float(i['Unit List Price'])* ProRatedFactor) / FinalSellPrice,2))