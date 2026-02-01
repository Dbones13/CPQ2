if Product.Attr('VS_No_Of_WorkLoad').GetValue() == '6':
	from GS_MigrationUtil import VSAddRow
	VSAddRow(Product,6)