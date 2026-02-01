from GS_CommonConfig import CL_CommonSettings as CS

def HDP_msid_count(cont, Product):
	if cont.Name == "SC_MSID_Container":
		count = 0
		for row in cont.Rows:
			if row.IsSelected == True:
				count += 1
		msidCount = int(Product.Attr('SC_Digital_Prime_MSID_Count').GetValue()) or 0
		if msidCount != count:
			Product.Attr('SC_Digital_Prime_MSID_Count').AssignValue(str(count))
			Product.Attr('SC_Num_of_MSID').AssignValue(str(count))

def CheckboxRelated(getselectAll, id):
    laborRows = None
    laborRows1 = None
    
    if Product.Name in CS.getLaborContainer:
        containers = CS.getLaborContainer[Product.Name]
        if isinstance(containers, dict):
            if id in containers:
                if isinstance(containers[id], list):
                    laborRows = Product.GetContainerByName(containers[id][0])
                    laborRows1 = Product.GetContainerByName(containers[id][1])
                elif isinstance(containers[id], dict):
                    laborRows = Product.GetContainerByName(containers[id][Product.Attr('SC_Product_Type').GetValue()])
                else:
                    laborRows = Product.GetContainerByName(containers[id])
            else:
                Trace.Write("Error: Param.ID is Missing/Invalid")
        else:
            Trace.Write("Error: Product doesn't have configured in dictionary")

    if getselectAll:
        laborRows.MakeAllRowsSelected()
        if laborRows1:
            laborRows1.MakeAllRowsSelected()
    else:
        for row in laborRows.Rows:
            row.IsSelected = False
        if laborRows1:
            for row1 in laborRows1.Rows:
                row1.IsSelected = False
    laborRows.Calculate()
    if laborRows1:
        laborRows1.Calculate()

    try:
        if Product.Name in('Solution Enhancement Support Program','Honeywell Digital Prime','Experion Extended Support - RQUP ONLY'):
            eval( CS.getLaborContainer[Product.Name]['CalculateAndTrigger'] )
    except Exception as e:
        Log.Info("Exception in executing script: {"+str(e)+'}')

    return laborRows.Name
    # Continue handling non-selectAll case as necessary...

def HCI_checkall(getselectAll,id):
	Trace.Write(str(['--->',getselectAll,id]))
	for row in Product.GetContainerByName(id).Rows:
		if row['Deliverable']!='Total':
			if (id =='HCI_PHD_EngineeringLabour' and row['Header']!='Header') or id !='HCI_PHD_EngineeringLabour':
				if getselectAll:
					row.IsSelected = True
				else:
					row.IsSelected = False
	return id

action = Param.Action
id = Param.id if Param.id else 'checkAll'
if action == 'CheckboxRelated':
	getselectAll = Param.getselectAll
	ApiResponse = ApiResponseFactory.JsonResponse(CheckboxRelated(getselectAll, id))
elif action == 'HCI_selectall':
	getselectAll = Param.getselectAll
	ApiResponse = ApiResponseFactory.JsonResponse(HCI_checkall(getselectAll, id))