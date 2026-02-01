def getContainer(Name):
	return Product.GetContainerByName(Name)

def setAttrValue(Name,value):
	Product.Attr(Name).AssignValue(value)

def populateFoEngColumn(container,row):
	for Row in container.Rows:
		if Row["Deliverable"] not in ('Total','Off-Site','On-Site') and Row.IsSelected:
			if row["Product_Module"] in ('OPM','LCN','EBR','ELCN','Orion Console','EHPM/EHPMX/ C300PM','TPS TO EXPERION','EHPM HART IO','TCMI','C200 Migration','CB-EC Upgrade to C300-UHIO','FDM Upgrade','FSC to SM','FSC to SM Audit','xPM to C300 Migration','LM to ELMM ControlEdge PLC','XP10 Actuator Upgrade','Graphics Migration','CD Actuator I-F Upgrade','CWS RAE Upgrade','FSC to SM IO Migration','3rd Party PLC to ControlEdge PLC/UOC','Virtualization System','QCS RAE Upgrade','Generic System 1','Generic System 2','Generic System 3','Generic System 4','Generic System 5','TPA/PMD Migration','FSC to SM IO Audit','ELEPIU ControlEdge RTU Migration Engineering'):
				Row["FO_Eng"] = row["FO_Part_Number"]
				Row["Regional_Cost"] = row["Cost"]
				Row["Manual_Entry"] = row["Manual_Entry"]
			elif row["Product_Module"] == "PM" and Row["Deliverable_Flag"] == "PM":
				Row["FO_Eng"] = row["FO_Part_Number"]
				Row["Regional_Cost"] = row["Cost"]
				Row["Manual_Entry"] = row["Manual_Entry"]
			elif row["Product_Module"] == "PA" and Row["Deliverable_Flag"] == "PA":
				Row["FO_Eng"] = row["FO_Part_Number"]
				Row["Regional_Cost"] = row["Cost"]
				Row["Manual_Entry"] = row["Manual_Entry"]
			#Row.IsSelected = False
			row.IsSelected = False

def populateGesEngColumn(container,row):
	for Row in container.Rows:
		if Row["Deliverable"] not in ('Total','Off-Site','On-Site') and Row.IsSelected:
			if row["Product_Module"] in ('OPM','LCN','EBR','ELCN','Orion Console','EHPM/EHPMX/ C300PM','TPS TO EXPERION','EHPM HART IO','TCMI','C200 Migration','CB-EC Upgrade to C300-UHIO','FDM Upgrade','FSC to SM','FSC to SM Audit','xPM to C300 Migration','LM to ELMM ControlEdge PLC','XP10 Actuator Upgrade','Graphics Migration','CD Actuator I-F Upgrade','FSC to SM IO Migration','3rd Party PLC to ControlEdge PLC/UOC','Virtualization System','Generic System 1','Generic System 2','Generic System 3','Generic System 4','Generic System 5','TPA/PMD Migration','FSC to SM IO Audit','ELEPIU ControlEdge RTU Migration Engineering'):
				Row["GES_Eng"] = row["GES_Part_Number"]
			elif row["Product_Module"] == "PM":
				Row["GES_Eng"] = row["GES_Part_Number"]
			elif row["Product_Module"] == "CWS RAE Upgrade":
				if Row["Deliverable"] != "MD CD Configuration":
					Row["GES_Eng"] = row["GES_Part_Number"]
			elif row["Product_Module"] == "QCS RAE Upgrade":
				if Row["Deliverable"] != "In-house Engineering MD-CD":
					Row["GES_Eng"] = row["GES_Part_Number"]
			#Row.IsSelected = False
			row.IsSelected = False

foPartNumberCon = getContainer("MSID_Labor_FO_Part_Number")
opmEngineeringCon = getContainer("MSID_Labor_OPM_Engineering")
lcnOneTimeUpgradeCon = getContainer("MSID_Labor_LCN_One_Time_Upgrade_Engineering")
ebrCon = getContainer("MSID_Labor_EBR_Con")
elcnCon = getContainer("MSID_Labor_ELCN_Con")
orionConsoleCon = getContainer("MSID_Labor_Orion_Console_Con")
ehpmCon = getContainer("MSID_Labor_EHPM_C300PM_Con")
tpsCon = getContainer("MSID_Labor_TPS_TO_EXPERION_Con")
ehpmhartioCon = getContainer("MSID_Labor_EHPM_HART_IO_Con")
tcmiCon = getContainer("MSID_Labor_TCMI_Con")
c200MigrationCon = getContainer("MSID_Labor_C200_Migration_Con")
cbecCon = getContainer("MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con")
fsctosmCon = getContainer("MSID_Labor_FSC_to_SM_con")
fsctosmauditCon = getContainer("MSID_Labor_FSC_to_SM_audit_Con")
fdmupgradeCon = getContainer("MSID_Labor_FDM_Upgrade_Con")
xPMCon = getContainer("MSID_Labor_xPM_to_C300_Migration_Con")
lmCon = getContainer("MSID_Labor_LM_to_ELMM_Con")
projectManagementCon = getContainer("MSID_Labor_Project_Management")
additonalCustomDelivCon = getContainer("MSID_Additional_Custom_Deliverables")
XP10Con = getContainer("MSID_Labor_XP10_Actuator_Upgrade_con")
GraphicsCon = getContainer("MSID_Labor_Graphics_Migration_con")
CDActuatorCon = getContainer("MSID_Labor_CD_Actuator_con")
fscsmioCon = getContainer("MSID_Labor_FSCtoSM_IO_con")
CWSCon = getContainer("MSID_Labor_CWS_RAE_Upgrade_con")
QCSCon = getContainer("MSID_Labor_QCS_RAE_Upgrade_con")
plcuocCon = getContainer("3rd_Party_PLC_UOC_Labor")
virtualizationCon = getContainer("MSID_Labor_Virtualization_con")
gen1Con=getContainer("MSID_Labor_Generic_System1_Cont")
gen2Con=getContainer("MSID_Labor_Generic_System2_Cont")
gen3Con=getContainer("MSID_Labor_Generic_System3_Cont")
gen4Con=getContainer("MSID_Labor_Generic_System4_Cont")
gen5Con=getContainer("MSID_Labor_Generic_System5_Cont")
TPACon = getContainer("MSID_Labor_TPA_con")
fsctosmioauditCon = getContainer('MSID_Labor_FSC_to_SM_IO_Audit_Con')
# Extended Logic for ELEPIU Module by adding container name -- Dipak Shekokar : CXCPQ-60162
ELEPIUCon = getContainer('MSID_Labor_ELEPIU_con')

laborMessagesAttrs = ['Labor_OPM_Message','Labor_LCN_Message','Labor_EBR_Message','Labor_ELCN_Message','Labor_Orion_Console_Message','Labor_EHPM_C300PM_Message','Labor_TPS_TO_EXPERION_Message','Labor_PM_Message','MSID_Labor_Message','Labor_TCMI_Message','Labor_EHPM_HART_IO_Message','Labor_C200_Migration_Message','Labor_CB-EC_Upgrade_to_C300-UHIO_Message','Labor_FDM_Upgrade_Message','Labor_FSC_to_SM_Message','Labor_xPM_to_C300_Migration_Message','Labor_LM_to_ELMM_Message','Labor_FSC_to_SM_audit_Message','Labor_XP10_Actuator_Upgrade_Message','Labor_Graphics_Migration_Message','Labor_CD_Actuator_Message','Labor_CWS_RAE_Upgrade_Message','Labor_FSCtoSM_IO_Message','3rd_party_PLC_UOC_Labor_Message','Labor_Virtualization_Message','Labor_QCS_RAE_Upgrade_Message','Generic1_Message','Generic2_Message','Generic3_Message','Generic4_Message','Generic5_Message','Labor_TPA_Message','Labor_FSCtoSM_IO_Audit_Message','Labor_ELEPIU_Message']
for attrName in laborMessagesAttrs:
	setAttrValue(attrName,'')

for row in foPartNumberCon.Rows:
	if row.IsSelected and row["Cost"] not in ("0.00",'') and row["GES_Part_Number"] == '':
		if row["Product_Module"] == "OPM":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(opmEngineeringCon,row)
			else:
				setAttrValue("Labor_OPM_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "LCN":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(lcnOneTimeUpgradeCon,row)
			else:
				setAttrValue("Labor_LCN_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "EBR":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(ebrCon,row)
			else:
				setAttrValue("Labor_EBR_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "ELCN":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(elcnCon,row)
			else:
				setAttrValue("Labor_ELCN_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')

		elif row["Product_Module"] == "Orion Console":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(orionConsoleCon,row)
			else:
				setAttrValue("Labor_Orion_Console_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "EHPM/EHPMX/ C300PM":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(ehpmCon,row)
			else:
				setAttrValue("Labor_EHPM_C300PM_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "TPS TO EXPERION":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(tpsCon,row)
			else:
				setAttrValue("Labor_TPS_TO_EXPERION_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "TCMI":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(tcmiCon,row)
			else:
				setAttrValue("Labor_TCMI_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "EHPM HART IO":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(ehpmhartioCon,row)
			else:
				setAttrValue("Labor_EHPM_HART_IO_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "C200 Migration":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(c200MigrationCon,row)
			else:
				setAttrValue("Labor_C200_Migration_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "CB-EC Upgrade to C300-UHIO":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(cbecCon,row)
			else:
				setAttrValue("Labor_CB-EC_Upgrade_to_C300-UHIO_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "FSC to SM":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(fsctosmCon,row)
			else:
				setAttrValue("Labor_FSC_to_SM_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "FSC to SM Audit":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(fsctosmauditCon,row)
			else:
				setAttrValue("Labor_FSC_to_SM_audit_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "FDM Upgrade":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(fdmupgradeCon,row)
			else:
				setAttrValue("Labor_FDM_Upgrade_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "xPM to C300 Migration":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(xPMCon,row)
			else:
				setAttrValue("Labor_xPM_to_C300_Migration_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "LM to ELMM ControlEdge PLC":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(lmCon,row)
			else:
				setAttrValue("Labor_LM_to_ELMM_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] in ('PA','PM'):
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(projectManagementCon,row)
			else:
				setAttrValue("Labor_PM_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "XP10 Actuator Upgrade":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(XP10Con,row)
			else:
				setAttrValue("Labor_XP10_Actuator_Upgrade_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "Graphics Migration":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(GraphicsCon,row)
			else:
				setAttrValue("Labor_Graphics_Migration_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "CD Actuator I-F Upgrade":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(CDActuatorCon,row)
			else:
				setAttrValue("Labor_CD_Actuator_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "CWS RAE Upgrade":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(CWSCon,row)
			else:
				setAttrValue("Labor_CWS_RAE_Upgrade_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "QCS RAE Upgrade":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(QCSCon,row)
			else:
				setAttrValue("Labor_QCS_RAE_Upgrade_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "3rd Party PLC to ControlEdge PLC/UOC":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(plcuocCon,row)
			else:
				setAttrValue("3rd_party_PLC_UOC_Labor_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "Virtualization System":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(virtualizationCon,row)
			else:
				setAttrValue("Labor_Virtualization_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "FSC to SM IO Migration":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(fscsmioCon,row)
			else:
				setAttrValue("Labor_FSCtoSM_IO_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "Generic System 1":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(gen1Con,row)
			else:
				setAttrValue("Generic1_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "Generic System 2":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(gen2Con,row)
			else:
				setAttrValue("Generic2_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "Generic System 3":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(gen3Con,row)
			else:
				setAttrValue("Generic3_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "Generic System 4":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(gen4Con,row)
			else:
				setAttrValue("Generic4_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "Generic System 5":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(gen5Con,row)
			else:
				setAttrValue("Generic5_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "TPA/PMD Migration":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(TPACon,row)
			else:
				setAttrValue("Labor_TPA_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		# Extended Logic Apply Parts Functionality for ELEPIU Module -- Dipak Shekokar : CXCPQ-60162
		elif row["Product_Module"] == "ELEPIU ControlEdge RTU Migration Engineering":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(ELEPIUCon,row)
			else:
				setAttrValue("Labor_ELEPIU_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		elif row["Product_Module"] == "FSC to SM IO Audit":
			if row["ListPrice"] not in ("0.00",'',"0"):
				populateFoEngColumn(fsctosmioauditCon,row)
			else:
				setAttrValue("Labor_FSCtoSM_IO_Audit_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
		if row["Product_Module"] in ('OPM','LCN','EBR','ELCN','Orion Console','EHPM/EHPMX/ C300PM','TPS TO EXPERION','TCMI','PM','PA','EHPM HART IO','C200 Migration','CB-EC Upgrade to C300-UHIO','FDM Upgrade','FSC to SM','xPM to C300 Migration','LM to ELMM ControlEdge PLC','FSC to SM Audit','XP10 Actuator Upgrade','Graphics Migration','CD Actuator I-F Upgrade','CWS RAE Upgrade','FSC to SM IO Migration','3rd Party PLC to ControlEdge PLC/UOC','Virtualization System','QCS RAE Upgrade','Generic System 1','Generic System 2','Generic System 3','Generic System 4','Generic System 5','TPA/PMD Migration', 'FSC to SM IO Audit','ELEPIU ControlEdge RTU Migration Engineering'):
			if additonalCustomDelivCon.Rows.Count > 0:
				for Row in additonalCustomDelivCon.Rows:
					if Row.IsSelected:
						if row["ListPrice"] not in ("0.00",'',"0"):
							Trace.Write('Row["Product_Module"]--'+str(Row["Product_Module"])+'--row["Product_Module"]--'+str(row["Product_Module"])+'--Row["Deliverable_Flag"]--'+str(Row["Deliverable_Flag"]))
							if row["Product_Module"] not in ('PM','PA'):
								if Row["Product_Module"] == row["Product_Module"]:
									Row["FO_Eng"] = row["FO_Part_Number"]
									Row["Regional_Cost"] = row["Cost"]
									Row["Manual_Entry"] = row["Manual_Entry"]
									#Row.IsSelected = False
							else:
								if Row["Product_Module"] == row["Product_Module"]:
									Row["FO_Eng"] = row["FO_Part_Number"]
									Row["Regional_Cost"] = row["Cost"]
									Row["Manual_Entry"] = row["Manual_Entry"]
									#Row.IsSelected = False
							row.IsSelected = False
						else:
							setAttrValue("MSID_Labor_Message",'Part Cannot be applied over activity as the selected Part Number does not have a list price.')
	if row.IsSelected and row["GES_Part_Number"] != '':
		if row["Product_Module"] == "OPM":
			populateGesEngColumn(opmEngineeringCon,row)
		elif row["Product_Module"] == "LCN":
			populateGesEngColumn(lcnOneTimeUpgradeCon,row)
		elif row["Product_Module"] == "EBR":
			populateGesEngColumn(ebrCon,row)
		elif row["Product_Module"] == "ELCN":
			populateGesEngColumn(elcnCon,row)
		elif row["Product_Module"] == "Orion Console":
			populateGesEngColumn(orionConsoleCon,row)
		elif row["Product_Module"] == "EHPM/EHPMX/ C300PM":
			populateGesEngColumn(ehpmCon,row)
		elif row["Product_Module"] == "TPS TO EXPERION":
			populateGesEngColumn(tpsCon,row)
		elif row["Product_Module"] == "EHPM HART IO":
			populateGesEngColumn(ehpmhartioCon,row)
		elif row["Product_Module"] == "C200 Migration":
			populateGesEngColumn(c200MigrationCon,row)
		elif row["Product_Module"] == "CB-EC Upgrade to C300-UHIO":
			populateGesEngColumn(cbecCon,row)
		elif row["Product_Module"] == "FSC to SM":
			populateGesEngColumn(fsctosmCon,row)
		elif row["Product_Module"] == "FSC to SM Audit":
			populateGesEngColumn(fsctosmauditCon,row)
		elif row["Product_Module"] == "FDM Upgrade":
			populateGesEngColumn(fdmupgradeCon,row)
		elif row["Product_Module"] == "LM to ELMM ControlEdge PLC":
			populateGesEngColumn(lmCon,row)
		elif row["Product_Module"] == "xPM to C300 Migration":
			populateGesEngColumn(xPMCon,row)
		elif row["Product_Module"] == "TCMI":
			populateGesEngColumn(tcmiCon,row)
		elif row["Product_Module"] == "PM":
			populateGesEngColumn(projectManagementCon,row)
		elif row["Product_Module"] == "XP10 Actuator Upgrade":
			populateGesEngColumn(XP10Con,row)
		elif row["Product_Module"] == "Graphics Migration":
			populateGesEngColumn(GraphicsCon,row)
		elif row["Product_Module"] == "CD Actuator I-F Upgrade":
			populateGesEngColumn(CDActuatorCon,row)
		elif row["Product_Module"] == "CWS RAE Upgrade":
			populateGesEngColumn(CWSCon,row)
		elif row["Product_Module"] == "QCS RAE Upgrade":
			populateGesEngColumn(QCSCon,row)
		elif row["Product_Module"] == "FSC to SM IO Migration":
			populateGesEngColumn(fscsmioCon,row)
		elif row["Product_Module"] == "3rd Party PLC to ControlEdge PLC/UOC":
			populateGesEngColumn(plcuocCon,row)
		elif row["Product_Module"] == "Virtualization System":
			populateGesEngColumn(virtualizationCon,row)
		elif row["Product_Module"] == "Generic System 1":
			populateGesEngColumn(gen1Con,row)
		elif row["Product_Module"] == "Generic System 2":
			populateGesEngColumn(gen2Con,row)
		elif row["Product_Module"] == "Generic System 3":
			populateGesEngColumn(gen3Con,row)
		elif row["Product_Module"] == "Generic System 4":
			populateGesEngColumn(gen4Con,row)
		elif row["Product_Module"] == "Generic System 5":
			populateGesEngColumn(gen5Con,row)
		elif row["Product_Module"] == "TPA/PMD Migration":
			populateGesEngColumn(TPACon,row)
		# Extended Logic Apply Parts Functionality for ELEPIU Module -- Dipak Shekokar : CXCPQ-60162
		elif row["Product_Module"] == "ELEPIU ControlEdge RTU Migration Engineering":
			populateGesEngColumn(ELEPIUCon,row)
		elif row["Product_Module"] == "FSC to SM IO Audit":
			populateGesEngColumn(fsctosmioauditCon,row)
		if row["Product_Module"] in ('OPM','LCN','EBR','ELCN','Orion Console','EHPM/EHPMX/ C300PM','TPS TO EXPERION','EHPM HART IO','TCMI','PM','PA','C200 Migration','CB-EC Upgrade to C300-UHIO','FDM Upgrade','FSC to SM','xPM to C300 Migration','LM to ELMM ControlEdge PLC','FSC to SM Audit','XP10 Actuator Upgrade','Graphics Migration','CD Actuator I-F Upgrade','CWS RAE Upgrade','FSC to SM IO Migration','3rd Party PLC to ControlEdge PLC/UOC','Virtualization System','QCS RAE Upgrade','Generic System 1','Generic System 2','Generic System 3','Generic System 4','Generic System 5','TPA/PMD Migration','FSC to SM IO Audit','ELEPIU ControlEdge RTU Migration Engineering'):
			if additonalCustomDelivCon.Rows.Count > 0:
				for Row in additonalCustomDelivCon.Rows:
					if Row.IsSelected:
						if Row["Product_Module"] == row["Product_Module"]:
							Row["GES_Eng"] = row["GES_Part_Number"]
							#Row.IsSelected = False
							row.IsSelected = False
if Product.Name == 'Migration_New':
	selectedProducts = Product.GetContainerByName('CONT_MSID_SUBPRD')
	for row in selectedProducts.Rows:
		prd_name = row['Selected_Products']
		Trace.Write("prd_name"+str(prd_name))
		Session["ProductName"] = Session["ProductName"] if Session["ProductName"] else []
		sessionval = Session["ProductName"]
		Trace.Write("sessionval"+str(sessionval))
		if prd_name not in sessionval:
			sessionval.append(prd_name)
			Trace.Write("sessionval after" + str(sessionval))
ScriptExecutor.Execute('PS_PopulateGESCost')
if Product.Name == 'Migration_New':
	ScriptExecutor.Execute('PS_PopulatePartSummary')
	ScriptExecutor.Execute('PS_PopulateChildParts')