resp_arr = []
def getContainer(Name):
    return Product.GetContainerByName(Name)



cont=getContainer('FDM_Upgrade_Hardware_to_host_FDM_Server')
if cont:
    for row in cont.Rows:
        resp_arr.append(row['FDM_Upgrade_Is_HW_required_for_this_FDM'])



ApiResponse = ApiResponseFactory.JsonResponse(resp_arr)