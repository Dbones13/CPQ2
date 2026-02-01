#PS_GMS_Update_Labor_Cost
Log.Write("Pricing Started")
from Update_System_Labor_Cost_Price import updateLaborCostPrice
Product.ApplyRules()
gesLocation = Product.Attr("GAS MeterSuite GES Location").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
cont = Product.GetContainerByName('Labor_PriceCost_Cont')
if Quote:
    contList = ['Gas_MeterSuite_Engineering_Labor_Container', 'Gas_MeterSuite_Additional_Labor_Container']
    foEngColumn = {'Gas_MeterSuite_Engineering_Labor_Container':'GAS_MeterSuite_Labor_FO1_FO2 Eng', 'Gas_MeterSuite_Additional_Labor_Container':'GAS_MeterSuite_Addi_Labor_FO_Eng'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True)
    cont.Calculate()

Product.Attr('PERF_ExecuteScripts').AssignValue('')