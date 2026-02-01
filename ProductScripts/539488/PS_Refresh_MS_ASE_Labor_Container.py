#PS_Update_Labor_Price_Cost
from Update_System_Labor_Cost_Price import updateLaborCostPrice
gesLocation = Product.Attr("MSASE_GES_Location").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
cont = Product.GetContainerByName('Labor_PriceCost_Cont')
if Quote:
    contList = ['MS_ASE_Engineering_Labor_Container', 'MS_ASE_Additional_Labour_Container']
    foEngColumn = {'MS_ASE_Engineering_Labor_Container':'MS_ASE_Labor_FO1_FO2 Eng', 'MS_ASE_Additional_Labour_Container':'MS_ASE_ADDI_Labor_FO_Eng'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True)
    cont.Calculate()