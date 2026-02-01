R2QFlag = Quote.GetCustomField('R2QFlag').Content
if R2QFlag:
    parameters = Quote.GetGlobal('Virtualization_Mapping_Param')
    if parameters:
        Quote.SetGlobal('VrtMappingFlag', 'True')
        vrt_list = eval(parameters)
        selectedProducts = Product.GetContainerByName('CONT_MSID_SUBPRD')
        for selectedRow in selectedProducts.Rows:
            if selectedRow['Selected_Products'] == 'Virtualization System Migration':
                for child_attr in selectedRow.Product.Attributes:
                    ScriptExecutor.ExecuteGlobal('VRT_CHECKING',{'msidproduct':child_attr.Product,'vrt_list':vrt_list})
                    break
        #Quote.SetGlobal('Virtualization_Mapping_Param', '')