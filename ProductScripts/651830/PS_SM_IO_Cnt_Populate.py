def sortRow(cont,rank,new_row_index):
    sort_needed = True
    if new_row_index == 0:
        return
    while sort_needed == True:
        #Trace.Write("rank of previous row: {0}, new_row_index: {1}".format(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value, new_row_index))
        if int(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value) > int(rank):
            cont.MoveRowUp(new_row_index, False)
            new_row_index -= 1
        else:
            sort_needed = False

io_cont_list = SqlHelper.GetList("Select distinct Container_Name from SM_IO_COUNTS")
Marshalling_option=""
DI_SIL_cont=""
Iota_Val=""
contCabLeft=Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left')
contCabRight=Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right')
coqu=Product.GetContainerByName('SM_CG_Common_Questions_Cont')
if contCabLeft.Rows.Count > 0:
	Marshalling_option = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').Value
if contCabRight.Rows.Count > 0:
	DI_SIL_cont = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName('DI_SIL1_Relay_5K_resistor_Adapter_UMC').Value
if coqu.Rows.Count > 0:
	Iota_Val = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Universal_IOTA').Value
Disallow_list_HMPF = {'Analog Input Type' : ['SAI(1)mA Type Current P+F UIO (0-5000)'],
'Analog Output Type' : ['SAO(1)mA Type P+F UIO (0-5000)'],
'Digital Input Type' : ['SDI(1)  24Vdc SIL2 P+F UIO (0-5000)', 'SDI(1)  24Vdc SIL3 P+F UIO (0-5000)'],
'Digital Output Type' : ['SDO(1) 24Vdc SIL3 P+F UIO (0-5000)']
}
Disallow_list_UM = {'Analog Input Type' : ['SAI(1)FIRE 3-4 wire current Sink UIO (0-5000)'],
'Digital Input Type' : ['SDI(1) 24Vdc with 5K Resistor UIO (0-5000)', 'SDI(1) 24Vdc with 5K Resistor DIO (0-5000)']
}
Disallow_list_HMPF_UM = {'Analog Input Type' : ['SAI(1)mA Type Current P+F UIO (0-5000)', 'SAI(1)FIRE 3-4 wire current Sink UIO (0-5000)'],
'Analog Output Type' : ['SAO(1)mA Type P+F UIO (0-5000)'],
'Digital Input Type' : ['SDI(1) 24Vdc SIL2 P+F UIO (0-5000)', 'SDI(1) 24Vdc SIL3 P+F UIO (0-5000)', 'SDI(1) 24Vdc with 5K Resistor UIO (0-5000)', 'SDI(1) 24Vdc with 5K Resistor DIO (0-5000)'],
'Digital Output Type' : ['SDO(1) 24Vdc SIL3 P+F UIO (0-5000)']
}
Disallow_list_Rusio = {'Digital Output Type' : ['SDO(2)24Vdc 1A UIO (0-5000)', 'SDO(4)24Vdc 2A UIO (0-5000)']}
Disallow_list_IIO = {'Digital Input Type' : ['SDI(1) 24Vdc with 5K Resistor UIO (0-5000)', 'SDI(1) 24Vdc with 5K Resistor DIO (0-5000)']}

for cont in io_cont_list:
    current_io_type = []
    io_cont = Product.GetContainerByName(cont.Container_Name)
    io_cont_dtls = SqlHelper.GetList("Select Cont_ColumnName, Type, Rank from SM_IO_COUNTS where Container_Name = '{0}'".format(cont.Container_Name))
    if io_cont.Rows.Count == 0: 
        for cont_dtls in io_cont_dtls:
            if Marshalling_option == 'Universal_Marshalling':
                if cont_dtls.Cont_ColumnName in Disallow_list_HMPF:
                    if cont_dtls.Type in Disallow_list_HMPF[cont_dtls.Cont_ColumnName]:
                        continue
            elif Marshalling_option == 'Hardware_Marshalling_with_P+F':
                if cont_dtls.Cont_ColumnName in Disallow_list_UM:
                    if cont_dtls.Type in Disallow_list_UM[cont_dtls.Cont_ColumnName]:
                        continue
            elif Marshalling_option == 'Hardware_Marshalling_with_Other':
                if cont_dtls.Cont_ColumnName in Disallow_list_HMPF_UM:
                    if cont_dtls.Type in Disallow_list_HMPF_UM[cont_dtls.Cont_ColumnName]:
                        continue
            if Iota_Val == 'PUIO':
                if cont_dtls.Cont_ColumnName in Disallow_list_Rusio:
                    if cont_dtls.Type in Disallow_list_Rusio[cont_dtls.Cont_ColumnName]:
                        continue
            if DI_SIL_cont != 'Yes' and Marshalling_option == 'Universal_Marshalling':
                if cont_dtls.Cont_ColumnName in Disallow_list_IIO:
                    if cont_dtls.Type in Disallow_list_IIO[cont_dtls.Cont_ColumnName]:
                        continue
            new_row = io_cont.AddNewRow(False)
            new_row.SetColumnValue(cont_dtls.Cont_ColumnName, cont_dtls.Type)
            new_row.SetColumnValue("Rank", str(cont_dtls.Rank))
        io_cont.Calculate()
    else:
            for row in io_cont.Rows:
                current_io_type.append(row.GetColumnByName(io_cont_dtls[0].Cont_ColumnName).Value)
            for cont_dtls in io_cont_dtls:
                if Marshalling_option == 'Universal_Marshalling':
                    if cont_dtls.Cont_ColumnName in Disallow_list_HMPF:
                        if cont_dtls.Type in Disallow_list_HMPF[cont_dtls.Cont_ColumnName]:
                            if cont_dtls.Type in current_io_type:
                                for cont_row in io_cont.Rows:
                                    if cont_dtls.Type == cont_row.GetColumnByName(cont_dtls.Cont_ColumnName).Value:
                                        io_cont.DeleteRow(cont_row.RowIndex)
                                        break
                            continue
                elif Marshalling_option == 'Hardware_Marshalling_with_P+F':
                    if cont_dtls.Cont_ColumnName in Disallow_list_UM:
                        if cont_dtls.Type in Disallow_list_UM[cont_dtls.Cont_ColumnName]:
                            if cont_dtls.Type in current_io_type:
                                for cont_row in io_cont.Rows:
                                    if cont_dtls.Type == cont_row.GetColumnByName(cont_dtls.Cont_ColumnName).Value:
                                        io_cont.DeleteRow(cont_row.RowIndex)
                                        break
                            continue
                elif Marshalling_option == 'Hardware_Marshalling_with_Other':
                    if cont_dtls.Cont_ColumnName in Disallow_list_HMPF_UM:
                        if cont_dtls.Type in Disallow_list_HMPF_UM[cont_dtls.Cont_ColumnName]:
                            if cont_dtls.Type in current_io_type:
                                for cont_row in io_cont.Rows:
                                    if cont_dtls.Type == cont_row.GetColumnByName(cont_dtls.Cont_ColumnName).Value:
                                        io_cont.DeleteRow(cont_row.RowIndex)
                                        break
                            continue
                if Iota_Val == 'PUIO':
                    if cont_dtls.Cont_ColumnName in Disallow_list_Rusio:
                        if cont_dtls.Type in Disallow_list_Rusio[cont_dtls.Cont_ColumnName]:
                            if cont_dtls.Type in current_io_type:
                                for cont_row in io_cont.Rows:
                                    if cont_dtls.Type == cont_row.GetColumnByName(cont_dtls.Cont_ColumnName).Value:
                                        io_cont.DeleteRow(cont_row.RowIndex)
                                        break
                            continue
                if DI_SIL_cont != 'Yes' and Marshalling_option == 'Universal_Marshalling':
                    if cont_dtls.Cont_ColumnName in Disallow_list_IIO:
                        if cont_dtls.Type in Disallow_list_IIO[cont_dtls.Cont_ColumnName]:
                            if cont_dtls.Type in current_io_type:
                                for cont_row in io_cont.Rows:
                                    if cont_dtls.Type == cont_row.GetColumnByName(cont_dtls.Cont_ColumnName).Value:
                                        io_cont.DeleteRow(cont_row.RowIndex)
                                        break
                if cont_dtls.Type not in current_io_type:
                    new_row = io_cont.AddNewRow(False)
                    new_row.SetColumnValue(cont_dtls.Cont_ColumnName, cont_dtls.Type)
                    new_row.SetColumnValue("Rank", str(cont_dtls.Rank))
                    sortRow(io_cont, cont_dtls.Rank, new_row.RowIndex)
            io_cont.Calculate()

do_cont = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont')
do_cont_rows = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows
count_do_cont_rows = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows.Count
if count_do_cont_rows > 0:
    if Iota_Val == 'PUIO':
        if do_cont_rows[2].GetColumnByName('Digital Output Type').Value == 'SDO(2)24Vdc 1A UIO (0-5000)':
            do_cont.DeleteRow(do_cont_rows[2].RowIndex)
        if do_cont_rows[3].GetColumnByName('Digital Output Type').Value == 'SDO(4)24Vdc 2A UIO (0-5000)':
            do_cont.DeleteRow(do_cont_rows[3].RowIndex)
        do_cont.Calculate()

di_cont = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont')
di_cont_rows = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows
count_di_cont_rows = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows.Count
if count_di_cont_rows > 0:
    if DI_SIL_cont != 'Yes'and Marshalling_option == 'Universal_Marshalling':
        #Trace.Write("Disabled")
        if count_di_cont_rows>5 and di_cont_rows[5].GetColumnByName('Digital Input Type').Value == 'SDI(1) 24Vdc with 5K Resistor DIO (0-5000)':
            di_cont.DeleteRow(di_cont_rows[5].RowIndex)
            #Trace.Write("deleted the row")
        if di_cont_rows[2].GetColumnByName('Digital Input Type').Value == 'SDI(1) 24Vdc with 5K Resistor UIO (0-5000)':
            di_cont.DeleteRow(di_cont_rows[2].RowIndex)
        di_cont.Calculate()