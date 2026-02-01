tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Scope Summary' in tabs and Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    models_scope_hif = Product.GetContainerByName("SC_WEP_Models_Scope_HIF")
    models_scope_ifs = Product.GetContainerByName("SC_WEP_Models_Scope_IFS")
    models_scope_halo = Product.GetContainerByName("SC_WEP_Models_Scope_Halo")
    models_scope_training = Product.GetContainerByName("SC_WEP_Models_Scope_Training")
    models_scope_config_training = Product.GetContainerByName("SC_WEP_Configurable_Models_Training")
    models_scope_tna = Product.GetContainerByName("SC_WEP_Models_Scope_TNA")
    system_selection_tna = Product.GetContainerByName("SC_WEP_System_Selection_TNA")
    subscription_price_om = Product.GetContainerByName("SC_WEP_Subscription_Price_OM")
    add_on_fees_om = Product.GetContainerByName("SC_WEP_Add_On_Fees_OM")
    conclusion_ocp = Product.GetContainerByName("SC_WEP_Conclusion_OCP")
    comparisonCont = Product.GetContainerByName('ComparisonSummary')

    listPrice_wep = 0
    listPrice_training = 0

    years = 1
    try:
        if Quote:
            contractDuration = Quote.GetCustomField("SC_CF_CONTRACTDURYR").Content
            contractYears = contractDuration.Split(" ")
            years = contractYears[0]
        if int(float(years)) == float(years):
            years = int(float(years))
        else:
            years = int(float(years)) + 1
    except:
        years = 1

    if models_scope_hif.Rows.Count:
        for row in models_scope_hif.Rows:
            listPrice_wep += float(row["PY_ListPrice"]) if row["PY_ListPrice"] != "" else 0
    if models_scope_ifs.Rows.Count:
        for row in models_scope_ifs.Rows:
            listPrice_wep += float(row["PY_ListPrice"]) if row["PY_ListPrice"] != "" else 0
    if models_scope_halo.Rows.Count:
        for row in models_scope_halo.Rows:
            listPrice_wep += float(row["PY_ListPrice"]) if row["PY_ListPrice"] != "" else 0
    if models_scope_tna.Rows.Count:
        for row in models_scope_tna.Rows:
            listPrice_wep += float(row["PY_ListPrice"]) if row["PY_ListPrice"] != "" else 0
    if system_selection_tna.Rows.Count:
        for row in system_selection_tna.Rows:
            listPrice_wep += float(row["PY_SystemPrice"]) if row["PY_SystemPrice"] != "" else 0
    if conclusion_ocp.Rows.Count:
        for row in conclusion_ocp.Rows:
            listPrice_wep += float(row["PY_Value"])/years if row["PY_Value"] != "" else 0

    if models_scope_training.Rows.Count:
        for row in models_scope_training.Rows:
            listPrice_training += float(row["PY_ListPrice"]) if row["PY_ListPrice"] != "" else 0
    if models_scope_config_training.Rows.Count:
        for row in models_scope_config_training.Rows:
            listPrice_training += float(row["PY_ListPrice"]) if row["PY_ListPrice"] != "" else 0
    if subscription_price_om.Rows.Count:
        for row in subscription_price_om.Rows:
            listPrice_training += float(row["PY_SubscriptionPrice"]) if row["PY_SubscriptionPrice"] != "" else 0
    if add_on_fees_om.Rows.Count:
        for row in add_on_fees_om.Rows:
            listPrice_training += float(row["PY_SubscriptionPrice"]) if row["PY_SubscriptionPrice"] != "" else 0

    if comparisonCont.Rows.Count:
        for row in comparisonCont.Rows:
            if row["Service_Product"] == "Workforce Excellence Program":
                if listPrice_wep > 0:
                    row["Configured_PY_List_Price"] = str(listPrice_wep)
                else:
                    row["Configured_PY_List_Price"] = row["PY_List_Price_SFDC"]
                row["Configured_PY_Sell_Price"] = str(float(row['Configured_PY_List_Price']) - (float(row['Configured_PY_List_Price']) * float(row['PY_Discount_SFDC']))) if row['PY_Discount_SFDC'] else str(float(row['Configured_PY_List_Price']))
            if row["Service_Product"] == "Training":
                if listPrice_training > 0:
                    row["Configured_PY_List_Price"] = str(listPrice_training)
                else:
                    row["Configured_PY_List_Price"] = row["PY_List_Price_SFDC"]
                row["Configured_PY_Sell_Price"] = str(float(row['Configured_PY_List_Price']) - (float(row['Configured_PY_List_Price']) * float(row['PY_Discount_SFDC']))) if row['PY_Discount_SFDC'] else str(float(row['Configured_PY_List_Price']))
            row.Calculate()