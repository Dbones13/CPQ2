def hide_attribute(attributename):
	Product.DisallowAttr(attributename)

def show_attribute(attributename):
	Product.AllowAttr(attributename)

def getContainer(Name):
	return Product.GetContainerByName(Name)

Session["Scope"] = scope = Product.Attr('MIgration_Scope_Choices').GetValue()
Session["MSID_Current_Experion_Release"]=Product.Attr('MSID_Current_Experion_Release').GetValue()
Session["MSID_Future_Experion_Release"]=Product.Attr('MSID_Future_Experion_Release').GetValue()  
Trace.Write("scope -- "+str(Session["Scope"])+" MSID_Current_Experion_Release -- "+str(Session["MSID_Current_Experion_Release"])+" future -- "+str(Session["MSID_Future_Experion_Release"]))
current_experion = Product.Attr('MSID_Current_Experion_Release').GetValue()
future_experion = Product.Attr('MSID_Future_Experion_Release').GetValue()
aa = Product.GetContainerByName('CONT_MSID_SUBPRD')
for row in aa.Rows:
	if row.Product.Name == 'OPM' :
		row.Product.Attr('MSID_Current_Experion_Release').AssignValue(current_experion)
		Trace.Write("currentexperion"+str(row.Product.Attr('MSID_Current_Experion_Release').GetValue()))
		row.Product.Attr('MSID_Future_Experion_Release').AssignValue(future_experion)
prdlist = Product.Attr('MSID_PRDCHOICES').GetValue().split(', ')

selectedProducts = set()
a = ''
addbr=''

for row in getContainer("CONT_MSID_SUBPRD").Rows:
	selectedProducts.add(row["Selected_Products"])
	if row["Selected_Products"] == 'Generic System Migration':
		a += addbr+row["Product Name"]
	else:
		a += addbr+row["Selected_Products"]
	addbr = '<br>'
	msid_product = row.Product

Product.Attr('MSID_Selected_Products').AssignValue(a)

if Product.Attr('MIgration_Scope_Choices').GetValue() == 'HW/SW':
	prdattrdict = {"MSID_FEL_Data_Gathering_Required": {},"MSID_Current_Experion_Release":{'OPM','Non-SESP Exp Upgrade'},"MSID_Future_Experion_Release":{'OPM','Non-SESP Exp Upgrade','xPM to C300 Migration','C200 Migration','CB-EC Upgrade to C300-UHIO','TPS to Experion'},"MSID_Current_TPN_Release":{'LCN One Time Upgrade'},"MSID_Future_TPN_Release":{'LCN One Time Upgrade'},"ATTR_COMQESYORN":{'LM to ELMM ControlEdge PLC'},"Yes-No Selection":{'LM to ELMM ControlEdge PLC','Orion Console'},'EHPM_HART_IO_Construction_Work_Package_doc_require':{'EHPM HART IO'},'Regional_Migration_Principal_Efforts_Required':{},'MSID_Is_Site_Acceptance_Test_Required':{},'MSID_Is_Switch_Configuration_in_Honeywell_Scope':{'xPM to C300 Migration','C200 Migration'},'MSID_Is_FTE_based_System_already_installed_on_Site':{},'MSID_Acceptance_Test_Required':{},'MSID_GES_Location':{}}
else:
	prdattrdict = {"MSID_FEL_Data_Gathering_Required": {'OPM','ELCN','EHPM/EHPMX/ C300PM','TPS to Experion'},"MSID_Current_Experion_Release":{'OPM','Non-SESP Exp Upgrade'},"MSID_Future_Experion_Release":{'OPM','Non-SESP Exp Upgrade','TPS to Experion','xPM to C300 Migration','C200 Migration','CB-EC Upgrade to C300-UHIO'},"MSID_Current_TPN_Release":{'LCN One Time Upgrade'},"MSID_Future_TPN_Release":{'LCN One Time Upgrade'},"MSID_Acceptance_Test_Required":{'CB-EC Upgrade to C300-UHIO','TPS to Experion'}, "MSID_Is_FTE_based_System_already_installed_on_Site":{'LM to ELMM ControlEdge PLC','C200 Migration','3rd Party PLC to ControlEdge PLC/UOC'},"Yes-No Selection":{'LM to ELMM ControlEdge PLC','Orion Console'},'MSID_Is_Switch_Configuration_in_Honeywell_Scope':{'TPS to Experion','xPM to C300 Migration','C200 Migration'},'Regional_Migration_Principal_Efforts_Required':{'EBR','OPM','ELCN','TPS to Experion','Virtualization System Migration','Orion Console','EHPM/EHPMX/ C300PM','EHPM HART IO','C200 Migration','FSC to SM','Generic System Migration','3rd Party PLC to ControlEdge PLC/UOC'},'MSID_Is_Site_Acceptance_Test_Required':{'xPM to C300 Migration','ELCN'},'EHPM_HART_IO_Construction_Work_Package_doc_require':{'EHPM HART IO'},"ATTR_COMQESYORN":{'LM to ELMM ControlEdge PLC'},'MSID_GES_Location':{'OPM', 'Non-SESP Exp Upgrade', 'LCN One Time Upgrade', 'EBR', 'ELCN', 'Virtualization System Migration', 'Graphics Migration', 'EHPM/EHPMX/ C300PM', 'Orion Console', 'TPS to Experion', 'TCMI', 'Spare Parts', 'C200 Migration', 'EHPM HART IO', 'CB-EC Upgrade to C300-UHIO', 'FSC to SM', 'FSC to SM IO Migration', 'xPM to C300 Migration', 'FDM Upgrade 1', 'Integrated Automation Assessment', 'LM to ELMM ControlEdge PLC', 'XP10 Actuator Upgrade', '3rd Party PLC to ControlEdge PLC/UOC', 'CWS RAE Upgrade', 'QCS RAE Upgrade', 'CD Actuator I-F Upgrade', 'TPA/PMD Migration', 'Generic System Migration', 'FDM Upgrade 2', 'FDM Upgrade 3', 'ELEPIU ControlEdge RTU Migration Engineering', 'Trace Software','Virtualization System'}}

prductlist = set(prdlist+list(selectedProducts))

for key,products in prdattrdict.items():
	x = prductlist.intersection(products)
	if len(x) == 0:
		hide_attribute(key)
	else:
		show_attribute(key)

if prdlist[0]=="" and len(list(selectedProducts))==0:
	Product.DisallowAttr("MSID_Crate_Type")
	Product.DisallowAttr("MSID_Crate_Design")

isLaborSelected = False
isHWSWSelected = False
isHSWLaborSelected = False
if scope == 'LABOR':
	isLaborSelected = True
if scope == 'HW/SW':
	isHWSWSelected = True
if scope == 'HW/SW/LABOR':
	isHSWLaborSelected = True
'''container = Product.GetContainerByName('CONT_MSID_SUBPRD')
for row in container.Rows:
	selectedProducts.update(row['Selected_Products'].split('<br>'))'''
Trace.Write("selectedProducts ----------------- "+str(selectedProducts))

if isLaborSelected or 'Non-SESP Exp Upgrade' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','NON_SESP_EXP')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','NON_SESP_EXP')

if 'LCN One Time Upgrade' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','LCN')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','LCN')

if 'OPM' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','OPM')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','OPM')

if 'EBR' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','EBR')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','EBR')

if 'ELCN' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','ELCN')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','ELCN')

if 'Orion Console' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','Orion_Console')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','Orion_Console')

if 'EHPM/EHPMX/ C300PM' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','EHPM_C300PM')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','EHPM_C300PM')

if 'TPS to Experion' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','TPS_to_Experion')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','TPS_to_Experion')

if isHWSWSelected or 'TCMI' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','TCMI')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','TCMI')

if 'C200 Migration' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','C200_Migration')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','C200_Migration')

if 'EHPM HART IO' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','EHPM_HART_IO')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','EHPM_HART_IO')
if 'Integrated Automation Assessment' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','Integrated_Automation_Assessment_IAA')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','Integrated_Automation_Assessment_IAA')

if 'xPM to C300 Migration' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','xPM_to_C300_Migration')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','xPM_to_C300_Migration')

if 'FSC to SM' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','FSC_to_SM')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','FSC_to_SM')

if 'FSC to SM IO Migration' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','FSC_to_SM_IO_Migration')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','FSC_to_SM_IO_Migration')

if 'CD Actuator I-F Upgrade' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','CD_Actuator_IF_Upgrade')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','CD_Actuator_IF_Upgrade')

if 'LM to ELMM ControlEdge PLC' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','LM_ELMM_ControlEdge_PLC')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','LM_ELMM_ControlEdge_PLC')

if 'CB-EC Upgrade to C300-UHIO' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','CB-EC_Upgrade_to_C300-UHIO_Objects')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','CB-EC_Upgrade_to_C300-UHIO_Objects')

if 'FDM Upgrade 1' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','FDM_Upgrade')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','FDM_Upgrade')

if 'FDM Upgrade 2' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','FDM_Upgrade_2')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','FDM_Upgrade_2')

if 'FDM Upgrade 3' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','FDM_Upgrade_3')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','FDM_Upgrade_3')

if 'XP10 Actuator Upgrade' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','XP10_Actuator_Upgrade')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','XP10_Actuator_Upgrade')
if '3rd Party PLC to ControlEdge PLC/UOC' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','3rd_Party_PLC_to_ControlEdge_PLC/UOC')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','3rd_Party_PLC_to_ControlEdge_PLC/UOC')

if isHWSWSelected or 'Graphics Migration' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','Graphics_Migration')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','Graphics_Migration')

if 'Virtualization System Migration' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','Virtualization_System_Migration')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','Virtualization_System_Migration')

if 'Generic System 5' in a.split('<br>') or scope == 'HW/SW':
	Product.DisallowAttrValues('MSID_PRDCHOICES','Generic_System_Migration')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','Generic_System_Migration')

if 'QCS RAE Upgrade' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','QCS_RAE_Upgrade')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','QCS_RAE_Upgrade')

if 'CWS RAE Upgrade' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','CWS_RAE_Upgrade')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','CWS_RAE_Upgrade')

if 'TPA/PMD Migration' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','TPA/PMD_Migration')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','TPA/PMD_Migration')

if 'Trace Software' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','Trace Software')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','Trace Software')

if isHWSWSelected or 'ELEPIU ControlEdge RTU Migration Engineering' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','ELEPIU_ControlEdge_RTU_Migration_Engineering')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','ELEPIU_ControlEdge_RTU_Migration_Engineering')#-- Dhrumil Shah : CXCPQ-60040 :end
if isLaborSelected or 'Spare Parts' in selectedProducts:
	Product.DisallowAttrValues('MSID_PRDCHOICES','Spare_Parts')
else:
	Product.AllowAttrValues('MSID_PRDCHOICES','Spare_Parts')

if len(selectedProducts) >1 and (isHWSWSelected or isHSWLaborSelected):
	Product.AllowAttrValues('MSID_PRDCHOICES','Spare_Parts')
elif len( selectedProducts) ==1 and (isHWSWSelected or isHSWLaborSelected):
	for product in selectedProducts:
		if product:
			Product.AllowAttrValues('MSID_PRDCHOICES','Spare_Parts')
		else:
			Product.DisallowAttrValues('MSID_PRDCHOICES','Spare_Parts')
else:
	Product.DisallowAttrValues('MSID_PRDCHOICES','Spare_Parts')
	
# For hiding the dropdown values of MSID_Future_Experion_Release based on MSID_Current_Experion_Release attribute
curr_rel = Product.Attr('MSID_Current_Experion_Release').GetValue()
fut_attr = Product.Attr('MSID_Future_Experion_Release')
if fut_attr.Allowed:
	if curr_rel == 'R511.x':
		for value in fut_attr.Values:
			if value.Display in ('R510','R511'):
				value.Allowed = False
				if value.IsSelected:
					Product.ResetAttr('MSID_Future_Experion_Release')
			else:
				value.Allowed = True

	elif curr_rel == 'R520.x':
		for value in fut_attr.Values:
			if value.Display in ('R510','R511','R520'):
				value.Allowed = False
				if value.IsSelected:
					Product.ResetAttr('MSID_Future_Experion_Release')
			else:
				value.Allowed = True

	elif curr_rel == 'R510.x':
		for value in fut_attr.Values:
			if value.Display in ('R510'):
				value.Allowed = False
				if value.IsSelected:
					Product.ResetAttr('MSID_Future_Experion_Release')
			else:
				value.Allowed = True
	else:
		for value in fut_attr.Values:
			value.Allowed = True