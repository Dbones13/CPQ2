for item in Quote.MainItems:
    if item.QI_SparePartsFlag.Value == "Spare Part":
        item.Edit()
        rURL = '/configurator.aspx'
        WorkflowContext.RedirectToURL = rURL
        break
else:
    product = SqlHelper.GetFirst("select p.product_ID from Products p join product_versions pv on p.Product_ID = pv.Product_ID where System_ID = 'VFD_Spare_Parts_cpq' and pv.Is_Active = 1")
    if product is not None:
        activePID = product.product_ID
        rURL = '/configurator.aspx?pid=' + str(activePID)+ '&cid=3184'
        WorkflowContext.RedirectToURL = rURL
