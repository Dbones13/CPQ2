def SetDropDownDefaultvalue(Product):
    Tabdetails = Product.Tabs
    for tab in Tabdetails:
        if tab.Name == 'General Inputs':
            for attr in tab.Attributes:
                if attr.DisplayType=="DropDown" and attr.Required and attr.Name not in ["LAN Type","SerC_CG_Type_of_Controller_Required","CMS Multi Window Support Option Required?",'DMS Multi Window Support Option Required?',"SerC_CG_Ethernet_Interface","SerC_CG_Foundation_Fieldbus_Interface_required","SerC_GC_Profibus_Gateway_Interface","SerC_RG_Single_Mod_FOE_Type_for_Control_Grp_Cabt","Display Size_server","Display Size (Mobile Server)","Hardware Design Selection_ACE Node", "Additional_Station_Cabinet_Mounting_Type","ELCN Solution Required","QVCS Support","Multi Window Support (Flex Server)","Multi_WindowSupportFlex_Server"]:
                    if not attr.GetValue():
                        for val in attr.Values:
                            attr.SelectValue(val.ValueCode)
                            break
            break