def populateQuoteTable_groupdata(dataDict, table, product_name):
	for key in dataDict:
		row = table.AddNewRow()
		row["Attribute"] = key
		row["Attribute_Value"] = dataDict[key]
		row["Migration_GUID"] = product_name
def uoccommon_proposal(unit,Item,msidAttributeDict):
	for attr in Item.SelectedAttributes:
		Trace.Write(Item.SelectedAttributes)
		attr_containers = Item.SelectedAttributes.GetContainerByName('UOC_Common_Questions_Cont').Rows
		if attr_containers:
			for row in attr_containers:
				if row["UOC_Cabinet_Required_Racks_Mounting"]:
					msidAttributeDict["UOC_Cabinet_Required_Racks_Mounting_"+str(unit)]=row["UOC_Cabinet_Required_Racks_Mounting"]
	return msidAttributeDict
def plccommon_proposal(unit,Item,msidAttributeDict):
	for attr in Item.SelectedAttributes:
		attr_containers = Item.SelectedAttributes.GetContainerByName('PLC_Software_Question_Cont').Rows
		if attr_containers:
			for row in attr_containers:
				msidAttributeDict["PLC_Software_Release_"+str(unit)]="R"+str(row["PLC_Software_Release"]) if row["PLC_Software_Release"] else ""
				msidAttributeDict["PLC_Media_Delivery_"+str(unit)]=row["PLC_Media_Delivery"] if row["PLC_Media_Delivery"] else ""
				msidAttributeDict["PLC_CE_Builder_Client_"+str(unit)]=row["PLC_CE_Builder_Client"] if row["PLC_CE_Builder_Client"] else ""
				msidAttributeDict["PLC_Migration_Tool_User_License_"+str(unit)]=row["PLC_Migration_Tool_User_License"] if row["PLC_Migration_Tool_User_License"] else ""
				msidAttributeDict["PLC_Subsea_MDIS_Interface_"+str(unit)]=row["PLC_Subsea_MDIS_Interface"] if row["PLC_Subsea_MDIS_Interface"] else ""
				msidAttributeDict["PLC_Cabinet_Required_Racks_Mounting_"+str(unit)]=row["PLC_Cabinet_Required_Racks_Mounting"] if row["PLC_Cabinet_Required_Racks_Mounting"] else ""
		attr_containers = Item.SelectedAttributes.GetContainerByName('CE_PLC_System_Hardware').Rows
		if attr_containers:
			for row in attr_containers:
				msidAttributeDict["PLC_Engineering_Station_Qty_"+str(unit)]=row["PLC_Engineering_Station_Qty"] if row["PLC_Engineering_Station_Qty"] else ""
				msidAttributeDict["PLC_Engineering_Station_Model_"+str(unit)]=row["PLC_Engineering_Station_Model"] if row["PLC_Engineering_Station_Model"] else ""
	return msidAttributeDict
def populateQuoteTable(dataDict, table):
	for key, value in dataDict.items():
		row = table.AddNewRow()
		row["Attribute"] = key
		row["Attribute_Value"] = value
def thirdparty_units(Item,Quote,uoc_unit,plc_unit,last_plc_unit_name,last_uoc_unit_name,plc_control_group_name,uoc_control_group_name):
	msidAttributeDict = dict()
	unitlist_cg = dict()
	unitlist_rg = dict()
	RacksList = dict()
	#table = Quote.QuoteTables["Migration_Document_Data"]
	pname = Item.ProductName
	Log.Info('3rd party units start execution'+str(pname))
	if pname == "ControlEdge UOC System Migration":
		uoc_unit += 1
		last_uoc_unit_name = "UOC Unit {0}".format(uoc_unit)
		RacksList=uoccommon_proposal(uoc_unit,Item,msidAttributeDict)
	if pname == "ControlEdge PLC System Migration":
		plc_unit += 1
		last_plc_unit_name = "PLC Unit {0}".format(plc_unit)
		RacksList=plccommon_proposal(plc_unit,Item,msidAttributeDict)
	if pname == "CE PLC Control Group" and last_plc_unit_name:
		plc_control_group_name = Item.PartNumber
		unitlist_cg[last_plc_unit_name] = Item.ParentItemGuid
	if pname == "UOC Control Group" and last_uoc_unit_name:
		uoc_control_group_name = Item.PartNumber
		unitlist_cg[last_uoc_unit_name] = Item.ParentItemGuid
	if pname == "CE PLC Remote Group" and last_plc_unit_name:
		last_plc_rg_name = last_plc_unit_name+" - "+ plc_control_group_name
		unitlist_rg[last_plc_rg_name] = Item.ParentItemGuid
	if pname == "UOC Remote Group" and last_uoc_unit_name:
		last_uom_rg_name = last_uoc_unit_name+" - "+ uoc_control_group_name
		unitlist_rg[last_uom_rg_name] = Item.ParentItemGuid
	return msidAttributeDict, RacksList, unitlist_cg, unitlist_rg, uoc_unit, plc_unit, last_plc_unit_name, last_uoc_unit_name, plc_control_group_name, uoc_control_group_name