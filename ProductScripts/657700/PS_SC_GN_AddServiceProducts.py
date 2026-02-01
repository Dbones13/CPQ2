#SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
#if SC_Product_Type == 'New':
Ent_Model = Product.GetContainerByName('SC_GN_AT_Product_Entitlement_Cont')
Opt_Ent = Product.GetContainerByName('SC_GN_AT_Optional_Ent_Cont')
product_family = Product.Attr('SC_GN_AT_Product_Family').GetValue()
ServiceProd = Product.GetContainerByName('SC_GN_AT_Service_Product_Cont') 

S = []

Ent_Model.Clear()

a = SqlHelper.GetList("select ServiceProduct from CT_SC_ENTITLEMENTS_DATA where Status = 'Active' and Product_Type = '{}'".format(product_family))
for row in a:
	i = Ent_Model.AddNewRow()
	for SP_row in ServiceProd.Rows:
		S.append(str((row.ServiceProduct)))