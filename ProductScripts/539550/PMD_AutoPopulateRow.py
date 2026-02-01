# ================================================================================================
# Component: PMD System
# Author: Dan Bragdon
# Purpose: This is used to create a adding row in a container having the attributes when product is loaded.
# Date: 02/24/2022
# ================================================================================================
def getContainer(Name):
    return Product.GetContainerByName(Name)

attrs = ["PMD_Cabinet_Rack_Mounting_cont","PMD_Controllers_2xProfibus_cont","PMD_Controllers_2xProfinet_cont","PMD_Cross_Connection_Cabinets_Cont","PMD_Cross_Connection_Cabinets_Cont_PLCIO","PMD_Cross_Connection_Cabling_Terminal_Cont","PMD_Cross_Connection_Cabling_Terminal_Cont_PLCIO","PMD_Field Power Supply_Cont","PMD_Field Power Supply_Cont_PLCIO","PMD_Field_Pow_Supp_Cont","PMD_IO_Ext_Rack_Cont","PMD_IO_Extension_Cabinet_Cont","PMD_Optical_Link_Modules_cont","PMD_Optional_Item_IO_Cont","PMD_PN_DP_Gateways_cont","PMD_Profibus_Active_End_Resistors_cont","PMD_Profibus_Connectors_cont","PMD_Profibus_Coupler_cont","PMD_Profibus_PA_Cont","PMD_Profibus_Repeaters_Cont","PMD_Profinet_Switches_cont","PMD_Pulse_input_IO_KIT_PMD_Profibus_Profinet_Cont","PMD_System Power Supply_Cont","PMD_CC_Cards","PMD_Labour_Details","PMD_General_Input","PMD_IO_ControlEdge_PLC_IO_Cards","PMD_CE_IO_Rack_Cab","PMD_Labour_Details_2","PMD_labour_cont_1","PMD Labor Additional Custom Deliverable","PMD_Add_on_Licenses","PMD_CE_UOC_Licences","PMD_product_family","Labor_Details_New/Expansion_Cont","PMD_Profibus_Drives_Cont","CE_General_Inputs_Cont"]
for attr in attrs:
    container = getContainer(attr)
    if container.Rows.Count == 0:
        container.AddNewRow(True)
        container.Calculate()