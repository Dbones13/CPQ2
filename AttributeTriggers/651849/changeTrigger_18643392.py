def hideAttr(attrList):
    for attr in attrList:
        Product.Attr(attr).Access = AttributeAccess.Hidden
def showAttr(attrList):
    for attr in attrList:
        Product.Attr(attr).Access = AttributeAccess.Editable
def setDefault(attrValDict):
    for attr in attrValDict:
        if Product.Attr(attr).DisplayType == 'DropDown':
            Product.Attr(attr).SelectDisplayValue(attrValDict[attr])
        else:
        	Product.Attr(attr).AssignValue(attrValDict[attr])

Workstation = {'FDM_Audit_Trail_Blocks(0-4000)' : '0','FDM_Server_Device_Adder_Blocks(0-4000)' : '0','FDM_Server_Network_Interface_License(0-5)' : '0','FDM_MUX_Monitoring_License(0-6)' : '0','FDM_Client_License(0-4)' : '0','Header_04_open' : '0','FDM_Station Node Type' : 'STN_STD_DELL_Tower_NonRAID','FDM Client Stations required' : 'No', 'FDM Client Station Qty (0-10)' : '0'}
Workstation1 = {'FDM_Audit_Trail_Blocks(0-4000)' : '0','FDM_Server_Device_Adder_Blocks(0-4000)' : '0','FDM_Server_Network_Interface_License(0-5)' : '0','FDM_MUX_Monitoring_License(0-6)' : '0','FDM_Client_License(0-4)' : '0','Header_04_open' : '0','FDM_Station Node Type' : '','FDM Client Stations required' : 'No', 'FDM Client Station Qty (0-10)' : '0'}

Server = {'FDM Server Device Adder Blocks (0-16000)' : '0','FDM Audit Trail Blocks (0-16000)' : '0','FDM Server Network Interface License (0-24)' : '0','FDM MUX Monitoring License (0-1)' : '0','FDM Client License (0-10)' : '0','Header_03_open' : '0','FDM_Server Node Type' : 'SVR_STD_DELL_Tower_RAID1','FDM Client Stations required' : 'No', 'FDM Client Station Qty (0-10)' : '0','FDM_Displays (Server) (0-1)' : ''}

Server1 = {'FDM Server Device Adder Blocks (0-16000)' : '0','FDM Audit Trail Blocks (0-16000)' : '0','FDM Server Network Interface License (0-24)' : '0','FDM MUX Monitoring License (0-1)' : '0','FDM Client License (0-10)' : '0','Header_03_open' : '0','FDM_Server Node Type' : '','FDM Client Stations required' : 'No', 'FDM Client Station Qty (0-10)' : '0','FDM_Displays (Server) (0-1)' : ''}

Specification_val = Product.Attr('FDM_Server_Specification').GetValue()
if Specification_val == 'Server':
    hideAttr(Workstation)
    showAttr(Server)
    setDefault(Server)
    #setDefault(Workstation)
    setDefault(Workstation1)
elif Specification_val == 'Workstation':
    hideAttr(Server)
    showAttr(Workstation)
    setDefault(Workstation)
    setDefault(Server1)