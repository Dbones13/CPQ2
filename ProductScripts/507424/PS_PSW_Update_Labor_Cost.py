#PS_PSW_Update_Labor_Cost
Product.ApplyRules()
Log.Write("PV"+Product.Attr('Final_Hrs').GetValue())
from Update_System_Labor_Cost_Price import updateLaborCostPrice
gesLocation = Product.Attr("PSW_GES_Location").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
cont = Product.GetContainerByName('Labor_PriceCost_Cont')
if Quote:
    contList = ['PSW_Labor_Container', 'PSW_Additional_Labor_Container']
    foEngColumn = {'PSW_Labor_Container':'PSW_Labor_FO 1/FO2 Eng', 'PSW_Additional_Labor_Container':'PSW_FO_Eng_dropdown'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True)
    cont.Calculate()
Product.Attr('PERF_ExecuteScripts').AssignValue('')