Product.Attr('SC_P1P2_ServiceProduct').Access = AttributeAccess.ReadOnly
Product.Attr('SC_P1P2_Entitlement').Access = AttributeAccess.ReadOnly
Product.Attr('SC_P1P2_ListPrice').Access = AttributeAccess.ReadOnly
Product.Attr('SC_Parts_Replacement_Pricing_Escalation').SelectValue("No")
Product.Attr('SC_Parts_Replacement_Pricing_Escalation').Access = AttributeAccess.ReadOnly
Product.Attr('SC_P1P2_PY_ListPrice').Access = AttributeAccess.ReadOnly
Product.Attr('SC_P1P2_LPDA_CY_FinalListPrice').Access = AttributeAccess.ReadOnly
Product.Attr('SC_P1P2_LTYA_CY_FinalListPrice').Access = AttributeAccess.ReadOnly
if Product.Attr('SC_Renewal_check').GetValue() == "0":
    Product.Attr('SC_P1P2_PartsUsageMethod').Access = AttributeAccess.ReadOnly