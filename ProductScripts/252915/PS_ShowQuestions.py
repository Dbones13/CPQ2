from GS_MigrationLaborHoursModule import getRowData,getContainer

def hideColumn(container,Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format(container,Column))
    Product.ParseString('<*CTX( Container({}).Row(1).Column({}).Set() )*>'.format(container,Column))
def visibleColumn(container,Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format(container,Column))
def isHidden(container,Column):
    return Product.ParseString('<*CTX( Container({}).Column({}).GetPermission )*>'.format(container,Column)) == 'Hidden'

def setDefaultValue(container,column):
    ColumnSet1 = {"OPM_Does_the_customer_have_EBR_installed":"No","OPM_RESS_Server_configuration":"Physical","OPM_Select_RESS_platform_configuration":"HP DL360 G10","OPM_Additional_Memory_for_RESS_Server":"No","OPM_Additional_Hard_Disk_For_RESS_Server":"No"}
    Container = getContainer(Product,container)
    for row in Container.Rows:
        if column in ColumnSet1:
            row.GetColumnByName(column).SetAttributeValue(ColumnSet1[column])

rmsQue = getRowData(Product,"OPM_Basic_Information","OPM_Is_this_is_a_Remote_Migration_Service_RMS")
rmsQue1 = getRowData(Product,"OPM_Basic_Information","OPM_RESS_Migration_in_scope")
rmsQue2 = getRowData(Product,"OPM_Migration_platforms","OPM_RESS_Server_configuration")
rmsQue3 = getRowData(Product,"OPM_Migration_platforms","OPM_Select_RESS_platform_configuration")
Trace.Write("Working = "+str(rmsQue2))


if isHidden("OPM_Basic_Information","OPM_Does_the_customer_have_EBR_installed") and rmsQue == "Yes":
    visibleColumn("OPM_Basic_Information","OPM_Does_the_customer_have_EBR_installed")
    setDefaultValue("OPM_Basic_Information","OPM_Does_the_customer_have_EBR_installed")

if rmsQue1 == "Yes" and rmsQue2 == 'Physical' and isHidden("OPM_Migration_platforms","OPM_Additional_Hard_Disk_For_RESS_Server") and isHidden("OPM_Migration_platforms","OPM_Additional_Memory_for_RESS_Server") and (rmsQue3 == 'HP DL360 G10' or rmsQue3 == 'Dell R740XL'):
    Trace.Write("Working")
    visibleColumn("OPM_Migration_platforms","OPM_Additional_Hard_Disk_For_RESS_Server")
    setDefaultValue("OPM_Migration_platforms","OPM_Additional_Hard_Disk_For_RESS_Server")
    visibleColumn("OPM_Migration_platforms","OPM_Additional_Memory_for_RESS_Server")
    setDefaultValue("OPM_Migration_platforms","OPM_Additional_Memory_for_RESS_Server")