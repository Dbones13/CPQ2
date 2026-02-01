Training_Match_Value = Product.Attr('SC_Training_Match_Contract_Value')
T = Product.Attr('SC_Training_Match_Contract_Value').GetValue()
if Training_Match_Value is not None:
    Product.Attr('SC_Training_Match_Contract_Value').AssignValue(T)
    Product.Attr('SC_Training_Match_Contract_Value_Percent').Access = AttributeAccess.ReadOnly