from Scripting.QuoteTables import AccessLevel
pld = Quote.QuoteTables['Product_Line_Details']
plsg = Quote.QuoteTables['Product_Line_Sub_Group_Details']
ptd  = Quote.QuoteTables['Product_Type_Details']
mpa_dis = Quote.GetCustomField('Labor MPA discount to be applied Manually').Content

if mpa_dis == "" or mpa_dis == None:
    Quote.GetCustomField('Labor MPA discount to be applied Manually').Content='No'

MPA=Quote.GetCustomField('MPA').Content
MPAPlan=Quote.GetCustomField('MPA Price Plan Commercial').Content
AgreementTypeQuery="Select Agreement_Type from MPA_PRICE_PLAN_MAPPING where Price_Plan_Name='{}'".format(MPAPlan)
results=SqlHelper.GetFirst(AgreementTypeQuery)
if MPA!='' and results:
    Trace.Write(str(results.Agreement_Type))
    Quote.GetCustomField('Agreement Type').Content=results.Agreement_Type
else:
    Quote.GetCustomField('Agreement Type').Content= None

if mpa_dis != "Yes":
    pld.GetColumnByName('Labour_MPA_Discount').AccessLevel = AccessLevel.Hidden
    plsg.GetColumnByName('Labour_MPA_Discount').AccessLevel = AccessLevel.Hidden
    ptd.GetColumnByName('Labour_MPA_Discount').AccessLevel = AccessLevel.Hidden
else:
    pld.GetColumnByName('Labour_MPA_Discount').AccessLevel = AccessLevel.Editable
    plsg.GetColumnByName('Labour_MPA_Discount').AccessLevel = AccessLevel.Editable
    ptd.GetColumnByName('Labour_MPA_Discount').AccessLevel = AccessLevel.Editable