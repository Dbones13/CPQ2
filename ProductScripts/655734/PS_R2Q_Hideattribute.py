R2QQuote = Quote.GetCustomField('isR2QRequest').Content
Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if Checkproduct != "PRJT R2Q":
    Quote.GetCustomField('isR2QRequest').Content = ""
if R2QQuote:
	Product.Attr('Calculation_Button').Allowed = False
	Product.Attr('Terminal_Experion_Server_(ESV)_Type').Access = AttributeAccess.Hidden
	Product.Attr('Terminal_Experion_Server_(ESV)_Type').SelectDisplayValue('Desk')
	for attr_name in ("Terminal_Media_kit_required", "Terminal_TM_Test_System_required?"):
		Product.Attr(attr_name).Access = AttributeAccess.Hidden