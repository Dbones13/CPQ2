prev_quote = Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content
active_contract = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
if active_contract and prev_quote in ("None","") and Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    Product.Attr('SC_License_type_PY').AssignValue('Perpetual')
    entitlementList = []
    opt_ent_cont = Product.GetContainerByName('SC_Select_Optional_Entitlements')
    serviceProduct = ""
    from CPQ_SF_SC_Modules import CL_SC_Modules
    Contract_Number = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
    class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None,Session)
    resp = class_contact_modules.get_ContractRenewalLineItem_Data(Contract_Number)

    for record in resp["records"]:
        product_name = str(record["Service_Product_Name__c"])
        entitlement_name = str(record["Name"])
        entitlement_query = SqlHelper.GetFirst("Select ServiceProduct from CT_SC_ENTITLEMENTS_DATA where Module_Name = 'Trace' and ServiceProduct = '{}'".format(product_name))
        if entitlement_query is not None:
            entitlementList.append(entitlement_name)
            serviceProduct = product_name


    if opt_ent_cont.Rows.Count:
        for row in opt_ent_cont.Rows:
            if row["Entitlement"] in entitlementList:
                row.IsSelected = True

    Product.Attr('SC_OPB_Check_SP_Ent').AssignValue('1')