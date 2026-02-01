laborDetails=SqlHelper.GetList("select Labor , Service_Material from CT_HCI_PHD_LABORMATERIAL ")
ServicelaborDict={}
for lab in laborDetails:
    ServicelaborDict[lab.Service_Material]=lab.Labor
for mainRow in Product.GetContainerByName('HCI_PHD_Selected_Products').Rows:
    parentProduct=mainRow.Product

    labourFinalHrsDict={}
    containersLst=['HCI_PHD_EngineeringLabour','HCI_PHD_ProjectManagement','HCI_PHD_ProjectManagement2','HCI_PHD_AdditionalDeliverables']
    for conts in containersLst:
        contRows=parentProduct.GetContainerByName(conts).Rows
        for row in contRows:
            if row['Final Hrs'] and row['Eng']!='':
                if row['Eng'] not in labourFinalHrsDict.keys():
                    labourFinalHrsDict[row['Eng']] = float(row['Final Hrs'])
                else:
                    labourFinalHrsDict[row['Eng']] += float(row['Final Hrs'])
    contRows=parentProduct.GetContainerByName('HCI_PHD_LabourProducts')
    #Trace.Write('Test11 '+str(labourFinalHrsDict))
    delRows=[]
    #if len(labourFinalHrsDict)==0:
    #    contRows.Clear()
    contRows.Clear()
    for labor in labourFinalHrsDict:
        laborDetails=SqlHelper.GetFirst("select Service_Material from CT_HCI_PHD_LABORMATERIAL where Labor='{}'".format(labor))
        if laborDetails:
            flg=0
            #for row in contRows.Rows:
            #    if row.Product.PartNumber==laborDetails.Service_Material:
            #        flg=1
            #        row.Product.Attr('ItemQuantity').AssignValue(str(labourFinalHrsDict[labor]))
            #    if ServicelaborDict[row.Product.PartNumber] not in labourFinalHrsDict.keys():
            #        #Trace.Write('Here2222')
            #        delRows.append(row.RowIndex)
            if flg==0:
                #Trace.Write('Here1111')
                row=contRows.AddNewRow(laborDetails.Service_Material,False)
                row.Product.Attr('ItemQuantity').AssignValue(str(labourFinalHrsDict[labor]))
    contRows.Calculate()
    #delRows.reverse()
    #for rowindx in delRows:
    #    contRows.DeleteRow(rowindx)
    #contRows=parentProduct.GetContainerByName('HCI_PHD_LabourProducts').Rows
    mainRow.ApplyProductChanges()