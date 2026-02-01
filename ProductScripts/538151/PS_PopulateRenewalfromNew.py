SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if SC_Product_Type == 'Renewal':
    SC_Training_Match_Contract_Value_PY =  Product.Attr('SC_Training_Match_Contract_Value_PY').GetValue()
    SC_Training_Match_Contract_Value_Percent_PY = float(Product.Attr('SC_Training_Match_Contract_Value_Percent_PY').GetValue() if Product.Attr('SC_Training_Match_Contract_Value_Percent_PY').GetValue() else 0)
    Trace.Write("SC_Training_Match_Contract_Value  New  " +str(SC_Training_Match_Contract_Value_PY))
    Trace.Write("SC_Training_Match_Contract_Value_Percent  New  " +str(SC_Training_Match_Contract_Value_Percent_PY))
    Product.Attr('SC_Training_Match_Contract_Value').AssignValue(str(SC_Training_Match_Contract_Value_PY))
    Product.Attr('SC_Training_Match_Contract_Value_Percent').AssignValue(str(SC_Training_Match_Contract_Value_Percent_PY))
    Training_Match_Value = Product.Attr('SC_Training_Match_Contract_Value')
    Training_Match_Value_Per = Product.Attr('SC_Training_Match_Contract_Value_Percent')
    if SC_Training_Match_Contract_Value_Percent_PY >= 10.0 :
        Training_Match_Value_Per.Allowed = True
        Training_Match_Value_Per.Access = AttributeAccess.Editable
    '''elif SC_Training_Match_Contract_Value_Percent_PY < 10.0 :
        Training_Match_Value.Allowed = True
        Training_Match_Value.Access = AttributeAccess.Editable'''
    #Product.Attr('SC_Renewal_check').AssignValue('1')