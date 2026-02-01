sparePartCabinet = dict()
for attr in Product.Attr('Spare_Parts_Cabinets_Configured').Values:
    sparePartCabinet[attr.UserInput] = attr.Quantity
productMapping = {"Server Cabinet":"Server_Cabinet_cpq", "Series C Cabinet" : "Series_C_Cabinet_cpq", "SM Chassis Cabinet":""}
qty = all(x == 0 for x in sparePartCabinet.values())
if not qty:
    sparePartCabinetCont = Product.GetContainerByName('MSID_Spare_Parts_Container')
    for k in sparePartCabinet:
        if sparePartCabinet[k] > 0:
            row=sparePartCabinetCont.AddNewRow(productMapping[k])
            row.Product.Attr('ItemQuantity').AssignValue(str(sparePartCabinet[k]))
            row['Qty'] = str(sparePartCabinet[k])
            row.Calculate()
    sparePartCabinetCont.Calculate()