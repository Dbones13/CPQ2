CE_Cont=Product.GetContainerByName('R2Q CE_System_Cont').Rows
def nestedchild(childproduct,ProdCount,attrlist,smList):
    count=0
    for childattr in childproduct.Attributes:
        if childattr.DisplayType == 'Container' and childattr.Name in ['Series_C_Control_Groups_Cont', 'Series_C_Remote_Groups_Cont','SM_ControlGroup_Cont','UOC_ControlGroup_Cont','UOC_RemoteGroup_Cont','HC900_Cont','Scada_CCR_Unit_Cont','PLC_ControlGroup_Cont','PLC_RemoteGroup_Cont'] and childattr.Name not in attrlist:
                childcontainerRows = childproduct.GetContainerByName(childattr.Name).Rows
                if childproduct.Name in ['R2Q Safety Manager ESD','R2Q Safety Manager FGS'] and childproduct.Name not in smList:#alieas product having same attribute name
                    count += childcontainerRows.Count
                    smList.append(childproduct.Name)
                else:
                    count += childcontainerRows.Count
                    attrlist.append(childattr.Name)
                if childcontainerRows.Count > 0:
                    for Childrow in childcontainerRows:
                        for attr in Childrow.Product.Attributes:
                            if attr.DisplayType == 'Container' and attr.Name in ['Series_C_Remote_Groups_Cont','SM_RemoteGroup_Cont','UOC_RemoteGroup_Cont','PLC_RemoteGroup_Cont']:
                                attrlist.append(attr.Name)
                                count += Childrow.Product.GetContainerByName(attr.Name).Rows.Count
    return count
def extractProductContainer(ProdCount, product):
    count=0
    smList=[]
    prodlist=[]
    containerRows = product.GetContainerByName('R2Q CE_System_Cont').Rows
    if containerRows.Count > 0:
        for contanierRow in containerRows:
            for col in containerRows:
                if col['Selected_Products'] not in ['HC900 System','R2Q C300 System','R2Q 3rd Party Devices/Systems Interface (SCADA)','R2Q Safety Manager ESD','R2Q Safety Manager FGS','R2Q ControlEdge UOC System','R2Q ControlEdge PLC System'] and col['Selected_Products'] not in prodlist:
                    ProdCount +=1
                    prodlist.append(col['Selected_Products'])
            count +=nestedchild(contanierRow.Product,ProdCount,prodlist,smList)
    prodCount=count+ProdCount
    return prodCount
def extractProductcount(ProdCount,Product):
    prodCount=0
    attributelist=["R2Q CE_System_Cont"]
    for attr in Product.Attributes:
        if attr.DisplayType == 'Container' and attr.Name in attributelist:
            prodCount = extractProductContainer(ProdCount, Product)
    return prodCount
if CE_Cont.Count >0:
    ProdCount=0
    ProdCount=extractProductcount(ProdCount,Product)
    #Trace.Write("Fanal Prod R2Q Prod Count : "+str(ProdCount))
    Product.Attr('R2Q_ProductCount').AssignValue(str(ProdCount))