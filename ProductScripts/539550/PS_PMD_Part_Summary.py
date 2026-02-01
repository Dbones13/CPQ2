try:
    import GS_PMD_ReadAttrs
    import GS_PMD_CC_Cards
    import GS_PMD_Display_Calcs
    import GS_PMD_Drive_Calcs
    import GS_PMD_Field_Pow_Supp
    import GS_PMD_IO_Extension_Cabinet
    import GS_PMD_Link_Gateway_Calcs
    import GS_PMD_Misc_Profibus_Profinet_Comp
    import GS_PMD_Motor_Controlling_Calcs
    import GS_PMD_Optical_Link_Modules
    import GS_PMD_Optional_Item_IO
    import GS_PMD_Other_Profibus_DP_Calcs
#   import GS_PMD_PN_DP_Gateways removed see line 83
    import GS_PMD_Profibus_Coupler
    import GS_PMD_Profibus_Modular_Calcs
    import GS_PMD_Profibus_Repeaters
    import GS_PMD_Profinet_Device_Support_Calcs
    import GS_PMD_Profinet_Switches
    import GS_PMD_System_Power_Supply
    import GS_PLC_UOC_PartUpdate
    import GS_PMD_FCE_Controllers
    import GS_PMD_CC_Cabinets
    import GS_PMD_Pulse_input_IO_KIT_PMD_Profibus_Profinet_Cont
    import GS_PMD_Profibus_Devices
    import GS_PMD_Addon
    import GS_PMD_UOC_Licenses
    import GS_PMD_Cross_Connection_Cabling_Terminal
    import GS_PMD_Field_Power_Supply
    import GS_PMD_Add_in_PLC_System
except Exception,e:
    Trace.Write("Error in PS_Part_Summary: module imports" + str(e))

try:
    attrs = GS_PMD_ReadAttrs.AttrStorage(Product)
except Exception,e:
    attrs = None
    Trace.Write("Error when Reading PMD System Attributes:" + str(e))
    #Product.ErrorMessages.Add("Error when Reading PMD System Attributes: " + str(e))

parts_dict = {}

if attrs:
    try:
        parts_dict = GS_PMD_CC_Cards.calc_display(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_CC_Cards: " + str(e))

    try:
        parts_dict = GS_PMD_Display_Calcs.calc_display(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Display_Calcs: " + str(e))

    try:
        parts_dict = GS_PMD_Field_Pow_Supp.calc_field_pow_supp(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Field_Pow_Supp: " + str(e))

    try:
        parts_dict = GS_PMD_IO_Extension_Cabinet.calc_display(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_IO_Extension_Cabinet: " + str(e))

    try:
        parts_dict = GS_PMD_Link_Gateway_Calcs.calc_link_gateway(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Link_Gateway_Calcs: " + str(e) )

    try:
        parts_dict = GS_PMD_Misc_Profibus_Profinet_Comp.calc_profib_conn(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Misc_Profibus_Profinet_Comp: " + str(e))

    try:
        parts_dict = GS_PMD_Motor_Controlling_Calcs.calc_motor_controlling(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Motor_Controlling_Calcs: " + str(e))

    try:
        parts_dict = GS_PMD_Optical_Link_Modules.calc_display(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Optical_Link_Modules: " + str(e))

    try:
        parts_dict = GS_PMD_Optional_Item_IO.calc_display(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Optional_Item_IO: " + str(e))

    try:
        parts_dict = GS_PMD_Other_Profibus_DP_Calcs.calc_other_profibus(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Other_Profibus_DP_Calcs: " + str(e))
    #removed due to same parts being added together for two different attributes
    #try:
    #    parts_dict = GS_PMD_PN_DP_Gateways.calc_display(parts_dict, attrs)
    #except Exception,e:
    #    Product.ErrorMessages.Add("Error in GS_PMD_PN_DP_Gateways: " + str(e))

    try:
        parts_dict = GS_PMD_Profibus_Coupler.calc_display(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Profibus_Coupler: " + str(e))

    try:
        parts_dict = GS_PMD_Profibus_Modular_Calcs.calc_profibus_modular(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Profibus_Modular_Calcs: " + str(e))

    try:
        parts_dict = GS_PMD_Profibus_Repeaters.calc_display(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Profibus_Repeaters: " + str(e))

    try:
        parts_dict = GS_PMD_Profinet_Device_Support_Calcs.calc_profinet(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Profinet_Device_Support_Calcs: " + str(e))

    try:
        parts_dict = GS_PMD_Profinet_Switches.calc_display(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Profinet_Switches: " + str(e))

    try:
        parts_dict = GS_PMD_System_Power_Supply.calc_display(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_System_Power_Supply: " + str(e))
    try:
        parts_dict = GS_PMD_FCE_Controllers.calc_fce_Controller(parts_dict, attrs)
    except Exception,e:
         Product.ErrorMessages.Add("Error in GS_PMD_FCE_Controllers: " + str(e))
    try:
        parts_dict =  GS_PMD_CC_Cabinets.calc_cc_cabinets(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_CC_Cabinets: " + str(e))

    try:
        parts_dict =  GS_PMD_Pulse_input_IO_KIT_PMD_Profibus_Profinet_Cont.calc_display(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Pulse_input_IO_KIT_PMD_Profibus_Profinet_Cont: " + str(e))

    try:
        parts_dict = GS_PMD_Profibus_Devices.calc_display(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Profibus_Devices : " + str(e))

    try:
        parts_dict = GS_PMD_Addon.calc_display(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Addon : " + str(e))

    try:
        parts_dict = GS_PMD_UOC_Licenses.calc_display(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_UOC_Licenses: " + str(e))

    try:
        parts_dict = GS_PMD_Cross_Connection_Cabling_Terminal.quantity_display(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Cross_Connection_Cabling_Terminal: " + str(e))
    try:
        parts_dict = GS_PMD_Field_Power_Supply.quantity_display(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Field_Power_Supply: " + str(e))
    try:
        parts_dict = GS_PMD_Add_in_PLC_System.pmd_plc_system(parts_dict, attrs)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PMD_Add_in_PLC_System: " + str(e))
    Trace.Write("Parts Dict: {0}".format(parts_dict))
    GS_PLC_UOC_PartUpdate.execute(Product, 'PMD_PartSummary_Cont', parts_dict)