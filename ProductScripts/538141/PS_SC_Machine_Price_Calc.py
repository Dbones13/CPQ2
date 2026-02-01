#To convert Machine Price(USD) to Quote Currency if Quote Currency is NOT USD:
quoteCurrency = Quote.SelectedMarket.CurrencyCode
NO_Machines =  Product.Attr('SC_QCS_No_Of_Machines').GetValue()
if NO_Machines == '':
    NO_Machines = 0
CM = Product.Attr('SC_QCS_Site_to_Cloud_Method').GetValue()
if CM == 'Edge Device Virtual Machine':
    Product.Attr('SC_QCS_Qty_Honeywell_Edge_Device_VM').SelectValue('&nbsp')
else:
    Product.ResetAttr('SC_QCS_Qty_Honeywell_Edge_Device_VM')
if CM == 'MSS-VSE/VPE (Service Node)':
    Product.Attr('SC_QCS_Quantity_Honeywell_Service_Node').SelectValue('&nbsp')
else:
    Product.ResetAttr('SC_QCS_Quantity_Honeywell_Service_Node')
Price_new = SqlHelper.GetFirst("select Price from SC_HARDCODE_PRICE where Name = 'QCS Support Edge Device' ")
USD_Price = Price_new.Price
EXCHANGE_RATE = Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content if Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content else 1 #SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = 'USD' and To_Currency = '{}'".format(quoteCurrency))
if quoteCurrency != 'USD':
    M_Price = round((float(USD_Price)*float(EXCHANGE_RATE)),2)
    Trace.Write(M_Price)    
if  quoteCurrency == 'USD': 
    M_Price = USD_Price
Product.Attr('SC_QCS_Per_Machine_Price').AssignValue(str(M_Price))
Support_LP = round((float(NO_Machines)*float(M_Price)),2)
Product.Attr('SC_QCS_Support_Center_List_Price').AssignValue(str(Support_LP))