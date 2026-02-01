from GS_CommonConfig import CL_CommonSettings as CS
for container in ('CCC_Valid_Parts','CCC_WriteInValid_Parts'):
    validPartsCon = Product.GetContainerByName(container)
    if validPartsCon.Rows.Count > 0:
        for row in validPartsCon.Rows:
            CS.setBeforeQuoteItems[row.UniqueIdentifier] = str(row["Quantity"])+'~'+str(row["Description"].strip().encode('unicode_escape'))+'~'+str(row["Unit Sell Price"])+'~'+str(row["Unit Cost"])+'~'+str(row["Unit List Price"])+'~'+str(row["PROJECT PRICE ADJUSTMENT"])+'~'+str(row["FRAME DISCOUNT"])+'~'+str(row["SERVICE DISCOUNT"])+'~'+str(row["REGIONAL DISCOUNT"])+'~'+str(row["BUSINESS DISCOUNT"])+'~'+str(row["APPLICATION DISCOUNT"])+'~'+str(row["DEFECT DISCOUNT"])+'~'+str(row["COMPETITIVE DISCOUNT"])+'~'+str(row["TOTAL DISCOUNT"])+'~'+str(row["Solution"])+'~'+str(row["Package"])+'~'+str(row["Flag"])