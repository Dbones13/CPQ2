#PS_Update_Labor_Price_Cost
from Update_System_Labor_Cost_Price import updateLaborCostPrice
gesLocation = Product.Attr("MSE GES Location").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
if Quote:
    contList = ['MSE_Engineering_Labor_Container', 'MSE_Additional_Labor_Container']
    foEngColumn = {'MSE_Engineering_Labor_Container':'MSE_FO_ENG', 'MSE_Additional_Labor_Container':'MSE_Addi_Labor_FO_Eng'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True)