PLSGFctrW2W = SqlHelper.GetList("SELECT WTW_FACTOR, Category FROM HPS_PLSG_WTW_FACTOR (nolock) JOIN WRITEINPRODUCTS(NOLOCK) ON ProductLineSubGroup = PL_PLSG  WHERE Product IN ('Write-In Process History and Analytics Srvc - BGP','Write-In Third Party Hardware & Software') ")
W2WDict = {i.Category:i.WTW_FACTOR for i in PLSGFctrW2W}

def calculate_sums(child_part_list, condition):
	price_sum = 0.0
	cost_sum = 0.0

	for item in child_part_list:
		if condition(item):
			price_sum += float(item.ExtendedListPrice)
			cost_sum += float(item.ExtendedCost)
			Trace.Write(str(item.PartNumber)+'-list prices '+str([str(item.ExtendedListPrice), str(item.ExtendedCost)]))
	return price_sum, cost_sum

def HCISoftwareWriteInCalc(Quote, item, AddWriteIns):
	productItemValues = {}
	itemValues = {val.Name: val.Values[0].Display for val in item.SelectedAttributes if val.Name in (
			'HCI_PHD_Product', 'HCI_PHD_BGP_SUPPORT', 'HCI_PHD_LicenseModel', 
			'HCI_PHD_OrderType', 'HCI_PHD_Scope', 'HCI_PHD_ESCALATIONFACTOR', 
			'Trace_Software_Do_you_need_hardware','Number_Of_Configurations_EDM')}
	productItemValues.update(itemValues)
	ChildPartList = [i for i in Quote.Items if (i.PartNumber in ('AS-UNSGHTS','AS-UNPHDES', 'AS-PHDAS', 'AS-PHDRDI','AS-PHDRDIS') or 'TP-' in i.PartNumber) and i.QI_VCProducts.Value == productItemValues.get('Number_Of_Configurations_EDM')]	
	Trace.Write('-irem-'+str(productItemValues))

	PHDProduct = productItemValues.get('HCI_PHD_Product')
	BGPSupportYr =  int(float(productItemValues.get('HCI_PHD_BGP_SUPPORT') or 1))
	LicenseModel =  productItemValues.get('HCI_PHD_LicenseModel')
	OrderType =  productItemValues.get('HCI_PHD_OrderType')
	PHDScope =  productItemValues.get('HCI_PHD_Scope')
	EscalatedFctr = productItemValues.get('HCI_PHD_ESCALATIONFACTOR')
	isHardwareRequired = productItemValues.get('Trace_Software_Do_you_need_hardware')
	

	if BGPSupportYr > 0:
		#AddWriteIns = AddWriteInSoftwareHardware(childItems)
		writeInProductQuery = SqlHelper.GetList("SELECT Product, PRODUCTALIAS, WRITEINS_DESC,PRODUCTLINE, PRODUCTLINEDESCRIPTION, PRODUCTLINESUBGROUPDESCRIPTION, PRODUCTLINESUBGROUP, PRODUCTCATEGORY FROM WRITEINPRODUCTS (nolock) JOIN CT_SW_HW_WRITEINS(NOLOCK) ON Product = WRITEINS  WHERE Category = 'HCP' AND PRODUCTNAME = '"+str(PHDProduct)+"' ")	

		SumofChildPrice, SumofChildCost = 0.00, 0.00
		part_mapping = {
			'Advanced Formula Manager (AFM)': lambda item: 'TP-' in item.PartNumber,
			'Insight': lambda item: item.PartNumber in ['AS-UNSGHTS'],
			'Process History Database (PHD)': lambda item: item.PartNumber in ['AS-UNPHDES', 'AS-PHDAS', 'AS-PHDRDI','AS-PHDRDIS']
		}
		costPriceDict = {}
		splitFlag = False
		other_products = ['PHD & Insight', 'PHD & Insight & AFM']
		escalatedYearWiseListPrice , escalatedYearWiseCost = 0.0 , 0.0
		if LicenseModel == 'Perpetual':
			Trace.Write('PHDProduct--'+str(PHDProduct))
			if (PHDScope == 'New Implementation' and OrderType == 'Standard New Commercial License') or PHDScope == 'Expansion':
				Trace.Write('if i pHD')
				if PHDProduct in part_mapping:
					condition = part_mapping[PHDProduct]
					SumofChildPrice, SumofChildCost = calculate_sums(ChildPartList, condition)
					#Trace.Write('SumofChildPrice 1-'+str(SumofChildPrice))
					escalatedYearWiseListPrice = float((SumofChildPrice/100)*20)
					escalatedYearWiseCost = float((escalatedYearWiseListPrice/100)*55)
				elif PHDProduct in other_products:
					splitFlag = True
					splitPrd = PHDProduct.split(' & ')
					aliasDict = {'AFM':'Advanced Formula Manager (AFM)','Insight':'Insight','PHD':'Process History Database (PHD)'}
					for i in splitPrd:
						condition = part_mapping[aliasDict[i]]
						SumofChildPrice, SumofChildCost = calculate_sums(ChildPartList, condition)
						Trace.Write('SumofChildPrice-'+str(SumofChildPrice))
						escalatedYearWiseListPrice = float((SumofChildPrice/100)*20)
						escalatedYearWiseCost = float((escalatedYearWiseListPrice/100)*55)
						costPriceDict[i] = [escalatedYearWiseListPrice, escalatedYearWiseCost]

			
			elif ((PHDScope == 'New Implementation' and OrderType == 'Competitive Replacement') or PHDScope == 'Upgrade' and OrderType =='Non-Support Upgrade') and OrderType != 'Maintenance Support Upgrade/Update (No Charge/ BGP Active)':
				Trace.Write('if iI pHD')
				if PHDProduct in part_mapping:
					condition = part_mapping[PHDProduct]
					SumofChildPrice, SumofChildCost = calculate_sums(ChildPartList, condition)
					escalatedYearWiseListPrice = float((SumofChildPrice/100)*40) if PHDProduct!='Advanced Formula Manager (AFM)' else float((SumofChildPrice/100)*20)
					escalatedYearWiseCost = float((escalatedYearWiseListPrice/100)*55)
				elif PHDProduct in other_products:
					splitFlag = True
					splitPrd = PHDProduct.split(' & ')
					aliasDict = {'AFM':'Advanced Formula Manager (AFM)','Insight':'Insight','PHD':'Process History Database (PHD)'}
					for i in splitPrd:
						condition = part_mapping[aliasDict[i]]
						SumofChildPrice, SumofChildCost = calculate_sums(ChildPartList, condition)
						escalatedYearWiseListPrice = float((SumofChildPrice/100)*40) if aliasDict[i]!= 'Advanced Formula Manager (AFM)' else float((SumofChildPrice/100)*20)
						escalatedYearWiseCost = float((escalatedYearWiseListPrice/100)*55)
						costPriceDict[i] = [escalatedYearWiseListPrice, escalatedYearWiseCost]
		
		SupportWriteIns = list(range(1,BGPSupportYr+1,1))
		#Trace.Write('SupportWriteIns--'+str(SupportWriteIns))
		for writeIn in writeInProductQuery:
			if splitFlag:
				Trace.Write(str(writeIn.PRODUCTALIAS)+'--costPriceDict--'+str(costPriceDict))
				escalatedYearWiseListPrice = costPriceDict[writeIn.PRODUCTALIAS][0] if writeIn.PRODUCTALIAS in costPriceDict else 0
				escalatedYearWiseCost = costPriceDict[writeIn.PRODUCTALIAS][1] if writeIn.PRODUCTALIAS in costPriceDict else 0
			for i in SupportWriteIns:
				if str(i)!= '1':
					escalatedYearWiseListPrice = float(escalatedYearWiseListPrice) * (1+(float(EscalatedFctr)/100))
					escalatedYearWiseCost = float((escalatedYearWiseListPrice/100)*55)	
				AddWriteIns[str(writeIn.WRITEINS_DESC).replace(' Yr', ' '+str(i)+'Yr')] = {'Product': str(writeIn.Product), 'UnitListPrice': str(escalatedYearWiseListPrice), 'UnitRegionalCost': str(escalatedYearWiseCost), 'QTY': 1, 'W2WCost':W2WDict.get('HCP'),'ProductLine':str(writeIn.PRODUCTLINE),'PLSGDesc':str(writeIn.PRODUCTLINEDESCRIPTION),'PLSG':str(writeIn.PRODUCTLINESUBGROUP),'CostCategory':str(writeIn.PRODUCTCATEGORY)}
	
		if isHardwareRequired == 'Yes':
			writeInProductQuery = SqlHelper.GetFirst("SELECT Product, UnitofMeasure,PRODUCTLINE, PRODUCTLINEDESCRIPTION, PRODUCTLINESUBGROUPDESCRIPTION, PRODUCTLINESUBGROUP, PRODUCTCATEGORY FROM WRITEINPRODUCTS (nolock) WHERE Category = 'Common' AND Product = 'Write-In Third Party Hardware & Software' ")
			getThirdParty = item.SelectedAttributes.GetContainerByName('HCI_Thrid_Party_Hardware')
			for rows in getThirdParty.Rows:
				if rows['Third_Party_Hardware']!= 'Total Number of Servers':
					listprice = float(rows['Price']) if str(rows['Price']) else 0
					costprice = float(rows['Cost']) if str(rows['Cost']) else 0
					qty = float(rows['Qty']) if str(rows['Qty']) else 0
					AddWriteIns[rows['Third_Party_Hardware']] = {'Description':rows['Extended_Description'],'UnitListPrice': str(listprice), 'UnitRegionalCost': str(costprice), 'QTY': qty, 'W2WCost':W2WDict.get('Common'),'ProductLine':str(writeInProductQuery.PRODUCTLINE),'PLSGDesc':str(writeInProductQuery.PRODUCTLINEDESCRIPTION),'PLSG':str(writeInProductQuery.PRODUCTLINESUBGROUP),'CostCategory':str(writeIn.PRODUCTCATEGORY)}
	'''getparentlistPrice = sum(float(i['UnitListPrice']) for i in AddWriteIns.values())
	getparentcostprice = sum(float(i['UnitRegionalCost']) for i in AddWriteIns.values())
	AddWriteIns[item.PartNumber] =  {'UnitListPrice': str(float(getparentlistPrice)+float(item.ExtendedListPrice)), 'UnitRegionalCost': str(float(getparentcostprice)+float(item.ExtendedCost) ), 'QTY': 1, 'W2WCost':W2WDict.get('Common')}'''
	Trace.Write('AddWriteIns--'+str(AddWriteIns))
	return AddWriteIns