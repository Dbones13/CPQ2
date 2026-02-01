#GS_SM_Populate_Price
from Update_System_Labor_Cost_Price import updateLaborCostPrice
gesLocation = 'None'
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None'}
if Product.GetContainerByName('SM_Labor_Cont').Rows.Count > 0:
    gesLocation = Product.GetContainerByName('SM_Labor_Cont').Rows[0].GetColumnByName('GES_Location').DisplayValue
    if (not gesLocation or gesLocation == 'None') and Quote.GetCustomField("R2QFlag").Content and Quote.GetGlobal('ExGesLocation'):
        gesLocation = gesMapping.keys()[gesMapping.values().index(Quote.GetGlobal('ExGesLocation'))]
gesLocationVC = gesMapping.get(gesLocation)
if Quote:
    contList = ['SM_SSE_Engineering_Labor_Container', 'SM Safety System - ESD/FGS/BMS/HIPPS Container', 'SM_Additional_Custom_Deliverables_Labor_Container']
    foEngColumn = {'SM_SSE_Engineering_Labor_Container':'SM_Labor_FO_Eng', 'SM Safety System - ESD/FGS/BMS/HIPPS Container':'SM_Labor_FO_Eng', 'SM_Additional_Custom_Deliverables_Labor_Container':'SM_Labor_FO_Eng'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True, Session)
Product.GetContainerByName('Labor_PriceCost_Cont').Calculate()
Product.Attr('PERF_ExecuteScriptsLabor').AssignValue('')