msidContainer = Product.GetContainerByName("Migration_MSID_Selection_Container")
#Product.Attr("PERF_ExecuteScriptsLabor").AssignValue("Yes")

for row in msidContainer.Rows:
    msidProduct = row.Product
    msidProduct.Attr("PERF_ExecuteScriptsLabor").AssignValue('Yes')
    row.ApplyProductChanges()
    msidProduct.ApplyRules()
    msidProduct.Attr("PERF_ExecuteScriptsLabor").AssignValue('No')
    row.ApplyProductChanges()
