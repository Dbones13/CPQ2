if Product.Attr('SC_Product_Type').GetValue() is not None and Product.Attr('SC_Product_Type').GetValue() == 'Renewal':
	PriceImpact=discount_percent=0
	py_discount1= 0
	comparisonCont = Product.GetContainerByName('ComparisonSummary')
	if comparisonCont.Rows.Count:
		for compRow in comparisonCont.Rows:
			py_discount1 = compRow["PY_Discount_SFDC"] if compRow["PY_Discount_SFDC"] else '0'
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
		EscalationPercentage = 0
		SumModelRow["EscalationPercentage"] = str(EscalationPercentage) + "%"
		if row['SC_Comment_HR_RWL'] == 'Scope Addition':
			EscalationValue = float(float(EscalationPercentage)/100) * float(row["SC_PreviousYearUnitPrice_HR_RWL"]) * float(row["SC_Quantity_HR_RWL"])
		else:
			EscalationValue = float(float(EscalationPercentage)/100) * int(float(row["SC_RenewalQuantity_HR_RWL"])) * float(row["SC_PreviousYearUnitPrice_HR_RWL"])
		if Product.Attr('SC_Pricing_Escalation').GetValue()=="No":
			SumModelRow["EscalationValue"] = str(0)
		else:
			SumModelRow["EscalationValue"] = str(EscalationValue)
		#SumModelRow["EscalationValue"] = str(EscalationValue)
		ScopeAdditionQuantity = int(float(row["SC_RenewalQuantity_HR_RWL"])) - int(float(row["SC_Quantity_HR_RWL"])) if int(float(row["SC_Quantity_HR_RWL"])) < int(float(row["SC_RenewalQuantity_HR_RWL"])) else 0
		SumModelRow["ScopeAdditionQuantity"] = str(ScopeAdditionQuantity)
		ScopeAdditionPrice =  ScopeAdditionQuantity * float(row["SC_HoneywellListPrice_HR_RWL"])
		SumModelRow["ScopeAdditionPrice"] = str(ScopeAdditionPrice)
		FinalListPrice = float(row["SC_PreviousYearListPrice_HR_RWL"]) + EscalationValue + ScopeReductionPrice + ScopeAdditionPrice
		if Product.Attr('SC_Pricing_Escalation').GetValue()=="No":
			FinalListPrice=float(row['Sc_CurrentYearListPrice_HR_RWL'])
		SumModelRow["FinalListPrice"] = str(FinalListPrice)
		LastYearDiscountPer = str(round(float(py_discount1) * 100,2))
		SumModelRow["LastYearDiscountPer"] = str(LastYearDiscountPer)
		TotalDiscountPer = 0
		SumModelRow["TotalDiscountPer"] = str(TotalDiscountPer) + "%"
		TotalDiscountPrice = FinalListPrice * (float(TotalDiscountPer)/100)
		SumModelRow["TotalDiscountPrice"] = str(TotalDiscountPrice)
		PreviousYearSellPrice = float(SumModelRow["PreviousYearListPrice"]) - (float(SumModelRow["PreviousYearListPrice"]) * float(py_discount1))
		#PreviousYearSellPrice = PreviousYearSellPrice-(PreviousYearSellPrice % 0.01)
		SumModelRow["PreviousYearSellPrice"] = str(PreviousYearSellPrice)
		FinalSellPrice = FinalListPrice * (1-(float(TotalDiscountPer)/100))
		SumModelRow["FinalSellPrice"] = str(FinalSellPrice)
		SumModelRow['PreviousYearCostPrice'] = row['SC_PreviousYearCostPrice_HR_RWL']
		SumModelRow['PreviousYearUnitCostPrice'] = row['SC_PreviousYearUnitCostPrice_HR_RWL']
		SumModelRow['Sc_CurrentYearListPrice_HR_RWL'] = row['Sc_CurrentYearListPrice_HR_RWL']
		SumModelRow['SC_CurrentYearUnitCostPrice_HR_RWL'] = row['SC_CurrentYearUnitCostPrice_HR_RWL']
		SumModelRow['SC_CurrentYearCostPrice_HR_RWL'] = row['SC_CurrentYearCostPrice_HR_RWL']
		ScopeChange = 0
		if FinalListPrice != 0 and float(row["SC_PreviousYearListPrice_HR_RWL"]) != 0:
			ScopeChange = (ScopeReductionPrice * (PreviousYearSellPrice/(float(row["SC_PreviousYearListPrice_HR_RWL"])))) + (ScopeAdditionPrice*(FinalSellPrice/FinalListPrice))
			SumModelRow["ScopeChange"] = str(ScopeChange)
			PriceImpact = FinalSellPrice - (ScopeChange + PreviousYearSellPrice)
			SumModelRow["PriceImpact"] = str(PriceImpact)
			SumModelRow["Comments"] = row["SC_Comment_HR_RWL"]
		if Product.Attr('SC_Pricing_Escalation').GetValue() == "Yes":
			if int(row['SC_RenewalQuantity_HR_RWL']) > int(row['SC_Quantity_HR_RWL']):
				SumModelRow['Escalation_Price'] = str(float(row['SC_Quantity_HR_RWL'])*float(row['SC_PreviousYearUnitPrice_HR_RWL']))
				SumModelRow['List Price'] = str((float(row['SC_Quantity_HR_RWL'])*float(row['SC_PreviousYearUnitPrice_HR_RWL'])) + ((int(row['SC_RenewalQuantity_HR_RWL']) - int(row['SC_Quantity_HR_RWL']))*float(row['Sc_CurrentYearListPrice_HR_RWL'])))
			else:
				SumModelRow['Escalation_Price'] = str(float(row['SC_RenewalQuantity_HR_RWL'])*float(row['SC_PreviousYearUnitPrice_HR_RWL']))
				SumModelRow['List Price'] = str(float(row['SC_RenewalQuantity_HR_RWL'])*float(row['SC_PreviousYearUnitPrice_HR_RWL']))
		else:
			SumModelRow['Escalation_Price'] = '0'
			SumModelRow['List Price'] = row['Sc_CurrentYearListPrice_HR_RWL']
		#PY sell price code
		if row['SC_Quantity_HR_RWL'] > row['SC_RenewalQuantity_HR_RWL']:
			SumModelRow['SR_Quantity'] = str(int(row['SC_RenewalQuantity_HR_RWL'])-int(row['SC_Quantity_HR_RWL']))
		else:
			SumModelRow['SR_Quantity']= str(0)
		if row['SC_Quantity_HR_RWL'] < row['SC_RenewalQuantity_HR_RWL']:
			SumModelRow['SA_Quantity'] = str(int(row['SC_RenewalQuantity_HR_RWL'])-int(row['SC_Quantity_HR_RWL']))
		else:
			SumModelRow['SA_Quantity']= str(0)
		SumModelRow['SR_Price'] = str(float(row['SC_PreviousYearUnitPrice_HR_RWL'])*float(SumModelRow['SR_Quantity']))
		SumModelRow['SA_Price'] = str(float(row['SC_HoneywellListPrice_HR_RWL'])*float(SumModelRow['SA_Quantity']))
		SP_Discount = {}
		HRHW_Cont = Product.GetContainerByName('SC_ModelsHiddenSS_HR_RWL')
		ComparisonSummary = Product.GetContainerByName("ComparisonSummary")
		if ComparisonSummary.Rows.Count:
			for row in ComparisonSummary.Rows:
				if row['PY_List_Price_SFDC']!='' and float(row['PY_List_Price_SFDC']) > 0:
					discount_percent = ((float(row['PY_List_Price_SFDC']) - float(row['PY_Sell_Price_SFDC']))/float(row['PY_List_Price_SFDC']) if float(row['PY_List_Price_SFDC']) != '' else 0)
				#SP_Discount[row['Asset']] = discount_percent
		if HRHW_Cont.Rows.Count:
			sscont= Product.GetContainerByName('SC_ModelsSS_HR_RWL')
			for hrow,ss in zip(HRHW_Cont.Rows,sscont.Rows):
				if hrow:
					discount = discount_percent
					hrow['PY_SellPrice'] = str(float(hrow['PreviousYearListPrice']) - (float(hrow['PreviousYearListPrice']) * discount))
					ss['PY_SellPrice'] = hrow['PY_SellPrice']
					Trace.Write("Lahu >>>>>>>>> " +str(hrow['PY_SellPrice']))
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
			sscont.Calculate()