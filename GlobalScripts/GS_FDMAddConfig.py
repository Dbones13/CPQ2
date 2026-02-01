resp_arr = []
def getContainer(Name):
    return Product.GetContainerByName(Name)

cont=getContainer('FDM_Upgrade_Additional_Configuration')
if cont:
    for row in cont.Rows:
        resp_arr.append(row['FDM_Upgrade_Are_additional_components_required_for_this_FDM'])

ApiResponse = ApiResponseFactory.JsonResponse(resp_arr)