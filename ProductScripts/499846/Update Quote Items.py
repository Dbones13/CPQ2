PSkidCont = Product.GetContainerByName('PRODUCTIZED _SKID_BOM')
for row in PSkidCont.Rows:
    if row["Type"] !='H' and row["Type"] !='S':
        for i in Quote.MainItems:
            if (i.PartNumber==row["Part Number"] or i.QI_FME.Value==row["Part Number"]) and row["Part Number"]!='':
                i.QI_PSKID_Item_Flag.Value='Y'