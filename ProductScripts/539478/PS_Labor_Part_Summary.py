#PS_Update_Labor_Price_Cost
from Update_System_Labor_Cost_Price import updateLaborCostPrice
gesLocation = Product.Attr("HC900_Ges_Location_Labour").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','GES Egypt':'EG','None':'None'}
gesLocationVC = gesMapping.get(gesLocation)
if Quote:
    contList = ['HC900 Engineering Labor Container', 'HC900 Additional Custom Deliverables']
    foEngColumn = {'HC900 Engineering Labor Container':'HC900_FO_ENG_LD', 'HC900 Additional Custom Deliverables':'HC900_FO_ENG_LD'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True, Session)

Product.Attr('PERF_ExecuteScripts').AssignValue('')