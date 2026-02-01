quotetype = Quote.GetCustomField("Quote Type").Content
SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if quotetype == 'Contract Renewal' and SC_Product_Type == 'New':
    modelScopeCont = Product.GetContainerByName('SC_BGP_Models_Scope_Cont')
    scopeContHidden = Product.GetContainerByName('SC_BGP_Models_Cont_Hidden')
    scopeContHidden.Rows.Clear()

    if modelScopeCont.Rows.Count:
        for row in modelScopeCont.Rows:
            scopeContRowHidden = scopeContHidden.AddNewRow(False)
            scopeContRowHidden['Service_Product'] = row['Service_Product']
            scopeContRowHidden['Asset_No'] = row['Asset No']
            scopeContRowHidden['Model_Number'] = row['Model_Number']
            scopeContRowHidden['Description'] = row['Description']
            scopeContRowHidden['Renewal_Quantity'] = row['Quantity']
            scopeContRowHidden['List_Price'] = row['Unit_List_Price']
            scopeContRowHidden['Cost_Price'] = row['Unit_Cost_Price']
        scopeContHidden.Calculate()