resp_arr = []
def getContainer(Name):
    return Product.GetContainerByName(Name)
attr_visible = dict()
attr_defn= SqlHelper.GetFirst("select STANDARD_ATTRIBUTE_CODE from Attribute_defn where System_Id='LM_to_ELMM_ControlEdge_PLC_Cont_cpq'")

sql_attr= SqlHelper.GetFirst("select PA_ID from Product_Attributes where STANDARD_ATTRIBUTE_CODE= {}".format(attr_defn.STANDARD_ATTRIBUTE_CODE))


cont=getContainer('LM_to_ELMM_ControlEdge_PLC_Cont')
if cont:
    resp_arr.append(str(sql_attr.PA_ID)+'_2_')
    for row in cont.Rows:
        resp_arr.append(row['LM_do_you_have_additional_space_in_the_cabinet_room_to_mount_the_CE_System'])

ApiResponse = ApiResponseFactory.JsonResponse(resp_arr)