#PS_Update_Labor_Price_Cost
from Update_System_Labor_Cost_Price import updateLaborCostPrice
gesLocation = Product.Attr("PlantCruise_Ges_Location_Labour").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None'}
gesLocationVC = gesMapping.get(gesLocation)
if Quote:
    contList = ['PlantCruise Engineering Labor Container', 'PlantCruise Additional Custom Deliverables']
    foEngColumn = {'PlantCruise Engineering Labor Container':'PlantCruise_FO_ENG_LD', 'PlantCruise Additional Custom Deliverables':'PlantCruise_FO_ENG_LD'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, False)