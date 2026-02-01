#Product.Attr('QuoteType_Check').AssignValue(Quote.GetCustomField("Quote Type").Content)
reference_number=Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content
if Product.Attr('SC_Product_Type').GetValue() is not None and Product.Attr('SC_Product_Type').GetValue() != 'Renewal':
	if Product.Name == 'Enabled Services Model':
		Product.Attr('SC_HWOS_Service_Product').AssignValue('Enabled Services Model')
		if Quote:
			duration =DateTime.Parse(Quote.GetCustomField('EGAP_Contract_End_Date').Content).Subtract(DateTime.Parse(Quote.GetCustomField('EGAP_Contract_Start_Date').Content)).Days / 365
			Product.Attr('DurationOfPlan_enabledServices').AssignValue(str(duration))
			Product.Attr('ContractStartDate_EnabledService').AssignValue(Quote.GetCustomField('EGAP_Contract_Start_Date').Content)
			Product.Attr('ContractEndDate_EnabledService').AssignValue(Quote.GetCustomField('EGAP_Contract_End_Date').Content)
			con = Product.GetContainerByName('SC_SESP_MultiSites')
			"""for i in range(1,4):
				row = con.AddNewRow(False)
				row['Sites'] = 'Site '+str(i)
			else :
				con.Calculate()"""
	if Product.Name == 'Trace':
		Product.Attr('SC_HWOS_Service_Product').AssignValue('Trace')
		Product.Attr('SC_HWOS_Service_Product_ScopeSummary').AssignValue('Trace')
		setDefaultValues = SqlHelper.GetList("select ServiceProduct, Entitlement from CT_SC_ENTITLEMENTS_DATA where Product_Type = '{}'".format('Trace'))
		con = Product.GetContainerByName('HWOS_Entitlement')
		for i in setDefaultValues:
			n = con.AddNewRow(False)
			n['Service Product'] = i.ServiceProduct
			n['Entitlement'] = i.Entitlement
		else :
			con.Calculate()
	elif Product.Name == 'Third Party':
		Product.Attr('SC_HWOS_Service_Product').AssignValue('Third Party Services')
		Product.Attr('SC_HWOS_Service_Product_ScopeSummary').AssignValue('Third Party Services')
		setDefaultValues = SqlHelper.GetList("select ServiceProduct, Entitlement from CT_SC_ENTITLEMENTS_DATA where Product_Type = '{}'".format('3rd Party'))
		con = Product.GetContainerByName('HWOS_Entitlement')
		for i in setDefaultValues:
			n = con.AddNewRow(False)
			n['Entitlement'] = i.Entitlement
		else :
			con.Calculate()
	elif Product.Name == 'Hardware Refresh':
		Product.Attr('SC_ItemEditFlag').AssignValue('Hidden')
		Product.Attr('SC_HWOS_Service_Product').AssignValue('Hardware Refresh')
		Product.Attr('SC_HWOS_Service_Product_ScopeSummary').AssignValue('Hardware Refresh')
		Product.Attr('SC_HWOS_Service_Product').Access = AttributeAccess.ReadOnly
		Product.DisallowAttr('HWOS_Invalid_Model Scope_3party')
		Product.DisallowAttr('Invalid_Third_Party_Delete')
		setDefaultValues = SqlHelper.GetList("select ServiceProduct, Entitlement from CT_SC_ENTITLEMENTS_DATA where IsMandatory = 'FALSE' and ServiceProduct = '{}'".format('Hardware Refresh'))
		con = Product.GetContainerByName('HWOS_Entitlement')
		for i in setDefaultValues:
			n = con.AddNewRow(False)
			n['Service Product'] = i.ServiceProduct
			n['Entitlement'] = i.Entitlement
			n.IsSelected = False
		else:
			con.Calculate()
		
	elif Product.Name == 'Workforce Excellence Program':
		Product.Attr('SC_HWOS_Service_Product').AssignValue('Workforce Excellence Program')
		Product.Attr('SC_HWOS_Service_Product_ScopeSummary').AssignValue('Workforce Excellence Program')
		setDefaultValues = SqlHelper.GetList("select ServiceProduct, Entitlement from CT_SC_ENTITLEMENTS_DATA where ServiceProduct = '{}'".format('Workforce Excellence Program'))
		con = Product.GetContainerByName('HWOS_Entitlement')
		for i in setDefaultValues:
			n = con.AddNewRow(False)
			n['Service Product'] = i.ServiceProduct
			n['Entitlement'] = i.Entitlement
		else :
			con.Calculate()
	elif Product.Name == 'Hardware Warranty':
		Product.Attr('SC_ItemEditFlag').AssignValue('Hidden')
		Product.Attr('SC_HWOS_Service_Product').AssignValue('Hardware Warranty')
		Product.Attr('SC_HWOS_Service_Product').Access = AttributeAccess.ReadOnly
		Product.Attr('SC_HWOS_Service_Product_ScopeSummary').AssignValue('Hardware Warranty')
		Product.DisallowAttr('HWOS_Invalid_Model Scope_3party')
		Product.DisallowAttr('Invalid_Third_Party_Delete')
		setDefaultValues = SqlHelper.GetList("select ServiceProduct, Entitlement from CT_SC_ENTITLEMENTS_DATA where  ServiceProduct = '{}' and IsMandatory = 'False'".format('Hardware Warranty'))
		con = Product.GetContainerByName('HWOS_Entitlement')
		for i in setDefaultValues:
			n = con.AddNewRow(False)
			n['Service Product'] = i.ServiceProduct
			n['Entitlement'] = i.Entitlement
			n.IsSelected = False
		else:
			con.Calculate()
		#Product.DisallowAttr('HWOS_Entitlement')
	############
	if Product.Name == 'Hardware Warranty':
		setDefaultValues = SqlHelper.GetList("select ServiceProduct, Entitlement from CT_SC_ENTITLEMENTS_DATA where IsMandatory = 'True' and ServiceProduct = '{}'".format('Hardware Warranty'))
		o = Product.GetContainerByName('HWOS_Entitlement_Optional')
		o.Rows.Clear()
		e = Product.GetContainerByName('HWOS_Entitlement')
		for i in setDefaultValues:
			row = o.AddNewRow(False)
			row['Include'] = 'Mandatory'
			row['Entitlement'] = i.Entitlement
		else:
			o.Calculate()
		for i in e.Rows:
			if i.IsSelected:
				row = o.AddNewRow(False)
				row['Include'] = 'Optional'
				row['Entitlement'] = i['Entitlement']
		else:
			o.Calculate()
	elif Product.Name == 'Training':
		Product.Attr('SC_HWOS_Service_Product').AssignValue('Training')
		Product.Attr('SC_HWOS_Service_Product_ScopeSummary').AssignValue('Training')
		setDefaultValues = SqlHelper.GetList("select Entitlement from CT_SC_ENTITLEMENTS_DATA where ServiceProduct = '{}'".format('Training'))
		con = Product.GetContainerByName('HWOS_Entitlement')
		for i in setDefaultValues:
			n = con.AddNewRow(False)
			#n['Service Product'] = i.ServiceProduct
			n['Entitlement'] = i.Entitlement
		else :
			con.Calculate()
#The below code is only for renewal will add condition later
def get_entitlements(service_prod):
	setDefaultValues = SqlHelper.GetList("select ServiceProduct, Entitlement from CT_SC_ENTITLEMENTS_DATA where IsMandatory = 'FALSE' and ServiceProduct = N'{}'".format(str(service_prod)))
	return setDefaultValues
selScopeCont = Product.GetContainerByName('SC_SelectionSS_HR_RWL')
rowList = ["Scope Addition","Scope Reduction","No Scope Change"]
if selScopeCont.Rows.Count < 1:
    for row in rowList:
        selScopeRow = selScopeCont.AddNewRow(False)
        selScopeRow["Scope"] = row
        selScopeRow.IsSelected = True
if Product.Attr('SC_Product_Type').GetValue() is not None and Product.Attr('SC_Product_Type').GetValue() == 'Renewal' and reference_number !='':
	query = SqlHelper.GetFirst("Select Product,ProductDetails from SC_RENEWAL_TABLE where Product = '{}' and QuoteID = '{}'".format(Product.Name,reference_number))
	if query:
		var = eval(query.ProductDetails)
		for attr in var:
			if attr["Name"] == "HWOS_Model Scope_3party":
				con = i.Product.GetContainerByName("SC_ValidModels_HR_RWL")
				if not con.Rows.Count > 0:
					for oldVModelRecord in attr["Value"]:
						row = con.AddNewRow(False)
						row["SC_Model_HR_RWL"] = oldVModelRecord["3rd Party Model"]
						row["SC_Description_HR_RWL"] = oldVModelRecord["Description"]
						row["SC_Quantity_HR_RWL"] = oldVModelRecord["Quantity"]
						row["SC_PreviousYearUnitPrice_HR_RWL"] = oldVModelRecord["Unit List Price"]
						row["SC_PreviousYearListPrice_HR_RWL"] = oldVModelRecord["List Price"]
						row["SC_RenewalQuantity_HR_RWL"] = '0'
						row["SC_Comment_HR_RWL"] = "Scope Reduction"
						row["Select"] = oldVModelRecord["Select"]
			elif attr["Name"] == "SC_HWOS_Service_Product":
				i.Product.Attr("SC_ServiceProduct_HR_RWL").AssignValue(str(attr["Value"]))
				i.Product.Attr("SC_ServiceProduct_HR_RWL").Access = AttributeAccess.ReadOnly
		else:
			setDefaultValues = get_entitlements(Product.Name)
			con = i.Product.GetContainerByName('SC_Entitlements_HR_RWL')
			for i in setDefaultValues:
				n = con.AddNewRow(False)
				n['SC_Entitlement_HR_RWL'] = i.Entitlement
				n.IsSelected = False
			else:
				con.Calculate()