if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    Product.Attr('SC_P1P2_PartsUsageMethod').Access = AttributeAccess.Editable
    Product.Attr('SC_Renewal_check').AssignValue('2')