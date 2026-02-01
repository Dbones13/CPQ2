resp_arr = []
def getContainer(Name):
    return Product.GetContainerByName(Name)



cont=getContainer('FDM_Upgrade_Configuration')
if cont:
    for row in cont.Rows:
        resp_arr.append(row['FDM_Upgrade_Do_you_want_to_upgrade_this_FDM'])



ApiResponse = ApiResponseFactory.JsonResponse(resp_arr)