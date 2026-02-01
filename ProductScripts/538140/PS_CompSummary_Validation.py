tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Scope Summary' in tabs:
    sp = Product.Attr('SC_TPS_Service_Product').GetValue()
    CSContainer = Product.GetContainerByName("ComparisonSummary")
    if CSContainer.Rows.Count>0:
        for crow in CSContainer.Rows:
            if crow.IsSelected: #scope removal selected
                crow['CY_Service_Product'] = None
                crow['Error_Message'] = None
            else:#Inscope
                if crow['PY_Service_Prod_Status']=='Active': #If previous year SP is active but not configured in the module
                    if sp != crow['Service_Product']:
                        crow['CY_Service_Product'] = None
                        #Display Error message
                        crow['Error_Message'] = crow['Service_Product']+' Service Product is not configured in the module.'
                    else:
                        crow['CY_Service_Product'] = crow['Service_Product']
                        crow['Error_Message'] = None
                else:#Inactive previous year service product
                    #validate replacement service product
                    if crow['CY_Service_Product'] not in (None,''):
                        if sp != crow['CY_Service_Product']:
                            crow['Error_Message'] = crow['CY_Service_Product'] +' Service Product is not configured in the module.'
                        else:
                            crow['Error_Message'] = None
                    else:
                        crow['Error_Message'] = 'Previous Year Service Product '+crow['Service_Product'] + ' is inactive. Please Choose the CY Service Product(Replacement Product) in Comparison Summary'