Product.Attr('SC_Labor_Admin_Fee').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Labor_Block_Discount').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Labor_Country_Labor_AOP').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Labor_Honeywell_List_Price').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Labor_Customer_List_Price').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Labor_Burden_for_Hr_Day').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Labor_Hrs_per_Full_Day').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Labor_PY_Deliverables_Hours').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Labor_Block_Discount').AssignValue(TagParserProduct.ParseString('<*XValue(../SC_OverAll_Labor_Block_Discount)*>'))
if (Product.Attr('SC_Labor_Resource_Type').SelectedValue.ValueCode if Product.Attr('SC_Labor_Resource_Type').SelectedValue != None else '') in ("A360 Contract Management","Service Contract Management"):
	Product.Attr('SC_Labor_Burden_for_Hr_Day').Access = AttributeAccess.Editable
	Product.Attr('SC_Labor_Honeywell_List_Price').Access = AttributeAccess.Editable
	Product.Attr('SC_Labor_PY_Deliverables_Hours').Access = AttributeAccess.Editable