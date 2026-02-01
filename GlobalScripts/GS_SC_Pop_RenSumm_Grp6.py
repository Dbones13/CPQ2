def fn_load_QuoteTable_Grp6(Quote,v_mod_name,item,v_child_dict,ProRatedFactor):
    if v_mod_name == "Generic Module":
		cyber_child_dict=v_child_dict
		Trace.Write("Nilesh Test cyber_child_dict -" + str(cyber_child_dict))
		cyber_renewal_summary = Quote.QuoteTables["Genericl_Module_Renewal_Summary"]
		#cyber_renewal_summary.Rows.Clear()
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		Trace.Write("NileshTest inside Grp6-" + str(SC_Product_Type))
		if SC_Product_Type == "Renewal":
			SC_Pricing_Escalation = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Pricing_Escalation'), '')
			cont = item.SelectedAttributes.GetContainerByName("SC_GN_AT_Models_Scope_Cont")
			compCont = item.SelectedAttributes.GetContainerByName('ComparisonSummary')
			scope_removed = []
			if compCont.Rows.Count:
				for cs_row in compCont.Rows:
					if cs_row.IsSelected == True:
						scope_removed.append(cs_row['Service_Product'])
						qt_row = cyber_renewal_summary.AddNewRow()
						qt_row['Service_Product'] = cs_row['Service_Product']
						qt_row['Asset_No'] = ""
						qt_row['Model_Number'] = ""
						qt_row['Description'] = "Scope Removed"
						qt_row['Previous_Year_Quantity'] = 1
						qt_row['Previous_Year_List_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] != '' else 0
						qt_row['Scope_Reduction_Quantity'] = -1
						qt_row['Scope_Reduction_Price'] = (-1)*float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] != '' else 0
						qt_row['Last_Year_Discount'] = float(cs_row['PY_Discount_SFDC'])*100 if cs_row['PY_Discount_SFDC'] != '' else 0
						qt_row['Previous_Year_Sell_Price'] = float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor if cs_row['PY_Sell_Price_SFDC'] != '' else 0
						qt_row['Previous_Year_Cost_Price'] = round((1-float(cs_row['Booked_Margin'])/100) *float(cs_row["PY_Sell_Price_SFDC"])*ProRatedFactor,2) if cs_row["PY_Sell_Price_SFDC"] and cs_row['Booked_Margin'] else 0
						qt_row['Scope_Change'] = str(round(-float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor,2)) if cs_row['PY_Sell_Price_SFDC'] != '' else 0
						qt_row['Comments'] = "Scope Reduction"
						for col in ['Renewal_Quantity','Honeywell_List_Price_per_Unit','Honeywell_List_Price','Scope_Addition_Quantity','Scope_Addition_Price','Escalation','Total_Discount','Escalation_Value','Final_List_Price','Total_Discount_Price','Final_Sell_Price','Price_Impact','Current_Year_Cost_Price','Margin']:
							qt_row[col] = 0
				cyber_renewal_summary.Save()
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					if ct_row['Service_Product'] not in scope_removed:
						qt_row = cyber_renewal_summary.AddNewRow()
						qt_row['Service_Product'] = ct_row['Service_Product']
						qt_row['Asset_No'] = ct_row['Asset No']
						qt_row['Model_Number'] = ct_row['Model_Number']
						qt_row['Description'] = ct_row['Description']
						qt_row['Previous_Year_Quantity'] = ct_row['PY_Quantity'] if ct_row['PY_Quantity'] != '' else 0
						qt_row['Renewal_Quantity'] = ct_row['Renewal_Quantity'] if ct_row['Renewal_Quantity'] != '' else 0
						qt_row['Previous_Year_List_Price'] = float(ct_row['PY_ListPrice'])*ProRatedFactor if ct_row['PY_ListPrice'] != '' else 0
						qt_row['Honeywell_List_Price_per_Unit'] = float(ct_row['HW_UnitPrice'])*ProRatedFactor if ct_row['HW_UnitPrice'] != '' else 0
						qt_row['Honeywell_List_Price'] = float(ct_row['CY_ListPrice'])*ProRatedFactor if ct_row['CY_ListPrice'] != '' else 0
						qt_row['Scope_Reduction_Quantity'] = ct_row['SR_Quantity'] if ct_row['SR_Quantity'] != '' else 0
						qt_row['Scope_Reduction_Price'] = (qt_row['Scope_Reduction_Quantity'] * (qt_row['Previous_Year_List_Price']/qt_row['Previous_Year_Quantity'])) if qt_row['Previous_Year_Quantity'] not in (0,'','0') else 0
						qt_row['Scope_Addition_Quantity'] = ct_row['SA_Quantity'] if ct_row['SA_Quantity'] != '' else 0
						qt_row['Scope_Addition_Price'] = (qt_row['Scope_Addition_Quantity'] * qt_row['Honeywell_List_Price_per_Unit'])
						try:
							if ct_row['Service_Product'] in cyber_child_dict.keys():
								qt_row['Escalation'] = cyber_child_dict[ct_row['Service_Product']][0]
								qt_row['Total_Discount'] = cyber_child_dict[ct_row['Service_Product']][1]
						except:
							qt_row['Escalation'] = 0
							qt_row['Total_Discount'] = 0
						qt_row['Last_Year_Discount'] = float(ct_row['LY_Discount']) * 100 if ct_row['LY_Discount'] != '' else 0
						qt_row['Previous_Year_Sell_Price'] = float(ct_row['PY_SellPrice'])*ProRatedFactor if ct_row['PY_SellPrice'] != '' else 0
						if SC_Pricing_Escalation == "No":
							qt_row['Escalation_Value'] = 0
							qt_row['Final_List_Price'] = float(ct_row['Renewal_Quantity']) * (float(ct_row['HW_UnitPrice'])*ProRatedFactor  if ct_row['HW_UnitPrice'] !='' else 0)
						elif SC_Pricing_Escalation == "Yes":
							if ct_row['Renewal_Quantity'] > ct_row['PY_Quantity']:
								qt_row['Escalation_Value'] = ((qt_row['Escalation']/100) * qt_row['Previous_Year_List_Price'])
							else:
								qt_row['Escalation_Value'] = ((qt_row['Escalation']/100) * (qt_row['Previous_Year_List_Price']/qt_row['Previous_Year_Quantity']) * qt_row['Renewal_Quantity']) if qt_row['Previous_Year_Quantity'] not in (0,'','0') else 0
							qt_row['Final_List_Price'] = (qt_row['Previous_Year_List_Price']+qt_row['Escalation_Value']+qt_row['Scope_Reduction_Price']+qt_row['Scope_Addition_Price'])
						qt_row['Final_Sell_Price'] = (qt_row['Final_List_Price'] * (1 - qt_row['Total_Discount']/100)) 
						qt_row['Total_Discount_Price'] = (qt_row['Final_List_Price'] * (qt_row['Total_Discount']/100))
						Reduction_val = (qt_row['Scope_Reduction_Price'] * (qt_row['Previous_Year_Sell_Price']/qt_row['Previous_Year_List_Price'])) if qt_row['Previous_Year_List_Price'] not in (0,'','0') else 0
						Addition_val = (qt_row['Scope_Addition_Price'] * (qt_row['Final_Sell_Price']/qt_row['Final_List_Price'])) if qt_row['Final_List_Price'] not in (0,'','0') else 0
						qt_row['Scope_Change'] = Reduction_val + Addition_val
						qt_row['Price_Impact'] = qt_row['Final_Sell_Price'] - (qt_row['Scope_Change']+qt_row['Previous_Year_Sell_Price'])
						qt_row['Previous_Year_Cost_Price'] = float(ct_row['PY_CostPrice'])*ProRatedFactor if ct_row['PY_CostPrice'] != "" else 0
						qt_row['Current_Year_Cost_Price'] = float(ct_row['CY_CostPrice'])*ProRatedFactor if ct_row['CY_CostPrice'] != "" else 0
						qt_row['Margin'] = ((1 - (qt_row['Current_Year_Cost_Price']/qt_row['Final_Sell_Price'])) * 100) if qt_row['Final_Sell_Price'] not in (0,'','0') else 0
						qt_row['Comments'] = ct_row['Comments']
				cyber_renewal_summary.Save()
		elif SC_Product_Type == "New":
			Trace.Write("Nilesh Test SC_Product_Type Line 82 -" + str(SC_Product_Type))
			cont = item.SelectedAttributes.GetContainerByName("SC_GN_AT_Models_Scope_Cont")
			Trace.Write("Nilesh Test cont Line 84 cont -" + str(cont))
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					qt_row = cyber_renewal_summary.AddNewRow()
					for col in ['Previous_Year_Quantity','Previous_Year_List_Price','Scope_Reduction_Quantity','Scope_Reduction_Price','Escalation','Last_Year_Discount','Escalation_Value','Previous_Year_Sell_Price','Price_Impact','Previous_Year_Cost_Price']:
						qt_row[col] = 0
					qt_row['Service_Product'] = ct_row['Service_Product']
					qt_row['Asset_No'] = ct_row['Asset No']
					qt_row['Model_Number'] = ct_row['Model']
					qt_row['Description'] = ct_row['Description']
					qt_row['Renewal_Quantity'] = ct_row['Quantity'] if ct_row['Quantity'] != '' else 0
					qt_row['Honeywell_List_Price_per_Unit'] = float(ct_row['Unit_List_Price'])*ProRatedFactor if ct_row['Unit_List_Price'] != '' else 0
					#qt_row['Honeywell_List_Price'] = float(ct_row['Unit_List_Price'])*ProRatedFactor if ct_row['CY_ListPrice'] != '' else 0
					qt_row['Honeywell_List_Price'] = float(qt_row['Honeywell_List_Price_per_Unit'])*float(qt_row['Renewal_Quantity'])*ProRatedFactor if qt_row['Honeywell_List_Price_per_Unit'] != '' else 0
					try:
						#Trace.Write("Nilesh Test cyber_child_dict Service_Product - " + str(cyber_child_dict) + "--" + str(ct_row['Service_Product'] ))
						if ct_row['Service_Product'] in cyber_child_dict.keys():
							qt_row['Total_Discount'] = cyber_child_dict[ct_row['Service_Product']][1]
					except:
						qt_row['Total_Discount'] = 0
					qt_row['Scope_Addition_Quantity'] = ct_row['Renewal_Quantity'] if ct_row['Renewal_Quantity'] != '' else 0
					qt_row['Scope_Addition_Price'] = qt_row['Scope_Addition_Quantity'] * qt_row['Honeywell_List_Price_per_Unit']
					qt_row['Final_List_Price'] = (qt_row['Honeywell_List_Price']+qt_row['Escalation_Value']+qt_row['Scope_Reduction_Price']+qt_row['Scope_Addition_Price'])
                    #qt_row['Final_List_Price'] = (qt_row['Previous_Year_List_Price']+qt_row['Escalation_Value']+qt_row['Scope_Reduction_Price']+qt_row['Scope_Addition_Price'])
					qt_row['Total_Discount_Price'] = (qt_row['Total_Discount']/100) * qt_row['Final_List_Price']
					qt_row['Final_Sell_Price'] = qt_row['Final_List_Price'] * (1 - qt_row['Total_Discount']/100)
					qt_row['Scope_Change'] = qt_row['Final_Sell_Price']
					qt_row['Current_Year_Cost_Price'] = float(ct_row['Unit_Cost_Price'])* float(qt_row['Renewal_Quantity'])*ProRatedFactor if ct_row['Unit_Cost_Price'] != '' else 0
                    #qt_row['Current_Year_Cost_Price'] = float(ct_row['Cost_Price'])*ProRatedFactor if ct_row['Cost_Price'] != '' else 0
					qt_row['Margin'] = round(1-(float(qt_row['Current_Year_Cost_Price']) / float(qt_row["Final_Sell_Price"])),2) if qt_row["Final_Sell_Price"] not in (0,'','0') else 0
					qt_row['Margin'] = float(qt_row['Margin'])*100
					qt_row['Comments'] = 'Scope Addition'
				cyber_renewal_summary.Save()