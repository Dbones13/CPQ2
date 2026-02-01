def deleteRowsByIoType(container_name, io_types):
	container = Product.GetContainerByName(container_name)
	rows_to_delete = [row.RowIndex for row in container.Rows if row['IO_Type'] in io_types]
	for row_index in sorted(rows_to_delete, reverse=True):
		container.DeleteRow(row_index)
familyType = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
mounting_soln = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
UIO_Mark1 = Product.GetContainerByName("C300_CG_Universal_IO_Mark_1")
UIO_Mark2 = Product.GetContainerByName("C300_CG_Universal_IO_Mark_2")
EnhancedIO_Mark1 = Product.GetContainerByName("C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont")
EnhancedIO_Mark2 = Product.GetContainerByName("C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1")
UIO_Cont1 = Product.GetContainerByName("C300_RG_Universal_IO_cont_1")
UIO_Cont2 = Product.GetContainerByName("C300_RG_Universal_IO_cont_2")
EnhancedIO_Cont1 = Product.GetContainerByName("SerC_RG_Enhanced_Function_IO_Cont")
EnhancedIO_Cont2 = Product.GetContainerByName("SerC_RG_Enhanced_Function_IO_Cont2")
TurboM_cont = Product.GetContainerByName("C300_TurboM_IOM_RG_Cont")
if familyType == "Series-C Mark II":
	if UIO_Mark1.Rows.Count == 0:
		UIO_Mark1.LoadFromDatabase("Select top 10 IO_Type, red_is, non_red_is, red_nis, non_red_nis, red_isltr, non_red_isltr from Universal_IO_Mark_1 WHERE IO_Type!=''",'Code')
	if UIO_Mark2.Rows.Count == 0:
		UIO_Mark2.LoadFromDatabase("Select top 10 IO_Type, red_is, non_red_is, red_nis, non_red_nis, red_isltr, non_red_isltr,red_rly,non_red_rly from Universal_IO_Mark_2 WHERE IO_Type!=''",'Code')
	if EnhancedIO_Mark1.Rows.Count == 0:
		EnhancedIO_Mark1.LoadFromDatabase("SELECT IO_Type FROM IO_Mark_II_Group2 WHERE Container_Name = 'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont'",'Code')
	if EnhancedIO_Mark2.Rows.Count == 0:
		EnhancedIO_Mark2.LoadFromDatabase("SELECT IO_Type FROM IO_MARK_II_GROUP WHERE Container_Name = 'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1'",'Code')
	deleteRowsByIoType('C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont',["SCM: HLAI (16) without HART with differential inputs (0-5000)","SCM: HLAI (13-16) with HART with differential inputs (0-5000)","SCM: HLAI (13-16) without HART with differential inputs (0-5000)"])
	deleteRowsByIoType('C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1',
		["SCM: DI (32) 110 VAC (0-5000)",
			"SCM: DI (32) 220 VAC (0-5000)",
			"SCM: DO (32) 24VDC Relay Bus above 30V (0-5000)",
			"SCM: DO (32) 24VDC Relay Bus up to 30V (0-5000)"])

elif familyType in ("Series C","Turbomachinery") and mounting_soln !="Universal Process Cab - 1.3M":
	if UIO_Cont1.Rows.Count == 0:
		UIO_Cont1.LoadFromDatabase("Select top 5 IO_Type, red_is, non_red_is, red_nis, non_red_nis, red_isltr, non_red_isltr from Universal_IO_count WHERE IO_Type!=''",'Code')
	if UIO_Cont2.Rows.Count == 0:
		UIO_Cont2.LoadFromDatabase("Select top 10 IO_Type, red_is, non_red_is, red_nis, non_red_nis, red_isltr,non_red_isltr,red_rly,non_red_rly from Universal_IO_count_1 WHERE IO_Type!=''",'Code')
	if EnhancedIO_Cont1.Rows.Count == 0:
		EnhancedIO_Cont1.LoadFromDatabase("Select top 10 IO_Type, red_is, non_red_is, red_nis, non_red_nis, red_isltr, non_red_isltr from Enhanced_Function_IO WHERE IO_Type!=''",'Code')
	if EnhancedIO_Cont2.Rows.Count == 0:
		EnhancedIO_Cont2.LoadFromDatabase("Select top 50 IO_Type, red_is, non_red_is, red_nis, non_red_nis, red_isltr, non_red_isltr, red_rly, non_red_rly, Parent_Product from Enhanced_Function_IO2 WHERE Parent_Product ='Remote Group'",'Code')
	deleteRowsByIoType('C300_RG_Universal_IO_cont_1',["Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)"])
	deleteRowsByIoType('SerC_RG_Enhanced_Function_IO_Cont',["Series-C: HLAI (16) without HART with differential inputs (0-5000)","Series-C: HLAI (13-16) with HART with differential inputs (0-5000)","Series-C: HLAI (13-16) without HART with differential inputs (0-5000)","SCM: HLAI (13-16) differential inputs (0-5000)"])
	deleteRowsByIoType('SerC_RG_Enhanced_Function_IO_Cont2',
		["Series-C: DI (32) 110 VAC (0-5000)",
			"Series-C: DI (32) 110 VAC PROX (0-5000)",
			"Series-C: DI (32) 220 VAC (0-5000)",
			"Series-C: DO (32) 24VDC Relay Bus above 30V (0-5000)",
			"Series-C: DO (32) 24VDC Relay Bus up to 30V (0-5000)"])
	if familyType == "Turbomachinery" and TurboM_cont.Rows.Count == 0:
		TurboM_cont.LoadFromDatabase("Select IO_Type, Red_IOM from C300_TurboM_IOM",'Code')
		deleteRowsByIoType('SerC_RG_Enhanced_Function_IO_Cont2',
	["Series-C: Pulse Input (8) Single Channel (0-5000)",
		"Series-C: Pulse Input (4) Dual Channel (0-5000)",
		"Series-C: Pulse Input (2) Fast Cut Off Channel (0-5000)",
    ])

if familyType == "Turbomachinery" and Product.Attr('R2QRequest').GetValue() == "Yes":
    for val in Product.Attr('SerC_RG_Marshalling_Cabinet_Type').Values:
        if val.Display == "Universal Marshalling":
            val.Allowed = False
    Product.Attr('SerC_RG_Marshalling_Cabinet_Type').SelectDisplayValue('None')