def sortRow(cont,rank,new_row_index):
    #Trace.Write("rank of previous row: {0}, new_row_index: {1}".format(rank,new_row_index))
    sort_needed = True
    if new_row_index == 0:
        return
    while sort_needed == True and new_row_index > 0:
        #Trace.Write("rank of previous row: {0}, new_row_index: {1}".format(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value, new_row_index))
        if int(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value) > int(rank):
            cont.MoveRowUp(new_row_index, False)
            new_row_index -= 1
        else:
            sort_needed = False

def add_new_row(cont, row, io_field_type):
    new_row = cont.AddNewRow('GIIS_with_on-board_P+F_Isolators_cpq', False)
    new_row.Product.Attributes.GetByName("type").AssignValue(row.Type)
    new_row.SetColumnValue(io_field_type, row.Type)
    new_row.GetColumnByName(io_field_type).SetAttributeValue(row.Type)
    new_row.SetColumnValue("Rank", str(row.Rank))
    new_row.GetColumnByName("Rank").SetAttributeValue(str(row.Rank))
    new_row.ApplyProductChanges()
    new_row.Product.ApplyRules()
    sortRow(cont,row.Rank, new_row.RowIndex)

def refresh_container(cont):
    ##new_row = cont.AddNewRow('GIIS_with_on-board_P+F_Isolators_cpq', True)
    #Trace.Write(new_row.RowIndex)
    ##cont.DeleteRow(new_row.RowIndex)
    cont.Calculate()

def del_row(cont, mod_to_delete):
    mod_to_delete.sort(reverse=True)
    for x in mod_to_delete:
        cont.DeleteRow(x)

def disallow_modules_list(container_name, field_value):
    ignore_option = ''
    result = []
    record = False
    query = ""
    if field_value == 'PUIO':
        query = "SELECT top 100 Container_Name, Type, Rank FROM SM_IO_Modules WHERE Product='SM Remote Group' and Container_Name ='{}' and Universal_IOTA  = 'RUSIO' ORDER BY Rank".format(container_name, field_value)
    elif field_value == 'Hardware Marshalling with P+F':
        ignore_option = 'Universal Marshalling'
    elif field_value == 'Universal Marshalling':
        ignore_option = 'Hardware Marshalling with P+F'

    if ignore_option != '':
        query = "SELECT top 100 Container_Name, Type, Rank FROM SM_IO_Modules WHERE Product='SM Remote Group' and Container_Name ='{}' and Marshalling_Option = '{}' ORDER BY Rank".format(container_name, ignore_option)
    elif field_value == 'Hardware Marshalling with Other':
        query = "SELECT top 100 Container_Name, Type, Rank FROM SM_IO_Modules WHERE Product='SM Remote Group' and Container_Name ='{}' and Marshalling_Option != '{}' ORDER BY Rank".format(container_name, field_value)

    if query != '':
        #Trace.Write("dis:{}".format(query))
        record = SqlHelper.GetList(query)
        for row in record:
            result.append(row.Type)
    return result

def update_modules_universal_iota(Product, container_name, field_value):
    current_modules = []
    mod_to_delete = []
    cont = Product.GetContainerByName(container_name)
    refresh_required = False
    type_hash = {'SM_RG_IO_Count_Analog_Input_Cont':'Analog_Input_Type', 'SM_RG_IO_Count_Analog_Output_Cont': 'Analog_Output_Type', 'SM_RG_IO_Count_Digital_Input_Cont': 'Digital_Input_Type', 'SM_RG_IO_Count_Digital_Output_Cont':'Digital_Output_Type'}
    type_field = type_hash[container_name]
    '''Getting all existing records from the container'''
    for row in cont.Rows:
        current_modules.append(row.GetColumnByName(type_field).Value)
    '''New records to be added with container'''
    if field_value == 'RUSIO':
        tableMod = SqlHelper.GetList("SELECT top 100 Container_Name, Type, Rank FROM SM_IO_Modules WHERE Product='SM Remote Group' and Container_Name ='{}' and Universal_IOTA  = '{}' ORDER BY Rank".format(container_name, field_value))
        for row in tableMod:
            if row.Type not in current_modules:
                add_new_row(cont, row, type_field)
                refresh_required = True
       	if refresh_required:
            refresh_container(cont)
    else:
        '''Records to be removed from the container'''
        disallow_modules = disallow_modules_list(container_name, field_value)
        for lst in disallow_modules:
            for cont_row in cont.Rows:
                if lst == cont_row.GetColumnByName(type_field).Value:
                    mod_to_delete.append(cont_row.RowIndex)

    if len(mod_to_delete):
        del_row(cont, mod_to_delete)


def update_modules_by_marshalling(Product, marshalling_option):
    refresh_required = False
    container_list = ["SM_RG_IO_Count_Analog_Input_Cont",  "SM_RG_IO_Count_Analog_Output_Cont", "SM_RG_IO_Count_Digital_Input_Cont", "SM_RG_IO_Count_Digital_Output_Cont"]
    type_hash = {'SM_RG_IO_Count_Analog_Input_Cont':'Analog_Input_Type', 'SM_RG_IO_Count_Analog_Output_Cont': 'Analog_Output_Type', 'SM_RG_IO_Count_Digital_Input_Cont': 'Digital_Input_Type', 'SM_RG_IO_Count_Digital_Output_Cont':'Digital_Output_Type'}

    #removing ui questions which are not required to the selected marshalling option
    for cont in container_list:
        disallow_modules = disallow_modules_list(cont, marshalling_option)
        container = Product.GetContainerByName(cont)
        mod_to_delete = []
        type_field = type_hash[cont]
        for lst in disallow_modules:
            for cont_row in container.Rows:
                if lst == cont_row.GetColumnByName(type_field).Value:
                    mod_to_delete.append(cont_row.RowIndex)
        if len(mod_to_delete):
            del_row(container, mod_to_delete)

    if marshalling_option == 'Universal Marshalling':
        container_list = ["SM_RG_IO_Count_Analog_Input_Cont", "SM_RG_IO_Count_Digital_Input_Cont"]

    for container_name in container_list:
        current_modules = []
        type_field = type_hash[container_name]
        '''Getting all existing records from the container'''
        container = Product.GetContainerByName(container_name)
        for row in container.Rows:
            current_modules.append(row.GetColumnByName(type_field).Value)

        tableMod = SqlHelper.GetList("SELECT top 100 Container_Name, Type, Rank FROM SM_IO_Modules WHERE Product='SM Remote Group' and Container_Name ='{}' and Marshalling_Option  = '{}' ORDER BY Rank".format(container_name, marshalling_option))
        for row in tableMod:
            #Trace.Write(row.Type)
            if row.Type not in current_modules:
                #Trace.Write(row.Type)
                add_new_row(container, row, type_field)
                refresh_required = True

       	if refresh_required:
            refresh_container(container)