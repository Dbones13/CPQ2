def hideAttr(attrList):
    for attr in attrList:
        Product.Attr(attr).Access = AttributeAccess.Hidden
def setDefault(attrValDict):
    for attr in attrValDict:
        if Product.Attr(attr).DisplayType == 'DropDown':
            Product.Attr(attr).SelectDisplayValue(attrValDict[attr])
        else:
        	Product.Attr(attr).AssignValue(attrValDict[attr])
def showAttr(attrList):
    for attr in attrList:
        Product.Attr(attr).Access = AttributeAccess.Editable
nonR2QAttr = ['FDM_Displays (Server) (0-1)','FDM_Experion_PKS_Release']
#nonR2Q_Server = {'FDM_Displays (Server) (0-1)':''}
#setDefault(nonR2Q_Server)
hideAttr(nonR2QAttr)
#Trace.Write("It is working")
Specification_val = Product.Attr('FDM_Server_Specification').GetValue()

Workstation = ['FDM_Audit_Trail_Blocks(0-4000)','FDM_Server_Device_Adder_Blocks(0-4000)','FDM_Server_Network_Interface_License(0-5)','FDM_MUX_Monitoring_License(0-6)','FDM_Client_License(0-4)','Header_04_open','FDM_Station Node Type']
Workstation1 = {'FDM_Audit_Trail_Blocks(0-4000)' : '0','FDM_Server_Device_Adder_Blocks(0-4000)' : '0','FDM_Server_Network_Interface_License(0-5)' : '0','FDM_MUX_Monitoring_License(0-6)' : '0','FDM_Client_License(0-4)' : '0','Header_04_open' : '0','FDM_Station Node Type' : ''}
Server = ['FDM Server Device Adder Blocks (0-16000)','FDM Audit Trail Blocks (0-16000)','FDM Server Network Interface License (0-24)','FDM MUX Monitoring License (0-1)','FDM Client License (0-10)','Header_03_open','FDM_Server Node Type']

if Specification_val == 'Server':
    hideAttr(Workstation)
    showAttr(Server)
    setDefault(Workstation1)
    #Product.Attr('FDM Client Station Qty (0-10)').AssignValue('0')
elif Specification_val == 'Workstation':
    hideAttr(Server)
    showAttr(Workstation)
    #hideAttr(nonR2Q_Server)