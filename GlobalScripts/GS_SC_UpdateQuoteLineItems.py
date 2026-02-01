def sumDict(sDict):
	result = {}
	for iDict in sDict:
		for k in iDict.keys():
			result[k] = result.get(k, 0) + float(iDict[k])
	return result

def GetServiceProductCode(prodName):
	prodCode = SqlHelper.GetFirst("SELECT ProductCode FROM CT_SC_Entitlements_Data WHERE ServiceProduct='{}'".format(prodName))
	return prodCode.ProductCode if prodCode else ''

def AddSESP(sesp_Dict, sProd, sProdkey, sc_ProdDist):
	sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
	sProd['Description'] = 'Description'
	sProd['Quantity'] = '1'
	sProd.IsSelected = True
	sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
	sProd.Product.Attr('SC_PartNumber').AssignValue('SESP')
	sProd.Product.Attr('SC_Description').AssignValue(sProdkey)
	sProd.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
	sProd.ApplyProductChanges()
	sesp_prods = sesp_Dict.keys()
	if 'Training Match' in sesp_Dict.keys():
		sesp_prods.remove('Training Match')
		sesp_prods.append('Training Match')
	if 'Other cost details' in sesp_Dict.keys():
		sesp_prods.remove('Other cost details')
		sesp_prods.append('Other cost details')
	for pProdkey in sesp_prods:
		if pProdkey.lower() == 'Training Match'.lower():
			m_Dict = sesp_Dict[pProdkey]
			p_container = sProd.Product.GetContainerByName("SC_Asset")
			pProd = p_container.AddNewRow(True)
			pProd['Asset'] = '<*VALUE(SC_AssetName)*>'
			pProd['Description'] = 'Description'
			pProd['Quantity'] = '1'
			pProd['Price'] = str(m_Dict['Price'])
			pProd.IsSelected = True
			pProd.ApplyProductChanges()
			pProd.Product.Attr('SC_ItemEditFlag').AssignValue('110')
			pProd.Product.Attr('SC_AssetName').AssignValue('Training Match')
			pProd.Product.Attr('SC_Description').AssignValue('Optional Entitlement')
			#pProd.Product.Attr('SC_Price').AssignValue(str(sesp_Dict[pProdkey]))
			pProd.Product.Attr('SC_Item_MarginPercent').AssignValue('45')
			
			pProd.Product.Attr('SC_Price').AssignValue(str(m_Dict['Price']))
			pProd.Product.Attr('SC_Honeywell_List_Price').AssignValue(str(m_Dict['Honeywell_List_Price']))
			pProd.Product.Attr('ItemQuantity').AssignValue(str(m_Dict['Quantity']))
			pProd.Product.Attr('SC_Escalation_Price').AssignValue(str(m_Dict['Escalation_Price']))
			pProd.Product.Attr('SC_PY_Price').AssignValue(str(m_Dict['PY_ListPrice']))
			pProd.Product.Attr('SC_PY_SellPrice').AssignValue(str(m_Dict['PY_SellPrice']))
			pProd.Product.Attr('SC_SA_Price').AssignValue(str(m_Dict['SA_Price']))
			pProd.Product.Attr('SC_SR_Price').AssignValue(str(m_Dict['SR_Price']))
		elif pProdkey.lower() == 'Other cost details'.lower():
			p_container = sProd.Product.GetContainerByName("SC_Asset")
			pProd = p_container.AddNewRow(True)
			pProd['Asset'] = '<*VALUE(SC_Platform_Entitlement)*>'
			pProd['Description'] = 'Description'
			pProd['Quantity'] = '1'
			pProd.IsSelected = True
			pProd.ApplyProductChanges()
			pProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
			pProd.Product.Attr('SC_Platform_Entitlement').AssignValue('Other cost details')
			pProd.Product.Attr('SC_Description').AssignValue('Other cost')
			m_Dict = sumDict(sesp_Dict[pProdkey])
			for mProdkey in m_Dict:
				m_container = pProd.Product.GetContainerByName("SC_Asset")
				mProd = m_container.AddNewRow(True)
				mProd['Asset'] = '<*VALUE(SC_AssetName)*>'
				mProd['Description'] = 'Description'
				mProd['Quantity'] = '1'
				mProd['Price'] = str(m_Dict[mProdkey])
				mProd.IsSelected = True
				mProd.ApplyProductChanges()
				m_container.Calculate()
				mProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
				mProd.Product.Attr('SC_AssetName').AssignValue('Asset')
				mProd.Product.Attr('SC_Description').AssignValue(mProdkey)
				mProd.Product.Attr('SC_Price').AssignValue('0')
				mProd.Product.Attr('SC_Item_Cost').AssignValue(str(m_Dict[mProdkey]))
				mProd.Product.Attr('SC_Item_CostStatus').AssignValue('1')
				#mProd.Product.Attr('SC_PLSG_description').AssignValue('Honeywell Software')
				#mProd.Product.Attr('SC_Product_line_sub_group').AssignValue('SESP')
		else:
			p_container = sProd.Product.GetContainerByName("SC_Asset")
			pProd = p_container.AddNewRow(True)
			pProd['Asset'] = '<*VALUE(SC_Platform_Entitlement)*>'
			pProd['Description'] = 'Description'
			pProd['Quantity'] = '1'
			pProd.IsSelected = True
			pProd.ApplyProductChanges()
			pProd.Product.Attr('SC_ItemEditFlag').AssignValue('110')
			pProd.Product.Attr('SC_Platform_Entitlement').AssignValue('Platform')
			pProd.Product.Attr('SC_Description').AssignValue(pProdkey)
			#m_Dict = sumDict(sesp_Dict[pProdkey])
			ItemEditFlag = False
			for mProdkey in sesp_Dict[pProdkey]:
				m_Dict = sesp_Dict[pProdkey][mProdkey]
				m_container = pProd.Product.GetContainerByName("SC_Asset")
				mProd = m_container.AddNewRow(True)
				mProd['Asset'] = '<*VALUE(SC_AssetName)*>'
				mProd['Description'] = 'Description'
				mProd['Quantity'] = '1'
				mProd['Price'] = str(m_Dict['Price'])
				mProd.IsSelected = True
				mProd.ApplyProductChanges()
				m_container.Calculate()
				mProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
				mProd.Product.Attr('SC_AssetName').AssignValue('Asset')
				mProd.Product.Attr('SC_Description').AssignValue(mProdkey)
				mProd.Product.Attr('SC_Price').AssignValue(str(m_Dict['Price']))
				mProd.Product.Attr('SC_Honeywell_List_Price').AssignValue(str(m_Dict['Honeywell_List_Price']))
				mProd.Product.Attr('SC_Item_MarginPercent').AssignValue('45')
				mProd.Product.Attr('ItemQuantity').AssignValue(str(m_Dict['Quantity']))
				mProd.Product.Attr('SC_Escalation_Price').AssignValue(str(m_Dict['Escalation_Price']))
				mProd.Product.Attr('SC_PY_Price').AssignValue(str(m_Dict['PY_ListPrice']))
				mProd.Product.Attr('SC_PY_SellPrice').AssignValue(str(m_Dict['PY_SellPrice']))
				mProd.Product.Attr('SC_SA_Price').AssignValue(str(m_Dict['SA_Price']))
				mProd.Product.Attr('SC_SR_Price').AssignValue(str(m_Dict['SR_Price']))
				if str(m_Dict['Quantity']) != '0':
					ItemEditFlag = True
			if ItemEditFlag == True:
				pProd.Product.Attr('SC_ItemEditFlag').AssignValue('110')
			else:
				pProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
		p_container.Calculate()

def AddParts(pp_Dict, sProd, sProdkey, sc_ProdDist):
	sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
	sProd['Description'] = 'Description'
	sProd['Quantity'] = '1'
	sProd.IsSelected = True
	sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
	sProd.Product.Attr('SC_PartNumber').AssignValue('Parts Management')
	sProd.Product.Attr('SC_Description').AssignValue('Parts Management')
	sProd.ApplyProductChanges()
	for pProdkey in pp_Dict:
		p_container = sProd.Product.GetContainerByName("SC_Asset")
		pProd = p_container.AddNewRow(True)
		pProd['Asset'] = '<*VALUE(SC_Platform_Entitlement)*>'
		pProd['Description'] = 'Description'
		pProd['Quantity'] = '1'
		pProd.IsSelected = True
		pProd.ApplyProductChanges()
		pProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
		pProd.Product.Attr('SC_Platform_Entitlement').AssignValue('Service Product')
		pProd.Product.Attr('SC_Description').AssignValue(pProdkey)
		m_Dict = pp_Dict[pProdkey]
		pProd.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
		#for mProdkey in m_Dict:
		m_container = pProd.Product.GetContainerByName("SC_Asset")
		mProd = m_container.AddNewRow(True)
		mProd['Asset'] = '<*VALUE(SC_AssetName)*>'
		mProd['Description'] = 'Description'
		mProd['Quantity'] = '1'
		mProd['Price'] = str(m_Dict['List_Price'])
		mProd.IsSelected = True
		mProd.ApplyProductChanges()
		m_container.Calculate()
		mProd.Product.Attr('SC_AssetName').AssignValue('Entitlement')
		mProd.Product.Attr('SC_Description').AssignValue(str(m_Dict['Entitlement']))
		mProd.Product.Attr('SC_Price').AssignValue(str(m_Dict['List_Price']))
		mProd.Product.Attr('SC_Escalation_Price').AssignValue(str(m_Dict['Escalation_Price']))
		mProd.Product.Attr('SC_PY_Price').AssignValue(str(m_Dict['PY_ListPrice']))
		mProd.Product.Attr('SC_PY_SellPrice').AssignValue(str(m_Dict['PY_SellPrice']))
		mProd.Product.Attr('SC_SA_Price').AssignValue(str(m_Dict['SA_Price']))
		mProd.Product.Attr('SC_SR_Price').AssignValue(str(m_Dict['SR_Price']))
		mProd.Product.Attr('ItemQuantity').AssignValue(str(m_Dict['Quantity']))
		mProd.Product.Attr('SC_Scope_Manual').AssignValue(str(m_Dict['SC_Scope_Manual']))
		if str(m_Dict['Quantity']) ==  '0':
			mProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
			mProd.Product.Attr('SC_Item_MarginPercent').AssignValue('0')
		else:
			if m_Dict['CostStatus'] == 'Fixed':
				mProd.Product.Attr('SC_ItemEditFlag').AssignValue('110')
				mProd.Product.Attr('SC_Item_Cost').AssignValue(str(m_Dict['Cost']))
				mProd.Product.Attr('SC_Item_CostStatus').AssignValue('1')
			else:
				mProd.Product.Attr('SC_ItemEditFlag').AssignValue('111')
				mProd.Product.Attr('SC_Item_MarginPercent').AssignValue('45')
		p_container.Calculate()

def AddLabor(lb_Dict, sProd, sProdkey, sc_ProdDist):
	sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
	sProd['Description'] = 'Description'
	sProd['Quantity'] = '1'
	sProd.IsSelected = True
	sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
	sProd.Product.Attr('SC_PartNumber').AssignValue('Labor')
	sProd.Product.Attr('SC_Description').AssignValue('Labor Deliverables')
	sProd.ApplyProductChanges()
	for pProdkey in lb_Dict:
		p_container = sProd.Product.GetContainerByName("SC_Asset")
		pProd = p_container.AddNewRow(True)
		pProd['Asset'] = '<*VALUE(SC_Platform_Entitlement)*>'
		pProd['Description'] = 'Description'
		pProd['Quantity'] = '1'
		pProd.IsSelected = True
		pProd.ApplyProductChanges()
		pProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
		pProd.Product.Attr('SC_Platform_Entitlement').AssignValue('Service Product')
		pProd.Product.Attr('SC_Description').AssignValue(pProdkey)
		pProd.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
		oE_Dict = lb_Dict[pProdkey]
		for eProdkey in oE_Dict:
			if eProdkey == 'ProductCode':
				continue
			e_container = pProd.Product.GetContainerByName("SC_Asset")
			eProd = e_container.AddNewRow(True)
			eProd['Asset'] = '<*VALUE(SC_Platform_Entitlement)*>'
			eProd['Description'] = 'Description'
			eProd['Quantity'] = '1'
			eProd.IsSelected = True
			eProd.ApplyProductChanges()
			eProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
			eProd.Product.Attr('SC_Platform_Entitlement').AssignValue('Entitlement')
			eProd.Product.Attr('SC_Description').AssignValue(eProdkey)
			for m_Dict in oE_Dict[eProdkey]:
				m_container = eProd.Product.GetContainerByName("SC_Asset")
				mProd = m_container.AddNewRow(True)
				mProd['Asset'] = '<*VALUE(SC_AssetName)*>'
				mProd['Description'] = 'Description'
				mProd['Quantity'] = '1'
				mProd['Price'] = str(m_Dict['Price'])
				mProd.IsSelected = True
				mProd.ApplyProductChanges()
				mProd.Product.Attr('SC_ItemEditFlag').AssignValue('110')
				if m_Dict['ResourceType'] == "A360 Contract Management" or m_Dict['ResourceType'] == "Service Contract Management":
					mProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
				mProd.Product.Attr('SC_AssetName').AssignValue('Resource Type')
				mProd.Product.Attr('SC_Description').AssignValue(m_Dict['ResourceType'])
				mProd.Product.Attr('SC_Price').AssignValue(str(m_Dict['Price']))
				mProd.Product.Attr('SC_Item_Cost').AssignValue(str(m_Dict['Cost']))
				mProd.Product.Attr('SC_Item_CostStatus').AssignValue('1')
				mProd.Product.Attr('SC_Item_MarginPercent').AssignValue(str(m_Dict['Margin']))
				mProd.Product.Attr('SC_Item_BlockDiscount').AssignValue(str(m_Dict['BlockDiscount']))
				mProd.Product.Attr('SC_Escalation_Price').AssignValue(str(m_Dict['Escalation_Price']))
				mProd.Product.Attr('SC_PY_Price').AssignValue(str(m_Dict['PY_ListPrice']))
				mProd.Product.Attr('ItemQuantity').AssignValue(str(m_Dict['Quantity'])) #CXCPQ-82629
				mProd.Product.Attr('SC_PY_SellPrice').AssignValue(str(m_Dict['PY_SellPrice']))
				mProd.Product.Attr('SC_SA_Price').AssignValue(str(m_Dict['SA_Price']))
				mProd.Product.Attr('SC_SR_Price').AssignValue(str(m_Dict['SR_Price']))
				if m_Dict['Expense'] > 0:
					ex_container = eProd.Product.GetContainerByName('SC_Asset')
					exRow = ex_container.AddNewRow(True)
					exRow['Asset'] = '<*VALUE(SC_AssetName)*>'
					exRow['Description'] = 'Description'
					exRow['Quantity'] = '1'
					exRow['Price'] = str(m_Dict['Price'])
					exRow.IsSelected = True
					exRow.ApplyProductChanges()
					ex_container.Calculate()
					exRow.Product.Attr('SC_ItemEditFlag').AssignValue('111')
					exRow.Product.Attr('SC_AssetName').AssignValue('Total Expense')
					exRow.Product.Attr('SC_Description').AssignValue('Other Expense')
					exRow.Product.Attr('SC_Price').AssignValue(str(m_Dict['Expense']))
					exRow.Product.Attr('SC_Item_MarginPercent').AssignValue('45')
					exRow.Product.Attr('SC_PY_Price').AssignValue(str(m_Dict['PY_Total_Expenses']))
					exRow.Product.Attr('SC_PY_SellPrice').AssignValue(str(m_Dict['PY_Total_Expenses']))
					exRow.Product.Attr('SC_Escalation_Price').AssignValue(str(m_Dict['Escalation_Price_TotalExpense']))
					exRow.Product.Attr('Extended Description').AssignValue('InfoMessage-Expenses related to Travel & Living')
				m_container.Calculate()	
			e_container.Calculate()
		p_container.Calculate()
def AddHwHR(lb_Dict, sProd, sProdkey, sc_ProdDist):
	sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
	sProd['Description'] = 'Description'
	sProd['Quantity'] = '1'
	sProd.IsSelected = True
	sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
	sProd.Product.Attr('SC_PartNumber').AssignValue(sProdkey)
	sProd.Product.Attr('SC_Description').AssignValue(sProdkey)
	sProd.ApplyProductChanges()
	for pProdkey in lb_Dict:
		p_container = sProd.Product.GetContainerByName("SC_Asset")
		pProd = p_container.AddNewRow(True)
		m_Dict = lb_Dict[pProdkey]
		pProd['Asset'] = '<*VALUE(SC_AssetName)*>'
		pProd['Description'] = 'Description'
		pProd['Quantity'] = '<*VALUE(ItemQuantity)*>'
		pProd['Price'] = str(m_Dict['Price'])
		pProd.IsSelected = True
		pProd.ApplyProductChanges()
		pProd.Product.Attr('SC_ItemEditFlag').AssignValue('110')
		pProd.Product.Attr('SC_AssetName').AssignValue('Service Product')
		pProd.Product.Attr('SC_Description').AssignValue(sProdkey)
		pProd.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
		pProd.Product.Attr('ItemQuantity').AssignValue('1')
		pProd.Product.Attr('SC_Price').AssignValue(str(m_Dict['Price']))
		pProd.Product.Attr('SC_Item_MarginPercent').AssignValue(str(m_Dict['Margin']))
		pProd.Product.Attr('SC_Item_Cost').AssignValue(str(m_Dict['Cost']))
		pProd.Product.Attr('SC_Item_CostStatus').AssignValue('1')
		pProd.Product.Attr('Extended Description').AssignValue('<h5>Entitlements</h5><ul><li>' + '</li><li>'.join(set(m_Dict['ExtDescription'])) + '</li></ul>')
		p_container.Calculate()
def addHWRWL(hh_Dict, sProd, sProdkey, sc_ProdDist):
	sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
	sProd['Description'] = 'Description'
	sProd['Quantity'] = '1'
	sProd.IsSelected = True
	sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
	sProd.Product.Attr('SC_PartNumber').AssignValue(sProdkey.split(' ')[0] + " "+ sProdkey.split(' ')[1])
	prd = sProdkey.split(' ')[0:2]
	sProd.Product.Attr('SC_Description').AssignValue(' '.join(prd))
	sProd.ApplyProductChanges()
	for pProdkey in hh_Dict:
		p_container = sProd.Product.GetContainerByName("SC_Asset")
		pProd = p_container.AddNewRow(True)
		pProd['Asset'] = '<*VALUE(SC_AssetName)*>'
		pProd['Description'] = 'Description'
		pProd['Quantity'] = '1'
		pProd.IsSelected = True
		pProd.ApplyProductChanges()
		pProd.Product.Attr('SC_AssetName').AssignValue('Service Product')
		pProd.Product.Attr('SC_Description').AssignValue(pProdkey)
		pProd.Product.Attr('SC_Price').AssignValue(str(hh_Dict[pProdkey]['total']))
		pProd.Product.Attr('SC_PriceImpact_RWL').AssignValue(str(hh_Dict[pProdkey]['PriceImpact']))
		pProd.Product.Attr('SC_ScopeChange_RWl').AssignValue(str(hh_Dict[pProdkey]['ScopeChange']))
		pProd.Product.Attr('SC_HWListPrice_RWL').AssignValue(str(hh_Dict[pProdkey]['hw_list_price']))
		pProd.Product.Attr('SC_PY_SellPrice').AssignValue(str(hh_Dict[pProdkey]['hw_PY_SellPrice']))
		pProd.Product.Attr('SC_PY_Price').AssignValue(str(hh_Dict[pProdkey]['prevListPrice']))
		pProd.Product.Attr('SC_Item_Cost').AssignValue(str(hh_Dict[pProdkey]['hw_cost_price']))
		pProd.Product.Attr('SC_Item_CostStatus').AssignValue('1')
		pProd.Product.Attr('SC_Item_MarginPercent').AssignValue(str((1-hh_Dict[pProdkey]['hw_cost_price']/hh_Dict[pProdkey]['total'])*100 if hh_Dict[pProdkey]['total'] else '0'))
		pProd.Product.Attr('SC_Escalation_Price').AssignValue(str(hh_Dict[pProdkey]['hw_Escalation_Price']))
		pProd.Product.Attr('SC_SA_Price').AssignValue(str(hh_Dict[pProdkey]['hw_SA_Price']))
		pProd.Product.Attr('SC_SR_Price').AssignValue(str(hh_Dict[pProdkey]['hw_SR_Price']))
		pProd.Product.Attr('ItemQuantity').AssignValue(str(hh_Dict[pProdkey]['iQuantity']))
		if str(hh_Dict[pProdkey]['iQuantity']) == '0':
			pProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
		else:
			pProd.Product.Attr('SC_ItemEditFlag').AssignValue('110')
		pProd.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
def addLSS(lbDict, sProd, sProdkey, sc_ProdDist):
    #lbDict = scDict[sProdkey]
    #SCprod_container = sProd.Product.GetContainerByName("SC_Asset")
    #sProd = SCprod_container.AddNewRow(True)
    sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
    sProd['Description'] = 'Description'
    sProd['Quantity'] = '1'
    sProd.IsSelected = True
    sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
    sProd.Product.Attr('SC_PartNumber').AssignValue('Local Support Standby')
    sProd.Product.Attr('SC_Description').AssignValue('Local Support Standby')
    cont_asse = sProd.Product.GetContainerByName('SC_Asset')
    prodrow = cont_asse.AddNewRow(True)
    prodrow['Asset'] = '<*VALUE(SC_AssetName)*>'
    prodrow['Description'] = 'Description'
    prodrow['Quantity'] = '1'
    prodrow.IsSelected = True
    prodrow.Product.Attr('SC_AssetName').AssignValue('Service Product')
    prodrow.Product.Attr('ItemQuantity').AssignValue(str(lbDict['Quantity']))
    prodrow.Product.Attr('SC_Price').AssignValue(str(lbDict['Price']))
    prodrow.Product.Attr('SC_Description').AssignValue('Local Support Standby')
    prodrow.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
    prodrow.Product.Attr('SC_Escalation_Price').AssignValue(str(lbDict['Escalation_Price']))
    prodrow.Product.Attr('SC_PY_Price').AssignValue(str(lbDict['PY_ListPrice']))
    prodrow.Product.Attr('SC_PY_SellPrice').AssignValue(str(lbDict['PY_SellPrice']))
    prodrow.Product.Attr('SC_SA_Price').AssignValue(str(lbDict['SA_Price']))
    prodrow.Product.Attr('SC_SR_Price').AssignValue(str(lbDict['SR_Price']))
    prodrow.Product.Attr('SC_Item_Cost').AssignValue(str(lbDict['Cost']))
    prodrow.Product.Attr('SC_Item_CostStatus').AssignValue('1')
    if str(lbDict['Quantity']) == '0':
        prodrow.Product.Attr('SC_ItemEditFlag').AssignValue('000')
        prodrow.Product.Attr('SC_Item_MarginPercent').AssignValue('0')
    else:
        prodrow.Product.Attr('SC_ItemEditFlag').AssignValue('000')
        prodrow.Product.Attr('SC_Item_MarginPercent').AssignValue(str((1-lbDict['Cost']/lbDict['Price'])*100 if lbDict['Price']>0 else 0))
    cont_asse.Calculate()
    #SCprod_container.Calculate()