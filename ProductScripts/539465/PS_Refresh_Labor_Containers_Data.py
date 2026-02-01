#PS_Populate_Prices
from Update_System_Labor_Cost_Price import updateLaborCostPrice
tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if Product.Attr('isProductLoaded').GetValue() == 'True':
    gesLocation = 'None'
    if Product.GetContainerByName('RTU_Software_Labor_Container2').Rows.Count > 0:
        gesLocation = Product.GetContainerByName('RTU_Software_Labor_Container2').Rows[0].GetColumnByName('RTU_GES_Location').DisplayValue
    gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None'}
    gesLocationVC = gesMapping.get(gesLocation)
    if Quote:
        contList = ['CE RTU Engineering Labor Container', 'CE RTU Additional Custom Deliverables']
        foEngColumn = {'CE RTU Engineering Labor Container':'CE_UOC_FO_ENG_LD', 'CE RTU Additional Custom Deliverables':'CE_UOC_FO_ENG_LD'}
        updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True, Session)
Product.Attr('PERF_ExecuteScripts').AssignValue('')