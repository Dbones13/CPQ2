from GS_R2Q_Product_Attribute_ContColms import MigrationProductsAttributesContainerColumns as contAttrDrop
Quote.SetGlobal('VSFlag', 'True')
VSContainer = Product.GetContainerByName('Virtualization_System_WorkLoad_Cont')
for row in VSContainer.Rows:
    attr4 = row.GetColumnByName("Work_Load_Type").DisplayValue
    for attribute_name, allowed_key in contAttrDrop.VS_Attr.items():
        attr = row.GetColumnByName(attribute_name).ReferencingAttribute
        for value in attr.Values:
            value.Allowed = (value.Display == 'No' or attr4 in contAttrDrop.VS_Attr_values[allowed_key])
    row.Calculate()
#added code for https://honeywell.atlassian.net/browse/CXCPQ-108517
def ContColumnLableChange(Cont,column,Label):
    if Product.GetContainerByName(Cont).Rows:
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