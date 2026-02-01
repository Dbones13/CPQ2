searchedTXT = Product.Attr("SYSDETAILS_SEARCHBOX_OTU_SESP").GetValue()
SESP_Models_Cont = Product.GetContainerByName('SystemDetails_OTU_SESP')
SESP_Models_Cont_Hidden = Product.GetContainerByName('SystemDetails_HIDDEN_OTU_SESP')
SESP_Models_Cont.Clear()
def insertSysDetails(MSIDSYSHID,SESP_Models_Cont,PREV_MSID):
	SYS_ROW = SESP_Models_Cont.AddNewRow(False)
	Trace.Write(PREV_MSID)
	Trace.Write(MSIDSYSHID['MSID_OTU_SESP'])
	if PREV_MSID != MSIDSYSHID['MSID_OTU_SESP']:
		SYS_ROW['MSID_OTU_SESP'] = MSIDSYSHID['MSID_OTU_SESP']
		PREV_MSID = MSIDSYSHID['MSID_OTU_SESP']
	SYS_ROW["System_OTU_SESP"] = MSIDSYSHID["System_OTU_SESP"]
	SYS_ROW["Models_OTU_SESP"] = MSIDSYSHID["Models_OTU_SESP"]
	SYS_ROW["Quantity_OTU_SESP"] = str(MSIDSYSHID["Quantity_OTU_SESP"])
	SYS_ROW["UnitListPrice_OTU_SESP"] = str(MSIDSYSHID["UnitListPrice_OTU_SESP"])
	SYS_ROW["ListPrice_OTU_SESP"] = str(MSIDSYSHID["ListPrice_OTU_SESP"])
	return PREV_MSID
PREV_MSID = ""
if searchedTXT == "" or searchedTXT is None:
	for MSIDSYSHID in SESP_Models_Cont_Hidden.Rows:
		PREV_MSID = insertSysDetails(MSIDSYSHID,SESP_Models_Cont,PREV_MSID)
	else:
		SESP_Models_Cont.Calculate()
else:
	for MSIDSYSHID in SESP_Models_Cont_Hidden.Rows:
		if str(MSIDSYSHID["MSID_OTU_SESP"]).upper().Contains(str(searchedTXT).upper()):
			PREV_MSID = insertSysDetails(MSIDSYSHID,SESP_Models_Cont,PREV_MSID)
	else:
		SESP_Models_Cont.Calculate()