if Product.Attr('R2QRequest').GetValue() != 'Yes':
	CurrentTab=Product.Tabs.GetByName('Labor Deliverables').IsSelected
	if CurrentTab == True:
		from GS_CyberProductModule import CyberProduct
		cyber = CyberProduct(Quote, Product, TagParserQuote)
		excecutionCountry = cyber.getExecutionCountry()

		allDeliverableList = ['Migration Audit','Site Visit Data Gathering','GAP Analysis','Plan Review and KOM','Hardware & Software Order','Documentation','In-house Engineering','Configuration','Pre-FAT','Factory Acceptance Test','Travel Time','Internal & External training','Project Close-out','Commissioning','Site Acceptance Test','Site Activities']

		requiredproductList = []
		targetProductList = ['SMX','PCN Hardening','MSS','Cyber App Control','Assessments','Cyber Generic System']
		for row in Product.GetContainerByName('Cyber Configurations').Rows:
			if row['Part Desc'] !='Project Management':
				requiredproductList.append(row['Part Desc'])
		notrequiredproductList = list(set(targetProductList) - set(requiredproductList))

		if Product.GetContainerByName('AR_Cyber_AdditionalCustomDeliverable').Rows.Count > 0:
			for customRow in Product.GetContainerByName('AR_Cyber_AdditionalCustomDeliverable').Rows:
				productDeliverable = []
				invalidDeliverables = []
				customRow.Product.DisallowAttrValues('AR_CyberPrdChoices', *notrequiredproductList)
				customRow.Product.AllowAttrValues('AR_CyberPrdChoices', *requiredproductList)
				if customRow['Product_Module'] == '':
					customRow.Product.Attr('AR_CyberPrdChoices').SelectDisplayValue(requiredproductList[0])
					customRow['Product_Module'] = requiredproductList[0]
				else:
					customRow.Product.Attr('AR_CyberPrdChoices').SelectDisplayValue(customRow['Product_Module'])
					customRow['Product_Module'] = customRow['Product_Module']
				if customRow['Product_Module'] in ['SMX','MSS','Cyber App Control']:
					if 'Travel Time' in allDeliverableList:
						allDeliverableList.remove('Travel Time')
					if 'Travel Time' not in invalidDeliverables:
						invalidDeliverables.append('Travel Time')
				if customRow['Product_Module'] == 'Assessments':
					product_name = 'Assessment'
				else:
					product_name = customRow['Product_Module']

				deleiverabletable = SqlHelper.GetList("SELECT Product_Module, UI_Deliverables FROM LSS_Deliverables_Mapping WHERE Product_Module = '{}'".format(product_name))

				for data in deleiverabletable:
					if data.UI_Deliverables in allDeliverableList:
						productDeliverable.append(data.UI_Deliverables)
				invalidDeliverables.extend(set(allDeliverableList) - set(productDeliverable))
				customRow.Product.AllowAttrValues('Labor_Standard_Deliverable_selection', *productDeliverable)
				customRow.Product.DisallowAttrValues('Labor_Standard_Deliverable_selection', *invalidDeliverables)

				if customRow['Activity'] == '' or customRow['Activity'] not in productDeliverable:
					customRow.Product.Attr('Labor_Standard_Deliverable_selection').SelectDisplayValue(productDeliverable[0])
					customRow['Activity'] = productDeliverable[0]
				else:
					customRow.Product.Attr('Labor_Standard_Deliverable_selection').SelectDisplayValue(customRow['Activity'])
					customRow['Activity'] = customRow['Activity']

				customRow["Execution Country"] = excecutionCountry
				customRow.GetColumnByName('Execution Country').SetAttributeValue(excecutionCountry)

				customRow.Calculate()