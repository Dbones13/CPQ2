P =  Product.Attr('SC_Training_Match_Contract_Value_Percent').GetValue()
TM_Value_Percent = Product.Attributes.GetByName("SC_Training_Match_Contract_Value_Percent")
if P != '' and P is not None:
    for value in TM_Value_Percent.Values:
        val=value.Display#.replace("%","")
        if int(float(val)) > int(10):
            value.Display = str(10)
        else:
            value.Display = value.Display 
if P=='' :
    Product.Attr('SC_Training_Match_Contract_Value').Access = AttributeAccess.Editable
else:
    Product.Attr('SC_Training_Match_Contract_Value').Access = AttributeAccess.ReadOnly