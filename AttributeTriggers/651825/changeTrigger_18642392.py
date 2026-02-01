ioFamilyType = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
controllerType = Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
remoteGroupCont = Product.GetContainerByName('Series_C_Remote_Groups_Cont')

if ioFamilyType == 'Series C':
    if remoteGroupCont and remoteGroupCont.Rows.Count > 0:
        for row in remoteGroupCont.Rows:
            row.Product.Attr('C300_RG_UPC_CNM').SelectDisplayValue('No CNM')
            row.Product.Attr('C300_RG_UPC_FTA').SelectDisplayValue('No Treatment')
            row.Product.Attr('SerC_RG_Cabinet_Base_(Plinth)').SelectDisplayValue('No')
            row.Product.Attr('SerC_RG_Cabinet_Thermostat_Default').SelectDisplayValue('No')
            row.Product.Attr('SerC_RG_Cabinet_Light_Default').SelectDisplayValue('No')

    if controllerType == 'C300 CEE':
        if remoteGroupCont and remoteGroupCont.Rows.Count > 0:
            for row in remoteGroupCont.Rows:
                row.Product.Attr('C300_RG_UPC_Fiber_Optic_Extender').SelectDisplayValue('Single Mode x2')
                row.Product.Attr('C300_RG_UPC_CN100_IO_HIVE').SelectDisplayValue('None')
    elif controllerType == 'CN100 CEE':
        if remoteGroupCont and remoteGroupCont.Rows.Count > 0:
            for row in remoteGroupCont.Rows:
                row.Product.Attr('C300_RG_UPC_Controlled_IO_License_Count').SelectDisplayValue('240 IO Control')