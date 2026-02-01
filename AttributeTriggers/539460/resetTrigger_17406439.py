NoOfMig = Product.Attr('xPM_NIMsconf').GetValue()
Trace.Write("no of mig" +str(NoOfMig))
if NoOfMig == '' or NoOfMig == '0':
	Product.Attr('xPM_NIMsconf').AssignValue(str(0))
	Product.GetContainerByName('ENB_Migration_Config_Cont').Rows.Clear()