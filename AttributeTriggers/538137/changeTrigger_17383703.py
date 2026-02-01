#To populate Burden rate  from CustomTable based  and Price from SAP on Resource Type:
import GS_GetPriceFromCPS

resourceType = Product.Attr('SC_Labor_Resource_Type').SelectedValue.ValueCode if Product.Attr('SC_Labor_Resource_Type').SelectedValue != None else ''
RT = Product.Attr('SC_Labor_Resource_Type').Values
Country = Quote.GetCustomField('Opportunity Tab Booking Country').Content
quoteCurrency = Quote.SelectedMarket.CurrencyCode
Burden = 0
Bur_PerHour = 0

RT_query = SqlHelper.GetFirst("select Currency,Work_Hour,Burden_Rate,List_Price from CT_SC_LABOR_RESOURCETYPE where Country = '{}' and Type = '{}'".format(Country,resourceType))
Trace.Write("Helll-->"+str(RT_query))
if resourceType == "A360 Contract Management" or resourceType == "Service Contract Management":
    Product.Attr('SC_Labor_Deliverable_Hours').AssignValue('1')
    Product.Attr('SC_Labor_Burden_for_Hr_Day').AssignValue('1')
    Product.Attr('SC_Labor_Honeywell_List_Price').AssignValue('1')
    Product.Attr('SC_Labor_Burden_for_Hr_Day').Access = AttributeAccess.Editable
    Product.Attr('SC_Labor_Honeywell_List_Price').Access = AttributeAccess.Editable

else:
    Product.Attr('SC_Labor_Burden_for_Hr_Day').Access = AttributeAccess.ReadOnly
    Product.Attr('SC_Labor_Honeywell_List_Price').Access = AttributeAccess.ReadOnly
    if RT_query is not None:
        currencyCode = RT_query.Currency
        Burden = round(float(RT_query.Burden_Rate),2)
        if quoteCurrency != currencyCode:
            a = extRateValue_query = SqlHelper.GetFirst("SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = '{}' AND To_Currency = '{}' ".format(str(currencyCode),str(Quote.GetCustomField('SC_CF_CURRENCY').Content)))
            Trace.Write("testting-->"+str(currencyCode)+"	str(Quote.GetCustomField('SC_CF_CURRENCY').Content)-->"+str(str(Quote.GetCustomField('SC_CF_CURRENCY').Content)))
            #extRateValue = Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content if Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content else 1
            extRateValue_query = SqlHelper.GetFirst("SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = '{}' AND To_Currency = '{}' ".format(str(currencyCode),str(Quote.GetCustomField('SC_CF_CURRENCY').Content)))
            extRateValue=1
            if extRateValue_query:
                extRateValue = extRateValue_query.Exchange_Rate
            Burden = Burden * float(extRateValue)
            Burden = round(float(Burden),2)
        Bur_PerHour = Burden/float(RT_query.Work_Hour)
    Product.Attr('SC_Labor_Burden_for_Hr_Day').AssignValue(str(Bur_PerHour))
    priceDict = {}
    part = ""
    if Product.Attr('SC_Labor_Resource_Type').GetValue():
        part = Product.Attr('SC_Labor_Resource_Type').GetValue().split(',')[0]
        priceDict = GS_GetPriceFromCPS.getPrice(Quote,priceDict,[part],TagParserQuote,Session)
    b = priceDict.get(part)
    if b == None:
        Product.Attr('SC_Labor_Honeywell_List_Price').AssignValue('0')
    else:
        Product.Attr('SC_Labor_Honeywell_List_Price').AssignValue(b)

ScriptExecutor.Execute('PS_Calculate_total_prices')