from GS_MigrationUtil import VSAddRow
isR2QRequest=Quote.GetCustomField("isR2QRequest").Content
VSAddRow(Product,6,isR2QRequest)