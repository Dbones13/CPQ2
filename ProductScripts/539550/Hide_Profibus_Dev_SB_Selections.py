container_list = ['PMD_Profibus_Drives_Cont',
                  'PMD_Profibus_Links_and_Gateways_Cont',
                  'PMD_Profibus_Motor_Starters and_CD_Cont',
                  'PMD_Other_Profibus_DP-Devices_Cont',
                  'PMD_Profibus_Modular_IO_Cont',
                  'PMD_Profibus_Displays_Cont',
                  'PMD_Profinet_Device_Support_blocks_Cont']
for cont in container_list:
    try:
        container = Product.GetContainerByName(cont)
        if container.Rows.Count != 0:
            # Set column width
            #container.Rows[0].GetColumnByName('Device').Width = 50
            newRows = container.Rows.Count
            
            # Generate list of previously selected drives
            sel_drives = []
            for i in range(newRows):
                sel_drives.append(container.Rows[i].GetColumnByName('Device').Value)
            
            # Disallow any selected drives from all other rows in container
            for i in range(newRows):
                for value in container.Rows[i].GetColumnByName('Device').ReferencingAttribute.Values:
                    if container.Rows[i].GetColumnByName('Device').Value != value.ValueCode and (value.ValueCode in sel_drives):
                        value.Allowed = False
                    else:
                        value.Allowed = True
    except:
        Log.Write('Error in "Hide_Profibus_Dev_SB_Selections" PS for cont: {}'.format(cont))