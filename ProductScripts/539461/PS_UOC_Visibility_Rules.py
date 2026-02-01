from GS_UpdateLaborPrices import getFloat
def getContainer(containerName):
	return Product.GetContainerByName(containerName)

def getAttributeValue(attribute_name):
	return Product.Attributes.GetByName(attribute_name)

def setHidden(cont,column):
	Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format(cont, column))
def setEditable(cont,column):
	Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format(cont, column))

def disallowattrs(attname):
	return Product.DisallowAttr(attname)
def allowattrs(attname):
	return Product.AllowAttr(attname)
if Product.Name in ("ControlEdge UOC System", "ControlEdge UOC System Migration"):
	setHidden('UOC_Labor_Details','UOC_Num_ProfiNet_Devices_Labour')
	setHidden('UOC_Labor_Details','UOC_Num_ProfiNet_Devices_IO_Labour')
	setHidden('UOC_Labor_Details','UOC_Num_EtherNet_Devices_Labour')
	setHidden('UOC_Labor_Details','UOC_Num_EtherNet_Devices_IO_Labour')
	if getContainer('UOC_Common_Questions_Cont'):
		for i in getContainer('UOC_Common_Questions_Cont').Rows:
			uoc_starter_kit = i['UOC_Starter_Kit']
			#uoc_starter_kit=getContainer('UOC_Common_Questions_Cont').Rows[0].Item['UOC_Starter_Kit']
			if uoc_starter_kit == "No" or uoc_starter_kit == "":
				Trace.Write('coming on first if condition')
				setHidden('UOC_Common_Questions_Cont','UOC_Starter_ Kit_with_Experion_License')
			else:
				setEditable('UOC_Common_Questions_Cont','UOC_Starter_ Kit_with_Experion_License')
				Trace.Write('coming on first else condition')
isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if Product.Name == "ControlEdge UOC System Migration" and isR2Qquote:
	if getContainer('UOC_Common_Questions_Cont'):
		setHidden('UOC_Common_Questions_Cont','UOC_Starter_ Kit_with_Experion_License')

	#Labor_Parameter_Peer
	peer_PCDI,peer_CDA,peer_to_Peer=0,0,0
	if getContainer('UOC_Labor_Details'):
		for j in getContainer('UOC_Labor_Details').Rows:
			peer_PCDI+=getFloat(j['UOC_Num_Peer_PCDI_Labour'])
	#peer_PCDI=getContainer('UOC_Labor_Details').Rows[0].Item['UOC_Num_Peer_PCDI_Labour'] if getContainer('UOC_Labor_Details') else ''
	if getContainer('UOC_Labor_Details'):
		for k in getContainer('UOC_Labor_Details').Rows:
			peer_CDA+=getFloat(k['UOC_Num_Peer_CDA_Labour'])
	#peer_CDA=getContainer('UOC_Labor_Details').Rows[0].Item['UOC_Num_Peer_CDA_Labour'] if getContainer('UOC_Labor_Details') else ''
	if getContainer('UOC_Labor_Details'):
		for l in getContainer('UOC_Labor_Details').Rows:
			peer_to_Peer+=getFloat(l['UOC_Num_Peer_to_Peer'])
	#peer_to_Peer=getContainer('UOC_Labor_Details').Rows[0].Item['UOC_Num_Peer_to_Peer'] if getContainer('UOC_Labor_Details') else ''
	'''if getContainer('UOC_Labor_Details'):
		for l in getContainer('UOC_Labor_Details').Rows:
			peer_to_Peer=l['UOC_Num_Peer_to_Peer']'''
	peer_PCDI = peer_PCDI if peer_PCDI else 0
	Trace.Write("-peer_PCDIpeer_PCDI--"+str(peer_PCDI))
	peer_CDA = peer_CDA if peer_CDA else 0
	peer_to_Peer = peer_to_Peer if peer_to_Peer else 0
	sum_labor_peer= getFloat(peer_PCDI)+getFloat(peer_CDA)+getFloat(peer_to_Peer)
	if getAttributeValue('Labor_Parameter_Peer'):
		getAttributeValue('Labor_Parameter_Peer').AssignValue(str(sum_labor_peer))

	#DCS_UOC_CGRG_System_Cabinet
	uoc_sys_cabinet , uoc_sys_cabinet_Rg=0,0
	if getContainer('UOC_ControlGroup_Cont'):
		for i in getContainer('UOC_ControlGroup_Cont').Rows:
			uoc_sys_cabinet+=getFloat(i['staging_UOC_Num_of_Sys_Cabinets'])
	if getContainer('UOC_ControlGroup_Cont'):
		for rg in getContainer('UOC_ControlGroup_Cont').Rows:
			uoc_sys_cabinet_Rg+=getFloat(rg['Staging_UOC_Num_of_Sys_Cabinets_RG'])
	#uoc_sys_cabinet=getContainer('UOC_ControlGroup_Cont').Rows[0].Item['staging_UOC_Num_of_Sys_Cabinets'] if getContainer('UOC_ControlGroup_Cont') else ''
	#uoc_sys_cabinet_Rg=getContainer('UOC_ControlGroup_Cont').Rows[0].Item['Staging_UOC_Num_of_Sys_Cabinets_RG'] if  getContainer('UOC_ControlGroup_Cont') else ''
	Trace.Write("-uoc_sys_cabinet-"+str(uoc_sys_cabinet))
	uoc_sys_cabinet = uoc_sys_cabinet if uoc_sys_cabinet else 0
	uoc_sys_cabinet_Rg = uoc_sys_cabinet_Rg if uoc_sys_cabinet_Rg else 0

	sum_Uoc_sys_Cabinet=getFloat(uoc_sys_cabinet)+getFloat(uoc_sys_cabinet_Rg)

	sum_Uoc_sys_Cabinet = sum_Uoc_sys_Cabinet if sum_Uoc_sys_Cabinet else 0
	if getAttributeValue('DCS_UOC_CGRG_System_Cabinet'):
		getAttributeValue('DCS_UOC_CGRG_System_Cabinet').AssignValue(str(sum_Uoc_sys_Cabinet))

	#Total_UOC_DCS_Marshalling
	if getAttributeValue('staging_Marshalling_Cabinets_c300_rtu_uoc_SM_plc'):
		staging_c300_rtu_uoc_Sm_plc=getAttributeValue('staging_Marshalling_Cabinets_c300_rtu_uoc_SM_plc').GetValue()
	#staging_c300_rtu_uoc_Sm_plc = staging_c300_rtu_uoc_Sm_plc if staging_c300_rtu_uoc_Sm_plc else 0
	if getAttributeValue('Total_UOC_DCS_Marshalling'):
		getAttributeValue('Total_UOC_DCS_Marshalling').AssignValue(str(staging_c300_rtu_uoc_Sm_plc))

	#ADC_Ges_Location
	if getContainer('UOC_Labor_Details'):
		for i in getContainer('UOC_Labor_Details').Rows:
			uoc_ges_loc=i['UOC_Ges_Location_Labour']
			if uoc_ges_loc == "None":
				if getAttributeValue('UOC_CD_LD_GES Engineer %'):
					disallowattrs('UOC_CD_LD_GES Engineer %')
				GES_Eng=setHidden('CE UOC Additional Custom Deliverables','GES Eng')
				GES_Eng_Split=setHidden('CE UOC Additional Custom Deliverables','GES Eng % Split')
				GES_Eng_unit_reg_cost=setHidden('CE UOC Additional Custom Deliverables','GES_Unit_Regional_Cost')
				GES_Eng_regional_cost=setHidden('CE UOC Additional Custom Deliverables','GES_Regional_Cost')
				GES_Eng_ListPrice=setHidden('CE UOC Additional Custom Deliverables','GES_ListPrice')
				GES_Eng_WTW_cost=setHidden('CE UOC Additional Custom Deliverables','GES_WTW_Cost')
				GES_Eng_MPA_Price=setHidden('CE UOC Additional Custom Deliverables','GES_MPA_Price')
			else:
				if getAttributeValue('UOC_CD_LD_GES Engineer %'):
					allowattrs('UOC_CD_LD_GES Engineer %')
				GES_Eng=setEditable('CE UOC Additional Custom Deliverables','GES Eng')
				GES_Eng_Split=setEditable('CE UOC Additional Custom Deliverables','GES Eng % Split')
				GES_Eng_unit_reg_cost=setEditable('CE UOC Additional Custom Deliverables','GES_Unit_Regional_Cost')
				GES_Eng_regional_cost=setEditable('CE UOC Additional Custom Deliverables','GES_Regional_Cost')
				GES_Eng_ListPrice=setEditable('CE UOC Additional Custom Deliverables','GES_ListPrice')
				GES_Eng_WTW_cost=setEditable('CE UOC Additional Custom Deliverables','GES_WTW_Cost')
				GES_Eng_MPA_Price=setEditable('CE UOC Additional Custom Deliverables','GES_MPA_Price')

	#Hide_UOC_Software_Question_Container
	if getAttributeValue('UOC_Software_Question_Cont'):
		disallowattrs('UOC_Software_Question_Cont')

	#Final Hrs 
	Ce_uoc_eng,Ce_uoc_Additional =0.0,0.0
	if getContainer('CE UOC Engineering Labor Container'):
		for i in getContainer('CE UOC Engineering Labor Container').Rows:
			if i['Final Hrs']:
				Ce_uoc_eng+=getFloat(i['Final Hrs'])
	if getContainer('CE UOC Additional Custom Deliverables'):
		for i in getContainer('CE UOC Additional Custom Deliverables').Rows:
			if i['Final Hrs']:
				Ce_uoc_Additional+=getFloat(i['Final Hrs'])
				Trace.Write(Ce_uoc_eng)
	Ce_uoc_eng= Ce_uoc_eng if Ce_uoc_eng else 0
	Ce_uoc_Additional= Ce_uoc_Additional if Ce_uoc_Additional else 0
	Total = getFloat(Ce_uoc_eng)+getFloat(Ce_uoc_Additional)
	if getAttributeValue('Final_Hrs'):
		getAttributeValue('Final_Hrs').AssignValue(str(Total))
	'''------GES Location ------'''
	if getContainer('UOC_Labor_Details'):
		for i in getContainer('UOC_Labor_Details').Rows:
			UOC_Ges_Location_labour =i['UOC_Ges_Location_Labour']
			if UOC_Ges_Location_labour == "None":
				disallowattrs('CE UOC GES Engineer %')
				GES_ENG =setHidden('CE UOC Engineering Labor Container','GES Eng')
				#modified for CE UOC Engineering Labor Container. CXCPQ-90688
				GES_Eng_Split=setHidden('CE UOC Engineering Labor Container','GES Eng % Split')
				GES_Eng_unit_reg_cost=setHidden('CE UOC Engineering Labor Container','GES_Unit_Regional_Cost')
				GES_Eng_regional_cost=setHidden('CE UOC Engineering Labor Container','GES_Regional_Cost')
				GES_Eng_ListPrice=setHidden('CE UOC Engineering Labor Container','GES_ListPrice')
				GES_Eng_WTW_cost=setHidden('CE UOC Engineering Labor Container','GES_WTW_Cost')
				GES_Eng_MPA_Price=setHidden('CE UOC Engineering Labor Container','GES_MPA_Price')
			else:
				allowattrs('CE UOC GES Engineer %')
				GES_Eng=setEditable('CE UOC Engineering Labor Container','GES Eng')
				GES_Eng_Split=setEditable('CE UOC Engineering Labor Container','GES Eng % Split')
				GES_Eng_unit_reg_cost=setEditable('CE UOC Engineering Labor Container','GES_Unit_Regional_Cost')
				GES_Eng_regional_cost=setEditable('CE UOC Engineering Labor Container','GES_Regional_Cost')
				GES_Eng_ListPrice=setEditable('CE UOC Engineering Labor Container','GES_ListPrice')
				GES_Eng_WTW_cost=setEditable('CE UOC Engineering Labor Container','GES_WTW_Cost')
				GES_Eng_MPA_Price=setEditable('CE UOC Engineering Labor Container','GES_MPA_Price')

	if getContainer('UOC_Labor_Details'):
		for i in getContainer('UOC_Labor_Details').Rows:
			UOC_process =i['UOC_Process_Type_Labour']
			if UOC_process in ['BatchPharma','BatchChemical']:
				setEditable('UOC_Labor_Details','UOC_Num_Complex_Operations_Per_Product_Labour')
				setEditable('UOC_Labor_Details','UOC_Input_Quality_Specific_Labour')
			else:
				setHidden('UOC_Labor_Details','ColumnUOC_Num_Complex_Operations_Per_Product_Labour')
				setHidden('UOC_Labor_Details','UOC_Input_Quality_Specific_Labour')
			if UOC_process =="BatchPharma":
				setEditable('UOC_Labor_Details','UOC_Num_Simple_Complexity_QA_Labour')
				setEditable('UOC_Labor_Details','UOC_Num_Medium_Complexity_QA_Labour')
				setEditable('UOC_Labor_Details','UOC_Num_Complex_Complexity_QA_Labour')
				setEditable('UOC_Labor_Details','UOC_Num_Complex_Operations_Per_Product_Labour')
				setEditable('UOC_Labor_Details','UOC_Percentage_Pre_FAT')
			else:
				setHidden('UOC_Labor_Details','UOC_Num_Simple_Complexity_QA_Labour')
				setHidden('UOC_Labor_Details','UOC_Num_Medium_Complexity_QA_Labour')
				setHidden('UOC_Labor_Details','UOC_Num_Complex_Complexity_QA_Labour')
				setHidden('UOC_Labor_Details','UOC_Num_Complex_Operations_Per_Product_Labour')
				setHidden('UOC_Labor_Details','UOC_Percentage_Pre_FAT')
	#LabourColumnsHide
			if UOC_process =="None" or UOC_process == 'Continuous' or UOC_process == 'Continuous + Interlock' or UOC_process =='Continuous + Sequence' or UOC_process == ' Continuous + Interlock + Sequence':
				setHidden('UOC_Labor_Details','UOC_Num_Batch_Units_Master_Labour')
				setHidden('UOC_Labor_Details',"UOC_Num_Batch_Units_Copies_Replica_Master_Labour")
				setHidden('UOC_Labor_Details',"UOC_Num_Product_Master_Recipes_Labour")
				setHidden('UOC_Labor_Details',"UOC_Num_Product_Copy_Unit_Product_Replicated_Unit")
				setHidden('UOC_Labor_Details',"UOC_Num_Complex_SCMs_Per_Unit_Labour")
				setHidden('UOC_Labor_Details',"UOC_Num_Complex_Operations_Per_Product_Labour")
			else:
				setEditable('UOC_Labor_Details','UOC_Num_Batch_Units_Master_Labour')
				setEditable('UOC_Labor_Details',"UOC_Num_Batch_Units_Copies_Replica_Master_Labour")
				setEditable('UOC_Labor_Details',"UOC_Num_Product_Master_Recipes_Labour")
				setEditable('UOC_Labor_Details',"UOC_Num_Product_Copy_Unit_Product_Replicated_Unit")
				setEditable('UOC_Labor_Details',"UOC_Num_Complex_SCMs_Per_Unit_Labour")
				setEditable('UOC_Labor_Details',"UOC_Num_Complex_Operations_Per_Product_Labour")
	#LabourContainerHideUOC
	if getAttributeValue('CE_Scope_Choices'):
		if getAttributeValue('CE_Scope_Choices').GetValue() =="HW/SW":
			if getAttributeValue ('UOC_Labor_Details'):
				disallowattrs('UOC_Labor_Details')
		else:
			if getAttributeValue ('UOC_Labor_Details'):
				allowattrs('UOC_Labor_Details')