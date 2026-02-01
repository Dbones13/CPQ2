#PS_FGC_Update_Labor_Cost
Log.Write("Pricing Started")
from Update_System_Labor_Cost_Price import updateLaborCostPrice
Product.ApplyRules()
gesLocation = Product.Attr("FGC_GES_Location").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
cont = Product.GetContainerByName('Labor_PriceCost_Cont')
if Quote:
    contList = ['FGC_Engineering_Labor_Container', 'FGC_Additional_Labour_Container']
    foEngColumn = {'FGC_Engineering_Labor_Container':'FGC_Labor_FO1_FO2 Eng', 'FGC_Additional_Labour_Container':'FGC_Addi_Labor_FO_Eng'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True)
    #updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True, Session)
    cont.Calculate()

Product.Attr('PERF_ExecuteScripts').AssignValue('')