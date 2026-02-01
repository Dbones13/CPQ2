if Product.Attr("HCI_PHD_CEJ_Required").SelectedValue:
	ScriptExecutor.Execute("HCI_ProductAttr_Validation")
if Product.Attr("R2QRequest").SelectedValue.Display=="Yes" and Product.Attr("HCI_PHD_CEJ_Required").SelectedValue.Display == "Yes":
    Product.Attr("HCI_Insight_Users_NoEvents").SelectDisplayValue("No")
    Product.Attr("HCI_Insight_Users_WithEvents").SelectDisplayValue("Yes")