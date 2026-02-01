#PS_Populate_Prices
from Update_System_Labor_Cost_Price import updateLaborCostPrice
tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if Product.Attr('isProductLoaded').GetValue() == 'True' and 'Labor Deliverables' in tabs:
    gesLocation = 'None'
    if Product.GetContainerByName('SM_Labor_Cont').Rows.Count > 0:
        gesLocation = Product.GetContainerByName('SM_Labor_Cont').Rows[0].GetColumnByName('GES_Location').DisplayValue
    gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','GES Egypt':'EG','None':'None'}
    gesLocationVC = gesMapping.get(gesLocation)
    if Quote:
        contList = ['SM_SSE_Engineering_Labor_Container', 'SM Safety System - ESD/FGS/BMS/HIPPS Container', 'SM_Additional_Custom_Deliverables_Labor_Container']
        foEngColumn = {'SM_SSE_Engineering_Labor_Container':'SM_Labor_FO_Eng', 'SM Safety System - ESD/FGS/BMS/HIPPS Container':'SM_Labor_FO_Eng', 'SM_Additional_Custom_Deliverables_Labor_Container':'SM_Labor_FO_Eng'}
        updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True, Session)