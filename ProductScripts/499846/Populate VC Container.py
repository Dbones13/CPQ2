def PopulateChildProduct(containerRow):
        containerRow.Product.Attributes.GetByName("Pskid Part Number").AssignValue(str(containerRow["Part Number"]))
        containerRow.Product.Attributes.GetByName("Pskid FME").AssignValue(str(containerRow["FME"]))
        containerRow.Product.Attributes.GetByName("Pskid Part Description").AssignValue(str(containerRow["Part Description"]))
        containerRow.Product.Attributes.GetByName("Pskid Item Qty").AssignValue(str(containerRow["Qty"]))
        containerRow.Product.Attributes.GetByName("Pskid Unit Cost").AssignValue(containerRow["Unit Cost"])
        containerRow.Product.Attributes.GetByName("Pskid Unit List Price").AssignValue(str(containerRow["Unit List Price"]))
        containerRow.ApplyProductChanges()


def PopulateSkidVCCon(partNumber, pfme,partDesc, pQty, punitCost,punitListPrice):
    try:
        Pskid_VC_Con = Product.GetContainerByName("PRODUCTIZED_SKID_VC_Cont")
        containerRow = Pskid_VC_Con.AddNewRow('Productized_Skid_Quote_Item_cpq')
        containerRow["Part Number"] = str(partNumber)
        containerRow["FME"] = str(pfme)
        containerRow["Part Description"] = str(partDesc)
        containerRow["Qty"]     = str(pQty)
        containerRow["Unit Cost"]        = str(punitCost)
        containerRow["Unit List Price"] = str(punitListPrice)
        containerRow.ApplyProductChanges()
        PopulateChildProduct(containerRow)
        containerRow.Calculate()
        
        
        
    except Exception, e:
        Trace.Write('Error while populating PRODUCTIZED_SKID_VC_Cont')
        
skidCon = Product.GetContainerByName("PRODUCTIZED _SKID_BOM")
Pskid_VC_Con = Product.GetContainerByName("PRODUCTIZED_SKID_VC_Cont")
Pskid_VC_Con.Rows.Clear()

for Vrow in skidCon.Rows:
    if str(Vrow['Type'])=='VC' and  str(Vrow['Error Message'])=='' and str(Vrow['Part Number'])!='':
        lv_fme=str(Vrow['Part Number'])
        if lv_fme[0]=='Y': # Get partNumber from FME
            lv_Pnumber=lv_fme[1:lv_fme.find('-')]
        else:
            lv_Pnumber=lv_fme[0:lv_fme.find('-')]
        PopulateSkidVCCon(lv_Pnumber, lv_fme,str(Vrow['Part Description']),str(Vrow['Qty']), str(Vrow['Unit Cost']),str(Vrow['Unit List Price']))
    if str(Vrow['Type'])=='CP' and  str(Vrow['Error Message'])=='' and str(Vrow['Part Number'])!='': #Populate simple materials CXCPQ-47392
        lv_Pnumber=str(Vrow['Part Number'])
        PopulateSkidVCCon(lv_Pnumber, '',str(Vrow['Part Description']),str(Vrow['Qty']), str(Vrow['Unit Cost']),str(Vrow['Unit List Price']))