#PS_IS_Update_Labor_Cost
#Log.Write("Pricing Started")
from Update_System_Labor_Cost_Price import updateLaborCostPrice
Product.ApplyRules()
gesLocation = Product.Attr("IS_GES_Location").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
cont = Product.GetContainerByName('Labor_PriceCost_Cont')
if Quote:
    contList = ['IS_Labor_Container', 'IS_Additional_Labor_Container']
    foEngColumn = {'IS_Labor_Container':'IS_Labor_FO1_FO2 Eng', 'IS_Additional_Labor_Container':'IS_Addi_Labor_FO_Eng'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True)
    cont.Calculate()

Product.Attr('PERF_ExecuteScripts').AssignValue('')