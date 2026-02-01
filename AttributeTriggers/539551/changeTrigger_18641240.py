if Quote.GetCustomField('IsR2QRequest').Content == "Yes":
	Quote.GetCustomField("R2Q_PRJT_Execution_Year").Content = Product.Attr('Project_Execution_Year').GetValue()