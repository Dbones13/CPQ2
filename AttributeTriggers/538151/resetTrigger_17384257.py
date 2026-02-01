att1=Product.Attr('SC_Training_Match_Contract_Value_Percent')
att2=Product.Attr('SC_Training_Match_Contract_Value')
val1=att1.GetValue()
val2=att2.GetValue()
if val1 in ("",None) and val2 in ("",None):
    Trace.Write("Both Editable")
    att1.Access=AttributeAccess.Editable
    att2.Access=AttributeAccess.Editable
elif val1=="" and val2!="":
    Trace.Write("ATT1 ReadOnly")
    att1.Access=AttributeAccess.ReadOnly
elif val1!="" and val2=="":
    Trace.Write("ATT2 ReadOnly")
    att2.Access=AttributeAccess.ReadOnly