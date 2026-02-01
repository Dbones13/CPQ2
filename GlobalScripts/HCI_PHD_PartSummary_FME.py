fme_dic  = {}
def escalation_calc(base, license_term, esc_factor):
	b = base
	esc_price = base
	for i in range(2 , int(license_term[:1])+1):
		per =  round(float((b) * int(esc_factor))/100)
		b +=  per
		esc_price += b
	esc_perc = (esc_price - (base * int(esc_factor))) /2
	return int(esc_perc),int(esc_price)

def phd(Product,scope,prod,license_model, order_type, sql_cals, esc_factor):
	attribute_keys = {"AddMediCopy": "Trace_Software_Additional_Media_Kits","StdUser": "HCI_PHD_Standard_User_CALs","StdDevice": "HCI_PHD_Standard Device","StdCore": "HCI_PHD_Standard_Cores","modbus":"HCI_PHD_Modbus_RDI","exist_modbus": "HCI_PHD_ExistingLicense_Modbus_RDI","restful_api": "HCI_PHD_API_RDI","exist_restful_api": "HCI_PHD_ExistingLicense_API_RDI","sys_monitor": "HCI_PHD_System_Monitoring_RDI","exist_sys_monitor": "HCI_PHD_ExistingLicense_System_Monitoring_RDI","cluster_opt": "HCI_PHD_Clustering_Option","cej_opc": "HCI_PHD_CEJ_OPC_Area_Wide","exist_cej_opc": "HCI_PHD_ExistingLicense_CEJ_OPC_Area_Wide","cej_exp": "HCI_PHD_CEJ_Experion_Area_Wide","exist_cej_exp": "HCI_PHD_ExistingLicense_CEJ_Experion_Area_Wide","cej_tpn": "HCI_PHD_CEJ_TPN_Area_Wide","exist_cej_tpn": "HCI_PHD_ExistingLicense_CEJ_TPN_Area_Wide","cej_req": "HCI_PHD_CEJ_Required","avail_redundancy": "HCI_PHD_Availability_Redundancy","exist_avail_redundancy": "HCI_PHD_ExistingLicense_Availability_Redundancy",    "rdi_file": "HCI_PHD_RDI_File_Access","rdi_file_exit": "HCI_PHD_ExistingLicense_RDI_File_Access","classic_rdi_opc": "HCI_PHD_Classic_RDI_OPC","classic_rdi_opc_exit": "HCI_PHD_ExistingLicense_Classic_RDI_OPC","rdi_web": "HCI_PHD_RDI_Web_Client","rdi_web_exit":"HCI_PHD_ExistingLicense_RDI_Web_Client","scout_exp": "HCI_PHD_Scout_Express","exist_scout_exp":"HCI_PHD_ExistingLicense_Scout_Express","base_sys_size": "HCI_PHD_Base_System_Size","exist_base_sys": "HCI_PHD_ExistingLicense_Base_System_Size","Tags_base_size": "HCI_PHD_Tags_Base_Size","archive_extract": "HCI_PHD_Archive_Extracto_ Tool","rdi_opc_ua":"HCI_PHD_RDI_OPC_UA","peer_tags": "HCI_PHD_Peer_Tags_Lincensed","license_term": "HCI_PHD_License_Term","upfront_payment": "HCI_PHD_UpFront_Payment","convert_cluster":"HCI_PHD_Convert_Clustering","exist_convert_cluster":"HCI_PHD_ExistingLicense_Convert_Clustering","Existing_Tags_base_size":"HCI_PHD_ExistingLicense_Tags_Base_Size","exist_archive_extract":"HCI_PHD_ExistingLicense_Archive_Extracto_ Tool"}
	attr = {key: Product.Attr(attr_key).SelectedValue.Display if key not in ['rdi_file','rdi_file_exit', 'classic_rdi_opc','classic_rdi_opc_exit', 'rdi_web','rdi_web_exit'] else Product.Attr(attr_key).SelectedValue for key, attr_key in  attribute_keys.items()}
	# FME string: AS-UNPHDE = "AS-UNPHDES-N-S-N-Y-N-1-1-AA-ZZ-N-0001-0-0-0-0-AA-0000-P-001-000000-000000"
	if (license_model == "Perpetual" or license_model == "Term") and order_type:
		base = SqlHelper.GetFirst(""" SELECT PRODUCT_PRICE FROM products p JOIN HPS_PRODUCTS_MASTER hpm ON p.PRODUCT_CATALOG_CODE = hpm.PartNumber WHERE PRODUCT_CATALOG_CODE='AS-UNPHDES' """)
		phd_FME3 = 'AS-UNPHDEM' if order_type == "Maintenance Support Upgrade/Update (No Charge/ BGP Active)" else 'AS-UNPHDES'
		if scope == "New Implementation" or scope == "Upgrade":
			phd_FME3 = phd_FME3 + '-N'
		elif scope == "Expansion":
			phd_FME3 = phd_FME3 + '-M'
		if order_type== "Competitive Replacement" or order_type == "Non-Support Upgrade":
			phd_FME3 = phd_FME3 + '-R'
		elif order_type == "Maintenance Support Upgrade/Update (No Charge/ BGP Active)":
			phd_FME3 = phd_FME3 + '-N'
		else:
			phd_FME3 = phd_FME3 + '-S'
		# Suite Factor - SOF, it is manually entered as 'N', no formula behind it .
		phd_FME3 = phd_FME3 + '-N'
		# Clustering/High avail option Factor:
		if attr["avail_redundancy"] == "Yes" and attr["cluster_opt"] == "Yes" : # and attr["convert_cluster"] == "Yes":
			phd_FME3 = phd_FME3 + '-Y'
		elif attr["avail_redundancy"] == "Yes" and attr["cluster_opt"] == "No" :  # and attr["convert_cluster"] == "Yes":
			phd_FME3 = phd_FME3 + '-Y'
		elif attr["avail_redundancy"] == "No" and attr["cluster_opt"] == "Yes":  # and attr["convert_cluster"] == "No":
			phd_FME3 = phd_FME3 + '-N'    
		elif attr["avail_redundancy"] == "No" and attr["cluster_opt"] == "No" :  # and attr["convert_cluster"] == "No":
			phd_FME3 = phd_FME3 + '-N'    
		# Conversion Factor, Base system, Tag size Base
		phd_FME3 = phd_FME3 + '-N-1-1'
		# Tag size Factor
		if (scope == "New Implementation" or scope == "Upgrade") and attr["base_sys_size"]:
			phd_FME3 = phd_FME3 +'-'+attr["base_sys_size"][:1] + attr["base_sys_size"][:1]
		elif scope == "Expansion" and (attr["base_sys_size"] and attr["exist_base_sys"]):
			if attr["base_sys_size"][:1] != attr["exist_base_sys"][:1]:
				phd_FME3 = phd_FME3 +'-'+attr["exist_base_sys"][:1] + attr["base_sys_size"][:1]
			else:
				phd_FME3 = phd_FME3 + '-ZZ'
		else:
			phd_FME3 = phd_FME3 + '-ZZ'
		# Prev Tag size factor:
		if (scope == "New Implementation" or scope == "Upgrade") and (attr["base_sys_size"]):
			#phd_FME3 = phd_FME3 +'-'+attr["base_sys_size"][:1] + attr["base_sys_size"][:1]
			phd_FME3 = phd_FME3 + '-ZZ'
		elif scope == "Expansion" and (attr["exist_base_sys"]):
			phd_FME3 = phd_FME3 +'-'+attr["exist_base_sys"][:1] + attr["exist_base_sys"][:1]
		else:
			phd_FME3 = phd_FME3 + '-ZZ'
		# Clustering/High Avail Catch up factor:
		if scope== "New Implementation" or scope == "Upgrade":
			phd_FME3 = phd_FME3 + '-N'
		elif scope == "Expansion":
			if attr["exist_avail_redundancy"]=="No" and attr["avail_redundancy"]=="Yes":
				phd_FME3 = phd_FME3 + '-Y'
			elif attr["exist_avail_redundancy"]=="Yes" and attr["avail_redundancy"]=="Yes":
				phd_FME3 = phd_FME3 + '-Y'
			else:
				phd_FME3 = phd_FME3 + '-N'
		#Tag Pack add 1000
		phd_FME3 = phd_FME3 +'-'+str(int(float(attr["Tags_base_size"]))).zfill(4)
		#Tag Pack Add 2500, Tag pack add 10000, Tag pack add 50000, Tag Pack 100 Factor
		phd_FME3 = phd_FME3 + '-0-0-0-0'
		if attr["base_sys_size"] and attr["base_sys_size"]:
			phd_FME3 = phd_FME3 +'-'+attr["base_sys_size"][:1] + attr["base_sys_size"][:1]
		else:
			phd_FME3 = phd_FME3 +'-ZZ'
		#Tag Pack Prev 1000 Quantity
		if scope == "New Implementation" or scope == "Upgrade":
			phd_FME3 = phd_FME3 + '-0000'
		elif scope == "Expansion":
			if attr["Tags_base_size"] > '0':
				phd_FME3 = phd_FME3 +'-'+str(int(float(attr["Existing_Tags_base_size"]))).zfill(4)
			else:
				phd_FME3 = phd_FME3 + '-0000'
		if license_model == "Perpetual":
			# Period Factor, Period Quantity, Escalation, Programs
			phd_FME3 = phd_FME3 + '-P-001-000000-000000'
		elif  license_model == "Term":
			# Period Factor, Period Quantity
			if scope == "Expansion":
				phd_FME3 = phd_FME3 + '-P'
			elif scope == "New Implementation" or scope == "Upgrade":
				license_mapping = {"1 Year": '-L-001',"2 Years": '-K-002',"3 Years": '-H-003',"4 Years": '-F-004',"5 Years": '-E-005',"6 Years": '-D-006'}
				phd_FME3 += license_mapping.get(attr["license_term"], '')
			# Escalation & Programs #
			#base = 4447 #base.PRODUCT_PRICE
			if base.PRODUCT_PRICE and esc_factor > 0:
				esc_perc, esc_price=escalation_calc(base.PRODUCT_PRICE, attr["license_term"], esc_factor)
				if attr["upfront_payment"]=="Yes":
					upfront_perc, upfront_price=escalation_calc(base.PRODUCT_PRICE, attr["license_term"],4)
					upfront_perc = (esc_price - upfront_price)/2
					phd_FME3 = phd_FME3 +'-'+str(esc_perc).zfill(6)+'-'+str(upfront_perc).zfill(6)
				elif attr["upfront_payment"]=="No":
					phd_FME3 = phd_FME3 +'-'+str(esc_perc).zfill(6)+'-000000'
			else:
				phd_FME3 = phd_FME3 + '-000000-000000'
		if order_type == "Maintenance Support Upgrade/Update (No Charge/ BGP Active)":
			fme_dic['AS-UNPHDEM'] = phd_FME3
		else:
			fme_dic['AS-UNPHDES'] = phd_FME3
	# FME string: AS-PHDAS = "AS-PHDAS-N-S-N-N-N-N-N-Y-H-N-N-N-N-N-0-00-00-00-00-0000-P-001-000000-000000"
	if (license_model == "Perpetual" or license_model == "Term") and order_type:
		base = SqlHelper.GetFirst(""" SELECT PRODUCT_PRICE FROM products p JOIN HPS_PRODUCTS_MASTER hpm ON p.PRODUCT_CATALOG_CODE = hpm.PartNumber WHERE PRODUCT_CATALOG_CODE='AS-PHDAS' """)
		phd_FME2 = 'AS-PHDAM' if order_type == "Maintenance Support Upgrade/Update (No Charge/ BGP Active)" else 'AS-PHDAS'
		if scope == "New Implementation" or scope == "Upgrade":
			phd_FME2 = phd_FME2 + '-N'
		elif scope == "Expansion":
			phd_FME2 = phd_FME2 + '-M'
		if order_type == "Competitive Replacement" or order_type == "Non-Support Upgrade":
			phd_FME2 = phd_FME2 + '-R'
		elif order_type == "Maintenance Support Upgrade/Update (No Charge/ BGP Active)":
			phd_FME2 = phd_FME2 + '-N'
		else:
			phd_FME2 = phd_FME2 + '-S'
		# Suite Factor, System Factor, Clustering option Factor:
		phd_FME2 = phd_FME2 + '-N-N-N'
		# CEJ EJC TPN Area Wide, CEJ Experion Area-Wide, CEJ OPC Area-Wide: 
		if scope == "New Implementation" or scope == "Upgrade":
			phd_FME2 = phd_FME2 +'-'+attr["cej_tpn"][:1] 
			phd_FME2 = phd_FME2 +'-'+attr["cej_exp"][:1]
			phd_FME2 = phd_FME2 +'-'+attr["cej_opc"][:1]
		else:
			if attr["cej_tpn"]=="Yes" and attr["exist_cej_tpn"]=="No":
				phd_FME2 = phd_FME2 +'-Y'
			else:
				phd_FME2 = phd_FME2 +'-N'
			if attr["cej_exp"]=="Yes" and attr["exist_cej_exp"]=="No":
				phd_FME2 = phd_FME2 +'-Y'
			else:
				phd_FME2 = phd_FME2 +'-N'
			if attr["cej_opc"]=="Yes" and attr["exist_cej_opc"]=="No":
				phd_FME2 = phd_FME2 +'-Y'
			else:
				phd_FME2 = phd_FME2 +'-N'
		# RDI File Access FTP:
		if attr["rdi_file"].Display[:1] != attr["rdi_file_exit"].Display[:1]:
			phd_FME2 = phd_FME2 +'-'+attr["rdi_file"].Display[:1]
		else:
			phd_FME2 = phd_FME2 +'-N'
		#Classic RDI OPC Area Wide
		if attr["classic_rdi_opc"]:
			if attr["classic_rdi_opc"].Display[:1] == attr["classic_rdi_opc_exit"].Display[:1]:
				phd_FME2 = phd_FME2 +'-N' 
			else:
				phd_FME2 = phd_FME2 +'-'+attr["classic_rdi_opc"].Display[:1]
		# RDI Web Client
		if attr["rdi_web"].Display[:1]  != attr["rdi_web_exit"].Display[:1]:
			phd_FME2 = phd_FME2 +'-'+attr["rdi_web"].Display[:1] 
		else:
			phd_FME2 = phd_FME2 +'-N' 
		# Scout Express
		if scope == "New Implementation" or scope == "Upgrade":
			if attr["scout_exp"]=="Yes":
				base_sys = str(attr["base_sys_size"]).split(" ")[1].replace(",", "")
				base_sys_size = int(base_sys) + (1000 * int(float(attr["Tags_base_size"])))
				if base_sys_size < 100001:
					phd_FME2 = phd_FME2 +'-A'
				elif base_sys_size >= 100001:
					phd_FME2 = phd_FME2 +'-B'
			else:
				phd_FME2 = phd_FME2 +'-N'
		elif scope == "Expansion":
			if attr["exist_scout_exp"] == "No" and attr["scout_exp"] == "Yes":
				ex_base_sys = str(attr["exist_base_sys"]).split(" ")[1].replace(",", "")
				ex_base_sys_size = int(ex_base_sys) + (1000 * int(float(attr["Existing_Tags_base_size"]))) + (1000 * int(float(attr["Tags_base_size"])))
				if ex_base_sys_size < 100001:
					phd_FME2 = phd_FME2 +'-A'
				elif ex_base_sys_size >= 100001:
					phd_FME2 = phd_FME2 +'-B'
			else:
				phd_FME2 = phd_FME2 +'-N'
		# Data Extender
		if scope == "New Implementation" or scope == "Upgrade":
			if attr["archive_extract"]=="Yes":
				base_sys = str(attr["base_sys_size"]).split(" ")[1].replace(",", "")
				base_sys_size = int(base_sys) + (1000 * int(float(attr["Tags_base_size"])))
				if base_sys_size < 100001:
					phd_FME2 = phd_FME2 +'-A'
				elif base_sys_size >= 100001:
					phd_FME2 = phd_FME2 +'-B'
			else:
				phd_FME2 = phd_FME2 +'-N'
		elif scope == "Expansion":
			if attr["exist_archive_extract"] == "No" and attr["archive_extract"] == "Yes":
				ex_base_sys = str(attr["exist_base_sys"]).split(" ")[1].replace(",", "")
				ex_base_sys_size = int(ex_base_sys) + (1000 * int(float(attr["Existing_Tags_base_size"]))) + (1000 * int(float(attr["Tags_base_size"])))
				if ex_base_sys_size < 100001:
					phd_FME2 = phd_FME2 +'-A'
				elif ex_base_sys_size >= 100001:
					phd_FME2 = phd_FME2 +'-B'
			else:
				phd_FME2 = phd_FME2 +'-N'
		# RDI OPC UA Area Wide
		phd_FME2 = phd_FME2 +'-'+attr["rdi_opc_ua"][:1] 
		# Peer Tag10K HA Tier1
		if attr["avail_redundancy"] == "Yes" and int(float(attr["peer_tags"])) > 0:
			phd_FME2 = phd_FME2 +'-1'
		else:
			phd_FME2 = phd_FME2 +'-0'
		# Peer Tag10K HA Tier2 upto 6
		if attr["avail_redundancy"] == "No":
			phd_FME2 = phd_FME2 +'-00-00-00-00-0000'
		elif attr["avail_redundancy"] == "Yes":
			if (int(float(attr["peer_tags"]))) <= 10000:
				phd_FME2 = phd_FME2 +'-00-00-00-00-0000'
			elif (int(float(attr["peer_tags"]))) <= 50000:
				t2 = attr["peer_tags"][:1].zfill(2)
				phd_FME2 = phd_FME2 +'-'+t2+'-00-00-00-0000'
			elif (int(float(attr["peer_tags"]))) <= 100000:
				t3 = str(int(attr["peer_tags"][:1]) -4).zfill(2)
				phd_FME2 = phd_FME2 +'-04-'+t3+'-00-00-0000'
			elif (int(float(attr["peer_tags"]))) <= 250000:
				t4 = str(int(attr["peer_tags"][:1]) -9).zfill(2)
				phd_FME2 = phd_FME2 +'-04-05-'+t4+'-00-0000'
			elif (int(float(attr["peer_tags"]))) <= 500000:
				t5 = str(int(attr["peer_tags"][:1]) -24).zfill(2)
				phd_FME2 = phd_FME2 +'-04-05-15-'+t5+'-0000'
			elif (int(float(attr["peer_tags"]))) <= 1000000:
				t6 = str(int(attr["peer_tags"][:2]) -49).zfill(4)
				phd_FME2 = phd_FME2 +'-04-05-15-25-'+t6
			elif (int(float(attr["peer_tags"]))) <= 9999999:
				t7 = str(int(attr["peer_tags"][:3]) -50).zfill(4)
				phd_FME2 = phd_FME2 +'-04-05-15-25-'+t7
		if license_model == "Perpetual":
			# Period Factor, Period Quantity, Escalation, Programs
			phd_FME2 = phd_FME2 +'-P-001-000000-000000'
		elif  license_model == "Term":
			# Period Factor, Period Quantity
			if scope == "Expansion":
				phd_FME2 = phd_FME2 + '-P'
			elif scope == "New Implementation" or scope == "Upgrade":
				license_mapping = {"1 Year": '-L-001',"2 Years": '-K-002',"3 Years": '-H-003',"4 Years": '-F-004',"5 Years": '-E-005',"6 Years": '-D-006'}
				phd_FME2 += license_mapping.get(attr["license_term"], '')
			# Escalation & Programs
			if base.PRODUCT_PRICE and esc_factor > 0:
				esc_perc, esc_price=escalation_calc(base.PRODUCT_PRICE, attr["license_term"], esc_factor)
				if attr["upfront_payment"]=="Yes":
					upfront_perc, upfront_price=escalation_calc(base.PRODUCT_PRICE, attr["license_term"],4)
					upfront_perc = (esc_price - upfront_price)/2
					phd_FME2 = phd_FME2 +'-'+str(esc_perc).zfill(6)+'-'+str(upfront_perc).zfill(6)
				elif attr["upfront_payment"]=="No":
					phd_FME2 = phd_FME2 +'-'+str(esc_perc).zfill(6)+'-000000'
			else:
				phd_FME2 = phd_FME2 + '-000000-000000'
		if order_type == "Maintenance Support Upgrade/Update (No Charge/ BGP Active)":
			fme_dic['AS-PHDAM'] = phd_FME2
		else:
			fme_dic['AS-PHDAS'] = phd_FME2
	# FME string: AS-PHDRDI = = "AS-PHDRDIS-N-S-N-N-N-Y-Y-P-001-000000-000000"
	if (license_model == "Perpetual" or license_model == "Term") and order_type:
		base = SqlHelper.GetFirst(""" SELECT PRODUCT_PRICE FROM products p JOIN HPS_PRODUCTS_MASTER hpm ON p.PRODUCT_CATALOG_CODE = hpm.PartNumber WHERE PRODUCT_CATALOG_CODE='AS-PHDRDIS' """)
		phd_FME1 = 'AS-PHDRDIM' if order_type == "Maintenance Support Upgrade/Update (No Charge/ BGP Active)" else 'AS-PHDRDIS'
		if scope == "New Implementation" or scope == "Upgrade":
			phd_FME1 = phd_FME1 + '-N'
		elif scope == "Expansion":
			phd_FME1 = phd_FME1 + '-M'
		if order_type == "Competitive Replacement" or order_type == "Non-Support Upgrade":
			phd_FME1 = phd_FME1 + '-R'
		elif order_type == "Maintenance Support Upgrade/Update (No Charge/ BGP Active)":
			phd_FME1 = phd_FME1 + '-N'
		else:
			phd_FME1 = phd_FME1 + '-S'
		# Suite Factor, System Factor.
		phd_FME1 = phd_FME1 + '-N-N'
		# MODBUS RDI, RESTFUL API RDI, System Monitoring RDI (WMI, PerfMon, Ping, SNMP)
		if scope == "New Implementation" or scope == "Upgrade":
			phd_FME1 = phd_FME1 +'-'+attr["modbus"][:1]
			phd_FME1 = phd_FME1 +'-'+attr["restful_api"][:1]
			phd_FME1 = phd_FME1 +'-'+attr["sys_monitor"][:1]
		elif scope == "Expansion": 
			if attr["exist_modbus"]=="No" and attr["modbus"]=="Yes":
				phd_FME1 = phd_FME1 +'-Y'
			else:
				phd_FME1 = phd_FME1 +'-N'
			if attr["exist_restful_api"]=="No" and attr["restful_api"]=="Yes":
				phd_FME1 = phd_FME1 +'-Y'
			else:
				phd_FME1 = phd_FME1 +'-N'
			if attr["exist_sys_monitor"]=="No" and attr["sys_monitor"]=="Yes": 
				phd_FME1 = phd_FME1 +'-Y'
			else:
				phd_FME1 = phd_FME1 +'-N'
		if license_model == "Perpetual":
			# Period Factor, Period Quantity, Escalation, Programs
			phd_FME1 = phd_FME1 + '-P-001-000000-000000'
		elif  license_model == "Term":
			# Period Factor, Period Quantity
			if scope == "Expansion":
				phd_FME1 = phd_FME1 + '-P'
			elif scope == "New Implementation" or scope == "Upgrade":
				license_mapping = {"1 Year": '-L-001',"2 Years": '-K-002',"3 Years": '-H-003',"4 Years": '-F-004',"5 Years": '-E-005',"6 Years": '-D-006'}
				phd_FME1 += license_mapping.get(attr["license_term"], '')
			# Escalation & Programs
			if base.PRODUCT_PRICE and esc_factor > 0:
				esc_perc, esc_price=escalation_calc(base.PRODUCT_PRICE, attr["license_term"], esc_factor)
				if attr["upfront_payment"]=="Yes":
					upfront_perc, upfront_price=escalation_calc(base.PRODUCT_PRICE, attr["license_term"],4)
					upfront_perc = (esc_price - upfront_price)/2
					phd_FME1 = phd_FME1 +'-'+str(esc_perc).zfill(6)+'-'+str(upfront_perc).zfill(6)
				elif attr["upfront_payment"]=="No":
					phd_FME1 = phd_FME1 +'-'+str(esc_perc).zfill(6)+'-000000'
			else:
				phd_FME1 = phd_FME1 + '-000000-000000'
		if order_type == "Maintenance Support Upgrade/Update (No Charge/ BGP Active)":
			fme_dic['AS-PHDRDIM'] = phd_FME1
		else:
			fme_dic['AS-PHDRDIS'] = phd_FME1
	return fme_dic

def ins(Product,scope,prod,license_model, order_type, sql_cals, esc_factor):
	attribute_keys = {"AddMediCopy": "HCI_Insight_Additional_Media_Copies","StdUser": "HCI_Insight_Standard_User_CALs","StdDevice": "HCI_Insight_Standard_Device_CALs","StdCore": "HCI_Insight_Standard_Cores","Ins_NoEvents": "HCI_Insight_Users_NoEvents","Ins_WithEvents": "HCI_Insight_Users_WithEvents","NoEvents_Single": "HCI_Insight_Single_User","NoEvents_5": "HCI_Insight_Five_User_Pack","NoEvents_10": "HCI_Insight_Ten_User_Pack","NoEvents_25": "HCI_Insight_TwentyFive_User_Pack","NoEvents_50": "HCI_Insight_Fifty_User_Pack","NoEvents_100": "HCI_Insight_Hundred_User_Pack","NoEvents_250": "HCI_Insight_250_User_Pack","Exist_NoEvents_Single": "HCI_Insight_ExistingLicense_Single_User","Exist_NoEvents_5": "HCI_Insight_ExistingLicense_Insight_Five_User_Pack","Exist_NoEvents_10": "HCI_Insight_ExistingLicense_Ten_User_Pack", "Exist_NoEvents_25": "HCI_Insight_ExistingLicense_TwentyFive_User_Pack","Exist_NoEvents_50": "HCI_Insight_ExistingLicense_Fifty_User_Pack","Exist_NoEvents_100": "HCI_Insight_ExistingLicense_Hundred_User_Pack","Exist_NoEvents_250": "HCI_Insight_ExistingLicense_250_User_Pack","Events_Single": "HCI_Insight_Events_Single_User","Events_5": "HCI_Insight_Events_Five_User_Pack","Events_10": "HCI_Insight_Events_Ten_User_Pack","Events_25": "HCI_Insight_Events_TwentyFive_User_Pack","Events_50": "HCI_Insight_Events_Fifty_User_Pack","Events_100": "HCI_Insight_Events_Hundred_User_Pack","Events_250": "HCI_Insight_Events_250_User_Pack","Exist_Events_Single": "HCI_Insight_ExistingLicense_Events_Single_User",    "Exist_Events_5": "HCI_Insight_ExistingLicense_Events_Five_User_Pack","Exist_Events_10": "HCI_Insight_ExistingLicense_Events_Ten_User_Pack","Exist_Events_25": "HCI_Insight_ExistingLicense_Events_TwentyFive_Pack","Exist_Events_50": "HCI_Insight_ExistingLicense_Events_Fifty_User_Pack","Exist_Events_100": "HCI_Insight_ExistingLicense_Events_Hundred_Pack","Exist_Events_250": "HCI_Insight_ExistingLicense_Events_250_User_Pack","license_term": "HCI_Insight_License_Term","upfront_payment": "HCI_Insight_UpFront_Payment_Option"}
	attr = {key: Product.Attr(attr_key).SelectedValue.Display for key, attr_key in attribute_keys.items()}
	# FME string: AS-UNSGHTS(No Events) = "AS-UNSGHTS-N-S-N-N-N-0-0-0-0-0-0-000-0000-0000-0000-0000-0000-0000-0000-0-A-A-Y-P-001-000000-000000"
	# This FME string is Valid Format   = "AS-UNSGHTS-N-S-N-N-N-0-0-0-0-0-0-0-0000-0000-0000-0000-0000-0000-0001-0-0-1-A-A-N-P-001-000000-000000"
	if (license_model == "Perpetual" or license_model == "Term") and order_type and attr["Ins_NoEvents"]=="Yes":
		base = SqlHelper.GetFirst(""" SELECT PRODUCT_PRICE FROM products p JOIN HPS_PRODUCTS_MASTER hpm ON p.PRODUCT_CATALOG_CODE = hpm.PartNumber WHERE PRODUCT_CATALOG_CODE='AS-UNSGHTS' """)
		Ins_FME1 = 'AS-UNSGHTS'
		if scope == "New Implementation" or scope == "Upgrade":
			Ins_FME1 = Ins_FME1 + '-N'
		elif scope == "Expansion":
			Ins_FME1 = Ins_FME1 + '-M'
		if order_type == "Competitive Replacement" or order_type == "Non-Support Upgrade":
			Ins_FME1 = Ins_FME1 + '-R'
		elif order_type=='Maintenance Support Upgrade/Update (No Charge/ BGP Active)':
			Ins_FME1 = Ins_FME1 + '-N'
		else:
			Ins_FME1 = Ins_FME1 + '-S'
		# Suite Factor, Historian Factor, Conversion Factor, Base system Price:
		Ins_FME1 = Ins_FME1 + '-N-N-N-0'
		# Added 5, 10, 25, 50, 100, 250 User Packs 
		if scope == "New Implementation" or scope == "Expansion" or (scope == "Upgrade" and order_type!='Maintenance Support Upgrade/Update (No Charge/ BGP Active)'):
			Ins_FME1 = Ins_FME1 +'-'+ str(int(float(attr["NoEvents_5"]))).zfill(1)
			Ins_FME1 = Ins_FME1 +'-'+ str(int(float(attr["NoEvents_10"]))).zfill(1)
			Ins_FME1 = Ins_FME1 +'-'+ str(int(float(attr["NoEvents_25"]))).zfill(1)
			Ins_FME1 = Ins_FME1 +'-'+ str(int(float(attr["NoEvents_50"]))).zfill(1)
			Ins_FME1 = Ins_FME1 +'-'+ str(int(float(attr["NoEvents_100"]))).zfill(1)
			Ins_FME1 = Ins_FME1 +'-'+ str(int(float(attr["NoEvents_250"]))).zfill(3)
		elif scope == "Upgrade" and order_type=='Maintenance Support Upgrade/Update (No Charge/ BGP Active)':
			Ins_FME1 = Ins_FME1 +'-0'
			Ins_FME1 = Ins_FME1 +'-0'
			Ins_FME1 = Ins_FME1 +'-0'
			Ins_FME1 = Ins_FME1 +'-0'
			Ins_FME1 = Ins_FME1 +'-0'
			Ins_FME1 = Ins_FME1 +'-000'
		# Upgrades from Web (Used for non-events to Events), Upgrades from Basic, Upgrades from Adv/Devt, Upgrades from OI, Upgrades from Workcenter
		Ins_FME1 = Ins_FME1 + '-0000-0000-0000-0000-0000'
		# Previous Users
		if scope == "New Implementation" or (scope == "Upgrade" and order_type!='Maintenance Support Upgrade/Update (No Charge/ BGP Active)'):
			Ins_FME1 = Ins_FME1 + '-0000'
			'''n = int(float(attr["NoEvents_Single"])) + int(float(attr["NoEvents_5"]))*5 + int(float(attr["NoEvents_10"]))*10 + int(float(attr["NoEvents_25"]))*25 + int(float(attr["NoEvents_50"]))*50 + int(float(attr["NoEvents_100"]))*100 + int(float(attr["NoEvents_250"]))*250
			if str(len(str(n))) > "4":
				n = str(n)[:4]
				Ins_FME1 = Ins_FME1 +'-'+ str(n).zfill(4)
			else:
				Ins_FME1 = Ins_FME1 +'-'+ str(n).zfill(4)'''
		elif scope == "Upgrade" and order_type=='Maintenance Support Upgrade/Update (No Charge/ BGP Active)':
			n = int(float(attr["NoEvents_Single"])) + int(float(attr["NoEvents_5"]))*5 + int(float(attr["NoEvents_10"]))*10 + int(float(attr["NoEvents_25"]))*25 + int(float(attr["NoEvents_50"]))*50 + int(float(attr["NoEvents_100"]))*100 + int(float(attr["NoEvents_250"]))*250
			if str(len(str(n))) > "4":
				n = str(n)[:4]
				Ins_FME1 = Ins_FME1 +'-'+ str(n).zfill(4)
			else:
				Ins_FME1 = Ins_FME1 +'-'+ str(n).zfill(4)
		elif scope == "Expansion":
			e = int(float(attr["Exist_NoEvents_Single"])) + int(float(attr["Exist_NoEvents_5"]))*5 + int(float(attr["Exist_NoEvents_10"]))*10 + int(float(attr["Exist_NoEvents_25"]))*25 + int(float(attr["Exist_NoEvents_50"]))*50 + int(float(attr["Exist_NoEvents_100"]))*100 + int(float(attr["Exist_NoEvents_250"]))*250
			if str(len(str(e))) > "4":
				e = str(e)[:4]
				Ins_FME1 = Ins_FME1 +'-'+ str(e).zfill(4)
			else:
				Ins_FME1 = Ins_FME1 +'-'+ str(e).zfill(4)
		# New Added Users SumUp
		if scope == "New Implementation" or scope == "Upgrade" and (order_type!='Maintenance Support Upgrade/Update (No Charge/ BGP Active)'):
			#Ins_FME1 = Ins_FME1 + '-000000'
			n = int(float(attr["NoEvents_Single"])) + int(float(attr["NoEvents_5"]))*5 + int(float(attr["NoEvents_10"]))*10 + int(float(attr["NoEvents_25"]))*25 + int(float(attr["NoEvents_50"]))*50 + int(float(attr["NoEvents_100"]))*100 + int(float(attr["NoEvents_250"]))*250
			if str(len(str(n))) > "":
				n = str(n)[:6]
				Ins_FME1 = Ins_FME1 +'-'+ str(n).zfill(6)
			else:
				Ins_FME1 = Ins_FME1 +'-'+ str(n).zfill(6)
		elif scope == "Upgrade" and order_type=='Maintenance Support Upgrade/Update (No Charge/ BGP Active)':
			Ins_FME1 = Ins_FME1 + '-000000'
		elif scope == "Expansion":
			n = int(float(attr["NoEvents_Single"])) + int(float(attr["NoEvents_5"]))*5 + int(float(attr["NoEvents_10"]))*10 + int(float(attr["NoEvents_25"]))*25 + int(float(attr["NoEvents_50"]))*50 + int(float(attr["NoEvents_100"]))*100 + int(float(attr["NoEvents_250"]))*250
			if str(len(str(n))) > "6":
				n = str(n)[:6]
				Ins_FME1 = Ins_FME1 +'-'+ str(n).zfill(6)
			else:
				Ins_FME1 = Ins_FME1 +'-'+ str(n).zfill(6)
		#Ins_FME1 = Ins_FME1 + '-0-0' # This FME string '-0-0' concat is right/valid format.
		# Added 1-User Packs
		if scope == "New Implementation" or scope == "Expansion" or (scope == "Upgrade" and order_type!='Maintenance Support Upgrade/Update (No Charge/ BGP Active)'):
			Ins_FME1 = Ins_FME1 +'-'+str(int(float(attr["NoEvents_Single"])))
		elif scope == "Upgrade" and order_type=='Maintenance Support Upgrade/Update (No Charge/ BGP Active)':
			Ins_FME1 = Ins_FME1 +'-0'
		#elif scope == "Expansion":
		#	Ins_FME1 = Ins_FME1 +'-'+str(int(float(attr["Exist_NoEvents_Single"])))
		# Web Upgrade Tier Factor ( Used for non-events to Events), Basic Upgrade Tier Factor, Event Analysis Option Factor
		Ins_FME1 = Ins_FME1 + '-A-A-N'
		if license_model == "Perpetual":
			# Period Factor, Period Quantity, Escalation, Programs
			Ins_FME1 = Ins_FME1 + '-P-001-000000-000000-0'
		elif  license_model == "Term":
			# Period Factor, Period Quantity
			if scope == "Expansion":
				Ins_FME1 = Ins_FME1 + '-P'
			elif scope == "New Implementation" or scope == "Upgrade":
				license_mapping = {"1 Year": '-L-001',"2 Years": '-K-002',"3 Years": '-H-003',"4 Years": '-F-004',"5 Years": '-E-005',"6 Years": '-D-006'}
				Ins_FME1 += license_mapping.get(attr["license_term"], '')
			# Escalation & Programs 
			#base = 4447 # base.PRODUCT_PRICE
			if base.PRODUCT_PRICE and esc_factor > 0:
				esc_perc, esc_price=escalation_calc(base.PRODUCT_PRICE, attr["license_term"], esc_factor)
				if attr["upfront_payment"]=="Yes":
					upfront_perc, upfront_price=escalation_calc(base.PRODUCT_PRICE, attr["license_term"],4)
					upfront_perc = (esc_price - upfront_price)/2
					Ins_FME1 = Ins_FME1 +'-'+str(esc_perc).zfill(6)+'-'+str(upfront_perc).zfill(6)
				elif attr["upfront_payment"]=="No":
					Ins_FME1 = Ins_FME1 +'-'+str(esc_perc).zfill(6)+'-000000'
			else:
				Ins_FME1 = Ins_FME1 + '-000000-000000'
		fme_dic['AS-UNSGHTS'] = Ins_FME1
	# FME string: AS-UNSGHTS(With Events)   = "AS-UNSGHTS-N-S-N-N-N-0-0-0-0-0-0-000-0000-0000-0000-0000-0000-0000-0000-0-A-A-Y-P-001-000000-000000"
	# This FME string is Valid Format = "AS-UNSGHTS-N-S-N-N-N-0-0-0-0-0-0-0-0000-0000-0000-0000-0000-0000-0001-0-0-1-A-A-N-P-001-000000-000000"
	if (license_model == "Perpetual" or license_model == "Term") and order_type and attr["Ins_WithEvents"]=="Yes":
		base = SqlHelper.GetFirst(""" SELECT PRODUCT_PRICE FROM products p JOIN HPS_PRODUCTS_MASTER hpm ON p.PRODUCT_CATALOG_CODE = hpm.PartNumber WHERE PRODUCT_CATALOG_CODE='AS-UNSGHTS' """)
		Ins_FME1 = 'AS-UNSGHTS'
		if scope == "New Implementation" or scope == "Upgrade":
			Ins_FME1 = Ins_FME1 + '-N'
		elif scope == "Expansion":
			Ins_FME1 = Ins_FME1 + '-M'
		if order_type == "Competitive Replacement" or order_type == "Non-Support Upgrade":
			Ins_FME1 = Ins_FME1 + '-R'
		elif order_type=='Maintenance Support Upgrade/Update (No Charge/ BGP Active)':
			Ins_FME1 = Ins_FME1 + '-N'
		else:
			Ins_FME1 = Ins_FME1 + '-S'
		# Suite Factor, Historian Factor, Conversion Factor, Base system Price:
		Ins_FME1 = Ins_FME1 + '-N-N-N-0'
		# Added 5, 10, 25, 50, 100, 250 User Packs 
		if scope == "New Implementation" or scope == "Expansion" or (scope == "Upgrade" and order_type!='Maintenance Support Upgrade/Update (No Charge/ BGP Active)'):
			Ins_FME1 = Ins_FME1 +'-'+ str(int(float(attr["Events_5"]))).zfill(1)
			Ins_FME1 = Ins_FME1 +'-'+ str(int(float(attr["Events_10"]))).zfill(1)
			Ins_FME1 = Ins_FME1 +'-'+ str(int(float(attr["Events_25"]))).zfill(1)
			Ins_FME1 = Ins_FME1 +'-'+ str(int(float(attr["Events_50"]))).zfill(1)
			Ins_FME1 = Ins_FME1 +'-'+ str(int(float(attr["Events_100"]))).zfill(1)
			Ins_FME1 = Ins_FME1 +'-'+ str(int(float(attr["Events_250"]))).zfill(3)
		elif scope == "Upgrade" and order_type=='Maintenance Support Upgrade/Update (No Charge/ BGP Active)':
			Ins_FME1 = Ins_FME1 +'-0'
			Ins_FME1 = Ins_FME1 +'-0'
			Ins_FME1 = Ins_FME1 +'-0'
			Ins_FME1 = Ins_FME1 +'-0'
			Ins_FME1 = Ins_FME1 +'-0'
			Ins_FME1 = Ins_FME1 +'-000'
		# Upgrades from Web (Used for non-events to Events), Upgrades from Basic, Upgrades from Adv/Devt, Upgrades from OI, Upgrades from Workcenter
		Ins_FME1 = Ins_FME1 + '-0000-0000-0000-0000-0000'
		# Previous Users
		if scope == "New Implementation" or (scope == "Upgrade" and order_type!='Maintenance Support Upgrade/Update (No Charge/ BGP Active)'):
			Ins_FME1 = Ins_FME1 + '-0000'
			'''n = int(float(attr["Events_Single"])) + int(float(attr["Events_5"]))*5 + int(float(attr["Events_10"]))*10 + int(float(attr["Events_25"]))*25 + int(float(attr["Events_50"]))*50 + int(float(attr["Events_100"]))*100 + int(float(attr["Events_250"]))*250
			if str(len(str(n))) > "4":
				n = str(n)[:4]
				Ins_FME1 = Ins_FME1 +'-'+ str(n).zfill(4)
			else:
				Ins_FME1 = Ins_FME1 +'-'+ str(n).zfill(4)'''
		elif scope == "Upgrade" and order_type=='Maintenance Support Upgrade/Update (No Charge/ BGP Active)':
			n = int(float(attr["Events_Single"])) + int(float(attr["Events_5"]))*5 + int(float(attr["Events_10"]))*10 + int(float(attr["Events_25"]))*25 + int(float(attr["Events_50"]))*50 + int(float(attr["Events_100"]))*100 + int(float(attr["Events_250"]))*250
			if str(len(str(n))) > "4":
				n = str(n)[:4]
				Ins_FME1 = Ins_FME1 +'-'+ str(n).zfill(4)
			else:
				Ins_FME1 = Ins_FME1 +'-'+ str(n).zfill(4)
		elif scope == "Expansion":
			e = int(float(attr["Exist_Events_Single"])) + int(float(attr["Exist_Events_5"]))*5 + int(float(attr["Exist_Events_10"]))*10 + int(float(attr["Exist_Events_25"]))*25 + int(float(attr["Exist_Events_50"]))*50 + int(float(attr["Exist_Events_100"]))*100 + int(float(attr["Exist_Events_250"]))*250
			if str(len(str(e))) > "4":
				e = str(e)[:4]
				Ins_FME1 = Ins_FME1 +'-'+ str(e).zfill(4)
			else:
				Ins_FME1 = Ins_FME1 +'-'+ str(e).zfill(4)
		# New Added Users SumUp
		if scope == "New Implementation" or (scope == "Upgrade" and order_type!='Maintenance Support Upgrade/Update (No Charge/ BGP Active)'):
			#Ins_FME1 = Ins_FME1 + '-0000'
			n = int(float(attr["Events_Single"])) + int(float(attr["Events_5"]))*5 + int(float(attr["Events_10"]))*10 + int(float(attr["Events_25"]))*25 + int(float(attr["Events_50"]))*50 + int(float(attr["Events_100"]))*100 + int(float(attr["Events_250"]))*250
			if str(len(str(n))) > "6":
				n = str(n)[:6]
				Ins_FME1 = Ins_FME1 +'-'+ str(n).zfill(6)
			else:
				Ins_FME1 = Ins_FME1 +'-'+ str(n).zfill(6)
		elif scope == "Upgrade" and order_type=='Maintenance Support Upgrade/Update (No Charge/ BGP Active)':
			Ins_FME1 = Ins_FME1 + '-000000'
		elif scope == "Expansion":
			n = int(float(attr["Events_Single"])) + int(float(attr["Events_5"]))*5 + int(float(attr["Events_10"]))*10 + int(float(attr["Events_25"]))*25 + int(float(attr["Events_50"]))*50 + int(float(attr["Events_100"]))*100 + int(float(attr["Events_250"]))*250
			if str(len(str(n))) > "6":
				n = str(n)[:6]
				Ins_FME1 = Ins_FME1 +'-'+ str(n).zfill(6)
			else:
				Ins_FME1 = Ins_FME1 +'-'+ str(n).zfill(6)
		#Ins_FME1 = Ins_FME1 + '-0-0' # This FME string '-0-0' concat is right/valid format.
		# Added 1-User Packs
		if scope == "New Implementation" or scope == "Expansion" or (scope == "Upgrade" and order_type!='Maintenance Support Upgrade/Update (No Charge/ BGP Active)'):
			Ins_FME1 = Ins_FME1 +'-'+str(int(float(attr["Events_Single"])))
		elif scope == "Upgrade" and order_type=='Maintenance Support Upgrade/Update (No Charge/ BGP Active)':
			Ins_FME1 = Ins_FME1 +'-0'
		#elif scope == "Expansion":
		#	Ins_FME1 = Ins_FME1 +'-'+str(int(float(attr["Exist_Events_Single"])))
		# Web Upgrade Tier Factor ( Used for non-events to Events), Basic Upgrade Tier Factor, Event Analysis Option Factor
		Ins_FME1 = Ins_FME1 + '-A-A-Y'
		if license_model == "Perpetual":
			# Period Factor, Period Quantity, Escalation, Programs
			Ins_FME1 = Ins_FME1 + '-P-001-000000-000000-0'
		elif  license_model == "Term":
			# Period Factor, Period Quantity
			if scope == "Expansion":
				Ins_FME1 = Ins_FME1 + '-P'
			elif scope == "New Implementation" or scope == "Upgrade":
				license_mapping = {"1 Year": '-L-001',"2 Years": '-K-002',"3 Years": '-H-003',"4 Years": '-F-004',"5 Years": '-E-005',"6 Years": '-D-006'}
				Ins_FME1 += license_mapping.get(attr["license_term"], '')
			# Escalation & Programs
			if base.PRODUCT_PRICE and esc_factor > 0:
				esc_perc, esc_price=escalation_calc(base.PRODUCT_PRICE, attr["license_term"], esc_factor)
				if attr["upfront_payment"]=="Yes":
					upfront_perc, upfront_price=escalation_calc(base.PRODUCT_PRICE, attr["license_term"],4)
					upfront_perc = (esc_price - upfront_price)/2
					Ins_FME1 = Ins_FME1 +'-'+str(esc_perc).zfill(6)+'-'+str(upfront_perc).zfill(6)
				elif attr["upfront_payment"]=="No":
					Ins_FME1 = Ins_FME1 +'-'+str(esc_perc).zfill(6)+'-000000'
			else:
				Ins_FME1 = Ins_FME1 + '-000000-000000'
		fme_dic['AS-UNSGHTS-EVENT'] = Ins_FME1
	return fme_dic