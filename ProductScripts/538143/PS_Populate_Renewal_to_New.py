quotetype = Quote.GetCustomField("Quote Type").Content
SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if quotetype == 'Contract Renewal' and SC_Product_Type == 'New':
    modelScopeCont = Product.GetContainerByName('SC_Experion_Models_Scope')
    scopeContHidden = Product.GetContainerByName('SC_Experion_Models_Hidden')
    scopeContHidden.Rows.Clear()

    if modelScopeCont.Rows.Count:
        for row in modelScopeCont.Rows:
            scopeContRowHidden = scopeContHidden.AddNewRow(False)
            scopeContRowHidden['MSIDs'] = row['MSIDs']
            scopeContRowHidden['Description'] = row['Description']
            scopeContRowHidden['Quantity'] = row['Quantity']
            scopeContRowHidden['List_Price'] = row['List_Price']
            scopeContRowHidden['Cost_Price'] = row['Cost_Price']
            scopeContRowHidden['Comment'] = row['Comment']
        scopeContHidden.Calculate()