from GS_CommonModule import getCFValue

CurrentYearExchangeRate = getCFValue(Quote , "SC_CF_EXCHANGE_RATE")
PreviousYearExchangeRate = getCFValue(Quote , "SC_CF_PRVYR_EXCHANGE_RATE")

def get_ExchangeRate(CurrentYearExchangeRate,PreviousYearExchangeRate):
    if PreviousYearExchangeRate!=0:
        ExchangeRateFactor = CurrentYearExchangeRate/PreviousYearExchangeRate
    else:
        ExchangeRateFactor = 1
    
    return ExchangeRateFactor

if	Quote.GetCustomField('Quote Type').Content == 'Contract Renewal':
	
	Generic_renewal_summary = Quote.QuoteTables["Genericl_Module_Renewal_Summary"]
	Generic_renewal_summary.Rows.Clear()
	Generic_renewal_summary.Save()
	from GS_SC_Pop_RenSumm_Grp1 import fn_load_QuoteTable_Grp1
	from GS_SC_Pop_RenSumm_Grp2 import fn_load_QuoteTable_Grp2
	from GS_SC_Pop_RenSumm_Grp3 import fn_load_QuoteTable_Grp3
	from GS_SC_Pop_RenSumm_Grp4 import fn_load_QuoteTable_Grp4
	from GS_SC_Pop_RenSumm_Grp5 import fn_load_QuoteTable_Grp5
	from GS_SC_Pop_RenSumm_Grp6 import fn_load_QuoteTable_Grp6
	reference_number = Quote.GetCustomField("SC_CF_PREVIOUS_QUOTE_NO").Content
    
	genric_prd =  SqlHelper.GetList("SELECT distinct Product_Type FROM CT_SC_Entitlements_Data WHERE Status='Active' and Module_Name ='Generic Module'")
	gen_product = [prd.Product_Type for prd in genric_prd]

	ProRatedFactor=1
	#if Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content=="True":
	#	 ProRatedFactor=float(Quote.GetCustomField("SC_CF_Term_duration_Months").Content)/12.0 if Quote.GetCustomField("SC_CF_Term_duration_Months").Content else 1

	scProducts = {}
	scProductLevel ={
		"SESP" : "Platform",
		"BGP inc Matrikon":"Service Product",
		"Hardware Refresh":"Service Product",
		"Hardware Warranty":"Service Product",
		"Third Party Services":"Entitlement",
		"Enabled Services":"Enabled Services",
		"Cyber":"Service Product",
		"Honeywell Digital Prime":"Service Product",
		"Module":"Service Product",
		"Trace":"Service Product",
		"Workforce Excellence Program":"Service Product",
		"QCS 4.0":["Service Product", "Entitlement"],
		"Parts Management":["Service Product", "Entitlement"],
		"MES Performix":["Service Product", "MES Models"],
		"Labor":["Service Product", "Entitlement"],
		"Experion Extended Support - RQUP ONLY":["Service Product", "Asset", "Asset"],
		"Local Support Standby":"Service Product",
        "Generic Module":"Service Product"
	}

	productExecutionDict = {
		"SESP": "fn_load_QuoteTable_Grp4(Quote,'SESP', item, scProducts.get('SESP', {}),ProRatedFactor,ExchangeRateFactor)",
		"Enabled Services": "fn_load_QuoteTable_Grp4(Quote,'Enabled Services', item, scProducts.get('Enabled Services', {}),ProRatedFactor,ExchangeRateFactor)",
		"Labor": "fn_load_QuoteTable_Grp1(Quote,'Labor', item, scProducts.get('Labor', {}),ProRatedFactor)",
		"Workforce Excellence Program": "fn_load_QuoteTable_Grp5(Quote,'Workforce Excellence Program', item, scProducts.get('Workforce Excellence Program', {}),ProRatedFactor)",
		"MES Performix": "fn_load_QuoteTable_Grp1(Quote,'MES Performix', item, scProducts.get('MES Performix', {}),ProRatedFactor)",
		"Condition Based Maintenance": "fn_load_QuoteTable_Grp2(Quote,'Condition Based Maintenance', item, scProducts.get('Module', {}),ProRatedFactor)",
		"Parts Management": "fn_load_QuoteTable_Grp2(Quote,'Parts Management', item, scProducts.get('Parts Management', {}),ProRatedFactor)",
		"Hardware Warranty": "fn_load_QuoteTable_Grp2(Quote,'Hardware Warranty', item, scProducts.get('Hardware Warranty', {}),ProRatedFactor)",
		"Hardware Refresh": "fn_load_QuoteTable_Grp4(Quote,'Hardware Refresh', item, scProducts.get('Hardware Refresh', {}),ProRatedFactor,ExchangeRateFactor)",
		"Cyber": "fn_load_QuoteTable_Grp5(Quote,'Cyber', item, scProducts.get('Cyber', {}),ProRatedFactor)",
		"Honeywell Digital Prime": "fn_load_QuoteTable_Grp3(Quote,'Honeywell Digital Prime', item, scProducts.get('Honeywell Digital Prime', {}),ProRatedFactor)",
		"Experion Extended Support - RQUP ONLY": "fn_load_QuoteTable_Grp3(Quote,'Experion Extended Support - RQUP ONLY', item, scProducts.get('Experion Extended Support - RQUP ONLY', {}),ProRatedFactor)",
		"Third Party Services": "fn_load_QuoteTable_Grp5(Quote,'Third Party Services', item, scProducts.get('Third Party Services', {}),ProRatedFactor)",
		"BGP inc Matrikon": "fn_load_QuoteTable_Grp3(Quote,'BGP inc Matrikon', item, scProducts.get('BGP inc Matrikon', {}),ProRatedFactor)",
		"QCS 4.0": "fn_load_QuoteTable_Grp3(Quote,'QCS 4.0', item, scProducts.get('QCS 4.0', {}),ProRatedFactor)",
		"Trace": "fn_load_QuoteTable_Grp1(Quote,'Trace', item, scProducts.get('Trace', {}),ProRatedFactor)",
		"Local Support Standby": "fn_load_QuoteTable_Grp5(Quote,'Local Support Standby', item, scProducts.get('Local Support Standby', {}),ProRatedFactor)",
        "Generic Module": "fn_load_QuoteTable_Grp6(Quote,'Generic Module', item, scProducts.get(item.PartNumber, {}),ProRatedFactor)",
		}

	def get_module_child_dic(child,sch_PartNumber):
		ret_dic={}
		for subchild in child.Children:
			Trace.Write("Nilestest subchild " + str(subchild))
			Trace.Write("Nilestest sch_PartNumber " + str(sch_PartNumber))
			escal_dis = []
			if subchild.PartNumber ==sch_PartNumber:
				prev_disc = 0
				escal = str(subchild.QI_SC_Escalation_Percent.Value)
				disc = str(subchild.QI_SC_Total_Discount_Percent.Value)
				escal_dis.extend([escal,disc,prev_disc])
				ret_dic[subchild.Description] = escal_dis
		return ret_dic

	def get_module_child_dic1(child,sch_ServiceProduct):
		ret_dic={}
		for subchild in child.Children:
			if subchild.PartNumber == sch_ServiceProduct[0]:
				for super_child in subchild.Children:
					escal_dis = []
					if super_child.PartNumber == sch_ServiceProduct[1]:
						escal = str(super_child.QI_SC_Escalation_Percent.Value)
						disc = str(super_child.QI_SC_Total_Discount_Percent.Value)
						escal_dis.extend([escal,disc])
						ret_dic[subchild.Description] = escal_dis
		return ret_dic

	def get_module_child_dic2(child,sch_ServiceProduct):
		ret_dic={}
		for subchild in child.Children:
			if subchild.PartNumber == sch_ServiceProduct[0]:
				for super_child in subchild.Children:
					if super_child.PartNumber == sch_ServiceProduct[1]:
						for super_sub_child in super_child.Children:
							escal_dis = []
							escal = disc = prev_disc = py_LP = py_SP = final_SP = final_LP = price_impact = margin = costPrice = 0
							escal = str(super_sub_child.QI_SC_Escalation_Percent.Value)
							disc = str(super_sub_child.QI_SC_Total_Discount_Percent.Value)
							if super_sub_child.Description == 'Other Expense':
								query = SqlHelper.GetFirst("Select Product,QuoteDetails from CT_SC_RENEWAL_QUOTE_TABLE where QuoteID = '{0}' and Product = '{2}' Union ALL Select Product,QuoteDetails from CT_SC_RENEWAL_QUOTE_TABLE where QuoteID = '{1}' and Product = '{2}' AND NOT EXISTS (SELECT 1 FROM CT_SC_RENEWAL_QUOTE_TABLE WHERE QuoteID = '{0}')".format(reference_number, reference_number.split('-')[0], 'Labor'))
								if query is not None:
									quote_details = eval(query.QuoteDetails)
									key = item.PartNumber + '|' + child.Description + "|" + subchild.Description + "|" + super_child.Description + "|" + super_sub_child.Description
									if key in quote_details.keys():
										prev_disc = quote_details[key]['TotalDiscount']
								py_LP = str(super_sub_child.QI_SC_Previous_Year_List_Price.Value)
								py_SP = str(super_sub_child.QI_SC_Previous_Year_Sell_Price.Value)
								final_LP = str(super_sub_child.ExtendedListPrice)
								final_SP = str(super_sub_child.ExtendedAmount)
								price_impact = str(super_sub_child.QI_SC_Price_Impact.Value)
								margin = str(super_sub_child.QI_SC_Margin_Percent.Value)
								numeric_value = ''.join(char for char in super_sub_child.QI_SC_CostPrice.Value if char.isdigit() or char == '.')
								costPrice = str(numeric_value)
								#Trace.Write("super_sub_child.QI_SC_CostPrice--->{0}".format(super_sub_child.QI_SC_CostPrice.Value))
								escal_dis.extend([escal,disc,py_LP,py_SP,final_LP,final_SP,price_impact,margin,prev_disc,costPrice])
							else:
								escal_dis.extend([escal,disc])
							ret_dic[subchild.Description + "|" + super_child.Description + "|" + super_sub_child.Description] = escal_dis
		return ret_dic

	def get_module_child_dic3(child,sch_ServiceProduct):
		ret_dic={}
		for subchild in child.Children:
			if subchild.PartNumber == sch_ServiceProduct:
				for child2 in subchild.Children:
					escal_dis = []
					escal = str(child2.QI_SC_Escalation_Percent.Value)
					disc = str(child2.QI_SC_Total_Discount_Percent.Value)
					escal_dis.extend([escal,disc])
					ret_dic[child2.Description] = escal_dis 
		return ret_dic

	def get_module_child_dic4(child,sch_ServiceProduct):
		ret_dic={}
		for subchild in child.Children:
			if subchild.PartNumber == sch_ServiceProduct[0]:
				for super_child in subchild.Children:
					if super_child.PartNumber == sch_ServiceProduct[1]:
						for super_sub_child in super_child.Children:
							escal_dis = []
							if super_sub_child.PartNumber == sch_ServiceProduct[2]:
								escal = str(super_sub_child.QI_SC_Escalation_Percent.Value)
								disc = str(super_sub_child.QI_SC_Total_Discount_Percent.Value)
								escal_dis.extend([escal,disc])
								ret_dic[super_sub_child.Description] = escal_dis
		return ret_dic

	def get_module_child_dic5(child,sch_ServiceProduct):
		ret_dic={}
		for subchild in child.Children:
			if subchild.PartNumber == sch_ServiceProduct[0]:
				for super_child in subchild.Children:
					escal_dis = []
					if super_child.PartNumber == sch_ServiceProduct[1]:
						escal = str(super_child.QI_SC_Escalation_Percent.Value)
						disc = str(super_child.QI_SC_Total_Discount_Percent.Value)
						escal_dis.extend([escal,disc])
						ret_dic[super_child.Description] = escal_dis
		return ret_dic

	for item in Quote.MainItems:
		if item.PartNumber == "Year-1":
			ProRatedFactor = (1 if (item.QI_SC_EndDate.Value - item.QI_SC_StartDate.Value).Days >= 364 else float(float((item.QI_SC_EndDate.Value - item.QI_SC_StartDate.Value).Days + 1)/365)) if item.QI_SC_EndDate.Value and item.QI_SC_StartDate.Value else 1
			for child in item.Children:
				Trace.Write("Nileshtest " + str(child.PartNumber))
				if child.PartNumber in ("SESP", "BGP inc Matrikon", "Hardware Refresh", "Hardware Warranty", "Third Party Services", "Enabled Services", "Cyber", "Honeywell Digital Prime", "Module", "Trace", "Local Support Standby") or child.PartNumber in gen_product:
					Trace.Write("Nileshtest inside loop" + str(child.PartNumber))
					scProducts[child.PartNumber] = get_module_child_dic(child,scProductLevel["Generic Module" if child.PartNumber in gen_product else child.PartNumber])
					Trace.Write("Nileshtest inside loop scProducts[child.PartNumber] " + str(scProducts[child.PartNumber]))
				elif child.PartNumber in ("QCS 4.0", "Parts Management"):
					scProducts[child.PartNumber] = get_module_child_dic1(child, scProductLevel[child.PartNumber])

				elif child.PartNumber == "Labor":
					scProducts[child.PartNumber] = get_module_child_dic2(child, scProductLevel[child.PartNumber])
					Trace.Write("scProducts[child.PartNumber]-->{0}".format(scProducts[child.PartNumber]))

				elif child.PartNumber == "Workforce Excellence Program":
					scProducts[child.PartNumber]=get_module_child_dic3(child, scProductLevel[child.PartNumber])

				elif child.PartNumber == "Experion Extended Support - RQUP ONLY":
					scProducts[child.PartNumber] = get_module_child_dic4(child,scProductLevel[child.PartNumber])

				elif child.PartNumber in ("MES Performix"):
					scProducts[child.PartNumber] = get_module_child_dic5(child, scProductLevel[child.PartNumber])
                    
		if item.QI_SC_ItemFlag.Value == "Hidden" and item.IsComplete and (item.PartNumber in productExecutionDict or item.ProductName == "Generic Module"):
			eval(productExecutionDict["Generic Module" if item.ProductName == "Generic Module" else item.PartNumber ])

	Quote.CustomFields.AssignValue('SC_CF_RENEWAL_FLAG',"1")