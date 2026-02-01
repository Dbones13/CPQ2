searchedTXT = Product.Attr("SearchMsid_SESP_OTU_Summary").GetValue()
SESP_Models_Cont = Product.GetContainerByName('SYSDetails_ScopeSumm_OTU_SESP')
SESP_Models_Cont_Hidden = Product.GetContainerByName('SystemDetails_HIDDEN_OTU_SESP')
SESP_Models_Cont.Clear()
def insertSysDetails(MSIDSYSHID,SESP_Models_Cont,PREV_MSID):
	SYS_ROW = SESP_Models_Cont.AddNewRow(False)
	if PREV_MSID != MSIDSYSHID['MSID_OTU_SESP']:
		SYS_ROW['MSIDs'] = MSIDSYSHID['MSID_OTU_SESP']
		PREV_MSID = MSIDSYSHID['MSID_OTU_SESP']
	SYS_ROW["System Name"] = MSIDSYSHID["System_OTU_SESP"]
	SYS_ROW["List Price"] = str(MSIDSYSHID["ListPrice_OTU_SESP"])
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