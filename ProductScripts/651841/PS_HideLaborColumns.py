def getContainer(Name):
    return Product.GetContainerByName(Name)

def hideColumn(container,Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format(container,Column))
    Product.ParseString('<*CTX( Container({}).Row(1).Column({}).Set() )*>'.format(container,Column))

def visibleColumn(container,Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format(container,Column))

col_lst = ["GES Eng","GES Eng % Split","GES_Unit_Regional_Cost","GES_Regional_Cost","GES_ListPrice","GES_WTW_Cost","GES_MPA_Price"]
con = getContainer("PLC_Labour_Details")

for row in con.Rows:
    Trace.Write(row["PLC_Ges_Location"])
    if row["PLC_Ges_Location"] in  ("None",""):
        for col in col_lst:
            hideColumn("CE PLC Engineering Labor Container",col)
    else:
        for col in col_lst:
            visibleColumn("CE PLC Engineering Labor Container",col)