if Product.Name == "Hardware Refresh":
	searchedTXT = Product.Attr("SC_SearchInputSS_HR_RWL").GetValue()
	SESP_Models_Cont = Product.GetContainerByName('SC_ModelsSS_HR_RWL')
	SESP_Models_Cont_Hidden = Product.GetContainerByName('SC_ModelsHiddenSS_HR_RWL')
	SESP_Models_Cont.Clear()
	Selection_Cont = Product.GetContainerByName('SC_SelectionSS_HR_RWL')
elif Product.Name == "Service Contract Products":
	contdetails = Product.GetContainerByName("Service Contract Modules")
	for rows in contdetails.Rows:
		if rows["Type"] == "Renewal" and rows["Module"] == "Hardware Refresh" and rows.Product.Attr('SC_Product_Type').GetValue() == 'Renewal':
			searchedTXT = rows.Product.Attr("SC_SearchInputSS_HR_RWL").GetValue()
			SESP_Models_Cont = rows.Product.GetContainerByName('SC_ModelsSS_HR_RWL')
			SESP_Models_Cont_Hidden = rows.Product.GetContainerByName('SC_ModelsHiddenSS_HR_RWL')
			SESP_Models_Cont.Clear()
			Selection_Cont = rows.Product.GetContainerByName('SC_SelectionSS_HR_RWL')
ScopeList = []
for row in Selection_Cont.Rows:
	if row.IsSelected:
		ScopeList.append(row["Scope"])
def insertSysDetails(AssetHID,SESP_Models_Cont):
	if AssetHID["Comments"] in ScopeList:
		MODEL_ROW = SESP_Models_Cont.AddNewRow(False)
		MODEL_ROW["Asset"] = AssetHID["Asset"]
		MODEL_ROW["Model"] = AssetHID["Model"]
		MODEL_ROW["Description"] = AssetHID["Description"]
		MODEL_ROW["PreviousYearQuantity"] = AssetHID["PreviousYearQuantity"]
		MODEL_ROW["RenewalQuantity"] = AssetHID["RenewalQuantity"]
		MODEL_ROW["PreviousYearUnitPrice"] = AssetHID["PreviousYearUnitPrice"]
		MODEL_ROW["PreviousYearListPrice"] = AssetHID["PreviousYearListPrice"]
		MODEL_ROW["HoneywellListPricePerUnit"] = AssetHID["HoneywellListPricePerUnit"]
		MODEL_ROW["ScopeReductionQuantity"] = AssetHID["ScopeReductionQuantity"]
		MODEL_ROW["ScopeReductionPrice"] = AssetHID["ScopeReductionPrice"]
		MODEL_ROW["EscalationPercentage"] = AssetHID["EscalationPercentage"]
		MODEL_ROW["EscalationValue"] = AssetHID["EscalationValue"]
		MODEL_ROW["ScopeAdditionQuantity"] = AssetHID["ScopeAdditionQuantity"]
		MODEL_ROW["ScopeAdditionPrice"] = AssetHID["ScopeAdditionPrice"]
		MODEL_ROW["FinalListPrice"] = AssetHID["FinalListPrice"]
		MODEL_ROW["LastYearDiscountPer"] = AssetHID["LastYearDiscountPer"]
		MODEL_ROW["TotalDiscountPer"] = AssetHID["TotalDiscountPer"]
		MODEL_ROW["TotalDiscountPrice"] = AssetHID["TotalDiscountPrice"]
		MODEL_ROW["PreviousYearSellPrice"] = AssetHID["PreviousYearSellPrice"]
		MODEL_ROW["FinalSellPrice"] = AssetHID["FinalSellPrice"]
		MODEL_ROW["ScopeChange"] = AssetHID["ScopeChange"]
		MODEL_ROW["PriceImpact"] = AssetHID["PriceImpact"]
		MODEL_ROW["Comments"] = AssetHID["Comments"]
		MODEL_ROW['PreviousYearUnitCostPrice'] = AssetHID['PreviousYearUnitCostPrice']
		MODEL_ROW['PreviousYearCostPrice'] = AssetHID['PreviousYearCostPrice']
		MODEL_ROW['Sc_CurrentYearListPrice_HR_RWL'] = AssetHID['Sc_CurrentYearListPrice_HR_RWL']
		MODEL_ROW['SC_CurrentYearUnitCostPrice_HR_RWL'] = AssetHID['SC_CurrentYearUnitCostPrice_HR_RWL']
		MODEL_ROW['SC_CurrentYearCostPrice_HR_RWL'] = AssetHID['SC_CurrentYearCostPrice_HR_RWL']
if searchedTXT == "" or searchedTXT is None:
	for AssetHID in SESP_Models_Cont_Hidden.Rows:
		insertSysDetails(AssetHID,SESP_Models_Cont)
	else:
		SESP_Models_Cont.Calculate()
else:
	for AssetHID in SESP_Models_Cont_Hidden.Rows:
		if str(AssetHID["Asset"]).upper().Contains(str(searchedTXT).upper()):
			insertSysDetails(AssetHID,SESP_Models_Cont)
	else:
		SESP_Models_Cont.Calculate()