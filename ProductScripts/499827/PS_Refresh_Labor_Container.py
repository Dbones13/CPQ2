#PS_Refresh_Labor_Container
import Update_Labor_Cost_Price
Product.ExecuteRulesOnce = True
if Quote:
    contList = ['Labor_Container']
    Update_Labor_Cost_Price.updateLaborCostPrice(Product, Quote, TagParserQuote, contList, False, Session)
Product.ExecuteRulesOnce = False