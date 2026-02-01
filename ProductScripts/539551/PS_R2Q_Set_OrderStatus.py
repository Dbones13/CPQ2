if Quote.GetCustomField("isR2QRequest").Content == 'Yes':
	Product.Attr("Order_Status").AssignValue(str(Quote.OrderStatus.Name))
	#Product.Attr("R2Q_EGAP_Approval").AssignValue(str(Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content))
	Product.Attr('R2Q_EGAP_Approval').AssignValue(str(Quote.GetCustomField('R2Q_Save').Content))
	Quote.SetGlobal('checkproduct', 'Migration')
	Quote.GetCustomField("R2Q_PRJT_Execution_Year").Content = Product.Attr('Project_Execution_Year').GetValue()