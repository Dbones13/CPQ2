cont = Product.GetContainerByName('CE_System_Cont')
for row in cont.Rows:
    if row.Product.Name == 'Experion Enterprise System':
        row.Product.Attr("MIB Configuration Required?").SelectValue( Product.Attr('MIB Configuration Required?').GetValue())
        row.Calculate()
cont.Calculate()