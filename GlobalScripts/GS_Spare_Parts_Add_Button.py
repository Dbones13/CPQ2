sparePart=Product.Attr('Spare_Parts_Search').GetValue()
if sparePart and Product.GetContainerByName('Spare_Parts').Rows.Count <= 500:
    partName = SqlHelper.GetFirst("Select DESCRIPTION from MIGRATION_SPARE_PARTS where MODELNUMBER = '{0}'".format(sparePart)).DESCRIPTION
    sparePartsCont = Product.GetContainerByName('Spare_Parts')
    row = sparePartsCont.AddNewRow()
    Product.Attributes.GetByName('IncompleteSpareParts').AssignValue(str(False))
    row['Spare_Parts_Part_Number'] = sparePart
    row['Spare_Parts_Part_Number_Description'] = partName