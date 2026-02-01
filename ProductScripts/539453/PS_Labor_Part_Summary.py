#PS_Labor_Part_Summary
from Update_System_Labor_Cost_Price import updateLaborCostPrice
nonr2q = Quote.GetCustomField('R2QFlag').Content
if not nonr2q:
    gesLocation = Product.Attr("Experion_HS_Ges_Location_Labour").GetValue()
    gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
    gesLocationVC = gesMapping.get(gesLocation)
else:
    gesLocationVC = Quote.GetGlobal('ExGesLocation')
cont = Product.GetContainerByName('Labor_PriceCost_Cont')
if Quote:
    contList = ['System_Network_Engineering_Labor_Container', 'System_Interface_Engineering_Labor_Container', 'Hardware Engineering Labour Container', 'HMI_Engineering_Labor_Container', 'Additional_CustomDev_Labour_Container','EBR_Engineering_Labor_Container']
    foEngColumn = {'System_Network_Engineering_Labor_Container':'System_Network_Labor_FO_Eng', 'System_Interface_Engineering_Labor_Container':'System_Interface_Labor_FO_Eng', 'Hardware Engineering Labour Container':'Hardware_Eng_FO_Eng_one', 'HMI_Engineering_Labor_Container':'HMI_Labor_FO_Eng', 'Additional_CustomDev_Labour_Container':'Additional_CustomDev_FO_Eng','EBR_Engineering_Labor_Container':'EBR_Labor_FO_Eng'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True, Session)
    if cont:
    	cont.Calculate()