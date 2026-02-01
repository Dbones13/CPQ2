scope = Product.Attr('AR_HCI_SCOPE').GetValue()
if scope == "Software" and Product.GetContainerByName('AR_HCI_SUBPRD').Rows.Count==0:
	Product.Attr("Header_02_open").Access = AttributeAccess.Hidden
	Product.Attr("ATTCON_02_open").Access = AttributeAccess.Hidden
	Product.Attr("AR_HCI_GES Participation %").Access = AttributeAccess.Hidden
	Product.Attr("AR_HCI_GES Location").Access = AttributeAccess.Hidden
	Product.Attr("R2Q_Alternate_Execution_Country").Access = AttributeAccess.Hidden
	Product.Attr("ATTCON_02_close").Access = AttributeAccess.Hidden
	Product.Attr("Header_02_close").Access = AttributeAccess.Hidden
elif scope == "Software + Labor" and Product.GetContainerByName('AR_HCI_SUBPRD').Rows.Count==0:
	Product.Attr("Header_02_open").Access = AttributeAccess.Editable
	Product.Attr("ATTCON_02_open").Access = AttributeAccess.Editable
	Product.Attr("AR_HCI_GES Participation %").Access = AttributeAccess.Editable
	Product.Attr("AR_HCI_GES Location").Access = AttributeAccess.Editable
	Product.Attr("R2Q_Alternate_Execution_Country").Access = AttributeAccess.Editable
	Product.Attr("ATTCON_02_close").Access = AttributeAccess.Editable
	Product.Attr("Header_02_close").Access = AttributeAccess.Editable