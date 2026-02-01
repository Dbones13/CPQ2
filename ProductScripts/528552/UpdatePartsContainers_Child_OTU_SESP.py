def insertParts(sysName,containerName):
	container = Product.GetContainerByName(containerName)
	if container.Rows.Count == 0:
		partQuery = SqlHelper.GetList("select Part_Number from SC_CT_OTU_SYSTEM_PARTS where System_Name = '"+sysName+"'")
		for part in partQuery:
			row = container.AddNewRow(False)
			row['Part Number'] = part.Part_Number
def makeAttReadOnly(attName):
    Product.Attr(attName).Access = AttributeAccess.ReadOnly
#################### Inseting Parts in to Containers ##########################
containerDict = {"EOP":"PartNum_EOPC_OTU_SESP","OTS":"PartNum_OTSC_OTU_SESP","HS":"ModelNum_HSC_OTU_SESP","Experion":"PartNum_EXPC_OTU_SESP","ESVT":"PartNum_ESTVC_OTU_SESP"}
for sysName,containerName in containerDict.items():
	insertParts(sysName,containerName)
####################    Maikng attributes ReadOnly   ##########################
"""readOnlyAttList = SqlHelper.GetList("select Property_Name from SC_CT_OTU_PROPERTIES where Access_Level = 'ReadOnly'")
for attName in readOnlyAttList:
    makeAttReadOnly(attName.Property_Name)"""