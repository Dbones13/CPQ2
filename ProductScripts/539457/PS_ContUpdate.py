#producthiddenContainer = Product.GetContainerByName('MSID_Product_Container_Virtualization_hidden')
#if producthiddenContainer.Rows.Count == 0:
	#newRowVir = producthiddenContainer.AddNewRow('Virtualization_System_Migration_cpq')
#newRowVir['Product Name'] = "Virtualization System"
#newRowVir.ApplyProductChanges()
RootProduct = Product.ParseString('<*CTX ( Product.RootProduct.SystemId )*>')
if Product.Name == 'Virtualization System Migration' and RootProduct != "Migration_cpq":
	msid_scope = Product.Attr('Scope').GetValue()
	msid_scope = msid_scope if msid_scope else Session["Scope"]
	#Trace.Write("scope"+Session["Scope"])
	Product.Attr('MIgration_Scope_Choices').SelectDisplayValue(msid_scope)
	Trace.Write("migration"+str(Product.Attr('MIgration_Scope_Choices').GetValue()))