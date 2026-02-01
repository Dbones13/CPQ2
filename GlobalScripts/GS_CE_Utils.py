def setContainerDefaults(Product):
    if Product.Name == "New / Expansion Project":
        labor_cont = Product.GetContainerByName('Labor_Details_New/Expansion_Cont')
        labor_cont.Rows[0].SetColumnValue('Labor_Percentage_FAT', '100')

    if Product.Name == "ControlEdge PLC System": #Sets all cont_Container defaults to 0 and a single exception value
        container_list = SqlHelper.GetList("Select distinct Container_Name from PLC_UOC_ATTRIBUTE_MINMAX where Product = '{0}' ".format(Product.Name))

        for each in container_list:
            cont = Product.GetContainerByName(each.Container_Name)
            column_list = SqlHelper.GetList("Select Cont_ColumnName from PLC_UOC_ATTRIBUTE_MINMAX where Container_Name = '{0}' ".format(each.Container_Name))
            for column in column_list:
                cont.Rows[0].SetColumnValue(column.Cont_ColumnName, '0')

        #This is set afterwards to overwrite the standard 0 value with the correct value
        software_cont = Product.GetContainerByName('PLC_Software_Question_Cont')
        software_cont.Rows[0].SetColumnValue('PLC_CE_Builder_Client', '0')
        cg_cont = Product.GetContainerByName('Number_PLC_Control_Groups')
        cg_cont.Rows[0].SetColumnValue('Number_PLC_Control_Groups', '1')
        sys_hw = Product.GetContainerByName('CE_PLC_System_Hardware')
        sys_hw.Rows[0].SetColumnValue('PLC_Engineering_Station_Qty', '0')
        

    elif Product.Name == "CE PLC Control Group": #Sets all container defaults to 0
        container_list = SqlHelper.GetList("Select distinct Container_Name from PLC_UOC_ATTRIBUTE_MINMAX where Product = '{0}' and Container_Name NOT IN ('PLC_CG_R_UIO_Cont', 'PLC_CG_NR_UIO_Cont')".format(Product.Name))

        for each in container_list:
            if each.Container_Name == "PLC_CG_UIO_Cont":
                cont = Product.GetContainerByName(each.Container_Name)
                column_list = SqlHelper.GetList("Select Cont_ColumnName from PLC_UOC_ATTRIBUTE_MINMAX where Container_Name = '{0}' ".format(each.Container_Name))
                for column in column_list:
                    cont.Rows[0].SetColumnValue(column.Cont_ColumnName, '0')
                    cont.Rows[1].SetColumnValue(column.Cont_ColumnName, '0')
            else:
                cont = Product.GetContainerByName(each.Container_Name)
                column_list = SqlHelper.GetList("Select Cont_ColumnName from PLC_UOC_ATTRIBUTE_MINMAX where Container_Name = '{0}' ".format(each.Container_Name))
                for column in column_list:
                    cont.Rows[0].SetColumnValue(column.Cont_ColumnName, '0')

        rg_cont = Product.GetContainerByName('Number_PLC_Remote_Groups')
        rg_cont.Rows[0].SetColumnValue('Number_PLC_Remote_Groups', '1')

        Product.Attr('isProductLoaded').AssignValue('True')

    elif Product.Name == "CE PLC Remote Group":#Sets all container defaults to 0
        container_list = SqlHelper.GetList("Select distinct Container_Name from PLC_UOC_ATTRIBUTE_MINMAX where Product = '{0}' and Container_Name NOT IN ('PLC_RG_R_UIO_Cont', 'PLC_RG_NR_UIO_Cont')".format(Product.Name))

        for each in container_list:
            if each.Container_Name == "PLC_RG_UIO_Cont":
                cont = Product.GetContainerByName(each.Container_Name)
                column_list = SqlHelper.GetList("Select Cont_ColumnName from PLC_UOC_ATTRIBUTE_MINMAX where Container_Name = '{0}' ".format(each.Container_Name))
                for column in column_list:
                    cont.Rows[0].SetColumnValue(column.Cont_ColumnName, '0')
                    cont.Rows[1].SetColumnValue(column.Cont_ColumnName, '0')
            else:
                cont = Product.GetContainerByName(each.Container_Name)
                column_list = SqlHelper.GetList("Select Cont_ColumnName from PLC_UOC_ATTRIBUTE_MINMAX where Container_Name = '{0}' ".format(each.Container_Name))
                for column in column_list:
                    cont.Rows[0].SetColumnValue(column.Cont_ColumnName, '0')
    
    elif Product.Name == "ControlEdge UOC System": #Sets all container defaults to 0 and a single exception value
        container_list = SqlHelper.GetList("Select distinct Container_Name from PLC_UOC_ATTRIBUTE_MINMAX where Product = '{0}' ".format(Product.Name))

        for each in container_list:
            cont = Product.GetContainerByName(each.Container_Name)
            column_list = SqlHelper.GetList("Select Cont_ColumnName from PLC_UOC_ATTRIBUTE_MINMAX where Container_Name = '{0}' ".format(each.Container_Name))
            for column in column_list:
                Trace.Write(column.Cont_ColumnName)
                cont.Rows[0].SetColumnValue(column.Cont_ColumnName, '0')

        #This is set afterwards to overwrite the standard 0 value with the correct value
        software_cont = Product.GetContainerByName('UOC_Software_Question_Cont')
        software_cont.Rows[0].SetColumnValue('UOC_CE_Builder_Client', '1')
        cg_cont = Product.GetContainerByName('Number_UOC_Control_Groups')
        cg_cont.Rows[0].SetColumnValue('Number_UOC_Control_Groups', '1')
        # Set FO Eng for UOC Additional Custom Deliverable Container
        labor_cont = Product.GetContainerByName('CE UOC Additional Custom Deliverables')
        labor_cont.Rows[0].GetColumnByName('FO Eng').SetAttributeValue('SYS LE1-Lead Eng')
        labor_cont.Rows[0].Product.Attr('CE_UOC_FO_ENG_LD').SelectDisplayValue('SYS LE1-Lead Eng')
        labor_cont.Rows[0].Product.ApplyRules()
        labor_cont.Rows[0].ApplyProductChanges()
        labor_cont.Rows[0].Calculate()
        labor_cont.Calculate()

    elif Product.Name == "UOC Control Group": #Sets all container defaults to 0
        container_list = SqlHelper.GetList("Select distinct Container_Name from PLC_UOC_ATTRIBUTE_MINMAX where Product = '{0}' and Container_Name NOT IN ('UOC_CG_R_UIO_Cont', 'UOC_CG_NR_UIO_Cont')".format(Product.Name))

        for each in container_list:
            if each.Container_Name == "UOC_CG_UIO_Cont":
                cont = Product.GetContainerByName(each.Container_Name)
                column_list = SqlHelper.GetList("Select Cont_ColumnName from PLC_UOC_ATTRIBUTE_MINMAX where Container_Name = '{0}' ".format(each.Container_Name))
                for column in column_list:
                    cont.Rows[0].SetColumnValue(column.Cont_ColumnName, '0')
                    cont.Rows[1].SetColumnValue(column.Cont_ColumnName, '0')
            else:
                cont = Product.GetContainerByName(each.Container_Name)
                column_list = SqlHelper.GetList("Select Cont_ColumnName from PLC_UOC_ATTRIBUTE_MINMAX where Container_Name = '{0}' ".format(each.Container_Name))
                for column in column_list:
                    cont.Rows[0].SetColumnValue(column.Cont_ColumnName, '0')
        
        rg_cont = Product.GetContainerByName('Number_UOC_Remote_Groups')
        rg_cont.Rows[0].SetColumnValue('Number_UOC_Remote_Groups', '1')
        
    elif Product.Name in ("ControlEdge CN900 System"): #Sets all container defaults to 0
        #This is set afterwards to overwrite the standard 0 value with the correct value
        cg_cont = Product.GetContainerByName('Number_CN900_Control_Groups')
        cg_cont.Rows[0].SetColumnValue('Number_CN900_Control_Groups', '1')

    elif Product.Name == "UOC Remote Group":#Sets all container defaults to 0
        container_list = SqlHelper.GetList("Select distinct Container_Name from PLC_UOC_ATTRIBUTE_MINMAX where Product = '{0}' and Container_Name NOT IN ('UOC_RG_R_UIO_Cont', 'UOC_RG_NR_UIO_Cont')".format(Product.Name))

        for each in container_list:
            if each.Container_Name == "UOC_RG_UIO_Cont":
                cont = Product.GetContainerByName(each.Container_Name)
                column_list = SqlHelper.GetList("Select Cont_ColumnName from PLC_UOC_ATTRIBUTE_MINMAX where Container_Name = '{0}' ".format(each.Container_Name))
                for column in column_list:
                    cont.Rows[0].SetColumnValue(column.Cont_ColumnName, '0')
                    cont.Rows[1].SetColumnValue(column.Cont_ColumnName, '0')
            else:
                cont = Product.GetContainerByName(each.Container_Name)
                column_list = SqlHelper.GetList("Select Cont_ColumnName from PLC_UOC_ATTRIBUTE_MINMAX where Container_Name = '{0}' ".format(each.Container_Name))
                for column in column_list:
                    cont.Rows[0].SetColumnValue(column.Cont_ColumnName, '0')
    
    elif Product.Name == "PMD System": #Sets all container defaults to 0, and a couple of exception cases.
        container_list = SqlHelper.GetList("Select distinct Container_Name from PMD_System_Attribute_MinMax where Product = '{0}'".format(Product.Name))

        for each in container_list:
            # Do not set defaults for PMD Profibus SB Containers
            if each.Container_Name not in ['PMD_Profibus_Drives_Cont','PMD_Profibus_Links_and_Gateways_Cont','PMD_Profibus_Motor_Starters and_CD_Cont','PMD_Profibus_Modular_IO_Cont','PMD_Profibus_Displays_Cont','PMD_Other_Profibus_DP-Devices_Cont','PMD_Profinet_Device_Support_blocks_Cont']:
                #Log.Write("TDH: Cont Name: "+each.Container_Name)
                cont = Product.GetContainerByName(each.Container_Name)
                column_list = SqlHelper.GetList("Select Cont_ColumnName from PMD_System_Attribute_MinMax where Container_Name = '{0}'".format(each.Container_Name))
                for column in column_list:
                    cont.Rows[0].SetColumnValue(column.Cont_ColumnName, '0')
        
        #Assigning value 15 to PMD_IO_Space_Req
        container_list_1 = Product.GetContainerByName('PMD_CC_Cards')
        container_list_1.Rows[0].SetColumnValue('PMD_IO_Space_Req', '15')
        #Assigning value 100 to PMD_Percentage of FAT
        container_list_2 = Product.GetContainerByName('PMD_Labour_Details')
        container_list_2.Rows[0].SetColumnValue('PMD_Percentage_of_FAT', '100')
        #assigning value 100 to PMD_Analog_OC
        container_list_3 = Product.GetContainerByName('PMD_CC_Cards')
        container_list_3.Rows[0].SetColumnValue('PMD_Analog_OC', '100')
        #assigning value 100 to PMD_Uni_IO
        container_list_4 = Product.GetContainerByName('PMD_IO_ControlEdge_PLC_IO_Cards')
        container_list_4.Rows[0].SetColumnValue('PMD_Uni_IO', '100')
        #Assigning value 15 to PMD_PMD_IO_Space_Req_2
        container_list_5 = Product.GetContainerByName('PMD_IO_ControlEdge_PLC_IO_Cards')
        container_list_5.Rows[0].SetColumnValue('PMD_IO_Space_Req_2', '15')
        #Assigning value 15 to PMD_PMD_IO_Space_Req_2
        container_list_5 = Product.GetContainerByName('PMD_IO_ControlEdge_PLC_IO_Cards')
        container_list_5.Rows[0].SetColumnValue('PMD_DO_32', '100')
        #Assigning value 100 to PMD_Percentage_of_FAT_2
        container_list_6 = Product.GetContainerByName('PMD_Labour_Details_2')
        container_list_6.Rows[0].SetColumnValue('PMD_Percentage_of_FAT_2', '100')