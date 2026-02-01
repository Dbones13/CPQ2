def deleteRowsByCondition(container_name, io_types):
    cont = Product.GetContainerByName(container_name)
    rows_to_delete = [row.RowIndex for row in cont.Rows if row['IO_Type'] in io_types]
    for row_index in sorted(rows_to_delete, reverse=True):
        cont.DeleteRow(row_index)

ioFamilyType = Product.Attr('SerC_CG_IO_Family_Type').GetValue()

if ioFamilyType != 'Turbomachinery':
    Product.Attr('SerC_CG_R2Q_Power_System_Vendor').SelectDisplayValue('Phoenix Contact')
else:
    Product.DisallowAttr('SerC_CG_Universal_Marshalling_Cabinet')#Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').AssignValue('')
Product.Attr('SerC_CG_Marshalling_Cabinet_Type').SelectDisplayValue('Universal Marshalling')
Product.Attr('SerC_CG_R2Q_Percent_Installed_Spare').AssignValue('0')
Product.Attr('SerC_CG_Percent_SpareSpace_Marshalling_Cabinet').AssignValue('0')

if Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue() == '':
    Product.Attr('SerC_CG_Type_of_Controller_Required').SelectDisplayValue("CN100 I/O HIVE - C300 CEE")
cgName = Product.Attr('Series_C_CG_Name').GetValue()
controller = Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
defaultList = {"SerC_CG_Foundation_Fieldbus_Interface_required":"No","SerC_CG_Ethernet_Interface":"No","SerC_GC_Profibus_Gateway_Interface":"No","SerC_CG_Controller_Memory_Backup":"No"}
if ioFamilyType == 'Series-C Mark II' or (ioFamilyType == 'Series C' and controller == 'C300 CEE'):
    for key,value in defaultList.items():
        #if Product.Attr(key).GetValue() == '':
        Product.Attr(key).SelectDisplayValue(value)

    deleteRowsByCondition('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont', ["SCM: HLAI (16) without HART with differential inputs (0-5000)"])
    deleteRowsByCondition('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1', [
            "SCM: DI (32) 110 VAC (0-5000)", "SCM: DI (32) 220 VAC (0-5000)", 
            "SCM: DO (32) 24VDC Relay Bus above 30V (0-5000)", "SCM: DO (32) 24VDC Relay Bus up to 30V (0-5000)"
        ])

elif ioFamilyType == 'Series C' and controller in ("CN100 CEE","CN100 I/O HIVE - C300 CEE","Control HIVE - Physical","Control HIVE - Virtual"):
    Product.DisallowAttr("SerC_CG_Foundation_Fieldbus_Interface_required")
    Product.DisallowAttr("SerC_CG_Ethernet_Interface")
    Product.DisallowAttr("SerC_GC_Profibus_Gateway_Interface")
    Product.DisallowAttr("SerC_CG_Controller_Memory_Backup")
if ioFamilyType == 'Series C':
    rgName = "Series-C {}".format(cgName)
else:
    rgName = "{} {}".format(ioFamilyType, cgName)
RGCont = Product.GetContainerByName('Series_C_Remote_Groups_Cont')
idx = 0
if RGCont.Rows.Count > 0:
    for row in RGCont.Rows:
        row["Series_C_RG_Name"] = "{} Remote Group{}".format(rgName, idx+1)
        idx += 1
        row.Product.Attr('Series_C_RG_Name').AssignValue(str(row["Series_C_RG_Name"]))
        row.ApplyProductChanges()
        row.Calculate()
fim_io_cont = Product.GetContainerByName('SerC_CG_FIM_FF_IO_Cont')
fim_io_cont.Rows.Clear()
UIO_Cont1 = Product.GetContainerByName("C300_CG_Universal_IO_cont_1")
UIO_Cont2 = Product.GetContainerByName("C300_CG_Universal_IO_cont_2")
EnhancedIO_Cont1 = Product.GetContainerByName("SerC_CG_Enhanced_Function_IO_Cont")
EnhancedIO_Cont2 = Product.GetContainerByName("SerC_CG_Enhanced_Function_IO_Cont2")
UIO_Mark1 = Product.GetContainerByName("C300_CG_Universal_IO_Mark_1")
UIO_Mark2 = Product.GetContainerByName("C300_CG_Universal_IO_Mark_2")
EnhancedIO_Mark1 = Product.GetContainerByName("C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont")
EnhancedIO_Mark2 = Product.GetContainerByName("C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1")
TurboM_Cont = Product.GetContainerByName("C300_TurboM_IOM_CG_Cont")
if ioFamilyType in ["Series C","Turbomachinery"]:
    if ioFamilyType == "Turbomachinery":
        Product.Attr("SerC_CG_Controller_Memory_Backup").SelectDisplayValue("No")
    if UIO_Cont1.Rows.Count == 0:
        UIO_Cont1.LoadFromDatabase("Select top 10 IO_Type, red_is, future_red_is, non_red_is, red_nis, future_red_nis, non_red_nis, red_isltr, future_red_isltr, non_red_isltr from Universal_IO_count WHERE IO_Type!=''",'Code')
    if UIO_Cont2.Rows.Count == 0:
        UIO_Cont2.LoadFromDatabase("Select top 10 IO_Type, red_is, future_red_is, non_red_is, red_nis, future_red_nis, non_red_nis, red_isltr,future_red_isltr,non_red_isltr,red_rly,future_red_rly,non_red_rly from Universal_IO_count_1 WHERE IO_Type!=''",'Code')
    if EnhancedIO_Cont1.Rows.Count == 0:
        EnhancedIO_Cont1.LoadFromDatabase("Select top 10 IO_Type, red_is, future_red_is, non_red_is, red_nis, future_red_nis, non_red_nis, red_isltr, future_red_isltr, non_red_isltr from Enhanced_Function_IO WHERE IO_Type!=''",'Code')
    if EnhancedIO_Cont2.Rows.Count == 0:
        EnhancedIO_Cont2.LoadFromDatabase("Select top 30 IO_Type, red_is, future_red_is, non_red_is, red_nis, future_red_nis, non_red_nis, red_isltr, future_red_isltr, non_red_isltr, red_rly, future_red_rly, non_red_rly, Parent_Product from Enhanced_Function_IO2 WHERE Parent_Product ='Control Group'",'Code')
    if ioFamilyType == "Turbomachinery" and TurboM_Cont.Rows.Count == 0:
        TurboM_Cont.LoadFromDatabase("Select IO_Type, Red_IOM from C300_TurboM_IOM",'Code')
    deleteRowsByCondition('C300_CG_Universal_IO_cont_1', ["Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)"])
    deleteRowsByCondition('SerC_CG_Enhanced_Function_IO_Cont', ["Series-C: HLAI (16) without HART with differential inputs (0-5000)"])
    deleteRowsByCondition('SerC_CG_Enhanced_Function_IO_Cont2', [
        "Series-C: DI (32) 110 VAC (0-5000)", "Series-C: DI (32) 110 VAC PROX (0-5000)", 
            "Series-C: DI (32) 220 VAC (0-5000)", "Series-C: DO (32) 24VDC Relay Bus above 30V (0-5000)", 
            "Series-C: DO (32) 24VDC Relay Bus up to 30V (0-5000)"
        ])

else:
    if UIO_Mark1.Rows.Count == 0:
        UIO_Mark1.LoadFromDatabase("Select top 10 IO_Type, red_is, future_red_is, non_red_is, red_nis, future_red_nis, non_red_nis, red_isltr, future_red_isltr, non_red_isltr from Universal_IO_Mark_1 WHERE IO_Type!=''",'Code')
    if UIO_Mark2.Rows.Count == 0:
        UIO_Mark2.LoadFromDatabase("Select top 10 IO_Type, red_is, future_red_is, non_red_is, red_nis, future_red_nis, non_red_nis, red_isltr, future_red_isltr, non_red_isltr,red_rly,future_red_rly,non_red_rly from Universal_IO_Mark_2 WHERE IO_Type!=''",'Code')
    if EnhancedIO_Mark1.Rows.Count == 0:
        EnhancedIO_Mark1.LoadFromDatabase("SELECT IO_Type FROM Enhanced_function1 WHERE Container_Name = 'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont'",'Code')
    if EnhancedIO_Mark2.Rows.Count == 0:
        EnhancedIO_Mark2.LoadFromDatabase("SELECT IO_Type FROM Enhanced_function WHERE Container_Name = 'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1'",'Code')

if ioFamilyType == "Turbomachinery":
	deleteRowsByCondition('SerC_CG_Enhanced_Function_IO_Cont2', [
		"Series-C: Pulse Input (8) Single Channel (0-5000)", 
		"Series-C: Pulse Input (4) Dual Channel (0-5000)", 
		"Series-C: Pulse Input (2) Fast Cut Off Channel (0-5000)"
	])
	Product.Attr('SerC_CG_Marshalling_Cabinet_Type').SelectDisplayValue('None')
	for row in Product.GetContainerByName('Series_C_Remote_Groups_Cont').Rows:
		for val in row.Product.Attr('SerC_RG_Marshalling_Cabinet_Type').Values:
			if val.Display == "Universal Marshalling":
				val.Allowed = False
		row.Product.Attr('SerC_RG_Marshalling_Cabinet_Type').SelectDisplayValue('None')

elif ioFamilyType == "Series C":
	# Reload the rows into the container for "Series C"
	EnhancedIO_Cont2.LoadFromDatabase("Select top 30 IO_Type, red_is, future_red_is, non_red_is, red_nis, future_red_nis, non_red_nis, red_isltr, future_red_isltr, non_red_isltr, red_rly, future_red_rly, non_red_rly, Parent_Product from Enhanced_Function_IO2 WHERE Parent_Product ='Control Group'",'Code')

elif ioFamilyType == 'Series-C Mark II':
	for row in Product.GetContainerByName('Series_C_Remote_Groups_Cont').Rows:
		row.Product.Attr('SerC_RG_Marshalling_Cabinet_Type').SelectDisplayValue('Universal Marshalling')