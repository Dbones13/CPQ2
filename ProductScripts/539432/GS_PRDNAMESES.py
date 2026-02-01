Session["ProductName"] = Session["ProductName"] if Session["ProductName"] else []
sessionval = Session["ProductName"]
prd_name = Product.Name
if prd_name not in sessionval:
    sessionval.append(prd_name)