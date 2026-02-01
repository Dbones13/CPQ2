sparePartCheck = 0
sparePartsCont = Product.GetContainerByName('Spare_Parts').Rows
for row in sparePartsCont:
    if row['Spare_Parts_Quantity'] == ''  or row['Spare_Parts_Quantity'] == None  or int(row['Spare_Parts_Quantity']) == 0 :
        sparePartCheck = sparePartCheck+ 1
if sparePartCheck > 0:
    Product.Attributes.GetByName('IncompleteSpareParts').AssignValue(str(False))
else:
    Product.Attributes.GetByName('IncompleteSpareParts').AssignValue(str(True))