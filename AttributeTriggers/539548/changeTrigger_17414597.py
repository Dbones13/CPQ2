contObj = Product.GetContainerByName('CONT_MSID_SUBPRD')
Crate_Design = Product.Attr('MSID_Crate_Design').GetValue()

for row in contObj.Rows:
    try:
        row['MSID_Crate_Design'] = Crate_Design
        row.Product.Attr('MSID_Crate_Design').SelectValue(Crate_Design)
        row.ApplyProductChanges()
    except Exception as e:
        Trace.Write('Error'+str(e))
contObj.Calculate()