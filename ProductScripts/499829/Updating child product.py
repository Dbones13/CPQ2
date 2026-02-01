con = Product.GetContainerByName("Trace_Software_License_Configuration_transpose")
if con.Rows.Count ==2:

	row1 = con.Rows[1]
	row1.Product.Attr("Trace_software_support_gray").AssignValue("2")
	row1.ApplyProductChanges()
#attribute_1 = row1.GetColumnByName("Trace_Software_Years_of_Support").ReferencingAttribute
#for value in attribute_1.Values:
#    if value.Display in ('0'):
#        value.Allowed = False