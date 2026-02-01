'''load  Model Entitlement container i.e. SC_Entitlements_Model'''
Ent_Model = Product.GetContainerByName('SC_Entitlements_Model')
Ent_Scope =  Product.GetContainerByName('SC_Entitlements')
Ent_Model.Clear()
Service = Product.Attr('SC_Honeywell_Digital_Prime').GetValue()
a = SqlHelper.GetList("select Entitlement,IsMandatory from CT_SC_ENTITLEMENTS_DATA where IsMandatory = 'TRUE' and ServiceProduct = '{}'".format(Service))
for row in a:
    i = Ent_Model.AddNewRow()
    i['Entitlement'] = row.Entitlement
    i['Type'] = 'Mandatory'

for row1 in  Ent_Scope.Rows:
    if row1.IsSelected == True:
        i = Ent_Model.AddNewRow()
        i['Entitlement'] = row1['Entitlement']
        i['Type'] = 'Optional'
Ent_Model.Calculate()
#Change product status as incomplete
#Product.Attr('SC_Product_Status').AssignValue("0")