from Update_System_Labor_Cost_Price import updateLaborCostPrice
tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if Product.Attr('isProductLoaded').GetValue() == 'True':
    gesLocation = 'None'
    if Product.GetContainerByName('CN900_Labor_Details').Rows.Count > 0:
        gesLocation = Product.GetContainerByName('CN900_Labor_Details').Rows[0].GetColumnByName('CN900_Ges_Location_Labour').DisplayValue
    gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','GES Egypt':'EG','None':'None'}
    gesLocationVC = gesMapping.get(gesLocation)
    if Quote:
        contList = ['CE CN900 Engineering Labor Container', 'CE CN900 Additional Custom Deliverables']
        foEngColumn = {'CE CN900 Engineering Labor Container':'CE_CN900_FO_ENG_LD', 'CE CN900 Additional Custom Deliverables':'CE_CN900_FO_ENG_LD'}
        updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True, Session)
Product.Attr('PERF_ExecuteScripts').AssignValue('')