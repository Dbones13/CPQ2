def getContainer(containerName):
     return Product.GetContainerByName(containerName)
res = []
colsToHide = []
try:
    opmBasic = getContainer("OPM_Basic_Information")
    row = opmBasic.Rows[0]
    hwReplaceNeeded = row["OPM_Servers_and_Stations_HW_replace_needed"] == 'Yes'
    lcnConnected = row["OPM_Is_the_Experion_System_LCN_Connected"] == 'Yes'

    if(not hwReplaceNeeded):
        colsToHide=['1','2','3','4','5','6','7','8','9','10']
    elif(not lcnConnected):
        colsToHide = ['2','3','5','6']
    attrId = Product.Attr('OPM_Node_Configuration').Id
    nodeConfig = getContainer("OPM_Node_Configuration")
    for id in colsToHide:
        res.append("#{}_{}_2".format(attrId , id))
    for row in nodeConfig.Rows:
        if row.RowIndex == 2:
            for col in row.Columns:
                if str(col.Rank) in colsToHide:
                    row[col.Name] = "0"
except:
    pass
ApiResponse = ApiResponseFactory.JsonResponse(res)