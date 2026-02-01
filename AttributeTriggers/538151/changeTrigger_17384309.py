productType = Product.Attr('SC_Product_Type').GetValue()
renewalCheck = Product.Attr('SC_Renewal_check').GetValue()
if ((productType == "Renewal" and  renewalCheck == 1) or productType != "Renewal"):
    #Refresh everything in enabled services in sesp.
    Product.Attr('#_of_independent_"areas"_enabledServicesModel').AssignValue('0.00')
    Product.Attr('#_l3_l4_file_move_licenses_enabledServicesModel').AssignValue('0.00')
    Product.Attr('Matrix License').AssignValue('0.00')
    EnableSelection_SESP = Product.Attr('EnableSelection_SESP').GetValue()
    if EnableSelection_SESP == '':
        Assets = Product.GetContainerByName('Asset_details_ServiceProd')
        Assets.Rows.Clear()
    Product.Attr('#_of_recommended_udc_servers_enabledServicesModel').AssignValue('0.00')
    Product.Attr("L3_L4_FILE_MOVER_ESSENTIAL_enabledServicesModel").AssignValue('0.00')
    #Product.Attr('EnabledServices_servprod').AssignValue('')
    Product.ResetAttr('EnabledServices_servprod')