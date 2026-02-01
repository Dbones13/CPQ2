from GS_MigrationUtil import VSAddRow
isR2QRequest=Quote.GetCustomField("isR2QRequest").Content
VSAddRow(Product,int(Product.Attr('VS_No_Of_WorkLoad').GetValue()),isR2QRequest)