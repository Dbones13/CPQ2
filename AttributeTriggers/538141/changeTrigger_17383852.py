#To convert Machine Price(USD) to Quote Currency if Quote Currency is NOT USD:
'''
quoteCurrency = Quote.SelectedMarket.CurrencyCode
NO_Machines =  Product.Attr('SC_QCS_No_Of_Machines').GetValue()
CM = Product.Attr('SC_QCS_Site_to_Cloud_Method').GetValue()
if CM == 'Edge Device':
    X = 1
elif CM == 'Edge Device Virtual Machine':
    X = 2
elif CM == 'MSS-VSE/VPE (Service Node)':
    X = 3
Price = SqlHelper.GetFirst("select Price from SC_HARDCODE_PRICE where Comments = '{}' ".format(X))
USD_Price = Price.Value

query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = 'USD' and To_Currency = '{}'".format(quoteCurrency))
if quoteCurrency != 'USD':
    M_Price = float(USD_Price)*float(query.Exchange_Rate)
    Trace.Write(M_Price)    
if  quoteCurrency == 'USD': 
    M_Price = float(USD_Price)
Product.Attr('SC_QCS_Per_Machine_Price').AssignValue(str(M_Price))
Support_LP = float(NO_Machines)*M_Price
Product.Attr('SC_QCS_Support_Center_List_Price').AssignValue(str(Support_LP))
Trace.Write(Support_LP)
'''
#Change product status as incomplete
'''tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Scope Selection' in tabs:
    Product.Attr('SC_Product_Status').AssignValue("0")
else:
    Product.Attr('SC_Product_Status').AssignValue("1")'''