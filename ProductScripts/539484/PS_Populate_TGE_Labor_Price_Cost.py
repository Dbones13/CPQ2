#PS_Update_Labor_Price_Cost
from Update_System_Labor_Cost_Price import updateLaborCostPrice
Product.ApplyRules()
gesLocation = Product.Attr("TGE_GES Location").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None'}
gesLocationVC = gesMapping.get(gesLocation)
cont = Product.GetContainerByName('Labor_PriceCost_Cont')
if Quote:
    contList = ['TGE_Engineering_Labor_Container', 'TGE_Additional_Labour_Container']
    foEngColumn = {'TGE_Engineering_Labor_Container':'TGE_Labor_FO1_FO2 Eng', 'TGE_Additional_Labour_Container':'TGE_ADDI_Labor_FO_Eng'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True)
    cont.Calculate()
    
Product.Attr('PERF_ExecuteScripts').AssignValue('')