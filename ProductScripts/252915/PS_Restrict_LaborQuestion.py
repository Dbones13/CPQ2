def getContainer(Name):
    return Product.GetContainerByName(Name)

def Hidden(attrname):
    Product.Attr(attrname).Access = AttributeAccess.Hidden

def Editable(attrname):
    Product.Attr(attrname).Access = AttributeAccess.Editable

Products=Product.Attr('MSID_Selected_Products').GetValue()
selectedProducts=set(Products.split('<br>'))

columnvisibilityDict = {"Regional_Migration_Principal_Efforts_Required": {'FSC to SM','OPM','EBR','TPS to Experion','ELCN','Orion Console','EHPM/EHPMX/ C300PM','EHPM HART IO','C200 Migration','Virtualization System'}}

for key,products in columnvisibilityDict.items():
    Prod = selectedProducts.intersection(products)
    if len(Prod) == 0:
        Hidden(key)
    else:
        Editable(key)
