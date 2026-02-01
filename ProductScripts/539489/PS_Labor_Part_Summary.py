#PS_Labor_Part_Summary
from Update_System_Labor_Cost_Price import updateLaborCostPrice
gesLocation = Product.Attr("MSC GES Location").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
cont = Product.GetContainerByName('Labor_PriceCost_Cont')
if Quote:
    contList = ['MSC_Engineering_Labor_Container','MSC_Additional_Labour_Container']
    foEngColumn = {'MSC_Engineering_Labor_Container':'MSC_FO_ENG','MSC_Additional_Labour_Container':'MSC_Addi_Labor_FO_Eng'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True)