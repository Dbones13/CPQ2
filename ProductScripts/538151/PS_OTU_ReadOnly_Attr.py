currentTab = arg.NameOfCurrentTab
SESP_Training_Match_Flag = Product.Attr('SESP_Training_Match_Flag').GetValue()
if currentTab == 'OTU':
	Product.Attr("Service_Product_OTU_SESP").Access = AttributeAccess.ReadOnly
	Product.Attr("Entitlement_OTU_SESP").Access = AttributeAccess.ReadOnly
	Product.Attr("Contract_OTU_SESP").Access = AttributeAccess.ReadOnly
if currentTab == 'Scope Summary' and SESP_Training_Match_Flag == "1":
	Product.Attr("SC_Training_Match_Contract_Value_SS").Access = AttributeAccess.ReadOnly