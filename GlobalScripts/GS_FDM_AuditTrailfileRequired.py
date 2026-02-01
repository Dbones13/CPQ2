resp_arr = []
def getContainer(Name):
    return Product.GetContainerByName(Name)
attr_visible = dict()
attr_defn= SqlHelper.GetFirst("select STANDARD_ATTRIBUTE_CODE from Attribute_defn where System_Id='FDM_Upgrade_Additional_Configuration_cpq'")
sql_attr= SqlHelper.GetFirst("select PA_ID from Product_Attributes where STANDARD_ATTRIBUTE_CODE= {}".format(attr_defn.STANDARD_ATTRIBUTE_CODE))

cont=getContainer('FDM_Upgrade_Additional_Configuration')
if cont:
    resp_arr.append(str(sql_attr.PA_ID)+'_3_')
    for row in cont.Rows:
        resp_arr.append(row['FDM_Upgrade_Audit_trail_file_required'])

ApiResponse = ApiResponseFactory.JsonResponse(resp_arr)