import ProductUtil as pu
selections = {
    '4SN' : {'POS' : '5', 'AllowedValues': None, "DisallowedValues" : ['U', 'V', 'W','Y'], 'defaultSelection': 'S'},
    '4N' : {'POS' : '14', 'AllowedValues': None, "DisallowedValues" : ['R'], 'defaultSelection': 'R'},
    '416SN' : {'POS' : '16', 'AllowedValues': ['X'], "DisallowedValues" : None, 'defaultSelection': 'X'},
    '4X' : {'POS' : '5', 'AllowedValues': ['U', 'V', 'W','Y'], "DisallowedValues" : None,'defaultSelection': 'U'},
    '910X' : {'POS' : '13', 'AllowedValues': ['X'], "DisallowedValues" : None,'defaultSelection': 'F'},
    '3SP' : {'POS' : '3', 'AllowedValues': ['B'], "DisallowedValues" : None,'defaultSelection': 'B'},
    # 1
    '69C' : {'POS' : '9', 'AllowedValues': ['C'], "DisallowedValues" : None,'defaultSelection': 'C'},
    '610X' : {'POS' : '10', 'AllowedValues': ['X'], "DisallowedValues" : None,'defaultSelection': 'X'},
    # 2
    '79X' : {'POS' : '9', 'AllowedValues': ['X'], "DisallowedValues" : None,'defaultSelection': 'X'},
    '710C' : {'POS' : '10', 'AllowedValues': ['C'], "DisallowedValues" : None,'defaultSelection': 'C'},
    # 3
    '69B' : {'POS' : '9', 'AllowedValues': ['B'], "DisallowedValues" : None,'defaultSelection': 'B'},
    '67M' : {'POS' : '7', 'AllowedValues': ['M' ,'U','I'], "DisallowedValues" : None,'defaultSelection': 'M'},
    # 4
    '710B' : {'POS' : '10', 'AllowedValues': ['B'], "DisallowedValues" : None,'defaultSelection': 'B'},
    '76M' : {'POS' : '6', 'AllowedValues': ['M' ,'U','I'], "DisallowedValues" : None,'defaultSelection': 'M'},
    # 5
    '611Q' : {'POS' : '11', 'AllowedValues': ['Q','D'], "DisallowedValues" : None,'defaultSelection': 'Q'},
    }

error_msgs = []

def disallowValues(lst, dropdownlist,selectedValue,attr_name,defaultSelection):
    if lst:
        flag = False
        for i in dropdownlist:
            if i.ValueCode in lst:
                if selectedValue == i.ValueCode:
                    Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName(attr_name).ReferencingAttribute.SelectValue(defaultSelection)
                    Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName(attr_name).SetAttributeValue(defaultSelection)
                    flag = True
                i.Allowed = False
            elif i.ValueCode not in lst:
                i.Allowed = True
        return flag


def allowValues(lst,dropdownlist,selectedValue,attr_name,defaultSelection):
    if lst:
        flag = False
        for i in dropdownlist:
            if i.ValueCode in lst:
                i.Allowed = True
            elif i.ValueCode not in lst:
                if selectedValue == i.ValueCode:
                    Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName(attr_name).ReferencingAttribute.SelectValue(defaultSelection)
                    Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName(attr_name).SetAttributeValue(defaultSelection)
                    flag = True
                i.Allowed = False
        return flag


def setDropdownSelections(sel, Product,selectedValue):
    if selections[sel]['AllowedValues'] is None:
        attr_name = SqlHelper.GetFirst('select * from CT_SM_Remote_Identifier_Modifier where POS='+str(selections[sel]['POS'])).IM_Name
        dropdownlist = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName(attr_name).ReferencingAttribute.Values
        lst = selections[sel]["DisallowedValues"]
        defaultSelection = selections[sel]["defaultSelection"]
        flag = disallowValues(lst,dropdownlist,selectedValue,attr_name,defaultSelection)
        return flag
    elif selections[sel]['AllowedValues'] is not None:
        attr_name = SqlHelper.GetFirst('select * from CT_SM_Remote_Identifier_Modifier where POS='+str(selections[sel]['POS'])).IM_Name
        dropdownlist = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName(attr_name).ReferencingAttribute.Values
        lst = selections[sel]["AllowedValues"]
        defaultSelection = selections[sel]["defaultSelection"]
        flag = allowValues(lst,dropdownlist,selectedValue,attr_name,defaultSelection)
        return flag

def checkFourthPosition(value, im_table, Product):
    forteenPos = ''
    sixteenPos = ''
    if value:
        if len(value) <=4:
            return
        fourthPos = value[3].upper()
        fifthPos = value[4].upper()
        if len(value) >=14:
            forteenPos = value[13].upper()
        if len(value) >=16:
            sixteenPos = value[15].upper()
    else:
        fourthPos = im_table['4'].upper()
        fifthPos = im_table['5'].upper()
        forteenPos = im_table['14'].upper()
        sixteenPos = im_table['16'].upper()

    if (fourthPos in ['S','N']): # CXCPQ-31218
        flag = False
        if not value:
            selection = '4SN'
            flag = setDropdownSelections(selection, Product, fifthPos)
            attr_name = SqlHelper.GetFirst('select * from CT_SM_Remote_Identifier_Modifier where POS='+str(5)).IM_Name
            fifthPos = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName(attr_name).Value
        Trace.Write("Fifth: " + str(fifthPos))
        if (fifthPos in ['U', 'V', 'W','Y'] ) and value:
            error_msgs.append('When S300 is selected available fiber optics extenders are only 5 = S, T, M or N.')
            pu.addMessage(Product , 'When S300 is selected available fiber optics extenders are only 5 = S, T, M or N.')
        if flag:
            pu.addMessage(Product , 'When S300 is selected available fiber optics extenders are only 5 = S, T, M or N.')

    if (fourthPos in ['S','N']):
        flag = False
        if not value:
            selection = '416SN'
            flag = setDropdownSelections(selection, Product, sixteenPos)
            attr_name = SqlHelper.GetFirst('select * from CT_SM_Remote_Identifier_Modifier where POS='+str(16)).IM_Name
            sixteenPos = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName(attr_name).Value
        Trace.Write("sixteenPos: " + str(sixteenPos))
        if sixteenPos != 'X' and value:
            error_msgs.append('If S300 = Redundant S300/Non-Redundant S300, then External (24VDC) terminal block cannot be = Ext TB')
            pu.addMessage(Product , 'If S300 = Redundant S300/Non-Redundant S300, then External (24VDC) terminal block cannot be = Ext TB')
        if flag:
            pu.addMessage(Product , 'If S300 = Redundant S300/Non-Redundant S300, then External (24VDC) terminal block cannot be = Ext TB')

    if fourthPos == "N":
        flag = False
        if not value:
            selection = '4N'
            flag = setDropdownSelections(selection, Product, forteenPos)
            attr_name = SqlHelper.GetFirst('select * from CT_SM_Remote_Identifier_Modifier where POS='+str(14)).IM_Name
            forteenPos = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName(attr_name).Value
        Trace.Write("forteenPos: " + str(forteenPos) + str(flag))

        if forteenPos != "X" and value:
            error_msgs.append('If S300 = Non-Redundant S300, then IO Redundancy cannot be select as Redundant.')
            pu.addMessage(Product , 'If S300 = Non-Redundant S300, then IO Redundancy cannot be select as Redundant.')
        if flag:
            pu.addMessage(Product , 'If S300 = Non-Redundant S300, then IO Redundancy cannot be select as Redundant.')

    if fourthPos == 'X': # CXCPQ-31284
        flag = False
        if not value:
            selection = '4X'
            flag = setDropdownSelections(selection,Product,fifthPos)
            attr_name = SqlHelper.GetFirst('select * from CT_SM_Remote_Identifier_Modifier where POS='+str(5)).IM_Name
            fifthPos = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName(attr_name).Value
        Trace.Write("Fifth: " + str(fifthPos))
        if (fifthPos not in  ['U', 'V', 'W','Y'] ) and value:
            error_msgs.append('If S300 = No S300, then Fiber Optic Extender cannot be (Single Mode x4 EDS-408A or Single Mode x4 EDS-305 or Multi Mode x4 EDS-408A or Multi Mode x4 EDS-305)')
            pu.addMessage(Product , 'If S300 = No S300, then Fiber Optic Extender cannot be (Single Mode x4 EDS-408A or Single Mode x4 EDS-305 or Multi Mode x4 EDS-408A or Multi Mode x4 EDS-305)')
        if flag:
            pu.addMessage(Product , 'If S300 = No S300, then Fiber Optic Extender cannot be (Single Mode x4 EDS-408A or Single Mode x4 EDS-305 or Multi Mode x4 EDS-408A or Multi Mode x4 EDS-305)')

# Nine Position----------------------------------------------------------------------
def checkNineTenPosition(value,im_table,Product):
    if value:
        if len(value) <13:
            return
        ninePos = value[8].upper()
        tenPos = value[9].upper()
        thirteenPos = value[12].upper()
    else:
        ninePos = im_table['9'].upper()
        tenPos = im_table['10'].upper()
        thirteenPos = im_table['13'].upper()
    if ninePos == 'X' and tenPos != 'X': #CXCPQ-31285
        flag = False
        if not value:
            selection = '910X'
            flag = setDropdownSelections(selection,Product,thirteenPos)
            #----------------
        if thirteenPos != 'X' and value:
            error_msgs.append('FC-TALARM01 and FC-TELD-0001 are not available for configurations with only PDIO.')
            pu.addMessage(Product , 'FC-TALARM01 and FC-TELD-0001 are not available for configurations with only PDIO.')
        if flag:
            pu.addMessage(Product , 'FC-TALARM01 and FC-TELD-0001 are not available for configurations with only PDIO.')

# 6-7 Pos----------------------------
def checkSixthSeventhPosition(value,im_table,Product):
    sixthPos='';sevenPos='';thirdPos='';ninePos='';tenPos='';elePos=''
    if value:
        if len(value) >=7:
            sixthPos = value[5].upper()
            sevenPos = value[6].upper()
            thirdPos = value[2].upper()
        if len(value) >=9:
            ninePos = value[8].upper()
        if len(value) >=10:
            tenPos = value[9].upper()
        if len(value) >=11:
            elePos = value[10].upper()
    else:
        sixthPos = im_table['6'].upper()
        sevenPos = im_table['7'].upper()
        thirdPos = im_table['3'].upper()
        ninePos = im_table['9'].upper()
        tenPos = im_table['10'].upper()
        elePos = im_table['11'].upper()

    if (sixthPos in ['I', 'A','B','C']) or (sevenPos in ['I', 'A','B','C']):
        flag = False
        if not value:
            selection = '3SP'
            flag = setDropdownSelections(selection,Product,thirdPos)
        if thirdPos != 'B' and value: # CXCPQ-31507
            error_msgs.append('For Intrinsically Safe systems all Field Termination Assemblies must have an Intrinsically Safe option selected to ensure the correct system labels are generated.')
            pu.addMessage(Product , 'For Intrinsically Safe systems all Field Termination Assemblies must have an Intrinsically Safe option selected to ensure the correct system labels are generated.')
        if flag:
            pu.addMessage(Product , 'For Intrinsically Safe systems all Field Termination Assemblies must have an Intrinsically Safe option selected to ensure the correct system labels are generated.')
    
    if sixthPos in ['A', 'B']: #CXCPQ-31520-1
        flag = False;flag_10=False;flag_9=False
        '''if not value:
            selection = '69C'
            selection_10 = '610X'
            flag_9 = setDropdownSelections(selection,Product,ninePos)
            flag_10 = setDropdownSelections(selection_10,Product,tenPos)'''

        if  ninePos != 'C' or tenPos != 'X' and value:
            error_msgs.append('If Field Termination Assembly for PUIO = "32 IS, 64 Non-IS" or "64 IS, 32 Non-IS", then PUIO Count should be 96 and PDIO Count should be 0.')
            pu.addMessage(Product , 'If Field Termination Assembly for PUIO = "32 IS, 64 Non-IS" or "64 IS, 32 Non-IS", then PUIO Count should be 96 and PDIO Count should be 0.')
        '''if flag_10 or flag_9:
            pu.addMessage(Product , 'If Field Termination Assembly for PUIO = "32 IS, 64 Non-IS" or "64 IS, 32 Non-IS", then PUIO Count should be 96 and PDIO Count should be 0.')'''


    if sevenPos in ['A', 'B']: #CXCPQ-31520-2
        flag = False;flag_10=False;flag_9=False
        '''if not value:
            selection = '79X'
            selection_10 = '710C'
            flag_9 = setDropdownSelections(selection,Product,ninePos)
            flag_10 = setDropdownSelections(selection_10,Product,tenPos)'''

        if  ninePos != 'X' or tenPos != 'C' and value:
            error_msgs.append('If Field Termination Assembly for PDIO = "32 IS, 64 Non-IS" or "64 IS, 32 Non-IS", then PDIO Count should be 96 and PUIO Count should be 0.')
            pu.addMessage(Product , 'If Field Termination Assembly for PDIO = "32 IS, 64 Non-IS" or "64 IS, 32 Non-IS", then PDIO Count should be 96 and PUIO Count should be 0.')
        '''if flag_10 or flag_9:
            pu.addMessage(Product , 'If Field Termination Assembly for PDIO = "32 IS, 64 Non-IS" or "64 IS, 32 Non-IS", then PDIO Count should be 96 and PUIO Count should be 0.')'''

    if sixthPos == 'C': #CXCPQ-31520-3
        flag = False;flag_7=False;flag_9=False
        if not value:
            selection = '69B'
            selection_7 = '67M'
            flag_9 = setDropdownSelections(selection,Product,ninePos)
            flag_7 = setDropdownSelections(selection_7,Product,sevenPos)

        if  ninePos != 'B' or sevenPos not in ['M', 'U', 'I'] and value:
            Trace.Write('Value33-----' + str(value))
            if str(type(value)) != "<type 'NoneType'>":
                error_msgs.append('If Field Termination Assembly for PUIO = "32 IS, 32 Non-IS", then PUIO Count should be 64 and Field Termination Assembly for PDIO should be (Default Marshaling FC-TDIO51/52 or Universal Marshalling, PTA or Intrinsically Safe).')
                pu.addMessage(Product , 'If Field Termination Assembly for PUIO = "32 IS, 32 Non-IS", then PUIO Count should be 64 and Field Termination Assembly for PDIO should be (Default Marshaling FC-TDIO51/52 or Universal Marshalling, PTA or Intrinsically Safe).')
        if flag_7 or flag_9:
            pu.addMessage(Product , 'If Field Termination Assembly for PUIO = "32 IS, 32 Non-IS", then PUIO Count should be 64 and Field Termination Assembly for PDIO should be (Default Marshaling FC-TDIO51/52 or Universal Marshalling, PTA or Intrinsically Safe).')
    
    if sevenPos == 'C': #CXCPQ-31520-4
        flag = False;flag_10=False;flag_6=False
        if not value:
            selection = '710B'
            selection_6 = '76M'
            flag_10 = setDropdownSelections(selection,Product,tenPos)
            flag_6 = setDropdownSelections(selection_6,Product,sixthPos)

        if  tenPos != 'B' or sixthPos not in ['M', 'U', 'I'] and value:
            Trace.Write('Value44-----' + str(value))
            if str(type(value)) != "<type 'NoneType'>":
                Trace.Write('Value45-----')
                error_msgs.append('If Field Termination Assembly for PDIO = "32 IS, 32 Non-IS", then PDIO Count should be 64 and Field Termination Assembly for PUIO should be (Default Marshaling FC-TDIO51/52 or Universal Marshalling, PTA or Intrinsically Safe)')
                pu.addMessage(Product , 'If Field Termination Assembly for PDIO = "32 IS, 32 Non-IS", then PDIO Count should be 64 and Field Termination Assembly for PUIO should be (Default Marshaling FC-TDIO51/52 or Universal Marshalling, PTA or Intrinsically Safe)')
        if flag_10 or flag_6:
            pu.addMessage(Product , 'If Field Termination Assembly for PDIO = "32 IS, 32 Non-IS", then PDIO Count should be 64 and Field Termination Assembly for PUIO should be (Default Marshaling FC-TDIO51/52 or Universal Marshalling, PTA or Intrinsically Safe)')

    # Commented as requested in CXCPQ-35878
    # if sixthPos in ['I', 'A','B','C'] or sevenPos in ['I', 'A','B','C']: #CXCPQ-31520-5
    #     flag = False;flag_11=False
    #     '''if not value:
    #         selection = '611Q'
    #         flag_11 = setDropdownSelections(selection,Product,elePos)'''

    #     if  elePos not in ['Q', 'D'] and value:
    #         if str(type(value)) != "<type 'NoneType'>":
    #             error_msgs.append('If Field Termination Assembly for PUIO or Field Termination Assembly for PDIO is selected as "Intrinsically Safe" or "32 IS, 64 Non-IS" or "64 IS, 32 Non-IS" or "32 IS, 32 Non-IS" then Power Supply Type should be (20A AC/DC QUINT4+ PS or 24 VDC/DC QUINT4+ Supply)')
    #             pu.addMessage(Product , 'If Field Termination Assembly for PUIO or Field Termination Assembly for PDIO is selected as "Intrinsically Safe" or "32 IS, 64 Non-IS" or "64 IS, 32 Non-IS" or "32 IS, 32 Non-IS" then Power Supply Type should be (20A AC/DC QUINT4+ PS or 24 VDC/DC QUINT4+ Supply)')
    #     '''if flag_11:
    #         pu.addMessage(Product , 'If Field Termination Assembly for PUIO or Field Termination Assembly for PDIO is selected as "Intrinsically Safe" or "32 IS, 64 Non-IS" or "64 IS, 32 Non-IS" or "32 IS, 32 Non-IS" then Power Supply Type should be (20A AC/DC QUINT4+ PS or 24 VDC/DC QUINT4+ Supply)')'''


def manualChange(newValue):
    tableData = SqlHelper.GetList('select * from CT_SM_Remote_Identifier_Modifier')
    im_table = {}
    for im in tableData:
        if im.POS == '1':
            continue
        im_table[im.POS] = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName(im.IM_Name).Value
    checkFourthPosition(newValue, im_table, Product)
    checkNineTenPosition(newValue, im_table, Product)
    checkSixthSeventhPosition(newValue, im_table, Product)

def dropdownChange(newValue):
    tableData = SqlHelper.GetList('select * from CT_SM_Remote_Identifier_Modifier')
    im_table = {}
    for im in tableData:
        if im.POS == '1':
            continue
        im_table[im.POS] = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName(im.IM_Name).Value
    checkFourthPosition(newValue, im_table, Product)
    checkNineTenPosition(newValue, im_table, Product)
    checkSixthSeventhPosition(newValue, im_table, Product)

im_manual_entry = ''
cont_usc = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont')
if Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows.Count > 0:
    im_manual_entry = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').Value
if im_manual_entry:
    manualChange(im_manual_entry)
elif cont_usc.Rows.Count > 0:
    dropdownChange(None)

error_msg = Product.Attr('ErrorMessage').GetValue()
Trace.Write(error_msg)
for msg in error_msgs:
    if not error_msg:
        error_msg +=msg
    else:
        error_msg += '<br/>' + msg
Trace.Write('Error Message1: ' + str(error_msg))
Trace.Write(error_msg)
Product.Attr('ErrorMessage').AssignValue(error_msg)