quotetype = Quote.GetCustomField("Quote Type").Content
SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if quotetype == 'Contract Renewal' and SC_Product_Type == 'New':
    modelScopeCont = Product.GetContainerByName('SC_GN_AT_Models_Scope_Cont')
    scopeContHidden = Product.GetContainerByName('SC_GN_AT_Models_Cont_Hidden')
    scopeContHidden.Rows.Clear()

    if modelScopeCont.Rows.Count:
        for row in modelScopeCont.Rows:
            scopeContRowHidden = scopeContHidden.AddNewRow(False)
            scopeContRowHidden['Service_Product'] = row['Service_Product']
            scopeContRowHidden['Asset'] = row['Asset No']
            Trace.Write("AssetNo" + row['Asset No'])
            scopeContRowHidden['Model'] = row['Model']
            scopeContRowHidden['Description'] = row['Description']
            scopeContRowHidden['Renewal_Quantity'] = row['Quantity']
            scopeContRowHidden['List_Price'] = row['Unit_List_Price']
            scopeContRowHidden['Cost_Price'] = row['Unit_Cost_Price']
            Log.Info("RP Renewal Script executed")
        scopeContHidden.Calculate()
Product.ApplyRules()