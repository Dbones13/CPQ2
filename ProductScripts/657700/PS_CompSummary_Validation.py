tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
chk_dupl_list=[]
if 'Scope Summary' in tabs: # run the script only on scope summary tab
    import GS_SC_UpdateProducts2  as gsup
    CSContainer = Product.GetContainerByName("ComparisonSummary")

    if CSContainer.Rows.Count>0:
        for crow in CSContainer.Rows:
            if crow['PY_Service_Prod_Status']=='Active':
                chk_dupl_list.append(crow['Service_Product'])
                
            
        for crow in CSContainer.Rows:
            #crow['Error_Message']=None
            Trace.Write(crow['Service_Product']+' before duplicates:'+str(chk_dupl_list))
            if crow.IsSelected: #scope removal selected
                crow['CY_Service_Product']=None
                crow['Error_Message']=None
            else:#Inscope
                if crow['PY_Service_Prod_Status']=='Active': #active previous year service product is configured
                    ret_v=gsup.CheckServiceProductInContainer(Quote, Product, 'SC_GN_AT_Models_Scope_Cont','Service_Product',crow['Service_Product'])
                    if ret_v==False: #check whether PY SP is configured
                        crow['Error_Message']=crow['Service_Product']+' Service Product is not configured in the module.'
                        crow['CY_Service_Product']=None
                    else:
                        crow['CY_Service_Product']=crow['Service_Product']
                        crow['Error_Message']=None
                else:#Inactive previous year service product
                    #validate replacement service product
                    if crow['CY_Service_Product'] not in (None,''):
                        if crow['CY_Service_Product'] in chk_dupl_list: 
                            crow['Error_Message']=crow['CY_Service_Product']+' Service Product cannot be added multiple times as a replacement product.'
                            Trace.Write(crow['Service_Product']+'::'+crow['CY_Service_Product']+'::'+str(chk_dupl_list)+':: duplicates')
                        else:
                            Trace.Write(crow['Service_Product']+'::'+crow['CY_Service_Product']+'::'+str(chk_dupl_list)+':: No duplicates')
                            ret_v=gsup.CheckServiceProductInContainer(Quote, Product, 'SC_GN_AT_Models_Scope_Cont','Service_Product',crow['CY_Service_Product']) #quote, product, Container name, column name, CY SP value
                            #check CY service product/Replaced SP configured in the product
                            if ret_v==False:
                                crow['Error_Message']=crow['CY_Service_Product']+' Service Product is not configured in the module.'
                            else:
                                #chk_dupl_list.append(crow['CY_Service_Product'])
                                crow['Error_Message']=None
                    else:
                        crow['Error_Message']='Previous Year Service Product '+crow['Service_Product'] + ' is inactive. Please Choose the CY Service Product(Replacement Product) in Comparison Summary'
            if crow['CY_Service_Product'] not in (None,''):
                chk_dupl_list.append(crow['CY_Service_Product'])