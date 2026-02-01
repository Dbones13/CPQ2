#PS_SESP_CompSummary_Validation
Product.Attr('SC_SP_Mismatch').AssignValue("0")
Pmessage=None
CSContainer = Product.GetContainerByName("ComparisonSummary")
SC_Service_Product = Product.Attr("SC_Service_Product").GetValue()
SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if CSContainer.Rows.Count>0 and SC_Product_Type == "Renewal":
    for crow in CSContainer.Rows:
        if crow.IsSelected: #scope removal selected
            if crow.GetColumnByName('CY_Service_Product').Value != SC_Service_Product:
                crow.GetColumnByName('CY_Service_Product').Value=None
        else:#Inscope
            if crow['PY_Service_Prod_Status']=='Active': #active previous year service product is configured
                if crow['Service_Product']!=SC_Service_Product: #check whether PY SP is configured
                    Pmessage=crow['Service_Product']+' Service Product is not configured in the SESP module.'
                    Product.Attr('SC_SP_Mismatch').AssignValue("1")
                    crow['CY_Service_Product']=None
                else:
                    crow['CY_Service_Product']=crow['Service_Product']
            else:#Inactive previous year service product
                #validate replacement service product
                if crow['CY_Service_Product'] not in (None,''):
                    #check CY service product/Replaced SP configured in the product
                    if crow['CY_Service_Product']!=SC_Service_Product:
                        Pmessage=crow['CY_Service_Product']+' Service Product is not configured in the SESP module.'
                        Product.Attr('SC_SP_Mismatch').AssignValue("1")
                        #changedRow.GetColumnByName('CY_Service_Product').Value=None
                else:
                    Pmessage='Please Choose the CY Service Product(Replacement Product) in SESP Comparison Summary'
                    Product.Attr('SC_SP_Mismatch').AssignValue("1")
if Pmessage is not None:
    if not Product.Messages.Contains(Pmessage):
        Product.Messages.Add(Pmessage)