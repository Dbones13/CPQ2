import HCI_PHD_PartSummary_FME
scope = Product.Attr("HCI_PHD_Scope").SelectedValue.Display
prod = Product.Attr("HCI_PHD_Product").SelectedValue.Display
license_model = Product.Attr("HCI_PHD_LicenseModel").SelectedValue.Display
order_type = Product.Attr("HCI_PHD_OrderType").SelectedValue.Display
sql_cals = Product.Attr("SC_Central_Managed_SQL").SelectedValue.Display
esc_factor = Product.Attr("HCI_PHD_ESCALATIONFACTOR").SelectedValue.Display
calc_dic, fme_dic  = {}, {}
product_map = {"PHD & Insight": {license_model: 'PHD(), Insight()'}, "PHD & Insight & AFM": {license_model: 'PHD(), Insight(), AFM()'}, "Advanced Formula Manager (AFM)": {license_model: 'AFM()'}, "Process History Database (PHD)": {license_model: 'PHD()'}, "Insight": {license_model: 'Insight()'}}

def PHD():
	val = 0
	attribute_keys = {"AddMediCopy": "Trace_Software_Additional_Media_Kits","StdUser": "HCI_PHD_Standard_User_CALs","StdDevice": "HCI_PHD_Standard Device","StdCore": "HCI_PHD_Standard_Cores","modbus":"HCI_PHD_Modbus_RDI","exist_modbus": "HCI_PHD_ExistingLicense_Modbus_RDI","restful_api": "HCI_PHD_API_RDI","exist_restful_api": "HCI_PHD_ExistingLicense_API_RDI","sys_monitor": "HCI_PHD_System_Monitoring_RDI","exist_sys_monitor": "HCI_PHD_ExistingLicense_System_Monitoring_RDI","cluster_opt": "HCI_PHD_Clustering_Option","cej_opc": "HCI_PHD_CEJ_OPC_Area_Wide","exist_cej_opc": "HCI_PHD_ExistingLicense_CEJ_OPC_Area_Wide","cej_exp": "HCI_PHD_CEJ_Experion_Area_Wide","exist_cej_exp": "HCI_PHD_ExistingLicense_CEJ_Experion_Area_Wide","cej_tpn": "HCI_PHD_CEJ_TPN_Area_Wide","exist_cej_tpn": "HCI_PHD_ExistingLicense_CEJ_TPN_Area_Wide","cej_req": "HCI_PHD_CEJ_Required","avail_redundancy": "HCI_PHD_Availability_Redundancy","exist_avail_redundancy": "HCI_PHD_ExistingLicense_Availability_Redundancy",    "rdi_file": "HCI_PHD_RDI_File_Access","classic_rdi_opc": "HCI_PHD_Classic_RDI_OPC","rdi_web": "HCI_PHD_RDI_Web_Client","scout_exp": "HCI_PHD_Scout_Express","base_sys_size": "HCI_PHD_Base_System_Size","exist_base_sys": "HCI_PHD_ExistingLicense_Base_System_Size","Tags_base_size": "HCI_PHD_Tags_Base_Size","archive_extract": "HCI_PHD_Archive_Extracto_ Tool","rdi_opc_ua":"HCI_PHD_RDI_OPC_UA","peer_tags": "HCI_PHD_Peer_Tags_Lincensed","license_term": "HCI_PHD_License_Term","upfront_payment": "HCI_PHD_UpFront_Payment"}
	attr = {key: Product.Attr(attr_key).SelectedValue.Display if key not in ['rdi_file', 'classic_rdi_opc', 'rdi_web'] else Product.Attr(attr_key).SelectedValue for key, attr_key in  attribute_keys.items()}
	if Product.IsComplete:
		val = 1
	if license_model == "Term":
		calc_dic['AS-UNPHDES'] = val
		calc_dic['AS-PHDAS'] = val
		calc_dic['AS-PHDRDIS'] = val if val >= 1 else 0
	elif license_model == "Perpetual":
		if order_type == "Maintenance Support Upgrade/Update (No Charge/ BGP Active)":
			calc_dic['AS-UNPHDEM'] = val
			calc_dic['AS-PHDAM'] = val
			calc_dic['AS-PHDRDIM'] = val if val >= 1 else 0
		else:
			calc_dic['AS-UNPHDES'] = val
			calc_dic['AS-PHDAS'] = val
			calc_dic['AS-PHDRDIS'] = val if val >= 1 else 0
		calc_dic['AS-PHDMEDE-430'] = val if val >= 1 else 0
		if int(float(attr["AddMediCopy"])) > 0:
			calc_dic['AS-PHDMEDX-430'] = str(attr["AddMediCopy"])
		if sql_cals == "Yes" and int(float(attr["StdUser"])) > 0:
			calc_dic['AS-HDB22SVRU'] = val
			calc_dic['AS-HDB22SU'] = str(int(float(attr["StdUser"]))-1)
		if sql_cals == "Yes" and int(float(attr["StdDevice"])) > 0:
			calc_dic['AS-HDB22SVRD'] = val
			calc_dic['AS-HDB22SD'] = str(int(float(attr["StdDevice"]))-1)
		if sql_cals == "Yes" and int(float(attr["StdCore"])) > 0:
			calc_dic['AS-HDB22SC'] = val
		if sql_cals == "Yes" and int(float(attr["StdCore"])) > 4:
			calc_dic['AS-HDB22SC2'] = str(round((float(attr["StdCore"])-4) / 2) * 1)
	phd = HCI_PHD_PartSummary_FME.phd(Product,scope,prod,license_model, order_type, sql_cals, esc_factor)
	fme_dic.update(phd)

def Insight():
	Trace.Write('Insight--')
	attribute_keys = {"AddMediCopy": "HCI_Insight_Additional_Media_Copies","StdUser": "HCI_Insight_Standard_User_CALs","StdDevice": "HCI_Insight_Standard_Device_CALs","StdCore": "HCI_Insight_Standard_Cores","Ins_NoEvents": "HCI_Insight_Users_NoEvents","Ins_WithEvents": "HCI_Insight_Users_WithEvents","NoEvents_Single": "HCI_Insight_Single_User","NoEvents_5": "HCI_Insight_Five_User_Pack","NoEvents_10": "HCI_Insight_Ten_User_Pack","NoEvents_25": "HCI_Insight_TwentyFive_User_Pack","NoEvents_50": "HCI_Insight_Fifty_User_Pack","NoEvents_100": "HCI_Insight_Hundred_User_Pack","NoEvents_250": "HCI_Insight_250_User_Pack","Exist_NoEvents_Single": "HCI_Insight_ExistingLicense_Single_User","Exist_NoEvents_5": "HCI_Insight_ExistingLicense_Insight_Five_User_Pack","Exist_NoEvents_10": "HCI_Insight_ExistingLicense_Ten_User_Pack", "Exist_NoEvents_25": "HCI_Insight_ExistingLicense_TwentyFive_User_Pack","Exist_NoEvents_50": "HCI_Insight_ExistingLicense_Fifty_User_Pack","Exist_NoEvents_100": "HCI_Insight_ExistingLicense_Hundred_User_Pack","Exist_NoEvents_250": "HCI_Insight_ExistingLicense_250_User_Pack","Events_Single": "HCI_Insight_Events_Single_User","Events_5": "HCI_Insight_Events_Five_User_Pack","Events_10": "HCI_Insight_Events_Ten_User_Pack","Events_25": "HCI_Insight_Events_TwentyFive_User_Pack","Events_50": "HCI_Insight_Events_Fifty_User_Pack","Events_100": "HCI_Insight_Events_Hundred_User_Pack","Events_250": "HCI_Insight_Events_250_User_Pack","Exist_Events_Single": "HCI_Insight_ExistingLicense_Events_Single_User",    "Exist_Events_5": "HCI_Insight_ExistingLicense_Events_Five_User_Pack","Exist_Events_10": "HCI_Insight_ExistingLicense_Events_Ten_User_Pack","Exist_Events_25": "HCI_Insight_ExistingLicense_Events_TwentyFive_Pack","Exist_Events_50": "HCI_Insight_ExistingLicense_Events_Fifty_User_Pack","Exist_Events_100": "HCI_Insight_ExistingLicense_Events_Hundred_Pack","Exist_Events_250": "HCI_Insight_ExistingLicense_Events_250_User_Pack"}
	attr = {key: Product.Attr(attr_key).SelectedValue.Display for key, attr_key in attribute_keys.items()}
	if license_model == "Term":
		if attr["Ins_NoEvents"]=="Yes":
			calc_dic['AS-UNSGHTS'] = "1"
		if attr["Ins_WithEvents"]=="Yes":
			calc_dic['AS-UNSGHTS-EVENT'] = "1"
	elif license_model == "Perpetual":
		if attr["Ins_NoEvents"]=="Yes":
			calc_dic['AS-UNSGHTS'] = "1"
		if attr["Ins_WithEvents"]=="Yes":
			calc_dic['AS-UNSGHTS-EVENT'] = "1"
		if int(float(attr["AddMediCopy"])) > 0:
			calc_dic['AS-UPSMEDX-323'] = str(attr["AddMediCopy"])
		# if AS-UNSGHTS > 0:
		calc_dic['AS-UIMEDE-240'] = "1"
		#calc_dic['AS-UIMEDX-240'] = str(attr["AddMediCopy"])
		#if AS-HDB9SVRU, AS-HDB9SU, AS-HDB9SVRD, AS-HDB9SD, AS-HDB9SC, AS-HDB9SC2 > 0:
		calc_dic['AS-HDB9ESD'] = "1"
		if calc_dic['AS-HDB9ESD'] == "0":
			calc_dic['AS-HDB9MEDX'] = "0"
		elif int(float(attr["AddMediCopy"])) > 0:
			calc_dic['AS-HDB9MEDX'] = str(attr["AddMediCopy"])
		if sql_cals == "Yes" and int(float(attr["StdUser"])) > 0:
			calc_dic['AS-HDB9SVRU'] = "1"
			calc_dic['AS-HDB9SU'] = str(int(float(attr["StdUser"]))-1)
		if sql_cals == "Yes" and int(float(attr["StdDevice"])) > 0:
			calc_dic['AS-HDB9SVRD'] = "1"
			calc_dic['AS-HDB9SD'] = str(int(float(attr["StdDevice"]))-1)
		if sql_cals == "Yes" and int(float(attr["StdCore"])) > 0:
			calc_dic['AS-HDB9SC'] = "1"
		if sql_cals == "Yes" and int(float(attr["StdCore"])) > 4:
			calc_dic['AS-HDB9SC2'] = str(round((float(attr["StdCore"])-4) / 2) * 1)
	ins = HCI_PHD_PartSummary_FME.ins(Product,scope,prod,license_model, order_type, sql_cals, esc_factor)
	fme_dic.update(ins)

def AFM():
	if license_model == "Perpetual": # and scope == "New Implementation":
		calc_dic['AS-AFMMEDE-206'] = "1"
		#if int(float(Product.Attr('HCI_AFM_Additional_Media').SelectedValue.Display)) > 0:
		#	calc_dic['AS-AFMMEDE-206'] = "1"
		if order_type != "Maintenance Support Upgrade/Update (No Charge/ BGP Active)" and Product.Attr('HCI_AFM_Tag_License_1000').SelectedValue.Display:
			calc_dic['TP-AFMTAGD'] = str(Product.Attr('HCI_AFM_Tag_License_1000').SelectedValue.Display)
		if order_type != "Maintenance Support Upgrade/Update (No Charge/ BGP Active)" and Product.Attr('HCI_AFM_Tag_License_2000').SelectedValue.Display:
			calc_dic['TP-AFMTAGE'] = str(Product.Attr('HCI_AFM_Tag_License_2000').SelectedValue.Display)
		if order_type != "Maintenance Support Upgrade/Update (No Charge/ BGP Active)" and Product.Attr('HCI_AFM_Tag_License_5000').SelectedValue.Display:
			calc_dic['TP-AFMTAGF'] = str(Product.Attr('HCI_AFM_Tag_License_5000').SelectedValue.Display)
		if order_type != "Maintenance Support Upgrade/Update (No Charge/ BGP Active)" and Product.Attr('HCI_AFM_Tag_License_10000').SelectedValue.Display:
			calc_dic['TP-AFMTAGG'] = str(Product.Attr('HCI_AFM_Tag_License_10000').SelectedValue.Display)
		if order_type != "Maintenance Support Upgrade/Update (No Charge/ BGP Active)" and Product.Attr('HCI_AFM_Tag_License_50000').SelectedValue.Display:
			calc_dic['TP-AFMTAGH'] = str(Product.Attr('HCI_AFM_Tag_License_50000').SelectedValue.Display)
		if order_type != "Maintenance Support Upgrade/Update (No Charge/ BGP Active)" and Product.Attr('HCI_AFM_Tag_License_Unlimited').SelectedValue.Display:
			calc_dic['TP-AFMTAGI'] = str(Product.Attr('HCI_AFM_Tag_License_Unlimited').SelectedValue.Display)

def part_summary_update():
	Product.Attr("Calculation_Button").Access = AttributeAccess.ReadOnly
	Session["calculate"] = "no"
	plsg_dic = {}
	product_codes = tuple(calc_dic.keys())
	if str(len(product_codes)) == '1':
		product_codes = str(product_codes)[:-2] + str(product_codes)[-1]
	placeholders = ', '.join(['%s'] * len(product_codes))
	part_summ = Product.GetContainerByName("HCI_PHD_PartSummary_Cont")
	part_summ_trace = Product.GetContainerByName("Trace_Software_Added_Parts_Common_Container") 
	part_summ.Clear()
	part_summ_trace.Clear()
	if product_codes:
		prod = SqlHelper.GetList(""" SELECT p.PRODUCT_NAME, p.PRODUCT_CATALOG_CODE, hpm.ProductLineDesc, hpm.PLSG, hpm.PLSGDesc FROM products p JOIN HPS_PRODUCTS_MASTER hpm ON p.PRODUCT_CATALOG_CODE = hpm.PartNumber WHERE PRODUCT_CATALOG_CODE IN {} """.format(str(product_codes)))
		for p in prod:
			plsg_dic[p.PRODUCT_CATALOG_CODE]=str(p.PRODUCT_NAME)+'~'+str(p.PLSG)+'~'+str(p.PLSGDesc)
		for part_number, quantity in calc_dic.items():
			#Trace.Write('part_summary_update--'+str(part_number))
			if quantity and int(round(float(quantity))) > 0:
				ps = part_summ.AddNewRow(True)
				if str(part_number) == "AS-UNSGHTS-EVENT":
					partnumber =  "AS-UNSGHTS"
				else:
					partnumber = part_number
				ps["PartNumber"] = str(partnumber) 
				ps["Quantity"] = str(int(round(float(quantity))))
				ps["Final Quantity"] = str(int(round(float(quantity))))
				if fme_dic.get(part_number):
					ps["fme"] = str(fme_dic.get(part_number))
				if plsg_dic.get(partnumber):
					(val1, val2, val3) = str(plsg_dic.get(partnumber)).split("~")
					ps["PartDescription"] = val1
					ps["PLSG"] = val2
					ps["plsgDescription"] = val3
				ps.Calculate()
try:
	Trace.Write("--try--")
	eval(product_map[prod][license_model])
except:
	Trace.Write("--Error--")
#eval(product_map[prod][license_model])
part_summary_update()