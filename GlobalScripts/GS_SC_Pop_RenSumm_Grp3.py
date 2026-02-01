#Honeywell Digital Prime, Experion Extended Support - RQUP ONLY, BGP and QCS
def fn_load_QuoteTable_Grp3(Quote,v_mod_name,item,v_child_dict,ProRatedFactor):
	if v_mod_name == "Honeywell Digital Prime":
		HDP_child_dict=v_child_dict
		Honeywell_Digital_Prime = Quote.QuoteTables["Honeywell_Digital_Prime"]
		Honeywell_Digital_Prime.Rows.Clear()
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		SC_Pricing_Escalation = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Pricing_Escalation'),"None")
		if SC_Product_Type == "Renewal":
			cont = item.SelectedAttributes.GetContainerByName("SC_RC_Honeywell_Scope_Summary_Pricing_Hidden")
			compCont = item.SelectedAttributes.GetContainerByName("ComparisonSummary")
			scope_removed = []
			for cs_row in compCont.Rows:
				if cs_row.IsSelected == True:
					for ct_row in cont.Rows:
						qt_row = Honeywell_Digital_Prime.AddNewRow()
						qt_row['Description'] = "Scope Removed"
						qt_row['Previous_Year_Quantity'] = ct_row['PY_Quantity'] if ct_row['PY_Quantity'] != '' else '0'
						qt_row['Previous_Year_Unit_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Previous_Year_List_Price'] = float(qt_row['Previous_Year_Quantity']) * (float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor) if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Scope_Reduction_Quantity'] = ct_row['SR_Quantity'] if ct_row['SR_Quantity'] != '' else '0'
						qt_row['Scope_Reduction_Price'] = qt_row['Scope_Reduction_Quantity'] * (float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor) if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Last_Year_Discount_'] = float(cs_row['PY_Discount_SFDC'])*100 if cs_row['PY_Discount_SFDC'] else 0
						qt_row['Previous_Year_Sell_Price'] = float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Scope_Change'] = str(round(-float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor,2)) if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Comments'] = "Scope Reduction"
						for col in ['Renewal_Quantity','Honeywell_List_Price_per_Unit','Honeywell_List_Price','Scope_Addition_Quantity','Scope_Addition_Price','Escalation_','Total_Discount_','Escalation_Value','Final_List_Price','Total_Discount_Price','Final_Sell_Price','Price_Impact']:
							qt_row[col] = 0
				Honeywell_Digital_Prime.Save()
		if SC_Product_Type == "Renewal":
			cont = item.SelectedAttributes.GetContainerByName("SC_RC_Honeywell_Scope_Summary_Pricing_Hidden")
			compCont = item.SelectedAttributes.GetContainerByName("ComparisonSummary")
			if cont.Rows.Count:
				for cs_row in compCont.Rows:
					if cs_row.IsSelected == False:
						for ct_row in cont.Rows:
							qt_row = Honeywell_Digital_Prime.AddNewRow()
							qt_row['Description'] = ct_row['Description']
							qt_row['Previous_Year_Quantity'] = ct_row['PY_Quantity'] if ct_row['PY_Quantity'] != '' else '0'
							qt_row['Renewal_Quantity'] = ct_row['Quantity'] if ct_row['Quantity'] != '' else '0'
							qt_row['Previous_Year_Unit_Price'] = float(ct_row['PY_UnitPrice'])*ProRatedFactor if ct_row['PY_UnitPrice'] != '' else '0'
							qt_row['Previous_Year_List_Price'] = float(ct_row['PY_ListPrice'])*ProRatedFactor if ct_row['PY_ListPrice'] != '' else '0'
							qt_row['Honeywell_List_Price_Per_Unit'] = float(ct_row['HW_ListPrice'])*ProRatedFactor if ct_row['HW_ListPrice'] != '' else '0'
							qt_row['Honeywell_List_Price'] = qt_row['Honeywell_List_Price_Per_Unit'] * qt_row['Renewal_Quantity']
							qt_row['Scope_Reduction_Quantity'] = ct_row['SR_Quantity'] if ct_row['SR_Quantity'] != '' else '0'
							if qt_row['Previous_Year_Quantity']:
								qt_row['Scope_Reduction_Price'] = qt_row['Scope_Reduction_Quantity'] * (qt_row['Previous_Year_List_Price']/qt_row['Previous_Year_Quantity'])
							try:
								qt_row['Escalation_'] = float(HDP_child_dict["Digital Prime Twin"][0])
								qt_row['Total_Discount_'] = float(HDP_child_dict["Digital Prime Twin"][1])
								qt_row['Last_Year_Discount_'] = float(ct_row['LY_Discount']) if ct_row['LY_Discount'] != '' else '0'
							except:
								qt_row['Escalation_'] = 0
								qt_row['Total_Discount_'] = 0
								qt_row['Last_Year_Discount_'] = 0
							if qt_row['Renewal_Quantity'] > qt_row['Previous_Year_Quantity']:
								qt_row['Escalation_Value'] = qt_row['Escalation_'] * ((qt_row['Previous_Year_Unit_Price'] * qt_row['Previous_Year_Quantity'])/100)
							else:
								if qt_row['Previous_Year_Quantity']:
									qt_row['Escalation_Value'] = qt_row['Escalation_'] * ((qt_row['Previous_Year_Unit_Price'] * qt_row['Renewal_Quantity'])/100)
							if SC_Pricing_Escalation == "No":
								qt_row["Escalation_Value"] = "0"
							qt_row['Scope_Addition_Quantity'] = ct_row['SA_Quantity'] if ct_row['SA_Quantity'] != '' else '0'
							qt_row['Scope_Addition_Price'] = qt_row['Scope_Addition_Quantity'] * qt_row['Honeywell_List_Price_per_Unit']
							qt_row['Final_List_Price'] = qt_row['Previous_Year_List_Price']+qt_row['Escalation_Value']+qt_row['Scope_Reduction_Price']+qt_row['Scope_Addition_Price']
							if SC_Pricing_Escalation == "No":
								qt_row["Final_List_Price"] = qt_row['Honeywell_List_Price_Per_Unit'] * qt_row['Renewal_Quantity']
							qt_row['Previous_Year_Sell_Price'] = float(ct_row['PY_SellPrice'])*ProRatedFactor if ct_row['PY_SellPrice'] != '' else '0'
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
							qt_row['Comments'] = ct_row['Comments']
						Honeywell_Digital_Prime.Save()
		elif SC_Product_Type == "New":
			cont = item.SelectedAttributes.GetContainerByName("SC_RC_Honeywell_Scope_Summary_Pricing_Hidden")
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					qt_row = Honeywell_Digital_Prime.AddNewRow()
					qt_row['Description'] = ct_row['Description']
					qt_row['Previous_Year_Quantity'] = 0
					qt_row['Renewal_Quantity'] = ct_row['Quantity'] if ct_row['Quantity'] != '' else 0
					qt_row['Previous_Year_List_Price'] = 0
					qt_row['Honeywell_List_Price_Per_Unit'] = ct_row['HW_ListPrice']*ProRatedFactor if ct_row['Quantity']	!= '' else 0
					qt_row['Honeywell_List_Price'] = qt_row['Honeywell_List_Price_Per_Unit'] * qt_row['Renewal_Quantity']
					qt_row['Scope_Reduction_Quantity'] = 0
					qt_row['Scope_Reduction_Price'] = 0
					qt_row['Escalation_'] = 0
					try:
						qt_row['Total_Discount_'] = float(HDP_child_dict['Digital Prime Twin'][1])
					except:
						qt_row['Total_Discount_'] = 0
					qt_row['Last_Year_Discount_'] = 0
					qt_row['Escalation_Value'] = 0
					qt_row['Scope_Addition_Quantity'] = ct_row['Quantity'] if ct_row['Quantity']  != '' else 0
					qt_row['Scope_Addition_Price'] = qt_row['Scope_Addition_Quantity'] * qt_row['Honeywell_List_Price_Per_Unit']
					qt_row['Final_List_Price'] = qt_row['Previous_Year_List_Price']+qt_row['Escalation_Value']+qt_row['Scope_Reduction_Price']+qt_row['Scope_Addition_Price']
					qt_row['Total_Discount_Price'] = qt_row['Total_Discount_'] * (qt_row['Final_List_Price']/100)
					qt_row['Previous_Year_Sell_Price'] = 0
					qt_row['Final_Sell_Price'] = qt_row['Final_List_Price']	 - qt_row['Total_Discount_Price']
					qt_row['Scope_Change'] = qt_row['Final_Sell_Price']
					qt_row['Price_Impact'] = 0
					qt_row['Comments'] = 'Scope Addition'
				Honeywell_Digital_Prime.Save()
	if v_mod_name== "Experion Extended Support - RQUP ONLY":
		rqup_child_dict=v_child_dict
		rqup_renewal_summary = Quote.QuoteTables["RQUP_Renewal_Summary"]
		rqup_renewal_summary.Rows.Clear()
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		if SC_Product_Type == "Renewal":
			SC_Pricing_Escalation = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Pricing_Escalation'), '')
			SC_ScopeRemoval = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_ScopeRemoval'),"None")
			cont = item.SelectedAttributes.GetContainerByName("SC_Experion_Models_Hidden")
			compCont = item.SelectedAttributes.GetContainerByName("ComparisonSummary")
			if SC_ScopeRemoval == 'True':
				if compCont.Rows.Count:
					for cs_row in compCont.Rows:
						qt_row = rqup_renewal_summary.AddNewRow()
						qt_row['MSID'] = cs_row['Service_Product']
						qt_row['Description'] = "Scope Removed"
						qt_row['Previous_Year_Quantity'] = 1
						qt_row['Previuos_Year_List_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Previous_Year_Cost_Price'] = str(round((1-float(cs_row['Booked_Margin'])/100) *float(cs_row["PY_Sell_Price_SFDC"])*ProRatedFactor,2)) if cs_row["PY_Sell_Price_SFDC"] else 0
						qt_row['Scope_Reduction_Price'] = (-1)*float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Last_Year_Discount_'] = float(cs_row['PY_Discount_SFDC'])*100 if cs_row['PY_Discount_SFDC'] else 0
						qt_row['Previous_Year_Sell_Price'] = float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Scope_Change'] = str(round(-float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor,2)) if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Comment'] = "Scope Reduction"
						for col in ['Renewal_Quantity','Honeywell_List_Price','Cost_Price','Scope_Addition_Price','Escalation_','Total_Discount_','Escalation_Value','Final_List_Price','Total_Discount_Price','Final_Sell_Price','Price_Impact']:
							qt_row[col] = 0
					rqup_renewal_summary.Save()
			else:
				if cont.Rows.Count:
					for ct_row in cont.Rows:
						qt_row = rqup_renewal_summary.AddNewRow()
						qt_row['MSID'] = ct_row['MSIDs']
						qt_row['Description'] = ct_row['Description']
						qt_row['Previous_Year_Quantity'] = ct_row['PY_Quantity'] if ct_row['PY_Quantity'] != '' else 0
						qt_row['Renewal_Quantity'] = float(ct_row['Renewal_Quantity']) if ct_row['Renewal_Quantity'] != '' else 0
						qt_row['Previuos_Year_List_Price'] = float(ct_row['PY_ListPrice'])*ProRatedFactor if ct_row['PY_ListPrice'] != '' else 0
						qt_row['Previous_Year_Cost_Price'] = float(ct_row['PY_CostPrice'])*ProRatedFactor if ct_row['PY_CostPrice'] != '' else 0
						qt_row['Honeywell_List_Price'] = float(ct_row['HW_ListPrice'])*ProRatedFactor if ct_row['HW_ListPrice'] != '' else 0
						qt_row['Cost_Price'] = float(ct_row['Cost_Price'])*ProRatedFactor if ct_row['Cost_Price'] != '' else 0
						qt_row['Scope_Reduction_Price'] = float(ct_row['SR_Price'])*ProRatedFactor if ct_row['SR_Price'] != '' else 0
						qt_row['Scope_Addition_Price'] = float(ct_row['SA_Price'])*ProRatedFactor if ct_row['SA_Price'] != '' else 0
						try:
							if ct_row['MSIDs'] in rqup_child_dict.keys():
								qt_row['Escalation_'] = rqup_child_dict[ct_row['MSIDs']][0]
								qt_row['Total_Discount_'] = rqup_child_dict[ct_row['MSIDs']][1]
						except:
							qt_row['Escalation_'] = 0
							qt_row['Total_Discount_'] = 0
						qt_row['Last_Year_Discount_'] = str(ct_row['LY_Discount']) if ct_row['LY_Discount'] != '' else 0
						qt_row['Previous_Year_Sell_Price'] = str(float(ct_row['PY_SellPrice'])*ProRatedFactor) if ct_row['PY_SellPrice'] != '' else 0
						if SC_Pricing_Escalation == "No":
							qt_row['Escalation_Value'] = 0
							qt_row['Final_List_Price'] = float(ct_row['HW_ListPrice'])*ProRatedFactor if ct_row['HW_ListPrice'] !='' else '0'
						elif SC_Pricing_Escalation == "Yes":
							qt_row['Escalation_Value'] = (float(qt_row['Escalation_'])/100) * (qt_row['Previuos_Year_List_Price'] - qt_row['Scope_Reduction_Price'])
							qt_row['Final_List_price'] = qt_row['Previuos_Year_List_Price']+qt_row['Escalation_Value']+qt_row['Scope_Reduction_Price']+qt_row['Scope_Addition_Price']
						qt_row['Total_Discount_Price'] = qt_row['Final_List_Price'] * (qt_row['Total_Discount_']/100)
						qt_row['Previous_Year_Sell_Price'] = qt_row['Previuos_Year_List_Price'] * (1 - qt_row['Last_Year_Discount_']/100)
						qt_row['Final_Sell_Price'] = qt_row['Final_List_Price'] * (1 - qt_row['Total_Discount_']/100)
						Reduction_val = (qt_row['Scope_Reduction_Price'] * (qt_row['Previous_Year_Sell_Price']/qt_row['Previuos_Year_List_Price'])) if qt_row['Previuos_Year_List_Price'] not in ('0',0,'') else 0
						Addition_val = (qt_row['Scope_Addition_Price'] * (qt_row['Final_Sell_Price']/qt_row['Final_List_Price'])) if qt_row['Final_List_Price'] not in ('0',0,'') else 0
						if SC_ScopeRemoval == 'True':
							qt_row['Scope_Change'] = str(round(-float(qt_row['Previous_Year_Sell_Price']),2))
						else:
							qt_row['Scope_Change'] = Reduction_val + Addition_val
						qt_row['Price_Impact'] = qt_row['Final_Sell_Price'] - (qt_row['Scope_Change']+qt_row['Previous_Year_Sell_Price'])
						qt_row['Comment'] = str(ct_row['Comment'])
					rqup_renewal_summary.Save()
		elif SC_Product_Type == "New":
			cont = item.SelectedAttributes.GetContainerByName("SC_Experion_Models_Hidden")
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					qt_row = rqup_renewal_summary.AddNewRow()
					for col in ['Previous_Year_Quantity','Previuos_Year_List_Price','Previous_Year_Cost_Price','Scope_Reduction_Price','Escalation_','Escalation_Value','Previous_Year_Sell_Price','Price_Impact']:
						qt_row[col] = 0
					qt_row['MSID'] = ct_row['MSIDs']
					qt_row['Description'] = ct_row['Description']
					qt_row['Renewal_Quantity'] = ct_row['Quantity'] if ct_row['Quantity'] else 0
					qt_row['Honeywell_List_Price'] = float(ct_row['List_Price'])*ProRatedFactor if ct_row['List_Price'] else 0
					qt_row['Cost_Price'] = float(ct_row['Cost_Price'])*ProRatedFactor if ct_row['Cost_Price'] else 0
					try:
						if ct_row['Service_Product'] in rqup_child_dict.keys():
							qt_row['Last_Year_Discount_'] = rqup_child_dict[ct_row['Service_Product']][2]
							qt_row['Total_Discount_'] = rqup_child_dict[ct_row['Service_Product']][1]
					except:
						qt_row['Total_Discount_'] = 0
						qt_row['Last_Year_Discount_'] = 0
					qt_row['Scope_Addition_Price'] = float(ct_row['List_Price'])*ProRatedFactor if ct_row['List_Price'] else 0
					qt_row['Final_List_price'] = qt_row['Previuos_Year_List_Price']+qt_row['Escalation_Value']+qt_row['Scope_Reduction_Price']+qt_row['Scope_Addition_Price']
					qt_row['Total_Discount_Price'] = qt_row['Final_List_Price'] * (qt_row['Total_Discount_']/100)
					qt_row['Final_Sell_Price'] = qt_row['Final_List_Price'] - qt_row['Total_Discount_Price']
					Reduction_val = (qt_row['Scope_Reduction_Price'] * (qt_row['Previous_Year_Sell_Price']/qt_row['Previuos_Year_List_Price'])) if qt_row['Previuos_Year_List_Price'] not in ('0',0,'') else 0
					Addition_val = (qt_row['Scope_Addition_Price'] * (qt_row['Final_Sell_Price']/qt_row['Final_List_Price'])) if qt_row['Final_List_Price'] not in ('0',0,'') else 0
					qt_row['Scope_Change'] = qt_row['Final_List_Price'] - qt_row['Total_Discount_Price']
					qt_row['Comment'] = 'Scope Addition'
				rqup_renewal_summary.Save()
	if v_mod_name == "BGP inc Matrikon":
		bgp_child_dict=v_child_dict
		bgp_Renewal_Summary = Quote.QuoteTables["BGP_Renewal_Summary"]
		bgp_Renewal_Summary.Rows.Clear()
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		SA = SR = 0
		if SC_Product_Type == "Renewal":
			cont = item.SelectedAttributes.GetContainerByName("SC_BGP_Models_Cont_Hidden")
			SC_Pricing_Escalation = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Pricing_Escalation'),"None")
			SC_ScopeRemoval = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_ScopeRemoval'), 'False')
			compCont = item.SelectedAttributes.GetContainerByName('ComparisonSummary')
			scope_removed = []
			if compCont.Rows.Count:
				for cs_row in compCont.Rows:
					if cs_row.IsSelected == True:
						scope_removed.append(cs_row['Service_Product'])
						qt_row = bgp_Renewal_Summary.AddNewRow()
						qt_row['Service_Product'] = cs_row['Service_Product']
						qt_row['Asset_No_'] = ""
						qt_row['Model_Number'] = ""
						qt_row['Previous_Year_Quantity'] = 1
						qt_row['Description'] = "Scope Removed"
						qt_row['Previous_Year_List_Price'] = float(cs_row['PY_List_Price_SFDC']) * ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Previous_Year_Cost_Price'] = str(round((1-float(cs_row['Booked_Margin'])/100) *float(cs_row["PY_Sell_Price_SFDC"]),2)* ProRatedFactor) if cs_row["PY_Sell_Price_SFDC"] else "0"
						qt_row['Scope_Reduction_Price'] = (-1)*float(cs_row['PY_List_Price_SFDC']) * ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Last_Year_Discount'] = float(cs_row['PY_Discount_SFDC'])*100 if cs_row['PY_Discount_SFDC'] else 0
						qt_row['Previous_Year_Sell_Price'] = (float(cs_row['PY_Sell_Price_SFDC']) * ProRatedFactor) if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Scope_Change'] = str(round(-float(cs_row['PY_Sell_Price_SFDC']) * ProRatedFactor,2)) if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Comments'] = "Scope Reduction"
						for col in ['Renewal_Quantity','Honeywell_List_Price','Current_Year_Cost_Price','Escalation','Total_Discount','Scope_Addition_Price','Escalation_Value','Final_List_Price','Total_Discount_Price','Final_Sell_Price','Price_Impact','Margin']:
							qt_row[col] = 0
				bgp_Renewal_Summary.Save()
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					if ct_row['Service_Product'] not in scope_removed:
						qt_row = bgp_Renewal_Summary.AddNewRow()
						qt_row['Service_Product'] = ct_row['Service_Product']
						qt_row['Asset_No_'] = ct_row['Asset_No']
						qt_row['Model_Number'] = ct_row['Model_Number']
						qt_row['Description'] = ct_row['Description']
						qt_row['Previous_Year_Quantity'] = ct_row['PY_Quantity'] if ct_row['PY_Quantity'] else '0'
						qt_row['Renewal_Quantity'] = ct_row['Renewal_Quantity'] if ct_row['Renewal_Quantity'] else '0'
						if ct_row['Previous_Year_List_Price'] == "":
							qt_row['Previous_Year_List_Price'] = 0
						else:
							qt_row['Previous_Year_List_Price'] = float(ct_row['Previous_Year_List_Price']) *ProRatedFactor
						qt_row['Honeywell_List_Price'] = float(ct_row['Honeywell_List_Price']) *ProRatedFactor
						if ct_row['Scope Reduction Price'] == "":
							qt_row['Scope_Reduction_Price'] = 0
						else:
							qt_row['Scope_Reduction_Price'] = float(ct_row['Scope Reduction Price']) *ProRatedFactor
						qt_row['Scope_Addition_Price'] = float(ct_row['Scope Addition Price']) *ProRatedFactor
						if ct_row['Previous_Year_Cost_Price'] == "":
							qt_row['Previous_Year_Cost_Price'] = 0
						else:
							qt_row['Previous_Year_Cost_Price'] = float(ct_row['Previous_Year_Cost_Price']) *ProRatedFactor
						if ct_row['Current_Year_Cost_Price'] == "":
							qt_row['Current_Year_Cost_Price'] = 0
						else:
							qt_row['Current_Year_Cost_Price'] = float(ct_row['Current_Year_Cost_Price']) *ProRatedFactor

						try:
							qt_row['Escalation'] = bgp_child_dict[ct_row['Service_Product']][0]
							qt_row['Total_Discount'] =bgp_child_dict[ct_row['Service_Product']][1]
						except:
							qt_row['Escalation'] = 0
							qt_row['Total_Discount'] = 0
						qt_row['Last_Year_Discount'] = float(ct_row['LY_Discount']) * 100 if ct_row['LY_Discount'] != '' else '0'
						if SC_Pricing_Escalation == "No":
							qt_row['Escalation_Value'] = 0
							qt_row['Final_List_Price'] = qt_row['Honeywell_List_Price'] if qt_row['Honeywell_List_Price'] != "" else 0
						elif SC_Pricing_Escalation == "Yes":
							qt_row['Escalation_Value'] = ((qt_row['Escalation']/100) * (qt_row['Previous_Year_List_Price']- qt_row['Scope_Reduction_Price']))
							qt_row['Final_List_Price'] = (qt_row['Previous_Year_List_Price'] + qt_row['Escalation_Value'] + qt_row['Scope_Reduction_Price'] + qt_row['Scope_Addition_Price'])
						qt_row['Final_Sell_Price'] = float(qt_row['Final_List_Price'] *(1 - (qt_row['Total_Discount']/100)))
						qt_row['Total_Discount_Price'] = (qt_row['Final_List_Price'] * (qt_row['Total_Discount']/100))

						qt_row['Previous_Year_Sell_Price'] = float(ct_row['Py_SellPrice']) *ProRatedFactor if ct_row['Py_SellPrice'] != '' else '0'

						if qt_row['Previous_Year_List_Price'] not in (0,""):
							SR = qt_row['Scope_Reduction_Price'] * (qt_row['Previous_Year_Sell_Price'] / qt_row['Previous_Year_List_Price'])
						if qt_row['Final_List_Price'] not in (0,""):
							SA = (qt_row['Scope_Addition_Price'] * (qt_row['Final_Sell_Price'] / qt_row['Final_List_Price']))

						if ct_row['Service_Product'] in SC_ScopeRemoval:
							qt_row['Scope_Change'] =(-1) * qt_row['Previous_Year_Sell_Price']
						else:
							qt_row['Scope_Change'] =  SR + SA
						qt_row['Price_Impact'] = (qt_row['Final_Sell_Price']- (qt_row['Scope_Change'] + qt_row['Previous_Year_Sell_Price']))
						if qt_row['Final_Sell_Price'] not in (0,""):
							qt_row['Margin'] = (1 - float(float(qt_row['Current_Year_Cost_Price'])/float(qt_row['Final_Sell_Price'])))*100
						if qt_row['Scope_Change'] > 0:
							qt_row['Comments'] = "Scope Addition"
						elif qt_row['Scope_Change'] < 0:
							qt_row['Comments'] = "Scope Reduction"
						elif qt_row['Scope_Change'] == 0:
							qt_row['Comments'] = "No scope change"
				bgp_Renewal_Summary.Save()
		elif SC_Product_Type == "New":
			cont = item.SelectedAttributes.GetContainerByName("SC_BGP_Models_Scope_Cont")
			qtTable = Quote.QuoteTables['BGP_Renewal_Summary']
			qtTable.GetColumnByName('Model_Number').AccessLevel = qtTable.AccessLevel.Hidden
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					qt_row = bgp_Renewal_Summary.AddNewRow()
					qt_row['Service_Product'] = ct_row['Service_Product']
					qt_row['Asset_No_'] = ct_row['Asset No']
					#qt_row['Model_Number'] = ct_row['Model_Number']
					qt_row['Description'] = ct_row['Description']
					qt_row['Previous_Year_Quantity'] = 0
					qt_row['Renewal_Quantity'] = ct_row['Quantity']
					qt_row['Previous_Year_List_Price'] = 0
					qt_row['Honeywell_List_Price'] = float(ct_row['Unit_List_Price']) *ProRatedFactor
					qt_row['Scope_Reduction_Price'] = 0
					qt_row['Scope_Addition_Price'] = float(ct_row['Unit_List_Price']) *ProRatedFactor
					qt_row['Previous_Year_Cost_Price'] = 0
					qt_row['Current_Year_Cost_Price'] = float(ct_row['Unit_Cost_Price']) *ProRatedFactor
					try:
						qt_row['Escalation'] = 0
						qt_row['Total_Discount'] = bgp_child_dict[ct_row['Service_Product']][1]
						qt_row['Last_Year_Discount'] = 0
					except:
						qt_row['Escalation'] = 0
						qt_row['Total_Discount'] = 0
						qt_row['Last_Year_Discount'] = 0
					qt_row['Escalation_Value'] = 0
					qt_row['Final_List_Price'] = float(ct_row['Unit_List_Price']) *ProRatedFactor
					qt_row['Final_Sell_Price'] = (qt_row['Final_List_Price'] *(1 - (qt_row['Total_Discount']/100)))
					qt_row['Total_Discount_Price'] = (qt_row['Final_List_Price'] * (qt_row['Total_Discount']/100))
					qt_row['Previous_Year_Sell_Price'] = 0
					qt_row['Scope_Change'] = float(qt_row['Honeywell_List_Price']) * float(qt_row['Final_Sell_Price']/qt_row['Final_List_Price'])
					qt_row['Price_Impact'] = 0
					qt_row['Margin'] = 1 - (float(qt_row['Current_Year_Cost_Price'])/float(qt_row['Final_Sell_Price']))
					if qt_row['Scope_Change'] > 0:
						qt_row['Comments'] = "Scope Addition"
					elif qt_row['Scope_Change'] < 0:
						qt_row['Comments'] = "Scope Reduction"
					elif qt_row['Scope_Change'] == 0:
						qt_row['Comments'] = "No scope change"
				bgp_Renewal_Summary.Save()
	if v_mod_name == "QCS 4.0":
		QCS_child_dict=v_child_dict
		QCS_Renewal_Summary = Quote.QuoteTables["QCS_4_0"]
		QCS_Renewal_Summary.Rows.Clear()
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		if SC_Product_Type == "Renewal":
			SC_Pricing_Escalation = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Pricing_Escalation'),"None")
			SC_ScopeRemoval = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_ScopeRemoval'), 'False')
			SA = SR = HW_ListPrice = 0
			cont = item.SelectedAttributes.GetContainerByName("SC_QCS_Pricing_Details_Cont_Hidden")
			compCont = item.SelectedAttributes.GetContainerByName('ComparisonSummary')
			scope_removed = []
			if compCont.Rows.Count:
				for cs_row in compCont.Rows:
					if cs_row.IsSelected == True:
						scope_removed.append(cs_row['Service_Product'])
						qt_row = QCS_Renewal_Summary.AddNewRow()
						qt_row['Service_Product'] = cs_row['Service_Product']
						qt_row['Section'] = ""
						qt_row['Previous_Year_Values'] = 1
						qt_row['Description'] = "Scope Removed"
						qt_row['Previous_Year_Unit_Price'] = float(cs_row['PY_List_Price_SFDC']) * ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Previous_Year_List_Price'] = float(cs_row['PY_List_Price_SFDC'])* ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Scope_Reduction_Quantity'] = -1
						qt_row['Scope_Reduction_Price'] = (-1)*float(cs_row['PY_List_Price_SFDC']) * ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Last_Year_Discount_'] = float(cs_row['PY_Discount_SFDC'])*100 if cs_row['PY_Discount_SFDC'] else 0
						qt_row['Previous_Year_Sell_Price'] = float(cs_row['PY_Sell_Price_SFDC'])* ProRatedFactor if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Scope_Change_Price'] = str(round(-float(cs_row['PY_Sell_Price_SFDC'])* ProRatedFactor,2)) if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Comments'] = "Scope Reduction"
						for col in ['Renewal_Year_Values','Honeywell_List_Price_per_Unit','Honeywell_List_Price','Escalation_','Total_Discount_','Scope_Addition_Quantity','Scope_Addition_Price','Escalation_Value','Final_List_Price','Total_Discount_Amount','Final_Sell_Price','Price_Impact']:
							qt_row[col] = 0
				QCS_Renewal_Summary.Save()
			if "QCS 4.0" not in scope_removed:
				if cont.Rows.Count:
					for ct_row in cont.Rows:
						if ct_row['Service Product'] not in scope_removed:
							qt_row = QCS_Renewal_Summary.AddNewRow()
							qt_row['Service_Product'] = ct_row['Service Product']
							qt_row['Description'] = ct_row['Description']
							qt_row['Section'] = ct_row['Section']
							qt_row['Previous_Year_Values'] = ct_row['PY_Quantity'] if ct_row['PY_Quantity'] != "" else 0
							qt_row['Renewal_Year_Values'] = ct_row['Renewal_Quantity'] if ct_row['Renewal_Quantity'] != "" else 0
							qt_row['Previous_Year_Unit_Price'] = float(ct_row['PY_UnitPrice'])*ProRatedFactor if ct_row['PY_UnitPrice'] != "" else 0
							qt_row['Previous_Year_List_Price'] = float(ct_row['PY_ListPrice'])*ProRatedFactor if ct_row['PY_ListPrice'] != "" else 0
							qt_row['Honeywell_List_Price_per_Unit'] = float(ct_row['HW_UnitPrice'])*ProRatedFactor if ct_row['HW_UnitPrice'] != "" else 0
							qt_row['Honeywell_List_Price'] = float(qt_row['Honeywell_List_Price_per_Unit'] * qt_row['Renewal_Year_Values'])
							qt_row['Comments'] = ct_row['Comments']
							HW_ListPrice = float(ct_row['HW_ListPrice'])
							try:
								qt_row['Escalation_'] = QCS_child_dict[ct_row['Service Product']][0]
								qt_row['Total_Discount_'] =QCS_child_dict[ct_row['Service Product']][1]
							except:
								qt_row['Escalation_'] = 0
								qt_row['Total_Discount_'] = 0
							qt_row['Last_Year_Discount_'] = float(ct_row['LY_Discount']) * 100 if ct_row['LY_Discount'] != '' else '0'
							qt_row['Scope_Reduction_Quantity']= ct_row['SR_Quantity'] if ct_row['SR_Quantity'] != "" else 0
							qt_row['Scope_Reduction_Price'] = (qt_row['Scope_Reduction_Quantity'] * qt_row['Previous_Year_Unit_Price'])
							qt_row['Scope_Addition_Quantity'] = ct_row['SA_Quantity'] if ct_row['SA_Quantity'] != "" else 0
							qt_row['Scope_Addition_Price'] = (qt_row['Scope_Addition_Quantity'] * qt_row['Honeywell_List_Price_per_Unit'])
							if SC_Pricing_Escalation == "No":
								qt_row['Escalation_Value'] = 0
							else:
								if qt_row['Previous_Year_Values'] < qt_row['Renewal_Year_Values']:
									qt_row['Escalation_Value']= str(float(qt_row['Escalation_']/100)* float(qt_row['Previous_Year_Unit_Price']) * float(qt_row['Previous_Year_Values']))
								else:
									qt_row['Escalation_Value']= str(float(qt_row['Escalation_']/100)* float(qt_row['Previous_Year_Unit_Price']) * float(qt_row['Renewal_Year_Values']))
							if SC_Pricing_Escalation == "No":
								qt_row['Final_List_Price'] = HW_ListPrice
							else:
								qt_row['Final_List_Price'] = (qt_row['Previous_Year_List_Price'] + qt_row['Escalation_Value'] + qt_row['Scope_Reduction_Price'] +qt_row['Scope_Addition_Price'])
							qt_row['Total_Discount_Amount'] = qt_row['Final_List_Price'] * (qt_row['Total_Discount_']/100)
							qt_row['Previous_Year_Sell_Price'] = float(ct_row['PY_SellPrice'])*ProRatedFactor if ct_row['PY_SellPrice'] != "" else 0
							qt_row['Final_Sell_Price'] = (qt_row['Final_List_Price'] - qt_row['Total_Discount_Amount'])
							if qt_row['Previous_Year_List_Price'] != 0:
								SR = (qt_row['Scope_Reduction_Price'] * (qt_row['Previous_Year_Sell_Price'] / (qt_row['Previous_Year_List_Price'])))
							if qt_row['Final_List_Price'] != 0:
								SA = (qt_row['Scope_Addition_Price'] * (qt_row['Final_Sell_Price'] / qt_row['Final_List_Price']))
							if str(ct_row['Service Product'] +'|') in SC_ScopeRemoval:
								qt_row['Scope_Change_Price'] =(-1) * qt_row['Previous_Year_Sell_Price']
							else:
								qt_row['Scope_Change_Price'] =	SR + SA
							qt_row['Price_Impact'] = (qt_row['Final_Sell_Price'] - (qt_row['Scope_Change_Price'] + qt_row['Previous_Year_Sell_Price']))
					QCS_Renewal_Summary.Save()
		elif SC_Product_Type == "New":
			cont = item.SelectedAttributes.GetContainerByName("SC_QCS_Pricing_Details_Cont_Hidden")
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					qt_row = QCS_Renewal_Summary.AddNewRow()
					qt_row['Service_Product'] = ct_row['Service Product']
					qt_row['Description'] = ct_row['Description']
					qt_row['Section'] = ct_row['Section']
					qt_row['Previous_Year_Values'] = 0
					qt_row['Renewal_Year_Values'] = ct_row['Renewal_Quantity'] if ct_row['Renewal_Quantity'] else '0'
					qt_row['Previous_Year_Unit_Price'] = 0
					qt_row['Previous_Year_List_Price'] = 0
					qt_row['Honeywell_List_Price_per_Unit'] = float(ct_row['List Price'])*ProRatedFactor
					qt_row['Honeywell_List_Price'] = float(ct_row['List Price'])*ProRatedFactor
					qt_row['Comments'] = 'Scope Addition'
					try:
						qt_row['Escalation_'] = 0
						qt_row['Total_Discount_'] =QCS_child_dict[ct_row['Product_Name']][1]
						qt_row['Last_Year_Discount_'] = 0
					except:
						qt_row['Escalation_'] = 0
						qt_row['Total_Discount_'] = 0
						qt_row['Last_Year_Discount_'] = 0
					qt_row['Scope_Reduction_Quantity'] = 0
					qt_row['Scope_Reduction_Price'] = 0
					qt_row['Escalation_Value'] = 0
					if qt_row['Previous_Year_Values'] < qt_row['Renewal_Year_Values']:
						qt_row['Scope_Addition_Quantity'] = (qt_row['Renewal_Year_Values'] - qt_row['Previous_Year_Values'])
					else:
						qt_row['Scope_Addition_Quantity'] = 0
					qt_row['Scope_Addition_Price'] = (qt_row['Scope_Addition_Quantity'] * qt_row['Honeywell_List_Price_per_Unit'])
					qt_row['Final_List_Price'] = (qt_row['Previous_Year_List_Price'] + qt_row['Escalation_Value'] + qt_row['Scope_Reduction_Price'] +qt_row['Scope_Addition_Price'])
					qt_row['Total_Discount_Amount'] = (qt_row['Final_List_Price'] * (qt_row['Total_Discount_']/100))
					qt_row['Previous_Year_Sell_Price'] = 0
					qt_row['Final_Sell_Price'] = (qt_row['Final_List_Price'] - qt_row['Total_Discount_Amount'])
					qt_row['Scope_Change_Price'] = qt_row['Final_Sell_Price']
					qt_row['Price_Impact'] = 0
				QCS_Renewal_Summary.Save()