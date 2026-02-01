'''LS = int(Product.ParseString("<* AttSel(SC_Labor_LumpSum) *>"))
RT = Product.Attr('SC_Labor_Resource_Type').GetValue()
Country = Quote.GetCustomField('Opportunity Tab Booking Country').Content
Trace.Write(LS)
if LS == 1 :
    Product.DisallowAttr('SC_Labor_Burden_for_Hr_Day')
    Product.DisallowAttr('SC_Labor_Hrs_per_Full_Day')
    Product.DisallowAttr('SC_Labor_Resource_Type')
    Product.Attr('SC_Labor_Honeywell_List_Price').Access = AttributeAccess.Editable
else:
    Product.AllowAttr('SC_Labor_Burden_for_Hr_Day')
    Product.AllowAttr('SC_Labor_Hrs_per_Full_Day')
    Product.AllowAttr('SC_Labor_Resource_Type')
    Product.Attr('SC_Labor_Hrs_per_Full_Day').AssignValue('8')
    Product.Attr('SC_Labor_Honeywell_List_Price').Access = AttributeAccess.ReadOnly
    Product.Attr('SC_Labor_Customer_List_Price').Access = AttributeAccess.ReadOnly
    Product.Attr('SC_Labor_Burden_for_Hr_Day').Access = AttributeAccess.ReadOnly
    ScriptExecutor.Execute('PS_Labor_Honeywell_Price_SAP')'''