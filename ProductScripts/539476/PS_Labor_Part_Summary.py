#PS_Update_Labor_Price_Cost
from Update_System_Labor_Cost_Price import updateLaborCostPrice
nonr2q = Quote.GetCustomField('R2QFlag').Content
if not nonr2q:
    gesLocation = Product.Attr("FDM_GES_Location").GetValue()
    gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
    gesLocationVC = gesMapping.get(gesLocation)
else:
    gesLocationVC = Quote.GetGlobal('ExGesLocation')

if Quote:
    contList = ['FDM Engineering Labor Container', 'FDM Additional Custom Deliverables']
    foEngColumn = {'FDM Engineering Labor Container':'FDM_FO_ENG_LD', 'FDM Additional Custom Deliverables':'FDM_FO_ENG_LD'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True, Session)
    cont=Product.GetContainerByName('Labor_PriceCost_Cont')
    if cont:
        cont.Calculate()
Product.Attr('PERF_ExecuteScripts').AssignValue('')