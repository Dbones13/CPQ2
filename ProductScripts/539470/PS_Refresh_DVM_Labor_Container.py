#PS_Update_Labor_Price_Cost
from Update_System_Labor_Cost_Price import updateLaborCostPrice
gesLocation = Product.Attr("DVM_GES_Location").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
if Quote:
    contList = ['DVM_Engineering_Labor_Container', 'DVM_Additional_Labour_Container']
    foEngColumn = {'DVM_Engineering_Labor_Container':'DVM_FOENG', 'DVM_Additional_Labour_Container':'DVM_Additional_Project_FOENG_Deliverables'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True, Session)