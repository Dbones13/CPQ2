value_to_disable = []
if Product.PartNumber == 'OPM':
    lcn_flag = Product.GetContainerByName('OPM_Basic_Information').Rows[0].GetColumnByName('OPM_Is_the_Experion_System_LCN_Connected').Value
    if lcn_flag == 'Yes':
        value_to_disable.extend(['DELL T160 MLK','DELL R260 MLK','DELL R360 MLK'])
ApiResponse = ApiResponseFactory.JsonResponse({"value_to_disable":value_to_disable})