#PS_Update_Labor_Price_Cost
from Update_System_Labor_Cost_Price import updateLaborCostPrice
gesLocation = Product.Attr("Experion_HS_Ges_Location_Labour").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
if Quote:
    contList = ['System_Network_Engineering_Labor_Container', 'System_Interface_Engineering_Labor_Container', 'Hardware Engineering Labour Container', 'HMI_Engineering_Labor_Container', 'Additional_CustomDev_Labour_Container','EBR_Engineering_Labor_Container']
    foEngColumn = {'System_Network_Engineering_Labor_Container':'System_Network_Labor_FO_Eng', 'System_Interface_Engineering_Labor_Container':'System_Interface_Labor_FO_Eng', 'Hardware Engineering Labour Container':'Hardware_Eng_FO_Eng_one', 'HMI_Engineering_Labor_Container':'HMI_Labor_FO_Eng', 'Additional_CustomDev_Labour_Container':'Additional_CustomDev_FO_Eng','EBR_Engineering_Labor_Container':'EBR_Labor_FO_Eng'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, False, Session)