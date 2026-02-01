def populateWEPModelScope(model,desc,cyQty,pyQty,unitPrice,unitCost,py_price,py_cost,tab):
    scweprow = sc_wep_cont.AddNewRow(False)
    scweprow["Model"] = model
    scweprow["Description"] = desc
    scweprow["CY_Quantity"] = cyQty
    scweprow["PY_Quantity"] = pyQty
    scweprow["unitPrice"] = unitPrice
    scweprow["unitCost"] = unitCost
    scweprow["PY_ListPrice"] = py_price
    scweprow["PY_CostPrice"] = py_cost
    scweprow["Tab"] = tab
    scweprow.Calculate()

sc_wep_cont = Product.GetContainerByName("SC_WEP_Models_Scope")
sc_wep_cont.Rows.Clear()

sc_module = Product.GetContainerByName("Service Contract Modules")
if sc_module.Rows.Count:
    for row in sc_module.Rows:
        if row["Module"] == "Workforce Excellence Program" and row.Product.Attr("SC_Product_Type").GetValue() == "Renewal":
            hif = row.Product.GetContainerByName("SC_WEP_Models_Scope_HIF")
            ifs = row.Product.GetContainerByName("SC_WEP_Models_Scope_IFS")
            halo = row.Product.GetContainerByName("SC_WEP_Models_Scope_Halo")
            training = row.Product.GetContainerByName("SC_WEP_Models_Scope_Training")
            tna = row.Product.GetContainerByName("SC_WEP_Models_Scope_TNA")
            wepList = [hif,ifs,halo,training,tna]
            for cont in wepList:
                if cont.Rows.Count:
                    for row in cont.Rows:
                        populateWEPModelScope(row["Model"],row["Description"],row["CY_Quantity"],row["PY_Quantity"],row["CY_UnitPrice"],row["CY_UnitCost"],row["PY_ListPrice"],row["PY_CostPrice"],cont.Name)