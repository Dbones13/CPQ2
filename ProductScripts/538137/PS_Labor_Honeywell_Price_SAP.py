#To populate Price from SAP on Resource Type:
import GS_GetPriceFromCPS
RT = Product.Attr('SC_Labor_Resource_Type').Values
Country = Quote.GetCustomField('Opportunity Tab Booking Country').Content
part = Product.Attr('SC_Labor_Resource_Type').GetValue().split(',')[0]
priceDict = {}
priceDict = GS_GetPriceFromCPS.getPrice(Quote,priceDict,[part],TagParserQuote,Session)
b = priceDict.get(part)
if b == None:
    Product.Attr('SC_Labor_Honeywell_List_Price').AssignValue('0')
else:
    Product.Attr('SC_Labor_Honeywell_List_Price').AssignValue(b)  
Trace.Write(b)