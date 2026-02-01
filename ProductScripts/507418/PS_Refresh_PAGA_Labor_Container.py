#PS_Update_Labor_Price_Cost
from Update_System_Labor_Cost_Price import updateLaborCostPrice
gesLocation = Product.Attr("PAGA_GES_Location").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
cont = Product.GetContainerByName('Labor_PriceCost_Cont')
if Quote:
    contList = ['PAGA_Labor_Container', 'PAGA_Additional_Labour_Container']
    foEngColumn = {'PAGA_Labor_Container':'PAGA_Labor_FO1_FO2 Eng', 'PAGA_Additional_Labour_Container':'PAGA_Addi_Labor_FO_Eng'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True)
    cont.Calculate()

Product.Attr('PERF_ExecuteScripts').AssignValue('')