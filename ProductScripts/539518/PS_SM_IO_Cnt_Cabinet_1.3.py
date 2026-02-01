def sortRow(cont,rank,new_row_index):
    sort_needed = True
    if new_row_index == 0:
        return
    while sort_needed == True:
        Trace.Write("rank of previous row: {0}, new_row_index: {1}".format(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value, new_row_index))
        if int(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value) > int(rank):
            cont.MoveRowUp(new_row_index, False)
            new_row_index -= 1
        else:
            sort_needed = False

io_cont_list = SqlHelper.GetList("Select distinct Container_Name from SM_IO_Count_Cabinet")
Comp=Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont')
contleft=Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left')
contDet=Product.GetContainerByName('SM_RG_Cabinet_Details_Cont')
Enclosure_Type=""
Marshalling_option=""
DI_SIL_cont=""
if Comp.Rows.Count > 0:
    Enclosure_Type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').Value
if contleft.Rows.Count > 0:
    Marshalling_option = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
if contDet.Rows.Count > 0:
    DI_SIL_cont = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName('SM_DI_Relay_resistor_Adapter_UMC').Value
#Iota_Val = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Universal_IOTA').Value
Disallow_list_HMPF = {'Analog_Input/Output_Type' : ['SAI(1)mA type Current UIO (0-5000)', 'SAO(1)mA Type UIO (0-5000)'],
'Digital_Input/Output_Type' : ['SDI(1) 24Vdc UIO (0-5000)', 'SDO(1) 24Vdc 500mA UIO (0-5000)']
}
Disallow_list_IIO = {'Digital_Input_Type' : ['SDI(1) 24Vdc with 5K Resistor UIO  (0-5000)', 'SDI(1) 24Vdc with 5K Resistor DIO  (0-5000)']}
for cont in io_cont_list:
    current_io_type = []
    io_cont = Product.GetContainerByName(cont.Container_Name)
    io_cont_dtls = SqlHelper.GetList("Select Cont_ColumnName, Type, Rank from SM_IO_Count_Cabinet where Container_Name = '{0}'".format(cont.Container_Name))
    if io_cont.Rows.Count == 0: 
        for cont_dtls in io_cont_dtls:
            if Enclosure_Type == 'Cabinet':
                if cont_dtls.Cont_ColumnName in Disallow_list_HMPF:
                    if cont_dtls.Type in Disallow_list_HMPF[cont_dtls.Cont_ColumnName]:
                        continue
            if DI_SIL_cont != 'Yes' and Marshalling_option == 'Universal Marshalling':
                if cont_dtls.Cont_ColumnName in Disallow_list_IIO:
                    if cont_dtls.Type in Disallow_list_IIO[cont_dtls.Cont_ColumnName]:
                        continue
            new_row = io_cont.AddNewRow(False)
            Trace.Write("Adding row at line 37")
            new_row.SetColumnValue(cont_dtls.Cont_ColumnName, cont_dtls.Type)
            new_row.SetColumnValue("Rank", str(cont_dtls.Rank))
        io_cont.Calculate()
    else:
            for row in io_cont.Rows:
                current_io_type.append(row.GetColumnByName(io_cont_dtls[0].Cont_ColumnName).Value)
            for cont_dtls in io_cont_dtls:
                if Enclosure_Type == 'Cabinet':
                    if cont_dtls.Cont_ColumnName in Disallow_list_HMPF:
                        if cont_dtls.Type in Disallow_list_HMPF[cont_dtls.Cont_ColumnName]:
                            if cont_dtls.Type in current_io_type:
                                for cont_row in io_cont.Rows:
                                    if cont_dtls.Type == cont_row.GetColumnByName(cont_dtls.Cont_ColumnName).Value:
                                        io_cont.DeleteRow(cont_row.RowIndex)
                                        break
                            continue
                if DI_SIL_cont != 'Yes' and Marshalling_option == 'Universal Marshalling':
                    if cont_dtls.Cont_ColumnName in Disallow_list_IIO:
                        if cont_dtls.Type in Disallow_list_IIO[cont_dtls.Cont_ColumnName]:
                            if cont_dtls.Type in current_io_type:
                                for cont_row in io_cont.Rows:
                                    if cont_dtls.Type == cont_row.GetColumnByName(cont_dtls.Cont_ColumnName).Value:
                                        io_cont.DeleteRow(cont_row.RowIndex)
                                        break
                            continue
                if cont_dtls.Type not in current_io_type:
                    new_row = io_cont.AddNewRow(False)
                    Trace.Write("Adding row at line 64")
                    new_row.SetColumnValue(cont_dtls.Cont_ColumnName, cont_dtls.Type)
                    new_row.SetColumnValue("Rank", str(cont_dtls.Rank))
                    sortRow(io_cont, cont_dtls.Rank, new_row.RowIndex)
            io_cont.Calculate()
            
di_cont = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont')
di_cont_rows = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows
count_di_cont_rows = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows.Count
if count_di_cont_rows > 0:
    if DI_SIL_cont != 'Yes'and Marshalling_option == 'Universal Marshalling':
        Trace.Write("Disabled")
        if count_di_cont_rows>5 and di_cont_rows[5].GetColumnByName('Digital_Input_Type').Value == 'SDI(1) 24Vdc with 5K Resistor DIO  (0-5000)':
            Trace.Write("Ayushi")
            di_cont.DeleteRow(di_cont_rows[5].RowIndex)
        if di_cont_rows[2].GetColumnByName('Digital_Input_Type').Value == 'SDI(1) 24Vdc with 5K Resistor UIO  (0-5000)':
            di_cont.DeleteRow(di_cont_rows[2].RowIndex)
        di_cont.Calculate()