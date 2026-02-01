def AddRows(rowCount, container):
    for i in range(rowCount):
        if container.Name == 'CE_SystemGroup_Cont':
            row = container.AddNewRow(False)
            row.Product.Attr("CE_System_Index").AssignValue(str(row.RowIndex + 1))
            row.Product.Attr('CE_Scope_Choices').SelectDisplayValue('HW/SW + LABOR')
            row.Product.ApplyRules()
            row.ApplyProductChanges()
            row.Calculate()
        else:
            container.AddNewRow(False)

if(Quote.GetCustomField('isR2QRequest').Content == 'Yes'):
    r2qParentProduct=Product
    parentContainerRowCount=-1
    CE_SystemGroup_Cont = Product.GetContainerByName('CE_SystemGroup_Cont')
    for existingFlowRow in CE_SystemGroup_Cont.Rows:
        existingFlowRow.Product.Attr('MIB Configuration Required?').SelectValues(r2qParentProduct.Attr('MIB Configuration Required?').GetValue())
        #CE_SystemGroup_Cont.Calculate()
        #existingFlowRow.Product.ApplyRules()
        #existingFlowRow.ApplyProductChanges()
        r2qParentProductContainer=r2qParentProduct.GetContainerByName('R2Q Container')
        for r2qParentProductContainerRow in r2qParentProductContainer.Rows:
            if r2qParentProductContainerRow.Columns['Part Number'].Value in ["C300 System"]:

                systemContainer = existingFlowRow.Product.GetContainerByName('CE_System_Cont')
                for systemProductRow in systemContainer.Rows:
                    if systemProductRow.Product.Name in ["C300 System"]:
                        systemProductRow.Product.Attr('C300_Process_Type').SelectValues(r2qParentProduct.Attr('C300_Process_Type').GetValue())
                        systemProductRow.Product.Attr('Experion_PKS_Software_Release').SelectValues(r2qParentProduct.Attr('Experion_PKS_Software_Release').GetValue())
                        systemProductRow.Product.ChangeTab('Labor Deliverables')
                        #systemContainer.Calculate()
                        #systemProductRow.Product.ApplyRules()
                        #systemProductRow.ApplyProductChanges()
                        group_count=  r2qParentProductContainerRow.Product.GetContainerByName('Series_C_Control_Groups_Cont').Rows.Count-1
                        group_count = int(group_count) if group_count else 0
                        existingFlowC300ControlGroupContainer = systemProductRow.Product.GetContainerByName('Series_C_Control_Groups_Cont')
                        try:
                            AddRows(group_count,existingFlowC300ControlGroupContainer)
                        except:
                            Product.Attr('ExceededLimit').AssignValue('True')
                            

                        r2qParentC300ControlGroupContainer=r2qParentProductContainerRow.Product.GetContainerByName('Series_C_Control_Groups_Cont')
                        for r2qParentC300ControlGroupContainerRow in r2qParentC300ControlGroupContainer.Rows:
                            parentContainerRowCount += 1
                            existingFlowC300ControlGroupContainerRow=existingFlowC300ControlGroupContainer.Rows[parentContainerRowCount]                       
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_CG_IO_Family_Type').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_CG_IO_Family_Type').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_CG_Type_of_Controller_Required').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_CG_Power_System_Vendor').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_CG_Power_System_Vendor').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_CG_Controller_Memory_Backup').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_CG_Controller_Memory_Backup').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_CG_Foundation_Fieldbus_Interface_required').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_CG_Foundation_Fieldbus_Interface_required').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_GC_Profibus_Gateway_Interface').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_GC_Profibus_Gateway_Interface').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_CG_Ethernet_Interface').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_CG_Ethernet_Interface').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_CG_Percent_Installed_Spare').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue())
                            
                            existingFlowC300ControlGroupContainerRow.Product.Attr('FIM_Type').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('FIM_Type').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('FIM_Percent_Installed_Spare_Fieldbus_IO').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('FIM_Percent_Installed_Spare_Fieldbus_IO').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('FIM_Num_Devices_Open_Loop').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('FIM_Num_Devices_Open_Loop').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('FIM_Num_Devices_Close_Loop').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('FIM_Num_Devices_Close_Loop').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('FIM_Num_Close_Loop_per_Segment').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('FIM_Num_Close_Loop_per_Segment').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('FIM_Num_FF_Temp_Mux_per_Segment').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('FIM_Num_FF_Temp_Mux_per_Segment').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('FIM_Num_of_MOVs_per_Segment').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('FIM_Num_of_MOVs_per_Segment').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('FIM_FF_IOs_with_Power_conditioner').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('FIM_FF_IOs_with_Power_conditioner').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('FIM_Power_Conditioner_Scope').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('FIM_Power_Conditioner_Scope').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Number_of_Profibus_DP_Slave_devices - Non_Red').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Number_of_Profibus_DP_Slave_devices - Non_Red').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Number_of_Profibus_DP_Slave_devices - Red').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Number_of_Profibus_DP_Slave_devices - Red').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Number_of_Devices_per_Profibus_Network (0-32)').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Number_of_Devices_per_Profibus_Network (0-32)').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Number_of_Rockwell_ControlLogix_Processors').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Number_of_Rockwell_ControlLogix_Processors').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Number of Rockwell Control Processors(NON)').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Number of Rockwell Control Processors(NON)').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Number of Process Connected I/O Devices 1').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Number of Process Connected I/O Devices 1').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Number of Motor Starter IOMs per EIM 255').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Number of Motor Starter IOMs per EIM 255').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_NO of Rock Ctrl Processors Redundant0-999NEW').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_NO of Rock Ctrl Processors Redundant0-999NEW').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Numbe of Rockwelix Proc EIM Redundant 0-10').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Numbe of Rockwelix Proc EIM Redundant 0-10').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Nu of Proc Conn I/O Devi (Redundant ) (0-999)').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Nu of Proc Conn I/O Devi (Redundant ) (0-999)').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Number of Motor Start IOMs per EIM Redun 255').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Number of Motor Start IOMs per EIM Redun 255').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Number of Non Redundant EIM for IEC61850').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Number of Non Redundant EIM for IEC61850').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Number of Redundant EIM for IEC61850').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Number of Redundant EIM for IEC61850').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Number of Non Redund EIM for Profinet Devices').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Number of Non Redund EIM for Profinet Devices').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Number of Redundant EIM for Profinet Devices').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Number of Redundant EIM for Profinet Devices').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Number of Non Redundant EIM for EIP Device').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Number of Non Redundant EIM for EIP Device').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Number of Redunt EIM for EIP Devices (0-300)').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Number of Redunt EIM for EIP Devices (0-300)').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Number_NonRedundant_EIM_for_Modbus').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Number_NonRedundant_EIM_for_Modbus').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_Number_Redundant_EIM_for_Modbus').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_Number_Redundant_EIM_for_Modbus').GetValue())
                            existingFlowC300ControlGroupContainerRow.Product.Attr('SerC_CG_Percentage_of_Spare_Space_required(0-100%)').SelectValues(r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_CG_Percentage_of_Spare_Space_required(0-100%)').GetValue())
                            
                            #existingFlowC300ControlGroupContainerRow.Product.ApplyRules()
                            #existingFlowC300ControlGroupContainerRow.ApplyProductChanges()
                            #existingFlowC300ControlGroupContainer.Calculate()
                            
                            try:
                            	if r2qParentC300ControlGroupContainerRow.Product.Attr('C300_CG_Universal_IO_cont_1').Allowed:
                                    cont1= r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('C300_CG_Universal_IO_cont_1')
                                    rowCount=r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('C300_CG_Universal_IO_cont_1').Rows.Count
                                    cont2= existingFlowC300ControlGroupContainerRow.Product.GetContainerByName('C300_CG_Universal_IO_cont_1')
                                    for i in range(rowCount):
                                        cont2.Rows[1].Columns['Red_IS'].Value=cont1.Rows[1].Columns['Red_IS'].Value
                                    	cont2.Rows[i].Columns['Future_Red_IS'].Value=cont1.Rows[i].Columns['Future_Red_IS'].Value
                                    	cont2.Rows[i].Columns['Non_Red_IS'].Value=cont1.Rows[i].Columns['Non_Red_IS'].Value
                                    	cont2.Rows[i].Columns['Red_NIS'].Value=cont1.Rows[i].Columns['Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Future_Red_NIS'].Value=cont1.Rows[i].Columns['Future_Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Non_Red_NIS'].Value=cont1.Rows[i].Columns['Non_Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Red_ISLTR'].Value=cont1.Rows[i].Columns['Red_ISLTR'].Value
                                    	cont2.Rows[i].Columns['Future_Red_ISLTR'].Value=cont1.Rows[i].Columns['Future_Red_ISLTR'].Value
                                    	cont2.Rows[i].Columns['Non_Red_ISLTR'].Value=cont1.Rows[i].Columns['Non_Red_ISLTR'].Value
                                    	#cont2.Rows[i].Columns['IO_Type_with_hint'].Value=cont1.Rows[i].Columns['IO_Type_with_hint'].Value
                                    	#cont2.Rows[i].Columns['AI'].Value=cont1.Rows[i].Columns['AI'].Value
                                    	#cont2.Rows[i].Columns['AO'].Value=cont1.Rows[i].Columns['AO'].Value
                                    	#cont2.Rows[i].Columns['Labor_IS'].Value=cont1.Rows[i].Columns['Labor_IS'].Value
                            except Exception as error:
                                Log.Info('Error in C300_CG_Universal_IO_cont_1 '+ str(error))
                                pass
                            try:
                                if r2qParentC300ControlGroupContainerRow.Product.Attr('C300_CG_Universal_IO_cont_2').Allowed:
                                    cont1= r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('C300_CG_Universal_IO_cont_2')
                                    rowCount=r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('C300_CG_Universal_IO_cont_2').Rows.Count
                                    cont2= existingFlowC300ControlGroupContainerRow.Product.GetContainerByName('C300_CG_Universal_IO_cont_2')
                                    for i in range(rowCount):
                                    	cont2.Rows[i].Columns['Red_IS'].Value=cont1.Rows[i].Columns['Red_IS'].Value
                                    	cont2.Rows[i].Columns['Future_Red_IS'].Value=cont1.Rows[i].Columns['Future_Red_IS'].Value
                                    	cont2.Rows[i].Columns['Non_Red_IS'].Value=cont1.Rows[i].Columns['Non_Red_IS'].Value
                                    	cont2.Rows[i].Columns['Red_NIS'].Value=cont1.Rows[i].Columns['Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Future_Red_NIS'].Value=cont1.Rows[i].Columns['Future_Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Non_Red_NIS'].Value=cont1.Rows[i].Columns['Non_Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Red_ISLTR'].Value=cont1.Rows[i].Columns['Red_ISLTR'].Value
                                    	cont2.Rows[i].Columns['Future_Red_ISLTR'].Value=cont1.Rows[i].Columns['Future_Red_ISLTR'].Value
                                    	cont2.Rows[i].Columns['Non_Red_ISLTR'].Value=cont1.Rows[i].Columns['Non_Red_ISLTR'].Value
                                    	#cont2.Rows[i].Columns['IO_Type_with_hint'].Value=cont1.Rows[i].Columns['IO_Type_with_hint'].Value
                                    	cont2.Rows[i].Columns['Red_RLY'].Value=cont1.Rows[i].Columns['Red_RLY'].Value
                                    	cont2.Rows[i].Columns['Future_Red_RLY'].Value=cont1.Rows[i].Columns['Future_Red_RLY'].Value
                                    	cont2.Rows[i].Columns['Non_Red_RLY'].Value=cont1.Rows[i].Columns['Non_Red_RLY'].Value
                                    	#cont2.Rows[i].Columns['DI'].Value=cont1.Rows[i].Columns['DI'].Value
                                    	#cont2.Rows[i].Columns['DO'].Value=cont1.Rows[i].Columns['DO'].Value
                                    	#cont2.Rows[i].Columns['Labor_IS'].Value=cont1.Rows[i].Columns['Labor_IS'].Value
                                    	cont2.Rows[i].Columns['Red_HV_Rly'].Value=cont1.Rows[i].Columns['Red_HV_Rly'].Value
                                    	cont2.Rows[i].Columns['Future_HV_Rly'].Value=cont1.Rows[i].Columns['Future_HV_Rly'].Value
                                    	cont2.Rows[i].Columns['Non_Red_HV_Rly'].Value=cont1.Rows[i].Columns['Non_Red_HV_Rly'].Value
                            except Exception as error:
                                        Log.Info('Error in C300_CG_Universal_IO_cont_2 '+ str(error))
                                        pass
                            
                            try:
                                if r2qParentC300ControlGroupContainerRow.Product.Attr('C300_CG_Universal_IO_Mark_1').Allowed:
                                    Log.Info('Inside Container :  C300_CG_Universal_IO_Mark_1')
                                    cont1= r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('C300_CG_Universal_IO_Mark_1')
                                    rowCount=r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('C300_CG_Universal_IO_Mark_1').Rows.Count
                                    cont2= existingFlowC300ControlGroupContainerRow.Product.GetContainerByName('C300_CG_Universal_IO_Mark_1')
                                    for i in range(rowCount):
                                    	Log.Info('Inside Container :  cont1 ' + str(cont1.Rows[i].Columns['Red_IS'].Value))
                                    	cont2.Rows[i].Columns['Red_IS'].Value=cont1.Rows[i].Columns['Red_IS'].Value
                                    	Log.Info('Inside Container :  cont2 ' + str(cont2.Rows[i].Columns['Red_IS'].Value))
                                    	cont2.Rows[i].Columns['Future_Red_IS'].Value=cont1.Rows[i].Columns['Future_Red_IS'].Value
                                    	cont2.Rows[i].Columns['Non_Red_IS'].Value=cont1.Rows[i].Columns['Non_Red_IS'].Value
                                    	cont2.Rows[i].Columns['Red_NIS'].Value=cont1.Rows[i].Columns['Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Future_Red_NIS'].Value=cont1.Rows[i].Columns['Future_Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Non_Red_NIS'].Value=cont1.Rows[i].Columns['Non_Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Red_ISLTR'].Value=cont1.Rows[i].Columns['Red_ISLTR'].Value
                                    	cont2.Rows[i].Columns['Future_Red_ISLTR'].Value=cont1.Rows[i].Columns['Future_Red_ISLTR'].Value
                                    	cont2.Rows[i].Columns['Non_Red_ISLTR'].Value=cont1.Rows[i].Columns['Non_Red_ISLTR'].Value
                                    	#cont2.Rows[i].Columns['IO_Type_with_hint'].Value=cont1.Rows[i].Columns['IO_Type_with_hint'].Value
                                    	#cont2.Rows[i].Columns['AI'].Value=cont1.Rows[i].Columns['AI'].Value
                                    	#cont2.Rows[i].Columns['AO'].Value=cont1.Rows[i].Columns['AO'].Value
                                    	#cont2.Rows[i].Columns['Labor_IS'].Value=cont1.Rows[i].Columns['Labor_IS'].Value
                            except Exception as error:
                                Log.Info('Error in C300_CG_Universal_IO_Mark_1 '+ str(error))
                                pass
                           
                            try:
                                if r2qParentC300ControlGroupContainerRow.Product.Attr('C300_CG_Universal_IO_Mark_2').Allowed:
                                    cont1= r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('C300_CG_Universal_IO_Mark_2')
                                    rowCount=r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('C300_CG_Universal_IO_Mark_2').Rows.Count
                                    cont2= existingFlowC300ControlGroupContainerRow.Product.GetContainerByName('C300_CG_Universal_IO_Mark_2')
                                    for i in range(rowCount):
                                    	cont2.Rows[i].Columns['Red_IS'].Value=cont1.Rows[i].Columns['Red_IS'].Value
                                    	cont2.Rows[i].Columns['Future_Red_IS'].Value=cont1.Rows[i].Columns['Future_Red_IS'].Value
                                    	cont2.Rows[i].Columns['Non_Red_IS'].Value=cont1.Rows[i].Columns['Non_Red_IS'].Value
                                    	cont2.Rows[i].Columns['Red_NIS'].Value=cont1.Rows[i].Columns['Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Future_Red_NIS'].Value=cont1.Rows[i].Columns['Future_Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Non_Red_NIS'].Value=cont1.Rows[i].Columns['Non_Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Red_ISLTR'].Value=cont1.Rows[i].Columns['Red_ISLTR'].Value
                                    	cont2.Rows[i].Columns['Future_Red_ISLTR'].Value=cont1.Rows[i].Columns['Future_Red_ISLTR'].Value
                                    	cont2.Rows[i].Columns['Non_Red_ISLTR'].Value=cont1.Rows[i].Columns['Non_Red_ISLTR'].Value
                                    	#cont2.Rows[i].Columns['IO_Type_with_hint'].Value=cont1.Rows[i].Columns['IO_Type_with_hint'].Value
                                    	cont2.Rows[i].Columns['Red_RLY'].Value=cont1.Rows[i].Columns['Red_RLY'].Value
                                    	cont2.Rows[i].Columns['Future_Red_RLY'].Value=cont1.Rows[i].Columns['Future_Red_RLY'].Value
                                    	cont2.Rows[i].Columns['Non_Red_RLY'].Value=cont1.Rows[i].Columns['Non_Red_RLY'].Value
                                    	#cont2.Rows[i].Columns['DI'].Value=cont1.Rows[i].Columns['DI'].Value
                                    	#cont2.Rows[i].Columns['DO'].Value=cont1.Rows[i].Columns['DO'].Value
                                    	#cont2.Rows[i].Columns['Labor_IS'].Value=cont1.Rows[i].Columns['Labor_IS'].Value
                                    	cont2.Rows[i].Columns['Red_HV_Rly'].Value=cont1.Rows[i].Columns['Red_HV_Rly'].Value
                                    	cont2.Rows[i].Columns['Future_HV_Rly'].Value=cont1.Rows[i].Columns['Future_HV_Rly'].Value
                                    	cont2.Rows[i].Columns['Non_Red_HV_Rly'].Value=cont1.Rows[i].Columns['Non_Red_HV_Rly'].Value
                            except Exception as error:
                                        Log.Info('Error in C300_CG_Universal_IO_Mark_2 '+ str(error))
                                        pass
                            
                            try:
                                if r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_CG_Enhanced_Function_IO_Cont2').Allowed:
                                    cont1= r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('SerC_CG_Enhanced_Function_IO_Cont2')
                                    rowCount=r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('SerC_CG_Enhanced_Function_IO_Cont2').Rows.Count
                                    cont2= existingFlowC300ControlGroupContainerRow.Product.GetContainerByName('SerC_CG_Enhanced_Function_IO_Cont2')
                                    for i in range(rowCount):
                                    	cont2.Rows[i].Columns['Red_IS'].Value=cont1.Rows[i].Columns['Red_IS'].Value
                                    	cont2.Rows[i].Columns['Future_Red_IS'].Value=cont1.Rows[i].Columns['Future_Red_IS'].Value
                                    	cont2.Rows[i].Columns['Non_Red_IS'].Value=cont1.Rows[i].Columns['Non_Red_IS'].Value
                                    	cont2.Rows[i].Columns['Red_NIS'].Value=cont1.Rows[i].Columns['Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Future_Red_NIS'].Value=cont1.Rows[i].Columns['Future_Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Non_Red_NIS'].Value=cont1.Rows[i].Columns['Non_Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Red_ISLTR'].Value=cont1.Rows[i].Columns['Red_ISLTR'].Value
                                    	cont2.Rows[i].Columns['Future_Red_ISLTR'].Value=cont1.Rows[i].Columns['Future_Red_ISLTR'].Value
                                    	cont2.Rows[i].Columns['Non_Red_ISLTR'].Value=cont1.Rows[i].Columns['Non_Red_ISLTR'].Value
                                    	#cont2.Rows[i].Columns['IO_Type_with_hint'].Value=cont1.Rows[i].Columns['IO_Type_with_hint'].Value
                                    	cont2.Rows[i].Columns['Red_RLY'].Value=cont1.Rows[i].Columns['Red_RLY'].Value
                                    	cont2.Rows[i].Columns['Future_Red_RLY'].Value=cont1.Rows[i].Columns['Future_Red_RLY'].Value
                                    	cont2.Rows[i].Columns['Non_Red_RLY'].Value=cont1.Rows[i].Columns['Non_Red_RLY'].Value
                                    	#cont2.Rows[i].Columns['AI'].Value=cont1.Rows[i].Columns['AI'].Value
                                    	#cont2.Rows[i].Columns['DI'].Value=cont1.Rows[i].Columns['DI'].Value
                                    	#cont2.Rows[i].Columns['DO'].Value=cont1.Rows[i].Columns['DO'].Value
                                    	#cont2.Rows[i].Columns['Parent_Product'].Value=cont1.Rows[i].Columns['Parent_Product'].Value
                                    	cont2.Rows[i].Columns['Red_HV_Rly'].Value=cont1.Rows[i].Columns['Red_HV_Rly'].Value
                                    	cont2.Rows[i].Columns['Future_HV_Rly'].Value=cont1.Rows[i].Columns['Future_HV_Rly'].Value
                                        cont2.Rows[i].Columns['Non_Red_HV_Rly'].Value=cont1.Rows[i].Columns['Non_Red_HV_Rly'].Value
                            except Exception as error:
                                Log.Info('Error in SerC_CG_Enhanced_Function_IO_Cont2 '+ str(error))
                                pass
                                    
                            try:
                                if r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_CG_Enhanced_Function_IO_Cont').Allowed:
                                    cont1= r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('SerC_CG_Enhanced_Function_IO_Cont')
                                    rowCount=r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('SerC_CG_Enhanced_Function_IO_Cont').Rows.Count
                                    cont2= existingFlowC300ControlGroupContainerRow.Product.GetContainerByName('SerC_CG_Enhanced_Function_IO_Cont')
                                    for i in range(rowCount):
                                    	cont2.Rows[i].Columns['Red_IS'].Value=cont1.Rows[i].Columns['Red_IS'].Value
                                    	cont2.Rows[i].Columns['Future_Red_IS'].Value=cont1.Rows[i].Columns['Future_Red_IS'].Value
                                    	cont2.Rows[i].Columns['Non_Red_IS'].Value=cont1.Rows[i].Columns['Non_Red_IS'].Value
                                    	cont2.Rows[i].Columns['Red_NIS'].Value=cont1.Rows[i].Columns['Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Future_Red_NIS'].Value=cont1.Rows[i].Columns['Future_Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Non_Red_NIS'].Value=cont1.Rows[i].Columns['Non_Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Red_ISLTR'].Value=cont1.Rows[i].Columns['Red_ISLTR'].Value
                                    	cont2.Rows[i].Columns['Future_Red_ISLTR'].Value=cont1.Rows[i].Columns['Future_Red_ISLTR'].Value
                                    	cont2.Rows[i].Columns['Non_Red_ISLTR'].Value=cont1.Rows[i].Columns['Non_Red_ISLTR'].Value
                                    	#cont2.Rows[i].Columns['IO_Type_with_hint'].Value=cont1.Rows[i].Columns['IO_Type_with_hint'].Value
                                    	#cont2.Rows[i].Columns['AI'].Value=cont1.Rows[i].Columns['AI'].Value
                                    	#cont2.Rows[i].Columns['AO'].Value=cont1.Rows[i].Columns['AO'].Value
                                    	#cont2.Rows[i].Columns['Labor_IS'].Value=cont1.Rows[i].Columns['Labor_IS'].Value
                            except Exception as error:
                                        Log.Info('Error in SerC_CG_Enhanced_Function_IO_Cont '+ str(error))
                                        pass
                            
                            try:
                                if r2qParentC300ControlGroupContainerRow.Product.Attr('C300_TurboM_IOM_CG_Cont').Allowed:
                                    cont1= r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('C300_TurboM_IOM_CG_Cont')
                                    rowCount=r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('C300_TurboM_IOM_CG_Cont').Rows.Count
                                    cont2= existingFlowC300ControlGroupContainerRow.Product.GetContainerByName('C300_TurboM_IOM_CG_Cont')
                                    for i in range(rowCount):
                                    	cont2.Rows[i].Columns['Red_IOM'].Value=cont1.Rows[i].Columns['Red_IOM'].Value
                            except Exception as error:
                                        Log.Info('Error in C300_TurboM_IOM_CG_Cont '+ str(error))
                                        pass
                            
                            try:
                                if r2qParentC300ControlGroupContainerRow.Product.Attr('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont').Allowed:
                                    cont1= r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont')
                                    rowCount=r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont').Rows.Count
                                    cont2= existingFlowC300ControlGroupContainerRow.Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont')
                                    for i in range(rowCount):
                                    	cont2.Rows[i].Columns['Red_IS'].Value=cont1.Rows[i].Columns['Red_IS'].Value
                                    	cont2.Rows[i].Columns['Future_Red_IS'].Value=cont1.Rows[i].Columns['Future_Red_IS'].Value
                                    	cont2.Rows[i].Columns['Non_Red_IS'].Value=cont1.Rows[i].Columns['Non_Red_IS'].Value
                                    	cont2.Rows[i].Columns['Red_NIS'].Value=cont1.Rows[i].Columns['Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Future_Red_NIS'].Value=cont1.Rows[i].Columns['Future_Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Non_Red_NIS'].Value=cont1.Rows[i].Columns['Non_Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Red_ISLTR'].Value=cont1.Rows[i].Columns['Red_ISLTR'].Value
                                    	cont2.Rows[i].Columns['Future_Red_ISLTR'].Value=cont1.Rows[i].Columns['Future_Red_ISLTR'].Value
                                    	cont2.Rows[i].Columns['Non_Red_ISLTR'].Value=cont1.Rows[i].Columns['Non_Red_ISLTR'].Value
                                    	#cont2.Rows[i].Columns['IO_Type_info'].Value=cont1.Rows[i].Columns['IO_Type_info'].Value
                                    	#cont2.Rows[i].Columns['Validation_check'].Value=cont1.Rows[i].Columns['Validation_check'].Value
                                    	#cont2.Rows[i].Columns['AI'].Value=cont1.Rows[i].Columns['AI'].Value
                                    	#cont2.Rows[i].Columns['AO'].Value=cont1.Rows[i].Columns['AO'].Value
                                    	#cont2.Rows[i].Columns['Labor_IS'].Value=cont1.Rows[i].Columns['Labor_IS'].Value
                            except Exception as error:
                                        Log.Info('Error in C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont '+ str(error))
                                        pass
                            
                            try:
                                if r2qParentC300ControlGroupContainerRow.Product.Attr('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1').Allowed:
                                    cont1= r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1')
                                    rowCount=r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1').Rows.Count
                                    cont2= existingFlowC300ControlGroupContainerRow.Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1')
                                    for i in range(rowCount):
                                    	cont2.Rows[i].Columns['Red_IS'].Value=cont1.Rows[i].Columns['Red_IS'].Value
                                    	cont2.Rows[i].Columns['Future_Red_IS'].Value=cont1.Rows[i].Columns['Future_Red_IS'].Value
                                    	cont2.Rows[i].Columns['Non_Red_IS'].Value=cont1.Rows[i].Columns['Non_Red_IS'].Value
                                    	cont2.Rows[i].Columns['Red_NIS'].Value=cont1.Rows[i].Columns['Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Future_Red_NIS'].Value=cont1.Rows[i].Columns['Future_Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Non_Red_NIS'].Value=cont1.Rows[i].Columns['Non_Red_NIS'].Value
                                    	cont2.Rows[i].Columns['Red_ISLTR'].Value=cont1.Rows[i].Columns['Red_ISLTR'].Value
                                    	cont2.Rows[i].Columns['Future_Red_ISLTR'].Value=cont1.Rows[i].Columns['Future_Red_ISLTR'].Value
                                    	cont2.Rows[i].Columns['Non_Red_ISLTR'].Value=cont1.Rows[i].Columns['Non_Red_ISLTR'].Value
                                    	cont2.Rows[i].Columns['Rank'].Value=cont1.Rows[i].Columns['Rank'].Value
                                    	cont2.Rows[i].Columns['Red_RLY'].Value=cont1.Rows[i].Columns['Red_RLY'].Value
                                    	cont2.Rows[i].Columns['Future_Red_RLY'].Value=cont1.Rows[i].Columns['Future_Red_RLY'].Value
                                    	cont2.Rows[i].Columns['Non_Red_RLY'].Value=cont1.Rows[i].Columns['Non_Red_RLY'].Value
                                    	#cont2.Rows[i].Columns['IO_Type_info'].Value=cont1.Rows[i].Columns['IO_Type_info'].Value
                                    	#cont2.Rows[i].Columns['Message_Check'].Value=cont1.Rows[i].Columns['Message_Check'].Value
                                    	#cont2.Rows[i].Columns['DO'].Value=cont1.Rows[i].Columns['DO'].Value
                                    	#cont2.Rows[i].Columns['DI'].Value=cont1.Rows[i].Columns['DI'].Value
                                    	#cont2.Rows[i].Columns['AI'].Value=cont1.Rows[i].Columns['AI'].Value
                                    	#cont2.Rows[i].Columns['Labor_IS'].Value=cont1.Rows[i].Columns['Labor_IS'].Value
                                    	cont2.Rows[i].Columns['Red_HV_Rly'].Value=cont1.Rows[i].Columns['Red_HV_Rly'].Value
                                    	cont2.Rows[i].Columns['Future_HV_Rly'].Value=cont1.Rows[i].Columns['Future_HV_Rly'].Value
                                    	cont2.Rows[i].Columns['Non_Red_HV_Rly'].Value=cont1.Rows[i].Columns['Non_Red_HV_Rly'].Value
                            except Exception as error:
                                Log.Info('Error in C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1 '+ str(error))
                                pass
                            try:
                                if r2qParentC300ControlGroupContainerRow.Product.Attr('SerC_CG_FIM_FF_IO_Cont').Allowed:
                                    cont1= r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('SerC_CG_FIM_FF_IO_Cont')
                                    rowCount=r2qParentC300ControlGroupContainerRow.Product.GetContainerByName('SerC_CG_FIM_FF_IO_Cont').Rows.Count
                                    cont2= existingFlowC300ControlGroupContainerRow.Product.GetContainerByName('SerC_CG_FIM_FF_IO_Cont')
                                    for i in range(rowCount):
                                    	cont2.Rows[i].Columns['Red_wo_C300'].Value=cont1.Rows[i].Columns['Red_wo_C300'].Value
                                    	cont2.Rows[i].Columns['Future_Red_wo_C300'].Value=cont1.Rows[i].Columns['Future_Red_wo_C300'].Value
                                    	cont2.Rows[i].Columns['Non_Red_wo_C300'].Value=cont1.Rows[i].Columns['Non_Red_wo_C300'].Value
                                    	cont2.Rows[i].Columns['Red_C300'].Value=cont1.Rows[i].Columns['Red_C300'].Value
                                    	cont2.Rows[i].Columns['Future_Red_C300'].Value=cont1.Rows[i].Columns['Future_Red_C300'].Value
                                    	cont2.Rows[i].Columns['Non_Red_C300'].Value=cont1.Rows[i].Columns['Non_Red_C300'].Value
                                    	#cont2.Rows[i].Columns['Identifiers'].Value=cont1.Rows[i].Columns['Identifiers'].Value
                                    	#cont2.Rows[i].Columns['AO'].Value=cont1.Rows[i].Columns['AO'].Value
                                    	#cont2.Rows[i].Columns['AI'].Value=cont1.Rows[i].Columns['AI'].Value
                            except Exception as error:
                                Log.Info('Error in SerC_CG_FIM_FF_IO_Cont '+ str(error))
                                pass
                            existingFlowC300ControlGroupContainerRow.Product.ChangeTab('Part Summary')