#Labor, TRACE and MES
def fn_load_QuoteTable_Grp1(Quote,v_mod_name,item,v_child_dict,ProRatedFactor):
	if v_mod_name=="Labor":
		labor_child_dict=v_child_dict
		labor_renewal_summary = Quote.QuoteTables["SC_Labor_Module_Renewal_Summary"]
		labor_renewal_summary.Rows.Clear()
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		if SC_Product_Type == "Renewal":
			cont = item.SelectedAttributes.GetContainerByName("SC_Labor_Summary_Container")
			compCont = item.SelectedAttributes.GetContainerByName('ComparisonSummary')
			scope_removed = []
			compareDict = {}
			if compCont.Rows.Count:
				for cs_row in compCont.Rows:
					compareDict[cs_row['Service_Product']] = float(cs_row['PY_Discount_SFDC'])*100 if cs_row['PY_Discount_SFDC'] else 0
					if cs_row.IsSelected == True:
						scope_removed.append(cs_row['Service_Product'])
						qt_row = labor_renewal_summary.AddNewRow()
						for col in ['Resource_Type','Service_Product','Entitlement','Related_Module','PY_Entitlement','PY_Related_Module','PY_Resource_Type']:
							qt_row[col] = 'None'
						for col in ['RY_Deliverables_Hours','HWl_List_Price_Per_Unit','HW_List_Price','C_List_Price','PY_Total_Expenses','RY_Total_Expenses','SA_Quantity','SA_Price','Escalation','Total_Discount','Customer_List_Price','Escalation_Value','Final_List_Price','Total_Discount_Price','Final_Sell_Price','PY_Contigency_Cost','Contigency_Cost','Final_Total_Cost_Price','Price_Impact','Margin']:
							qt_row[col] = 0
						qt_row['PY_Service_Product'] = cs_row['Service_Product']
						qt_row['PY_Deliverables_Hours'] = 1
						qt_row['PY_Unit_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['PY_List_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['SR_Quantity'] = -1
						qt_row['SR_Price'] = (-1)*float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Last_Year_Discount'] = float(cs_row['PY_Discount_SFDC'])*100 if cs_row['PY_Discount_SFDC'] else 0
						qt_row['PY_Sell_Price'] = float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Scope_Change'] = str(round(-float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor,2)) if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['PY_Total_Cost_Price']  = str(round((1-float(cs_row['Booked_Margin'])/100)*float(cs_row["PY_Sell_Price_SFDC"])*ProRatedFactor,2)) if cs_row["PY_Sell_Price_SFDC"] else "0"
						qt_row['Comments'] = "Scope Reduction"
				labor_renewal_summary.Save()
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					if ct_row['Service_Product'] not in scope_removed:
						SC_Pricing_Escalation_LB = ct_row['SC_Labor_Pricing_Escalation_Based']
						qt_row = labor_renewal_summary.AddNewRow()
						qt_row['Resource_Type'] = ct_row['Resource_Type']
						qt_row['Service_Product'] = ct_row['Service_Product']
						qt_row['Entitlement'] = ct_row['Entitlement']
						qt_row['Related_Module'] = ct_row['Related Module']
						qt_row['PY_Service_Product'] = ct_row['PY_Service_Product']
						qt_row['PY_Entitlement'] = ct_row['PY_Entitlement']
						qt_row['PY_Related_Module'] = ct_row['PY_Related_Module']
						qt_row['PY_Resource_Type'] = ct_row['PY_Resource_Type']
						qt_row['PY_Deliverables_Hours'] = int(eval(ct_row['PY_Deliverables_Hours'])) if ct_row['PY_Deliverables_Hours'] else 0
						qt_row['RY_Deliverables_Hours'] = ct_row['Renewal_Year_Deliverables_Hours'] if ct_row['Renewal_Year_Deliverables_Hours'] else 0
						qt_row['C_List_Price'] = float(ct_row['Total_Customer_List_Price'])*ProRatedFactor if ct_row['Total_Customer_List_Price'] else 0
						qt_row['HW_List_Price'] = float(ct_row['Total_Honeywell_List_Price'])*ProRatedFactor if ct_row['Total_Honeywell_List_Price'] else 0
						qt_row['PY_Unit_Price'] = round(float(ct_row['PY_UnitPrice'])*ProRatedFactor,2) if ct_row['PY_UnitPrice']	else 0
						qt_row['PY_List_Price'] = float(ct_row['PY_ListPrice'])*ProRatedFactor if ct_row['PY_ListPrice']	else 0
						qt_row['HWl_List_Price_Per_Unit'] = float(ct_row['Honeywell_List_Price'])*ProRatedFactor / float(ct_row['SC_Labor_Hrs_per_Full_Day']) if ct_row['Honeywell_List_Price']!= '' and ct_row['SC_Labor_Hrs_per_Full_Day'] != '' else 0
						for column in ['PY_Total_Expenses','RY_Total_Expenses']:
							qt_row[column] = 0
						qt_row['SR_Quantity'] = float(qt_row['RY_Deliverables_Hours']) - float(qt_row['PY_Deliverables_Hours']) if float(qt_row['PY_Deliverables_Hours']) > float(qt_row['RY_Deliverables_Hours']) else 0
						qt_row['SA_Quantity'] = float(qt_row['RY_Deliverables_Hours']) - float(qt_row['PY_Deliverables_Hours']) if float(qt_row['PY_Deliverables_Hours']) < float(qt_row['RY_Deliverables_Hours']) else 0
						qt_row['SR_Price'] = float(qt_row['SR_Quantity']) * (float(qt_row['PY_List_Price'])/float(qt_row['PY_Deliverables_Hours'])) if qt_row['PY_Deliverables_Hours'] > 0 else 0
						qt_row['SA_Price'] = float(qt_row['SA_Quantity']) * float(qt_row['HWl_List_Price_Per_Unit'])
						if ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + ct_row['Resource_Type'] in labor_child_dict.keys():
							qt_row['Escalation'] = labor_child_dict[ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + ct_row['Resource_Type']][0]
							qt_row['Total_Discount'] =labor_child_dict[ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + ct_row['Resource_Type']][1]
						else:
							qt_row['Escalation'] = 0
							qt_row['Total_Discount'] = 0
						if SC_Pricing_Escalation_LB == "Yes":
							qt_row['Customer_List_Price'] = float(ct_row['Customer_List_Price'])*ProRatedFactor if ct_row['Customer_List_Price'] else 0
							if qt_row['RY_Deliverables_Hours'] > qt_row['PY_Deliverables_Hours']:
								qt_row['Escalation_Value'] = (qt_row['Escalation']/100) * qt_row['PY_Unit_Price'] * qt_row['PY_Deliverables_Hours']
							elif qt_row['RY_Deliverables_Hours'] <= qt_row['PY_Deliverables_Hours']:
								qt_row['Escalation_Value'] = (qt_row['Escalation']/100) * qt_row['PY_Unit_Price'] * qt_row['RY_Deliverables_Hours']
							ListPrice = qt_row['PY_List_Price'] + ((((float(ct_row["Escalation_Price"] or 0) if ct_row["Escalation_Price"] else 0)) * ProRatedFactor * float(qt_row['Escalation'])/100))
							qt_row['Final_List_Price'] = ListPrice + qt_row['SR_Price'] + qt_row['SA_Price']
						else:
							qt_row['Customer_List_Price'] = float(ct_row['Honeywell_List_Price'])*ProRatedFactor if ct_row['Honeywell_List_Price'] else 0
							qt_row['Escalation_Value'] = 0
							qt_row['Final_List_Price'] = float(qt_row['HWl_List_Price_Per_Unit']) * float(qt_row['RY_Deliverables_Hours'])
						qt_row['Total_Discount_Price'] = qt_row['Final_List_Price'] * (qt_row['Total_Discount']/100)
						qt_row['Last_Year_Discount'] = compareDict.get(ct_row['Service_Product'],'0')
						#qt_row['PY_Sell_Price'] = (1 - float(qt_row['Last_Year_Discount'])/100) * float(qt_row['PY_List_Price']) if float(qt_row['Last_Year_Discount'])>0 else float(qt_row['PY_List_Price']) #CXCPQ-91384
						qt_row['PY_Sell_Price'] = ct_row['PY_SellPrice']
						qt_row['Final_Sell_Price'] = float(qt_row['Final_List_Price']) - float(qt_row['Total_Discount_Price'])
						qt_row['PY_Contigency_Cost'] = float(ct_row['PY_Contigency_Cost'])*ProRatedFactor if ct_row['PY_Contigency_Cost'] else 0
						qt_row['PY_Total_Cost_Price'] = float(ct_row['PY_Total_Cost_Price'])*ProRatedFactor if ct_row['PY_Total_Cost_Price'] else 0
						qt_row['Contigency_Cost'] = float(ct_row['Contigency_Cost'])*ProRatedFactor if ct_row['Contigency_Cost'] else '0'
						qt_row['Final_Total_Cost_Price'] = float(ct_row['Final_Total_Cost_Price'])*ProRatedFactor*(1+(qt_row['Escalation']/100)) if ct_row['Final_Total_Cost_Price'] else '0'
						Reduction_val = qt_row['SR_Price'] * (qt_row['PY_Sell_Price'] / qt_row['PY_List_Price']) if qt_row['PY_List_Price'] not in (0,'0','',0.00,'0.00','0.0',0.0) else 0
						Addition_val = qt_row['SA_Price'] * (qt_row['Final_Sell_Price'] / qt_row['Final_List_Price']) if qt_row['Final_List_Price'] not in (0,'0','',0.00,'0.00','0.0',0.0) else 0
						qt_row['Scope_Change'] = Reduction_val + Addition_val
						qt_row['Price_Impact'] = float(qt_row['Final_Sell_Price']) - (float(qt_row['Scope_Change']) + float(qt_row['PY_Sell_Price']))
						qt_row['Margin'] = (1 - (float(qt_row['Final_Total_Cost_Price']) / float(qt_row['Final_Sell_Price']))) * 100 if qt_row['Final_Sell_Price'] not in (0,'0','',0.00,'0.00','0.0',0.0) else 0
						qt_row['Comments'] = ct_row['Comments']

						if ct_row['Other_Expenses'] not in ('0','0.00','',0.0,'0.0'):
							qt_row2 = labor_renewal_summary.AddNewRow()
							for column2 in ['PY_Deliverables_Hours','RY_Deliverables_Hours','PY_Unit_Price','PY_List_Price','HWl_List_Price_Per_Unit','Customer_List_Price','SR_Quantity','SA_Quantity','SR_Price','SA_Price','PY_Contigency_Cost','Contigency_Cost','Final_Total_Cost_Price','Scope_Change','HW_List_Price','C_List_Price']:
								qt_row2[column2] = 0
							qt_row2['Resource_Type'] = 'Total Expense'
							qt_row2['Service_Product'] = ct_row['Service_Product']
							qt_row2['Entitlement'] = ct_row['Entitlement']
							qt_row2['Related_Module'] = ct_row['Related Module']
							qt_row2['PY_Service_Product'] = ct_row['PY_Service_Product']
							qt_row2['PY_Entitlement'] = ct_row['PY_Entitlement']
							qt_row2['PY_Related_Module'] = ct_row['PY_Related_Module']
							qt_row2['PY_Resource_Type'] = ct_row['PY_Resource_Type']
							qt_row2['PY_Total_Cost_Price'] = ct_row['PY_Expenses_Cost'] if ct_row['PY_Expenses_Cost'] != '' else 0.0
							qt_row2['PY_Total_Expenses'] = float(ct_row['PY_Total_Expenses'])*ProRatedFactor if ct_row['PY_Total_Expenses'] else 0
							qt_row2['RY_Total_Expenses'] = float(ct_row['Renewal_Year_Total_Expenses'])*ProRatedFactor if ct_row['Renewal_Year_Total_Expenses'] else 0
							if qt_row2['PY_Total_Expenses'] > qt_row2['RY_Total_Expenses']:
								qt_row2['Comments'] = 'Scope Reduction'
							elif qt_row2['PY_Total_Expenses'] < qt_row2['RY_Total_Expenses']:
								qt_row2['Comments'] = 'Scope Addition'
							else:
								qt_row2['Comments'] = 'No Scope Change'

							if ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + 'Other Expense' in labor_child_dict.keys():
								qt_row2['Escalation'] = labor_child_dict[ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + 'Other Expense'][0]
								qt_row2['Total_Discount'] = labor_child_dict[ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + 'Other Expense'][1]
								qt_row2['PY_List_Price'] = labor_child_dict[ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + 'Other Expense'][2]
								qt_row2['PY_Sell_Price'] = labor_child_dict[ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + 'Other Expense'][3]
								qt_row2['Final_List_Price'] = labor_child_dict[ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + 'Other Expense'][4]
								qt_row2['Final_Sell_Price'] = labor_child_dict[ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + 'Other Expense'][5]
								qt_row2['Price_Impact'] = labor_child_dict[ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + 'Other Expense'][6]
								qt_row2['Margin'] = labor_child_dict[ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + 'Other Expense'][7]
								qt_row2['Last_Year_Discount'] = labor_child_dict[ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + 'Other Expense'][8]
								qt_row2['Final_Total_Cost_Price'] = labor_child_dict[ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + 'Other Expense'][9]
							else:
								for qt_col in ['Escalation','Total_Discount','PY_List_Price','PY_Sell_Price','Final_List_Price','Final_Sell_Price','Price_Impact','Margin','Last_Year_Discount']:
									qt_row2[qt_col] = 0
							if SC_Pricing_Escalation_LB == "Yes":
								if qt_row2['RY_Total_Expenses'] > qt_row2['PY_Total_Expenses']:
									qt_row2['Escalation_Value'] = (qt_row2['Escalation']/100) * qt_row2['PY_Total_Expenses']
								elif qt_row2['RY_Total_Expenses'] <= qt_row2['PY_Total_Expenses']:
									qt_row2['Escalation_Value'] = (qt_row2['Escalation']/100) * qt_row2['RY_Total_Expenses']	
							else:
								qt_row2['Escalation_Value'] = 0
							qt_row2['Total_Discount_Price'] = qt_row2['Final_List_Price'] * (qt_row2['Total_Discount']/100)
				labor_renewal_summary.Save()
		elif SC_Product_Type == "New":
			cont = item.SelectedAttributes.GetContainerByName("SC_Labor_Summary_Container")
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					qt_row = labor_renewal_summary.AddNewRow()
					qt_row['Service_Product'] = ct_row['Service_Product']
					qt_row['Entitlement'] = ct_row['Entitlement']
					qt_row['Related_Module'] = ct_row['Related Module']
					qt_row['Resource_Type'] = ct_row['Resource_Type']
					qt_row['PY_Service_Product'] = 'None'
					qt_row['PY_Entitlement'] = 'None'
					qt_row['PY_Related_Module'] = 'None'
					qt_row['PY_Resource_Type'] = 'None'
					qt_row['RY_Deliverables_Hours'] = ct_row['Renewal_Year_Deliverables_Hours'] if ct_row['Renewal_Year_Deliverables_Hours'] else 0
					qt_row['C_List_Price'] = float(ct_row['Total_Customer_List_Price'])*ProRatedFactor if ct_row['Total_Customer_List_Price'] else 0
					qt_row['HW_List_Price'] = float(ct_row['Total_Honeywell_List_Price'])*ProRatedFactor if ct_row['Total_Honeywell_List_Price'] else 0
					qt_row['HWl_List_Price_Per_Unit'] = float(ct_row['Honeywell_List_Price'])*ProRatedFactor / float(ct_row['SC_Labor_Hrs_per_Full_Day']) if ct_row['Honeywell_List_Price']!= '' and ct_row['SC_Labor_Hrs_per_Full_Day'] != '' else 0
					qt_row['Customer_List_Price'] = float(ct_row['Customer_List_Price'])*ProRatedFactor if ct_row['Customer_List_Price'] else 0
					for newcol in ['RY_Total_Expenses','PY_Total_Expenses']:
						qt_row[newcol] = 0
					qt_row['SA_Quantity'] = ct_row['Renewal_Year_Deliverables_Hours'] if ct_row['Renewal_Year_Deliverables_Hours'] else 0
					qt_row['SA_Price'] = qt_row['SA_Quantity'] * qt_row['HWl_List_Price_Per_Unit']
					qt_row['Final_List_Price'] = qt_row['SA_Quantity'] * qt_row['HWl_List_Price_Per_Unit']
					if ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + ct_row['Resource_Type'] in labor_child_dict.keys():
						qt_row['Total_Discount'] = labor_child_dict[ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + ct_row['Resource_Type']][1]
					else:
						qt_row['Total_Discount'] = 0
					qt_row['Total_Discount_Price'] = qt_row['Final_List_Price'] * (qt_row['Total_Discount']/100)
					qt_row['Final_Sell_Price'] = qt_row['Final_List_Price'] - qt_row['Total_Discount_Price']
					qt_row['Contigency_Cost'] = float(ct_row['Contigency_Cost'])*ProRatedFactor if ct_row['Contigency_Cost'] else '0'
					qt_row['Final_Total_Cost_Price'] = float(ct_row['Final_Total_Cost_Price'])*ProRatedFactor*(1+(qt_row['Escalation']/100)) if ct_row['Final_Total_Cost_Price'] else '0'
					qt_row['Margin'] = (1 - (float(qt_row['Final_Total_Cost_Price']) / float(qt_row['Final_Sell_Price']))) * 100 if qt_row['Final_Sell_Price'] not in (0,'0','',0.00,'0.00','0.0',0.0) else 0
					qt_row['Scope_Change'] = qt_row['Final_Sell_Price'] if qt_row['Final_Sell_Price'] else '0'
					qt_row['Comments'] = 'Scope Addition'
					if ct_row['Other_Expenses'] not in ('0','0.00','',0.0,'0.0'):
						qt_row2 = labor_renewal_summary.AddNewRow()
						qt_row2['Resource_Type'] = 'Total Expense'
						qt_row2['PY_Service_Product'] = 'None'
						qt_row2['PY_Entitlement'] = 'None'
						qt_row2['PY_Related_Module'] = 'None'
						qt_row2['PY_Resource_Type'] = 'None'
						qt_row2['Service_Product'] = ct_row['Service_Product']
						qt_row2['Entitlement'] = ct_row['Entitlement']
						qt_row2['Related_Module'] = ct_row['Related Module']
						qt_row2['RY_Total_Expenses'] = float(ct_row['Renewal_Year_Total_Expenses'])*ProRatedFactor if ct_row['Renewal_Year_Total_Expenses'] else 0
						if ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + 'Other Expense' in labor_child_dict.keys():
							qt_row2['Total_Discount'] = labor_child_dict[ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + 'Other Expense'][1]
							qt_row2['Final_List_Price'] = labor_child_dict[ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + 'Other Expense'][4]
							qt_row2['Final_Sell_Price'] = labor_child_dict[ct_row['Service_Product'] + "|" + ct_row['Entitlement'] + "|" + 'Other Expense'][5]
						else:
							qt_row2['Total_Discount'] = 0
							qt_row2['Final_List_Price'] = 0
							qt_row2['Final_Sell_Price'] = 0
						qt_row2['Total_Discount_Price'] = qt_row2['Final_List_Price'] * (qt_row2['Total_Discount']/100)
						qt_row2['Comments'] = 'Scope Addition'
		labor_renewal_summary.Save()
	if v_mod_name == "Trace":
		Trace_Child_Dict=v_child_dict
		Trace_Renewal_Summary = Quote.QuoteTables["QT_SC_Trace_Renewal_Summary"]
		Trace_Renewal_Summary.Rows.Clear()
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		if SC_Product_Type == "Renewal":
			SC_Pricing_Escalation_TR = next(val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Pricing_Escalation')
			cont = item.SelectedAttributes.GetContainerByName("SC_Trace_Summary")
			compCont = item.SelectedAttributes.GetContainerByName('ComparisonSummary')
			scope_removed = []
			Configured_PY_Sell_Price = 0
			if compCont.Rows.Count:
				for cs_row in compCont.Rows:
					Configured_PY_Sell_Price = float(cs_row['Configured_PY_Sell_Price'])*ProRatedFactor if cs_row['Configured_PY_Sell_Price'] else '0'
					if cs_row.IsSelected == True:
						scope_removed.append(cs_row['Service_Product'])
						qt_row = Trace_Renewal_Summary.AddNewRow()
						qt_row['Service_Product_Current_year'] = cs_row['Service_Product']
						qt_row['Previous_Year_List_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Previous_year_cost_price'] = str(round((1-float(cs_row['Booked_Margin'])/100) *float(cs_row["PY_Sell_Price_SFDC"])*ProRatedFactor,2)) if cs_row["PY_Sell_Price_SFDC"] and cs_row['Booked_Margin'] else "0"
						qt_row['Scope_reduction_Price'] = (-1)*float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Last_Year_Discount'] = float(cs_row['PY_Discount_SFDC'])*100 if cs_row['PY_Discount_SFDC'] else 0
						qt_row['Previous_Year_Sell_Price'] = float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Scope_Change'] = str(round(-float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor,2)) if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Comments'] = "Scope Reduction"
						for col in ['Renewal_Quantity','Current_year_list_Price','Current_year_cost_price','Escalation','Total_Discount','Scope_Addition_Price','Escalation_price','Final_List_Price','Total_Discount_Price','Final_Sell_Price','Price_Impact']:
							qt_row[col] = 0
				Trace_Renewal_Summary.Save()
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					if ct_row['Service_Product'] not in scope_removed:
						qt_row = Trace_Renewal_Summary.AddNewRow()
						qt_row['Service_Product_Current_year'] = ct_row['Service_Product']
						qt_row['Renewal_Quantity'] = ct_row['Quantity']
						qt_row['Previous_Year_List_Price'] = float(ct_row['PY_ListPrice'])*ProRatedFactor if ct_row['PY_ListPrice'] else 0
						qt_row['Current_year_list_Price'] = float(ct_row['CY_ListPrice'])*ProRatedFactor if ct_row['CY_ListPrice'] else 0
						qt_row['Previous_year_cost_price'] = float(ct_row['PY_CostPrice'])*ProRatedFactor if ct_row['PY_CostPrice'] else 0
						qt_row['Current_year_cost_price'] = float(ct_row['CY_CostPrice'])*ProRatedFactor if ct_row['CY_CostPrice'] else 0
						qt_row['Scope_reduction_Price'] = float(ct_row['SR_Price'])*ProRatedFactor if ct_row['SR_Price'] else 0
						try:
							qt_row['Escalation'] = Trace_Child_Dict[ct_row['Service_Product']][0]
							qt_row['Total_Discount'] = Trace_Child_Dict[ct_row['Service_Product']][1]
						except:
							qt_row['Escalation'] = 0
							qt_row['Total_Discount'] = 0
						qt_row['Scope_Addition_Price'] = float(ct_row['SA_Price'])*ProRatedFactor if ct_row['SA_Price'] else 0
						if SC_Pricing_Escalation_TR == "No":
							qt_row['Escalation_price'] = 0
							qt_row['Final_List_Price'] = float(ct_row['CY_ListPrice'])*ProRatedFactor if ct_row['CY_ListPrice'] else 0
						elif SC_Pricing_Escalation_TR == "Yes":
							qt_row['Escalation_price'] = qt_row['Escalation'] / 100 * (qt_row['Previous_Year_List_Price'] - qt_row['Scope_Reduction_Price'])
							qt_row['Final_List_Price'] = qt_row['Previous_Year_List_Price'] + qt_row['Scope_Addition_Price'] + qt_row['Scope_Reduction_Price'] + qt_row['Escalation_price']
						qt_row['Last_Year_Discount'] = ct_row['PY_Discount'] if ct_row['PY_Discount'] else 0
						qt_row['Total_Discount_Price'] = (qt_row['Final_List_Price']/100) * qt_row['Total_Discount']
						qt_row['Previous_Year_Sell_Price'] = Configured_PY_Sell_Price
						qt_row['Final_Sell_Price'] = qt_row['Final_List_Price'] - qt_row['Total_Discount_Price']
						if qt_row['Previous_Year_List_Price'] not in ('',0,'0') and qt_row['Final_List_Price'] not in ('',0,'0'):
							qt_row['Scope_Change'] = (qt_row['Scope_reduction_Price']*(qt_row['Previous_Year_Sell_Price']/qt_row['Previous_Year_List_Price'])) + (qt_row['Scope_Addition_Price']*(qt_row['Final_Sell_Price']/qt_row['Final_List_Price']))
						elif qt_row['Final_List_Price'] not in ('',0,'0') and qt_row['Previous_Year_List_Price'] in ('',0,'0'):
							qt_row['Scope_Change'] = (qt_row['Scope_Addition_Price']*(qt_row['Final_Sell_Price']/qt_row['Final_List_Price']))
						elif qt_row['Previous_Year_List_Price'] not in ('',0,'0') and qt_row['Final_List_Price'] in ('',0,'0'):
							qt_row['Scope_Change'] = (qt_row['Scope_reduction_Price']*(qt_row['Previous_Year_Sell_Price']/qt_row['Previous_Year_List_Price']))
						qt_row['Price_Impact'] = qt_row['Final_Sell_Price'] - (qt_row['Scope_Change'] + qt_row['Previous_Year_Sell_Price'])
						qt_row['Comments'] = ct_row['Comments']
				Trace_Renewal_Summary.Save()
		elif SC_Product_Type == "New":
			cont = item.SelectedAttributes.GetContainerByName("SC_Trace_Summary")
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					qt_row = Trace_Renewal_Summary.AddNewRow()
					for col in ['Previous_Year_List_Price','Previous_year_cost_price','Scope_reduction_Price','Escalation','Escalation_price','Last_Year_Discount','Previous_Year_Sell_Price','Price_Impact']:
						qt_row[col] = 0
					qt_row['Service_Product_Current_year'] = ct_row['Service_Product']
					qt_row['Renewal_Quantity'] = 1
					qt_row['Current_year_list_Price'] = float(ct_row['CY_ListPrice'])*ProRatedFactor if ct_row['CY_ListPrice'] else 0
					qt_row['Current_year_cost_price'] = float(ct_row['CY_CostPrice'])*ProRatedFactor if ct_row['CY_CostPrice'] else 0
					qt_row['Scope_Addition_Price'] = qt_row['Current_year_list_Price']
					qt_row['Final_List_Price'] = qt_row['Current_year_list_Price']
					try:
						qt_row['Total_Discount'] = Trace_Child_Dict[ct_row['Service_Product']][1]
					except:
						qt_row['Total_Discount'] = 0
					qt_row['Total_Discount_Price'] = (qt_row['Final_List_Price']/100) * qt_row['Total_Discount']
					qt_row['Final_Sell_Price'] = qt_row['Final_List_Price'] - qt_row['Total_Discount_Price']
					qt_row['Scope_Change'] = qt_row['Final_Sell_Price']
					qt_row['Comments'] = "Scope Addition"
				Trace_Renewal_Summary.Save()
	if v_mod_name == "MES Performix":
		mes_child_dict=v_child_dict
		mes_renewal_summary = Quote.QuoteTables["MES_Renewal_Summary"]
		mes_renewal_summary.Rows.Clear()
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		if SC_Product_Type == "Renewal":
			SC_Pricing_Escalation_MES = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Pricing_Escalation'), '')
			SC_Scope_Removal = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_ScopeRemoval'), '')
			SC_Service_Product = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_MES_ServiceProduct'), '')
			cont = item.SelectedAttributes.GetContainerByName("SC_MES_Models_Hidden")
			compCont = item.SelectedAttributes.GetContainerByName("ComparisonSummary")
			if compCont.Rows.Count:
				for cs_row in compCont.Rows:
					if cs_row.IsSelected == True:
						qt_row = mes_renewal_summary.AddNewRow()
						qt_row['MES_Models'] = cs_row['Service_Product']
						qt_row['Description'] = "Scope Removed"
						qt_row['Previous_Year_Quantity'] = 1
						qt_row['Previous_Year_Unit_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Previous_Year_List_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Scope_Reduction_Quantity'] = -1
						qt_row['Last_Year_Discount'] = float(cs_row['PY_Discount_SFDC'])*100 if cs_row['PY_Discount_SFDC'] else 0
						qt_row['Scope_Reduction_Price'] = (-1)*float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Previous_Year_Sell_Price'] = float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Scope_Change_Price'] = str(round(-float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor,2)) if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Comments'] = "Scope Reduction"
						for col in ['Renewal_Quantity','Honeywell_List_Price_Per_Unit','Honeywell_List_Price','Scope_Addition_Quantity','Scope_Addition_Price','Escalation','Total_Discount','Escalation_Value','Final_List_Price','Total_Discount_Amount','Final_Sell_Price','Price_Impact']:
							qt_row[col] = 0
				mes_renewal_summary.Save()
			if SC_Service_Product != SC_Scope_Removal:
				if cont.Rows.Count:
					for ct_row in cont.Rows:
						qt_row = mes_renewal_summary.AddNewRow()
						qt_row['MES_Models'] = ct_row['MES Models']
						qt_row['Description'] = ct_row['Description']
						qt_row['Previous_Year_Quantity'] = ct_row['PY_Quantity'] if ct_row['PY_Quantity'] != "" else 0
						qt_row['Renewal_Quantity'] = ct_row['Renewal_Quantity'] if ct_row['Renewal_Quantity'] != "" else 0
						qt_row['Previous_Year_Unit_Price'] = float(ct_row['PY_UnitPrice'])*ProRatedFactor if ct_row['PY_UnitPrice'] != "" else 0
						qt_row['Previous_Year_List_Price'] = float(ct_row['PY_ListPrice'])*ProRatedFactor if ct_row['PY_ListPrice'] != "" else 0
						qt_row['Honeywell_List_Price_Per_Unit'] = float(ct_row['HW_UnitPrice'])*ProRatedFactor if ct_row['HW_UnitPrice'] != "" else 0
						qt_row['Honeywell_List_Price'] = float(ct_row['HW_ListPrice'])*ProRatedFactor if ct_row['HW_ListPrice'] != "" else 0
						qt_row['Scope_Reduction_Quantity'] = ct_row['SR_Quantity'] if ct_row['SR_Quantity'] != "" else 0
						qt_row['Scope_Addition_Quantity'] = ct_row['SA_Quantity'] if ct_row['SA_Quantity'] != "" else 0
						try:
							qt_row['Escalation'] = mes_child_dict["MES Models"][0]
							qt_row['Total_Discount'] = mes_child_dict["MES Models"][1]
						except:
							qt_row['Escalation'] = 0
							qt_row['Total_Discount'] = 0
						qt_row['Last_Year_Discount'] = ct_row['PY_Discount']
						qt_row['Scope_Reduction_Price'] = qt_row['Scope_Reduction_Quantity']*qt_row['Previous_Year_Unit_Price']
						qt_row['Scope_Addition_Price'] = qt_row['Scope_Addition_Quantity']*qt_row['Honeywell_List_Price_Per_Unit']
						if SC_Pricing_Escalation_MES == "No":
							qt_row['Escalation_Value'] = 0
							qt_row['Final_List_Price'] = qt_row['Honeywell_List_Price'] if qt_row['Honeywell_List_Price'] !='' else '0'
						elif SC_Pricing_Escalation_MES == "Yes":
							if qt_row['Renewal_Quantity'] > qt_row['Previous_Year_Quantity']:
								qt_row['Escalation_Value'] = (qt_row['Escalation']) / 100 * qt_row['Previous_Year_Quantity'] * qt_row['Previous_Year_Unit_Price']
							else:
								qt_row['Escalation_Value'] = (qt_row['Escalation']) / 100 * qt_row['Renewal_Quantity'] * qt_row['Previous_Year_Unit_Price']
							qt_row['Final_List_Price'] = qt_row['Previous_Year_List_Price'] + qt_row['Scope_Reduction_Price'] + qt_row['Escalation_Value'] + qt_row['Scope_Addition_Price']
						qt_row['Total_Discount_Amount'] = qt_row['Final_List_Price'] * (qt_row['Total_Discount']/100)
						qt_row['Previous_Year_Sell_Price'] = float(ct_row['PY_SellPrice'])*ProRatedFactor if ct_row['PY_SellPrice'] != "" else 0
						qt_row['Final_Sell_Price'] = qt_row['Final_List_Price'] - qt_row['Total_Discount_Amount']
						Reduction_val = 0
						Addition_val = 0
						if qt_row['Previous_Year_List_Price'] not in (0,""):
							Reduction_val = qt_row['Scope_Reduction_Price'] * (qt_row['Previous_Year_Sell_Price']/qt_row['Previous_Year_List_Price'])
						if qt_row['Final_List_Price'] not in (0,""):
							Addition_val = qt_row['Scope_Addition_Price'] * (qt_row['Final_Sell_Price']/qt_row['Final_List_Price'])
						qt_row['Scope_Change_Price'] = Reduction_val + Addition_val
						qt_row['Price_Impact'] = qt_row['Final_Sell_Price'] - (qt_row['Scope_Change_Price'] + qt_row['Previous_Year_Sell_Price'])
						qt_row['Comments'] = ct_row['Comments']
					mes_renewal_summary.Save()
		elif SC_Product_Type == "New":
			cont = item.SelectedAttributes.GetContainerByName("SC_MES_Models_Hidden")
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					qt_row = mes_renewal_summary.AddNewRow()
					for col in ['Previous_Year_Quantity','Previous_Year_Unit_Price','Previous_Year_List_Price','Scope_Reduction_Quantity','Scope_Reduction_Price','Escalation','Last_Year_Discount','Escalation_Value','Previous_Year_Sell_Price','Price_Impact']:
						qt_row[col] = 0
					qt_row['MES_Models'] = ct_row['MES Models']
					qt_row['Description'] = ct_row['Description']
					qt_row['Renewal_Quantity'] = ct_row['Quantity'] if ct_row['Quantity'] != "" else 0
					qt_row['Honeywell_List_Price_Per_Unit'] = float(ct_row['Unit Price'])*ProRatedFactor if ct_row['Unit Price'] != "" else 0
					qt_row['Honeywell_List_Price'] = float(ct_row['List Price'])*ProRatedFactor if ct_row['List Price'] != "" else 0
					qt_row['Scope_Addition_Quantity'] = ct_row['Quantity'] if ct_row['Quantity'] != "" else 0
					qt_row['Scope_Addition_Price'] = qt_row['Scope_Addition_Quantity']*qt_row['Honeywell_List_Price_Per_Unit']
					qt_row['Final_List_Price'] = qt_row['Previous_Year_List_Price'] + qt_row['Scope_Reduction_Price'] + qt_row['Escalation_Value'] + qt_row['Scope_Addition_Price']
					try:
						qt_row['Total_Discount'] = mes_child_dict["MES Models"][1]
					except:
						qt_row['Total_Discount'] = 0
					qt_row['Total_Discount_Amount'] = qt_row['Final_List_Price'] * (qt_row['Total_Discount']/100)
					qt_row['Final_Sell_Price'] = qt_row['Final_List_Price'] - qt_row['Total_Discount_Amount']
					if qt_row['Final_List_Price'] not in (0,""):
						qt_row['Scope_Change_Price'] = qt_row['Scope_Addition_Price'] * (qt_row['Final_Sell_Price']/qt_row['Final_List_Price'])
					else:
						qt_row['Scope_Change_Price'] = 0
					qt_row['Comments'] = "Scope Addition"
				mes_renewal_summary.Save()