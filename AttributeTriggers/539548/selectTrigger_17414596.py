contObj = Product.GetContainerByName('CONT_MSID_SUBPRD')
Crate_Type = Product.Attr('MSID_Crate_Type').GetValue()

for row in contObj.Rows:
    try:
        row['MSID_Crate_Type'] = Crate_Type
        row.Product.Attr('MSID_Crate_Type').SelectValue(Crate_Type)
        row.ApplyProductChanges()
    except Exception as e:
        Trace.Write('Error'+str(e))
contObj.Calculate()