import re
import GS_APIGEE_Integration_Util
def getSFQuoteID():
    from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
    class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
    cartId = Quote.QuoteId
    ownerId = Quote.UserId
    class_sf_integration_modules = CL_SalesforceIntegrationModules(Quote, TagParserQuote, None, Session)
    bearerToken = class_sf_integration_modules.get_auth2_token()
    headers = class_sf_integration_modules.get_authorization_header(bearerToken)
    query = "?q="+"select+Id+from+Quote+where+Quote_ID__c={cartId}+and+Owner_ID__c={ownerId}".format(cartId = str(cartId),ownerId = str(ownerId))
    quoteID = class_sf_integration_modules.call_soql_api(headers, query)
    #OppOwner = SalesforceProxy.Binding.query("SELECT Name,Phone,email FROM User WHERE Id = '"+str(Id)+"'")
    if len(quoteID.records) != 0:
            for q in quoteID.records:
                SFQuoteID = str(q.Id)
            return SFQuoteID

IoContainerlist = ['C300_RG_Universal_IO_cont_1', 'SerC_RG_Enhanced_Function_IO_Cont', 'C300_CG_Universal_IO_cont_1', 'SerC_CG_Enhanced_Function_IO_Cont', 'C300_RG_Universal_IO_cont_2','C300_CG_Universal_IO_cont_2','SerC_CG_Enhanced_Function_IO_Cont2', 'C300_CG_Universal_IO_Mark_1', 'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont ', 'C300_CG_Universal_IO_Mark_2', 'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1', 'SerC_RG_Enhanced_Function_IO_Cont2', 'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont', 'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1','SM_IO_Count_Digital_Input_Cont','SM_IO_Count_Digital_Output_Cont','SM_IO_Count_Analog_Input_Cont','SM_IO_Count_Analog_Output_Cont','SM_SC_Universal_Safety_Cab_1_3M_Details_cont','UOC_CG_UIO_Cont','UOC_CG_Other_IO_Cont','UOC_RG_UIO_Cont','UOC_RG_Other_IO_Cont', 'C300_TurboM_IOM_CG_Cont', 'C300_TurboM_IOM_RG_Cont', 'SM_RG_IO_Count_Digital_Input_Cont', 'SM_RG_IO_Count_Digital_Output_Cont', 'SM_RG_IO_Count_Analog_Input_Cont', 'SM_RG_IO_Count_Analog_Output_Cont', 'SM_RG_DI_RLY_NMR_Cont', 'SM_RG_DO_RLY_NMR_Cont', 'SM_RG_IO_Count_Analog_Input_1.3_Cabinet_Cont', 'SM_RG_IO_Count_Digital_Input_1.3_Cabinet_Cont','PLC_CG_UIO_Cont','PLC_CG_Other_IO_Cont','HC900_Additional_IO_Details_of_SIL2','HC900_IO_Details_of_SIL2','HC900_IO_Details_of_Non-SIL','PLC_RG_Other_IO_Cont','PLC_RG_UIO_Cont']


colnamelist=['IO_Type','Selected_Products','IO_Type_with_hint','Parent_Product','AI','AO','DI','DO','Labor_IS','IO_Type_info','Message_Check','Validity_Check','IO_Type Info Icon','Digital Input Type','Rank','Total DI Point','Total DO Point','Analog Input Type','Total AI Point','Analog Output Type','Total AO Point','Power_Supply_Type','CNM_SFP_Type','Number_of_SFP_0-500','Number_of_Control_Network_Module_0','Abu_Dhabi_Build_Loc,External _24VDC_Terminal_Block','Temperature_Monitoring','IO_Redundancy,Earth_Leakage_Detector_TELD','Power_Supply_Redundancy','Wire_Routing_Options','Field_Termination_Assembly_for_PDIO','Field_Termination_Assembly_for_PUIO','Fiber_Optic_Extender','S300','Ambient_Temperature_Range','Cabinet_Material_Type_Ingress_Protection']
HC900Col=['IO_Point_Quantity','Euro_TB']
HC900IOCont=['HC900_Additional_IO_Details_of_SIL2','HC900_IO_Details_of_SIL2','HC900_IO_Details_of_Non-SIL']

nested_dict = {}
dubcontaonlist=[]
Esdorderlist=[]
FGSorderlist=[]
UOCorderlist=[]
PLCorderlist=[]
HC900orderlist=[]
orderbasedlist=[]
Iocontdatalist={}
SCADAdict={}
def to_yes_no(value):
    try:
        return 'Yes' if int(value) > 0 else 'No'
    except (ValueError, TypeError):
        return 'No'

def is_convertible_to_int(value):
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False
def nestedchild(childnest, childproduct, key,Ioname):
    for childattr in childproduct.Attributes:
        if childattr.DisplayType == 'Container' and childattr.Name in ['Series_C_Control_Groups_Cont', 'Series_C_Remote_Groups_Cont','SM_ControlGroup_Cont','SM_RemoteGroup_Cont','UOC_ControlGroup_Cont','UOC_RemoteGroup_Cont','PLC_ControlGroup_Cont','HC900_Cont','PLC_RemoteGroup_Cont']:
                childcontainerRows = childproduct.GetContainerByName(childattr.Name).Rows
                if childcontainerRows.Count > 0:
                    for containerRow in childcontainerRows:
                        for childcol in containerRow.Columns:
                            if childcol.Name in[ 'Series_C_CG_Name','Control Group Name','HC900 Group Name']: 
                                # Extract and ensure key exists in the dictionary
                                cg_name = containerRow[childcol.Name]
                                #if cg_name not in nested_dict:
                                nested_dict[cg_name] = {"RG_Name": []}
                                if childcol.Name=='Series_C_CG_Name':
                                    orderbasedlist.append(cg_name)
                                elif(childproduct.Name=='R2Q Safety Manager FGS'):
                                    FGSorderlist.append(cg_name)
                                elif(childproduct.Name=='R2Q ControlEdge UOC System'):
                                    UOCorderlist.append(cg_name)
                                elif(childproduct.Name=='R2Q ControlEdge PLC System'):
                                    PLCorderlist.append(cg_name)
                                elif(childproduct.Name=='HC900 System'):
                                    HC900orderlist.append(cg_name)
                                else:
                                    Esdorderlist.append(cg_name)
                                nestedchild(nested_dict[cg_name], containerRow.Product, childcol.Name,cg_name)
                            elif childcol.Name in ['Series_C_RG_Name','Remote Group Name','UOC_RemoteGroup_Cont']:
                                # Add Remote Group name to RG_Name list
                                if key:  # Only append if key is not empty
                                    childnest["RG_Name"].append(containerRow[childcol.Name])
                                    nestedchild(childnest, containerRow.Product, childcol.Name,containerRow[childcol.Name])
        elif (childattr.DisplayType == 'Container' and childattr.Name in IoContainerlist):
            childdatacontainerRows = childproduct.GetContainerByName(childattr.Name).Rows
            IoIsSum =0
            if childdatacontainerRows.Count > 0:
                for datacontanierRow in childdatacontainerRows:
                    for datacol in datacontanierRow.Columns:
                        if datacontanierRow[datacol.Name] != '':
                            if (datacol.Name not in colnamelist and childattr.Name not in HC900IOCont) or (childattr.Name in HC900IOCont and datacol.Name in HC900Col):
                                if datacol.Name in ['PUIO_Count','PDIO_Count']:
                                    if is_convertible_to_int(datacontanierRow.GetColumnByName(datacol.Name).DisplayValue):
                                        IoIsSum = IoIsSum + int(datacontanierRow.GetColumnByName(datacol.Name).DisplayValue)
                                    else:
                                        IoIsSum = IoIsSum + int(0)
                                else:
                                    if is_convertible_to_int(datacontanierRow[datacol.Name]):
                                        IoIsSum = IoIsSum + int(datacontanierRow[datacol.Name])
                                    else:
                                        IoIsSum = IoIsSum + int(0)
            if Ioname in Iocontdatalist:
                getval=Iocontdatalist[Ioname]
                IoIsSum = IoIsSum + int(getval)
            Iocontdatalist[Ioname]=IoIsSum
        else:
            if childattr.DisplayType == 'DropDown':
                if childattr.Name == 'C300_RG_UPC_Universal_IO_Count':
                    cabinetCountInput = childproduct.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
                    ioCountGet = Iocontdatalist.get(Ioname, 0)
                    if ioCountGet == 0 and cabinetCountInput:
                        Iocontdatalist[Ioname] = cabinetCountInput


def extractProductContainer(attrName, product,getselectAttributedict):
    containerList = []
    containerProductList = []
    containerRows = product.GetContainerByName(attrName).Rows
    if(attrName=='Modbus/OPC Interfaces'):
        if 'ethenetval' in SCADAdict:
            devicval=str(containerRows[0]['Nodes']) if containerRows[0]['Nodes'] !='' else '0'
            SCADAdict['ethenetval']=str(int(SCADAdict['ethenetval']) + int(devicval))
        else:
            SCADAdict['ethenetval']=str(containerRows[0]['Nodes']) if containerRows[0]['Nodes'] !='' else '0'
        if 'DevicesOnSerial' in SCADAdict:
            ethenval=str(containerRows[1]['Nodes']) if containerRows[1]['Nodes'] !='' else '0'
            SCADAdict['DevicesOnSerial']=str(int(SCADAdict['DevicesOnSerial']) + int(ethenval))
        else:
            SCADAdict['DevicesOnSerial']=str(containerRows[1]['Nodes']) if containerRows[1]['Nodes'] !='' else '0'
    if containerRows.Count > 0:
        for contanierRow in containerRows:
            contanierRowDict = {}
            for col in contanierRow.Columns:
                if col.Name == 'Selected_Products':
                    nestedchild(nested_dict, contanierRow.Product, "","")
                contanierRowDict[col.Name] = contanierRow[col.Name]
            containerList.append(contanierRowDict)
            if contanierRow.Product and attrName not in ['R2Q_Project_Questions_Cont']:
                selectAttributedict_level = {}
                extractProductAttributes(selectAttributedict_level, contanierRow.Product,getselectAttributedict)
                containerProductList.append(selectAttributedict_level)
    return [containerList , containerProductList]


def extractProductAttributes(attributedict, product,getselectAttributedict):
    for attr in product.Attributes:
        if attr.DisplayType == 'Container' and attr.Name not in attributedict:
            attributedict[attr.Name] = extractProductContainer(attr.Name, product,getselectAttributedict)
        else:
            if product.Attr(attr.Name).GetValue() != '' and attr.Name not in attributedict:
                attributedict[attr.Name] = product.Attr(attr.Name).GetValue()
                if attr.Name in ['Colour A4 printer', 'Colour_A3_printer', 'B_W_A3_printer','ESD_FGS_Aux_PanelsConsoles', 'CMS Flex Station Qty 0_60','Flex Station Qty (0-60)', 'DMS Flex Station Qty 0_60', 'Additional Stations','Laptop (0-50)','LaserJet Printer - Monochrome (0-99)'] and getselectAttributedict.get(attr.Name) is not None:
                    oldvalue = int(getselectAttributedict[attr.Name] or 0)
                    newvalue = int(product.Attr(attr.Name).GetValue() or 0)
                    getselectAttributedict[attr.Name] = str(oldvalue + newvalue)
                else:
                    #Trace.Write("Prod {} Attr {} Value {}".format(product.Name,attr.Name,product.Attr(attr.Name).GetValue()))
                    if product.Name=="Terminal Manager" and attr.Name== "Terminal_Mode_of_Transport":
                        getselectAttributedict["Terminal_Mode"] = product.Attr(attr.Name).GetValue()
                    if product.Name in ["R2Q C300 System","C300 System"]:
                        getselectAttributedict["cotTypec300"] = "Yes"
                    if product.Name in ['ControlEdge PLC System','ControlEdge UOC System','R2Q ControlEdge UOC System','R2Q ControlEdge PLC System']:
                        getselectAttributedict["ContTypeCOntEdge"] = "Yes"
                    if product.Name in ['Tank Gauging Engineering','Tank Gauging']:
                        getselectAttributedict["Tank_G"] = "Yes"
                    if attr.Name=="HC900_System_Type" and product.Attr("HC900_System_Type").GetValue()=="SIL2 Safety System":
                        getselectAttributedict["HC900_System"] = product.Attr(attr.Name).GetValue()
                    if attr.Name =="SM_General_RelayTypeForESD" and product.Attr("SM_General_RelayTypeForESD").GetValue()=="SIL3":
                        getselectAttributedict["RelayTypeForESD"] = product.Attr(attr.Name).GetValue()
                    getselectAttributedict[attr.Name] = product.Attr(attr.Name).GetValue()

def Architecture(Product):
    saveAction = Quote.GetCustomField("R2Q_Save").Content
    isR2Qquote = True if Quote.GetCustomField("R2QFlag").Content else False
    getselectAttributedict = {}
    if isR2Qquote and saveAction != 'Save':
        selectAttributedict = {}
        extractProductAttributes(selectAttributedict,Product,getselectAttributedict)
        containerValues = selectAttributedict
    DomainControllerRequired=''
    OPCServer_NodeType=''
    ServerRedundancy=''
    DCSControllerType = getselectAttributedict.get('SerC_CG_Type_of_Controller_Required','')
    network_firewall_required = to_yes_no(getselectAttributedict.get('Network_Firewall_Required', '0'))
    l3Switch = to_yes_no(getselectAttributedict.get('L3 Switch Required (0-10)', '0'))
    GPNValue = to_yes_no(getselectAttributedict.get('GPS NTP Server System (0-1)', '0'))
    additionalStation=getselectAttributedict.get('Additional Stations', '')
    entlaptop = getselectAttributedict.get('Laptop (0-50)', '')
    A4Printer = getselectAttributedict.get('Colour A4 printer', '0')
    A3Printer = getselectAttributedict.get('Colour_A3_printer', '0')
    bwA3printer = getselectAttributedict.get('B_W_A3_printer', '0')
    BnWA4Printers=getselectAttributedict.get('LaserJet Printer - Monochrome (0-99)', '0')
    DomainController= getselectAttributedict.get('Domain_Controller_Required','') 
    #TAS Atributes collection start
    ERP_BSI=SAP_Interface= getselectAttributedict.get('Terminal_SAP_ERP_BSI_Interface_required?','')
    RelayTypeForESD= getselectAttributedict.get('RelayTypeForESD','')
    HC900Syst= getselectAttributedict.get('HC900_System','')
    SMSyst= getselectAttributedict.get('HC900_System_Type','')
    ESD_system="HC900/SIL-3 (SM)" if RelayTypeForESD =="SIL3" and HC900Syst=="Non-SIL HC900 System" else ("HC900/None" if HC900Syst =="SIL2 Safety System" else("None/SIL-3 (SM)" if RelayTypeForESD =="SIL3" else "None/None"))
    FG_System= getselectAttributedict.get('FG_System','')
    Tank_G=getselectAttributedict.get('Tank_G','No')
    ModeofTransport=getselectAttributedict.get('Terminal_Mode','')
    Truck_laoding="Yes" if "Truck loading/unloading" in ModeofTransport else "No"
    Rail_laoding="Yes" if "Rail Wagon loading/unloading" in ModeofTransport else "No"
    Marine_laoding="Yes" if "Marine loading/unloading" in ModeofTransport else "No"
    Pipeline_Loading="Yes" if "Pipeline loading/unloading" in ModeofTransport else "No"
    Cctv_Req="Yes" if getselectAttributedict.get('CCTV_System_Required','') not in [""] else "No"
    cotTypec300=getselectAttributedict.get('cotTypec300','No')
    conttypeHc900="Yes" if HC900Syst not in ["None",""] else "No"
    ContTypeCOntEdge=getselectAttributedict.get('ContTypeCOntEdge','No')
    WBIdentification=getselectAttributedict.get('Identification_method','')
    WBRail=getselectAttributedict.get('Number_of_WeighBridge_for_Rail_Loading','')
    WBtruck=getselectAttributedict.get('Number_of_WeighBridge_for_Truck_Loading','')
    WBPCDET=getselectAttributedict.get('PCDET_Required','')
    LOIdentification=getselectAttributedict.get('Entry_Identification_Method','')
    LOEntry=getselectAttributedict.get('Number_of_Entry_Gates','')
    LOExit=getselectAttributedict.get('Number_of_Exit_Gates','')
    LOPCDETEntry=getselectAttributedict.get('Entry_Gate_PCDET_Required','')
    LOPCDETExit=getselectAttributedict.get('Exit_Gate_PCDET_Required','')
    ELOIdentification=getselectAttributedict.get('Exit_Identification_Method','')
    Web_portal=getselectAttributedict.get('Terminal_Web_Portal_required?','')
    experion_TAS=getselectAttributedict.get('R2Q_Type_of_TAS_System','')
    integrated="No"
    if getselectAttributedict.get('Terminal_to_be_integrated_at_Enterprise_level','') !='':
        integrated ="Yes" if int(getselectAttributedict.get('Terminal_to_be_integrated_at_Enterprise_level','')) > 0 else "No"
    Terminal_Level=integrated
    #TAS Atributes collection end
    if DomainController=='Yes':
        DomainControllerRequired='Rack' if 'Rack' in getselectAttributedict.get('Server Type1', '') else ('Tower' if 'Tower' in getselectAttributedict.get('Server Type1', '') else '')
    eServerRequired='Rack' if 'Rack' in getselectAttributedict.get('ES_Server_Node_Type', '') else ('Tower' if 'Tower' in getselectAttributedict.get('ES_Server_Node_Type', '') else '')
    EBRServer_NodeType='Rack' if 'Rack' in getselectAttributedict.get('Server Node Type EBR', '') else ('Tower' if 'Tower' in getselectAttributedict.get('Server Node Type EBR', '') else '')
    
    FDMServer=getselectAttributedict.get('FDM_Server_Specification','')
    
    if FDMServer=='Server':
        FDMServer_NodeType='Rack' if 'Rack' in getselectAttributedict.get('FDM_Server Node Type', '') else ('Tower' if 'Tower' in getselectAttributedict.get('FDM_Server Node Type', '') else '')
    else:
        FDMServer_NodeType=''
    opcserverreq =  getselectAttributedict.get('Opc_server_required','')
    opcserverredundreq = getselectAttributedict.get('OPC_server_redundancy_required', '')
    # Determine OPCServer_NodeType based on conditions
    if opcserverreq == 'Yes' and opcserverredundreq !='':
        server_type = getselectAttributedict.get('Server Type1', '')
        if opcserverredundreq == 'Non Redundant':
            OPCServer_NodeType = 'Non Red. Rack' if 'Rack' in server_type else ('Non Red. Tower' if 'Tower' in server_type else '')
        else:
            OPCServer_NodeType = 'Red. Rack' if 'Rack' in server_type else ('Red. Tower' if 'Tower' in server_type else '')
   
    # Extract values from the attribute dictionary
    ServerMounting = getselectAttributedict.get('Server Mounting', '')
    pksserverredundreq = getselectAttributedict.get('Server Redundancy Requirement?', '')
    
    # Check conditions for ServerRedundancy assignment
    if pksserverredundreq !='' and ServerMounting !='':
        if ServerMounting == 'Desk':
            ServerRedundancyval = getselectAttributedict.get('Server Node Type_desk', '')
        else:
            ServerRedundancyval = getselectAttributedict.get('Server_NodeType', '')

        if pksserverredundreq == 'Non Redundant':
            ServerRedundancy = 'Non Red. Rack' if 'Rack' in ServerRedundancyval else ('Non Red. Tower' if 'Tower' in ServerRedundancyval else '')
        else:
            ServerRedundancy = 'Red. Rack' if 'Rack' in ServerRedundancyval else ('Red. Tower' if 'Tower' in ServerRedundancyval else '')

    ESDnFGSAuxPanels = getselectAttributedict.get('ESD_FGS_Aux_PanelsConsoles', '0')
    ESDFGSEnggStations = getselectAttributedict.get('Additional Stations', '0')
    OpStations1 = getselectAttributedict.get('CMS Flex Station Qty 0_60', '0')
    OpStations2 = getselectAttributedict.get('Flex Station Qty (0-60)', '0')
    OpStations3 = getselectAttributedict.get('DMS Flex Station Qty 0_60', '0')
    DCSESDFGSOperatorStations= str(int(OpStations1)+int(OpStations2)+int(OpStations3))
    DevicesOnSerial=SCADAdict.get('DevicesOnSerial','0') or '0'
    ethenetval=SCADAdict.get('ethenetval','0') or '0'

    CustomGroupNames = [""] * 10
    IOCountControlGroupConfigs = [""] * 10
    IOCountRemoteGroupConfigs = [""] * 10
    CustomGroupDCSRemoteCounts = [""] * 10
    EsdCustomGroupNames = [""] * 10
    EsdIOCountControlGroupConfigs = [""] * 10
    EsdIOCountRemoteGroupConfigs = [""] * 10
    EsdCustomGroupDCSRemoteCounts = [""] * 10
    
    FgsCustomGroupNames = [""] * 10
    FgsIOCountControlGroupConfigs = [""] * 10
    FgsIOCountRemoteGroupConfigs = [""] * 10
    FgsCustomGroupDCSRemoteCounts = [""] * 10
    UOCIOCountControlGroupConfigs = [""] * 10
    UOCIOCountRemoteGroupConfigs = [""] * 10
    UOCCustomGroupRemoteCounts = [""] * 10
    PLCIOCountControlGroupConfigs = [""] * 10
    PLCIOCountRemoteGroupConfigs = [""] * 10
    PLCCustomGroupRemoteCounts = [""] * 10
    HC900IOCountControlGroupConfigs = [""] * 10
    HC900IOCountRemoteGroupConfigs = [""] * 10
    HC900CustomGroupRemoteCounts = [""] * 10
    rgiocountlist = []
    rgnamelenth = []
    Esdrgiocountlist = []
    Esdrgnamelenth = []
    Fgsrgiocountlist = []
    Fgsrgnamelenth = []
    
    Uocrgiocountlist = []
    Uocrgnamelenth = []
    PLCrgiocountlist = []
    PLCrgnamelenth = []
    HC900rgiocountlist = []
    HC900rgnamelenth = []
    if Quote.GetCustomField("R2QFlag").Content=="Yes":
        SFQuoteID =  getSFQuoteID()
    else:
        SFQuoteID = Quote.GetCustomField("CF_R2Q_SFDCQuoteId").Content
    QuoteNumber=Quote.CompositeNumber
    if getselectAttributedict.get('R2Q Select Category','')=="TA System":
        if (Tank_G=="Yes" or Rail_laoding=="Yes" or Marine_laoding=="Yes" or Pipeline_Loading=="Yes" or FG_System !='' or Truck_laoding=="Yes" or Cctv_Req=="Yes") or (LOIdentification or LOEntry or LOExit or LOPCDETEntry or LOPCDETExit or ELOIdentification or WBPCDET or WBIdentification or WBRail or WBtruck)  not in ['0',0,'NO','']:
            DevicesOnSerial= 1
        if ERP_BSI =="Yes" or integrated=="Yes" or Web_portal=="Yes":
            network_firewall_required = "Yes"
        final_request_body = {"SFQuoteID":SFQuoteID,"CPQQuoteNumber":QuoteNumber,"Module":"TAS","ERP_System":ERP_BSI,"CCTV":{"Cctv_Req":Cctv_Req},"ESD_System":ESD_system,"Fire_And_Gas_System":{"FnG_Scope":FG_System},"Tank_Gauging_System":{"Tank_Gauge_Req":Tank_G},"Truck_Loading_Scope":Truck_laoding,"Rail_Loading_Scope":Rail_laoding,"Marine_Loading_Scope":Marine_laoding,"Pipeline_Loading_Scope":Pipeline_Loading,"Entry_And_Exit_Gates":{"Entry_Identification":LOIdentification,"Entry_Gate_Count":LOEntry,"Exit_Gate_Count":LOExit,"Entry_Gate_PCDET_Req":LOPCDETEntry,"Exit_Gate_PCDET_Req":LOPCDETExit,"Exit_Identification":ELOIdentification},"Weigh_Bridge_Interface":{"Weigh_Bridge_Count_Truck_Loading":WBtruck,"Weigh_Bridge_Count_Rail_Loading":WBRail,"Weigh_Bridge_Identification_Method":WBIdentification,"Weigh_Bridge_PCDET_Req":WBPCDET},"Controller_Type_C300":cotTypec300,"Controller_Type_ControlEdge":ContTypeCOntEdge,"Controller_Type_HC900":conttypeHc900,'NetworkFirewallRequired': network_firewall_required, 'eServerRequired': eServerRequired, 'L3SwitchRequired': l3Switch, 'DCSESDFGSOperatorStations': DCSESDFGSOperatorStations, 'GPSNTPServerRequired': GPNValue, 'ESDFGSEnggStations': ESDFGSEnggStations, 'DCSEnggStations': '0', 'Laptops': entlaptop, 'ColorA4Printers': A4Printer, 'ColorA3Printers': A3Printer , 'BnWA4Printers': BnWA4Printers, 'BnWA3Printers': bwA3printer, 'DotMatrixPrinters': '0', 'DCSControllerType': DCSControllerType, 'SAP_Interface':SAP_Interface,'Enterprise_Node':Terminal_Level,'Web_portal':Web_portal,'experion_TAS_server':experion_TAS,}
    else:
        final_request_body = { 'SFQuoteID':SFQuoteID, 'quoteNumber': QuoteNumber, 'Module': 'ICSS', 'NetworkFirewallRequired': network_firewall_required, 'eServerRequired': eServerRequired, 'L3SwitchRequired': l3Switch, 'DCSESDFGSOperatorStations': DCSESDFGSOperatorStations, 'GPSNTPServerRequired': GPNValue, 'ESDFGSEnggStations': ESDFGSEnggStations, 'DCSEnggStations': '0', 'Laptops': entlaptop, 'ColorA4Printers': A4Printer, 'ColorA3Printers': A3Printer , 'BnWA4Printers': BnWA4Printers, 'BnWA3Printers': bwA3printer, 'DotMatrixPrinters': '0', 'DCSControllerType': DCSControllerType, }
    # Loop through `orderbasedlist` to assign values to dynamic variables
    for i in range(len(orderbasedlist)):
        CustomGroupNames[i] = orderbasedlist[i]
        IOCountControlGroupConfigs[i] = Iocontdatalist.get(orderbasedlist[i], "")
        
        # Calculate IOCountRemoteGroupConfig and CustomGroupDCSRemoteCount
        if i < len(orderbasedlist):
            coutnreset = 0
            rgiosum = 0
            for control_group, value in nested_dict.items():
                if orderbasedlist[i] == control_group:
                    rg_count = 0
                    for rg_name in value['RG_Name']:
                        io_count = int(Iocontdatalist.get(rg_name, 0))
                        if io_count > 0:
                            rg_count += 1
                        rgiosum += io_count
                    rgnamelenth.append(rg_count if rg_count > 0 else 0)
            rgiocountlist.append(rgiosum)
    
    for i in range(len(UOCorderlist)):
        CustomGroupNames[i] = UOCorderlist[i]
        UOCIOCountControlGroupConfigs[i] = Iocontdatalist.get(UOCorderlist[i], "")
        
        # Calculate IOCountRemoteGroupConfig and CustomGroupDCSRemoteCount
        if i < len(UOCorderlist):
            coutnreset = 0
            rgiosum = 0
            for control_group, value in nested_dict.items():
                if UOCorderlist[i] == control_group:
                    rg_count = 0
                    for rg_name in value['RG_Name']:
                        io_count = int(Iocontdatalist.get(rg_name, 0))
                        if io_count > 0:
                            rg_count += 1
                        rgiosum += io_count
                    Uocrgnamelenth.append(rg_count if rg_count > 0 else 0)
            Uocrgiocountlist.append(rgiosum)
    for i in range(len(PLCorderlist)):
        CustomGroupNames[i] = PLCorderlist[i]
        PLCIOCountControlGroupConfigs[i] = Iocontdatalist.get(PLCorderlist[i], "")
        
        # Calculate IOCountRemoteGroupConfig and CustomGroupDCSRemoteCount
        if i < len(PLCorderlist):
            coutnreset = 0
            rgiosum = 0
            for control_group, value in nested_dict.items():
                if PLCorderlist[i] == control_group:
                    rg_count = 0
                    for rg_name in value['RG_Name']:
                        io_count = int(Iocontdatalist.get(rg_name, 0))
                        if io_count > 0:
                            rg_count += 1
                        rgiosum += io_count
                    PLCrgnamelenth.append(rg_count if rg_count > 0 else 0)
            PLCrgiocountlist.append(rgiosum)
    for i in range(len(HC900orderlist)):
        CustomGroupNames[i] = HC900orderlist[i]
        HC900IOCountControlGroupConfigs[i] = Iocontdatalist.get(HC900orderlist[i], "")
        
        # Calculate IOCountRemoteGroupConfig and CustomGroupDCSRemoteCount
        if i < len(HC900orderlist):
            coutnreset = 0
            rgiosum = 0
            for control_group, value in nested_dict.items():
                if HC900orderlist[i] == control_group:
                    rg_count = 0
                    for rg_name in value['RG_Name']:
                        io_count = int(Iocontdatalist.get(rg_name, 0))
                        if io_count > 0:
                            rg_count += 1
                        rgiosum += io_count
                    HC900rgnamelenth.append(rg_count if rg_count > 0 else 0)
            HC900rgiocountlist.append(rgiosum)
            
    for i in range(len(Esdorderlist)):
        EsdCustomGroupNames[i] = Esdorderlist[i]
        EsdIOCountControlGroupConfigs[i] = Iocontdatalist.get(Esdorderlist[i], "")
        
        # Calculate IOCountRemoteGroupConfig and CustomGroupDCSRemoteCount
        if i < len(Esdorderlist):
            coutnreset = 0
            rgiosum = 0
            for control_group, value in nested_dict.items():
                if Esdorderlist[i] == control_group:
                    rg_count = 0
                    for rg_name in value['RG_Name']:
                        io_count = int(Iocontdatalist.get(rg_name, 0))
                        if io_count > 0:
                            rg_count += 1
                        rgiosum += io_count
                    Esdrgnamelenth.append(rg_count if rg_count > 0 else 0)
            Esdrgiocountlist.append(rgiosum)
    
    for i in range(len(FGSorderlist)):
        FgsCustomGroupNames[i] = FGSorderlist[i]
        FgsIOCountControlGroupConfigs[i] = Iocontdatalist.get(FGSorderlist[i], "")
        
        # Calculate IOCountRemoteGroupConfig and CustomGroupDCSRemoteCount
        if i < len(FGSorderlist):
            coutnreset = 0
            rgiosum = 0
            for control_group, value in nested_dict.items():
                if FGSorderlist[i] == control_group:
                    rg_count = 0
                    for rg_name in value['RG_Name']:
                        io_count = int(Iocontdatalist.get(rg_name, 0))
                        if io_count > 0:
                            rg_count += 1
                        rgiosum += io_count
                    Fgsrgnamelenth.append(rg_count if rg_count > 0 else 0)
            Fgsrgiocountlist.append(rgiosum)

    for i in range(len(rgnamelenth)): 
        IOCountRemoteGroupConfigs[i] = rgiocountlist[i] if i < len(rgiocountlist) else "0"
        CustomGroupDCSRemoteCounts[i] = rgnamelenth[i] if i < len(rgnamelenth) else "0"
    
    for i in range(len(Esdrgnamelenth)): 
        EsdIOCountRemoteGroupConfigs[i] = Esdrgiocountlist[i] if i < len(Esdrgiocountlist) else "0"
        EsdCustomGroupDCSRemoteCounts[i] = Esdrgnamelenth[i] if i < len(Esdrgnamelenth) else "0"
        
    for i in range(len(Fgsrgnamelenth)): 
        FgsIOCountRemoteGroupConfigs[i] = Fgsrgiocountlist[i] if i < len(Fgsrgiocountlist) else "0"
        FgsCustomGroupDCSRemoteCounts[i] =  Fgsrgnamelenth[i] if i < len(Fgsrgnamelenth) else "0"
    
    for i in range(len(Uocrgnamelenth)): 
        UOCIOCountRemoteGroupConfigs[i] = Uocrgiocountlist[i] if i < len(Uocrgiocountlist) else "0"
        UOCCustomGroupRemoteCounts[i] =  Uocrgnamelenth[i] if i < len(Uocrgnamelenth) else "0"

    for i in range(len(PLCrgnamelenth)): 
        PLCIOCountRemoteGroupConfigs[i] = PLCrgiocountlist[i] if i < len(PLCrgiocountlist) else "0"
        PLCCustomGroupRemoteCounts[i] =  PLCrgnamelenth[i] if i < len(PLCrgnamelenth) else "0"

    for i in range(len(HC900rgnamelenth)): 
        HC900IOCountRemoteGroupConfigs[i] = HC900rgiocountlist[i] if i < len(HC900rgiocountlist) else "0"
        HC900CustomGroupRemoteCounts[i] =  HC900rgnamelenth[i] if i < len(HC900rgnamelenth) else "0"        
    if getselectAttributedict.get('R2Q Select Category','') in ["ICS System","TA System"]:
        for i in range(10):
            # Create the key by concatenating the string parts
            final_request_body["CustomGroupName" + str(i + 1)] = "Unit # " + str(i+1)
            final_request_body["CustomGroupDCSRemoteCount" + str(i+1)] = str(CustomGroupDCSRemoteCounts[i]) if i < len(CustomGroupDCSRemoteCounts) and len(IOCountRemoteGroupConfigs) and str(IOCountRemoteGroupConfigs[i]) > "0"  else "0"
            final_request_body["IOCountControlGroupConfig" + str(i+1)] = str(IOCountControlGroupConfigs[i]) if i < len(IOCountControlGroupConfigs) else ""
            final_request_body["IOCountRemoteGroupConfig" + str(i+1)] = str(IOCountRemoteGroupConfigs[i]) if i < len(IOCountRemoteGroupConfigs) else ""
            final_request_body["CustomGroupESDRemoteCount" + str(i+1)] = str(EsdCustomGroupDCSRemoteCounts[i]) if i < len(EsdCustomGroupDCSRemoteCounts) and len(EsdIOCountRemoteGroupConfigs) and str(EsdIOCountRemoteGroupConfigs[i]) > "0" else "0"
            final_request_body["IOCountESDControlGroupConfig" + str(i+1)] = str(EsdIOCountControlGroupConfigs[i]) if i < len(EsdIOCountControlGroupConfigs) else "0"
            final_request_body["IOCountESDRemoteGroupConfig" + str(i+1)] = str(EsdIOCountRemoteGroupConfigs[i]) if i < len(EsdIOCountRemoteGroupConfigs) else "0"

            final_request_body["CustomGroupFGSRemoteCount" + str(i+1)] = str(FgsCustomGroupDCSRemoteCounts[i]) if i < len(FgsCustomGroupDCSRemoteCounts) and len(FgsIOCountRemoteGroupConfigs) and str(FgsIOCountRemoteGroupConfigs[i]) > "0" else "0"
            final_request_body["IOCountFGSControlGroupConfig" + str(i+1)] = str(FgsIOCountControlGroupConfigs[i]) if i < len(FgsIOCountControlGroupConfigs) else "0"
            final_request_body["IOCountFGSRemoteGroupConfig" + str(i+1)] = str(FgsIOCountRemoteGroupConfigs[i]) if i < len(FgsIOCountRemoteGroupConfigs) else "0"

            final_request_body["CustomGroupUOCRemoteCount" + str(i+1)] = str(UOCCustomGroupRemoteCounts[i]) if i < len(UOCCustomGroupRemoteCounts) and len(UOCIOCountRemoteGroupConfigs) and str(UOCIOCountRemoteGroupConfigs[i]) > "0" else "0"
            final_request_body["IOCountUOCControlGroupConfig" + str(i+1)] = str(UOCIOCountControlGroupConfigs[i]) if i < len(UOCIOCountControlGroupConfigs) else "0"
            final_request_body["IOCountUOCRemoteGroupConfig" + str(i+1)] = str(UOCIOCountRemoteGroupConfigs[i]) if i < len(UOCIOCountRemoteGroupConfigs) else "0"

            final_request_body["CustomGroupPLCRemoteCount" + str(i+1)] = str(PLCCustomGroupRemoteCounts[i]) if i < len(PLCCustomGroupRemoteCounts) and len(PLCIOCountRemoteGroupConfigs) and str(PLCIOCountRemoteGroupConfigs[i]) > "0" else "0"
            final_request_body["IOCountPLCControlGroupConfig" + str(i+1)] = str(PLCIOCountControlGroupConfigs[i]) if i < len(PLCIOCountControlGroupConfigs) else "0"
            final_request_body["IOCountPLCRemoteGroupConfig" + str(i+1)] = str(PLCIOCountRemoteGroupConfigs[i]) if i < len(PLCIOCountRemoteGroupConfigs) else "0"
            
            #final_request_body["CustomGroupHC900RemoteCount" + str(i+1)] = str(HC900CustomGroupRemoteCounts[i]) if i < len(HC900CustomGroupRemoteCounts) and len(HC900IOCountRemoteGroupConfigs) and str(HC900IOCountRemoteGroupConfigs[i]) > "0" else "0"
            final_request_body["IOCountHC900ControlGroupConfig" + str(i+1)] = str(HC900IOCountControlGroupConfigs[i]) if i < len(HC900IOCountControlGroupConfigs) else "0"
            #final_request_body["IOCountHC900RemoteGroupConfig" + str(i+1)] = str(HC900IOCountRemoteGroupConfigs[i]) if i < len(HC900IOCountRemoteGroupConfigs) else "0"

        final_request_body.update({'ESDnFGSAuxPanels':ESDnFGSAuxPanels, 'DevicesOnEthernet': ethenetval, 'DevicesOnSerial': DevicesOnSerial, 'OPCServerRequired': OPCServer_NodeType, 'ServerRedundancy': ServerRedundancy, 'DomainControllerRequired': DomainControllerRequired, 'FDMServerRequired': FDMServer_NodeType, 'EBRServerRequired': EBRServer_NodeType })
    
    Log.Info(str(final_request_body))
    
    #Trace.Write(str(final_request_body))
    #Trace.Write(str(rgiocountlist))
    #Trace.Write(str(rgnamelenth))
    #Trace.Write(str(rgnamelenth))
    #Trace.Write(str(getselectAttributedict))
    APIGEE_Credentials = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_Credentials'").Value
    APIGEE_R2Q_URL = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_URL'").Value
    tokenUrl = "{}/v2/oauth/accesstoken".format(APIGEE_R2Q_URL)
    responseToken=AuthorizedRestClient.GetClientCredentialsGrantOAuthToken(APIGEE_Credentials,tokenUrl)
    Req_Token = "{} {}".format(responseToken["token_type"] , responseToken["access_token"])
    QuoteNumber=Quote.CompositeNumber
    arch_Url="https://it.api-beta.honeywell.com/cpq/r2q/sfdc/v1/architecture-diagram"
    header = {"Content-Type" : "application/json","Authorization" : "{}".format(Req_Token),"HON-Org-Id" : "PMT-HPS" }
    res = RestClient.Post(arch_Url, RestClient.SerializeToJson(str(final_request_body)),header)

excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()
try:
    QuoteNumber = Param.QuoteNumber
    Quote = QuoteHelper.Edit(QuoteNumber)
    if Quote.ContainsAnyProduct('Project_cpq'):
        for item in Quote.MainItems:
            if item.PartNumber == 'PRJT R2Q':
                newProd = item.EditConfiguration()
                Architecture(newProd)
    Log.Info('GS_R2Q_System_Architecturediagram Success-->>')
    final_request_body={'QuoteNumber':str(Param.QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':'New/Expansion','Action':'Update','Status':'Success','Action_List':[{'ActionName':'System Architecture','ScriptName':'GS_R2Q_System_Architecturediagram'}]}
    RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
except Exception as ex:
    Log.Info('GS_R2Q_System_Architecturediagram Error-->>'+str(ex))
    final_request_body={'QuoteNumber':str(Param.QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':'New/Expansion','Action':'Update','Status':'Fail','Action_List':[{'ActionName':'System Architecture','ScriptName':'GS_R2Q_System_Architecturediagram','ErrorMessage':str(ex)}]}
    RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)