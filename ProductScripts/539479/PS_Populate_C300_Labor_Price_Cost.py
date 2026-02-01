#PS_Update_Labor_Price_Cost
from Update_System_Labor_Cost_Price import updateLaborCostPrice
gesLocation = Product.Attr("C300_GES_Location").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
cont = Product.GetContainerByName('Labor_PriceCost_Cont')
if Quote:
    contList = ['C300_Engineering_Labor_Container', 'C300_Additional_Custom_Deliverables_Container']
    foEngColumn = {'C300_Engineering_Labor_Container':'C300_FO_ENG', 'C300_Additional_Custom_Deliverables_Container':'C300_FO_ENG'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True, Session)
    #cont.Calculate()
Product.Attr('PERF_ExecuteScriptsLabor').AssignValue('')