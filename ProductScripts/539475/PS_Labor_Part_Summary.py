#PS_Update_Labor_Price_Cost
from Update_System_Labor_Cost_Price import updateLaborCostPrice
gesLocation = Product.Attr("Experion_HS_Ges_Location_Labour").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None'}
gesLocationVC = gesMapping.get(gesLocation)
if Quote:
    contList = ['Experion HS Engineering Labor Container', 'Experion HS Additional Custom Deliverables']
    foEngColumn = {'Experion HS Engineering Labor Container':'Experion_HS_FO_ENG_LD', 'Experion HS Additional Custom Deliverables':'Experion_HS_FO_ENG_LD'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True, Session)

Product.Attr('PERF_ExecuteScripts').AssignValue('')