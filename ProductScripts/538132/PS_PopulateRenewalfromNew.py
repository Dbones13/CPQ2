if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    import GS_GetPriceFromCPS
    Exchange_Rate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content else 1
    Invalid_cont = Product.GetContainerByName("SC_MES_Invalid_Models")
    Invalid_cont.Rows.Clear()
    Model_cont = Product.GetContainerByName("SC_MES_Models_Scope")
    m = []
    if Model_cont.Rows.Count:
        for row in Model_cont.Rows:
            row['PY_Quantity'] = row['Hidden_Quantity']
            row['PY_UnitPrice'] = str(float(row['Hidden_UnitPrice']) * Exchange_Rate) if row['Hidden_UnitPrice'] else '0'
            row['PY_ListPrice'] = str(float(row['Hidden_ListPrice']) * Exchange_Rate) if row['Hidden_ListPrice'] else '0'
            row['Renewal_Quantity'] = '0'
            row['BackupRenewalQuantity'] = '0'
            row['Difference'] = str(0 - int(row['Hidden_Quantity']))
            if int(row['Difference']) > 0:
                row['Comments'] = "Scope Addition"
            if int(row['Difference']) < 0:
                row['Comments'] = "Scope Reduction"
            if int(row['Difference']) == 0:
                row['Comments'] = "No Scope Change"
            priceDict = {}
            priceDict = GS_GetPriceFromCPS.getPrice(Quote,priceDict,[row['MES Models']],TagParserQuote,Session)
            if len(priceDict)>0:
                row["HW_UnitPrice"] = priceDict[row["MES Models"]]
                row["Hidden_UnitPrice"] = priceDict[row["MES Models"]]
            else:
                row["HW_UnitPrice"] = '0'
                row["Hidden_UnitPrice"] = '0'
            row['Hidden_Quantity'] = '0'
            row.Calculate()
        Model_cont.Calculate()
    Product.Attr('SC_ScopeRemoval').AssignValue('')
Product.Attr('SC_Renewal_check').AssignValue('1')