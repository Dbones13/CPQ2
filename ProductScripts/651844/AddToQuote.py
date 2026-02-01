Quote.SetGlobal('PerformanceUpload', "Yes")
# PRJT R2Q - AddToQuote
from System.Collections.Specialized import OrderedDictionary
Log.Info('-------r2q addtoquote start---')
import R2QContainerRowAdded
import R2QRMContainerRowAdded
import GS_DEF_CONT_ATT_DICT
#from TAS_PRJT_MAPPING import r2q_to_prjt_mapping
import datetime
modifieddate =datetime.datetime.now()

mappingDict = {"HC900_Cont" : ['HC900_Cont', 'HC900_Cont_cpq'],"Series_C_Control_Groups_Cont" : ['Series_C_Control_Groups_Cont', 'Series-C_Control_Group_cpq'], "Series_C_Remote_Groups_Cont": ['Series_C_Remote_Groups_Cont', 'Series-C_Remote_Group_cpq'], "ES_Group": ['ES_Group', 'ES_Group_cpq'], "FDM_System_Group_Cont": ['FDM_System_Group_Cont', 'FDM_System_Group_cpq'], "Experion_Enterprise_Cont":['Experion_Enterprise_Cont','Experion_Enterprise_Group_cpq'], "Scada_CCR_Unit_Cont":['Scada_CCR_Unit_Cont','CCR_cpq'], 'UOC_ControlGroup_Cont': ['UOC_ControlGroup_Cont','UOC_Control_Group_cpq'], "UOC_RemoteGroup_Cont": ['UOC_RemoteGroup_Cont','UOC_Remote_Group_cpq'], 'SM_ControlGroup_Cont' : ['SM_ControlGroup_Cont', 'SM_Control_Group_cpq'], 'SM_RemoteGroup_Cont':['SM_RemoteGroup_Cont', 'SM_Remote_Group_cpq'], 'PLC_ControlGroup_Cont':['PLC_ControlGroup_Cont', 'Control_Group_cpq'], 'PLC_RemoteGroup_Cont':['PLC_RemoteGroup_Cont', 'Remote_Group_cpq']}
Experion_dict ={}
def get_c300AttrDict():
    query = SqlHelper.GetList("SELECT ATTRIBUTE_CONT_NAME, ATTRIBUTE_COLUMN_NAME, ATTRIBUTE_VALUE FROM R2Q_MAPPING_DICT")
    c300AttrDict = {}
    for row in query:
        cont_name = row.ATTRIBUTE_CONT_NAME
        column_name = row.ATTRIBUTE_COLUMN_NAME
        attribute_value = row.ATTRIBUTE_VALUE
        if cont_name not in c300AttrDict:
            c300AttrDict[cont_name] = {}
        c300AttrDict[cont_name][column_name] = attribute_value
    return c300AttrDict

# def attrList(product):
#     tab_list = []
#     for tab in product.Tabs:
#         if tab.Name == "General Inputs":
#             tab_list.append(tab.Attributes)
#         elif tab.Name == "General Input":
#             tab_list.append(tab.Attributes)
#         elif  tab.Name == "C300 Remote Group":
#             tab_list.append(tab.Attributes)
#     return tab_list


def getProductAttributes(product):
    prod_name = product.Name
    if 'Safety Manager' in prod_name:
        prod_name = "Safety Manager"
    getPrd = SqlHelper.GetFirst(""" SELECT PA.PRODUCT_ID, PA.PRODUCT_NAME FROM products PA INNER JOIN product_versions PV ON PV.product_id = PA.PRODUCT_ID WHERE PA.PRODUCT_NAME = '{}' AND PV.is_active = 'True'  and PA.IsSimple ='False' """.format(prod_name))

    prd_id = int(getPrd.PRODUCT_ID)

    product_tabs_obj = SqlHelper.GetList("""SELECT TOP 1000 TAB_NAME,TAB_DEFN.SYSTEM_ID, TAB_RANK, TAB_PROD_ID, TAB_PRODUCTS.TAB_CODE as tabcode FROM TAB_PRODUCTS (NOLOCK)  JOIN sys_ProductTabs (NOLOCK)  TAB_DEFN ON TAB_DEFN.TAB_CODE = TAB_PRODUCTS.TAB_CODE WHERE TAB_PRODUCTS.PRODUCT_ID = {ProductId} and TAB_NAME in ('General Inputs', 'General Input', 'C300 Remote Group', 'General Attribute') ORDER BY TAB_PRODUCTS.RANK""".format(ProductId =prd_id))

    attribute_names_list = []
    for tab in product_tabs_obj:
        tabcode = tab.tabcode
        product_attributes_obj = SqlHelper.GetList("""SELECT TOP 1000 PAT_SCHEMA.STANDARD_ATTRIBUTE_CODE, TAB_PRODUCTS.TAB_PROD_ID, TAB_PRODUCTS.TAB_CODE, ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_NAME as Attribute_Name,PRODUCT_ATTRIBUTES.LABEL AS LABEL, ATTRIBUTE_DEFN.SYSTEM_ID AS SYSTEM_ID, ATT_DISPLAY_DEFN.ATT_DISPLAY_DESC AS ATT_DISPLAY_DESC FROM TAB_PRODUCTS (NOLOCK) LEFT JOIN  PAT_SCHEMA (NOLOCK) ON PAT_SCHEMA.TAB_PROD_ID=TAB_PRODUCTS.TAB_PROD_ID LEFT JOIN PRODUCT_ATTRIBUTES (NOLOCK)  ON PRODUCT_ATTRIBUTES.STANDARD_ATTRIBUTE_CODE = PAT_SCHEMA.STANDARD_ATTRIBUTE_CODE AND PRODUCT_ATTRIBUTES.PRODUCT_ID = TAB_PRODUCTS.PRODUCT_ID LEFT JOIN ATTRIBUTE_DEFN (NOLOCK)  ON ATTRIBUTE_DEFN.STANDARD_ATTRIBUTE_CODE = PRODUCT_ATTRIBUTES.STANDARD_ATTRIBUTE_CODE LEFT JOIN ATT_DISPLAY_DEFN (NOLOCK)  ON ATT_DISPLAY_DEFN.ATT_DISPLAY = PRODUCT_ATTRIBUTES.ATT_DISPLAY WHERE TAB_PRODUCTS.PRODUCT_ID = {} AND TAB_PRODUCTS.TAB_CODE ='{}' ORDER BY TAB_PRODUCTS.RANK,PRODUCT_ATTRIBUTES.ATT_SUBRANK""".format(prd_id,tabcode))
        attribute_names_list.extend([attr.Attribute_Name for attr in product_attributes_obj])
    if product.Name in ('C300 System','New / Expansion Project','Series-C Control Group','Series-C Remote Group','Experion Enterprise System','Experion Enterprise Group','eServer System','eServer System Group','Field Device Manager','FDM System Group','Experion Enterprise System','Experion Enterprise Group','ControlEdge UOC System','UOC Control Group','UOC Remote Group','Safety Manager FGS','SM Control Group','SM Remote Group','Safety Manager ESD','3rd Party Devices/Systems Interface (SCADA)','CCR','Safety Manager'):
        pass
        #attribute_names_list.append('R2Q_CONFIGURATION')

    if product.Name == 'Experion Enterprise Group':
        attribute_names_list.append('EBR_Software_Required')
        attribute_names_list.append('Experion Enterprise Group Name')
        product.ApplyRules()

    if product.Name == 'Series-C Remote Group':
        attribute_names_list.append('C300_RG_UPC_FTA')
        product.ApplyRules()
    ##Log.Info("attribute_names_list =>"+str(attribute_names_list))

    return attribute_names_list

def deleteProd(prodname):
    for item in Quote.Items:
        if item.ProductName == prodname:
            getitem = Quote.GetItemByQuoteItem(item.RolledUpQuoteItem)
            getitem.Delete()

def attrValueCheck(product, attr_name, value):
    if product.Attr(attr_name).GetValue() == value:
        return False
    else:
        return True


def attrValueSelection(product, distype, attr_name, attr_value):
    if distype == "DropDown":
        if product.Attr(attr_name).Allowed == False:
            product.AllowAttr(attr_name)
        if attr_name in ['SerC_CG_IO_Family_Type','SerC_CG_Ethernet_Interface','SerC_GC_Profibus_Gateway_Interface','Total_Profibus_Red_NonRed_IOs']:
            ##Log.Info("attr_name "+str(attr_name)+ " attr_value "+str(attr_value))
            product.AllowAttr('SerC_CG_Ethernet_Interface')
            #product.Attr('SerC_CG_Ethernet_Interface').SelectDisplayValue(attr_value)
            product.AllowAttr('SerC_GC_Profibus_Gateway_Interface')
        if attr_name=='C300_RG_UPC_Universal_IO_Count' and Quote.GetGlobal('UPC_Universal_IO_Count')=='':
            Quote.SetGlobal('UPC_Universal_IO_Count', str(attr_value))
        product.Attr(attr_name).SelectDisplayValue(attr_value)
    else:
        if product.Attr(attr_name).Allowed == False:
            product.AllowAttr(attr_name)
        product.Attr(attr_name).AssignValue(attr_value)
    if product.Name in ['Series-C Control Group','Series-C Remote Group']:
        product.ApplyRules()
    if product.Name in ('Experion Enterprise System', 'Experion Enterprise Group'):
        product.Attr('CE_Site_Voltage').AssignValue('120V')
        product.ApplyRules()
        if product.Attr('EBR_Software_Required').GetValue() == 'Yes':
            product.Attr('Experion Backup Restore Software Release').AssignValue('R520')

def AddRows(rowCount, container, Groups_Cont_count, attrValue, attr_name, contname, sysid=''):
    row_Count =0
    if contname == 'HC900_Cont':
        for i in range(Groups_Cont_count, rowCount):
            newRow = container.AddNewRow(False)
            container_column_values  = attrValue[0][row_Count]
            for col_name, col_value in container_column_values.items():
                newRow[col_name] = col_value
            row_Count = row_Count + 1
    else:
        for i in range(Groups_Cont_count, rowCount):
            newRow = container.AddNewRow(sysid,True)
            container_column_values  = attrValue[0][row_Count]
            for col_name, col_value in container_column_values.items():
                newRow[col_name] = col_value
            try:
                newRow.Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
            except:
                Log.Info("contname  "+str(contname))
            row_Count = row_Count + 1

def applyProductSelection(product):
    systemContainer = product.GetContainerByName('CE_SystemGroup_Cont')
    selectedProducts = product.Attr('CE_Product_Choices').SelectedValues
    for row in systemContainer.Rows:
        if row.IsSelected:
            systemGroupProduct = row.Product
            productContainer = systemGroupProduct.GetContainerByName('CE_System_Cont')
            for value in selectedProducts:
                newRow = productContainer.AddNewRow(value.ValueCode + '_cpq',True)
                newRow['product Name'] = value.Display
                newRow.ApplyProductChanges()
            productContainer.Calculate()
            systemGroupProduct.ApplyRules()
            row.ApplyProductChanges()
    systemContainer.Calculate()
    product.Messages.Add('Products are successfully applied against the Selected System')

def populateGroupContainer(product, contname, sysid, attrValue, attr_name):
    Groups_Cont = product.GetContainerByName(contname)
    Groups_Cont_row = Groups_Cont.Rows
    if Groups_Cont_row:
        Groups_Cont_count = Groups_Cont_row.Count
    else:
        Groups_Cont_count = 0
    rowCount = len(attrValue[0])
    ##Log.Info('-row_Count--'+str(rowCount)+' --contname-- '+str(contname)+' --contcount-- '+str(Groups_Cont_count)+' --sysid-- '+str(sysid)+' --attr_name-- '+str(attr_name) + str(attrValue))
    AddRows(rowCount, Groups_Cont, Groups_Cont_count, attrValue, attr_name, contname, sysid)

def ChildlevelDataMapping(product, values):
    Log.Info('product name in child level = '+str(product.Name))
    if product.Name =='Experion Enterprise System' and Experion_dict:
        GS_DEF_CONT_ATT_DICT.Experion_system_update(product,Experion_dict)
    SM_Node_Supplier = {'Honeywell':'Honeywell', 'Customer_Supplied' : 'Customer Supplied'}
    SM_Marshalling_Option = {'Hardware_Marshalling_with_Other' : 'Hardware Marshalling with Other', 'Hardware_Marshalling_with_P+F' : 'Hardware Marshalling with P+F', 'Universal_Marshalling' : 'Universal Marshalling'} 
    SM_Enclosure =  {'Cabinet' : 'Cabinet', 'Universal Safety Cab-1.3M' : 'Universal Safety Cab-1.3M'}
    UOC_Process_Type_Labour = {'None':'None', 'Continuous':'Continuous', 'ContinuousInterlock' : 'Continuous + Interlock', 'ContinuousSequence' : 'Continuous + Sequence','ContinuousInterlockSequence':'Continuous + Interlock + Sequence','BatchPharma':'Batch - Pharma','BatchChemical':'Batch - Chemical'}
    SM_RG_S300 = {'N' : 'Non Redundant S300', 'S' : 'Redundant S300', 'X' : 'No S300'}
    SM_RG_PUIO_Count = {'C' : '96', 'B' : '64', 'A' : '32', 'X' : '0'}
    SM_RG_PDIO_Count = {'C' : '96', 'B' : '64', 'A' : '32', 'X' : '0'}
    UOC_Input_Quality_Specific_Labour = {'FunctionPlanavailableSimple' : 'Function Plan available(Simple correction necessary) 15 %','FunctionPlanavailableOne' : 'Function Plan available(One revision) 40 %','OnlyverbalDescription' : 'Only verbal Description(Function Plan must be developed from scratch) 100%'}
    UOC_Labor = {'GESEgypt':'GES Egypt', 'GESUzbekistan':'GES Uzbekistan', 'GESRomania':'GES Romania', 'GESChina':'GES China', 'GESIndia':'GES India', 'None':'None'}
    PLC_Labor = {'GESEgypt':'GES Egypt', 'GESUzbekistan':'GES Uzbekistan', 'GESRomania':'GES Romania', 'GESChina':'GES China', 'GESIndia':'GES India', 'None':'None'}
    SM_Impl_Method_Labour = {'StandardBuildEstimate':'Standard Build Estimate', 'NonStandardBuildEstimate':'Non-Standard Build Estimate'}
    uoc_controller_type = {'NonRedundant': 'Non Redundant', 'Redundant':'Redundant'}
    PLC_Media_Delivery = {'PD': 'Physical Delivery', 'ED':'Electronic Download'}
    column_mapping = {
        'Node_Supplier': SM_Node_Supplier,
        'Marshalling_Option' : SM_Marshalling_Option,
        'SM_Enclosure Type' : SM_Enclosure,
        'UOC_Process_Type_Labour': UOC_Process_Type_Labour,
        'UOC_Input_Quality_Specific_Labour': UOC_Input_Quality_Specific_Labour,
        'UOC_Ges_Location_Labour': UOC_Labor,
        'Implementation_Methodology':SM_Impl_Method_Labour,
        'GES_Location' : UOC_Labor,
        'PLC_Ges_Location': PLC_Labor,
        'GES_Location' : PLC_Labor,
        'UOC_Controller_Type':uoc_controller_type,
        'PLC_Media_Delivery' : PLC_Media_Delivery
    }
    columnMappingCode = {
        'S300' : SM_RG_S300,
        'PUIO_Count' : SM_RG_PUIO_Count,
        'PDIO_Count' : SM_RG_PDIO_Count
    }
    level2_attribute = getProductAttributes(product)
    r2qAttr = values.keys()
    ##Log.Info("r2qAttr = "+str(r2qAttr))
    for attr_name in level2_attribute:
        if product.Attr(attr_name).Allowed == False:
            product.AllowAttr(attr_name)
        if attr_name in r2qAttr and 'message' not in attr_name and 'Header' not in attr_name:
            distype = product.Attr(attr_name).DisplayType
            attr_val = values[attr_name]
            attr_type = str(type(attr_val))
            list_none = True
            if 'list' in attr_type:
                if len(attr_val[0]) == 0:
                    list_none = False
            if distype != 'Container':
                if attrValueCheck(product, attr_name, attr_val):
                    ##Log.Info("inside not cont = "+str(attr_name)+" value="+str(attr_val))
                    attrValueSelection(product, distype, attr_name, attr_val)
            elif distype == 'Container' and list_none:
                if attr_name in  ["Series_C_Control_Groups_Cont", "Series_C_Remote_Groups_Cont", "ES_Group", "FDM_System_Group_Cont", "Experion_Enterprise_Cont", "Scada_CCR_Unit_Cont", "UOC_ControlGroup_Cont", "UOC_RemoteGroup_Cont", "SM_ControlGroup_Cont", "SM_RemoteGroup_Cont", "PLC_ControlGroup_Cont", "PLC_RemoteGroup_Cont","HC900_Cont"]:
                    ##Log.Info('ChildlevelDataMapping -- '+str(attr_name))
                    populateGroupContainer(product,mappingDict[attr_name][0], mappingDict[attr_name][1], attr_val, attr_name)
                ioTypeDict = {}
                if len(attr_val[0]) > 0:
                    if 'IO_Type' in attr_val[0][0].keys():
                        for row in attr_val[0]:
                            ioTypeDict[row['IO_Type']] = row

                identifierDict = {}
                if len(attr_val[0]) > 0:
                    for row_data in attr_val[0]:
                        if 'Identifiers' in row_data: 
                            identifierDict[row_data['Identifiers']] = row_data
                cgAnalogInputType = {}
                if len(attr_val[0]) > 0:
                    for row_data in attr_val[0]:
                        if 'Analog_Input_Type' in row_data: 
                            cgAnalogInputType[row_data['Analog_Input_Type']] = row_data

                cgAnalogOutputType = {}
                if len(attr_val[0]) > 0:
                    for row_data in attr_val[0]:
                        if 'Analog_Output_Type' in row_data: 
                            cgAnalogOutputType[row_data['Analog_Output_Type']] = row_data

                cgDigitalInputType = {}
                if len(attr_val[0]) > 0:
                    for row_data in attr_val[0]:
                        if 'Digital_Input_Type' in row_data: 
                            cgDigitalInputType[row_data['Digital_Input_Type']] = row_data

                cgDigitalOutputType = {}
                if len(attr_val[0]) > 0:
                    for row_data in attr_val[0]:
                        if 'Digital_Output_Type' in row_data: 
                            cgDigitalOutputType[row_data['Digital_Output_Type']] = row_data
                rgAnalogInputType = {}
                if len(attr_val[0]) > 0:
                    for row_data in attr_val[0]:
                        if 'Analog Input Type' in row_data: 
                            rgAnalogInputType[row_data['Analog Input Type']] = row_data

                rgAnalogOutputType = {}
                if len(attr_val[0]) > 0:
                    for row_data in attr_val[0]:
                        if 'Analog Output Type' in row_data: 
                            rgAnalogOutputType[row_data['Analog Output Type']] = row_data
                rgDigitalInputType = {}
                if len(attr_val[0]) > 0:
                    for row_data in attr_val[0]:
                        if 'Digital Input Type' in row_data: 
                            rgDigitalInputType[row_data['Digital Input Type']] = row_data

                rgDigitalOutputType = {}
                if len(attr_val[0]) > 0:
                    for row_data in attr_val[0]:
                        if 'Digital Output Type' in row_data: 
                            rgDigitalOutputType[row_data['Digital Output Type']] = row_data
                container_name = product.GetContainerByName(attr_name)
                if container_name.Rows.Count > 0:
                    containerAttrName = {}
                    c300AttrDict = get_c300AttrDict()
                    ##Log.Info('c300AttrDict = ' + str(c300AttrDict))
                    if attr_name in c300AttrDict.keys():
                        containerAttrName = c300AttrDict[attr_name]
                    for row in container_name.Rows:
                        if len(attr_val[0]) > 0:
                            if ioTypeDict:
                                if row['IO_Type'] in ioTypeDict.keys():
                                    attr_value1 = ioTypeDict[row['IO_Type']]
                                    for col_name, col_value in attr_value1.items():
                                        row[col_name] = col_value
                                        #Log.Info('col_name = ' + str(col_name) + ' col_value = ' + str(col_value))
                                        #row.GetColumnByName(col_name).SetAttributeValue(col_value)
                                        if containerAttrName:
                                            if col_name in containerAttrName.keys():
                                                if row.Product.Attr(containerAttrName[col_name]).DisplayType == 'DropDown':
                                                    row.Product.Attr(containerAttrName[col_name]).SelectDisplayValue(col_value)
                                                else:
                                                    row.Product.Attr(containerAttrName[col_name]).AssignValue(col_value)
                                                    row[col_name] = col_value
                            else:
                                if identifierDict:
                                    row_cont_val = 0
                                    for row1 in container_name.Rows:
                                        row1_identifier = None
                                        try:
                                            row1_identifier = row1['Identifiers']
                                        except Exception:
                                            pass 

                                        if row1_identifier and row1_identifier in identifierDict:
                                            matched_row_data = identifierDict[row1_identifier]
                                            for col_name, col_value in matched_row_data.items():
                                                row1[col_name] = col_value
                                                row1.GetColumnByName(col_name).SetAttributeValue(col_value)
                                                if containerAttrName:
                                                    if col_name in containerAttrName.keys():
                                                        if row1.Product.Attr(containerAttrName[col_name]).DisplayType == 'DropDown':
                                                            row1.Product.Attr(containerAttrName[col_name]).SelectDisplayValue(col_value)
                                                        else:
                                                            row1.Product.Attr(containerAttrName[col_name]).AssignValue(col_value)
                                elif cgAnalogInputType or cgAnalogOutputType or cgDigitalInputType or cgDigitalOutputType or rgAnalogInputType or rgAnalogOutputType or rgDigitalInputType or rgDigitalOutputType:
                                    inputOutputTypes = [cgAnalogInputType, cgAnalogOutputType, cgDigitalInputType, cgDigitalOutputType, rgAnalogInputType, rgAnalogOutputType, rgDigitalInputType, rgDigitalOutputType]
                                    inputOutputKeys = ['Analog_Input_Type', 'Analog_Output_Type', 'Digital_Input_Type', 'Digital_Output_Type', 'Analog Input Type', 'Analog Output Type', 'Digital Input Type', 'Digital Output Type']
                                    for dic, kys in zip(inputOutputTypes, inputOutputKeys):
                                        if dic:
                                            for row1 in container_name.Rows:
                                                row1_identifier = None
                                                try:
                                                    row1_identifier = row1[kys]
                                                except Exception:
                                                    pass 

                                                if row1_identifier and row1_identifier in dic:
                                                    matched_row_data = dic[row1_identifier]
                                                    for col_name, col_value in matched_row_data.items():
                                                        row1[col_name] = col_value
                                                        if containerAttrName:
                                                            if col_name in containerAttrName.keys():
                                                                if row1.Product.Attr(containerAttrName[col_name]).DisplayType == 'DropDown':
                                                                    row1.Product.Attr(containerAttrName[col_name]).SelectDisplayValue(col_value)
                                                                else:
                                                                    row1.Product.Attr(containerAttrName[col_name]).AssignValue(col_value)
                                else:
                                    row_cont_val = 0
                                    for row1 in container_name.Rows:
                                        if len(attr_val[0]) > 0 and len(attr_val[0]) >= row_cont_val+1:
                                            for col_name, col_value in attr_val[0][row_cont_val].items():
                                                row1[col_name] = col_value
                                                row1.GetColumnByName(col_name).SetAttributeValue(col_value)
                                                ##Log.Info("col_name=> "+str(col_name)+"col_value => "+str(col_value))
                                                try:
                                                    if col_name in column_mapping:
                                                        row1.GetColumnByName(col_name).SetAttributeValue(column_mapping[col_name][col_value])
                                                    if col_name in columnMappingCode:
                                                        row1[col_name] = columnMappingCode[col_name][col_value]
                                                        row1.GetColumnByName(col_name).ReferencingAttribute.SelectValue(columnMappingCode[col_name][col_value])
                                                except:
                                                    pass
                                                if containerAttrName:
                                                    try:
                                                        if row1.Product.Attr(containerAttrName[col_name]).DisplayType == 'DropDown':
                                                            row1.Product.Attr(containerAttrName[col_name]).SelectDisplayValue(col_value)
                                                            if col_name in columnMappingCode:
                                                                row1.Product.Attr(containerAttrName[col_name]).SelectDisplayValue(columnMappingCode[col_name][col_value])
                                                        else:
                                                            row1.Product.Attr(containerAttrName[col_name]).AssignValue(col_value)
                                                    except:
                                                        pass
                                        if len(attr_val[1]) > 0 and len(attr_val[1]) >= row_cont_val+1:
                                            ChildlevelDataMapping(row1.Product, attr_val[1][row_cont_val])
                                            row1.Product.ApplyRules()
                                        row_cont_val = row_cont_val + 1

                    if attr_name == "SM_CG_Cabinet_Details_Cont_Left":
                        R2QContainerRowAdded.cal_function(product)
                    if attr_name == "SM_RG_Cabinet_Details_Cont_Left":
                        R2QRMContainerRowAdded.cal_function(product)
                    '''if attr_name == "SM_RG_ATEX Compliance_and_Enclosure_Type_Cont":
                        R2QRemoteGroupAddContainerRows.addRows(product)'''

        

def addProd(containerDict):
    getPrd = SqlHelper.GetFirst("SELECT PA.PRODUCT_ID, PA.PRODUCT_NAME FROM products PA INNER JOIN product_versions PV ON PV.product_id = PA.PRODUCT_ID WHERE PA.PRODUCT_NAME = 'New / Expansion Project' AND PV.is_active = 'True'")
    if getPrd.PRODUCT_NAME:
        deleteProd(getPrd.PRODUCT_NAME)
    prd_id = int(getPrd.PRODUCT_ID)
    newProd = ProductHelper.CreateProduct(prd_id)
    newProd.ParseString('<* ExecuteScript(PS_R2Q_ProjectQueCont) *>')
    if newProd.GetContainerByName('Project_management_Labor_Container'):
        newProd.ParseString('<* ExecuteScript(PS_PM_Calc_Final_Hrs) *>')
    level1_attribute = getProductAttributes(newProd)

    MSID_GES_Location = {'EG':'GES Egypt', 'UZ':'GES Uzbekistan', 'RO':'GES Romania', 'CN':'GES China', 'IN':'GES India', 'None':'None'}
    Exp_Project_Categorization = {'None':'None', 'Small Project':'Small Project', 'Medium Large Project':'Medium/Large Project', 'Hardware only Project':'Hardware only Project'}
    column_mapping = {
        'GES_Location': MSID_GES_Location,
        'Project Categorization' : Exp_Project_Categorization
    }

    #for attr_name, attr_value in containerDict.items():
    for attr_name in containerDict:
        attr_value=containerDict[attr_name]
        if (attr_name in level1_attribute):
            distype = newProd.Attr(attr_name).DisplayType
            if distype != 'Container':
                attrValueSelection(newProd, distype, attr_name, attr_value)

    containerMapping = {
        'R2Q CE_System_Cont': newProd.GetContainerByName('CE_SystemGroup_Cont'),
        'R2Q_Project_Questions_Cont': newProd.GetContainerByName('CE_Project_Questions_Cont')
    }

    selectedProducts = []
    scopeValue=containerDict['CE_Scope_Choices'] if 'CE_Scope_Choices' in containerDict.Keys else ''
    #scopeValue = containerDict.get('CE_Scope_Choices', '')
    Level2_dict = []
    #for key, values in containerDict.items():
    for key in containerDict:
        values=containerDict[key]
        if key in containerMapping:
            container = containerMapping[key]
            if key == 'R2Q CE_System_Cont':
                for value in values[0]:
                    selectedProducts.append(value['Selected_Products'])
                    replacement_map =  {"R2Q C300 System": "C300 System","R2Q eServer System": "eServer System", "R2Q Field Device Manager": "Field Device Manager", "R2Q ControlEdge UOC System": "ControlEdge UOC System", "R2Q 3rd Party Devices/Systems Interface (SCADA)": "3rd Party Devices/Systems Interface (SCADA)", "R2Q Safety Manager ESD" :"Safety Manager ESD", "R2Q Safety Manager FGS": "Safety Manager FGS", "R2Q Experion Enterprise System" :"Experion Enterprise System", "R2Q ControlEdge PLC System": "ControlEdge PLC System"}
                    selectedProducts1 = [replacement_map.get(prod, prod) for prod in selectedProducts]
                    ##Log.Info("selectedProducts1"+str(selectedProducts1))
                    Quote.SetGlobal('selectedProducts1', str(selectedProducts1))
                    if container.Rows.Count > 0:
                        for row in container.Rows:
                            row.IsSelected = True
                            row.Product.Attr('CE_Scope_Choices').SelectDisplayValue(scopeValue)
                            replaced_value = selectedProducts1[0] if selectedProducts1 else ''
                            row['Selected_Products'] = replaced_value
                            choice_attr = newProd.Attr('CE_Product_Choices').Values
                            for i in choice_attr:
                                if i.Display in selectedProducts1:
                                    i.IsSelected = True
                applyProductSelection(newProd)
                Level2_dict.append(values)
            elif key == 'R2Q_Project_Questions_Cont':
                for value in values[0]:
                    if container.Rows.Count > 0:
                        for row in container.Rows:
                            for col_name, col_value in value.items():
                                row[col_name] = col_value
                                row.GetColumnByName(col_name).SetAttributeValue(col_value)
                                if col_name == 'Estimated_Project_Value_Cost':
                                    row.SetColumnValue(col_name, '3')
                                    row.GetColumnByName(col_name).SetAttributeValue('$1M - $5M')
                                try:
                                    if col_name in column_mapping:
                                        row.GetColumnByName(col_name).SetAttributeValue(column_mapping[col_name][col_value])
                                except:
                                    pass
            else:
                for value in values[0]:
                    if container.Rows.Count > 0:
                        for row in container.Rows:
                            for col_name, col_value in value.items():
                                row[col_name] = col_value
                    else:
                        new_row = container.AddNewRow()
                        for col_name, col_value in value.items():
                            new_row[col_name] = col_value

    #Level 2 System Group Level
    if len(Level2_dict[0]) > 0:
        order_products = {}
        row_index = 0
        for selected_Product_order in Level2_dict[0][0]:
            if selected_Product_order['Selected_Products'] =='R2Q C300 System':
                order_products["C300 System"] = Level2_dict[0][1][row_index]
            elif selected_Product_order['Selected_Products'] == 'R2Q Experion Enterprise System':
                order_products["Experion Enterprise System"] = Level2_dict[0][1][row_index]
            elif selected_Product_order['Selected_Products'] == 'R2Q eServer System':
                order_products["eServer System"] = Level2_dict[0][1][row_index]
            elif selected_Product_order['Selected_Products'] == 'R2Q Field Device Manager':
                order_products["Field Device Manager"] = Level2_dict[0][1][row_index]
            elif selected_Product_order['Selected_Products'] == 'R2Q 3rd Party Devices/Systems Interface (SCADA)':
                order_products["3rd Party Devices/Systems Interface (SCADA)"] = Level2_dict[0][1][row_index]
            elif selected_Product_order['Selected_Products'] == 'R2Q ControlEdge UOC System':
                order_products["ControlEdge UOC System"] = Level2_dict[0][1][row_index]
            elif selected_Product_order['Selected_Products'] == 'R2Q Safety Manager ESD':
                order_products["Safety Manager ESD"] = Level2_dict[0][1][row_index]
            elif selected_Product_order['Selected_Products'] == 'R2Q Safety Manager FGS':
                order_products["Safety Manager FGS"] = Level2_dict[0][1][row_index]
            elif selected_Product_order['Selected_Products'] == 'R2Q ControlEdge PLC System':
                order_products["ControlEdge PLC System"] = Level2_dict[0][1][row_index]
            elif selected_Product_order['Selected_Products'] == 'HC900 System':
                order_products["HC900 System"] = Level2_dict[0][1][row_index]
            elif selected_Product_order['Selected_Products'] == 'Terminal Manager':
                order_products["Terminal Manager"] = Level2_dict[0][1][row_index]
            row_index =  row_index + 1
        for ChildProduct in newProd.GetContainerByName('CE_SystemGroup_Cont').Rows:
            for key, values in order_products.items():
                system_prd_row = [row for row in ChildProduct.Product.GetContainerByName('CE_System_Cont').Rows if row['product Name'] == key]
                ChildlevelDataMapping(system_prd_row[0].Product, values)

    #Level3 Control Group
    #GS_DEF_CONT_ATT_DICT.container_functions(newProd,Quote)
    '''prdselectAttributedict = {}
    extractProductAttributes(prdselectAttributedict,newProd)
    Quote.SetGlobal('R2QdatanewProd', str(prdselectAttributedict))'''
    #newProd.ApplyRules()
    newProd.AddToQuote()
    Quote.SetGlobal('PerformanceUpload', "")
    Quote.Save(False)

def extractProductContainer(attrName, product):
    containerList = []
    containerProductList = []
    containerRows = product.GetContainerByName(attrName).Rows
    if containerRows.Count > 0:
        for contanierRow in containerRows:
            contanierRowDict = {}
            for col in contanierRow.Columns:
                contanierRowDict[col.Name] = contanierRow[col.Name]
            containerList.append(contanierRowDict)
            if contanierRow.Product and attrName not in ['R2Q_Project_Questions_Cont']:
                selectAttributedict_level = {}
                select_r2qdict={}
                extractProductAttributes(selectAttributedict_level, contanierRow.Product,select_r2qdict)
                containerProductList.append(selectAttributedict_level)
    return [containerList , containerProductList]

def extractProductAttributes(attributedict, product, select_r2qdict):
    for attr in product.Attributes:
        if attr.DisplayType == 'Container':
            if attr.Name not in attributedict:
                attributedict[attr.Name] = extractProductContainer(attr.Name, product)
            if attr.Name not in select_r2qdict:
                select_r2qdict[attr.Name] = extractProductContainer(attr.Name, product)
        else:
            if product.Attr(attr.Name).GetValue() != '':
                if attr.Name not in attributedict:
                    attributedict[attr.Name] = product.Attr(attr.Name).GetValue()
                if attr.Name not in select_r2qdict:
                    select_r2qdict[attr.Name] = product.Attr(attr.Name).GetValue()
        if attr.Name in ('Network_Firewall_Required','Opc_server_required','OPC_server_redundancy_required','Domain_Controller_Required','CMS Flex Station Qty 0_60'):
            Experion_dict[attr.Name]=product.Attr(attr.Name).GetValue()

test = str(Session['SelectedAttsData'])
saveAction = Quote.GetCustomField("R2Q_Save").Content
if saveAction != 'Save':
    selectAttributedict = OrderedDictionary()
    select_r2qdict = {}
    extractProductAttributes(selectAttributedict,Product,select_r2qdict)
    Session['SelectedAttsData'] = select_r2qdict
    #Session['select_r2qdict'] = select_r2qdict
    Quote.SetGlobal('R2Qdataorddict', JsonHelper.Serialize(selectAttributedict))
    #Quote.SetGlobal('R2Qdata', str(normaldict).replace('null', '""'))
    #Quote.SetGlobal('R2Qdata', str(selectAttributedict))
    Quote.SetGlobal('R2Qdata', str(select_r2qdict))
    Quote.GetCustomField('C300 Cabinet Count').Content = '0'
    Quote.GetCustomField('SM FGS Cabinet Count').Content = '0'
    Quote.GetCustomField('SM ESD Cabinet Count').Content = '0'
    selectAttributedictkey=eval((Quote.GetGlobal("R2Qdataorddict")).replace('null', '""'))
    data = addProd(selectAttributedictkey)

Session['R2Q_CompositeNumber'] = Quote.CompositeNumber
SellPricesStrategy = Product.Attr('Sell Price Strategy').SelectedValue.Display
customerBudget = Product.Attr('Customer_Budget_TextField').GetValue()
Quote.GetCustomField("SellPricestrategy").Content = SellPricesStrategy
Quote.GetCustomField("CustomerBudget").Content= customerBudget
SelectCategory = Product.Attr('R2Q Select Category').SelectedValue.Display
Quote.GetCustomField("R2Q_Category_PRJT").Content = SelectCategory
Log.Info('-------r2q addtoquote ended---')