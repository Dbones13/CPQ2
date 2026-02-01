Training_Match_Value = Product.Attr('SC_Training_Match_Contract_Value')
T = Product.Attr('SC_Training_Match_Contract_Value').GetValue()
P = Product.Attr('SC_Training_Match_Contract_Value_Percent').GetValue()
if Training_Match_Value is not None:
    Training_Match_Value = T
    Product.Attr('SC_Training_Match_Contract_Value').AssignValue(T)
    Product.Attr('SC_Training_Match_Contract_Value_Percent').Access = AttributeAccess.ReadOnly