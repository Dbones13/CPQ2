exeperionEntContainer = Product.GetContainerByName('Experion_Enterprise_Cont')
if exeperionEntContainer.Rows.Count == 0:
    new_row = exeperionEntContainer.AddNewRow(False)
    new_row.Product.Attr('MIB Configuration Required?').AssignValue(Product.Attr('MIB Configuration Required?').GetValue())
    new_row.ApplyProductChanges()
else:
    for row in exeperionEntContainer.Rows:
        row.Product.Attr('MIB Configuration Required?').AssignValue(Product.Attr('MIB Configuration Required?').GetValue())
        row.ApplyProductChanges()
exeperionEntContainer.Calculate()