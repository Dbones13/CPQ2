#GS_SC_OPB_ES_SESP_Module
def getServiceProducts():
	#Fetch distinct service products of the ES and SESP modules
	res = SqlHelper.GetList("select distinct ServiceProduct, Product_Type from CT_SC_ENTITLEMENTS_DATA where Module_Name  in ('Solution Enhancement Support Program', 'Enabled Services') and Product_Type	in	('SESP', 'ES')")
	serviceProductES = set()
	serviceProductSESP = set()
	for row in res:
		if row.Product_Type == 'ES':
			serviceProductES.add(row.ServiceProduct)
		elif row.Product_Type == 'SESP':
			serviceProductSESP.add(row.ServiceProduct)
	return serviceProductES, serviceProductSESP

def setESAttr(Product, EnabledServices_servprod):
	#Set Service product from SFDC
	Product.Attributes.GetByName('EnabledServices_servprod').SelectDisplayValue(EnabledServices_servprod)
	#Remove New option from the Order Type Dropdown
	attrOrderType = Product.Attr('OrderType_EnabledService')
	for val in attrOrderType.Values:
		if val.ValueCode != "Renewal":
			val.Allowed = False
	attrOrderType.SelectDisplayValue('Renewal', False)
	#Previous Year Asset Information
	cont = Product.GetContainerByName('ES_PY_Asset_Details')
	cont.Rows.Clear()
	row = cont.AddNewRow(False)
	for col in row.Columns:
		if col.Name != 'MSID':
			row[col.Name] = '0'
	#Asset Summary - make previous year columns are editable
	cont = Product.GetContainerByName('ES_Asset_Summary')
	cont.Rows.Clear()
	row = cont.AddNewRow(False)
	for col in row.Columns:
		if col.Name in ['No_MSID_PY', 'PY_List_Price']:
			col.DisplayType = 'TextBox'

def getConfiguredServiceProducts(Product_list, serviceProductES, serviceProductSESP):
	EnabledServices_servprod = ''
	SC_Service_Product = ''
	isES = 0
	isSESP = 0
	SC_Coverage = '8X5'
	for prod in Product_list:
		if prod in serviceProductES:
			isES = 1
			EnabledServices_servprod = prod
		elif prod in serviceProductSESP:
			isSESP = 1
			SC_Service_Product = prod
		if isES == 1 and isSESP == 1:
			break
	return isES, isSESP, EnabledServices_servprod, SC_Service_Product, SC_Coverage

def setSESPAttr(Product, SC_Service_Product, SC_Coverage, isES):
	#Select the Enabled Services Checkbox
	if isES:
		values = Product.Attr('EnableSelection_SESP').Values
		for v in values:
			v.IsSelected = True
	Product.Attributes.GetByName('SC_Service_Product').SelectDisplayValue(SC_Service_Product)
	Product.Attr('SC_Coverage').SelectDisplayValue(SC_Coverage, False)