prev_quote = Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content
active_contract = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
SPList = []
opt_ent_cont = Product.GetContainerByName('SC_BGP_Optional_Ent_Cont')
serviceProduct = ""

if Product.Attr('SC_Product_Type').GetValue() == "Renewal":

    from CPQ_SF_SC_Modules import CL_SC_Modules
    Contract_Number = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
    class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None,Session)
    resp = class_contact_modules.get_ContractRenewalLineItem_Data(Contract_Number)

    for record in resp["records"]:
        product_name = str(record["Service_Product_Name__c"])
        entitlement_name = str(record["Name"])
        entitlement_query = SqlHelper.GetFirst("Select ServiceProduct,Entitlement,IsMandatory from CT_SC_ENTITLEMENTS_DATA where Product_Type = 'BGP' and ServiceProduct = '{}'".format(product_name))
        if entitlement_query is not None:
            SPList.append(product_name)
            serviceProduct = product_name
            Product.Attr('SC_BGP_Serv_Product').SelectValues(*SPList)
            if entitlement_name in entitlement_query.Entitlement and entitlement_query.IsMandatory == 'FALSE':
                if opt_ent_cont.Rows.Count:
                    for Erow in opt_ent_cont.Rows:
                        if Erow['Service_Product'] in entitlement_query.ServiceProduct and Erow['Optional_Entitlement'] in entitlement_query.Entitlement:
                            Erow.IsSelected = True
                else:
                    ent_row = opt_ent_cont.AddNewRow(False)
                    ent_row['Service_Product'] = entitlement_query.ServiceProduct
                    ent_row['Optional_Entitlement'] = entitlement_query.Entitlement
                    ent_row.IsSelected = True
                opt_ent_cont.Calculate()
    Product.Attr('SC_OPB_Check_SP_Ent').AssignValue('1')