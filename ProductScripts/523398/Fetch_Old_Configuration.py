if Quote.GetCustomField("Quote Type").Content == "Contract Renewal":
	#to populate previous quote configuration data to renewal quote
	from CPQ_SF_SC_Modules import CL_SC_Modules
	from GS_SC_GetQuoteData import CL_QuoteHandler
	class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None,Session)
	Contract_Number = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
	quotetype = Quote.GetCustomField("Quote Type").Content
	cont = Product.GetContainerByName("Service Contract Modules")
	quoteNumber = Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content
	contractExtension = Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content
	currentQuoteCurrency = Quote.SelectedMarket.CurrencyCode
	update_dict_gen = {}

	col_dict = {'Model':'Model_Number','Quantity':'PY_Quantity','Unit_Cost_Price':'PY_CostPrice','Unit_List_Price':'PY_ListPrice'}
	reference_number = quoteNumber
	Exchange_Rate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content and Quote.GetCustomField("Quote Type").Content == 'Contract Renewal' else 1
	CF_ErpRef_No = Quote.GetCustomField('SC_CF_ERPREFNO').Content

	def getQuoteDetails(reference_number):
		a = SqlHelper.GetFirst("select QuoteDetails from CT_SC_Renewal_Quote_Table where QuoteID = '{}'".format(reference_number))
		result= {}
		if a is not None:
			b = a.QuoteDetails
			z = eval(b)
			for k,v in z.items():
				if 'Year-1' not in k:
					continue
				result[k.replace('Year-1|Labor Deliverables|', '')] = v
		return result

	def UpdateComparisionSummary_SESP(mProd, ltrainingMatchValue):
		cont = mProd.GetContainerByName('ComparisonSummary')
		if cont.Rows.Count:
			for irow in cont.Rows:
				irow['PY_List_Price_SFDC'] = str(float(irow['PY_List_Price_SFDC']) - ltrainingMatchValue)
				irow['PY_Sell_Price_SFDC'] = str(float(irow['PY_Sell_Price_SFDC'])- ltrainingMatchValue)
				irow['PY_Training_Match_SFDC'] =str(float(ltrainingMatchValue))
			cont.Calculate()

	def populateComparisionSummary(mProd, Contract_Number,CPQ_PList_Inactive, class_contact_modules, isES = 0, Service_Product = ''):
		cont = mProd.GetContainerByName('ComparisonSummary')
		productName = mProd.Name if mProd.Name != 'Generic Module' else Service_Product
		if mProd.Name == 'Generic Module':
			Service_Product = ''
		if isES:
			cont = mProd.GetContainerByName('ESComparisonSummary')
			productName = 'Enabled Services'
		if not cont:
			return
		resp = class_contact_modules.get_ServiceContract_QuoteLine_Data(Contract_Number, productName)
		cont.Rows.Clear()
		if resp and resp["records"]:
			for scProd in resp["records"]:
				PYContractCurrency = str(scProd['CurrencyIsoCode'])
				Ex_Rate = 1 / float(Quote.GetCustomField('SC_CF_PRVYR_EXCHANGE_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCHANGE_RATE').Content and PYContractCurrency != 'USD' and currentQuoteCurrency == 'USD' else Exchange_Rate
				if Service_Product == '' or Service_Product == str(scProd["Product_Name__c"]):
					row = cont.AddNewRow(False)
					row['Service_Product'] = str(scProd["Product_Name__c"])
					row['PY_List_Price_SFDC'] = str(float(scProd["List_Price__c"])*Ex_Rate) if str(scProd["List_Price__c"]) != '' else '0'
					row['Configured_PY_List_Price'] = '0'
					row['List_Price_Delta'] = str(float(scProd["List_Price__c"])*Ex_Rate) if str(scProd["List_Price__c"]) != '' else '0'
					row['PY_Sell_Price_SFDC'] = str(float(scProd["Booked_Value__c"])*Ex_Rate) if str(scProd["Booked_Value__c"]) != '' else '0'
					if Service_Product == str(scProd["Product_Name__c"]):
						row['Configured_PY_Sell_Price'] = row['PY_Sell_Price_SFDC']
						row['Sell_Price_Delta'] = '0'
					else:
						row['Configured_PY_Sell_Price'] = '0'
						row['Sell_Price_Delta'] = str(float(scProd["Booked_Value__c"])*Ex_Rate) if str(scProd["Booked_Value__c"]) != '' else '0'
					row['Booked_Margin'] = str(float(scProd["Booked_Margin__c"])*Ex_Rate) if str(scProd["Booked_Margin__c"]) != '' else '0'
					row['PY_Discount_SFDC'] = str(1-(float(row['PY_Sell_Price_SFDC'])*Ex_Rate/(float(row['PY_List_Price_SFDC'])*Ex_Rate))) if row['PY_Sell_Price_SFDC'] and row['PY_List_Price_SFDC'] and float(row['PY_List_Price_SFDC'])!=0 else '0'
					row['PY_Service_Prod_Status'] = "Active"
					if row['Service_Product'] in CPQ_PList_Inactive:
						row.IsSelected = True
						row['PY_Service_Prod_Status'] = "Inactive"
			cont.Calculate()

	def populate_configuration_hardware(rowp):
		try:
			if query:
				var = eval(query.ProductDetails)
				for attr in var:
					if attr["Name"] == "HWOS_Model Scope_3party":
						con = rowp.Product.GetContainerByName("SC_ValidModels_HR_RWL")
						if not con.Rows.Count > 0:
							for oldVModelRecord in attr["Value"]:
								row = con.AddNewRow(False)
								row["SC_Asset_HR_RWL"] = oldVModelRecord["Asset"]
								row["SC_Model_HR_RWL"] = oldVModelRecord["3rd Party Model"]
								row["SC_Description_HR_RWL"] = oldVModelRecord["Description"]
								row["SC_Quantity_HR_RWL"] = oldVModelRecord["Quantity"]
								row["SC_PreviousYearUnitPrice_HR_RWL"] = str(float(oldVModelRecord["Unit List Price"])*Exchange_Rate) if oldVModelRecord["Unit List Price"] else 0
								row["SC_PreviousYearListPrice_HR_RWL"] = str(float(oldVModelRecord["List Price"])*Exchange_Rate) if oldVModelRecord["List Price"] else 0
								row['SC_PreviousYearUnitCostPrice_HR_RWL'] = str(float(oldVModelRecord["Unit Cost"])*Exchange_Rate) if oldVModelRecord["Unit Cost"] else 0
								row['SC_PreviousYearCostPrice_HR_RWL'] = str(float(oldVModelRecord["Ext Cost"])*Exchange_Rate) if oldVModelRecord["Ext Cost"] else 0
								row["SC_RenewalQuantity_HR_RWL"] = '0'
								row["SC_Comment_HR_RWL"] = "Scope Reduction"
								row["Select"] = oldVModelRecord["Select"]
					elif attr["Name"] == "SC_HWOS_Service_Product":
						rowp.Product.Attr("SC_ServiceProduct_HR_RWL").AssignValue(str(attr["Value"]))
						rowp.Product.Attr("SC_ServiceProduct_HR_RWL").Access = AttributeAccess.ReadOnly
					elif attr['Name'] == "HWOS_Entitlement":
						con = rowp.Product.GetContainerByName('SC_Entitlements_HR_RWL')
						for i in attr['Value']:
							row = con.AddNewRow(False)
							row['SC_Entitlement_HR_RWL'] = i['Entitlement']
							row.IsSelected = True if str(i['Include']).lower() == 'true' else False
						else:
							con.Calculate()
				"""else:
					if rowp['Module'] == 'Hardware Refresh':
						setDefaultValues = SqlHelper.GetList("select ServiceProduct, Entitlement from CT_SC_ENTITLEMENTS_DATA where IsMandatory = 'FALSE' and ServiceProduct = N'{}'".format('Hardware Refresh'))
						con = rowp.Product.GetContainerByName('SC_Entitlements_HR_RWL')
						for i in setDefaultValues:
							n = con.AddNewRow(False)
							n['SC_Entitlement_HR_RWL'] = i.Entitlement
							n.IsSelected = False
						else:
							con.Calculate()"""
		except Exception as e:
			Trace.Write('Exception occured in populate_configuration_hardware method -> '+str(e))

	def writeContianer(Mod_Name):
		contvar = eval(str(i['Value']))
		contName = i['Name']
		cont2 = row.Product.GetContainerByName(contName)
		cont2.Rows.Clear()
		if contName == "SC_Labor_Summary_Container":
			result = getQuoteDetails(reference_number)
		for j in contvar:
			row2 = cont2.AddNewRow(False)
			for col in row2.Columns:
				if col.Name not in j:
					continue
				if col.DisplayType == "DropDown":
					row2.GetColumnByName(col.Name).SetAttributeValue(j[col.Name])
					row2[col.Name] = j[col.Name]
				elif col.DisplayType == "SelectorCheckBox":
						row2.IsSelected = True if j[col.Name] == 'True' else False
				elif col.DisplayType == "AutocompleteCustomTable":
					try:
						row2.GetColumnByName(col.Name).ReferencingAttribute.SelectDisplayValue(j[col.Name],False)
						row2[col.Name] = j[col.Name]
					except Exception as e:
						Trace.Write('Exception in autocomplete-->'+str(e))
						Trace.Write('autocomplete-2-->'+str([col.Name,contName]))
				else:
					row2[col.Name] = j[col.Name]
					if contName == "SC_GN_AT_Models_Scope_Cont" and col.Name in col_dict.keys():
						row2[col_dict[col.Name]] = j[col.Name]
						update_dict_gen[row2.UniqueIdentifier] = j
						update_dict_gen[row2.UniqueIdentifier]['ModuleName'] = Mod_Name

			if contName == "SC_Labor_Summary_Container":
				row2['Product_Type'] = '0'
				if result.get(row2['Service_Product'] + "|" + row2['Entitlement'] + "|" + row2['Resource_Type'], ""):
					row2['PY_UnitPrice'] = str(float(result[row2['Service_Product'] + "|" + row2['Entitlement'] + "|" + row2['Resource_Type']]['ListPrice'])/float(row2['Deliverable_Hours']))
					row2['PY_ListPrice'] = result[row2['Service_Product'] + "|" + row2['Entitlement'] + "|" + row2['Resource_Type']]['ListPrice']
					row2['PY_SellPrice'] = result[row2['Service_Product'] + "|" + row2['Entitlement'] + "|" + row2['Resource_Type']]['SellPrice']
					row2['PY_Discount'] = result[row2['Service_Product'] + "|" + row2['Entitlement'] + "|" + row2['Resource_Type']]['TotalDiscount']
			#row2.ApplyProductChanges()
			row2.Calculate()
		cont2.Calculate()

	def writelaborContianer(row3,contName,contvar):
		cont3 = row3.Product.GetContainerByName(contName)
		cont3.Rows.Clear()
		for j in contvar:
			row4 = cont3.AddNewRow(False)
			for col in row4.Columns:
				try:
					if col.DisplayType == "DropDown":
						row4.GetColumnByName(col.Name).SetAttributeValue(j[col.Name])
						row4[col.Name] = j[col.Name]
					elif col.DisplayType == "SelectorCheckBox":
						row4.IsSelected = True if j[col.Name] == 'True' else False
					elif col.DisplayType == "AutocompleteCustomTable":
						row4.GetColumnByName(col.Name).ReferencingAttribute.SelectDisplayValue(j[col.Name],False)
						row4[col.Name] = j[col.Name]
					else:
						row4[col.Name] = j[col.Name]
				except:
					pass
			#row4.ApplyProductChanges()
		cont3.Calculate()


	def populateDeliverables(i):
		contName = i['Name']
		cont2 = row.Product.GetContainerByName(contName)
		for row3 in cont2.Rows:
			row3['Type'] = 'Renewal'
			row3.GetColumnByName('Type').ReferencingAttribute.AssignValue('Renewal')
			query_deliv = SqlHelper.GetFirst("Select Product,ProductDetails from SC_RENEWAL_TABLE where Product = 'Labor Deliverables' and LaborRowId = '{0}' and QuoteID = '{1}' UNION ALL Select Product,ProductDetails from SC_RENEWAL_TABLE where Product = 'Labor Deliverables' and LaborRowId = '{0}' and QuoteID = '{2}' AND NOT EXISTS (SELECT 1 FROM SC_RENEWAL_TABLE WHERE QuoteID = '{1}')".format(row3.RowIndex,reference_number, reference_number.split('-')[0]))
			if query_deliv is not None:
				var = eval(query_deliv.ProductDetails)
				for i in var:
					if i['Type'] == 'FreeInputNoMatching':
						row3.Product.Attributes.GetByName(i['Name']).AssignValue(i['Value'])
					elif i['Type'] == 'DropDown':
						row3.Product.Attributes.GetByName(i['Name']).SelectValue(i['Value'])
					elif i['Type'] in ('CheckBox', 'ListBoxMultipleSelect'):
						attrValue = i['Value'].split(', ')
						row3.Product.Attributes.GetByName(i['Name']).SelectValues(*attrValue)
					elif i['Type'] == 'AutoCompleteCustomTable':
						row3.Product.Attributes.GetByName(i['Name']).SelectDisplayValue(i['Value'],False)
					elif i['Type'] == 'Container':
						contName = i['Name']
						contvar = eval(str(i['Value']))
						writelaborContianer(row3,contName,contvar)
				row3.Product.Attributes.GetByName('SC_Renewal_check').AssignValue('0')
				row3.Product.Attributes.GetByName('SC_Product_Type').AssignValue('Renewal')

				### Contract Extension Logic Starts ###
				if contractExtension == "True":
					row3.Product.Attributes.GetByName('SC_Labor_Pricing_Escalation_Based').SelectValue('Yes')
				### Contract Extension Logic Ends ###

				row3.Product.ApplyRules()
				row3.ApplyProductChanges()
				row3.Calculate()

	if cont.Rows.Count == 0:
		if reference_number:
			TagParserProduct.ParseString("<*CTX ( Container(Service Contract Modules ).Column(Apply OPB file).SetPermission(Hidden) )*>")
			prodQuery = SqlHelper.GetList("Select Product,SystemID from SC_RENEWAL_TABLE where QuoteID = '{0}' UNION ALL Select Product,SystemID from SC_RENEWAL_TABLE where QuoteID = '{1}' AND NOT EXISTS (SELECT 1 FROM SC_RENEWAL_TABLE WHERE QuoteID = '{0}')".format(reference_number, reference_number.split('-')[0]))
			generic_module = {}
			if prodQuery is not None:
				for i in prodQuery:
					crow = cont.AddNewRow(i.SystemID,True)
					if crow:
						crow['Product_Name'] = i.Product
						generic_module[str(crow.RowIndex)] = i.Product
				cont.Calculate()
			deleteRowsId = []
			if cont.Rows.Count:
				for row in cont.Rows:
					row['Type'] = 'Renewal'
					row.GetColumnByName('Type').ReferencingAttribute.AssignValue('Renewal')
					row.Product.Attr('SC_Product_Type').AssignValue('Renewal')
					prod = row.Product
					Trace.Write("Product : >>>>>> "+str(row.Product))
					query = SqlHelper.GetFirst("Select Product,ProductDetails from SC_RENEWAL_TABLE where Product = '{0}' and QuoteID = '{1}' UNION ALL Select Product,ProductDetails from SC_RENEWAL_TABLE where Product = '{0}' and QuoteID = '{2}' AND NOT EXISTS (SELECT 1 FROM SC_RENEWAL_TABLE WHERE QuoteID = '{1}')".format(row['Module'] if row['Module'] != 'Generic Module' else generic_module[str(row.RowIndex)],reference_number, reference_number.split('-')[0]))
					if row['Module'] == 'Hardware Refresh' or row['Module'] == 'Hardware Warranty':
						row['Product_Status'] = 'Incomplete'
						populate_configuration_hardware(row)
						row.Product.Attributes.GetByName('SC_Product_Type').AssignValue('Renewal')
						Product.Attr('SC_Product_Status').AssignValue('Please review the configuration of following Module(s)')
					else:
						if query is not None:
							var = eval(query.ProductDetails)
							for i in var:
								if i['Type'] == 'FreeInputNoMatching':
									row.Product.Attributes.GetByName(i['Name']).AssignValue(i['Value'])
								elif i['Type'] == 'DropDown':
									row.Product.Attributes.GetByName(i['Name']).SelectValue(i['Value'])
								elif i['Type'] == 'CheckBox':
									attrValue = i['Value'].split(', ')
									row.Product.Attributes.GetByName(i['Name']).SelectValues(*attrValue)
								elif i['Type'] == 'AutoCompleteCustomTable':
									row.Product.Attributes.GetByName(i['Name']).SelectDisplayValue(i['Value'],False)
								elif i['Type'] == 'ListBoxMultipleSelect':
									attrValue = i['Value'].split(', ')
									row.Product.Attributes.GetByName(i['Name']).SelectValues(*attrValue)
								elif i['Type'] == 'Container':
									writeContianer(generic_module[str(row.RowIndex)])
									if row['Module'] == "Labor" and i['Name'] == "SC_Labor_Summary_Container":
										populateDeliverables(i)
										laborrows = row.Product.GetContainerByName(i['Name']).Rows
										for laborrow in laborrows:
											laborrow.ApplyProductChanges()
											laborrow.Calculate()
						row.Product.Attributes.GetByName('SC_Product_Type').AssignValue('Renewal')
						row.Product.Attributes.GetByName('SC_Renewal_check').AssignValue('0')
						row.Product.Attributes.GetByName('SC_Product_Status').AssignValue('0')

					### Contract Extension Logic Starts ###
					if contractExtension == "True":
						if row['Module']  not in ('Workforce Excellence Program', 'Labor'):
							row.Product.Attributes.GetByName('SC_Pricing_Escalation').SelectValue('Yes')
						elif row['Module'] == "Workforce Excellence Program":
							for esc in ['SC_WEP_HIF_Pricing_Escalation','SC_WEP_IFS_Pricing_Escalation','SC_WEP_Halo_Pricing_Escalation','SC_WEP_Training_Pricing_Escalation','SC_WEP_TNA_Pricing_Escalation','SC_WEP_OM_Pricing_Escalation','SC_WEP_OCP_Pricing_Escalation']:
								row.Product.Attributes.GetByName(esc).SelectValue('Yes')
					### Contract Extension Logic Ends ###

					row["Product_Status"] = "Incomplete"
					if row['Module'] == 'Generic Module':
						row['Product_Name'] = generic_module[str(row.RowIndex)]
					if prod.Name == 'Solution Enhancement Support Program':
						populateComparisionSummary(row.Product, Contract_Number,[], class_contact_modules)
						populateComparisionSummary(row.Product, Contract_Number,[], class_contact_modules, 1)
					elif prod.Name == 'Enabled Services':
						populateComparisionSummary(row.Product, Contract_Number,[], class_contact_modules, 1)
					elif row['Module'] == 'Generic Module':
						row.Product.Attr('SC_GN_AT_Product_Family').SelectDisplayValue(generic_module[str(row.RowIndex)],False)
						populateComparisionSummary(row.Product, Contract_Number,[], class_contact_modules, 0, generic_module[str(row.RowIndex)])
					else:
						populateComparisionSummary(row.Product, Contract_Number,[], class_contact_modules)
					row.Product.ApplyRules()
					row.ApplyProductChanges()
					row.Calculate()
					#Uncheck enabled services checkbox if enabled services is not part of the renewal contract
					if prod.Name == 'Solution Enhancement Support Program' and prod.Attr('EnableSelection_SESP').GetValue() == '&nbsp' and prod.GetContainerByName('ESComparisonSummary').Rows.Count == 0:
						values = prod.Attr('EnableSelection_SESP').Values
						for v in values:
							v.IsSelected = False
						prod.GetContainerByName("Asset_details_ServiceProd").Rows.Clear()
						prod.Attr('SC_Renewal_check').AssignValue('1')
					#check comparison summary container has populated, if not remove the module from the container
					compContName = 'ComparisonSummary' if prod.Name != 'Enabled Services' else 'ESComparisonSummary'
					compCont = prod.GetContainerByName(compContName)
					if compCont.Rows.Count == 0:
						deleteRowsId.append(row.RowIndex)
			#Remove modules which are not part of the renewal contract
			if len(deleteRowsId) > 0:
				deleteRowsId.sort(reverse=True)
				for i in deleteRowsId:
					cont.DeleteRow(i)
				cont.Calculate()
		else:
			Contract_Number = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
			if Contract_Number:
				import GS_SC_OPB_ES_SESP_Module
				#class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None,Session)
				resp = class_contact_modules.get_ServiceContract_QuoteLine_Data(Contract_Number)
				Product_list =	[str(record["Product_Name__c"]) for record in resp["records"]]
				if Product_list:
					serviceProductES, serviceProductSESP = GS_SC_OPB_ES_SESP_Module.getServiceProducts()
					isES, isSESP, EnabledServices_servprod, SC_Service_Product, SC_Coverage = GS_SC_OPB_ES_SESP_Module.getConfiguredServiceProducts(Product_list, serviceProductES, serviceProductSESP)
					#PList = SqlHelper.GetList("SELECT DISTINCT P.SYSTEM_ID, P.PRODUCT_NAME, C.PRODUCTTYPE_NAME, S.Module_Name_GN FROM CT_SC_Entitlements_Data as S INNER JOIN PRODUCTS as P ON P.PRODUCT_NAME=S.Module_Name INNER JOIN PRODUCT_TYPES_DEFN as C on P.PRODUCTTYPE_CD = C.PRODUCTTYPE_CD WHERE C.PRODUCTTYPE_NAME = 'Service Contract' and P.PRODUCT_ACTIVE = 'True' and S.ServiceProduct in {}".format(str(tuple(Product_list)).replace(',)',')')))
					#ALL_PList = SqlHelper.GetList("SELECT DISTINCT ServiceProduct,Module_Name,Status FROM CT_SC_Entitlements_Data WHERE ServiceProduct in {}".format(str(tuple(Product_list)).replace(',)',')')))
					PList = SqlHelper.GetList("SELECT DISTINCT P.SYSTEM_ID, P.PRODUCT_NAME, C.PRODUCTTYPE_NAME, S.Module_Name_GN FROM CT_SC_Entitlements_Data as S INNER JOIN PRODUCTS as P ON P.PRODUCT_NAME=S.Module_Name INNER JOIN PRODUCT_TYPES_DEFN as C on P.PRODUCTTYPE_CD = C.PRODUCTTYPE_CD WHERE C.PRODUCTTYPE_NAME = 'Service Contract' and P.PRODUCT_ACTIVE = 'True' and S.ServiceProduct in {} and S.Module_Name_GN != 'Offline Products'".format(str(tuple(Product_list)).replace(',)',')')))
					ALL_PList = SqlHelper.GetList("SELECT DISTINCT ServiceProduct,Module_Name,Status FROM CT_SC_Entitlements_Data WHERE ServiceProduct in {} and Module_Name_GN != 'Offline Products'".format(str(tuple(Product_list)).replace(',)',')')))
					#CPQ_PList = [lst.ServiceProduct for lst in ALL_PList]
					CPQ_PList = []
					CPQ_PList_Inactive = []
					for lst in ALL_PList:
						CPQ_PList.append(lst.ServiceProduct)
						if lst.Status.lower() == 'inactive':
							CPQ_PList_Inactive.append(lst.ServiceProduct)
					for prod in PList:
						addRow = True
						if prod.PRODUCT_NAME == 'Enabled Services':
							if isES == 1 and isSESP == 1:
								addRow = False
						if addRow:
							row = cont.AddNewRow(prod.SYSTEM_ID, False)
							row['Module'] = prod.PRODUCT_NAME
							row['Product_Status'] = 'Incomplete'
							row.Product.Attr('SC_Product_Status').AssignValue("0")
							row['Type'] = 'Renewal'
							row.GetColumnByName('Type').ReferencingAttribute.AssignValue('Renewal')
							if isES == 1 and prod.PRODUCT_NAME == 'Enabled Services':
								populateComparisionSummary(row.Product, Contract_Number,CPQ_PList_Inactive, class_contact_modules, isES, EnabledServices_servprod)
							elif isES == 1 and prod.PRODUCT_NAME == 'Solution Enhancement Support Program':
								populateComparisionSummary(row.Product, Contract_Number,CPQ_PList_Inactive, class_contact_modules, isES, EnabledServices_servprod)
								populateComparisionSummary(row.Product, Contract_Number,CPQ_PList_Inactive, class_contact_modules, 0, '')
							elif row['Module'] == 'Generic Module':
								row.Product.Attr('SC_GN_AT_Product_Family').SelectDisplayValue(prod.Module_Name_GN,False)
								populateComparisionSummary(row.Product, Contract_Number,CPQ_PList_Inactive, class_contact_modules, 0, prod.Module_Name_GN)
							else:
								populateComparisionSummary(row.Product, Contract_Number,CPQ_PList_Inactive, class_contact_modules, 0, '')
							childProduct = row.Product
							row.Calculate()
							if isES == 1 and prod.PRODUCT_NAME == 'Enabled Services':
								GS_SC_OPB_ES_SESP_Module.setESAttr(childProduct, EnabledServices_servprod)
							elif prod.PRODUCT_NAME == 'Solution Enhancement Support Program':
								GS_SC_OPB_ES_SESP_Module.setSESPAttr(childProduct, SC_Service_Product, SC_Coverage, isES)
								if isES == 1 and isSESP == 1:
									GS_SC_OPB_ES_SESP_Module.setESAttr(childProduct, EnabledServices_servprod)
								budgetedQuota = 0
								res = class_contact_modules.get_Training_Match_Data(Contract_Number)
								if res["records"]:
									for rec in res["records"]:
										PYContractCurrency = str(rec['CurrencyIsoCode'])
										Ex_Rate = 1 / float(Quote.GetCustomField('SC_CF_PRVYR_EXCHANGE_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCHANGE_RATE').Content and PYContractCurrency != 'USD' and currentQuoteCurrency == 'USD' else Exchange_Rate
										budgetedQuota = (float(rec['Budgeted_Quota__c'])/2.0)*Ex_Rate
										break
								if budgetedQuota >0:
									contSP = childProduct.GetContainerByName("SC_Entitlements")
									if contSP.Rows.Count:
										for i in contSP.Rows:
											if i['Entitlement']=="Training Match":
												i.IsSelected = True
												trainingMatchValue = childProduct.Attr('SC_Training_Match_Contract_Value')
												trainingMatchValue.Allowed = True
												trainingMatchValue.Access = AttributeAccess.Editable
												trainingMatchValue.AssignValue(str(budgetedQuota))
												trainingMatchValuePer = childProduct.Attr('SC_Training_Match_Contract_Value_Percent')
												trainingMatchValuePer.Allowed = True
												trainingMatchValuePer.Access = AttributeAccess.ReadOnly
												UpdateComparisionSummary_SESP(row.Product, budgetedQuota)

							### Contract Extension Logic Starts ###
							if contractExtension == "True":
								if row['Module']  not in ('Workforce Excellence Program', 'Labor'):
									row.Product.Attributes.GetByName('SC_Pricing_Escalation').SelectValue('Yes')
								elif row['Module'] == "Workforce Excellence Program":
									for esc in ['SC_WEP_HIF_Pricing_Escalation','SC_WEP_IFS_Pricing_Escalation','SC_WEP_Halo_Pricing_Escalation','SC_WEP_Training_Pricing_Escalation','SC_WEP_TNA_Pricing_Escalation','SC_WEP_OM_Pricing_Escalation','SC_WEP_OCP_Pricing_Escalation']:
										row.Product.Attributes.GetByName(esc).SelectValue('Yes')
							### Contract Extension Logic Ends ###

							row.Product.ApplyRules()
							if row['Module'] == 'Generic Module':
								row['Product_Name'] = row.Product.Attr('SC_GN_AT_Product_Family').GetValue()
							else:
								row['Product_Name'] = row['Module']
					cont.Calculate()
					Delta_ProdLst = [lst for lst in Product_list if lst not in CPQ_PList]
					if len(Delta_ProdLst) != 0:
						Product.Attr('SC_OPB_Not_Available_Product_List').AssignValue("Invalid Service Products '" + ','.join(Delta_ProdLst) + "' Cannot configure renewal Quote.")
	cont.Calculate()

	if update_dict_gen:
		col_dict = {'Model':'Model_Number','Quantity':'PY_Quantity','Unit_Cost_Price':'PY_CostPrice','Unit_List_Price':'PY_ListPrice'}
		for data in Product.GetContainerByName('Service Contract Modules').Rows:
			if data['Module'] == 'Generic Module':
				gen_cont= data.Product.GetContainerByName('SC_GN_AT_Models_Scope_Cont')
				if gen_cont.Rows.Count == 0:
					for tp_up in update_dict_gen.values():
						if tp_up['ModuleName'] == data.Product.Attr('SC_GN_AT_Product_Family').GetValue():
							daata = gen_cont.AddNewRow(False)
							daata['PY_Quantity'] = tp_up['Quantity']
							daata['PY_CostPrice'] = str(float(tp_up['Unit_Cost_Price']) * float(tp_up['Quantity'])) if tp_up['Unit_Cost_Price'] and tp_up['Quantity'] else '0'
							daata['PY_ListPrice'] = str(float(tp_up['Unit_List_Price']) * float(tp_up['Quantity'])) if tp_up['Unit_List_Price'] and tp_up['Quantity'] else '0'
							daata['Service_Product'] = tp_up['Service_Product']
							daata['Model_Number'] = tp_up['Model']
							daata['Asset No'] = tp_up['Asset No']
							daata['Description'] = tp_up['Description']
							#daata['PY_CostPrice'] = tp_up['Unit_Cost_Price']
							#daata['PY_ListPrice'] = tp_up['Unit_List_Price']
							daata['Quantity'] = daata['Renewal_Quantity'] if daata['Renewal_Quantity'] not in (None,'') else '0'
							data.Product.ParseString("<*CTX( Container(SC_GN_AT_Models_Scope_Cont).Row({}).Column(Service_Product).Set({}) )*>".format(daata.RowIndex+1,tp_up['Service_Product']))
				gen_cont.Calculate()