try:
    if Quote.GetCustomField("Quote Type").Content=='Projects' and Quote.GetCustomField("IsERPCalled").Content=='False':
    	Quote.GetCustomField("IsERPCalled").Content='True'
        Quote.ExecuteAction(1823)
except:
    pass