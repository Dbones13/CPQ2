from GS_SC_UpdateProducts import *
from GS_SC_UpdateQuoteLineItems import *
from System.Collections.Specialized import OrderedDictionary
from GS_SC_QuoteLinesHelper import CL_SC_QuoteLinesHelper
SC_container = Product.GetContainerByName("SC_Asset")
SC_container.Clear()
SC_container.Calculate()
oneTimeProducts = []

def GetServiceProductCode(prodName):
	prodCode = SqlHelper.GetFirst("SELECT ProductCode FROM CT_SC_Entitlements_Data WHERE ServiceProduct='{}'".format(prodName))
	return prodCode.ProductCode if prodCode else ''

def removeOneTimeProducts(pc_container):
	deleteStatus = 0
	if oneTimeProducts:
		modulesList = [mod.get('module') for mod in oneTimeProducts]
		for row in pc_container.Rows:
			if row.Product.Attr('SC_PartNumber').GetValue() in modulesList:
				removeIndex = []
				cc_container=row.Product.GetContainerByName("SC_Asset")
				for crow in cc_container.Rows:
					for prod in oneTimeProducts:
						if crow.Product.Attributes.GetByName(prod['attName']) and prod['attValue'] == crow.Product.Attr(prod['attName']).GetValue():
							removeIndex.append(crow.RowIndex)
						kp = crow.Product.Attributes.GetByName('SC_Asset')
						if kp:
							dc_container=crow.Product.GetContainerByName("SC_Asset")
							removeDIndex = []
							for drow in dc_container.Rows:
								if drow.Product.Attributes.GetByName(prod['attName']) and prod['attValue'] == drow.Product.Attr(prod['attName']).GetValue():
									dc_container.DeleteRow(drow.RowIndex)
									deleteStatus = 1
									dc_container.Calculate()
									break
				if removeIndex:
					removeIndex.sort(reverse=True)
					for delindex in removeIndex:
						cc_container.DeleteRow(delindex)
						deleteStatus = 1
					cc_container.Calculate()
	pc_container.Calculate()
	return deleteStatus, pc_container

def UpdateMultiYearPricing(pc_container, scFDist, Year = None, prodDict = None):
	for row in pc_container.Rows:
		cc_container=row.Product.GetContainerByName("SC_Asset")
		if row.Product.Attributes.GetByName('SC_Year') and 'Year-' in row.Product.Attr('SC_Year').GetValue():
			Year = row.Product.Attr('SC_Year').GetValue()
		if row.Product.Attributes.GetByName('SC_PartNumber') and Year and row.Product.Attr('SC_PartNumber').GetValue() in scFDist:
			if Year in scFDist[row.Product.Attr('SC_PartNumber').GetValue()]:
				prodDict = scFDist[row.Product.Attr('SC_PartNumber').GetValue()][Year]
		if cc_container != None:
			UpdateMultiYearPricing(cc_container, scFDist, Year, prodDict)
		else:
			if prodDict and row.Product.Attr('SC_Description').GetValue() in prodDict:
				row.Product.Attr('SC_Price').AssignValue(str(prodDict[row.Product.Attr('SC_Description').GetValue()]['ListPrice']))
				row.Product.Attr('SC_Item_Cost').AssignValue(str(prodDict[row.Product.Attr('SC_Description').GetValue()]['CostPrice']))
				row.ApplyProductChanges()
				pc_container.Calculate()

qLineHelper = CL_SC_QuoteLinesHelper(Quote, TagParserQuote, None, Session)
qLineHelper.setSCLineItemsData()
pCont = Product.GetContainerByName('Service Contract Modules')
SC_ProductsType = {}
for pcrow in pCont.Rows:
	SC_ProductsType[ pcrow['Product_Name'] if pcrow['Module'] == 'Generic Module' else pcrow['Module']] = pcrow['Type']
productlist, scDict, prodYearDict, scFyDict = GenerateProdDictFromContainer(pCont)
ps=str(scDict)
SC_container = Product.GetContainerByName("SC_Asset")
yearList = []
if Product.Attr('SC_Contract_StartDate').GetValue() and Product.Attr('SC_Contract_EndDate').GetValue():
	SC_CF_ContractEndDate = Quote.GetGlobal('SC_CF_ContractEndDate')
	SC_CF_ContractEndDate = DateTime.Parse(SC_CF_ContractEndDate) if (SC_CF_ContractEndDate !='' and SC_CF_ContractEndDate!= None) else None
	Contract_Ed_Dt = UserPersonalizationHelper.CovertToDate(Quote.GetCustomField('EGAP_Contract_End_Date').Content) if Quote.GetCustomField('EGAP_Contract_End_Date').Content else ''
	if Quote.GetCustomField("Quote Type").Content == 'Contract Renewal' and ((SC_CF_ContractEndDate and SC_CF_ContractEndDate == Contract_Ed_Dt) or Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content =='True'):
		yearList = sc_yearlist(UserPersonalizationHelper.CovertToDate(Quote.GetCustomField('SC_CF_CURANNDELSTDT').Content),  UserPersonalizationHelper.CovertToDate(Quote.GetCustomField('SC_CF_CURANNDELENDT').Content))
	else:
		yearList = sc_yearlist(UserPersonalizationHelper.CovertToDate(Quote.GetCustomField('EGAP_Contract_Start_Date').Content),  UserPersonalizationHelper.CovertToDate(Quote.GetCustomField('EGAP_Contract_End_Date').Content))
if scDict and yearList:
	SC_container.Clear()
	yProd = SC_container.AddNewRow(True)
	yProd['Asset'] = '<*VALUE(SC_Year)*>'
	yProd['Description'] = 'Year-1'
	yProd['Quantity'] = '1'
	yProd.IsSelected = True
	yProd.ApplyProductChanges()
	yProd.Product.Attr('SC_ItemEditFlag').AssignValue('0000')
	yProd.Product.Attr('SC_Description').AssignValue(yearList[0])
	yProd.Product.Attr('SC_Year').AssignValue('Year-1')
	SCprod_container = yProd.Product.GetContainerByName("SC_Asset")
	genric_prd =  SqlHelper.GetList("SELECT distinct Product_Type FROM CT_SC_Entitlements_Data WHERE Status='Active' and Module_Name ='Generic Module'")
	gen_product = [prd.Product_Type for prd in genric_prd]
	for sc_ProdDist in productlist:
		sProdkey = sc_ProdDist['ProductName']
		if sProdkey in ('SESP Value Remote Plus', 'SESP Value Plus', 'Value Shield', 'SESP Software Flex', 'SESP Support Flex','System Evolution Program'):
			sesp_Dict = scDict[sProdkey]
			sProd = SCprod_container.AddNewRow(True)
			AddSESP(sesp_Dict, sProd, sProdkey, sc_ProdDist)
		elif sProdkey == 'Enabled Services SESP':
			SC_ProductsType['Enabled Services'] = SC_ProductsType['Solution Enhancement Support Program']
			lbDict = scDict[sProdkey]
			desc2 = ''
			if lbDict.get('Enabled Services - Essential'):
				desc2 = 'Enabled Services - Essential'
			elif lbDict.get('Enabled Services - Enhanced'):
				desc2 = 'Enabled Services - Enhanced'
			sProd = SCprod_container.AddNewRow(True)
			sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
			sProd['Description'] = 'Description'
			sProd['Quantity'] = '1'
			sProd.IsSelected = True
			sProd.Product.Attr('SC_PartNumber').AssignValue('Enabled Services')
			sProd.Product.Attr('SC_Description').AssignValue('Enabled Services')
			sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
			sProd.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
			for p_Dict in lbDict[desc2]:
				p_container = sProd.Product.GetContainerByName('SC_Asset')
				pProd = p_container.AddNewRow(True)
				pProd['Asset'] = '<*VALUE(SC_AssetName)*>'
				pProd['Description'] = 'Description'
				pProd['Quantity'] = '<*VALUE(ItemQuantity)*>'
				pProd['Price'] = '<*VALUE(SC_Price)*>'
				pProd.IsSelected = True
				if str(p_Dict['ServiceProduct']) != 'Matrikon License':
					pProd.Product.Attr('SC_AssetName').AssignValue('Enabled Services')
					pProd.Product.Attr('SC_Description').AssignValue(str(p_Dict['ServiceProduct']))
					pProd.Product.Attr('SC_ItemEditFlag').AssignValue('111')
				else:
					pProd.Product.Attr('SC_AssetName').AssignValue('Matrikon License')
					pProd.Product.Attr('SC_Description').AssignValue('License')
					pProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
					oneTimeProducts.append({'module': 'Enabled Services', 'attName': 'SC_AssetName', 'attValue': 'Matrikon License'})
				pProd.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
				pProd.Product.Attr('SC_Price').AssignValue(str(p_Dict['Price']))
				pProd.Product.Attr('ItemQuantity').AssignValue(str(p_Dict['Quantity']))
				pProd.Product.Attr('SC_Item_MarginPercent').AssignValue('25')
				pProd.Product.Attr('SC_Escalation_Price').AssignValue(str(p_Dict['Escalation_Price']))
				pProd.Product.Attr('SC_PY_Price').AssignValue(str(p_Dict['PY_ListPrice']))
				pProd.Product.Attr('SC_PY_SellPrice').AssignValue(str(p_Dict['PY_SellPrice']))
				pProd.Product.Attr('SC_SA_Price').AssignValue(str(p_Dict['SA_Price']))
				pProd.Product.Attr('SC_SR_Price').AssignValue(str(p_Dict['SR_Price']))
				p_container.Calculate()
			SCprod_container.Calculate()
		elif sProdkey == "Parts Management":
			Quote.GetCustomField("SC_CF_IS_STATUS_CHECK").Content = '1'
			pp_Dict = scDict[sProdkey]
			sProd = SCprod_container.AddNewRow(True)
			AddParts(pp_Dict, sProd, sProdkey, sc_ProdDist)
		elif sProdkey == "Labor":
			lb_Dict = scDict[sProdkey]
			sProd = SCprod_container.AddNewRow(True)
			AddLabor(lb_Dict, sProd, sProdkey, sc_ProdDist)
		elif sProdkey == "BGP inc Matrikon" or sProdkey == "Cyber" or sProdkey in gen_product :
			pp_Dict = scDict[sProdkey]
			sProd = SCprod_container.AddNewRow(True)
			sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
			sProd['Description'] = 'Description'
			sProd['Quantity'] = '1'
			sProd.IsSelected = True
			sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
			sProd.Product.Attr('SC_PartNumber').AssignValue(sProdkey)
			sProd.Product.Attr('SC_Description').AssignValue(sProdkey)
			sProd.ApplyProductChanges()
			for pProdkey in pp_Dict:
				p_container = sProd.Product.GetContainerByName("SC_Asset")
				pProd = p_container.AddNewRow(True)
				pProd['Asset'] = '<*VALUE(SC_AssetName)*>'
				pProd['Description'] = 'Description'
				pProd['Quantity'] = '1'
				pProd.IsSelected = True
				pProd.ApplyProductChanges()
				pProd.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
				pProd.Product.Attr('SC_AssetName').AssignValue('Service Product')
				pProd.Product.Attr('SC_Description').AssignValue(pProdkey)
				pProd.Product.Attr('SC_Price').AssignValue(str(pp_Dict[pProdkey]['Price']))
				pProd.Product.Attr('SC_Item_Cost').AssignValue(str(pp_Dict[pProdkey]['Cost']))
				pProd.Product.Attr('SC_Item_CostStatus').AssignValue('1')
				pProd.Product.Attr('SC_Item_MarginPercent').AssignValue(str((1-pp_Dict[pProdkey]['Cost']/pp_Dict[pProdkey]['Price'])*100 if pp_Dict[pProdkey]['Price']>0 else 0))
				pProd.Product.Attr('ItemQuantity').AssignValue(str(pp_Dict[pProdkey]['Quantity']))
				pProd.Product.Attr('SC_Escalation_Price').AssignValue(str(pp_Dict[pProdkey]['Escalation_Price']))
				pProd.Product.Attr('SC_PY_Price').AssignValue(str(pp_Dict[pProdkey]['PY_ListPrice']))
				pProd.Product.Attr('SC_PY_SellPrice').AssignValue(str(pp_Dict[pProdkey]['PY_SellPrice']))
				pProd.Product.Attr('SC_SA_Price').AssignValue(str(pp_Dict[pProdkey]['SA_Price']))
				pProd.Product.Attr('SC_SR_Price').AssignValue(str(pp_Dict[pProdkey]['SR_Price']))
				if str(pp_Dict[pProdkey]['Quantity']) == '0':
					pProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
				else:
					pProd.Product.Attr('SC_ItemEditFlag').AssignValue('110')
		elif sProdkey == "QCS 4.0":
			QC_Dict = scDict[sProdkey]
			sProd = SCprod_container.AddNewRow(True)
			sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
			sProd['Description'] = 'Description'
			sProd['Quantity'] = '1'
			sProd.IsSelected = True
			sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
			sProd.Product.Attr('SC_PartNumber').AssignValue('QCS 4.0')
			sProd.Product.Attr('SC_Description').AssignValue('QCS 4.0')
			sProd.ApplyProductChanges()
			for pProdkey in QC_Dict.Keys:
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
				for m_Dict in QC_Dict[pProdkey]:
					m_container = pProd.Product.GetContainerByName("SC_Asset")
					mProd = m_container.AddNewRow(True)
					mProd['Asset'] = '<*VALUE(SC_AssetName)*>'
					mProd['Description'] = 'Description'
					mProd['Quantity'] = str(m_Dict["Quantity"])
					mProd['Price'] = str(m_Dict["Price"])
					mProd.IsSelected = True
					mProd.ApplyProductChanges()
					m_container.Calculate()
					mProd.Product.Attr('ItemQuantity').AssignValue(str(m_Dict["Quantity"]))
					mProd.Product.Attr('SC_Escalation_Price').AssignValue(str(m_Dict["Escalation_Price"]))
					mProd.Product.Attr('SC_Price').AssignValue(str(m_Dict["Price"]))
					mProd.Product.Attr('SC_PY_Price').AssignValue(str(m_Dict["PY_ListPrice"]))
					mProd.Product.Attr('SC_PY_SellPrice').AssignValue(str(m_Dict["PY_SellPrice"]))
					mProd.Product.Attr('SC_SR_Price').AssignValue(str(m_Dict["SR_Price"]))
					mProd.Product.Attr('SC_SA_Price').AssignValue(str(m_Dict["SA_Price"]))
					mProd.Product.Attr('SC_AssetName').AssignValue('Entitlement')
					mProd.Product.Attr('SC_Description').AssignValue(str(m_Dict["Entitlement"]))
					if 'One-time Service Charge' in str(m_Dict["Entitlement"]):
						oneTimeProducts.append({'module': 'QCS 4.0', 'attName': 'SC_Description', 'attValue': str(m_Dict["Entitlement"])})
					if str(m_Dict["Quantity"]) == '0':
						mProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
						mProd.Product.Attr('SC_Item_MarginPercent').AssignValue('0')
					else:
						mProd.Product.Attr('SC_ItemEditFlag').AssignValue('111')
						mProd.Product.Attr('SC_Item_MarginPercent').AssignValue('45')
				p_container.Calculate()
		elif sProdkey == "Third Party Services":
			tp_Dict = scDict[sProdkey]
			sProd = SCprod_container.AddNewRow(True)
			sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
			sProd['Description'] = 'Description'
			sProd['Quantity'] = '1'
			sProd.IsSelected = True
			sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
			sProd.Product.Attr('SC_PartNumber').AssignValue('Third Party Services')
			sProd.Product.Attr('SC_Description').AssignValue('Third Party Services')
			sProd.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
			sProd.ApplyProductChanges()
			for pProdkey in tp_Dict:
				p_container = sProd.Product.GetContainerByName("SC_Asset")
				pProd = p_container.AddNewRow(True)
				pProd['Asset'] = '<*VALUE(SC_AssetName)*>'
				pProd['Description'] = 'Description'
				pProd['Quantity'] = '1'
				pProd.IsSelected = True
				pProd.ApplyProductChanges()
				pProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
				pProd.Product.Attr('SC_AssetName').AssignValue('Entitlement')
				pProd.Product.Attr('SC_Description').AssignValue(pProdkey)
				pProd.Product.Attr('ItemQuantity').AssignValue(str(tp_Dict[pProdkey]['Quantity']))
				pProd.Product.Attr('SC_Price').AssignValue(str(tp_Dict[pProdkey]['Price']))
				pProd.Product.Attr('SC_Item_Cost').AssignValue(str(tp_Dict[pProdkey]['Cost']))
				pProd.Product.Attr('SC_Item_CostStatus').AssignValue('1')
				tp_Dict[pProdkey]['Cost'] = float(tp_Dict[pProdkey]['Cost']) if tp_Dict[pProdkey]['Cost'] > 0 else 0.0
				tp_Dict[pProdkey]['Price'] = float(tp_Dict[pProdkey]['Price']) if tp_Dict[pProdkey]['Price'] > 0 else 0.0
				ItemMagrinPercentage = ((1-tp_Dict[pProdkey]['Cost']/tp_Dict[pProdkey]['Price'])*100 if tp_Dict[pProdkey]['Price']>0 else 0.0)
				pProd.Product.Attr('SC_Item_MarginPercent').AssignValue(str(ItemMagrinPercentage))
				#pProd.Product.Attr('SC_Item_MarginPercent').AssignValue(str((1-tp_Dict[pProdkey]['Cost']/tp_Dict[pProdkey]['Price'])*100 if tp_Dict[pProdkey]['Price']>0 else 0)) since it was throwing str cannot divide with string when the value was 0
				pProd.Product.Attr('SC_Escalation_Price').AssignValue(str(tp_Dict[pProdkey]['Escalation_Price']))
				pProd.Product.Attr('SC_PY_Price').AssignValue(str(tp_Dict[pProdkey]['PY_ListPrice']))
				pProd.Product.Attr('SC_PY_SellPrice').AssignValue(str(tp_Dict[pProdkey]['PY_SellPrice']))
				pProd.Product.Attr('SC_SA_Price').AssignValue(str(tp_Dict[pProdkey]['SA_Price']))
				pProd.Product.Attr('SC_SR_Price').AssignValue(str(tp_Dict[pProdkey]['SR_Price'])) 
			p_container.Calculate()
		elif sProdkey == "MES Performix":
			tp_Dict = scDict[sProdkey]
			mProd = SCprod_container.AddNewRow(True)
			mProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
			mProd['Description'] = 'Description'
			mProd['Quantity'] = '1'
			mProd.IsSelected = True
			mProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
			mProd.Product.Attr('SC_PartNumber').AssignValue('MES Performix')
			mProd.Product.Attr('SC_Description').AssignValue('MES Performix - Model')
			mProd.ApplyProductChanges()
			for pProdkey in tp_Dict:
				m_container = mProd.Product.GetContainerByName("SC_Asset")
				sProd = m_container.AddNewRow(True)
				sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
				sProd['Description'] = 'Description'
				sProd['Quantity'] = str(tp_Dict[pProdkey]['Quantity'])
				sProd.IsSelected = True
				sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
				sProd.Product.Attr('SC_PartNumber').AssignValue('Service Product')
				sProd.Product.Attr('SC_Description').AssignValue(pProdkey)
				sProd.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
				sProd.ApplyProductChanges()
				p_container = sProd.Product.GetContainerByName("SC_Asset")
				pProd = p_container.AddNewRow(True)
				pProd['Asset'] = '<*VALUE(SC_AssetName)*>'
				pProd['Description'] = 'Description'
				pProd['Quantity'] = str(tp_Dict[pProdkey]['Quantity'])
				pProd.IsSelected = True
				pProd.ApplyProductChanges()
				pProd.Product.Attr('ItemQuantity').AssignValue(str(tp_Dict[pProdkey]['Quantity']))
				pProd.Product.Attr('SC_AssetName').AssignValue('MES Models')
				pProd.Product.Attr('SC_Description').AssignValue('MES Models')
				pProd.Product.Attr('SC_Price').AssignValue(str(tp_Dict[pProdkey]['Price']))
				pProd.Product.Attr('SC_Escalation_Price').AssignValue(str(tp_Dict[pProdkey]['Escalation_Price']))
				pProd.Product.Attr('SC_PY_Price').AssignValue(str(tp_Dict[pProdkey]['PY_ListPrice']))
				pProd.Product.Attr('SC_PY_SellPrice').AssignValue(str(tp_Dict[pProdkey]['PY_SellPrice']))
				pProd.Product.Attr('SC_SA_Price').AssignValue(str(tp_Dict[pProdkey]['SA_Price']))
				pProd.Product.Attr('SC_SR_Price').AssignValue(str(tp_Dict[pProdkey]['SR_Price']))
				if str(tp_Dict[pProdkey]['Quantity']) == '0':
					pProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
					pProd.Product.Attr('SC_Item_MarginPercent').AssignValue('0')
				else:
					pProd.Product.Attr('SC_ItemEditFlag').AssignValue('111')
					pProd.Product.Attr('SC_Item_MarginPercent').AssignValue('45')
			p_container.Calculate()
			m_container.Calculate()
		elif sProdkey == "Honeywell Digital Prime":
			tp_Dict = scDict[sProdkey]
			for pProdkey in tp_Dict:
				sProd = SCprod_container.AddNewRow(True)
				sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
				sProd['Description'] = 'Description'
				sProd['Quantity'] = '1'
				sProd.IsSelected = True
				sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
				sProd.Product.Attr('SC_PartNumber').AssignValue('Honeywell Digital Prime')
				sProd.Product.Attr('SC_Description').AssignValue(pProdkey)
				sProd.ApplyProductChanges()
				p_container = sProd.Product.GetContainerByName("SC_Asset")
				pProd = p_container.AddNewRow(True)
				pProd['Asset'] = '<*VALUE(SC_AssetName)*>'
				pProd['Description'] = 'Description'
				pProd['Quantity'] = '1'
				pProd.IsSelected = True
				pProd.ApplyProductChanges()
				pProd.Product.Attr('SC_AssetName').AssignValue('Service Product')
				pProd.Product.Attr('SC_Description').AssignValue(pProdkey)
				pProd.Product.Attr('SC_Price').AssignValue(str(tp_Dict[pProdkey]['Price']))
				pProd.Product.Attr('SC_Item_Cost').AssignValue(str(tp_Dict[pProdkey]['Price'] * 0.75))
				pProd.Product.Attr('ItemQuantity').AssignValue(str(tp_Dict[pProdkey]['Quantity']))
				pProd.Product.Attr('SC_Escalation_Price').AssignValue(str(tp_Dict[pProdkey]['Escalation_Price']))
				pProd.Product.Attr('SC_SR_Price').AssignValue(str(tp_Dict[pProdkey]['SR_Price']))
				pProd.Product.Attr('SC_PY_Price').AssignValue(str(tp_Dict[pProdkey]['PY_ListPrice']))
				pProd.Product.Attr('SC_PY_SellPrice').AssignValue(str(tp_Dict[pProdkey]['PY_SellPrice']))
				pProd.Product.Attr('SC_SA_Price').AssignValue(str(tp_Dict[pProdkey]['SA_Price']))
				pProd.Product.Attr('SC_Item_CostStatus').AssignValue('1')
				if str(tp_Dict[pProdkey]['Quantity']) == '0':
					pProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
					#pProd.Product.Attr('SC_Item_MarginPercent').AssignValue('0')
				else:
					pProd.Product.Attr('SC_ItemEditFlag').AssignValue('101')
					#pProd.Product.Attr('SC_Item_MarginPercent').AssignValue('25')
				pProd.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
			p_container.Calculate()
		## RQUP
		elif sProdkey == "Experion Extended Support - RQUP ONLY":
			RQ_Dict = scDict[sProdkey]
			sProd = SCprod_container.AddNewRow(True)
			sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
			sProd['Description'] = 'Description'
			sProd['Quantity'] = '1'
			sProd.IsSelected = True
			sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
			sProd.Product.Attr('SC_PartNumber').AssignValue('Experion Extended Support - RQUP ONLY')
			sProd.Product.Attr('SC_Description').AssignValue('Experion Extended Support - RQUP ONLY')
			sProd.ApplyProductChanges()
			for pProdkey in RQ_Dict:
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
				pProd.Product.Attr('Extended Description').AssignValue('Remote GTAC Support')
				pProd.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
				oE_Dict = RQ_Dict[pProdkey]
				for eProdkey in oE_Dict:
					e_container = pProd.Product.GetContainerByName("SC_Asset")
					eProd = e_container.AddNewRow(True)
					eProd['Asset'] = '<*VALUE(SC_Platform_Entitlement)*>'
					eProd['Description'] = 'Description'
					eProd['Quantity'] = '1'
					eProd.IsSelected = True
					eProd.ApplyProductChanges()
					eProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
					eProd.Product.Attr('SC_Platform_Entitlement').AssignValue('Asset')
					eProd.Product.Attr('SC_Description').AssignValue(eProdkey)
					for m_Dict in oE_Dict[eProdkey]:
						m_container = eProd.Product.GetContainerByName("SC_Asset")
						mProd = m_container.AddNewRow(True)
						mProd['Asset'] = '<*VALUE(SC_AssetName)*>'
						mProd['Description'] = 'Description'
						mProd['Quantity'] = '1'
						mProd['Price'] = str(m_Dict['List_price'])
						mProd.IsSelected = True
						mProd.ApplyProductChanges()
						mProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
						mProd.Product.Attr('SC_AssetName').AssignValue('Asset')
						mProd.Product.Attr('SC_Description').AssignValue(m_Dict['MSID'])
						mProd.Product.Attr('SC_Price').AssignValue(str(m_Dict['List_price']))
						mProd.Product.Attr('ItemQuantity').AssignValue(str(m_Dict['Quantity']))
						mProd.Product.Attr('SC_Item_Cost').AssignValue(str(m_Dict['Cost_price']))
						mProd.Product.Attr('SC_Escalation_Price').AssignValue(str(m_Dict['Escalation_Price']))
						mProd.Product.Attr('SC_PY_Price').AssignValue(str(m_Dict['PY_ListPrice']))
						mProd.Product.Attr('SC_PY_SellPrice').AssignValue(str(m_Dict['PY_SellPrice']))
						mProd.Product.Attr('SC_SA_Price').AssignValue(str(m_Dict['SA_Price']))
						mProd.Product.Attr('SC_SR_Price').AssignValue(str(m_Dict['SR_Price']))
						mProd.Product.Attr('SC_Item_CostStatus').AssignValue('1')
						m_container.Calculate()	
					e_container.Calculate()
				p_container.Calculate()
		elif sProdkey == "Workforce Excellence Program":
			lb_Dict = scDict[sProdkey]
			sProd = SCprod_container.AddNewRow(True)
			sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
			sProd['Description'] = 'Description'
			sProd['Quantity'] = '1'
			sProd.IsSelected = True
			sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
			sProd.Product.Attr('SC_PartNumber').AssignValue('Workforce Excellence Program')
			sProd.Product.Attr('SC_Description').AssignValue('Workforce Excellence Program')
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
				m_Dict = lb_Dict[pProdkey]
				sp_Entitlements = []
				for mProdData in m_Dict:
					m_container = pProd.Product.GetContainerByName("SC_Asset")
					mProd = m_container.AddNewRow(True)
					mProd['Asset'] = '<*VALUE(SC_AssetName)*>'
					mProd['Description'] = 'Description'
					mProd['Quantity'] = '1'
					mProd['Price'] = str(mProdData['ListPrice'])
					mProd.IsSelected = True
					mProd.ApplyProductChanges()
					m_container.Calculate()
					sp_Entitlements.extend(mProdData['ExtDescription'])
					mProd.Product.Attr('SC_AssetName').AssignValue('Offering Name')
					mProd.Product.Attr('SC_Description').AssignValue(mProdData['OfferingName'])
					mProd.Product.Attr('SC_Price').AssignValue(str(mProdData['ListPrice']))
					mProd.Product.Attr('SC_Escalation_Price').AssignValue(str(mProdData['Escalation_Price']))
					mProd.Product.Attr('ItemQuantity').AssignValue(str(mProdData['Quantity'])) #CXCPQ-82646
					mProd.Product.Attr('SC_PY_Price').AssignValue(str(mProdData['PY_ListPrice']))
					mProd.Product.Attr('SC_PY_SellPrice').AssignValue(str(mProdData['PY_SellPrice']))
					mProd.Product.Attr('SC_SA_Price').AssignValue(str(mProdData['SA_Price']))
					mProd.Product.Attr('SC_SR_Price').AssignValue(str(mProdData['SR_Price']))
					if str(mProdData['Quantity']) == '0':
						mProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
						mProd.Product.Attr('SC_Item_MarginPercent').AssignValue('0')
					else:
						if mProdData['OfferingName'].lower() == 'Operations and Maintenance'.lower():
							mProd.Product.Attr('SC_ItemEditFlag').AssignValue('111')
							mProd.Product.Attr('SC_Item_MarginPercent').AssignValue('25')
						else:
							mProd.Product.Attr('SC_ItemEditFlag').AssignValue('110')
							mProd.Product.Attr('SC_Item_Cost').AssignValue(str(mProdData['CostPrice']))
							mProd.Product.Attr('SC_Item_CostStatus').AssignValue('1')
				pProd.Product.Attr('Extended Description').AssignValue('<h5>Entitlements</h5><ul><li>' + '</li><li>'.join(set(sp_Entitlements)) + '</li></ul>')
				p_container.Calculate()
		elif sProdkey == "Trace":
			lb_Dict = scDict[sProdkey]
			sProd = SCprod_container.AddNewRow(True)
			sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
			sProd['Description'] = 'Description'
			sProd['Quantity'] = '1'
			sProd.IsSelected = True
			sProd.Product.Attr('SC_PartNumber').AssignValue('Trace')
			sProd.Product.Attr('SC_Description').AssignValue('Trace Service')
			sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
			sProd.ApplyProductChanges()
			for pProdkey in lb_Dict:
				p_container = sProd.Product.GetContainerByName("SC_Asset")
				pProd = p_container.AddNewRow(True)
				m_Dict = lb_Dict[pProdkey]
				pProd['Asset'] = '<*VALUE(SC_AssetName)*>'
				pProd['Description'] = 'Description'
				pProd['Quantity'] = '<*VALUE(ItemQuantity)*>'
				pProd['Price'] = str(m_Dict['ListPrice'])
				pProd.IsSelected = True
				pProd.ApplyProductChanges()
				pProd.Product.Attr('SC_AssetName').AssignValue('Service Product')
				pProd.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
				pProd.Product.Attr('SC_Description').AssignValue(pProdkey)
				#pProd.Product.Attr('PRD_PartNumber').AssignValue(GetServiceProductCode(pProdkey))
				pProd.Product.Attr('ItemQuantity').AssignValue(str(m_Dict['Quantity']))
				pProd.Product.Attr('SC_Price').AssignValue(str(m_Dict['ListPrice']))
				pProd.Product.Attr('SC_Item_Cost').AssignValue(str(m_Dict['CostPrice']))
				pProd.Product.Attr('SC_Item_CostStatus').AssignValue('1')
				pProd.Product.Attr('SC_Item_MarginPercent').AssignValue(str((1-m_Dict['CostPrice']/m_Dict['ListPrice'])*100 if m_Dict['ListPrice'] else '0'))
				pProd.Product.Attr('Extended Description').AssignValue('<h5>Entitlements</h5><ul><li>' + '</li><li>'.join(set(m_Dict['ExtDescription'])) + '</li></ul>')
				pProd.Product.Attr('SC_Escalation_Price').AssignValue(str(m_Dict['Escalation_Price']))
				pProd.Product.Attr('SC_PY_Price').AssignValue(str(m_Dict['PY_ListPrice']))
				pProd.Product.Attr('SC_PY_SellPrice').AssignValue(str(m_Dict['PY_SellPrice']))
				pProd.Product.Attr('SC_SA_Price').AssignValue(str(m_Dict['SA_Price']))
				pProd.Product.Attr('SC_SR_Price').AssignValue(str(m_Dict['SR_Price']))
				if str(m_Dict['Quantity']) == '0':
					pProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
				else:
					pProd.Product.Attr('SC_ItemEditFlag').AssignValue('110')
				p_container.Calculate()
			SCprod_container.Calculate()
		elif sProdkey == "Hardware Warranty" or sProdkey == "Hardware Refresh":
			lb_Dict = scDict[sProdkey]
			sProd = SCprod_container.AddNewRow(True)
			AddHwHR(lb_Dict, sProd, sProdkey, sc_ProdDist)
		elif sProdkey == "Local Support Standby":
			lssDict = scDict[sProdkey]
			sProd = SCprod_container.AddNewRow(True)
			addLSS(lssDict, sProd, sProdkey, sc_ProdDist)
			SCprod_container.Calculate()
		elif sProdkey == 'Enabled Services':
			lbDict = scDict[sProdkey]
			desc2 = ''
			if lbDict.get('Enabled Services - Essential'):
				desc2 = 'Enabled Services - Essential'
			elif lbDict.get('Enabled Services - Enhanced'):
				desc2 = 'Enabled Services - Enhanced'
			sProd = SCprod_container.AddNewRow(True)
			sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
			sProd['Description'] = 'Description'
			sProd['Quantity'] = '1'
			sProd.IsSelected = True
			sProd.Product.Attr('SC_PartNumber').AssignValue('Enabled Services')
			sProd.Product.Attr('SC_Description').AssignValue('Enabled Services')
			sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
			for p_Dict in lbDict[desc2]:
				p_container = sProd.Product.GetContainerByName('SC_Asset')
				pProd = p_container.AddNewRow(True)
				pProd['Asset'] = '<*VALUE(SC_AssetName)*>'
				pProd['Description'] = 'Description'
				pProd['Quantity'] = '<*VALUE(ItemQuantity)*>'
				pProd['Price'] = '<*VALUE(SC_Price)*>'
				pProd.IsSelected = True
				if str(p_Dict['ServiceProduct']) != 'Matrikon License':
					pProd.Product.Attr('SC_AssetName').AssignValue('Enabled Services')
					pProd.Product.Attr('SC_Description').AssignValue(str(p_Dict['ServiceProduct']))
					pProd.Product.Attr('SC_ItemEditFlag').AssignValue('111')
				else:
					pProd.Product.Attr('SC_AssetName').AssignValue('Matrikon License')
					pProd.Product.Attr('SC_Description').AssignValue('License')
					pProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
					oneTimeProducts.append({'module': 'Enabled Services', 'attName': 'SC_AssetName', 'attValue': 'Matrikon License'})
				pProd.Product.Attr('SC_Price').AssignValue(str(p_Dict['Price']))
				pProd.Product.Attr('ItemQuantity').AssignValue(str(p_Dict['Quantity']))
				pProd.Product.Attr('SC_Item_MarginPercent').AssignValue('25')
				pProd.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
				pProd.Product.Attr('SC_Escalation_Price').AssignValue(str(p_Dict['Escalation_Price']))
				pProd.Product.Attr('SC_PY_Price').AssignValue(str(p_Dict['PY_ListPrice']))
				pProd.Product.Attr('SC_PY_SellPrice').AssignValue(str(p_Dict['PY_SellPrice']))
				pProd.Product.Attr('SC_SA_Price').AssignValue(str(p_Dict['SA_Price']))
				pProd.Product.Attr('SC_SR_Price').AssignValue(str(p_Dict['SR_Price']))
				p_container.Calculate()
			SCprod_container.Calculate()
		elif sProdkey == 'Condition Based Maintenance':
			lbDict = scDict[sProdkey]
			sProd = SCprod_container.AddNewRow(True)
			sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
			sProd['Description'] = 'Description'
			sProd['Quantity'] = '1'
			sProd.IsSelected = True
			sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
			sProd.Product.Attr('SC_PartNumber').AssignValue('Module')
			sProd.Product.Attr('SC_Description').AssignValue('Condition Based Maintenance')
			cont_asse = sProd.Product.GetContainerByName('SC_Asset')
			prodrow = cont_asse.AddNewRow(True)
			prodrow['Asset'] = '<*VALUE(SC_AssetName)*>'
			prodrow['Description'] = 'Description'
			prodrow['Quantity'] = '1'
			prodrow.IsSelected = True
			prodrow.Product.Attr('SC_AssetName').AssignValue('Service Product')
			prodrow.Product.Attr('ItemQuantity').AssignValue(str(lbDict['Quantity']))
			prodrow.Product.Attr('SC_Price').AssignValue(str(lbDict['Price']))
			prodrow.Product.Attr('SC_Description').AssignValue('Condition Based Maintenance')
			prodrow.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
			prodrow.Product.Attr('SC_Escalation_Price').AssignValue(str(lbDict['Escalation_Price']))
			prodrow.Product.Attr('SC_PY_Price').AssignValue(str(lbDict['PY_ListPrice']))
			prodrow.Product.Attr('SC_PY_SellPrice').AssignValue(str(lbDict['PY_SellPrice']))
			prodrow.Product.Attr('SC_SA_Price').AssignValue(str(lbDict['SA_Price']))
			prodrow.Product.Attr('SC_SR_Price').AssignValue(str(lbDict['SR_Price']))
			if str(lbDict['Quantity']) == '0':
				prodrow.Product.Attr('SC_ItemEditFlag').AssignValue('000')
				prodrow.Product.Attr('SC_Item_MarginPercent').AssignValue('0')
			else:
				prodrow.Product.Attr('SC_ItemEditFlag').AssignValue('111')
				prodrow.Product.Attr('SC_Item_MarginPercent').AssignValue('45')
			cont_asse.Calculate()
			SCprod_container.Calculate()
		elif sProdkey == 'One Time Upgrade':
			spDict = scDict[sProdkey]
			sProd = SCprod_container.AddNewRow(True)
			sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
			sProd['Description'] = 'Description'
			sProd['Quantity'] = '1'
			sProd.IsSelected = True
			sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
			sProd.Product.Attr('SC_PartNumber').AssignValue('One Time Upgrade')
			#sProd.Product.Attr('SC_Price').AssignValue(str(lbDict['Price']))
			sProd.Product.Attr('SC_Description').AssignValue('Software Upgrades')
			sProd.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
			for sys in spDict.Keys:
				if sys != 'Total' and spDict[sys][0] != '' and float(spDict[sys][0]) > 0:
					sysProd = sProd.Product.GetContainerByName('SC_Asset')
					s = sysProd.AddNewRow(True)
					s['Asset'] = '<*VALUE(SC_AssetName)*>'
					s['Description'] = 'Description'
					s['Quantity'] = '1'
					s['Price'] = '<*VALUE(SC_Price)*>'
					s.IsSelected = True
					s.Product.Attr('SC_ItemEditFlag').AssignValue('110')
					s.Product.Attr('SC_AssetName').AssignValue(sys)
					s.Product.Attr('SC_Price').AssignValue(str(spDict[sys][0]))
					s.Product.Attr('SC_Description').AssignValue(str(spDict[sys][1]))
					s.Product.Attr('SC_Item_MarginPercent').AssignValue('45')
					sysProd.Calculate()
			SCprod_container.Calculate()
		elif sProdkey == 'Hardware Warranty Renewal':
			hh_Dict = scDict[sProdkey]
			sProd = SCprod_container.AddNewRow(True)
			addHWRWL(hh_Dict, sProd, sProdkey, sc_ProdDist)
			SCprod_container.Calculate()
		elif sProdkey == 'Hardware Refresh Renewal': # or sProdkey == 'Hardware Warranty Renewal':
			hh_Dict = scDict[sProdkey]
			sProd = SCprod_container.AddNewRow(True)
			sProd['Asset'] = '<*VALUE(SC_PartNumber)*>'
			sProd['Description'] = 'Description'
			sProd['Quantity'] = '1'
			sProd.IsSelected = True
			sProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
			sProd.Product.Attr('SC_PartNumber').AssignValue(sProdkey.split(' ')[0] + " "+ sProdkey.split(' ')[1])
			prd = sProdkey.split(' ')[0:2]
			sProd.Product.Attr('SC_Description').AssignValue(' '.join(prd))
			sProd.ApplyProductChanges()
			p_container = sProd.Product.GetContainerByName("SC_Asset")
			pProd = p_container.AddNewRow(True)
			pProd['Asset'] = '<*VALUE(SC_AssetName)*>'
			pProd['Description'] = 'Description'
			pProd['Quantity'] = '1'
			pProd.IsSelected = True
			pProd.ApplyProductChanges()
			pProd.Product.Attr('SC_AssetName').AssignValue('Service Product')
			pProd.Product.Attr('SC_Description').AssignValue(' '.join(prd))
			pProd.Product.Attr('SC_Price').AssignValue(str(scDict[sProdkey][0]))
			pProd.Product.Attr('SC_PriceImpact_RWL').AssignValue(str(scDict[sProdkey][1]))
			pProd.Product.Attr('SC_ScopeChange_RWl').AssignValue(str(scDict[sProdkey][2]))
			pProd.Product.Attr('SC_HWListPrice_RWL').AssignValue(str(scDict[sProdkey][3]))
			pProd.Product.Attr('SC_PY_SellPrice').AssignValue(str(scDict[sProdkey][11]))
			pProd.Product.Attr('SC_PY_Price').AssignValue(str(scDict[sProdkey][5]))
			pProd.Product.Attr('SC_Item_Cost').AssignValue(str(scDict[sProdkey][6]))
			pProd.Product.Attr('SC_Item_CostStatus').AssignValue('1')
			pProd.Product.Attr('SC_Item_MarginPercent').AssignValue(str((1-scDict[sProdkey][6]/scDict[sProdkey][0])*100 if scDict[sProdkey][0] else '0'))
			pProd.Product.Attr('SC_Escalation_Price').AssignValue(str(scDict[sProdkey][9]))
			pProd.Product.Attr('SC_SA_Price').AssignValue(str(scDict[sProdkey][7]))
			pProd.Product.Attr('SC_SR_Price').AssignValue(str(scDict[sProdkey][8]))
			pProd.Product.Attr('ItemQuantity').AssignValue(str(scDict[sProdkey][10]))
			if str(scDict[sProdkey][10]) == '0':
				pProd.Product.Attr('SC_ItemEditFlag').AssignValue('000')
			else:
				pProd.Product.Attr('SC_ItemEditFlag').AssignValue('110')
			pProd.Product.Attr('PRD_PartNumber').AssignValue(sc_ProdDist['UniqueID'])
			#pProd.Product.Attr('SC_Item_MarginPercent').AssignValue('45')
	yProd.ApplyProductChanges()
	SC_container.Calculate()
	yearList.pop(0)
	i = 0
	SC_Delete = []
	copyIndex = 0
	removeOneTime = True
	for yVal in yearList:
		i+=1
		SC_container.CopyRow(copyIndex)
		SC_container.Rows[i].Product.Attr('SC_Description').AssignValue(yVal)
		SC_container.Rows[i].Product.Attr('SC_Year').AssignValue('Year-' + str(i+1))
		pc_container=SC_container.Rows[i].Product.GetContainerByName("SC_Asset")
		#if copyIndex == 0 and removeOneTime:
		#	copyIndex, pc_container = removeOneTimeProducts(pc_container)
		#	removeOneTime = False
		for pkey in prodYearDict:
			if i >= int(prodYearDict[pkey]):
				pkeyIndex = next((index for (index, d) in enumerate(productlist) if d["ProductName"] == pkey), None)
				enabledpkeyIndex = next((index for (index, d) in enumerate(productlist) if d["ProductName"] in ('Enabled Services SESP','Enabled Services')), None)
				if pkeyIndex != None:
					pc_container.DeleteRow(pkeyIndex)
					pc_container.Calculate()
				if pc_container.Rows.Count == 0:
					SC_Delete.append(i)
				if enabledpkeyIndex != None:
					ppc_container=pc_container.Rows[enabledpkeyIndex].Product.GetContainerByName("SC_Asset")
					index =  [row.RowIndex for row in ppc_container.Rows if row.Product.Attr('SC_AssetName').GetValue() == 'Matrikon License']
					ppc_container.DeleteRow(index[0]) if index else Trace.Write('No matrikon')
		SC_container.Rows[i].ApplyProductChanges()
	if SC_Delete:
		SC_Delete.sort(reverse=True)
		for i in SC_Delete:
			SC_container.DeleteRow(i)
	Quote.SetGlobal('EditFlag','1')
	SC_container.Calculate()
Quote.SetGlobal('SC_ProductsType', str(SC_ProductsType))