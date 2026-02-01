#prev_quote = Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content
active_contract = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]

if active_contract and Product.Attr('SC_Product_Type').GetValue() == "Renewal" and 'Scope Summary' in tabs:
    sp_ent_cont = Product.GetContainerByName('SC_WEP_ServiceProduct_Entitlement')
    entitlement_Cont = Product.GetContainerByName("SC_WEP_Offering_Entitlement")
    sp_Ent = {}
    error_string = ""

    for row in sp_ent_cont.Rows:
        sp_Ent.setdefault(row["Service_Product"],[]).append(row["Entitlement"])

    for row in entitlement_Cont.Rows:
        for key in sp_Ent.Keys:
            if row["Service_Product"] == key and row["Entitlements"] in sp_Ent[key]:
                sp_Ent[key].remove(row["Entitlements"])
                if len(sp_Ent[key]) == 0:
                    sp_Ent.pop(key)
                break
    Trace.Write(str(sp_Ent))
    if len(sp_Ent):
        for key in sp_Ent.Keys:
            err = "Entitlements need to be selected for " + key + " : "
            for value in sp_Ent[key]:
                err += value + " ,"
            err = err[:-1] + "<br>"
            error_string += err
    Product.Attr("Error_Message").AssignValue(error_string)