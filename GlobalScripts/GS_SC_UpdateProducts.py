import GS_SC_UpdateProducts2 as GSCUpdProd2
from System.Collections.Specialized import OrderedDictionary
def sc_yearlist(StartDate, EndDate, ReqDates = None):
	yList = []
	dtDict = {}
	i=EndDate.Year - StartDate.Year + 1
	yIndex = 1
	while i > 0 :
		stYear = StartDate.Year
		stDate = StartDate
		StartDate = StartDate.AddYears(1).AddDays(-1)
		if StartDate>=EndDate:
			if (EndDate - StartDate.AddYears(-1).AddDays(1)).Days >= 0:
					dtDict['Year-' + str(yIndex)] = {'StartDate': stDate.ToString('yyyy-MM-dd'), 'EndDate': EndDate.ToString('yyyy-MM-dd')}
					yList.append(str(stYear) + '-' + str(EndDate.Year))
			break
		else:
				dtDict['Year-' + str(yIndex)] = {'StartDate': stDate.ToString('yyyy-MM-dd'), 'EndDate': StartDate.ToString('yyyy-MM-dd')}
				yList.append(str(stYear) + '-' + str(StartDate.Year))
		StartDate = StartDate.AddDays(1)
		i-=1
		yIndex+=1
	if ReqDates:
		return yList, dtDict
	return yList

def sumDict(sDict):
	result = {}
	for iDict in sDict:
		for k in iDict.keys():
			result[k] = result.get(k, 0) + float(iDict[k])
	return result

def sumOrderedDict(sDict):
	result = OrderedDictionary()
	for iDict in sDict:
		for k in iDict.keys():
			result[k] = result[k] if k in result.Keys else 0  + float(iDict[k])
	return result

def GenerateProdDictFromContainer(pCont):
	productlist = []
	scDict = {}
	scFyDict = {}
	prodYearDict = {}
	srDict = {}
	for row in pCont.Rows:
		if row['Product_Status'] != 'Complete':
			continue
		spRemovalList = []
		spRemovalDist = {}
		if row['Type'] == 'Renewal':
			ComSummaryList = []
			if row.Product.GetContainerByName('ComparisonSummary'):
				ComSummaryList.append('ComparisonSummary')
			if row.Product.GetContainerByName('ESComparisonSummary'):
				ComSummaryList.append('ESComparisonSummary')
			for ComSummaryListName in ComSummaryList:
				for CompSummary in row.Product.GetContainerByName(ComSummaryListName).Rows:
					if CompSummary.IsSelected:
						spRemovalDist[CompSummary['Service_Product']]={'PY_ListPrice': float(CompSummary['PY_List_Price_SFDC']) if CompSummary['PY_List_Price_SFDC'] else 0, 'PY_SellPrice': float(CompSummary['PY_Sell_Price_SFDC']) if CompSummary['PY_Sell_Price_SFDC'] else 0}
						spRemovalList.append(CompSummary['Service_Product'])
					elif CompSummary['CY_Service_Product'] and CompSummary['CY_Service_Product'] != CompSummary['Service_Product']:
						spRemovalDist[CompSummary['Service_Product']]={'PY_ListPrice': 0, 'PY_SellPrice': 0}
						spRemovalList.append(CompSummary['Service_Product'])
				if spRemovalDist:
					srDict[row['Module']] = spRemovalDist
		if row['Module'] == 'Solution Enhancement Support Program':
			sespContainer = row.Product.GetContainerByName('SC_SESP Models Hidden')
			sespDict = {}
			LP_ColumnName = 'Price'
			if row.Product.Attr('SC_Service_Product').GetValue() not in spRemovalList:
				for sRow in sespContainer.Rows:
					List_Price = float(sRow[LP_ColumnName]  if sRow[LP_ColumnName] else 0)
					if sRow['Platform']:
						if sRow['Platform'] in sespDict:
							if sRow['MSID'] in sespDict[sRow['Platform']]:
								sespDict[sRow['Platform']][sRow['MSID']]['Price'] = float(sespDict[sRow['Platform']][sRow['MSID']]['Price']) + List_Price
								sespDict[sRow['Platform']][sRow['MSID']]['Honeywell_List_Price'] = float(sespDict[sRow['Platform']][sRow['MSID']]['Honeywell_List_Price']) + float(sRow['Honeywell List Price']  if sRow['Honeywell List Price'] else 0)
								sespDict[sRow['Platform']][sRow['MSID']]['Escalation_Price'] = float(sespDict[sRow['Platform']][sRow['MSID']]['Escalation_Price']) + float(sRow['Escalation_Price']  if sRow['Escalation_Price'] else 0)
								sespDict[sRow['Platform']][sRow['MSID']]['SR_Price'] = float(sespDict[sRow['Platform']][sRow['MSID']]['SR_Price']) + float(sRow['SR_Price']  if sRow['SR_Price'] else 0)
								sespDict[sRow['Platform']][sRow['MSID']]['SA_Price'] = float(sespDict[sRow['Platform']][sRow['MSID']]['SA_Price']) + float(sRow['SA_Price']  if sRow['SA_Price'] else 0)
								sespDict[sRow['Platform']][sRow['MSID']]['PY_ListPrice'] = float(sespDict[sRow['Platform']][sRow['MSID']]['PY_ListPrice']) + float(sRow['PY_ListPrice']  if sRow['PY_ListPrice'] else 0)
								sespDict[sRow['Platform']][sRow['MSID']]['PY_SellPrice'] = float(sespDict[sRow['Platform']][sRow['MSID']]['PY_SellPrice']) + float(sRow['PY_SellPrice']  if sRow['PY_SellPrice'] else 0)
							else:
								sespDict[sRow['Platform']][sRow['MSID']] = {'Price': List_Price, 'Honeywell_List_Price': float(sRow['Honeywell List Price']  if sRow['Honeywell List Price'] else 0), 'Escalation_Price': float(sRow['Escalation_Price']) if sRow['Escalation_Price'] else 0, 'SR_Price': float(sRow['SR_Price']) if sRow['SR_Price'] else 0, 'SA_Price': float(sRow['SA_Price']) if sRow['SA_Price'] else 0, 'PY_ListPrice': float(sRow['PY_ListPrice']) if sRow['PY_ListPrice'] else 0, 'PY_SellPrice': float(sRow['PY_SellPrice']) if sRow['PY_SellPrice'] else 0, 'Quantity': 1}
						else:
							sespDict[sRow['Platform']] = {sRow['MSID']: {'Price': List_Price, 'Honeywell_List_Price': float(sRow['Honeywell List Price']  if sRow['Honeywell List Price'] else 0), 'Escalation_Price': float(sRow['Escalation_Price']) if sRow['Escalation_Price'] else 0, 'SR_Price': float(sRow['SR_Price']) if sRow['SR_Price'] else 0, 'SA_Price': float(sRow['SA_Price']) if sRow['SA_Price'] else 0, 'PY_ListPrice': float(sRow['PY_ListPrice']) if sRow['PY_ListPrice'] else 0, 'PY_SellPrice': float(sRow['PY_SellPrice']) if sRow['PY_SellPrice'] else 0, 'Quantity': 1}}
				sesplabContainer = row.Product.GetContainerByName('SC_Entitlements_Model')
				SC_Training_Match_Contract_Value_SS_Py = float(row.Product.Attr('SC_Training_Match_Contract_Value_SS_Py').GetValue())
				TM_found = 0
				for sRow in sesplabContainer.Rows:
					if sRow['Entitlement'].lower() == 'Training Match'.lower():
						TM_found = 1
						tm_LPrice = float(row.Product.Attr('SC_Training_Match_Contract_Value_SS').GetValue().strip() if row.Product.Attr('SC_Training_Match_Contract_Value_SS').GetValue().strip() else 0)
						tm_pyLPrice = float(row.Product.Attr('SC_Training_Match_Contract_Value_SS_Py').GetValue().strip() if row.Product.Attr('SC_Training_Match_Contract_Value_SS_Py').GetValue().strip() else 0)
						if tm_pyLPrice > tm_LPrice and tm_LPrice == 0 :
							tm_SA_Price = 0
							tm_SR_Price = tm_LPrice - tm_pyLPrice
						elif tm_pyLPrice < tm_LPrice and tm_pyLPrice == 0:
							tm_SA_Price = tm_LPrice - tm_pyLPrice
							tm_SR_Price = 0
						elif tm_pyLPrice > 0 and tm_LPrice > 0:
							tm_SR_Price = 0
							tm_SA_Price = 0
						sespDict[sRow['Entitlement']] = {'Price': tm_LPrice, 'Honeywell_List_Price': tm_LPrice, 'Escalation_Price': 0, 'SR_Price': tm_SR_Price, 'SA_Price': tm_SA_Price, 'PY_ListPrice': tm_pyLPrice, 'PY_SellPrice': tm_pyLPrice, 'Quantity': 1}
				if TM_found == 0 and SC_Training_Match_Contract_Value_SS_Py > 0:
					tm_LPrice = float(row.Product.Attr('SC_Training_Match_Contract_Value_SS').GetValue().strip() if row.Product.Attr('SC_Training_Match_Contract_Value_SS').GetValue().strip() else 0)
					tm_pyLPrice = float(row.Product.Attr('SC_Training_Match_Contract_Value_SS_Py').GetValue().strip() if row.Product.Attr('SC_Training_Match_Contract_Value_SS_Py').GetValue().strip() else 0)
					if tm_pyLPrice > tm_LPrice:
						tm_SA_Price = 0
						tm_SR_Price = tm_LPrice - tm_pyLPrice
					else:
						tm_SA_Price = tm_LPrice - tm_pyLPrice
						tm_SR_Price = 0
					sespDict["Training Match"] = {'Price': tm_LPrice, 'Honeywell_List_Price': tm_LPrice, 'Escalation_Price': 0, 'SR_Price': tm_SR_Price, 'SA_Price': tm_SA_Price, 'PY_ListPrice': tm_pyLPrice, 'PY_SellPrice': tm_pyLPrice, 'Quantity': 0}

				otherCostContainer = row.Product.GetContainerByName('SC Other Cost Details')
				for oRow in otherCostContainer.Rows:
					sespDict.setdefault('Other cost details', []).append({oRow['Site Annual Audit'] : oRow['Cost']})
			else:
				for spproductName in spRemovalDist:
					sespDict['Scope Removed'] = {'Scope Removed': {'Price': 0, 'Honeywell_List_Price': 0,  'Escalation_Price': 0, 'SR_Price': 0, 'SA_Price': 0, 'PY_ListPrice': float(spRemovalDist[spproductName]['PY_ListPrice']), 'PY_SellPrice': float(spRemovalDist[spproductName]['PY_SellPrice']), 'Quantity': 0}}
			if sespDict:
				scDict[row.Product.Attr('SC_Service_Product').GetValue()] = sespDict
				productlist.append({'ProductName' : row.Product.Attr('SC_Service_Product').GetValue(), 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})

			if row.Product.AttrValue('EnableSelection_SESP','&nbsp').IsSelected:
				if row.Product.Attr('EnabledService_Entitlement').GetValue() == 'Enabled Services - Enhanced' or row.Product.Attr('EnabledService_Entitlement').GetValue() == 'Enabled Services - Essential':
					scDict['Enabled Services SESP'] = GSCUpdProd2.GenProdDictFromConRow(row,spRemovalList,spRemovalDist)
					productlist.append({'ProductName' : 'Enabled Services SESP', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
					if 'Matrikon License' in str(scDict['Enabled Services SESP']):
						prodYearDict['Matrikon License'] = 1
						
			if row.Product.AttrValue('One time upgrade','&nbsp').IsSelected:
				attrs = OrderedDictionary()
				attrs['DVM'] = ['ListPrice_DVM_OTU_SESP','Digital Video Manager']
				attrs['EOP'] = ['ListPrice_EOP_OTU_SESP','Experion Off Process (EOP)']
				attrs['eServer'] = ['ListPrice_ESS_OTU_SESP', 'e-Server System']
				attrs['OTS'] 		= ['ListPrice_OTS_OTU_SESP','OTS']
				attrs['Simulation'] = ['ListPrice_SS_OTU_SESP','Simulation System']
				attrs['HS']       = ['ListPrice_HS_OTU_SESP','HS']
				attrs['FDM']      = ['ListPrice_FDM_OTU_SESP','Field Device Manager']
				attrs['Experion'] = ['ListPrice_EXP_OTU_SESP','Experion PKS']
				attrs['TPN']  = ['ListPrice_ExTPS_OTU_SESP','Total Plant Network']
				attrs['TPS']  = ['ListPrice_ExTPS_OTU_SESP','Experion-TPS']
				attrs['ESVT'] = ['ListPrice_ESVT_OTU_SESP','Experion PKS for TPS (EVST)']
				attrs = {'DVM':['ListPrice_DVM_OTU_SESP','Digital Video Manager'],'EOP':['ListPrice_EOP_OTU_SESP','Experion Off Process (EOP)'],'eServer':['ListPrice_ESS_OTU_SESP', 'e-Server System'],'Simulation':['ListPrice_SS_OTU_SESP','Simulation System'],'OTS':['ListPrice_OTS_OTU_SESP','OTS'],'HS':['ListPrice_HS_OTU_SESP','HS'],'FDM':['ListPrice_FDM_OTU_SESP','Field Device Manager'],'Experion':['ListPrice_EXP_OTU_SESP','Experion PKS'],'TPN':['ListPrice_TPN_OTU_SESP','Total Plant Network'],'TPS':['ListPrice_ExTPS_OTU_SESP','Experion-TPS'],'ESVT':['ListPrice_ESVT_OTU_SESP','Experion PKS for TPS (EVST)'],'Third Party':['ListPrice_ThirdParty_OTU_SESP','Third Party Component'],'EBR':['ListPrice_EBR_OTU_SESP','Enterprise Backup and Recovery']}
				otu_dict = OrderedDictionary()
				for i in attrs:
					val = row.Product.Attr(attrs[i][0]).GetValue()
					if 1 == 1:
						otu_dict[i] = []
						otu_dict[i].append(val)
						otu_dict[i].append(attrs[i][1])
				scDict['One Time Upgrade'] = otu_dict
				productlist.append({'ProductName' : 'One Time Upgrade', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
				prodYearDict['One Time Upgrade'] = 1
		elif row['Module'] == 'Parts Management':
			ContainerDetail = row.Product.GetContainerByName('SC_P1P2_Parts_List_Summary')
			ContainerDetail2 = row.Product.GetContainerByName('SC_P1P2_ServiceProduct_Entitlement')
			P1Dict = {}
			for srow in ContainerDetail.Rows:
				for srows in ContainerDetail2.Rows:
					if srow['Service_Product'] == srows['Service Product'] and  srow['Service_Product'] not in spRemovalList:
						P1Dict[srow['Service_Product']]={'Entitlement' : srows['Entitlement'], 'List_Price' : srow['Ext_Holding_Price'] if srow['Ext_Holding_Price'] else '0', 'CostStatus': 'Fixed', 'Cost': srow['CY_TotalCost'] if srow['CY_TotalCost'] else '0', 'Escalation_Price' : srow['Escalation_Price'] if srow['Escalation_Price'] else '0', 'SA_Price' : srow['SA_Price'] if srow['SA_Price'] else '0', 'SR_Price' : srow['SR_Price'] if srow['SR_Price'] else '0',  'PY_ListPrice' : srow['PY_ExtHoldingPrice'] if srow['PY_ExtHoldingPrice'] else '0', 'PY_SellPrice' : srow['PY_SellPrice'] if srow['PY_SellPrice'] else '0','Quantity': 1, 'SC_Scope_Manual' : ''}
			ContainerDetail3 = row.Product.GetContainerByName('SC_P1P2_Parts_Replacement_Summary')
			for srow in ContainerDetail3.Rows:
				if srow['Service_Product'] not in spRemovalList:
					P1Dict[srow['Service_Product']] = {'Entitlement': srow['Service_Product'], 'List_Price' : srow['List_Price'] if srow['List_Price'] else '0', 'CostStatus':'Dynamic', 'Escalation_Price' : '0', 'SA_Price' : '0', 'SR_Price' : '0',  'PY_ListPrice' : srow['PY_ListPrice'] if srow['PY_ListPrice'] else '0', 'PY_SellPrice' : srow['PY_SellPrice'] if srow['PY_SellPrice'] else '0','Quantity': 1, 'SC_Scope_Manual':srow['Scope_Change'] if srow['Scope_Change'] else '0'}
			for p1productName in spRemovalDist:
				P1Dict[p1productName] =  {'Entitlement': p1productName,'Quantity': 0, 'List_Price' : 0, 'CostStatus': 'Fixed','Cost': 0, 'Escalation_Price': 0, 'PY_ListPrice': float(spRemovalDist[p1productName]['PY_ListPrice']), 'PY_SellPrice': float(spRemovalDist[p1productName]['PY_SellPrice']), 'SA_Price': 0, 'SR_Price': 0,'SC_Scope_Manual' : ''}
			if P1Dict:
				scDict['Parts Management'] = P1Dict
				productlist.append({'ProductName' : 'Parts Management', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
		elif row['Module'] == 'Labor':
			
			laborDict = GSCUpdProd2.GenProdDictFromConRow(row,spRemovalList,spRemovalDist)
			if laborDict:
				scDict['Labor'] = laborDict
				productlist.append({'ProductName' : 'Labor', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
		elif row['Module'] == 'Local Support Standby':
			lssDict = GSCUpdProd2.GenProdDictFromConRow(row,spRemovalList,spRemovalDist)
			if lssDict:
				scDict['Local Support Standby'] = lssDict
				productlist.append({'ProductName' : 'Local Support Standby', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
		elif row['Module'] == 'BGP inc Matrikon':
			ContainerName = 'SC_BGP_Models_Cont_Hidden'
			LP_ColumnName = 'List_Price'
			CP_ColumnName = 'Cost_Price'
			BGPDict = {}
			BGPContainer = row.Product.GetContainerByName('SC_BGP_Models_Cont_Hidden')
			for brow in BGPContainer.Rows:
				if brow['Service_Product'] in BGPDict:
					BGPDict[brow['Service_Product']]['Price'] = float(BGPDict[brow['Service_Product']]['Price']) + float(brow[LP_ColumnName]  if brow[LP_ColumnName] else 0)
					BGPDict[brow['Service_Product']]['Cost'] = float(BGPDict[brow['Service_Product']]['Cost']) + float(brow[CP_ColumnName] if brow[CP_ColumnName] else 0)
					BGPDict[brow['Service_Product']]['Escalation_Price'] = float(BGPDict[brow['Service_Product']]['Escalation_Price']) + float(brow['Escalation_Price'] if brow['Escalation_Price'] else 0) 
					BGPDict[brow['Service_Product']]['SR_Price'] = float(BGPDict[brow['Service_Product']]['SR_Price']) + float(brow['SR_Price'] if brow['SR_Price'] else 0)
					BGPDict[brow['Service_Product']]['SA_Price'] = float(BGPDict[brow['Service_Product']]['SA_Price']) + float(brow['SA_Price'] if brow['SA_Price'] else 0)
					BGPDict[brow['Service_Product']]['PY_ListPrice'] = float(BGPDict[brow['Service_Product']]['PY_ListPrice']) + float(brow['PY_ListPrice'] if brow['PY_ListPrice'] else 0)
					BGPDict[brow['Service_Product']]['PY_SellPrice'] = float(BGPDict[brow['Service_Product']]['PY_SellPrice']) + float(brow['PY_SellPrice'] if brow['PY_SellPrice'] else 0)
				else:
					if brow['Service_Product'] not in spRemovalList:
						BGPDict[brow['Service_Product']] = {'Price': float(brow[LP_ColumnName]) if brow[LP_ColumnName] else 0, 'Cost': float(brow[CP_ColumnName]) if brow[CP_ColumnName] else 0, 'Escalation_Price': float(brow['Escalation_Price']) if brow['Escalation_Price'] else 0, 'SR_Price': float(brow['SR_Price']) if brow['SR_Price'] else 0, 'SA_Price': float(brow['SA_Price']) if brow['SA_Price'] else 0, 'PY_ListPrice': float(brow['PY_ListPrice']) if brow['PY_ListPrice'] else 0, 'PY_SellPrice': float(brow['PY_SellPrice']) if brow['PY_SellPrice'] else 0, 'Quantity': 1}
			for bgproductName in spRemovalDist:
				BGPDict[bgproductName] =  {'Quantity': 0, 'Price' : 0, 'Cost': 0, 'Escalation_Price': 0, 'PY_ListPrice': float(spRemovalDist[bgproductName]['PY_ListPrice']), 'PY_SellPrice': float(spRemovalDist[bgproductName]['PY_SellPrice']), 'SA_Price': 0, 'SR_Price': 0}
			if BGPDict:
				scDict['BGP inc Matrikon'] = BGPDict
				productlist.append({'ProductName' : 'BGP inc Matrikon', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
		elif row['Module'] == 'Generic Module':
			GSCUpdProd2.GenProdDictFromConRow(row,spRemovalList,spRemovalDist,scDict, productlist)
		elif row['Module'] == 'Cyber':
			ContainerName = 'SC_Cyber_Models_Cont_Hidden' if row['Type'] == 'Renewal' else 'SC_Cyber_Models_Cont_Hidden'
			LP_ColumnName = 'List_Price'
			CP_ColumnName = 'CY_CostPrice' if row['Type'] == 'Renewal' else 'Cost_Price'
			CyDict = {}
			CyContainer = row.Product.GetContainerByName(ContainerName)
			for crow in CyContainer.Rows:
				if crow['Service_Product'] in CyDict:
					CyDict[crow['Service_Product']]['Price'] = float(CyDict[crow['Service_Product']]['Price']) + float(crow[LP_ColumnName] if crow[LP_ColumnName] else 0)
					CyDict[crow['Service_Product']]['Cost'] = float(CyDict[crow['Service_Product']]['Cost']) + float(crow[CP_ColumnName] if crow[CP_ColumnName] else 0)
					CyDict[crow['Service_Product']]['Escalation_Price'] = float(CyDict[crow['Service_Product']]['Escalation_Price']) + float(crow['Escalation_Price'] if crow['Escalation_Price'] else 0)
					CyDict[crow['Service_Product']]['SR_Price'] = float(CyDict[crow['Service_Product']]['SR_Price']) + float(crow['SR_Price'] if crow['SR_Price'] else 0)
					CyDict[crow['Service_Product']]['SA_Price'] = float(CyDict[crow['Service_Product']]['SA_Price']) + float(crow['SA_Price'] if crow['SA_Price'] else 0)
					CyDict[crow['Service_Product']]['PY_ListPrice'] = float(CyDict[crow['Service_Product']]['PY_ListPrice']) + float(crow['PY_ListPrice'] if crow['PY_ListPrice'] else 0)
					CyDict[crow['Service_Product']]['PY_SellPrice'] = float(CyDict[crow['Service_Product']]['PY_SellPrice']) + float(crow['PY_SellPrice'] if crow['PY_SellPrice'] else 0)
				else:
					if crow['Service_Product'] not in spRemovalList:
						CyDict[crow['Service_Product']] = {'Price': float(crow[LP_ColumnName]) if crow[LP_ColumnName] else 0, 'Cost': float(crow[CP_ColumnName]) if crow[CP_ColumnName] else 0, 'Escalation_Price': float(crow['Escalation_Price']) if crow['Escalation_Price'] else 0, 'SR_Price': float(crow['SR_Price']) if crow['SR_Price'] else 0, 'SA_Price': float(crow['SA_Price']) if crow['SA_Price'] else 0, 'PY_ListPrice': float(crow['PY_ListPrice']) if crow['PY_ListPrice'] else 0, 'PY_SellPrice': float(crow['PY_SellPrice']) if crow['PY_SellPrice'] else 0, 'Quantity': 1}
			for cyproductName in spRemovalDist:
				CyDict[cyproductName] =  {'Quantity': 0, 'Price' : 0, 'Cost': 0, 'Escalation_Price': 0, 'PY_ListPrice': float(spRemovalDist[cyproductName]['PY_ListPrice']), 'PY_SellPrice': float(spRemovalDist[cyproductName]['PY_SellPrice']), 'SA_Price': 0, 'SR_Price': 0}
			if CyDict:
				scDict['Cyber'] = CyDict
				productlist.append({'ProductName' : 'Cyber', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
		elif row['Module'] == 'QCS 4.0':
			QCSContainer = row.Product.GetContainerByName('SC_QCS_Pricing_Details_Cont_Hidden')
			QCSContainer2 = row.Product.GetContainerByName('SC_QCS_Product_Container')
			LP_ColumnName = 'List Price'
			QCSDict = OrderedDictionary()
			for qrow in QCSContainer.Rows:
				if len(qrow['Service Product']) < 1 :
					defNull = 'QCS 4.0'
				else :
					defNull = qrow['Service Product']
				for qrows in QCSContainer2.Rows:
					if defNull == qrows['Service Product']:
						if defNull in QCSDict:
							QCSDict[defNull].append({"Entitlement" : qrows['Entitlement'] + ': ' + qrow['Description'], "Price": qrow[LP_ColumnName], 'Escalation_Price': float(qrow['Escalation_Price']) if qrow['Escalation_Price'] else 0, 'SR_Price': float(qrow['SR_Price']) if qrow['SR_Price'] else 0, 'SA_Price': float(qrow['SA_Price']) if qrow['SA_Price'] else 0, 'PY_ListPrice': float(qrow['PY_ListPrice']) if qrow['PY_ListPrice'] else 0, 'PY_SellPrice': float(qrow['PY_SellPrice']) if qrow['PY_SellPrice'] else 0, 'Quantity': 1 })
						else:
							if defNull not in spRemovalList:
								QCSDict[defNull] = [{"Entitlement" : qrows['Entitlement'] + ': ' + qrow['Description'], "Price": qrow[LP_ColumnName], 'Escalation_Price': float(qrow['Escalation_Price']) if qrow['Escalation_Price'] else 0, 'SR_Price': float(qrow['SR_Price']) if qrow['SR_Price'] else 0, 'SA_Price': float(qrow['SA_Price']) if qrow['SA_Price'] else 0, 'PY_ListPrice': float(qrow['PY_ListPrice']) if qrow['PY_ListPrice'] else 0, 'PY_SellPrice': float(qrow['PY_SellPrice']) if qrow['PY_SellPrice'] else 0, 'Quantity': 1 }]
				for rpproductName in spRemovalDist:
					QCSDict[rpproductName] = [{"Entitlement" : rpproductName, 'Quantity': 0, 'Price' : 0, 'Cost': 0, 'Escalation_Price': 0, 'PY_ListPrice': float(spRemovalDist[rpproductName]['PY_ListPrice']), 'PY_SellPrice': float(spRemovalDist[rpproductName]['PY_SellPrice']), 'SA_Price': 0, 'SR_Price': 0}]
			if QCSDict:
				scDict['QCS 4.0'] = QCSDict
				productlist.append({'ProductName' : 'QCS 4.0', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
		elif row['Module'] == 'Third Party Services':
			ContainerName = 'SC_TPS_RC_Entitlements_Scope_summary_hidden'
			LP_ColumnName = 'List_Price'
			CP_ColumnName = 'COST'
			Escalation_Price = 'Escalation_Price'
			PY_ListPrice ='PY_ListPrice'
			PY_SellPrice ='PY_SellPrice'
			SR_Price ='SR_Price'
			SA_Price ='SA_Price'
			TPSContainer = row.Product.GetContainerByName(ContainerName)
			TPSDict = {}
			if 'Third Party Services' not in spRemovalList:
				for trow in TPSContainer.Rows:
					if trow['Entitlement'] in TPSDict:
						TPSDict[trow['Entitlement']]['Price'] = float(TPSDict[trow['Entitlement']]['Price']) + (float(trow[LP_ColumnName]) if trow[LP_ColumnName] != "" else 0)
						TPSDict[trow['Entitlement']]['Cost'] = float(TPSDict[trow['Entitlement']]['Cost']) + (float(trow[CP_ColumnName]) if trow[CP_ColumnName] != "" else 0)
						TPSDict[trow['Entitlement']]['Escalation_Price'] = float(TPSDict[trow['Entitlement']]['Escalation_Price']) + float(trow[Escalation_Price] if trow['Escalation_Price'] else 0)
						TPSDict[trow['Entitlement']]['PY_ListPrice'] = float(TPSDict[trow['Entitlement']]['PY_ListPrice']) + float(trow[PY_ListPrice] if trow['PY_ListPrice'] else 0)
						TPSDict[trow['Entitlement']]['PY_SellPrice'] = float(TPSDict[trow['Entitlement']]['PY_SellPrice']) + float(trow[PY_SellPrice] if trow['PY_SellPrice'] else 0)
						TPSDict[trow['Entitlement']]['SR_Price'] = float(TPSDict[trow['Entitlement']]['SR_Price']) + float(trow[SR_Price] if trow['SR_Price'] else 0)
						TPSDict[trow['Entitlement']]['SA_Price'] = float(TPSDict[trow['Entitlement']]['SA_Price']) + float(trow[SA_Price] if trow['SA_Price'] else 0)
					else:
						TPSDict[trow['Entitlement']] =  {'Price' : float(trow[LP_ColumnName]) if trow[LP_ColumnName] else '0', 'Cost':float(trow[CP_ColumnName]) if trow[CP_ColumnName] else '0','Escalation_Price':float(trow[Escalation_Price]) if trow[Escalation_Price] else '0','PY_ListPrice':float(trow[PY_ListPrice]) if trow[PY_ListPrice] else '0','PY_SellPrice':float(trow[PY_SellPrice]) if trow[PY_SellPrice] else '0','SR_Price': float(trow[SR_Price]) if trow[SR_Price] else '0','SA_Price': float(trow[SA_Price]) if trow[SA_Price] else '0', 'Quantity': 1}
			for TPproductName in spRemovalDist:
				TPSDict['Third Party Services'] =  {'Quantity': 0, 'Price' : 0, 'Cost': 0, 'Escalation_Price': 0, 'PY_ListPrice': float(spRemovalDist[TPproductName]['PY_ListPrice']), 'PY_SellPrice': float(spRemovalDist[TPproductName]['PY_SellPrice']), 'SA_Price': 0, 'SR_Price': 0}
			if TPSDict:
				scDict['Third Party Services'] = TPSDict
				productlist.append({'ProductName' : 'Third Party Services', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
		elif row['Module'] == 'MES Performix':
			ContainerName = 'SC_MES_Models_Hidden'
			LP_ColumnName = 'List Price' 
			MPContainer = row.Product.GetContainerByName(ContainerName)
			MESproductName = row.Product.Attr('SC_MES_Service_Product').GetValue()
			MESDict = {}
			for mrow in MPContainer.Rows:
				if MESproductName in MESDict:
					MESDict[MESproductName]['Price'] = float(MESDict[MESproductName]['Price']) + (float(mrow[LP_ColumnName]) if mrow[LP_ColumnName] != "" else 0)
					MESDict[MESproductName]['PY_ListPrice'] = float(MESDict[MESproductName]['PY_ListPrice']) + (float(mrow['PY_ListPrice']) if mrow['PY_ListPrice'] != "" else 0)
					MESDict[MESproductName]['PY_SellPrice'] = float(MESDict[MESproductName]['PY_SellPrice']) + (float(mrow['PY_SellPrice']) if mrow['PY_SellPrice'] != "" else 0)
					MESDict[MESproductName]['Escalation_Price'] = float(MESDict[MESproductName]['Escalation_Price']) + (float(mrow['Escalation_Price']) if mrow['Escalation_Price'] != "" else 0)
					MESDict[MESproductName]['SA_Price'] = float(MESDict[MESproductName]['SA_Price']) + (float(mrow['SA_Price']) if mrow['SA_Price'] != "" else 0)
					MESDict[MESproductName]['SR_Price'] = float(MESDict[MESproductName]['SR_Price']) + (float(mrow['SR_Price']) if mrow['SR_Price'] != "" else 0)
				else:
					if MESproductName not in spRemovalList:
						MESDict[MESproductName] =  {'Quantity': 1, 'Price' : float(mrow[LP_ColumnName]), 'Escalation_Price': float(mrow['Escalation_Price'] if mrow['Escalation_Price'] != "" else 0), 'PY_ListPrice': float(mrow['PY_ListPrice']) if mrow['PY_ListPrice'] != "" else 0, 'PY_SellPrice': float(mrow['PY_SellPrice']) if mrow['PY_SellPrice'] != "" else 0, 'SA_Price': float(mrow['SA_Price']) if mrow['SA_Price'] != "" else 0, 'SR_Price': float(mrow['SR_Price']) if mrow['SR_Price'] != "" else 0}
			for MExproductName in spRemovalDist:
				MESDict[MExproductName] =  {'Quantity': 0, 'Price' : 0, 'Escalation_Price': 0, 'PY_ListPrice': float(spRemovalDist[MExproductName]['PY_ListPrice']), 'PY_SellPrice': float(spRemovalDist[MExproductName]['PY_SellPrice']), 'SA_Price': 0, 'SR_Price': 0}
			if MESDict:
				scDict['MES Performix'] = MESDict
				productlist.append({'ProductName' : 'MES Performix', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
		elif row['Module'] == 'Honeywell Digital Prime':
			HDPDict = {}
			HDPContainer = row.Product.GetContainerByName('SC_RC_Honeywell_Scope_Summary_Pricing_Hidden')
			HDPDict['Digital Prime Twin'] = {}
			if HDPContainer.TotalRow and 'Digital Prime Twin' not in spRemovalList:
				HDPDict['Digital Prime Twin']['Price'] = float(HDPContainer.TotalRow['Hidden_ListPrice'])
				HDPDict['Digital Prime Twin']['Escalation_Price'] = float(HDPContainer.TotalRow['Escalation_Price'] if HDPContainer.TotalRow['Escalation_Price'] else 0) 
				HDPDict['Digital Prime Twin']['PY_ListPrice'] = float(HDPContainer.TotalRow['PY_ListPrice'] if HDPContainer.TotalRow['PY_ListPrice'] else 0)
				HDPDict['Digital Prime Twin']['PY_SellPrice'] = float(HDPContainer.TotalRow['PY_SellPrice'] if HDPContainer.TotalRow['PY_SellPrice'] else 0)
				HDPDict['Digital Prime Twin']['SR_Price'] = float(HDPContainer.TotalRow['SR_Price'] if HDPContainer.TotalRow['SR_Price'] else 0)
				HDPDict['Digital Prime Twin']['SA_Price'] = float(HDPContainer.TotalRow['SA_Price'] if HDPContainer.TotalRow['SA_Price'] else 0)
				HDPDict['Digital Prime Twin']['Quantity'] = 1
			else:
				HDPDict['Digital Prime Twin'] =  {'Quantity': 0, 'Price' : 0, 'Escalation_Price': 0, 'PY_ListPrice': float(spRemovalDist['Digital Prime Twin']['PY_ListPrice']), 'PY_SellPrice': float(spRemovalDist['Digital Prime Twin']['PY_SellPrice']), 'SA_Price': 0, 'SR_Price': 0}
			if HDPDict:
				scDict['Honeywell Digital Prime'] = HDPDict
				productlist.append({'ProductName' : 'Honeywell Digital Prime', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
		elif row['Module'] == 'Experion Extended Support - RQUP ONLY':
			EESDict = {}
			EESDict_combo = {}
			Service_prod = row.Product.Attr('SC_Exp_Ext_Supp_RQUP_summary').GetValue()
			Model_cont = row.Product.GetContainerByName('SC_Experion_Models_Hidden')
			if str(Service_prod) not in spRemovalList:
				for mod_row in Model_cont.Rows:
					EESDict_combo.setdefault("Asset",[]).append({"MSID":mod_row["MSIDs"], 'Quantity': 1, "List_price":mod_row['List_Price'],"Cost_price":mod_row["Cost_Price"],"Escalation_Price":mod_row["Escalation_Price"],"PY_ListPrice":mod_row["PY_ListPrice"],"PY_SellPrice":mod_row["PY_SellPrice"],"SR_Price":mod_row["SR_Price"],"SA_Price":mod_row["SA_Price"] })
			else:
				for RQproductName in spRemovalDist:
					EESDict_combo["Asset"] =  [{"MSID":'-', 'Quantity': 0, 'List_price' : 0, 'Cost_price': 0, 'Escalation_Price': 0, 'PY_ListPrice': float(spRemovalDist[RQproductName]['PY_ListPrice']), 'PY_SellPrice': float(spRemovalDist[RQproductName]['PY_SellPrice']), 'SA_Price': 0, 'SR_Price': 0}]
			EESDict[str(Service_prod)] = EESDict_combo
			if EESDict:
				scDict['Experion Extended Support - RQUP ONLY'] = EESDict
				productlist.append({'ProductName' : 'Experion Extended Support - RQUP ONLY', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
		elif row['Module'] == 'Workforce Excellence Program':
			WEPDict = GSCUpdProd2.GenProdDictFromConRow(row,spRemovalList,spRemovalDist)
			if WEPDict is not None:
				scDict['Workforce Excellence Program'] = WEPDict
				productlist.append({'ProductName' : 'Workforce Excellence Program', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
		elif row['Module'] == 'Trace':
			TDict = {}
			FDict = {}
			TEntDict = {}
			prodYearDict['Trace'] = int(row.Product.Attr('SC_License_period_Year').GetValue()) if row.Product.Attr('SC_License_type').GetValue() == "Term" else 100
			TEntitleContainer = row.Product.GetContainerByName('SC_Trace_ServiceProduct_Entitlement')
			for erow in TEntitleContainer.Rows:
				TEntDict.setdefault(erow['Service_Product'], []).append(erow['Entitlement'])
			TContainer = row.Product.GetContainerByName('SC_Trace_Summary')
			SC_License_Type = row.Product.Attr('SC_License_Type').GetValue()
			for trow in TContainer.Rows:
				if trow['Service_Product'] not in TDict and trow['Service_Product'] not in spRemovalList:
					TDict[trow['Service_Product']] = {'Quantity': 1, 'ListPrice' : float(trow['List_Price']), 'CostPrice' : float(trow['Cost_Price']),'ExtDescription': TEntDict[trow['Service_Product']] if trow['Service_Product'] in TEntDict else '', 'Escalation_Price' : float(trow['Escalation_Price']) if trow['Escalation_Price'] !='' else 0, 'PY_ListPrice' : float(trow['PY_ListPrice']) if trow['PY_ListPrice'] != '' else 0, 'PY_SellPrice' : float(trow['PY_SellPrice'])if trow['PY_SellPrice'] !='' else 0 , 'SR_Price' : float(trow['SR_Price']) if trow['SR_Price'] != '' else 0, 'SA_Price' : float(trow['SA_Price']) if trow['SA_Price'] != '' else 0}
				if SC_License_Type == 'Term':
					FDict['Year-' + trow['Year']] = {trow['Service_Product']: {'ListPrice' : float(trow['List_Price']), 'CostPrice' : float(trow['Cost_Price'])}}
			for TrproductName in spRemovalDist:
				TDict[TrproductName] =  {'Quantity': 0, 'ListPrice' : 0, 'CostPrice': 0, 'ExtDescription': TrproductName, 'Escalation_Price': 0, 'PY_ListPrice': float(spRemovalDist[TrproductName]['PY_ListPrice']), 'PY_SellPrice': float(spRemovalDist[TrproductName]['PY_SellPrice']), 'SA_Price': 0, 'SR_Price': 0}
			if TDict:
				scDict['Trace'] = TDict
				productlist.append({'ProductName' : 'Trace', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
				if FDict:
					scFyDict['Trace'] = FDict
		elif row['Module'] == 'Hardware Warranty':
			try:
				if row['Type'] == 'Renewal':
					(total, final_sell_price, PriceImpact, ScopeChange, prevListPrice, hw_list_price, hw_cost_price, hw_SA_Price, hw_SR_Price, hw_Escalation_Price, hw_PY_SellPrice) = (0,) * 11
					iQuantity = 1
					service_prd= row.Product.Attr('SC_ServiceProduct_HR_RWL').GetValue()
					prices = {}
					summry = row.Product.GetContainerByName("SC_ModelsHiddenSS_HR_RWL")
					if service_prd not in spRemovalList:
						for i in summry.Rows:
							if i['FinalListPrice'] != '':
								total += float(i['FinalListPrice'])
							if i['FinalSellPrice'] != '':
								final_sell_price += float(i['FinalSellPrice'])
							if i['PreviousYearListPrice'] != '':
								prevListPrice +=  float(i['PreviousYearListPrice'])
							if i['PreviousYearSellPrice'] != '':
								hw_PY_SellPrice +=  float(i['PreviousYearSellPrice'])
							if i['PriceImpact'] != '':
								PriceImpact += float(i['PriceImpact'])
							if i['ScopeChange'] != '':
								ScopeChange += float(i['ScopeChange'])
							if i['Sc_CurrentYearListPrice_HR_RWL'] != '':
								hw_list_price += float(i['Sc_CurrentYearListPrice_HR_RWL'])
							if i['SC_CurrentYearCostPrice_HR_RWL'] != '':
								hw_cost_price += float(i['SC_CurrentYearCostPrice_HR_RWL'])
							if i['SA_Price'] != '':
								hw_SA_Price += float(i['SA_Price'])
							if i['SR_Price'] != '':
								hw_SR_Price += float(i['SR_Price'])
							if i['Escalation_Price'] != '':
								hw_Escalation_Price += float(i['Escalation_Price'])
					prices[service_prd]= {'total':total, 'PriceImpact':PriceImpact, 'ScopeChange':ScopeChange, 'hw_list_price':hw_list_price,'final_sell_price':final_sell_price, 'prevListPrice':prevListPrice, 'hw_cost_price':hw_cost_price, 'hw_SA_Price':hw_SA_Price, 'hw_SR_Price':hw_SR_Price, 'hw_Escalation_Price':hw_Escalation_Price, 'iQuantity':iQuantity, 'hw_PY_SellPrice':hw_PY_SellPrice}
					prevListPrice = hw_PY_SellPrice = 0
					for rproductName in spRemovalDist:
						if rproductName !='':
							if spRemovalDist[rproductName]['PY_ListPrice']:
								prevListPrice+= float(spRemovalDist[rproductName]['PY_ListPrice'])
							if spRemovalDist[rproductName]['PY_SellPrice']:
								hw_PY_SellPrice+= float(spRemovalDist[rproductName]['PY_SellPrice'])
							prices[rproductName]=  {'total':0, 'PriceImpact':0, 'ScopeChange':0, 'hw_list_price':0,'final_sell_price':0, 'prevListPrice':prevListPrice, 'hw_cost_price':0, 'hw_SA_Price':0, 'hw_SR_Price':0, 'hw_Escalation_Price':0, 'iQuantity':0, 'hw_PY_SellPrice':hw_PY_SellPrice}
					scDict['Hardware Warranty Renewal'] = prices
					productlist.append({'ProductName' : 'Hardware Warranty Renewal', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
				else:
					EntList = []
					for erow in row.Product.GetContainerByName('HWOS_Entitlement_Optional').Rows:
						EntList.append(erow['Entitlement'])
					priceSum = qtySum = extCostTot = 0
					for i in row.Product.GetContainerByName('HWOS_Model Scope_3party').Rows:
						priceSum += float(i['List Price'])
						qtySum += float(i['Quantity'])
						extCostTot += float(i['Ext Cost'])
					scDict['Hardware Warranty'] = {'Hardware Warranty': {'Price' : priceSum, 'Qty': qtySum, 'Margin': (1-(extCostTot/priceSum))*100 if priceSum>0 else 0, 'ExtDescription': EntList, 'Cost':extCostTot}}
					productlist.append({'ProductName' : 'Hardware Warranty', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
			except Exception as e:
				Log.Info('Exception in Hardware Warranty' + str(e))

		elif row['Module'] == 'Hardware Refresh':
			try:
				if row['Type'] == 'Renewal':
					(total, final_sell_price, PriceImpact, ScopeChange, prevListPrice, hw_list_price, hw_cost_price, hw_SA_Price, hw_SR_Price, hw_Escalation_Price, hw_PY_SellPrice) = (0,) * 11
					prices = []
					iQuantity = 1
					if not spRemovalList:
						summry = row.Product.GetContainerByName("SC_ModelsHiddenSS_HR_RWL")
						for i in summry.Rows:
							if i['FinalListPrice'] != '':
								total += float(i['FinalListPrice'])
							if i['FinalSellPrice'] != '':
								final_sell_price += float(i['FinalSellPrice'])
							if i['PreviousYearListPrice'] != '':
								prevListPrice +=  float(i['PreviousYearListPrice'])
							if i['PreviousYearSellPrice'] != '':
								hw_PY_SellPrice +=  float(i['PreviousYearSellPrice'])
							if i['PriceImpact'] != '':
								PriceImpact += float(i['PriceImpact'])
							if i['ScopeChange'] != '':
								ScopeChange += float(i['ScopeChange'])
							if i['Sc_CurrentYearListPrice_HR_RWL'] != '':
								hw_list_price += float(i['Sc_CurrentYearListPrice_HR_RWL'])
							if i['SC_CurrentYearCostPrice_HR_RWL'] != '':
								hw_cost_price += float(i['SC_CurrentYearCostPrice_HR_RWL'])
							if i['SA_Price'] != '':
								hw_SA_Price += float(i['SA_Price'])
							if i['SR_Price'] != '':
								hw_SR_Price += float(i['SR_Price'])
							if i['Escalation_Price'] != '':
								hw_Escalation_Price += float(i['Escalation_Price'])
						prices.extend([total,PriceImpact,ScopeChange,hw_list_price,final_sell_price,prevListPrice,hw_cost_price,hw_SA_Price,hw_SR_Price,hw_Escalation_Price,iQuantity,hw_PY_SellPrice])
					else:
						iQuantity = 0
						for rproductName in spRemovalDist:
							if spRemovalDist[rproductName]['PY_ListPrice']:
								prevListPrice+= float(spRemovalDist[rproductName]['PY_ListPrice'])
							if spRemovalDist[rproductName]['PY_SellPrice']:
								hw_PY_SellPrice+= float(spRemovalDist[rproductName]['PY_SellPrice'])
					prices.extend([total,PriceImpact,ScopeChange,hw_list_price,final_sell_price,prevListPrice,hw_cost_price,hw_SA_Price,hw_SR_Price,hw_Escalation_Price,iQuantity,hw_PY_SellPrice])
					scDict['Hardware Refresh Renewal'] = prices
					productlist.append({'ProductName' : 'Hardware Refresh Renewal', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
				else:
					EntList = []
					for erow in row.Product.GetContainerByName('HWOS_Entitlement_Optional').Rows:
						EntList.append(erow['Entitlement'])
					priceSum = qtySum = extCostTot = 0
					for i in row.Product.GetContainerByName('HWOS_Model Scope_3party').Rows:
						priceSum += float(i['List Price'])
						qtySum += float(i['Quantity'])
						extCostTot += float(i['Ext Cost'])
					scDict['Hardware Refresh'] = {'Hardware Refresh': {'Price' : priceSum, 'Qty': qtySum, 'Margin': (1-(extCostTot/priceSum))*100 if priceSum>0 else 0, 'ExtDescription': EntList, 'Cost':extCostTot}}
					productlist.append({'ProductName' : 'Hardware Refresh', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
			except Exception as e:
				Log.Info('Exception in Hardware Refresh' + str(e))

		elif row['Module'] == 'Enabled Services':
			scDict['Enabled Services'] = GSCUpdProd2.GenProdDictFromConRow(row,spRemovalList,spRemovalDist)
			productlist.append({'ProductName' : 'Enabled Services', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
			if 'Matrikon License' in str(scDict['Enabled Services']):
				prodYearDict['Matrikon License'] = 1
		elif row['Module'] == 'Condition Based Maintenance':
			resDict = GSCUpdProd2.GenProdDictFromConRow(row,spRemovalList,spRemovalDist)
			if resDict:
				scDict['Condition Based Maintenance'] = resDict
			productlist.append({'ProductName' : 'Condition Based Maintenance', 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
	return productlist, scDict, prodYearDict, scFyDict