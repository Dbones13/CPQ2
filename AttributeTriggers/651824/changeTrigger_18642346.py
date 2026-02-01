if Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue() == "":
    Product.Attr('C300_RG_UPC_Universal_IO_Count').SelectDisplayValue('32') 
if Product.Attr('C300_RG_UPC_Cab_Count').GetValue() =="":
	Product.Attr('C300_RG_UPC_Cab_Count').AssignValue('1')

#Family type
family_type = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
controller = Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
mounting = Product.Attr('Dummy_RG_IO_Mounting_Solution').GetValue()
mounting_options = {
	'Cabinet': 'Cabinet',
	'Mounting Panel': 'Mounting Panel',
	'Universal Process Cab - 1.3M': 'Universal Process Cab - 1.3M'
}
default_mounting = 'Cabinet'
if family_type == 'Series C' and controller != 'CN100 CEE':
	selected_mounting = mounting_options.get(mounting, default_mounting)
	Product.Attr('SerC_IO_Mounting_Solution').SelectDisplayValue(selected_mounting)

#mounting solution
def set_permissions(allowed_groups, disallowed_groups):
    for group in allowed_groups:
        for attr in attribute_groups[group]:
            Product.AllowAttr(attr)
    for group in disallowed_groups:
        for attr in attribute_groups[group]:
            Product.DisallowAttr(attr)
attribute_groups = {
   "seriesC": ["Header_15_close","Header_15_open","SerC_RG_Enhanced_Function_IO_Cont","SerC_RG_Enhanced_Function_IO_Cont2","Header_21_close","Header_21_open","C300_RG_Universal_IO_cont_1","C300_RG_Universal_IO_cont_2"],
   "seriesCM":["C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont", "C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1", "C300_CG_Universal_IO_Mark_1", "C300_CG_Universal_IO_Mark_2","Header_03_open","Header_03_close"],
   "turboM":["Header_16_open","Header_16_close","C300_TurboM_IOM_RG_Cont"],
   "cabinet":["Header_06_open","Header_06_close","C300_RG_UPC_Cab_Count","C300_RG_UPC_UIO2_Redundancy","C300_RG_UPC_Universal_IO_Count"],
   "DefaultsList":["Header_19_open","Header_19_close","SerC_RG_Group_label_Defaults_for_Cabinet","SerC_RG_CN100_I/O_HOVE","SerC_RG_Power_System_Vendor","SerC_RG_Percent_Installed_Spare(0-100%)","SerC_RG_Marshalling_Cabinet_Type","SerC_RG_Percentage_SSM_Cabinet (0-100%)"]
}

mounting_solution = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
seriesC_attrlist = ["Header_15_close","Header_15_open","SerC_RG_Enhanced_Function_IO_Cont","SerC_RG_Enhanced_Function_IO_Cont2","Header_21_close","Header_21_open","C300_RG_Universal_IO_cont_1","C300_RG_Universal_IO_cont_2"]
seriesCM_attrlist=["C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont", "C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1", "C300_CG_Universal_IO_Mark_1", "C300_CG_Universal_IO_Mark_2","Header_03_open","Header_03_close"]
turboM_attrlist=["Header_16_open","Header_16_close","C300_TurboM_IOM_RG_Cont"]

cabinet_attr = ["Header_06_open","Header_06_close","C300_RG_UPC_Cab_Count","C300_RG_UPC_UIO2_Redundancy","C300_RG_UPC_Universal_IO_Count"]
DefaultsList = ["Header_19_open","Header_19_close","SerC_RG_Group_label_Defaults_for_Cabinet","SerC_RG_CN100_I/O_HOVE","SerC_RG_Power_System_Vendor","SerC_RG_Percent_Installed_Spare(0-100%)","SerC_RG_Marshalling_Cabinet_Type","SerC_RG_Percentage_SSM_Cabinet (0-100%)"]

if mounting_solution != 'Universal Process Cab - 1.3M':
	if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue() == '':
		Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').AssignValue('0')
	if Product.Attr('SerC_RG_Percentage_SSM_Cabinet (0-100%)').GetValue() == '':
		Product.Attr('SerC_RG_Percentage_SSM_Cabinet (0-100%)').AssignValue('0')
	Product.Attr('SerC_RG_Power_System_Vendor').SelectDisplayValue('Phoenix Contact')


if mounting_solution == "Cabinet":
    if family_type == 'Series C' and controller != 'CN100 CEE':
        set_permissions(["DefaultsList"],["cabinet"])
    elif family_type == "Series C":
        set_permissions(["seriesC"], ["seriesCM", "turboM"])
    elif family_type == "Turbomachinery":
        set_permissions(["seriesC", "turboM"], ["seriesCM"])
    else:
        set_permissions(["seriesCM"], ["seriesC", "turboM"])
    if family_type == "Series-C Mark II":
        set_permissions(["DefaultsList"],[])
else:
    set_permissions(["cabinet"], ["seriesC", "seriesCM","turboM","DefaultsList"])