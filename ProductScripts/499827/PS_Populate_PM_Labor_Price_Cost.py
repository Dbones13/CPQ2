#PS_Populate_PM_Labor_Price_Cost
import Update_Labor_Cost_Price
##Product.ExecuteRulesOnce = True
if Quote:
    contList = ['Project_management_Labor_Container', 'Labor_Container', 'PLE_Labor_Container', 'PM_Additional_Custom_Deliverables_Labor_Container']
    Update_Labor_Cost_Price.updateLaborCostPrice(Product, Quote, TagParserQuote, contList, False, Session)