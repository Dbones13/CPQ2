prev_quote = Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content
active_contract = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
entitlementList = []
opt_ent_cont = Product.GetContainerByName('SC_MES_Optional_Entitlement')
serviceProduct = ""

if active_contract and prev_quote in ("None","") and Product.Attr('SC_Product_Type').GetValue() == "Renewal":

    from CPQ_SF_SC_Modules import CL_SC_Modules
    Contract_Number = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
    class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None,Session)
    resp = class_contact_modules.get_ContractRenewalLineItem_Data(Contract_Number)

    for record in resp["records"]:
        product_name = str(record["Service_Product_Name__c"])
        entitlement_name = str(record["Name"])
        entitlement_query = SqlHelper.GetFirst("Select ServiceProduct from CT_SC_ENTITLEMENTS_DATA where Module_Name = 'MES Performix' and ServiceProduct = '{}'".format(product_name))
        if entitlement_query is not None:
            entitlementList.append(entitlement_name)
            serviceProduct = product_name

    Product.Attr('SC_MES_Service_Product').SelectValue(serviceProduct)

    if opt_ent_cont.Rows.Count:
        for row in opt_ent_cont.Rows:
            if row["Entitlement"] in entitlementList:
                row.IsSelected = True

    Product.Attr('SC_OPB_Check_SP_Ent').AssignValue('1')