#PS_Labor_Part_Summary
from Update_System_Labor_Cost_Price import updateLaborCostPrice
gesLocation = Product.Attr("OWS_GES Location").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
cont = Product.GetContainerByName('Labor_PriceCost_Cont')
if Quote:
    contList = ['OWS_Engineering_Labor_Container','OWS_Additional_Labour_Container']
    foEngColumn = {'OWS_Engineering_Labor_Container':'OWS_Labor_FO1_FO2 Eng','OWS_Additional_Labour_Container':'OWS_ADDI_Labor_FO_Eng'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True)