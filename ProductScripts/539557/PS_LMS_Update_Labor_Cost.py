#PS_LMS_Update_Labor_Cost
Log.Write("Pricing Started")
from Update_System_Labor_Cost_Price import updateLaborCostPrice
Product.ApplyRules()
gesLocation = Product.Attr("LMS_GES_Location").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
cont = Product.GetContainerByName('Labor_PriceCost_Cont')
if Quote:
    contList = ['LMS_Labor_Container', 'LMS_Additional_Labor_Container']
    foEngColumn = {'LMS_Labor_Container':'LMS_Labor_FO1_FO2 Eng', 'LMS_Additional_Labor_Container':'LMS_Addi_Labor_FO_Eng'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True)
    cont.Calculate()

Product.Attr('PERF_ExecuteScripts').AssignValue('')