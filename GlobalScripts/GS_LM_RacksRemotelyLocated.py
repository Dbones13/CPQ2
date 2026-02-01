resp_arr = []
def getContainer(Name):
    return Product.GetContainerByName(Name)

cont=getContainer('LM_to_ELMM_ControlEdge_PLC_Cont')
if cont:
    for row in cont.Rows:
        resp_arr.append(row['LM_Are_the_IO_Racks_remotely_located'])

ApiResponse = ApiResponseFactory.JsonResponse(resp_arr)