if Quote.GetCustomField('IsR2QRequest').Content:
	Product.Attr("R2QRequest").AssignValue("Yes")
	Product.Attr("Order_Status").AssignValue(str(Quote.OrderStatus.Name))
	Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
	Quote.GetCustomField('R2Q_Alternate_Execution_Country').Content = Product.Attr('R2Q_Alternate_Execution_Country').GetValue()
	Quote.GetCustomField('R2Q_PRJT_Execution_Year').Content = Product.Attr('Project_Execution_Year').GetValue()
	Product.Attr('R2Q_EGAP_Approval').AssignValue(str(Quote.GetCustomField('R2Q_Save').Content))
	def hide_column(container, Column):
		Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format(container, Column))
	hide_column('Cyber Configurations','Product Name')
	hide_column('Cyber Configurations','User_Define_Name')