#PS_Refresh_PM_Labor_Container
import Update_Labor_Cost_Price
Product.ExecuteRulesOnce = True
if Quote:
    contList = ['Project_management_Labor_Container']
    Update_Labor_Cost_Price.updateLaborCostPrice(Product, Quote, TagParserQuote, contList, False, Session)
Product.ExecuteRulesOnce = False