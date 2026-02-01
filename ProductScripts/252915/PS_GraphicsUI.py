from GS_MigrationGraphicsUI import getgraphicsMigrationUI 

def getAttributeValue(Name):
    return Product.Attr(Name).GetValue()
def getContainer(Name):
    return Product.GetContainerByName(Name)
def getFloat(Var):
    if Var:
        return float(Var)
    return 0


selectedProducts = list()
for row in getContainer("MSID_Product_Container").Rows:
    selectedProducts.append(row["Product Name"])

if 'Graphics Migration' in selectedProducts and getAttributeValue("MIgration_Scope_Choices") not in ["HW/SW"]:
    Ds,Dm,Dc,Ss,Sm,Sc,Fs,Fm,Fc,Fvc,shape,facePlates = getgraphicsMigrationUI(Product) 
    graphicCon = getContainer("Graphics_Migration_Displays_Shapes_Faceplates")
    if graphicCon.Rows.Count == 2:
        row1 = graphicCon.Rows[0]
        row2 = graphicCon.Rows[1]
        flagSum = 0
        sumColumn = {"Number_of_Simple_Displays":str(Ds),"Number_of_Medium_Displays":str(Dm),"Number_of_Complex_Displays":str(Dc),"Number_of_Simple_Custom_Shapes":str(Ss),"Number_of_Medium_Custom_Shapes":str(Sm),"Number_of_Complex_Custom_Shapes":str(Sc),"Number_of_Simple_Custom_Faceplates":str(Fs),"Number_of_Medium_Custom_Faceplates":str(Fm),"Number_of_Complex_Custom_Faceplates":str(Fc),"Number_of_Very_Complex_Custom_Faceplates":str(Fvc)}
        for key in sumColumn:
            flagSum += getFloat(row1[key])
        for key in sumColumn:
            row2[key] = sumColumn[key]
            if int(flagSum) == 0:
                row1[key] = sumColumn[key]
        row2["Total_Number_of_Custom_Shapes"] = str(shape)
        row2["Total_Number_of_Custom_Faceplates"] = str(facePlates)