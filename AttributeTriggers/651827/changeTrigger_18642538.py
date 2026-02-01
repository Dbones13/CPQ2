from GS_Curr_ExchRate_Mod import fn_get_curr_exchrate
Quote_Currency = Quote.GetCustomField("SC_CF_CURRENCY").Content
exchange_rate = fn_get_curr_exchrate(Quote_Currency, "USD")
customerBudget = Product.Attr('Customer_Budget_TextField').GetValue()
if customerBudget:
    cust_bud_usd = round(float(customerBudget)*exchange_rate, 2)
    formatted_value = "{:,.2f}".format(cust_bud_usd)
    Product.Attr('Customer_Budget_USD').AssignValue(str(formatted_value))
else:
    Product.Attr('Customer_Budget_USD').AssignValue('')