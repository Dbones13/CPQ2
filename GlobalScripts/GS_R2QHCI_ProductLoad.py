#Trace.Write('R2Q HCI Module')
def hideContainerColumns(cont,contColumnList,TagParserProduct):
    for col in contColumnList:
        TagParserProduct.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format(cont,col))
               
def laborconfigRolldown(laborConfigRow,TagParserProduct):
    HideContColumns(TagParserProduct)
    phdContDefaultDict={}
    phdContDefaultDict['HCI_PHD_NewDisplaysforInsight']=['Number of medium displays','New Displays for Insight']
    phdContDefaultDict['HCI_PHD_ExcelReports']=['Number of medium reports','Reports']
    phdConts=['AR_HCI_PHD_ProjectInputs1','AR_HCI_PHD_ProjectInputs2','HCI_PHD_NewDisplaysforInsight','HCI_PHD_ExcelReports','HCI_PHD_CrystalReports','HCI_PHD_Hardware','HCI_PHD_VirtualCalculations','HCI_PHD_USMConfiguration']
    for conts in phdConts:
        prdCont= laborConfigRow.Product.GetContainerByName(conts)
        if prdCont.Rows.Count==0:
            newRow=prdCont.AddNewRow(False)
            if conts in phdContDefaultDict.keys():
                for col in phdContDefaultDict[conts]:
                	newRow[col]='1'
    NoSysInterfared= laborConfigRow.Product.Attributes.GetByName('HCI_PHD_NoSysInterfared').GetValue()
    if not NoSysInterfared:
        setNoSysInterfared = '4' # R2Q Default
        laborConfigRow.Product.Attributes.GetByName('HCI_PHD_NoSysInterfared').SelectDisplayValue(setNoSysInterfared)
        cont=laborConfigRow.Product.GetContainerByName('HCI_PHD_Tech_Scope')
        cont.Clear()
        sysInterList = ['Type A RDI:  Experion Link (Experion or TPS DCS)','Type A RDI:  OPC RDI (Third Party or Other DCS)','LIMS Interface','ERP Interface']
        sysInterList_connections = {'Type A RDI:  Experion Link (Experion or TPS DCS)':'3','Type A RDI:  OPC RDI (Third Party or Other DCS)':'2','LIMS Interface':'1','ERP Interface':'1'}
        for i in range(0,int(setNoSysInterfared)):
            sysrow=cont.AddNewRow(False)
            sysrow.GetColumnByName('System to be interfaced to').ReferencingAttribute.SelectDisplayValue(sysInterList[i])
            sysrow['Number of Connections']='0' #sysInterList_connections.get(sysInterList[i],'1')
            sysrow['Number of Collected Tags']='0' #'1000'
            if sysInterList[i]!='Type A RDI:  OPC RDI (Third Party or Other DCS)':
                sysrow.GetColumnByName('Interface Connectivity Complexity').SetAttributeValue('Simple')
                sysrow['Interface Connectivity Complexity'] = 'Simple'
                sysrow['Tag configuration Complexity'] = 'Simple'
            else:
                sysrow.GetColumnByName('Interface Connectivity Complexity').SetAttributeValue('Typical')
                sysrow.GetColumnByName('Tag configuration Complexity').SetAttributeValue('Typical')
                sysrow['Interface Connectivity Complexity'] = 'Typical'
                sysrow['Tag configuration Complexity'] = 'Typical'
def HideContColumns(TagParserProduct):
    contColumns= {'AR_HCI_PHD_ProjectInputs2':['Post-Go-Live Activities','Post Delivery Support','USM Implementation'],'AR_HCI_PHD_ProjectInputs1':['Scope of Work','Material Ordering','Staging Area Hardware and LAN Setup','Build and Configure']}
    hideContainerColumns('AR_HCI_PHD_ProjectInputs2',contColumns.get('AR_HCI_PHD_ProjectInputs2'),TagParserProduct)
    hideContainerColumns('AR_HCI_PHD_ProjectInputs1',contColumns.get('AR_HCI_PHD_ProjectInputs1'),TagParserProduct)