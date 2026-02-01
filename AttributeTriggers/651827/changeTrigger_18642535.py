Quote.GetCustomField('R2Q_Alternate_Execution_Country').Content = Product.Attr("R2Q_Alternate_Execution_Country").GetValue()
cont = Product.GetContainerByName('AR_HCI_SUBPRD')
if cont.Rows.Count>1:
	row=cont.Rows[1]
	row.Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').SelectValue(Quote.GetCustomField("R2Q_Alternate_Execution_Country").Content)