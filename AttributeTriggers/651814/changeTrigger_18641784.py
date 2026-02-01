#Trace.Write("--->"+str(Product.Attr("HCI_PHD_OrderType").SelectedValue.Display))
prod = Product.Attr("HCI_PHD_Product").SelectedValue.Display
if prod in ("PHD & Insight","PHD & Insight & AFM","Process History Database (PHD)") and Product.Attr("HCI_PHD_OrderType").SelectedValue and Product.Attr("HCI_PHD_OrderType").SelectedValue.Display == "Maintenance Support Upgrade/Update (No Charge/ BGP Active)":
	Product.Attr("HCI_PHD_Non_Production_QA").Access = AttributeAccess.Editable
else:
	Product.Attr("HCI_PHD_Non_Production_QA").Access = AttributeAccess.Hidden
	Product.Attr("HCI_PHD_ExistingLicense_Non_Production_QA").Access = AttributeAccess.Hidden