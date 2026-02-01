#Number of years in Price Calculator
Duration = Quote.GetCustomField('SC_CF_CONTRACTDURYR').Content
ContractExt = Quote.GetCustomField('SC_CF_IS_CONTRACT_EXTENSION').Content
Remove_str = "years"
Year = []
for ele in Duration:
    if ele not in Remove_str:
        Year.append(ele)
Year = ''.join(Year)
if ContractExt == "True":
    Year = "1"

Product.Attr('SC_QCS_Number of Years').Access = AttributeAccess.ReadOnly
Product.Attr('SC_QCS_Qty_Honeywell_Edge_Device_VM').Access = AttributeAccess.ReadOnly
Product.Attr('SC_QCS_Qty_Honeywell_Edge_Device').Access = AttributeAccess.ReadOnly
Product.Attr('SC_QCS_Quantity_Honeywell_Service_Node').Access = AttributeAccess.ReadOnly
Product.Attr('SC_QCS_No_Of_Machines').Access = AttributeAccess.ReadOnly
Product.Attr('SC_QCS_Per_Machine_Price').Access = AttributeAccess.ReadOnly
Product.Attr('SC_QCS_Support_Center_List_Price').Access = AttributeAccess.ReadOnly
Product.Attr('SC_QCS_Local Day Rate').Access = AttributeAccess.ReadOnly
Product.Attr('SC_QCS_Number of Years').AssignValue(Year)
#Hide other section and its attributes
OTattr = ['SC_QCS_Local Day Rate','SC_QCS_Local_Onboarding_Support_Days','SC_QCS_Qty_Honeywell_Edge_Device_VM','SC_QCS_Qty_Honeywell_Edge_Device','SC_QCS_Quantity_Honeywell_Service_Node','SC_QCS_Section_OneTime_Service_Charges']
SCattr =['SC_QCS_No_Of_Machines','SC_QCS_Per_Machine_Price','SC_QCS_Support_Center_List_Price','SC_QCS_Section_Support Center']
def disallowattr(attribute):
    Product.Attr(attribute).Allowed = False
A = int(Product.ParseString('<*AttSel(SC_QCS_One Time Service Charges)*>'))
B = int(Product.ParseString('<*AttSel(SC_QCS_Support_Center_Select)*>'))
if A == 0:
    for i in OTattr:
        disallowattr(i)
if B == 0:
    for j in SCattr:
        disallowattr(j)