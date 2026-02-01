def getContainer(Name):
    return Product.GetContainerByName(Name)

check = Product.ParseString('<*VALUE(Trace_Software_What_is_the_scope)*>')
con1 = getContainer("Trace_Software_License_Configuration_transpose")
if(check =="New License"):
    if con1.Rows.Count == 2:
    	con1.DeleteRow(1)
con.Calculate()