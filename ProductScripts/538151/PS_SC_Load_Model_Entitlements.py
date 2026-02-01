currentTab = "".join([tab.Name for tab in Product.Tabs if tab.IsSelected])
if currentTab == 'Scope Selection':
	# Training Match visibility code:
	container_Entitlements = Product.GetContainerByName("SC_Entitlements")
	if container_Entitlements is not None:
		for row in container_Entitlements.Rows:
			if row['Entitlement'] == 'Training Match':
				if row.IsSelected:
					Product.Attr('SC_Training_Match_Contract_Value').Allowed = True
					Product.Attr('SC_Training_Match_Contract_Value_Percent').Allowed = True
				else:
					Product.Attr('SC_Training_Match_Contract_Value').Allowed = False
					Product.Attr('SC_Training_Match_Contract_Value_Percent').Allowed = False
				break
	if container_Entitlements and container_Entitlements.Rows.Count == 0:
		Product.Attr('SC_Training_Match_Contract_Value').Allowed = False
		Product.Attr('SC_Training_Match_Contract_Value_Percent').Allowed = False
	#container_Entitlements.Calculate()
elif currentTab == 'Scope Summary':
	#to load  Model Entitlement container
	Coverage = Product.Attr('SC_Coverage').GetValue()
	Product.Attr('SC_Coverage_Model').AssignValue(Coverage)
	Service = Product.Attr('SC_Service_Product').GetValue()
	Product.Attr('SC_Service_Product_Model').AssignValue(Service)
	Ent_Model = Product.GetContainerByName('SC_Entitlements_Model')
	Ent_Scope =	 Product.GetContainerByName('SC_Entitlements')
	Ent_Model.Clear()
	Service = Product.Attr('SC_Service_Product_Model').GetValue()
	a = SqlHelper.GetList("select distinct Entitlement,IsMandatory,ServiceProduct,Asset_Level from CT_SC_ENTITLEMENTS_DATA where IsMandatory = 'TRUE' and ServiceProduct = '{}'".format(Service))
	for row in a:
		i = Ent_Model.AddNewRow(False)
		i['Entitlement'] = row.Entitlement
		i['ServiceProduct'] = str(row.ServiceProduct)
		i['ProductLevel'] = str(row.Asset_Level)
		i['Type'] = 'Mandatory'

	for row1 in	 Ent_Scope.Rows:
		if row1.IsSelected == True:
			i = Ent_Model.AddNewRow(False)
			i['Entitlement'] = row1['Entitlement']
			i['ServiceProduct'] = row1['ServiceProduct']
			i['ProductLevel'] = row1['ProductLevel']
			i['Type'] = 'Optional'
	#Ent_Model.Calculate()