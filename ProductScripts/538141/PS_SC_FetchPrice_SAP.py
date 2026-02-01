#For populating Local day rate
import GS_GetPriceFromCPS
part = ['SVC-QST2-FD']
priceDict = {}
priceDict = GS_GetPriceFromCPS.getPrice(Quote,priceDict,part,TagParserQuote,Session)
b = priceDict.get('SVC-QST2-FD')
Product.Attr('SC_QCS_Local Day Rate').AssignValue(str(b))