otu = Product.Attr('One time upgrade').SelectedValue
if otu:
	MSID_HID_CON = Product.GetContainerByName("SC_Select_MSID_Cont_Hidden")
	OTU_MSID_CON = Product.GetContainerByName("MSIDS_V1_OTU_SESP")
	for HID_ROW in MSID_HID_CON.Rows:
		if HID_ROW.IsSelected:
			fetchSelectedRow = filter(lambda otuRow : otuRow["MSIDS_OTU_SESP"] == HID_ROW["MSIDs"] and otuRow["SystemName_OTU_SESP"] == HID_ROW["System Name"] and otuRow["SystemNumber_OTU_SESP"] == HID_ROW["System Number"],OTU_MSID_CON.Rows)
			if len(fetchSelectedRow) < 1:
				OTU_SYS = OTU_MSID_CON.AddNewRow(False)
				OTU_SYS["MSIDS_OTU_SESP"] = HID_ROW["MSIDs"]
				OTU_SYS.Product.Attr('MSIDChild_OTU_SESP').AssignValue(HID_ROW['MSIDs'])
				OTU_SYS["SystemName_OTU_SESP"] = HID_ROW["System Name"]
				OTU_SYS["SystemNumber_OTU_SESP"] = HID_ROW["System Number"]
				OTU_SYS.Product.Attr('SITEC_OTU_SESP').AssignValue(HID_ROW['SiteID'])
			else:
				pass
	else:
		OTU_MSID_CON.Calculate()
	DeleteRowsId = []
	for HID_ROW in MSID_HID_CON.Rows:
		if HID_ROW.IsSelected == False:
			fetchDeSelectedRow = filter(lambda otuRow : otuRow["MSIDS_OTU_SESP"] == HID_ROW["MSIDs"] and otuRow["SystemName_OTU_SESP"] == HID_ROW["System Name"] and otuRow["SystemNumber_OTU_SESP"] == HID_ROW["System Number"],OTU_MSID_CON.Rows)
			if len(fetchDeSelectedRow) > 0:
				DeleteRowsId.append(fetchDeSelectedRow[0].RowIndex)
	DeleteRowsId.sort()
	decRow = 0
	for rowId in DeleteRowsId:
		rowId -= decRow
		OTU_MSID_CON.DeleteRow(rowId)
		decRow += 1
	OTU_MSID_CON.Calculate()
	######
	MSID_HID_CON = Product.GetContainerByName("SC_Models_Scope")
	OTU_MSID_CON = Product.GetContainerByName("MSIDS_V1_OTU_SESP")
	for HID_ROW in MSID_HID_CON.Rows:
		if HID_ROW.IsSelected:
			fetchSelectedRow = filter(lambda otuRow : otuRow["MSIDS_OTU_SESP"] == HID_ROW["MSIDs"] and otuRow["SystemName_OTU_SESP"] == HID_ROW["System_Name"] and otuRow["SystemNumber_OTU_SESP"] == HID_ROW["System_Number"],OTU_MSID_CON.Rows)
			if len(fetchSelectedRow) < 1:
				OTU_SYS = OTU_MSID_CON.AddNewRow(False)
				OTU_SYS["MSIDS_OTU_SESP"] = HID_ROW["MSIDs"]
				OTU_SYS.Product.Attr('MSIDChild_OTU_SESP').AssignValue(HID_ROW['MSIDs'])
				OTU_SYS["SystemName_OTU_SESP"] = HID_ROW["System_Name"]
				OTU_SYS["SystemNumber_OTU_SESP"] = HID_ROW["System_Number"]
				OTU_SYS.Product.Attr('SITEC_OTU_SESP').AssignValue(HID_ROW['SiteID'])
			else:
				pass
	else:
		OTU_MSID_CON.Calculate()
	DeleteRowsId = []
	for HID_ROW in MSID_HID_CON.Rows:
		if HID_ROW.IsSelected == False:
			fetchDeSelectedRow = filter(lambda otuRow : otuRow["MSIDS_OTU_SESP"] == HID_ROW["MSIDs"] and otuRow["SystemName_OTU_SESP"] == HID_ROW["System_Name"] and otuRow["SystemNumber_OTU_SESP"] == HID_ROW["System_Number"],OTU_MSID_CON.Rows)
			if len(fetchDeSelectedRow) > 0:
				DeleteRowsId.append(fetchDeSelectedRow[0].RowIndex)
	DeleteRowsId.sort()
	decRow = 0
	for rowId in DeleteRowsId:
		rowId -= decRow
		OTU_MSID_CON.DeleteRow(rowId)
		decRow += 1
	OTU_MSID_CON.Calculate()