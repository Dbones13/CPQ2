#PS_Update_Labor_Price_Cost
from Update_System_Labor_Cost_Price import updateLaborCostPrice
gesLocation = Product.Attr("Generic_Ges_Location_Labour").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','GES Egypt':'EG','None':'None'}
gesLocationVC = gesMapping.get(gesLocation)
if Quote:
    contList = ['Generic Engineering Labor Container', 'Generic Additional Custom Deliverables']
    foEngColumn = {'Generic Engineering Labor Container':'Generic_FO_ENG_LD', 'Generic Additional Custom Deliverables':'Generic_FO_ENG_LD'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True, Session)

Product.Attr('PERF_ExecuteScripts').AssignValue('')