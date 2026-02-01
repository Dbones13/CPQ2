if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    modelScopeCont = Product.GetContainerByName('SC_MES_Models_Scope')
    comparisonCont = Product.GetContainerByName('ComparisonSummary')
    sp = Product.Attr('SC_MES_ServiceProduct').GetValue()
    listPrice = 0

    if modelScopeCont.Rows.Count:
        for row in modelScopeCont.Rows:
            listPrice += float(row["PY_ListPrice"]) if row["PY_ListPrice"] != "" else 0


    if comparisonCont.Rows.Count:
        for row in comparisonCont.Rows:
            if row["Service_Product"] == sp:
                if modelScopeCont.Rows.Count:
                    row["Configured_PY_List_Price"] = str(listPrice)
                else:
                    row["Configured_PY_List_Price"] = row["PY_List_Price_SFDC"]
                row["Configured_PY_Sell_Price"] = str(float(row['Configured_PY_List_Price']) - (float(row['Configured_PY_List_Price']) * float(row['PY_Discount_SFDC']))) if row['PY_Discount_SFDC'] else str(float(row['Configured_PY_List_Price']))
            else:
                row.IsSelected = True
                row["Configured_PY_List_Price"] = '0'
                row["Configured_PY_Sell_Price"] = '0'
            row.Calculate()