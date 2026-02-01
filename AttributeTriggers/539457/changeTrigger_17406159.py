def getContainer(Name):
    return Product.GetContainerByName(Name)
count = int(Product.Attr("Virtualization_Number_of_Clusters_in_the_network").GetValue()) if Product.Attr('Virtualization_Number_of_Clusters_in_the_network').GetValue().isdigit() else 0
cont = getContainer("Virtualization_cluster_transpose")
rowCount = cont.Rows.Count

if rowCount < count:
    for i in range(rowCount,count):
        r = cont.AddNewRow(False)
    cont.Calculate()
elif rowCount > count:
    flag = 0
    for i in range(count,rowCount):
        flag += 1
        cont.DeleteRow(rowCount-flag)
    cont.Calculate()
#added code for https://honeywell.atlassian.net/browse/CXCPQ-108517
def ContColumnLableChange(Cont,column,Label):
    for i in Product.GetContainerByName(Cont).Rows:
        i.GetColumnByName(column).HeaderLabel=Label

columnDict={"Virtualization_cluster_transpose":["Virtualization_Number_of_A_VxRail_E660_Servers","Virtualization_Number_of_B_VxRail_E660_Servers"]
     }

labledict={"Virtualization_Number_of_A_VxRail_E660_Servers":"Number of Performance A Servers (0-9 per cluster)","Virtualization_Number_of_B_VxRail_E660_Servers":"Number of Performance B Servers (0-9 per cluster)"}

if Quote.GetCustomField('R2QFlag').Content !="Yes":
    for Key,values in columnDict.items():
        for value in values:
            Label = labledict[value]
            ContColumnLableChange(Key,value,Label)