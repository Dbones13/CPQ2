#PS_Update_Labor_Price_Cost
from Update_System_Labor_Cost_Price import updateLaborCostPrice
gesLocation = Product.Attr("MX_HC_GES_Location").GetValue()
gesMapping = {'India':'IN','China':'CN','Romania':'RO','Uzbekistan':'UZ','Egypt':'EG','None':'None'}
gesLocationVC = gesMapping.get(gesLocation)
if Quote:
    contList = ['Experion_mx_Labor_Container', 'Experion_mx_labor_Additional_Cust_Deliverables_con']
    foEngColumn = {'Experion_mx_Labor_Container':'Experion_mx_Labor_FO_Eng_1', 'Experion_mx_labor_Additional_Cust_Deliverables_con':'Experion_mx_Labor_FO_Eng'}
    updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True, Session)
    Product.GetContainerByName('Labor_PriceCost_Cont').Calculate()