migSys = Product.Attr('TPA_What_system_are_we_migrating').GetValue()
if  migSys == "TPA Alcont":
    Product.Attr('TPA_How_many_process_scada_points_are_licensed_currently_in_existing_PMD').AssignValue(str(0))
    Product.Attr('TPA_How_many_flex_licenses_are_currently_licensed_in_existing_PMD').AssignValue(str(0))
    Product.Attr('TPA_How_many_multi_window_licenses_are_currently_licensed_in_existing_PMD').AssignValue(str(0))
    Product.Attr('TPA_How_many_PMD_systems_need_to_publish_DSA_data_in_DSA_community').AssignValue(str(0))
elif migSys == "PMD R61x or older":
    Product.Attr('TPA_How_many_PMD_systems_need_to_publish_DSA_data_in_DSA_community').AssignValue(str(0))
elif migSys == "PMD R7xx (>R612)":
    Product.Attr('TPA_How_many_PFI_Pulse_input_channels_are_in_existing_system_which_need_to_be_replaced_with_new_solution').AssignValue(str(0))
    Product.Attr('TPA_How_many_PMD_systems_need_to_publish_DSA_data_in_DSA_community').AssignValue(str(0))
elif migSys in ["PMD R80x" , "PMD R83x" ,"PMD R90x" ,"PMD R91x"]:
    Product.Attr('TPA_How_many_PFI_Pulse_input_channels_are_in_existing_system_which_need_to_be_replaced_with_new_solution').AssignValue(str(0))
    Product.Attr('TPA_How_many_XPRs_VPRs_which_has_IO_in_same_rack_are_in_the_system').AssignValue(str(0))

Session['TPA_System_migrating'] = Product.Attr('TPA_What_system_are_we_migrating').GetValue()