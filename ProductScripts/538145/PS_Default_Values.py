license_period = 1
if Quote:
    contract_duration = Quote.GetCustomField('SC_CF_CONTRACTDURYR').Content
    if contract_duration != "":
        contract_duration = contract_duration.split()
        if int(eval(contract_duration[0])) < float(contract_duration[0]):
            contract_duration[0] = int(eval(contract_duration[0])) + 1
        else:
            contract_duration[0] = int(eval(contract_duration[0]))
        license_period = contract_duration[0]
        if license_period <= 3:
            Product.Attr('SC_Years_of_Support').AssignValue(str(license_period))
        else:
            Product.Attr('SC_Years_of_Support').AssignValue('3')
            
    Product.Attr('SC_Disallowed_Values').AssignValue(str(license_period))

SC_Select_Optional_Entitlements = Product.GetContainerByName('SC_Select_Optional_Entitlements')
SC_Select_Optional_Entitlements.Rows.Clear()
entitlements_query = SqlHelper.GetList("select ServiceProduct,Entitlement from CT_SC_ENTITLEMENTS_DATA where ServiceProduct = 'Trace Software Support' and IsMandatory = 'FALSE'")

if entitlements_query is not None:
    for row in entitlements_query:
        ent_row = SC_Select_Optional_Entitlements.AddNewRow(False)
        ent_row['Service_Product_Line_Item']  = row.ServiceProduct
        ent_row['Entitlement']  = row.Entitlement