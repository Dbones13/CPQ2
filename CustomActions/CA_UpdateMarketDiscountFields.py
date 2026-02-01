def getCFValue(cfName):
    return Quote.GetCustomField(cfName).Content

def setCFValue(cfName,Value):
    Quote.GetCustomField(cfName).Content = Value

if getCFValue("Booking LOB") in ('LSS','PAS','HCP') and getCFValue("Quote Type") == "Projects":
    setCFValue("Schedule Price Plan Updated","False")

    MultiplePricePlanPresent = False
    query = TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Honeywell_Ref = '<*CTX(Quote.CustomField(MPA Honeywell Ref))*>' and Price_Plan_Status= 'Active' and Price_Plan_Parts_Discount = 'Y' and Price_Plan_Start_Date <= '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date >= '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
    res = SqlHelper.GetList(query)
    if res and len(res) > 1:
        MultiplePricePlanPresent = True
    if MultiplePricePlanPresent:
        setCFValue("Selected Discount Plan","")
        setCFValue("Recommended Discount Plan","")
        quoteDetails = Quote.QuoteTables["Quote_Details"]
        for row in quoteDetails.Rows:
            row["Recommended_Target_Price"] = 0
        quoteDetails.Save()