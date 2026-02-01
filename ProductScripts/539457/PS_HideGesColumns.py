def getContainer(Name):
    return Product.GetContainerByName(Name)

def hideColumn(container,Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format(container,Column))
    Product.ParseString('<*CTX( Container({}).Row(1).Column({}).Set() )*>'.format(container,Column))

def visibleColumn(container,Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format(container,Column))

col_lst = ["GES Eng","GES Eng % Split","GES_Unit_Regional_Cost","GES_Regional_Cost","GES_ListPrice","GES_WTW_Cost","GES_MPA_Price"]

con = getContainer("Virtualization_Labor_Deliverable")
gesLocation = Product.Attr('Virtualization_Ges_Location').GetValue()
if gesLocation == "None" or gesLocation == "":
    for col in col_lst:
        hideColumn("Virtualization_Labor_Deliverable",col)
else:
    for col in col_lst:
        visibleColumn("Virtualization_Labor_Deliverable",col)