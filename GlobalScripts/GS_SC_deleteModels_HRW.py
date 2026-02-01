models = Product.GetContainerByName('SC_ValidModels_HR_RWL')
m=[]
for i in models.Rows:
    if i.IsSelected :
        m.append(i.RowIndex)
m.reverse()
for i in m:
    models.DeleteRow(i)
    models.Calculate()
MODELS_CONT_SS_Hidden = Product.GetContainerByName('SC_ModelsHiddenSS_HR_RWL')
MODELS_SSE_CONT = Product.GetContainerByName('SC_ValidModels_HR_RWL')
MODELS_CONT_SS_Hidden.Clear()
for row in MODELS_SSE_CONT.Rows:
	SumModelRow = MODELS_CONT_SS_Hidden.AddNewRow(False)
	SumModelRow["Asset"] = row["SC_Asset_HR_RWL"]
	SumModelRow["Model"] = row["SC_Model_HR_RWL"]
	SumModelRow["Description"] = row["SC_Description_HR_RWL"]
	SumModelRow["PreviousYearQuantity"] = row["SC_Quantity_HR_RWL"]
	SumModelRow["RenewalQuantity"] = row["SC_RenewalQuantity_HR_RWL"]
	SumModelRow["PreviousYearUnitPrice"] = row["SC_PreviousYearUnitPrice_HR_RWL"]
	SumModelRow["PreviousYearListPrice"] = row["SC_PreviousYearListPrice_HR_RWL"]
	SumModelRow["HoneywellListPricePerUnit"] = row["SC_HoneywellListPrice_HR_RWL"]
	ScopeReductionQuantity = int(float(row["SC_RenewalQuantity_HR_RWL"])) - int(float(row["SC_Quantity_HR_RWL"])) if int(float(row["SC_Quantity_HR_RWL"])) > int(float(row["SC_RenewalQuantity_HR_RWL"])) else 0
	SumModelRow["ScopeReductionQuantity"] = str(ScopeReductionQuantity)
	ScopeReductionPrice = ScopeReductionQuantity * float(row["SC_PreviousYearUnitPrice_HR_RWL"])
	SumModelRow["ScopeReductionPrice"] = str(ScopeReductionPrice)
	EscalationPercentage = 10
	SumModelRow["EscalationPercentage"] = str(EscalationPercentage) + "%"
	if row['SC_Comment_HR_RWL'] == 'Scope Addition':
		EscalationValue = float(float(EscalationPercentage)/100) * float(row["SC_PreviousYearUnitPrice_HR_RWL"]) * float(row["SC_Quantity_HR_RWL"])
	else:
		EscalationValue = float(float(EscalationPercentage)/100) * int(float(row["SC_RenewalQuantity_HR_RWL"])) * float(row["SC_PreviousYearUnitPrice_HR_RWL"])
	SumModelRow["EscalationValue"] = str(EscalationValue)
	ScopeAdditionQuantity = int(float(row["SC_RenewalQuantity_HR_RWL"])) - int(float(row["SC_Quantity_HR_RWL"])) if int(float(row["SC_Quantity_HR_RWL"])) < int(float(row["SC_RenewalQuantity_HR_RWL"])) else 0
	SumModelRow["ScopeAdditionQuantity"] = str(ScopeAdditionQuantity)
	ScopeAdditionPrice =  ScopeAdditionQuantity * float(row["SC_HoneywellListPrice_HR_RWL"])
	SumModelRow["ScopeAdditionPrice"] = str(ScopeAdditionPrice)
	FinalListPrice = float(row["SC_PreviousYearListPrice_HR_RWL"]) + EscalationValue + ScopeReductionPrice + ScopeAdditionPrice
	SumModelRow["FinalListPrice"] = str(FinalListPrice)
	LastYearDiscountPer = 10
	SumModelRow["LastYearDiscountPer"] = str(LastYearDiscountPer) + "%"
	TotalDiscountPer = 10
	SumModelRow["TotalDiscountPer"] = str(TotalDiscountPer) + "%"
	TotalDiscountPrice = FinalListPrice * (float(TotalDiscountPer)/100)
	SumModelRow["TotalDiscountPrice"] = str(TotalDiscountPrice)
	PreviousYearSellPrice = float(row["SC_PreviousYearListPrice_HR_RWL"]) * (1-(float(LastYearDiscountPer)/100))
	SumModelRow["PreviousYearSellPrice"] = str(PreviousYearSellPrice)
	FinalSellPrice = FinalListPrice * (1-(float(TotalDiscountPer)/100))
	SumModelRow["FinalSellPrice"] = str(FinalSellPrice)
	ScopeChange = 0
	SumModelRow['PreviousYearCostPrice'] = row['SC_PreviousYearCostPrice_HR_RWL']
	SumModelRow['PreviousYearUnitCostPrice'] = row['SC_PreviousYearUnitCostPrice_HR_RWL']
	SumModelRow['Sc_CurrentYearListPrice_HR_RWL'] = row['Sc_CurrentYearListPrice_HR_RWL']
	SumModelRow['SC_CurrentYearUnitCostPrice_HR_RWL'] = row['SC_CurrentYearUnitCostPrice_HR_RWL']
	SumModelRow['SC_CurrentYearCostPrice_HR_RWL'] = row['SC_CurrentYearCostPrice_HR_RWL']
	if FinalListPrice != 0 and float(row["SC_PreviousYearListPrice_HR_RWL"]) != 0:
		ScopeChange = (ScopeReductionPrice * (PreviousYearSellPrice/(float(row["SC_PreviousYearListPrice_HR_RWL"])))) + (ScopeAdditionPrice*(FinalSellPrice/FinalListPrice))
	SumModelRow["ScopeChange"] = str(ScopeChange)
	PriceImpact = FinalSellPrice - (ScopeChange + PreviousYearSellPrice)
	SumModelRow["PriceImpact"] = str(PriceImpact)
	SumModelRow["Comments"] = row["SC_Comment_HR_RWL"]
	Trace.Write("ScopeReductionQuantity --------->>		"+str(ScopeReductionQuantity)+"
"+"ScopeReductionPrice --------->>		"+str(ScopeReductionPrice)+"
"+"EscalationPercentage --------->>		 "+str(EscalationPercentage)+"
"+"EscalationValue --------->>			 "+str(EscalationValue)+"
"+"ScopeAdditionQuantity --------->>		 "+str(ScopeAdditionQuantity)+"
"+"ScopeAdditionPrice --------->>			 "+str(ScopeAdditionPrice)+"
"+"FinalListPrice --------->>				 "+str(FinalListPrice)+"
"+"LastYearDiscountPer --------->>		 "+str(LastYearDiscountPer)+"
"+"TotalDiscountPer --------->>			 "+str(TotalDiscountPer)+"
"+"TotalDiscountPrice --------->>			 "+str(TotalDiscountPrice)+"
"+"PreviousYearSellPrice --------->>		 "+str(PreviousYearSellPrice)+"
"+"FinalSellPrice --------->>				 "+str(FinalSellPrice)+"
"+"ScopeChange --------->>				 "+str(ScopeChange)+"
"+"PriceImpact --------->>		 		"+str(PriceImpact))
MODELS_CONT_SS_Hidden.Calculate()
#ScriptExecutor.Execute('GS_SCR_SearchModel_HR_RWL')
#For Message Flags update  for renewal on deletion of valid models
if Product.Attr('SC_Product_Type').GetValue() is not None and Product.Attr('SC_Product_Type').GetValue() == 'Renewal':
	Product.Attr("SC_ServiceProduct_HR_RWL").Access = AttributeAccess.ReadOnly
	#Product incomplete on renewal quantity / Honeywell list price is zero
	isNone = False
	con = Product.GetContainerByName("SC_ValidModels_HR_RWL")
	if con.Rows.Count:
		for i in con.Rows:
			if i['SC_RenewalQuantity_HR_RWL'] == '' or float(i['SC_RenewalQuantity_HR_RWL']) == 0 or i['SC_HoneywellListPrice_HR_RWL'] == '' or float(i['SC_HoneywellListPrice_HR_RWL']) == 0 or i['SC_Asset_HR_RWL'] == '' or i['SC_Asset_HR_RWL'] is None or i['SC_Model_HR_RWL'] is None or i['SC_Description_HR_RWL'] is None or i['SC_Model_HR_RWL'] == '' or i['SC_Description_HR_RWL'] == '':
				isNone = True
				Product.Attr('IncompleteMessageFlag_HWR').AssignValue('False')
				Product.Attr('ModelAndDescription_CompleteCheck_HRW').AssignValue('False')
				Product.Attr('qtyAndUnitprice_CompleteCheck_HRW').AssignValue('False')
				if (i['SC_RenewalQuantity_HR_RWL'] == '' or float(i['SC_RenewalQuantity_HR_RWL']) == 0) and (i['SC_HoneywellListPrice_HR_RWL'] == '' or float(i['SC_HoneywellListPrice_HR_RWL']) == 0) and (i['SC_Asset_HR_RWL'] == '' or i['SC_Asset_HR_RWL'] is None) and (i['SC_Model_HR_RWL'] is None or i['SC_Model_HR_RWL'] == '') and (i['SC_Description_HR_RWL'] is None or i['SC_Description_HR_RWL'] == ''):
					Product.Attr('IncompleteMessageFlag_HWR').AssignValue('True')
				elif i['SC_Model_HR_RWL'] is None or i['SC_Description_HR_RWL'] is None or i['SC_Model_HR_RWL'] == '' or i['SC_Description_HR_RWL'] == '':
					Product.Attr('ModelAndDescription_CompleteCheck_HRW').AssignValue('True')
					Product.Attr('qtyAndUnitprice_CompleteCheck_HRW').AssignValue('False')
				elif i['SC_RenewalQuantity_HR_RWL'] == '' or float(i['SC_RenewalQuantity_HR_RWL']) == 0 or i['SC_HoneywellListPrice_HR_RWL'] == '' or float(i['SC_HoneywellListPrice_HR_RWL']) == 0:
					Product.Attr('qtyAndUnitprice_CompleteCheck_HRW').AssignValue('True')
		else :
			if isNone:
				Product.Attr('IsproductComplete_HRW').Required = True
				#Product.Attr('IncompleteMessageFlag_HWR').AssignValue('True')
			else:
				Product.Attr('IsproductComplete_HRW').Required = False
				#Product.Attr('IncompleteMessageFlag_HWR').AssignValue('False')
	else :
		Product.Attr('IsproductComplete_HRW').Required = True
		Product.Attr('IncompleteMessageFlag_HWR').AssignValue('True')
else:
	Product.Attr('IsproductComplete_HRW').Required = False
	Product.Attr('IncompleteMessageFlag_HWR').AssignValue('False')