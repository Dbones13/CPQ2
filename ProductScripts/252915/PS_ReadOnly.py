def getContainer(Name):
    return Product.GetContainerByName(Name)
def ReadOnly(attrname):
    Product.Attr(attrname).Access = AttributeAccess.ReadOnly
def Editable(attrname):
    Product.Attr(attrname).Access = AttributeAccess.Editable

selectedProducts = list()
for row in getContainer("MSID_Product_Container").Rows:
    selectedProducts.append(row["Product Name"])
if "TPA/PMD Migration" in selectedProducts:

    ReadOnly('TPA_IO_replacement_with_Universal_Marshalling')
    ReadOnly('TPA_IO_replacement_without_Universal_Marshalling')
    ReadOnly('TPA_Calculated_amount_of_FCEs_to_be_included_in_new_system')
    migSys = Product.Attr('TPA_What_system_are_we_migrating').GetValue()
    doUKnow = Product.Attr('TPA_Do_you_know_the_number_of_huge_and_normal_TPA_PMD_HMI_graphics').GetValue()

    if migSys == "TPA Alcont":
        ReadOnly('TPA_How_many_process_scada_points_are_licensed_currently_in_existing_PMD')
        ReadOnly('TPA_How_many_flex_licenses_are_currently_licensed_in_existing_PMD')
        ReadOnly('TPA_How_many_multi_window_licenses_are_currently_licensed_in_existing_PMD')
    else:
        Editable('TPA_How_many_process_scada_points_are_licensed_currently_in_existing_PMD')
        Editable('TPA_How_many_flex_licenses_are_currently_licensed_in_existing_PMD')
        Editable('TPA_How_many_multi_window_licenses_are_currently_licensed_in_existing_PMD')

    if migSys in ["PMD R80x" , "PMD R83x","PMD R90x","PMD R91x"]:
        ReadOnly('TPA_How_many_XPRs_VPRs_which_has_IO_in_same_rack_are_in_the_system')
    else:
        Editable('TPA_How_many_XPRs_VPRs_which_has_IO_in_same_rack_are_in_the_system') 

    if migSys in ["TPA Alcont" , "PMD R61x or older"]:
        Editable('TPA_How_many_PFI_Pulse_input_channels_are_in_existing_system_which_need_to_be_replaced_with_new_solution')
    else:
        ReadOnly('TPA_How_many_PFI_Pulse_input_channels_are_in_existing_system_which_need_to_be_replaced_with_new_solution')

    if migSys  in ["PMD R80x" , "PMD R83x","PMD R90x","PMD R91x"]:
        Editable('TPA_How_many_PMD_systems_need_to_publish_DSA_data_in_DSA_community')
    else:
        ReadOnly('TPA_How_many_PMD_systems_need_to_publish_DSA_data_in_DSA_community')
    if doUKnow =="No":
        ReadOnly('TPA_Count_of_huge_TPA_PMD_HMI_graphics')
        ReadOnly('TPA_Count_of_normal_TPA_PMD_HMI_graphics')
        ReadOnly('TPA_Count_of_popup_displays')
    else:
        Editable('TPA_Count_of_huge_TPA_PMD_HMI_graphics')
        Editable('TPA_Count_of_normal_TPA_PMD_HMI_graphics')
        Editable('TPA_Count_of_popup_displays')

if "QCS RAE Upgrade" in selectedProducts:
    ReadOnly('QCS_Mig_Total_number_of_HC_900_IO_points')
if "FSC to SM IO Migration" in selectedProducts:
    ReadOnly('FSC_SM_IO_Total_ Calculated_SIC_cables')
