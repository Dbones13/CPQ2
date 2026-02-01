#Third Party, Cyber, WEP and Local Support Standby
def fn_load_QuoteTable_Grp5(Quote,v_mod_name,item,v_child_dict,ProRatedFactor):
	if v_mod_name == "Third Party Services":
		tps_child_dict=v_child_dict
		tps_renewal_summary = Quote.QuoteTables["SC_ThirdParty_Renewal_Summary"]
		tps_renewal_summary.Rows.Clear()
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		if SC_Product_Type == "Renewal":
			SC_Pricing_Escalation_TP = next(val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Pricing_Escalation')
			SC_ScopeRemoval = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_ScopeRemoval'), 'False')
			cont = item.SelectedAttributes.GetContainerByName("SC_TPS_RC_Entitlements_Scope_summary_hidden")
			compCont = item.SelectedAttributes.GetContainerByName('ComparisonSummary')
			if compCont.Rows.Count:
				for cs_row in compCont.Rows:
					if cs_row.IsSelected == True: 
						qt_row = tps_renewal_summary.AddNewRow()
						qt_row['Entitlement'] = cs_row['Service_Product']
						qt_row['Third_Party_Models'] = ""
						qt_row['Descrption'] = "Scope  Removed"
						qt_row['Previous_Year_Quantity'] = 1
						qt_row['Previous_Year_List_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Comments'] = "Scope Reduction"
						qt_row['Last_Year_Discount'] = float(cs_row['PY_Discount_SFDC'])*100 if cs_row['PY_Discount_SFDC'] else 0
						qt_row['Scope_Reduction_Price'] = (-1)*float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Previous_Year_Sell_Price'] = float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Scope_Change_Price'] = str(round(-float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor,2)) if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['PY_CostPrice'] = str(round((1-float(cs_row['Booked_Margin'])/100) *float(cs_row["PY_Sell_Price_SFDC"])*ProRatedFactor,2)) if cs_row["PY_Sell_Price_SFDC"] and cs_row['Booked_Margin'] else "0"
						for col in ['Quantity','Honeywell_List_Price','Escalation','Total_Discount','Scope_Addition_Price','Escalation_Value','Final_List_Price','Total_Discount_Price','Final_Sell_Price','Price_Impact','CY_CostPrice','Margin']:
							qt_row[col] = 0
				tps_renewal_summary.Save()
			if SC_ScopeRemoval == "False":
				if cont.Rows.Count:
					for ct_row in cont.Rows:
						qt_row = tps_renewal_summary.AddNewRow()
						qt_row['Entitlement'] = ct_row['Entitlement']
						qt_row['Third_Party_Models'] = ct_row['3rd_Party_Models']
						qt_row['Descrption'] = ct_row['Description']
						qt_row['Previous_Year_Quantity'] = ct_row['PY_Quantity'] if ct_row['PY_Quantity'] != "" else '0'
						qt_row['Quantity'] = ct_row['Quantity'] if ct_row['Quantity'] != "" else '0'
						qt_row['Previous_Year_List_Price'] = float(ct_row['PY_ListPrice'])*ProRatedFactor if ct_row['PY_ListPrice'] != "" else '0'
						qt_row['Honeywell_List_Price'] = float(ct_row['HW_ListPrice'])*ProRatedFactor if ct_row['HW_ListPrice'] != "" else '0'
						qt_row['Comments'] = ct_row['Comments']
						try:
							if ct_row['Entitlement'] in tps_child_dict.keys():
								qt_row['Escalation'] = tps_child_dict[ct_row['Entitlement']][0]
								qt_row['Total_Discount'] = tps_child_dict[ct_row['Entitlement']][1]
						except:
							qt_row['Escalation'] = 0
							qt_row['Total_Discount'] = 0
						qt_row['Last_Year_Discount'] = ct_row['PY_Discount']
						qt_row['Scope_Reduction_Price'] = float(ct_row['SR_Price'])*ProRatedFactor if ct_row['SR_Price'] != "" else '0'
						qt_row['Scope_Addition_Price'] = float(ct_row['SA_Price'])*ProRatedFactor if ct_row['SA_Price'] != "" else '0'
						if SC_Pricing_Escalation_TP == "No":
							qt_row['Escalation_Value'] = 0
							qt_row['Final_List_Price'] = float(ct_row['HW_ListPrice'])*ProRatedFactor if ct_row['HW_ListPrice'] != "" else '0'
						elif SC_Pricing_Escalation_TP == "Yes":
							qt_row['Escalation_Value'] = qt_row['Escalation'] / 100 * (qt_row['Previous_Year_List_Price'] + qt_row['Scope_Reduction_Price'])
							qt_row['Final_List_Price'] = qt_row['Previous_Year_List_Price'] + qt_row['Scope_Addition_Price'] + qt_row['Scope_Reduction_Price'] + qt_row['Escalation_Value']
						qt_row['Total_Discount_Price'] = qt_row['Final_List_Price'] * (qt_row['Total_Discount']/100)
						qt_row['Previous_Year_Sell_Price'] = float(ct_row['PY_SellPrice'])*ProRatedFactor if ct_row['PY_SellPrice'] != "" else 0
						qt_row['Final_Sell_Price'] = qt_row['Final_List_Price'] - qt_row['Total_Discount_Price']
						if qt_row['Final_List_Price'] not in ('','0',0) and qt_row['Previous_Year_List_Price'] not in ('','0',0):
							qt_row['Scope_Change_Price'] = qt_row['Scope_Addition_Price'] * (qt_row['Final_Sell_Price'] / qt_row['Final_List_Price']) + qt_row['Scope_Reduction_Price'] * (qt_row['Previous_Year_Sell_Price'] / qt_row['Previous_Year_List_Price'])
						elif qt_row['Final_List_Price'] in ('','0',0) and qt_row['Previous_Year_List_Price'] not in ('','0',0):
							qt_row['Scope_Change_Price'] = qt_row['Scope_Reduction_Price'] * (qt_row['Previous_Year_Sell_Price'] / qt_row['Previous_Year_List_Price'])
						elif qt_row['Final_List_Price'] not in ('','0',0) and qt_row['Previous_Year_List_Price'] in ('','0',0):
							qt_row['Scope_Change_Price'] = qt_row['Scope_Addition_Price'] * (qt_row['Final_Sell_Price'] / qt_row['Final_List_Price'])
						qt_row['Price_Impact'] = qt_row['Final_Sell_Price'] - (qt_row['Previous_Year_Sell_Price'] + qt_row['Scope_Change_Price'])
						qt_row['CY_CostPrice'] = float(ct_row['COST'])*ProRatedFactor if ct_row['COST'] != "" else '0'
						qt_row['PY_CostPrice'] = float(ct_row['PY_COST'])*ProRatedFactor if ct_row['PY_COST'] != "" else '0'
						if qt_row['Final_Sell_Price'] not in ('','0',0):
							qt_row['Margin'] = (1- (qt_row['CY_CostPrice'] / qt_row['Final_Sell_Price'])) * 100
						else:
							qt_row['Margin'] = 100
					tps_renewal_summary.Save()
		elif SC_Product_Type == "New":
			cont = item.SelectedAttributes.GetContainerByName("SC_TPS_RC_Entitlements_Scope_summary_hidden")
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					qt_row = tps_renewal_summary.AddNewRow()
					for col in ['Previous_Year_Quantity','Previous_Year_List_Price','Escalation','Last_Year_Discount','Escalation_Value','Previous_Year_Sell_Price','Price_Impact']:
						qt_row[col] = 0
					qt_row['Entitlement'] = ct_row['Entitlement']
					qt_row['Third_Party_Models'] = ct_row['3rd_Party_Models']
					qt_row['Descrption'] = ct_row['Description']
					qt_row['Quantity'] = ct_row['Quantity'] if ct_row['Quantity'] != "" else 0
					qt_row['Honeywell_List_Price'] = float(ct_row['HW_ListPrice'])*ProRatedFactor if ct_row['HW_ListPrice'] != "" else 0
					qt_row['Scope_Addition_Price'] = qt_row['Honeywell_List_Price'] if qt_row['Honeywell_List_Price'] else '0'
					if qt_row['Honeywell_List_Price'] == "":
						qt_row['Comments'] = 'No Scope Change'
					elif qt_row['Honeywell_List_Price'] > 0:
						qt_row['Comments'] = 'Scope Addition'
					elif qt_row['Honeywell_List_Price'] < 0:
						qt_row['Comments'] = 'Scope Reduction'
					try:
						qt_row['Total_Discount'] = tps_child_dict[ct_row['Entitlement']][1]
					except:
						qt_row['Total_Discount'] = 0
					qt_row['Final_List_Price'] = qt_row['Honeywell_List_Price'] if qt_row['Honeywell_List_Price'] else '0'
					qt_row['Total_Discount_Price'] = qt_row['Final_List_Price'] * (qt_row['Total_Discount']/100)
					qt_row['Final_Sell_Price'] = qt_row['Final_List_Price'] - qt_row['Total_Discount_Price']
					qt_row['CY_CostPrice'] = float(ct_row['COST'])*ProRatedFactor if ct_row['COST'] else '0'
					qt_row['Scope_Change_Price'] = qt_row['Final_Sell_Price']  if qt_row['Final_Sell_Price']  else '0'
					qt_row['Margin'] = (1- (qt_row['CY_CostPrice'] / qt_row['Final_Sell_Price'])) * 100
				tps_renewal_summary.Save()
	if v_mod_name == "Cyber":
		cyber_child_dict=v_child_dict
		cyber_renewal_summary = Quote.QuoteTables["Cyber_Renewal_Summary"]
		cyber_renewal_summary.Rows.Clear()
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		if SC_Product_Type == "Renewal":
			SC_Pricing_Escalation = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Pricing_Escalation'), '')
			cont = item.SelectedAttributes.GetContainerByName("SC_Cyber_Models_Cont_Hidden")
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
						qt_row['Descrption'] = "Scope Removed"
						qt_row['Previous_Year_Quantity'] = 1
						qt_row['Previous_Year_List_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] != '' else 0
						qt_row['Scope_Reduction_Quantity'] = -1
						qt_row['Scope_Reduction_Price'] = (-1)*float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] != '' else 0
						qt_row['Last_Year_Discount'] = float(cs_row['PY_Discount_SFDC'])*100 if cs_row['PY_Discount_SFDC'] != '' else 0
						qt_row['Previous_Year_Sell_Price'] = float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor if cs_row['PY_Sell_Price_SFDC'] != '' else 0
						qt_row['Previous_Year_Cost_Price'] = round((1-float(cs_row['Booked_Margin'])/100) *float(cs_row["PY_Sell_Price_SFDC"])*ProRatedFactor,2) if cs_row["PY_Sell_Price_SFDC"] and cs_row['Booked_Margin'] else 0
						qt_row['Scope_Change'] = str(round(-float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor,2)) if cs_row['PY_Sell_Price_SFDC'] != '' else 0
						qt_row['Comments'] = "Scope Reduction"
						for col in ['Quantity','Honeywell_List_Price_per_Unit','Honeywell_List_Price','Scope_Addition_Quantity','Scope_Addition_Price','Escalation','Total_Discount','Escalation_Value','Final_List_Price','Total_Discount_Price','Final_Sell_Price','Price_Impact','Current_Year_Cost_Price','Margin']:
							qt_row[col] = 0
				cyber_renewal_summary.Save()
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					if ct_row['Service_Product'] not in scope_removed:
						qt_row = cyber_renewal_summary.AddNewRow()
						qt_row['Service_Product'] = ct_row['Service_Product']
						qt_row['Asset_No'] = ct_row['Asset']
						qt_row['Model_Number'] = ct_row['Model']
						qt_row['Descrption'] = ct_row['Description']
						qt_row['Previous_Year_Quantity'] = ct_row['PY_Quantity'] if ct_row['PY_Quantity'] != '' else 0
						qt_row['Quantity'] = ct_row['Renewal_Quantity'] if ct_row['Renewal_Quantity'] != '' else 0
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
								qt_row['Escalation_Value'] = ((qt_row['Escalation']/100) * (qt_row['Previous_Year_List_Price']/qt_row['Previous_Year_Quantity']) * qt_row['Quantity']) if qt_row['Previous_Year_Quantity'] not in (0,'','0') else 0
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
			cont = item.SelectedAttributes.GetContainerByName("SC_Cyber_Models_Cont_Hidden")
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					qt_row = cyber_renewal_summary.AddNewRow()
					for col in ['Previous_Year_Quantity','Previous_Year_List_Price','Scope_Reduction_Quantity','Scope_Reduction_Price','Escalation','Last_Year_Discount','Escalation_Value','Previous_Year_Sell_Price','Price_Impact','Previous_Year_Cost_Price']:
						qt_row[col] = 0
					qt_row['Service_Product'] = ct_row['Service_Product']
					qt_row['Asset_No'] = ct_row['Asset']
					qt_row['Model_Number'] = ct_row['Model']
					qt_row['Descrption'] = ct_row['Description']
					qt_row['Quantity'] = ct_row['Renewal_Quantity'] if ct_row['Renewal_Quantity'] != '' else 0
					qt_row['Honeywell_List_Price_per_Unit'] = float(ct_row['List_Price'])*ProRatedFactor if ct_row['List_Price'] != '' else 0
					qt_row['Honeywell_List_Price'] = float(ct_row['CY_ListPrice'])*ProRatedFactor if ct_row['CY_ListPrice'] != '' else 0
					try:
						if ct_row['Service_Product'] in cyber_child_dict.keys():
							qt_row['Total_Discount'] = cyber_child_dict[ct_row['Service_Product']][1]
					except:
						qt_row['Total_Discount'] = 0
					qt_row['Scope_Addition_Quantity'] = ct_row['Renewal_Quantity'] if ct_row['Renewal_Quantity'] != '' else 0
					qt_row['Scope_Addition_Price'] = qt_row['Scope_Addition_Quantity'] * qt_row['Honeywell_List_Price_per_Unit']
					qt_row['Final_List_Price'] = (qt_row['Previous_Year_List_Price']+qt_row['Escalation_Value']+qt_row['Scope_Reduction_Price']+qt_row['Scope_Addition_Price'])
					qt_row['Total_Discount_Price'] = (qt_row['Total_Discount']/100) * qt_row['Final_List_Price']
					qt_row['Final_Sell_Price'] = qt_row['Final_List_Price'] * (1 - qt_row['Total_Discount']/100)
					qt_row['Scope_Change'] = qt_row['Final_Sell_Price']
					qt_row['Current_Year_Cost_Price'] = float(ct_row['Cost_Price'])*ProRatedFactor if ct_row['Cost_Price'] != '' else 0
					qt_row['Margin'] = round(1-(float(qt_row['Current_Year_Cost_Price']) / float(qt_row["Final_Sell_Price"])),2) if qt_row["Final_Sell_Price"] not in (0,'','0') else 0
					qt_row['Comments'] = 'Scope Addition'
				cyber_renewal_summary.Save()
	if v_mod_name == "Workforce Excellence Program":
		wep_child_dict=v_child_dict
		WEP_Renewal_Summary = Quote.QuoteTables["Workforce_Excellence_Program"]
		WEP_Renewal_Summary.Rows.Clear()
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		if SC_Product_Type == "Renewal":
			cont = item.SelectedAttributes.GetContainerByName("SC_WEP_Offering_ServiceProduct_Hidden")
			compCont = item.SelectedAttributes.GetContainerByName("ComparisonSummary")
			scope_removed = []
			if compCont.Rows.Count:
				for cs_row in compCont.Rows:
					if cs_row.IsSelected == True:
						scope_removed.append(cs_row['Service_Product'])
						qt_row = WEP_Renewal_Summary.AddNewRow()
						qt_row['Offering'] = cs_row['Service_Product']
						qt_row['Model'] = ""
						qt_row['Description'] = "Scope Removed"
						qt_row['Previous_Year_Quantity'] = 1
						qt_row['Previous_Year_Unit_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Previous_Year_List_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Scope_Reduction_Quantity'] = -1
						qt_row['Scope_Reduction_Price'] = (-1)*float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Last_Year_Discount'] = float(cs_row['PY_Discount_SFDC'])*100 if cs_row['PY_Discount_SFDC'] else 0
						qt_row['Previous_Year_Sell_Price'] = float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Scope_Change_Price'] = str(round(-float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor,2)) if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Previous_Year_Cost_Price'] = str(round((1-float(cs_row['Booked_Margin'])/100) *float(cs_row["PY_Sell_Price_SFDC"])*ProRatedFactor,2)) if cs_row["PY_Sell_Price_SFDC"] and cs_row['Booked_Margin'] else "0"
						qt_row['Comments'] = "Scope Reduction"
						for col in ['Renewal_Quantity','Honeywell_List_Price_per_Unit','Honeywell_List_Price','Scope_Addition_Quantity','Scope_Addition_Price','Escalation','Total_Discount','Escalation_Value','Final_List_Price','Total_Discount_Amount','Final_Sell_Price','Price_Impact','Final_Cost_Price','Margin']:
							qt_row[col] = 0
				WEP_Renewal_Summary.Save()
			if cont.Rows.Count:
				escalationDict = {
					'Honeywell Integrated Field App' : 'SC_WEP_HIF_Pricing_Escalation',
					'Immersive Field Simulator' : 'SC_WEP_IFS_Pricing_Escalation',
					'HALO OA' : 'SC_WEP_Halo_Pricing_Escalation',
					'Training' : 'SC_WEP_Training_Pricing_Escalation',
					'Training Needs Assessment' : 'SC_WEP_TNA_Pricing_Escalation',
					'Operations and Maintenance' : 'SC_WEP_OM_Pricing_Escalation',
					'Outcome Competency Program' : 'SC_WEP_OCP_Pricing_Escalation'
				}
				for ct_row in cont.Rows:
					if ct_row['Service_Product'] not in scope_removed:
						qt_row = WEP_Renewal_Summary.AddNewRow()
						qt_row['Offering'] = ct_row['Offering_Name']
						qt_row['Model'] = ct_row['Model']
						qt_row['Description'] = ct_row['Description']
						qt_row['Previous_Year_Quantity'] = ct_row['PY_Quantity']
						qt_row['Renewal_Quantity'] = ct_row['CY_Quantity']
						qt_row['Previous_Year_Unit_Price'] = float(ct_row['PY_UnitPrice'])*ProRatedFactor if ct_row['PY_UnitPrice'] != "" else 0
						qt_row['Previous_Year_List_Price'] = float(ct_row['PY_ListPrice'])*ProRatedFactor if ct_row['PY_ListPrice'] != "" else 0
						qt_row['Honeywell_List_Price_per_Unit'] = float(ct_row['CY_UnitPrice'])*ProRatedFactor if ct_row['CY_UnitPrice'] != "" else 0
						qt_row['Honeywell_List_Price'] = float(ct_row['CY_ListPrice'])*ProRatedFactor if ct_row['CY_ListPrice'] != "" else 0
						qt_row['Scope_Reduction_Quantity'] = ct_row['SR_Quantity'] if ct_row['SR_Quantity'] != "" else 0
						qt_row['Scope_Reduction_Price'] = float(ct_row['SR_Price'])*ProRatedFactor if ct_row['SR_Price'] != "" else 0
						qt_row['Scope_Addition_Quantity'] = ct_row['SA_Quantity'] if ct_row['SA_Quantity'] != "" else 0
						qt_row['Scope_Addition_Price'] = float(ct_row['SA_Price'])*ProRatedFactor if ct_row['SA_Price'] != "" else 0
						try:
							qt_row['Escalation'] = wep_child_dict[ct_row['Offering_Name']][0]
							qt_row['Total_Discount'] =wep_child_dict[ct_row['Offering_Name']][1]
						except:
							qt_row['Escalation'] = 0
							qt_row['Total_Discount'] = 0
						qt_row['Last_Year_Discount'] = ct_row['PY_Discount'] if ct_row['PY_Discount'] != "" else 0
						SC_Pricing_Escalation_WEP = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == escalationDict[ct_row['Offering_Name']]),'No')
						if SC_Pricing_Escalation_WEP == "No":
							qt_row['Escalation_Value'] = 0
							qt_row['Final_List_Price'] = float(ct_row['CY_ListPrice'])*ProRatedFactor if ct_row['CY_ListPrice'] else 0
						elif SC_Pricing_Escalation_WEP == "Yes":
							qt_row['Escalation_Value'] = float(ct_row['Escalation_Price'])*ProRatedFactor * float(qt_row['Escalation']/100)
							qt_row['Final_List_Price'] = qt_row['Previous_Year_List_Price'] + qt_row['Escalation_Value'] + qt_row['Scope_Reduction_Price'] +qt_row['Scope_Addition_Price']
						qt_row['Total_Discount_Amount'] = qt_row['Final_List_Price'] * (qt_row['Total_Discount']/100)
						qt_row['Previous_Year_Sell_Price'] = qt_row['Previous_Year_List_Price'] * (1-(qt_row['Last_Year_Discount']/100))
						qt_row['Final_Sell_Price'] = qt_row['Final_List_Price'] - qt_row['Total_Discount_Amount']
						scope_reduce_var = 0
						scope_add_var = 0
						if qt_row['Previous_Year_List_Price'] not in (0,'0','',0.00,'0.00','0.0',0.0):
							scope_reduce_var = (qt_row['Scope_Reduction_Price'] * (qt_row['Previous_Year_Sell_Price'] / (qt_row['Previous_Year_List_Price'])))
						if qt_row['Final_List_Price'] not in (0,'0','',0.00,'0.00','0.0',0.0):
							scope_add_var = (qt_row['Scope_Addition_Price'] * (qt_row['Final_Sell_Price'] / (qt_row['Final_List_Price'])))
						qt_row['Scope_Change_Price'] = scope_reduce_var + scope_add_var
						qt_row['Price_Impact'] = (qt_row['Final_Sell_Price'] - (qt_row['Scope_Change_Price'] + qt_row['Previous_Year_Sell_Price']))
						qt_row['Previous_Year_Cost_Price'] = float(ct_row['PY_CostPrice'])*ProRatedFactor if ct_row['PY_CostPrice'] != "" else 0
						qt_row['Final_Cost_Price'] = float(ct_row['CY_CostPrice'])*ProRatedFactor if ct_row['CY_CostPrice'] != "" else 0
						if qt_row['Final_Sell_Price'] != 0:
							qt_row['Margin'] = (1-(qt_row['Final_Cost_Price']/qt_row['Final_Sell_Price']))*100
						qt_row['Comments'] = ct_row['Comments']
				WEP_Renewal_Summary.Save()
		elif SC_Product_Type == "New":
			cont = item.SelectedAttributes.GetContainerByName("SC_WEP_Offering_ServiceProduct_Hidden")
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					qt_row = WEP_Renewal_Summary.AddNewRow()
					for col in ['Previous_Year_Quantity','Previous_Year_Unit_Price','Previous_Year_List_Price','Scope_Reduction_Quantity','Scope_Reduction_Price','Escalation','Last_Year_Discount','Escalation_Value','Previous_Year_Sell_Price','Previous_Year_Cost_Price','Price_Impact']:
						qt_row[col] = 0
					qt_row['Offering'] = ct_row['Offering_Name']
					qt_row['Model'] = ct_row['Model']
					qt_row['Description'] = ct_row['Description']
					qt_row['Renewal_Quantity'] = ct_row['CY_Quantity'] if ct_row['CY_Quantity'] != "" else 0
					qt_row['Honeywell_List_Price_per_Unit'] = float(ct_row['CY_UnitPrice'])*ProRatedFactor if ct_row['CY_UnitPrice'] != "" else 0
					qt_row['Honeywell_List_Price'] = float(ct_row['CY_ListPrice'])*ProRatedFactor if ct_row['CY_ListPrice'] != "" else 0
					qt_row['Scope_Addition_Quantity'] = ct_row['SA_Quantity'] if ct_row['SA_Quantity'] != "" else 0
					qt_row['Scope_Addition_Price'] = float(ct_row['SA_Price'])*ProRatedFactor if ct_row['SA_Price'] != "" else 0
					try:
						qt_row['Total_Discount'] =wep_child_dict[ct_row['Offering_Name']][1]
					except:
						qt_row['Total_Discount'] = 0
					qt_row['Final_List_Price'] = qt_row['Previous_Year_List_Price'] + qt_row['Escalation_Value'] + qt_row['Scope_Reduction_Price'] +qt_row['Scope_Addition_Price']
					qt_row['Total_Discount_Amount'] = qt_row['Final_List_Price'] * (qt_row['Total_Discount']/100)
					qt_row['Final_Sell_Price'] = qt_row['Final_List_Price'] - qt_row['Total_Discount_Amount']
					qt_row['Scope_Change_Price'] = qt_row['Final_Sell_Price']
					qt_row['Final_Cost_Price'] = float(ct_row['CY_CostPrice'])*ProRatedFactor if ct_row['CY_CostPrice'] != "" else 0
					if qt_row['Final_Sell_Price'] != 0:
						qt_row['Margin'] = (1-(qt_row['Final_Cost_Price']/qt_row['Final_Sell_Price']))*100
					qt_row['Comments'] = "Scope Addition"
				WEP_Renewal_Summary.Save()
	if v_mod_name == "Local Support Standby":
		lss_child_dict = v_child_dict
		lss_renewal_summary = Quote.QuoteTables["SC_LocalStandbySupport_Renewal_Summary"]
		lss_renewal_summary.Rows.Clear()
		SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), '')
		if SC_Product_Type == "Renewal":
			scopeRemoved = False
			SC_Pricing_Escalation_LSS = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Pricing_Escalation'), '')
			cont = item.SelectedAttributes.GetContainerByName("SC_LSS_Models_Summary_Cont_Hidden")
			compCont = item.SelectedAttributes.GetContainerByName("ComparisonSummary")
			compDict = {}
			if compCont.Rows.Count:
				for cs_row in compCont.Rows:
					compDict[cs_row["Service_Product"]] = float(cs_row["PY_Discount_SFDC"]) if cs_row["PY_Discount_SFDC"] else '0'
					if cs_row.IsSelected == True:
						scopeRemoved = True
						qt_row = lss_renewal_summary.AddNewRow()
						qt_row['Model'] = cs_row['Service_Product']
						qt_row['Description'] = "Scope Removed"
						qt_row['Previous_Year_Quantity'] = 1
						qt_row['Previous_Year_Unit_List_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Previous_Year_List_Price'] = float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Previous_Year_Unit_Cost_Price'] = str(round((1-float(cs_row['Booked_Margin'])/100) *float(cs_row["PY_Sell_Price_SFDC"])*ProRatedFactor,2)) if cs_row["PY_Sell_Price_SFDC"] and cs_row['Booked_Margin'] else "0"
						qt_row['Previous_Year_Cost_Price'] = str(round((1-float(cs_row['Booked_Margin'])/100) *float(cs_row["PY_Sell_Price_SFDC"])*ProRatedFactor,2)) if cs_row["PY_Sell_Price_SFDC"] and cs_row['Booked_Margin'] else "0"
						qt_row['Scope_Reduction_Quantity'] = -1
						qt_row['Scope_Reduction_Price'] = (-1)*float(cs_row['PY_List_Price_SFDC'])*ProRatedFactor if cs_row['PY_List_Price_SFDC'] else 0
						qt_row['Last_Year_Discount'] = float(cs_row['PY_Discount_SFDC'])*100 if cs_row['PY_Discount_SFDC'] else 0
						qt_row['Previous_Year_Sell_Price'] = float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Scope_Change'] = str(round(-float(cs_row['PY_Sell_Price_SFDC'])*ProRatedFactor,2)) if cs_row['PY_Sell_Price_SFDC'] else 0
						qt_row['Comments'] = "Scope Reduction"
						for col in ['Renewal_Quantity','Honeywell_List_Price_Per_Unit','Honeywell_List_Price','Current_Year_Unit_Cost_Price','Current_Year_Cost_Price','Escalation','Escalation_Value','Scope_Addition_Quantity','Scope_Addition_Price','Final_List_Price','Total_Discount','Total_Discount_Price','Final_Sell_Price','Price_Impact','Margin']:
							qt_row[col] = 0
				lss_renewal_summary.Save()
			if scopeRemoved == False:
				if cont.Rows.Count:
					for ct_row in cont.Rows:
						qt_row = lss_renewal_summary.AddNewRow()
						qt_row['Model'] = ct_row['Model']
						qt_row['Description'] = ct_row['Description']
						qt_row['Previous_Year_Quantity'] = ct_row['PY_Quantity'] if ct_row['PY_Quantity'] != "" else 0
						qt_row['Renewal_Quantity'] = ct_row['CY_Quantity'] if ct_row['CY_Quantity'] != "" else 0
						qt_row['Previous_Year_Unit_List_Price'] = float(ct_row['PY_UnitPrice'])*ProRatedFactor if ct_row['PY_UnitPrice'] != "" else 0
						qt_row['Previous_Year_List_Price'] = float(ct_row['PY_ListPrice'])*ProRatedFactor if ct_row['PY_ListPrice'] != "" else 0
						qt_row['Previous_Year_Unit_Cost_Price'] = float(ct_row['PY_UnitCost'])*ProRatedFactor if ct_row['PY_UnitCost'] != "" else 0
						qt_row['Previous_Year_Cost_Price'] = float(ct_row['PY_CostPrice'])*ProRatedFactor if ct_row['PY_CostPrice'] != "" else 0
						qt_row['Honeywell_List_Price_Per_Unit'] = float(ct_row['CY_UnitPrice'])*ProRatedFactor if ct_row['CY_UnitPrice'] != "" else 0
						qt_row['Honeywell_List_Price'] = float(ct_row['CY_ListPrice'])*ProRatedFactor if ct_row['CY_ListPrice'] != "" else 0
						qt_row['Current_Year_Unit_Cost_Price'] = float(ct_row['CY_UnitCost'])*ProRatedFactor if ct_row['CY_UnitCost'] != "" else 0
						qt_row['Current_Year_Cost_Price'] = float(ct_row['CY_CostPrice'])*ProRatedFactor if ct_row['CY_CostPrice'] != "" else 0
						qt_row['Scope_Reduction_Quantity'] = ct_row['SR_Quantity'] if ct_row['SR_Quantity'] != "" else 0
						qt_row['Scope_Reduction_Price'] = float(qt_row['Scope_Reduction_Quantity'])*float(qt_row['Previous_Year_Unit_List_Price'])
						qt_row['Scope_Addition_Quantity'] = ct_row['SA_Quantity'] if ct_row['SA_Quantity'] != "" else 0
						qt_row['Scope_Addition_Price'] = float(qt_row['Scope_Addition_Quantity'])*float(qt_row['Honeywell_List_Price_Per_Unit'])
						qt_row['Last_Year_Discount'] = compDict.get("Local Support Standby",0)
						try:
							qt_row['Escalation'] = lss_child_dict["Local Support Standby"][0]
							qt_row['Total_Discount'] = lss_child_dict["Local Support Standby"][1]
						except:
							qt_row['Escalation'] = 0
							qt_row['Total_Discount'] = 0
						if SC_Pricing_Escalation_LSS == "No":
							qt_row['Escalation_Value'] = 0
							qt_row['Final_List_Price'] = qt_row['Honeywell_List_Price'] if qt_row['Honeywell_List_Price'] !='' else '0'
						elif SC_Pricing_Escalation_LSS == "Yes":
							if qt_row['Renewal_Quantity'] > qt_row['Previous_Year_Quantity']:
								qt_row['Escalation_Value'] = (qt_row['Escalation']) / 100 * qt_row['Previous_Year_Quantity'] * qt_row['Previous_Year_Unit_List_Price']
							else:
								qt_row['Escalation_Value'] = (qt_row['Escalation']) / 100 * qt_row['Renewal_Quantity'] * qt_row['Previous_Year_Unit_List_Price']
							qt_row['Final_List_Price'] = qt_row['Previous_Year_List_Price'] + qt_row['Scope_Reduction_Price'] + qt_row['Escalation_Value'] + qt_row['Scope_Addition_Price']
						qt_row['Total_Discount_Price'] = qt_row['Final_List_Price'] * (qt_row['Total_Discount']/100)
						qt_row['Previous_Year_Sell_Price'] = str(float(qt_row['Previous_Year_List_Price']) - (float(qt_row['Previous_Year_List_Price']) * float(qt_row['Last_Year_Discount'])))
						qt_row['Final_Sell_Price'] = qt_row['Final_List_Price'] - qt_row['Total_Discount_Price']
						Reduction_val = 0
						Addition_val = 0
						if qt_row['Previous_Year_List_Price'] not in (0,'0','',0.00,'0.00','0.0',0.0):
							Reduction_val = qt_row['Scope_Reduction_Price'] * (qt_row['Previous_Year_Sell_Price']/qt_row['Previous_Year_List_Price'])
						if qt_row['Final_List_Price'] not in (0,'0','',0.00,'0.00','0.0',0.0):
							Addition_val = qt_row['Scope_Addition_Price'] * (qt_row['Final_Sell_Price']/qt_row['Final_List_Price'])
						qt_row['Scope_Change'] = Reduction_val + Addition_val
						qt_row['Price_Impact'] = qt_row['Final_Sell_Price'] - (qt_row['Scope_Change'] + qt_row['Previous_Year_Sell_Price'])
						if qt_row['Final_Sell_Price'] != 0:
							qt_row['Margin'] = (1-(qt_row['Current_Year_Cost_Price']/qt_row['Final_Sell_Price']))*100
						qt_row['Comments'] = ct_row['Comments']
					lss_renewal_summary.Save()
		elif SC_Product_Type == "New":
			cont = item.SelectedAttributes.GetContainerByName("SC_LSS_Models_Summary_Cont_Hidden")
			if cont.Rows.Count:
				for ct_row in cont.Rows:
					qt_row = lss_renewal_summary.AddNewRow()
					for col in ['Previous_Year_Quantity','Previous_Year_Unit_List_Price','Previous_Year_List_Price','Previous_Year_Unit_Cost_Price','Previous_Year_Cost_Price','Scope_Reduction_Quantity','Scope_Reduction_Price','Escalation','Escalation_Value','Last_Year_Discount','Previous_Year_Sell_Price','Price_Impact']:
						qt_row[col] = 0
					qt_row['Model'] = ct_row['Model']
					qt_row['Description'] = ct_row['Description']
					qt_row['Renewal_Quantity'] = ct_row['Quantity'] if ct_row['Quantity'] != "" else 0
					qt_row['Honeywell_List_Price_Per_Unit'] = float(ct_row['List_Price'])*ProRatedFactor if ct_row['List_Price'] != "" else 0
					qt_row['Honeywell_List_Price'] = float(ct_row['List_Price'])*ProRatedFactor if ct_row['List_Price'] != "" else 0
					qt_row['Current_Year_Unit_Cost_Price'] = float(ct_row['Cost_Price'])*ProRatedFactor if ct_row['Cost_Price'] != "" else 0
					qt_row['Current_Year_Cost_Price'] = float(ct_row['Cost_Price'])*ProRatedFactor if ct_row['Cost_Price'] != "" else 0
					qt_row['Scope_Addition_Quantity'] = ct_row['Quantity'] if ct_row['Quantity'] != "" else 0
					qt_row['Scope_Addition_Price'] = float(ct_row['List_Price'])*ProRatedFactor if ct_row['List_Price'] != "" else 0
					qt_row['Final_List_Price'] = float(ct_row['List_Price'])*ProRatedFactor if ct_row['List_Price'] != "" else 0
					try:
						qt_row['Total_Discount'] = lss_child_dict["Local Support Standby"][1]
					except:
						qt_row['Total_Discount'] = 0
					qt_row['Total_Discount_Price'] = qt_row['Final_List_Price'] * (qt_row['Total_Discount']/100)
					qt_row['Final_Sell_Price'] = qt_row['Final_List_Price'] - qt_row['Total_Discount_Price']
					qt_row['Scope_Change'] = qt_row['Final_Sell_Price']
					if qt_row['Final_Sell_Price'] != 0:
						qt_row['Margin'] = (1-(qt_row['Current_Year_Cost_Price']/qt_row['Final_Sell_Price']))*100
					qt_row['Comments'] = "Scope Addition"
				lss_renewal_summary.Save()