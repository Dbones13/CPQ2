import GS_GetPriceFromCPS as cps
#from GS_SC_SFDCD_STRUCTURE_OTU import dummyresponse_structure
class OTU_SystemDetails():
	def __init__(self):
		self.database_lic_parts = SqlHelper.GetList("select * from SC_CT_OTU_LICENSEDPARTS")
		self.database_nonlic_parts = SqlHelper.GetList("select * from SC_CT_OTU_NonLic_Parts")
		self.database_part_prices_len = SqlHelper.GetFirst("select  count(distinct PartNumber) as c from SC_PRICING_SESP").c
		self.database_part_prices = self.updateIntializer()
	def roundUp(self,n):
		res = int(n)
		return res if round(res,2) == round(n,2) else res+1
	def updateIntializer(self):
		d = []
		for i in range(0,self.database_part_prices_len,999):
			query = SqlHelper.GetList("select PartNumber, BasePrice from SC_PRICING_SESP ORDER BY CpqTableEntryId OFFSET "+ str(i) +" ROWS FETCH NEXT 999 ROWS ONLY")
			d += query
		return d
	def getLicPartData(self,sys_name,current_version,target_version):
		for i in self.database_lic_parts:
			if i.System_Name.ToString() == sys_name and i.Current_Version.ToString() == current_version and i.Target_Version.ToString() == target_version:
				return i
	def get_part_price(self,part):
		for price in self.database_part_prices:
			if price.PartNumber == part:
				return price.BasePrice
		else :
			return '0.0'
	def get_nonLicensedparts(self,sys_name,msid_row):
		parts = []
		for i in self.database_nonlic_parts:
			if i.System_Name == sys_name:
				a = {}
				a['Part'] = i.Part_Number
				price = self.get_part_price(i.Part_Number)
				a['Price'] = price
				a['CurrentVersion'] = ''
				a['TargetVersion'] = ''
				if i.Part_Id == 'DVM1':
					serverRedundancy = 1 if msid_row.Product.Attr('EP_DVMR01_DVMC_OTU_SESP').GetValue() == "Yes" else 0
					baseModel = 0
					if msid_row.Product.Attr('EP_DVML01_DVMC_OTU_SESP').GetValue() != '':
						baseModel = 1 if float(msid_row.Product.Attr('EP_DVML01_DVMC_OTU_SESP').GetValue()) > 0 else 0
					dvmQty = int(baseModel) + int(serverRedundancy) + int(msid_row.Product.Attr('IntExplClients_DVMC_OTU_SESP').GetValue())
					a['Qty'] = str(dvmQty)
				elif i.Part_Id == 'EOP1':
					a['Qty'] = msid_row.Product.Attr('MZSQLCL4_EOPC_OTU_SESP').GetValue()
				elif i.Part_Id == "OTS1":
					a['Qty'] = msid_row.Product.Attr('MZSQLCL4_OTSC_OTU_SESP').GetValue()
				elif i.Part_Id == "EXP2":
					a['Qty'] = msid_row.Product.Attr('EPBRWE06_EXPC_OTU_SESP').GetValue()
				elif i.Part_Id == "EXP3":
					a['Qty'] = msid_row.Product.Attr('EPBRVE06_EXPC_OTU_SESP').GetValue()
				elif i.Part_Id == "EXP4":
					a['Qty'] = msid_row.Product.Attr('EPBRSE06_EXPC_OTU_SESP').GetValue()
				elif i.Part_Id == "EXP7":
					a['Qty'] = 2 if msid_row.Product.Attr('ServerRedundancy_EXPC_OTU_SESP').GetValue() == "Yes" else 1
				elif i.Part_Id == "EXP8":
					a['Qty'] = round(float(msid_row.Product.Attr('ConsoleStations_EXPC_OTU_SESP').GetValue()) + float(msid_row.Product.Attr('FlexStations_EXPC_OTU_SESP').GetValue()))
				elif i.Part_Id == "EXP9":
					a['Qty'] = 1 if msid_row.Product.Attr('ExpDVMIntr_EXPC_OTU_SESP').GetValue() == "Yes" else 0
				elif i.Part_Id == "EXP10":
					a['Qty'] = (2 if msid_row.Product.Attr('ServerRedundancy_EXPC_OTU_SESP').GetValue() == "Yes" else 1) + float(msid_row.Product.Attr('ConsoleStations_EXPC_OTU_SESP').GetValue()) + float(msid_row.Product.Attr('FlexStations_EXPC_OTU_SESP').GetValue())
				elif i.Part_Id == "ESS2":
					a['Qty'] = round(float(msid_row.Product.Attr('EPBRWE06_ESSC_OTU_SESP').GetValue()))
				elif i.Part_Id == "ESS3":
					a['Qty'] = round(float(msid_row.Product.Attr('EPBRVE06_ESSC_OTU_SESP').GetValue()))
				elif i.Part_Id == "ESS4":
					a['Qty'] = round(float(msid_row.Product.Attr('EPBRSE06_ESSC_OTU_SESP').GetValue()))
				elif i.Part_Id == 'FDM2':
					a['Qty'] = float(msid_row.Product.Attr('FDMClients_FDMC_OTU_SESP').GetValue()) + 1
				elif i.Part_Id == 'ESVT2':
					a['Qty'] =  msid_row.Product.Attr('EPBRWE06_ESTVC_OTU_SESP').GetValue()
				elif i.Part_Id == 'ESVT3':
					a['Qty'] =  msid_row.Product.Attr('EPBRVE06_ESTVC_OTU_SESP').GetValue()
				elif i.Part_Id == 'ESVT4':
					a['Qty'] =  msid_row.Product.Attr('EPBRSE06_ESTVC_OTU_SESP').GetValue()
				elif i.Part_Id == 'ESVT6':
					a['Qty'] = round(float(msid_row.Product.Attr('ConsoleStations_ESTVC_OTU_SESP').GetValue()) + float(msid_row.Product.Attr('flexStations_ESTVC_OTU_SESP').GetValue()) + (2 if msid_row.Product.Attr('ServerRedundancy_ESTVC_OTU_SESP').GetValue() == "Yes" else 1))
				elif i.Part_Id == 'ESVT7':
					a['Qty'] = 1 if msid_row.Product.Attr('ExpDVMIntr_ESTVC_OTU_SESP').GetValue() == "Yes" else 0
				elif i.Part_Id == 'ESVT8':
					a['Qty'] = 2 if msid_row.Product.Attr('ServerRedundancy_ESTVC_OTU_SESP').GetValue() == "Yes" else 1
				elif i.Part_Id == 'ESVT9':
					a['Qty'] = round(float(msid_row.Product.Attr('ConsoleStations_ESTVC_OTU_SESP').GetValue()) + float(msid_row.Product.Attr('flexStations_ESTVC_OTU_SESP').GetValue()))
				elif i.Part_Id == 'SS3':
					a['Qty'] = round(float(msid_row.Product.Attr('EPBRVE06_SSC_OTU_SESP').GetValue()))
				elif i.Part_Id == 'SS4':
					a['Qty'] = round(float(msid_row.Product.Attr('EPBRSE06_SSC_OTU_SESP').GetValue()))
				elif i.Part_Id == 'SS5':
					a['Qty'] = round(float(msid_row.Product.Attr('EPBRWE06_SSC_OTU_SESP').GetValue()))
				elif i.Part_Id == 'TPS1':
					a['Qty'] = round(float(msid_row.Product.Attr('EPCONTPS_TPSC_OTU_SESP').GetValue()))
					price = self.get_part_price('MZ-SQLCL4')
					a['Price'] = price
				elif i.Part_Id == 'TPS2':
					a['Qty'] = round(float(msid_row.Product.Attr('EPABV020_TPSC_OTU_SESP').GetValue()))
					price = self.get_part_price('EP-COAS16')
					a['Price'] = price
				elif i.Part_Id == 'TPS3':
					a['Qty'] = round(float(msid_row.Product.Attr('EPCONTPS_TPSC_OTU_SESP').GetValue()))
					price = self.get_part_price('EP-COAW10')
					a['Price'] = price
				elif i.Part_Id == 'HS1':
					a['Qty'] = 1
				elif i.Part_Id == 'HS3':
					a['Qty'] = round(float(msid_row.Product.Attr('MZSQLCL4_HSC_OTU_SESP').GetValue()))
				elif i.Part_Id == 'HS4':
					a['Qty'] = round(float(msid_row.Product.Attr('EPBRVE06_HSC_OTU_SESP').GetValue()))
				elif i.Part_Id == 'HS5':
					a['Qty'] = round(float(msid_row.Product.Attr('EPBRSE06_HSC_OTU_SESP').GetValue()))
				elif i.Part_Id == 'HS6':
					a['Qty'] = round(float(msid_row.Product.Attr('EPBRWE06_HSC_OTU_SESP').GetValue()))
				elif i.Part_Id == 'OTS3':
					a['Qty'] = round(float(msid_row.Product.Attr('EPBRWE06_OTSC_OTU_SESP').GetValue()))
				elif i.Part_Id == 'OTS4':
					a['Qty'] = round(float(msid_row.Product.Attr('EPBRSE06_OTSC_OTU_SESP').GetValue()))
				elif i.Part_Id == 'OTS5':
					a['Qty'] = round(float(msid_row.Product.Attr('EPBRVE06_OTSC_OTU_SESP').GetValue()))
				else:
					a['Qty'] = i.Qty
				a['IsLicensed'] = 'False'
				parts.append(a)
		else:
			return parts
	def getAddationalParts(self,container,ChildProduct):
		con_parts = ChildProduct.GetContainerByName(container)
		addationalParts = []
		for i in con_parts.Rows:
			if (i['Qty'] is not None and i['Qty'] != '' and i['Qty'] != 0 and str(i['Qty']).isdigit()) :
				if float(i['Qty']) > 0:
					d = {}
					price = self.get_part_price(i['Part Number'])
					d['Price'] = price
					d['Qty'] = i['Qty']
					d['Part'] = i['Part Number']
					d['CurrentVersion'] = ""
					d['TargetVersion'] = ""
					d['IsLicensed'] = 'False'
					addationalParts.append(d)
		return addationalParts
	def get_dvm_parts(self,ChildProduct,msid_row):
		DVM_Cam_Qua = ChildProduct.Attr("Cameras_DVMC_OTU_SESP").GetValue()
		dvm_parts = []
		dvm_current_version = ChildProduct.Attr("CurrentVer_DVMC_OTU_SESP").GetValue()
		dvm_target_version = ChildProduct.Attr("TargetVer_DVMC_OTU_SESP").GetValue()
		#Licensed Part
		data = self.getLicPartData('DVM',dvm_current_version,dvm_target_version)
		dvm_lic_part = {}
		if data is not None:
			round_up_qty = float(DVM_Cam_Qua)
			if round_up_qty > 0:
				price = self.get_part_price(data.Part_Number)
				dvm_lic_part['Part'] = data.Part_Number
				dvm_lic_part['Qty'] = round_up_qty
				dvm_lic_part['Price'] = price
				dvm_lic_part['IsLicensed'] = 'True'
				dvm_lic_part['CurrentVersion'] = dvm_current_version
				dvm_lic_part['TargetVersion'] = dvm_target_version
				dvm_parts.append(dvm_lic_part)
			# Non Licensed Part
		non_lcensed_parts_data = self.get_nonLicensedparts('DVM',msid_row)
		if non_lcensed_parts_data is not None:
			for non_part in non_lcensed_parts_data:
				if len(dvm_lic_part) > 0:
					dvm_parts.append(non_part)
		return dvm_parts
	def get_eop_parts(self,ChildProduct,msid_row):
		eop_current_version = ChildProduct.Attr("CurrentVer_EOPC_OTU_SESP").GetValue()
		eop_target_version = ChildProduct.Attr("TargetVer_EOPC_OTU_SESP").GetValue()
		# EOP Licensed Parts
		eop_lic_parts = self.getLicPartData('EOP',eop_current_version,eop_target_version)
		eop_parts = []
		eop_lic_parts_1 = ['EP-UPANR2','EP-UPANR3','EP-UPANRX']#To check MZ-SQLCL4 eligibility for system details
		eop_lic_parts_2 = ['EP-UPANR1','EP-UPANR2','EP-UPANR3','EP-UPANRX']#To check EP-PKS520-ESD eligibility for system details
		base_unit_eop = ChildProduct.Attr('BaseUnits_EOPC_OTU_SESP').GetValue()
		eop_lic_part = {}
		if round(float(base_unit_eop)) > 0:
			if eop_lic_parts is not None:
				price = self.get_part_price(eop_lic_parts.Part_Number)
				eop_lic_part['Price'] = price
				eop_lic_part['Part'] = eop_lic_parts.Part_Number
				eop_lic_part['Qty'] = str(round(float(base_unit_eop)))
				eop_lic_part['IsLicensed'] = 'True'
				eop_lic_part['CurrentVersion'] = eop_current_version
				eop_lic_part['TargetVersion'] = eop_target_version
				eop_parts.append(eop_lic_part)
		# EOP Non Licensed Parts
		eop_non_lic_parts = self.get_nonLicensedparts('EOP',msid_row)
		if eop_non_lic_parts is not None:
			for non_part in eop_non_lic_parts:
				if len(eop_lic_part)>0:
					if eop_lic_parts.Part_Number  in eop_lic_parts_1 and non_part['Part'] == 'MZ-SQLCL4':
						eop_parts.append(non_part)
					if eop_lic_parts.Part_Number  in eop_lic_parts_2 and non_part['Part'] == 'EP-PKS520-ESD':
						eop_parts.append(non_part)
		eop_addParts = self.getAddationalParts("PartNum_EOPC_OTU_SESP",ChildProduct)
		eop_parts = eop_parts + eop_addParts
		return eop_parts
	def get_hs_parts(self,ChildProduct,msid_row):
		HS_current_version = ChildProduct.Attr("CurrentVer_HSC_OTU_SESP").GetValue()
		HS_target_version = ChildProduct.Attr("TargetVer_HSC_OTU_SESP").GetValue()
		HS_points = ChildProduct.Attr("ExpHSPoints_HSC_OTU_SESP").GetValue()
		HS_EPBRM520ESD_Dep = ["EP-BRWE06","EP-BRVE06","EP-BRSE06"]
		Server_Redundancy = 2 if ChildProduct.Attr('ServerRedundancy_HSC_OTU_SESP').GetValue() == "Yes" else 1
		HS_Stations = float(ChildProduct.Attr("Stations_HSC_OTU_SESP").GetValue())
		# HS Licensed Parts
		HS_lic_parts = self.getLicPartData('HS',HS_current_version,HS_target_version)
		HS_parts = []
		HS_lic_part = {}
		if HS_lic_parts is not None:
			qty = 65 + round(((float(HS_points)*6)/100.0)) * Server_Redundancy + HS_Stations*15
			#qty = self.roundUp(65 + ((float(HS_points)*6)/100.0))
			if qty > 0:
				price = self.get_part_price(HS_lic_parts.Part_Number)
				HS_lic_part['Price'] = price
				HS_lic_part['Part'] = HS_lic_parts.Part_Number
				HS_lic_part['Qty'] = qty
				HS_lic_part['IsLicensed'] = 'True'
				HS_lic_part['CurrentVersion'] = HS_current_version
				HS_lic_part['TargetVersion'] = HS_target_version
				HS_parts.append(HS_lic_part)
		# HS Non Licensed Part
		HS_non_lcensed_parts_data = self.get_nonLicensedparts('HS',msid_row)
		if HS_non_lcensed_parts_data is not None:
			EBR_Parts = self.get_ebr_parts(ChildProduct)
			HS_NONLIC_Dep = [non_part['Part'] for non_part in EBR_Parts if round(float(non_part['Qty'])) > 0]
			EPBRM520ESD_Flag = False
			for depPart in HS_EPBRM520ESD_Dep:
				if depPart in HS_NONLIC_Dep:
					EPBRM520ESD_Flag = True
					break
			for non_part in HS_non_lcensed_parts_data:
				if non_part['Part'] == "EP-BRM520-ESD":
					if EPBRM520ESD_Flag and len(HS_lic_part) > 0:
						HS_parts.append(non_part)
				elif non_part['Part'] == "MZ-SQLCL4" or non_part["Part"] == "EP-HME520-ESD":
					if len(HS_lic_part) > 0:
						HS_parts.append(non_part)
				elif non_part['Part'] == 'EP-BRWE06' or non_part['Part'] == 'EP-BRVE06' or non_part['Part'] == 'EP-BRSE06':
					HS_parts.append(non_part)
				else:
					pass
		HS_addParts = self.getAddationalParts("ModelNum_HSC_OTU_SESP",ChildProduct)
		HS_parts = HS_parts + HS_addParts
		return HS_parts
	def get_ots_parts(self,ChildProduct,msid_row):
		OTS_current_version = ChildProduct.Attr("CurrentVer_OTSC_OTU_SESP").GetValue()
		OTS_target_version = ChildProduct.Attr("TargetVer_OTSC_OTU_SESP").GetValue()
		# OTS Licensed Parts
		OTS_lic_parts = self.getLicPartData('OTS',OTS_current_version,OTS_target_version)
		OTS_lic_parts_1 = ['EP-UPANR2','EP-UPANR3','EP-UPANRX']
		OTS_EPBRM520ESD_Dep = ["EP-BRWE06","EP-BRVE06","EP-BRSE06"]
		OTS_parts = []
		OTS_lic_part = {}
		if OTS_lic_parts is not None:
			price = self.get_part_price(OTS_lic_parts.Part_Number)
			OTS_lic_part['Part'] = OTS_lic_parts.Part_Number
			OTS_lic_part["Price"] = price
			OTS_lic_part['Qty'] = round(25)
			OTS_lic_part['IsLicensed'] = 'True'
			OTS_lic_part['CurrentVersion'] = OTS_current_version
			OTS_lic_part['TargetVersion'] = OTS_target_version
			OTS_parts.append(OTS_lic_part)
		# OTS Non Licensed Part
		OTS_non_lcensed_parts_data = self.get_nonLicensedparts('OTS',msid_row)
		if OTS_non_lcensed_parts_data is not None:
			EBR_Parts = self.get_ebr_parts(ChildProduct)
			OTS_NONLIC_Dep = [non_part['Part'] for non_part in EBR_Parts if round(float(non_part['Qty'])) > 0]
			EPBRM520ESD_Flag = False
			for depPart in OTS_EPBRM520ESD_Dep:
				if depPart in OTS_NONLIC_Dep:
					EPBRM520ESD_Flag = True
					break
			for non_part in OTS_non_lcensed_parts_data:
				if non_part['Part'] == 'MZ-SQLCL4':
					if len(OTS_lic_part) > 0:
						if OTS_lic_parts.Part_Number  in OTS_lic_parts_1:
							OTS_parts.append(non_part)
				elif non_part['Part'] == "EP-PKS520-ESD":
					if len(OTS_lic_part) > 0:
						OTS_parts.append(non_part)
				elif non_part['Part'] == "EP-BRM520-ESD":
					if EPBRM520ESD_Flag and len(OTS_lic_part) > 0:
						OTS_parts.append(non_part)
				else:
					OTS_parts.append(non_part)
		OTS_addParts = self.getAddationalParts("PartNum_OTSC_OTU_SESP",ChildProduct)
		OTS_parts = OTS_parts + OTS_addParts
		return OTS_parts
	def get_experion_parts(self,ChildProduct,msid_row):
		EXP_current_version = ChildProduct.Attr("CurrentVer_EXPC_OTU_SESP").GetValue()
		EXP_target_version = ChildProduct.Attr("TargetVer_EXPC_OTU_SESP").GetValue()
		EXP_SCADA = ChildProduct.Attr("ExpSCADAPoints_EXPC_OTU_SESP").GetValue()
		EXP_PROCESS = ChildProduct.Attr("ExpProcessPoints_EXPC_OTU_SESP").GetValue()
		EXP_CONSOLE = ChildProduct.Attr("ConsoleStations_EXPC_OTU_SESP").GetValue()
		EXP_FLEX = ChildProduct.Attr("FlexStations_EXPC_OTU_SESP").GetValue()
		EXP_lic_parts_1 = ['EP-UPANR2','EP-UPANR3','EP-UPANRX']
		EXP_EPBRM520ESD_Dep = ["EP-BRWE06","EP-BRVE06","EP-BRSE06"]
		Server_Redundancy = 2 if ChildProduct.Attr('ServerRedundancy_EXPC_OTU_SESP').GetValue() == "Yes" else 1
		F = float(ChildProduct.Attr("NoOfIntExpTps_EXPC_OTU_SESP").GetValue())*100
		# EXP Licensed Parts
		EXP_lic_parts = self.getLicPartData('Experion',EXP_current_version,EXP_target_version)
		EXP_parts = []
		EXP_lic_part = {}
		if EXP_lic_parts is not None:
			#qty = 65 + ((float(EXP_SCADA) - 50) if float(EXP_SCADA)>=50 else 0) + ((float(EXP_PROCESS) - 50) if float(EXP_PROCESS)>=50 else 0 ) + float(EXP_CONSOLE) + float(EXP_FLEX)
			qty = (65+(float(EXP_PROCESS)*5)/100*Server_Redundancy +(float(EXP_SCADA)*3)/100*Server_Redundancy+float(EXP_FLEX)*35+float(EXP_CONSOLE)*140 + F)
			if qty > 0:
				price = self.get_part_price(EXP_lic_parts.Part_Number)
				EXP_lic_part['Price'] = price
				EXP_lic_part['Part'] = EXP_lic_parts.Part_Number
				EXP_lic_part['Qty'] = round(qty)
				EXP_lic_part['IsLicensed'] = 'True'
				EXP_lic_part['CurrentVersion'] = EXP_current_version
				EXP_lic_part['TargetVersion'] = EXP_target_version
				EXP_parts.append(EXP_lic_part)
			# EXP Non Licensed Part
		EXP_non_lcensed_parts_data = self.get_nonLicensedparts('Experion',msid_row)
		if EXP_non_lcensed_parts_data is not None:
			EBR_Parts = self.get_ebr_parts(ChildProduct)
			EXP_NONLIC_Dep = [non_part['Part'] for non_part in EBR_Parts if round(float(non_part['Qty'])) > 0]
			EPBRM520ESD_Flag = False
			for depPart in EXP_EPBRM520ESD_Dep:
				if depPart in EXP_NONLIC_Dep:
					EPBRM520ESD_Flag = True
					break
			for non_part in EXP_non_lcensed_parts_data:
				if non_part['Part'] == 'EP-PKS520-ESD':
					if len(EXP_lic_part) > 0:
						EXP_parts.append(non_part)
				elif non_part['Part'] == 'EP-BRWE06' or non_part['Part'] == 'EP-BRVE06' or non_part['Part'] == 'EP-BRSE06':
					EXP_parts.append(non_part)
				elif non_part['Part'] == 'EP-BRM520-ESD':
					if EPBRM520ESD_Flag and len(EXP_lic_part) > 0:
						EXP_parts.append(non_part)
				elif non_part['Part'] == 'MZ-SQLCL4' or non_part['Part'] == 'EP-COAW10' or non_part['Part'] == 'EP-COAS16':
					if len(EXP_lic_part) > 0:
						if EXP_lic_part["Part"] in EXP_lic_parts_1:
							EXP_parts.append(non_part)
				elif non_part['Part'] == 'EP-IADDVM':
					pass
				else:
					EXP_parts.append(non_part)
		EXP_addParts = self.getAddationalParts("PartNum_EXPC_OTU_SESP",ChildProduct)
		UPDATED_EXP_addParts = []
		for addPart in EXP_addParts:
			if addPart["Part"] == "EP-T09CAL":
				if EXP_current_version not in ["R510","R511","R501"]:
					UPDATED_EXP_addParts.append(addPart)
			elif addPart["Part"] == "EP-MSVS10":
				if EXP_current_version in ["R432","R400","R410","R311","R301","R210","R201","R10x"]:
					UPDATED_EXP_addParts.append(addPart)
			else:
				UPDATED_EXP_addParts.append(addPart)
		EXP_parts = EXP_parts + UPDATED_EXP_addParts
		return EXP_parts
	def get_eServer_Parts(self,ChildProduct,msid_row):
		ESS_current_version = ChildProduct.Attr("CurrentVer_ESSC_OTU_SESP").GetValue()
		ESS_target_version = ChildProduct.Attr("TargetVer_ESSC_OTU_SESP").GetValue()
		ESS_PAU = ChildProduct.Attr("eServerPAU_ESSC_OTU_SESP").GetValue()
		ESS_EPBRM520ESD_Dep = ["EP-BRWE06","EP-BRVE06","EP-BRSE06"]
		# ESS Licensed Parts
		ESS_lic_parts = self.getLicPartData('Eserver',ESS_current_version,ESS_target_version)
		ESS_parts = []
		ESS_lic_part = {}
		if ESS_lic_parts is not None:
			qty = round(25 + (float(ESS_PAU)*10))
			if qty > 0:
				price = self.get_part_price(ESS_lic_parts.Part_Number)
				ESS_lic_part['Price'] = price
				ESS_lic_part['Part'] = ESS_lic_parts.Part_Number
				#ESS_lic_part['Qty'] = 25 + (int(float(ESS_PAU))*10)
				ESS_lic_part['Qty'] = qty
				ESS_lic_part['IsLicensed'] = 'True'
				ESS_lic_part['CurrentVersion'] = ESS_current_version
				ESS_lic_part['TargetVersion'] = ESS_target_version
				ESS_parts.append(ESS_lic_part)
			# ESS Non Licensed Part
		ESS_non_lcensed_parts_data = self.get_nonLicensedparts('ESS',msid_row)
		if ESS_non_lcensed_parts_data is not None:
			EBR_Parts = self.get_ebr_parts(ChildProduct)
			ESS_NONLIC_Dep = [non_part['Part'] for non_part in EBR_Parts if round(float(non_part['Qty'])) > 0]
			EPBRM520ESD_Flag = False
			for depPart in ESS_EPBRM520ESD_Dep:
				if depPart in ESS_NONLIC_Dep:
					EPBRM520ESD_Flag = True
					break
			for non_part in ESS_non_lcensed_parts_data:
				if non_part['Part'] == 'EP-PKS520-ESD':
					if len(ESS_lic_part)>0:
						ESS_parts.append(non_part)
				elif non_part['Part'] == 'EP-BRM520-ESD':
					if EPBRM520ESD_Flag and len(ESS_lic_part) > 0:
						ESS_parts.append(non_part)
				elif non_part['Part'] == 'EP-BRWE06' or non_part['Part'] == 'EP-BRVE06' or non_part['Part'] == 'EP-BRSE06':
					ESS_parts.append(non_part)
				else:
					pass
		return ESS_parts
	def get_fdm_parts(self,ChildProduct,msid_row):
		FDM_current_version = ChildProduct.Attr("CurrentVer_FDMC_OTU_SESP").GetValue()
		FDM_target_version = ChildProduct.Attr("TargetVer_FDMC_OTU_SESP").GetValue()
		FDM_serviceDevicePoints = ChildProduct.Attr("ServiceDevicePoints_FDMC_OTU_SESP").GetValue()
		FDM_AuditTrailDevice = ChildProduct.Attr("AduitTrailDevicePoints_FDMC_OTU_SESP").GetValue()
		FDM_RciInterfaces = ChildProduct.Attr("RCIIntefaces_FDMC_OTU_SESP").GetValue()
		FDM_clients = ChildProduct.Attr("FDMClients_FDMC_OTU_SESP").GetValue()
		FDM_MuxInterfacesV1 = ChildProduct.Attr("MUXInterfaces_V1_FDMC_OTU_SESP").GetValue()
		FDM_MuxInterfacesV2 = ChildProduct.Attr("MUXInterfaces_V2_FDMC_OTU_SESP").GetValue()
		#FDM Licensed Parts
		FDM_lic_parts = self.getLicPartData('FDM',FDM_current_version,FDM_target_version)
		FDM_Parts = []
		FDM_lic_part = {}
		if FDM_lic_parts is not None:
			qty = round(50 + (float(FDM_serviceDevicePoints) * 0.22) + (float(FDM_AuditTrailDevice) * 0.22) + (float(FDM_RciInterfaces) * 31) + (float(FDM_clients) * 17) + (float(FDM_MuxInterfacesV1) * 14) + (float(FDM_MuxInterfacesV2) * 14))
			if qty > 0:
				price = self.get_part_price(FDM_lic_parts.Part_Number)
				FDM_lic_part['Price'] = price
				FDM_lic_part['Part'] = FDM_lic_parts.Part_Number
				FDM_lic_part['Qty'] = qty
				FDM_lic_part['IsLicensed'] = 'True'
				FDM_lic_part['CurrentVersion'] = FDM_current_version
				FDM_lic_part['TargetVersion'] = FDM_target_version
				FDM_Parts.append(FDM_lic_part)
		FDM_non_lcensed_parts_data = self.get_nonLicensedparts('FDM',msid_row)
		if FDM_non_lcensed_parts_data is not None:
			for FDM_NONLIC_Part in FDM_non_lcensed_parts_data:
				if FDM_NONLIC_Part['Part'] == "HC-UPGCLN":
					if float(ChildProduct.Attr('FDMBaseLic_FDMC_OTU_SESP').GetValue()) > 0 :
						FDM_Parts.append(FDM_NONLIC_Part)
					else:
						pass
				elif FDM_NONLIC_Part['Part'] == "HC-HCM520-ESD":
					if len(FDM_lic_part) > 0:
						FDM_Parts.append(FDM_NONLIC_Part)
				else:
					FDM_Parts.append(FDM_NONLIC_Part)
		return FDM_Parts
	def get_simulation_parts(self,ChildProduct,msid_row):
		SS_current_version = ChildProduct.Attr("CurrentVer_SSC_OTU_SESP").GetValue()
		SS_target_version = ChildProduct.Attr("TargetVer_SSC_OTU_SESP").GetValue()
		SS_lic_parts = self.getLicPartData('Simulation',SS_current_version,SS_target_version)
		SS_EPBRM520ESD_Dep = ["EP-BRWE06","EP-BRVE06","EP-BRSE06"]
		SS_parts = []
		SS_lic_part = {}
		if SS_lic_parts is not None:
			price = self.get_part_price(SS_lic_parts.Part_Number)
			SS_lic_part['Price'] = price
			SS_lic_part['Part'] = SS_lic_parts.Part_Number
			SS_lic_part['Qty'] = 200
			SS_lic_part['CurrentVersion'] = SS_current_version
			SS_lic_part['TargetVersion'] = SS_target_version
			SS_lic_part['IsLicensed'] = 'True'
			SS_parts.append(SS_lic_part)
		SS_non_lcensed_parts_data = self.get_nonLicensedparts('SS',msid_row)
		if SS_non_lcensed_parts_data is not None:
			EBR_Parts = self.get_ebr_parts(ChildProduct)
			SS_NONLIC_Dep = [non_part['Part'] for non_part in EBR_Parts if round(float(non_part['Qty'])) > 0]
			EPBRM520ESD_Flag = False
			for depPart in SS_EPBRM520ESD_Dep:
				if depPart in SS_NONLIC_Dep:
					EPBRM520ESD_Flag = True
					break
			for non_part in SS_non_lcensed_parts_data:
				if non_part['Part'] == 'EP-PKS520-ESD':
					if len(SS_lic_part) > 0:
						SS_parts.append(non_part)
				elif non_part['Part'] == 'EP-BRWE06' or non_part['Part'] == 'EP-BRVE06' or non_part['Part'] == 'EP-BRSE06':
					SS_parts.append(non_part)
				elif non_part['Part'] == 'EP-BRM520-ESD':
					if EPBRM520ESD_Flag and len(SS_lic_part) > 0:
						SS_parts.append(non_part)
				else:
					SS_parts.append(non_part)
		return SS_parts
	def get_tps_parts(self,ChildProduct,msid_row):
		TPS_parts = []
		TPS_non_lcensed_parts_data = self.get_nonLicensedparts('TPS',msid_row)
		TPS_parts += TPS_non_lcensed_parts_data
		tps = ["EPASP020_TPSC_OTU_SESP","EPRGC020_TPSC_OTU_SESP","EPRNW020_TPSC_OTU_SESP","EPFLT020_TPSC_OTU_SESP","EPMDS020_TPSC_OTU_SESP","EPGPT020_TPSC_OTU_SESP","EPCLS020_TPSC_OTU_SESP","EPABV020_TPSC_OTU_SESP","EPDSS020_TPSC_OTU_SESP","EPCONTPS_TPSC_OTU_SESP","EPSTAC10_TPSC_OTU_SESP","EPSTAC05_TPSC_OTU_SESP","EPSTAC01_TPSC_OTU_SESP"]
		for i in tps:
			splited = str(i.split('_')[0])[0:2] + '-'+ str(i.split('_')[0])[2:]
			price = self.get_part_price(splited)
			if ChildProduct.Attr(i).GetValue() != '':
				if round(float(ChildProduct.Attr(i).GetValue())) > 0:
					tps_UE_Parts = {}
					tps_UE_Parts['Part'] = splited
					tps_UE_Parts['Qty'] = round(float(ChildProduct.Attr(i).GetValue()))
					tps_UE_Parts['Price'] = price
					tps_UE_Parts['CurrentVersion'] = ''
					tps_UE_Parts['TargetVersion'] = ''
					tps_UE_Parts['IsLicensed'] = 'False'
					TPS_parts.append(tps_UE_Parts)
		return TPS_parts
	def get_esvt_parts(self,ChildProduct,msid_row):
		ESVT_current_version = ChildProduct.Attr("CurrentVer_ESTVC_OTU_SESP").GetValue()
		ESVT_target_version = ChildProduct.Attr("TargetVer_ESTVC_OTU_SESP").GetValue()
		ESVT_SCADA = ChildProduct.Attr("ExpSCADAPoints_ESTVC_OTU_SESP").GetValue()
		ESVT_PROCESS = ChildProduct.Attr("ExpProcessPoints_ESTVC_OTU_SESP").GetValue()
		ESVT_CONSOLE = ChildProduct.Attr("ConsoleStations_ESTVC_OTU_SESP").GetValue()
		ESVT_FLEX = ChildProduct.Attr("flexStations_ESTVC_OTU_SESP").GetValue()
		Server_Redundancy = 2 if ChildProduct.Attr('ServerRedundancy_ESTVC_OTU_SESP').GetValue() == "Yes" else 1
		ESVT_lic_parts_1 = ['EP-UPANR2','EP-UPANR3','EP-UPANRX']
		ESVT_EPBRM520ESD_Dep = ["EP-BRWE06","EP-BRVE06","EP-BRSE06"]
		evst = ["EPDSS020_ESTVC_OTU_SESP","EPMDS020_ESTVC_OTU_SESP","EPGPT020_ESTVC_OTU_SESP","EPRNW020_ESTVC_OTU_SESP","EPCLS020_V1_ESTVC_OTU_SESP","EPASP020_V1_ESTVC_OTU_SESP","EPFLT020_ESTVC_OTU_SESP","EPRGC020_ESTVC_OTU_SESP",'EPABV020_ESTVC_OTU_SESP',"EPASP020_V2_ESTVC_OTU_SESP","EPCLS020_V2_ESTVC_OTU_SESP"]
		# ESVT Licensed Parts
		ESVT_lic_parts = self.getLicPartData('ESVT',ESVT_current_version,ESVT_target_version)
		ESVT_parts = []
		ESVT_lic_part = {}
		F = float(ChildProduct.Attr("NoOfIntExpTps_ESTVC_OTU_SESP").GetValue())*100
		if ESVT_lic_parts is not None:
			#qty = round(65 + ((float(ESVT_SCADA) - 50) if float(ESVT_SCADA)>=50 else 0) + ((float(ESVT_PROCESS) - 50) if float(ESVT_PROCESS)>=50 else 0) + float(ESVT_CONSOLE))
			qty = (65+(float(ESVT_PROCESS)*5)/100*Server_Redundancy +(float(ESVT_SCADA)*3)/100*Server_Redundancy+float(ESVT_FLEX)*35+float(ESVT_CONSOLE)*140 + F)
			if qty > 0:
				price = self.get_part_price(ESVT_lic_parts.Part_Number)
				ESVT_lic_part['Price'] = price
				ESVT_lic_part['Part'] = ESVT_lic_parts.Part_Number
				ESVT_lic_part['Qty'] = qty
				ESVT_lic_part['CurrentVersion'] = ESVT_current_version
				ESVT_lic_part['TargetVersion'] = ESVT_target_version
				ESVT_lic_part['IsLicensed'] = 'True'
				ESVT_parts.append(ESVT_lic_part)
		# ESVT Non Licensed Part
		ESVT_non_lcensed_parts_data = self.get_nonLicensedparts('ESVT',msid_row)
		if ESVT_non_lcensed_parts_data is not None:
			EBR_Parts = self.get_ebr_parts(ChildProduct)
			ESVT_NONLIC_Dep = [non_part['Part'] for non_part in EBR_Parts if round(float(non_part['Qty'])) > 0]
			EPBRM520ESD_Flag = False
			for depPart in ESVT_EPBRM520ESD_Dep:
				if depPart in ESVT_NONLIC_Dep:
					EPBRM520ESD_Flag = True
					break
			for non_part in ESVT_non_lcensed_parts_data:
				if non_part['Part'] == 'EP-PKS520-ESD':
					if len(ESVT_lic_part) > 0:
						ESVT_parts.append(non_part)
				elif non_part['Part'] == 'EP-BRWE06' or non_part['Part'] == 'EP-BRVE06' or non_part['Part'] == 'EP-BRSE06':
					ESVT_parts.append(non_part)
				elif non_part['Part'] == 'EP-BRM520-ESD':
					if EPBRM520ESD_Flag and len(ESVT_lic_part) > 0:
						ESVT_parts.append(non_part)
				elif non_part['Part'] == 'MZ-SQLCL4' or non_part['Part'] == 'EP-COAW10' or non_part['Part'] == 'EP-COAS16':
					if len(ESVT_lic_part) > 0:
						if ESVT_lic_part["Part"] in ESVT_lic_parts_1:
							ESVT_parts.append(non_part)
				else:
					ESVT_parts.append(non_part)
		for i in evst:
			splited = str(i.split('_')[0])[0:2] + '-'+ str(i.split('_')[0])[2:]
			price = self.get_part_price(splited)
			if ChildProduct.Attr(i).GetValue() != '':
				if float(ChildProduct.Attr(i).GetValue()) > 0:
					ESVT_UE_parts = {}
					ESVT_UE_parts['Part'] = splited
					ESVT_UE_parts['Qty'] = round(float(ChildProduct.Attr(i).GetValue()))
					ESVT_UE_parts['Price'] = price
					ESVT_UE_parts['CurrentVersion'] = ''
					ESVT_UE_parts['TargetVersion'] = ''
					ESVT_UE_parts['IsLicensed'] = 'False'
					ESVT_parts.append(ESVT_UE_parts)
		ESVT_addParts = self.getAddationalParts("PartNum_ESTVC_OTU_SESP",ChildProduct)
		ESVT_parts = ESVT_parts + ESVT_addParts
		return ESVT_parts
	def get_tpn_parts(self,ChildProduct,msid_row):
		tpn = {"MPCLMB1AR_TPNC_OTU_SESP":"MP-CLMB1AR","MPCLMB1AUN_TPNC_OTU_SESP":'MP-CLMB1AUN', "MPCLMB1BR_TPNC_OTU_SESP":"MP-CLMB1BR" ,"MPCLMB1BUN_TPNC_OTU_SESP":"MP-CLMB1BUN","MPCLMM1AR_TPNC_OTU_SESP":"MP-CLMM1AR" , "MPCLMM1AUN_TPNC_OTU_SESP":"MP-CLMM1AUN" ,"MPCLMM1BR_TPNC_OTU_SESP":"MP-CLMM1BR","MPCLMM1BUN_TPNC_OTU_SESP":"MP-CLMM1BUN" , "MPCLMP1AR_TPNC_OTU_SESP":"MP-CLMP1AR" , "MPCLMP1AUN_TPNC_OTU_SESP":"MP-CLMP1AUN" ,"MPCLMP1BR_TPNC_OTU_SESP":"MP-CLMP1BR" ,"MPCLMP1BUN_TPNC_OTU_SESP":"MP-CLMP1BUN","MPSWOP01_TPNC_OTU_SESP":"MP-SWOP01","MPSWOP03_TPNC_OTU_SESP":"MP-SWOP03","MPSWOP05_TPNC_OTU_SESP":"MP-SWOP05","MPSWOP07_TPNC_OTU_SESP":"MP-SWOP07","MPSWOP08_TPNC_OTU_SESP":"MP-SWOP08","MPSWS000_TPNC_OTU_SESP":"MP-SWS000","MPUPGMEDIA_TPNC_OTU_SESP":"MP-UPGMEDIA"}
		UpgradeRequired = ChildProduct.Attr('UpgradeRequired_TPNC_OTU_SESP').GetValue()
		LCNNodes = round(float(ChildProduct.Attr('LCNNodes_TPNC_OTU_SESP').GetValue()))
		tpn_parts = []
		tpn_lic_part = {}
		if UpgradeRequired == 'Yes' and LCNNodes > 0:
			TPN_current_version	= ChildProduct.Attr('CurrentVer_TPNC_OTU_SESP').GetValue()
			TPN_target_version = ChildProduct.Attr('TargetVer_TPNC_OTU_SESP').GetValue()
			TPN_lic_parts = self.getLicPartData('TPN',TPN_current_version,TPN_target_version)
			if TPN_lic_parts is not None:
				tpn_lic_part['Price'] = 0
				tpn_lic_part['Part'] = TPN_lic_parts.Part_Number
				tpn_lic_part['Qty'] = LCNNodes
				tpn_lic_part['IsLicensed'] = 'True'
				tpn_lic_part['CurrentVersion'] = TPN_current_version
				tpn_lic_part['TargetVersion'] = TPN_target_version
				tpn_parts.append(tpn_lic_part)
		for i,k in tpn.items():
			price = self.get_part_price(k)
			if ChildProduct.Attr(i).GetValue() != '':
				if float(ChildProduct.Attr(i).GetValue()) > 0:
					TPN_UE_Parts = {}
					TPN_UE_Parts['Part'] = k
					TPN_UE_Parts['Qty'] = round(float(ChildProduct.Attr(i).GetValue()))
					TPN_UE_Parts['Price'] = price
					TPN_UE_Parts['CurrentVersion'] = ''
					TPN_UE_Parts['TargetVersion'] = ''
					TPN_UE_Parts['IsLicensed'] = 'False'
					tpn_parts.append(TPN_UE_Parts)
		return tpn_parts
	def other_Part_Prices(self,ChildProduct,msid_row, Quote, TagParserQuote, Session):
		priceDict = dict()
		#Get list price of TPS and GUS parts
		partNumbers = ["EP-STAC01", "EP-STAC05", "EP-STAC10", "EP-CONTPS", "EP-DSS020", "EP-GPT020", "EP-MDS020", "EP-FLT020", "EP-RNW020", "EP-RGC020", "EP-ABV020", "EP-ASP020", "EP-CLS020"]
		priceDict = cps.getPrice(Quote, priceDict, partNumbers, TagParserQuote, Session)
		TPS_OTU_PRICE_PARTS = ["EPASP020_TPSC_OTU_SESP","EPRGC020_TPSC_OTU_SESP","EPRNW020_TPSC_OTU_SESP","EPFLT020_TPSC_OTU_SESP","EPMDS020_TPSC_OTU_SESP","EPGPT020_TPSC_OTU_SESP","EPCLS020_TPSC_OTU_SESP","EPABV020_TPSC_OTU_SESP","EPDSS020_TPSC_OTU_SESP","EPCONTPS_TPSC_OTU_SESP","EPSTAC10_TPSC_OTU_SESP","EPSTAC05_TPSC_OTU_SESP","EPSTAC01_TPSC_OTU_SESP"]
		TPS_OTU_PRICE = 0
		GUSS_PARTS = ["EPDSS020_ESTVC_OTU_SESP","EPMDS020_ESTVC_OTU_SESP","EPGPT020_ESTVC_OTU_SESP","EPRNW020_ESTVC_OTU_SESP","EPCLS020_V1_ESTVC_OTU_SESP","EPASP020_V1_ESTVC_OTU_SESP","EPFLT020_ESTVC_OTU_SESP","EPRGC020_ESTVC_OTU_SESP"]
		GUS_OTU_PRICE = 0
		for TPS_PART in TPS_OTU_PRICE_PARTS:
			TPS_QTY = round(float(ChildProduct.Attr(TPS_PART).GetValue()))
			if TPS_QTY > 0:
				splited = str(TPS_PART.split('_')[0])[0:2] + '-'+ str(TPS_PART.split('_')[0])[2:]
				#Trace.Write('TPS _ SPLITED - >' +str(splited))
				TPS_PRICE = float(priceDict.get(splited,0)) * TPS_QTY
				TPS_OTU_PRICE += TPS_PRICE
		for GUS_PART in GUSS_PARTS:
			GUS_QTY = round(float(ChildProduct.Attr(GUS_PART).GetValue()))
			if GUS_QTY > 0:
				splited_gus = str(GUS_PART.split('_')[0])[0:2] + '-'+ str(GUS_PART.split('_')[0])[2:]
				GUS_PRICE = float(priceDict.get(splited_gus,0)) * GUS_QTY
				GUS_OTU_PRICE += GUS_PRICE
		return [TPS_OTU_PRICE,GUS_OTU_PRICE]
	def get_ebm_prices(self,ChildProduct,msid_row):
		parts = ["EPBRVE06_HSC_OTU_SESP","EPBRVE06_ESTVC_OTU_SESP","EPBRVE06_EXPC_OTU_SESP","EPBRVE06_SSC_OTU_SESP","EPBRVE06_ESSC_OTU_SESP","EPBRWE06_HSC_OTU_SESP","EPBRWE06_ESTVC_OTU_SESP","EPBRWE06_EXPC_OTU_SESP","EPBRWE06_SSC_OTU_SESP","EPBRWE06_ESSC_OTU_SESP","EPBRSE06_HSC_OTU_SESP","EPBRSE06_ESTVC_OTU_SESP","EPBRSE06_EXPC_OTU_SESP","EPBRSE06_SSC_OTU_SESP","EPBRSE06_ESSC_OTU_SESP"]
		total = 0
		for i in parts:
			splitedpart = str(i.split('_')[0])[0:2] + "-" + str(i.split('_')[0])[2:]
			qty = ChildProduct.Attr(i).GetValue()
			price = self.get_part_price(splitedpart)
			total += (float(price) * float(qty))
		return total
	def get_ebr_parts(self,ChildProduct):
		EBR_Parts_Dict = {"EP-BRVE06":"EPBRVE06_EBR_OTU_SESP","EP-BRSE06":"EPBRSE06_EBR_OTU_SESP","EP-BRWE06":"EPBRWE06_EBR_OTU_SESP"}
		ebr_parts = []
		for part,attr in EBR_Parts_Dict.items():
			res = dict()
			qty = ChildProduct.Attr(attr).GetValue()
			qty = int(float(qty)) if str(qty).strip() != '' else 0
			res['Part'] = part
			res['Price'] = 0
			res['CurrentVersion'] = ''
			res['TargetVersion'] = ''
			res['IsLicensed'] = 'False'
			res['Qty'] = qty
			ebr_parts.append(res)
		return ebr_parts