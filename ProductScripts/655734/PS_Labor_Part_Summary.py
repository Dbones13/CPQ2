#PS_Update_Labor_Price_Cost
from Update_System_Labor_Cost_Price import updateLaborCostPrice
gesLocation = Product.Attr("Terminal_Ges_Location_Labour").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','None':'None'}
gesLocationVC = gesMapping.get(gesLocation)
if Quote:
    contList = ['Terminal Engineering Labor Container', 'Terminal Additional Custom Deliverables']
    foEngColumn = {'Terminal Engineering Labor Container':'Terminal_FO_ENG_LD', 'Terminal Additional Custom Deliverables':'Terminal_FO_ENG_LD'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True, Session)

Product.Attr('PERF_ExecuteScripts').AssignValue('')