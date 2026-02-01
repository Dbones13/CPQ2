if Product.Attr("HCI_PHD_Product").SelectedValue:
	ScriptExecutor.Execute("HCI_ProductAttr_Validation")
	#Trace.Write("--->"+str(Product.Attr("HCI_PHD_OrderType").SelectedValue.Display))
	Trace.Write("R2Q bfr---"+str(Product.Attr('R2QRequest').GetValue()))
	if Product.Attr('R2QRequest').GetValue() == 'Yes':
		Trace.Write("inside R2Q")
		#Product.Attribute.GetByName("AR_R2Q_AddFmePrd").AssignValue("True")
		ScriptExecutor.ExecuteGlobal('R2Q_HCI_Attributepermission')