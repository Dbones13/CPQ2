contObj = Product.GetContainerByName('CONT_MSID_SUBPRD')
val = Product.Attr('MSID_FEL_Data_Gathering_Required').GetValue()

for row in contObj.Rows:
    try:
        row['MSID_FEL_Data_Gathering_Required'] = val
        row.Product.Attr('MSID_FEL_Data_Gathering_Required').SelectValue(val)
        row.ApplyProductChanges()
    except Exception as e:
        Trace.Write('Error'+str(e))
contObj.Calculate()