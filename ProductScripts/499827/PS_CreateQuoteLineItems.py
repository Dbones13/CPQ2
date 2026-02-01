def selectBOMItems(contObject):
    update=False
    if contObject is not None:
        if contObject.Rows.Count > 0:
            for row in contObject.Rows:
                Trace.Write("Applying qty and select" + row["partnumber"])
                try:
                    if row.IsSelected == False and int(row["Final_Quantity"])>0:
                        row.IsSelected = True
                        row.Calculate()
                        update=True
                    if row.IsSelected == True and int(row["Final_Quantity"])==0:
                        row.IsSelected = False
                        update=True
                    if int(row["Final_Quantity"]) !=  row.Product.Attr('ItemQuantity').GetValue() and int(row["Final_Quantity"])>0:
                        row.Product.Attr('ItemQuantity').AssignValue(row["Final_Quantity"])
                        update=True
                except:
                    Trace.Write("Applying qty and select error" + row["partnumber"])
    return update
rL0isUpdated=False
rL1isUpdated=False
rL2isUpdated=False
rL3isUpdated=False
for rL0 in Product.GetContainerByName("CE_SystemGroup_Cont").Rows:
    for rL1 in rL0.Product.GetContainerByName("CE_System_Cont").Rows:
        if rL1.Product.Name == 'Terminal Manager':
            isUpdated = selectBOMItems(rL1.Product.GetContainerByName("Terminal_PartSummary_Cont"))
            if isUpdated == True:
                rL1isUpdated=True
                rL0isUpdated=True
        if rL1.Product.Name == 'Measurement IQ System':
            isUpdated = selectBOMItems(rL1.Product.GetContainerByName("MIQ_PartSummary_Cont"))
            if isUpdated == True:
                rL1isUpdated=True
                rL0isUpdated=True
        if rL1.Product.Name == 'ControlEdge PCD System':
            for rL2 in rL1.Product.GetContainerByName("PCD_Cont").Rows:
                isUpdated = selectBOMItems(rL2.Product.GetContainerByName("PCD_PartSummary_Cont"))
                if isUpdated == True:
                    rL2isUpdated=True
                    rL1isUpdated=True
                    rL0isUpdated=True
        if rL1.Product.Name == 'Experion HS System':
            for rL2 in rL1.Product.GetContainerByName("Experion_HS_Cont").Rows:
                isUpdated = selectBOMItems(rL2.Product.GetContainerByName("Experion_HS_PartSummary_Cont"))
                if isUpdated == True:
                    rL2isUpdated=True
                    rL1isUpdated=True
                    rL0isUpdated=True
        if rL1.Product.Name == 'PlantCruise System':
            for rL2 in rL1.Product.GetContainerByName("PlantCruise_Cont").Rows:
                isUpdated = selectBOMItems(rL2.Product.GetContainerByName("PlantCruise_PartSummary_Cont"))
                if isUpdated == True:
                    rL2isUpdated=True
                    rL1isUpdated=True
                    rL0isUpdated=True
        if rL1.Product.Name == 'ARO, RESS & ERG System':
            for rL2 in rL1.Product.GetContainerByName("ARO_System_Group_Cont").Rows:
                isUpdated = selectBOMItems(rL2.Product.GetContainerByName("ARO_Sys_Grp_Part_Summery_Cont"))
                if isUpdated == True:
                    rL2isUpdated=True
                    rL1isUpdated=True
                    rL0isUpdated=True
        if rL1.Product.Name == 'HC900 System':
            for rL2 in rL1.Product.GetContainerByName("HC900_Cont").Rows:
                isUpdated = selectBOMItems(rL2.Product.GetContainerByName("HC900_PartSummary_Cont"))
                if isUpdated == True:
                    rL2isUpdated=True
                    rL1isUpdated=True
                    rL0isUpdated=True
        if rL1.Product.Name == 'Field Device Manager':
            for rL2 in rL1.Product.GetContainerByName("FDM_System_Group_Cont").Rows:
                isUpdated = selectBOMItems(rL2.Product.GetContainerByName("FDM_PartSummary_Cont"))
                if isUpdated == True:
                    rL2isUpdated=True
                    rL1isUpdated=True
                    rL0isUpdated=True
        if rL1.Product.Name == 'C300 System':
            for rL2 in rL1.Product.GetContainerByName("Series_C_Control_Groups_Cont").Rows:
                isUpdated = selectBOMItems(rL2.Product.GetContainerByName("Series_C_CG_Part_Summary_Cont"))
                if isUpdated == True:
                    rL2isUpdated=True
                    rL1isUpdated=True
                    rL0isUpdated=True
                for rL3 in rL2.Product.GetContainerByName("Series_C_Remote_Groups_Cont").Rows:
                    isUpdated = selectBOMItems(rL3.Product.GetContainerByName("Series_C_RG_Part_Summary_Cont"))
                    if isUpdated == True:
                        rL3.ApplyProductChanges()
                        rL2isUpdated = True
                        rL1isUpdated = True
                        rL0isUpdated = True
        if rL1.Product.Name == 'Experion Enterprise System':
            for rL2 in rL1.Product.GetContainerByName("Experion_Enterprise_Cont").Rows:
                isUpdated = selectBOMItems(rL2.Product.GetContainerByName("Exp_Ent_Grp_Part_Summary_Cont"))
                if isUpdated == True:
                    rL2isUpdated=True
                    rL1isUpdated=True
                    rL0isUpdated=True
                for rL3 in rL2.Product.GetContainerByName("List of Locations/Clusters/Network Groups").Rows:
                    isUpdated = selectBOMItems(rL3.Product.GetContainerByName("Location_Cluster_Part_Summary_Cont"))
                    if isUpdated == True:
                        rL3.ApplyProductChanges()
                        rL2isUpdated = True
                        rL1isUpdated = True
                        rL0isUpdated = True
                if rL2isUpdated==True:
                    rL2.ApplyProductChanges()
                    rL2isUpdated = False
        if rL1isUpdated==True:
            rL1.ApplyProductChanges()
            rL1isUpdated = False
    if rL0isUpdated==True:
        rL0.ApplyProductChanges()
        rL0isUpdated = False