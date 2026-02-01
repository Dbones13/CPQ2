#PS_Update_Labor_Price_Cost
from Update_System_Labor_Cost_Price import updateLaborCostPrice
gesLocation = Product.Attr("PCD_Ges_Location_Labour").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None'}
gesLocationVC = gesMapping.get(gesLocation)
if Quote:
    contList = ['PCD Engineering Labor Container', 'PCD Additional Custom Deliverables']
    foEngColumn = {'PCD Engineering Labor Container':'PCD_FO_ENG_LD', 'PCD Additional Custom Deliverables':'PCD_FO_ENG_LD'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, False)