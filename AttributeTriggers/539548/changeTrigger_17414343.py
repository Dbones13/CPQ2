contObj = Product.GetContainerByName('CONT_MSID_SUBPRD')
val = Product.Attr('MSID_Is_Switch_Configuration_in_Honeywell_Scope').GetValue()

for row in contObj.Rows:
    try:
        row['MSID_Is_Switch_Configuration_in_Honeywell_Scope'] = val
        row.Product.Attr('MSID_Is_Switch_Configuration_in_Honeywell_Scope').SelectValue(val)
        row.ApplyProductChanges()
    except Exception as e:
        Trace.Write('Error'+str(e))
contObj.Calculate()