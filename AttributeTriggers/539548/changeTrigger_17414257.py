contObj = Product.GetContainerByName('CONT_MSID_SUBPRD')
val = Product.Attr('MSID_Future_TPN_Release').GetValue()

for row in contObj.Rows:
    try:
        row['MSID_Future_TPN_Release'] = val
        row.Product.Attr('MSID_Future_TPN_Release').SelectValue(val)
        row.ApplyProductChanges()
    except Exception as e:
        Trace.Write('Error'+str(e))
contObj.Calculate()