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
    
SC_Select_Optional_Entitlements = Product.GetContainerByName('SC_Select_Optional_Entitlements')
SC_Select_Optional_Entitlements.Rows.Clear()
SC_License_type = Product.Attr('SC_License_type').GetValue()


if SC_License_type == 'Term':
    if license_period < 5:
        Product.Attr('SC_License_period_Year').SelectValue(str(license_period))

    else:
        Product.Attr('SC_License_period_Year').SelectValue('5')
        
    entitlements_query = SqlHelper.GetList("select ServiceProduct,Entitlement from CT_SC_ENTITLEMENTS_DATA where ServiceProduct = 'Trace Subscription Service' and IsMandatory = 'FALSE'")
    if entitlements_query is not None:
        for row in entitlements_query:
            ent_row = SC_Select_Optional_Entitlements.AddNewRow(False)
            ent_row['Service_Product_Line_Item']  = row.ServiceProduct
            ent_row['Entitlement']  = row.Entitlement

elif SC_License_type == 'Perpetual':
    if license_period <= 3:
        Product.Attr('SC_Years_of_Support').AssignValue(str(license_period))
    else:
        Product.Attr('SC_Years_of_Support').AssignValue('3')
    entitlements_query = SqlHelper.GetList("select ServiceProduct,Entitlement from CT_SC_ENTITLEMENTS_DATA where ServiceProduct = 'Trace Software Support' and IsMandatory = 'FALSE'")
    if entitlements_query is not None:
        for row in entitlements_query:
            ent_row = SC_Select_Optional_Entitlements.AddNewRow(False)
            ent_row['Service_Product_Line_Item']  = row.ServiceProduct
            ent_row['Entitlement']  = row.Entitlement
ScriptExecutor.Execute('PS_Set_Summary_Entitlements')
Product.Attr('SC_Product_Status').AssignValue("0")