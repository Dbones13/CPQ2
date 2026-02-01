resp_arr = []
def getContainer(Name):
    return Product.GetContainerByName(Name)

cont=getContainer('FDM_Upgrade_General_questions')
if cont:
    for row in cont.Rows:
        resp_arr.append(row['FDM_Upgrade_Select_desired_FDM_release'])

ApiResponse = ApiResponseFactory.JsonResponse(resp_arr)