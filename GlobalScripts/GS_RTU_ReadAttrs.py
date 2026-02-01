# GS_RTU_ReadAttrs

class AttrStorage:
    def __init__(self, Product):
        ## Product: Project
        if Product.Name == "New / Expansion Project":

            ## Container: CE_Project_Questions_Cont
            ce_proj_cont = Product.GetContainerByName('CE_Project_Questions_Cont').Rows[0]
            self.ce_proj_type = ce_proj_cont.GetColumnByName('CE_Project_Type').Value
            self.ce_proj_site_volt = ce_proj_cont.GetColumnByName('CE_Site_Voltage').Value
            self.ce_proj_site_freq = ce_proj_cont.GetColumnByName('CE_Site_Frequency').Value

        ## Product: System Group
        elif Product.Name == "System Group":

            #Inherit attr from parent product
            self.ce_proj_site_volt = Product.Attr('CE_Site_Voltage').GetValue()

            ## Container: CE_General_Inputs_Cont
            ce_gen_inputs_cont = Product.GetContainerByName('CE_General_Inputs_Cont').Rows[0]
            self.ce_gen_inputs_sys_asset = ce_gen_inputs_cont.GetColumnByName('CE_System_Asset').Value
            self.ce_gen_inputs_sys_num = ce_gen_inputs_cont.GetColumnByName('CE_System_Number').Value
            self.ce_gen_inputs_ebr_media = ce_gen_inputs_cont.GetColumnByName('CE_EBR_Media').Value

        # UOC System
            ## Product: UOC System
        elif Product.Name == "ControlEdge RTU System":
            # Inheriting site voltage
            self.ce_proj_site_volt = Product.Attr('CE_Site_Voltage').GetValue()

            ## Container: RTU_Software_Labor_Container1
            sfw1_labor_container = Product.GetContainerByName('RTU_Software_Labor_Container1').Rows[0]
            self.gas_liquid_cals = sfw1_labor_container.GetColumnByName('RTU_Gas_Liquid_Metering_Calcs').Value
            self.builder_client_License = sfw1_labor_container.GetColumnByName('RTU_Builder_Client').Value
            self.rtu_engineering_stations = sfw1_labor_container.GetColumnByName('RTU_Engineering_Stations').Value
            self.base_media_delivery = sfw1_labor_container.GetColumnByName('RTU_Base_Media_delivery').Value
            self.ce_rtu_release = sfw1_labor_container.GetColumnByName('RTU_System_Software_Release').Value
            self.rtu_cabinet_mounting = sfw1_labor_container.GetColumnByName('RTU_Cabinet_Required_Racks_Mounting').Value
        elif Product.Name == "RTU Group":
            # Inheriting site voltage
            self.ce_proj_site_volt = Product.Attr('CE_Site_Voltage').GetValue()
            self.cabinet_mounting = Product.Attr('RTU_Cabinet_Required_Racks_Mounting').GetValue()
            # Cabinet cont
            conttrol = Product.GetContainerByName('RTU_CG_Controller_Cont').Rows.Count
            cabinet = Product.GetContainerByName('RTU_CG_Cabinet_Cont').Rows.Count
            if conttrol and cabinet:
                RTU_labor_container_control = Product.GetContainerByName('RTU_CG_Controller_Cont').Rows[0]
                RTU_labor_container_cabinet = Product.GetContainerByName('RTU_CG_Cabinet_Cont').Rows[0]
                self.cabinet_type = RTU_labor_container_cabinet.GetColumnByName('Cabinet_Type').Value
                self.IO_Spare_Percentage = RTU_labor_container_control.GetColumnByName('IO_Spare_Percentage').Value
                self.Cabinet_Thermostat = RTU_labor_container_cabinet.GetColumnByName('Cabinet_Thermostat').Value
                self.cabinet_Door_Type = ''
                #self.cabinet_Door_Type = RTU_labor_container.GetColumnByName('Cabinet_Door_Type').Value
                self.cabinet_access = RTU_labor_container_cabinet.GetColumnByName('Cabinet_Access').Value
                self.cabinet_Base_Size = RTU_labor_container_cabinet.GetColumnByName('Cabinet_Base_Size').Value
                self.cabinet_Door_Keylock = RTU_labor_container_cabinet.GetColumnByName('Cabinet_Door_Keylock').Value
                self.cabinet_Power_Entry = RTU_labor_container_cabinet.GetColumnByName('Cabinet_Power_Entry').Value
                self.cabinet_light = RTU_labor_container_cabinet.GetColumnByName('Cabinet_Light').Value
                self.controller_redundancy = RTU_labor_container_control.GetColumnByName('Controller_Redundancy').Value
                self.pwr_sply_type = RTU_labor_container_control.GetColumnByName('Power_Supply_Type').Value
                self.pwr_sply_model = RTU_labor_container_control.GetColumnByName('Power_Supply_Model').Value
                self.num_replica = RTU_labor_container_control.GetColumnByName('Replica_configurations').Value
                self.io_spare_per = RTU_labor_container_control.GetColumnByName('IO_Spare_Percentage').Value
                self.cab_spare_space_per = RTU_labor_container_cabinet.GetColumnByName('Cabinet_Spare_space').Value
                self.integrated_marshalling_cab = RTU_labor_container_cabinet.GetColumnByName('Integrated_Marshalling_Cabinet').Value
                
            ctio = Product.GetContainerByName('RTU_CG_IO_Container').Rows.Count
            if ctio:
                RTU_IO_container = Product.GetContainerByName('RTU_CG_IO_Container').Rows[0]
                self.Modbus_TCP_IP_Ethernet_Device = RTU_IO_container.GetColumnByName('Modbus_TCP_IP_Ethernet_Device').Value
                self.Non_HART_Analog_Input = RTU_IO_container.GetColumnByName('Non_HART_Analog_Input').Value
                self.HART_Analog_Input = RTU_IO_container.GetColumnByName('HART_Analog_Input').Value
                self.Non_HART_Analog_Output = RTU_IO_container.GetColumnByName('Non_HART_Analog_Output').Value
                self.HART_Analog_Output = RTU_IO_container.GetColumnByName('HART_Analog_Output').Value
                self.Digital_Input = RTU_IO_container.GetColumnByName('Digital_Input').Value
                self.Digital_Output = RTU_IO_container.GetColumnByName('Digital_Output').Value
                self.Digital_Input_Output = RTU_IO_container.GetColumnByName('Digital_Input_Output').Value
                self.Pulse_Input = RTU_IO_container.GetColumnByName('Pulse_Input').Value
                self.FIM_Analog_Input = RTU_IO_container.GetColumnByName('FIM_Analog_Input').Value
                self.FIM_devices_segment_withOpen_loop = RTU_IO_container.GetColumnByName('FIM_devices_segment_withOpen_loop').Value
                self.Number_Segments_FIM4 = RTU_IO_container.GetColumnByName('Number_Segments_FIM4').Value
                self.Field_ISA100 = RTU_IO_container.GetColumnByName('Field_ISA100_Wireless_Devices').Value
                self.FDAP = RTU_IO_container.GetColumnByName('FDAP').Value
                self.Modbus_RS485_Serial_Communication_Devices = RTU_IO_container.GetColumnByName('Modbus_RS485_Serial_Communication_Devices').Value
                self.Modbus_RS232_Serial_Communication_Devices = RTU_IO_container.GetColumnByName('Modbus_RS232_Serial_Communication_Devices').Value
                
            #Software Controller
            ctsw = Product.GetContainerByName('RTU_CG_Sofware_Cont').Rows.Count
            if ctsw:
                RTU_Software_Cont = Product.GetContainerByName('RTU_CG_Sofware_Cont').Rows[0]
                self.Gas_and_Liquid_Meter_Run_License = RTU_Software_Cont.GetColumnByName('Gas_and_Liquid_Meter_Run_License').Value
                self.RTU_ELEPIU_Library_License = RTU_Software_Cont.GetColumnByName('RTU_ELEPIU_Library_License').Value
                self.UpgradeKit_RTU_Non_Redundant = RTU_Software_Cont.GetColumnByName('UpgradeKit_RTU_Non_Redundant').Value
            # Additional Controller
            ctad = Product.GetContainerByName('RTU_CG_AdditionalController_Ques_Cont').Rows.Count
            if ctad:
                RTU_Additional_Cont = Product.GetContainerByName('RTU_CG_AdditionalController_Ques_Cont').Rows[0]
                self.add_ctrl = RTU_Additional_Cont.GetColumnByName('Additional_Controller_Required').Value