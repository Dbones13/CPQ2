product_family = Product.Attr('SC_GN_AT_Product_Family').GetValue()
service_prod = Product.GetContainerByName('SC_GN_AT_Service_Product_Cont')
opt_ent = Product.GetContainerByName('SC_GN_AT_Optional_Ent_Cont')
scope = Product.GetContainerByName('SC_GN_AT_Models_Scope_Cont')

listt = SqlHelper.GetList("select Distinct ServiceProduct,ISMULTISELALLOWED from CT_SC_ENTITLEMENTS_DATA where Module_Name = 'Generic Module' and Product_Type = '{}'".format(product_family))

service_prod.Clear()
opt_ent.Clear()
scope.Clear()

for row in listt:
	i = service_prod.AddNewRow()
	i['Service_Product'] = row.ServiceProduct