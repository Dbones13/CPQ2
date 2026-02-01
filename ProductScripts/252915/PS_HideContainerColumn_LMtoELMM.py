def getAttributeValue(Name):
    return Product.Attr(Name).GetValue()

def getContainer(Name):
    return Product.GetContainerByName(Name)

def hideColumn(container,Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format(container,Column))
    Product.ParseString('<*CTX( Container({}).Row(1).Column({}).Set() )*>'.format(container,Column))

def setDefaultColumnForDropdown(container,Column, value):
    Product.ParseString('<*CTX( Container({}).Row(1).Column({}).Set({}) )*>'.format(container,Column, value))

def visibleColumn(container,Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format(container,Column))

def isHidden(container,Column):
    return Product.ParseString('<*CTX( Container({}).Column({}).GetPermission )*>'.format(container,Column)) == 'Hidden'

def getContainer(Name):
    return Product.GetContainerByName(Name)
selectedProducts = Product.Attr('MSID_Selected_Products').GetValue().split('<br>')

if "LM to ELMM ControlEdge PLC" in selectedProducts:
    if getAttributeValue("MIgration_Scope_Choices") in ["LABOR"]:
        hideColumn("LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont", "LM_Current_Experion_Release")
        hideColumn("LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont", "LM_Does_The_Customer_Have_TPN_Release_R688.1_Or_Later")
        hideColumn("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_CE_Power_Input_Type")
        hideColumn("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_select_IO_network_topology")
        hideColumn("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_select_type_of_Switch_for_the_IO_network")
        container = Product.GetContainerByName('LM_to_ELMM_3rd_Party_Items')
        count = container.Rows.Count
        if count:
            for row in range(count,-1,-1):
                container.DeleteRow(row)
            container.Calculate()
    elif getAttributeValue("MIgration_Scope_Choices") in ["HW/SW", "HW/SW/LABOR"]:
        if isHidden("LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont", "LM_Current_Experion_Release"):
            visibleColumn("LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont", "LM_Current_Experion_Release")
            setDefaultColumnForDropdown("LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont", "LM_Current_Experion_Release", "No Experion")
        if isHidden("LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont", "LM_Does_The_Customer_Have_TPN_Release_R688.1_Or_Later"):
            visibleColumn("LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont", "LM_Does_The_Customer_Have_TPN_Release_R688.1_Or_Later")
            setDefaultColumnForDropdown("LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont", "LM_Does_The_Customer_Have_TPN_Release_R688.1_Or_Later", "No")
        if isHidden("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_CE_Power_Input_Type"):
            visibleColumn("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_CE_Power_Input_Type")
            setDefaultColumnForDropdown("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_CE_Power_Input_Type", "DC")
        if isHidden("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_select_IO_network_topology"):
            visibleColumn("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_select_IO_network_topology")
            setDefaultColumnForDropdown("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_select_IO_network_topology", "Star")
        if isHidden("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_select_type_of_Switch_for_the_IO_network"):
            visibleColumn("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_select_type_of_Switch_for_the_IO_network")
            setDefaultColumnForDropdown("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_select_type_of_Switch_for_the_IO_network", "Multimode Redundant")
        container = Product.GetContainerByName('LM_to_ELMM_3rd_Party_Items')
        count = container.Rows.Count
        if count == 0:
            for i in range(0,2):
                container.AddNewRow()
            container.Calculate()
    if getAttributeValue("MIgration_Scope_Choices") in ["HW/SW"]:
        hideColumn("LM_to_ELMM_Migration_Additional_IO_Cont", "LM_any_unsupported_instruction_in_the_LM_ladder_logic")
        hideColumn("LM_to_ELMM_Migration_Additional_IO_Cont", "qty_3party_customized_ladder_used_in_the_LM_0_100")
        hideColumn("LM_to_ELMM_Migration_Additional_IO_Cont", "qty_IO_points_to_be_rewired_0_5000")
    else:
        visibleColumn("LM_to_ELMM_Migration_Additional_IO_Cont", "LM_any_unsupported_instruction_in_the_LM_ladder_logic")
        visibleColumn("LM_to_ELMM_Migration_Additional_IO_Cont", "qty_3party_customized_ladder_used_in_the_LM_0_100")
        visibleColumn("LM_to_ELMM_Migration_Additional_IO_Cont", "qty_IO_points_to_be_rewired_0_5000")
        
    if getAttributeValue("MIgration_Scope_Choices") in ["HW/SW/LABOR", "LABOR"]:
        container = Product.GetContainerByName('LM_to_ELMM_Services')
        count = container.Rows.Count
        if count == 0:
            container.AddNewRow()
            container.Calculate()
    else:
        container = Product.GetContainerByName('LM_to_ELMM_Services')
        count = container.Rows.Count
        if count:
            container.DeleteRow(0)
        container.Calculate()
    lMELMMGeneralCont=  getContainer('LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont')
    for row in lMELMMGeneralCont.Rows:
        if row['Is_Honeywell_Providing_FTE_Cables'] == "No" or row['Is_Honeywell_Providing_FTE_Cables'] == "":
            hideColumn('LM_to_ELMM_ControlEdge_PLC_Cont', 'LM_average_Cable_length_for_IO_network_connection')
            hideColumn('LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont', 'Average_Cable_Length_For_PLC_Uplink')
        else:
            if isHidden('LM_to_ELMM_ControlEdge_PLC_Cont', 'LM_average_Cable_length_for_IO_network_connection'):
                visibleColumn('LM_to_ELMM_ControlEdge_PLC_Cont', 'LM_average_Cable_length_for_IO_network_connection')
                setDefaultColumnForDropdown('LM_to_ELMM_ControlEdge_PLC_Cont', 'LM_average_Cable_length_for_IO_network_connection', "10m")
            if isHidden('LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont', 'Average_Cable_Length_For_PLC_Uplink'):
                visibleColumn('LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont', 'Average_Cable_Length_For_PLC_Uplink')
                setDefaultColumnForDropdown('LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont', 'Average_Cable_Length_For_PLC_Uplink', "10m")
        if row['LM_Number_Of_Additional_Switches'] == "0" or row['LM_Number_Of_Additional_Switches'] == "":
            hideColumn('LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont', 'LM_Additional_Switch_Selection')
        else:
            if isHidden('LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont', 'LM_Additional_Switch_Selection'):
                visibleColumn('LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont', 'LM_Additional_Switch_Selection')

if 'TPS to Experion' in selectedProducts and getAttributeValue("MIgration_Scope_Choices") in ["LABOR"]:
    tps3rdparty = getContainer('TPS_to_EX_3rd_Party_Items')
    count = tps3rdparty.Rows.Count
    if count > 0:
        while count > 0:
            tps3rdparty.DeleteRow(count-1)
            count-=1
    if not isHidden("TPS_to_EX_3rd_Party_Items","Thin_Client_cables_and_adapters"):
        hideColumn("TPS_to_EX_3rd_Party_Items","Thin_Client_cables_and_adapters")

if 'TPS to Experion' in selectedProducts and getAttributeValue("MIgration_Scope_Choices") not in ["LABOR"]:
    if isHidden("TPS_to_EX_3rd_Party_Items","Thin_Client_cables_and_adapters"):
        visibleColumn("TPS_to_EX_3rd_Party_Items","Thin_Client_cables_and_adapters")
