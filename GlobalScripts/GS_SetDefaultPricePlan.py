def setCFValue(Quote, CF_Name, CF_Value):
    Quote.GetCustomField(CF_Name).Content = CF_Value
def getCFValue(Quote, CF_Name):
    return Quote.GetCustomField(CF_Name).Content
def setDefaultMpa(Quote,TagParserQuote):
    quote_type = TagParserQuote.ParseString('<*CTX( Quote.CustomField(Quote Type) )*>')
    Log.Info("quote_type :"+str(quote_type))
    if quote_type != "":
        query = TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Honeywell_Ref = '<*CTX(Quote.CustomField(MPA Honeywell Ref))*>' and Honeywell_Ref !='' and Price_Plan_Status= 'Active' and [IF]([EQ](<*CTX( Quote.CustomField(Quote Type) )*>,Projects)){Price_Plan_Systems_Discount}{Price_Plan_Parts_Discount}[ENDIF] = 'Y' and Price_Plan_Start_Date <= '<*CTX( Date.Format(MM/dd/yyyy) )*>' and ( Price_Plan_End_Date  IS NULL  or Price_Plan_End_Date >= '<*CTX( Date.Format(MM/dd/yyyy) )*>')")
        res = SqlHelper.GetList(query)
        Log.Info("res :"+str(query))
        if res and len(res) == 1:
            setCFValue(Quote , 'MPA Price Plan' , res[0].Price_Plan_Name)
        elif  res and len(res) >1:
            if getCFValue(Quote, 'Quote Type') != "Projects":
                for result in res:
                    if str(result.IS_DEFAULT_PRICE_PLAN) == "True":
                        setCFValue(Quote , 'MPA Price Plan' , str(result.Price_Plan_Name))
                        break
            elif getCFValue(Quote, 'Quote Type') == "Projects":
                for result in res:
                    if str(result.IS_DEFAULT_SYSTEM_PLAN) == "True":
                        Log.Info(" MPA PP cus := "+str(result.Price_Plan_Name))
                        setCFValue(Quote , 'MPA Price Plan' , str(result.Price_Plan_Name))
                        break
        else:
            setCFValue(Quote , 'MPA Price Plan' , '')
    else:
        setCFValue(Quote , 'MPA Price Plan' , '')