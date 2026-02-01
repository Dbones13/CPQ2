class AttrStorage:
    def get_column_value(self, row, col):
        return row.GetColumnByName(col).Value

    def get_value(self, container_rows, key, value, col):
        row = container_rows.GetByColumnName(key, value)
        if row:
            return self.get_column_value(row, col)
        return 0

    def __init__(self, Product):
        if Product.Name == "SM Control Group":
            # Control Group
            self.Universal_IOTA=Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Universal_IOTA').Value
            self.Marshalling_Opt_cg = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').Value
            self.SIC_length= Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('SIC_Length').DisplayValue

            io_count_ai_cont_rows = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows
            io_count_ao_cont_rows = Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont').Rows
            io_count_do_cont_rows = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows
            io_count_di_cont_rows = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows
            general_que_cont_rows = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows
            cabinet_details_left_cont_rows = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows
            cabinet_details_right_cont_rows = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows

            self.saftey_io_switch = self.get_column_value(general_que_cont_rows[0], "SM_Switch_Safety_IO")
            self.distance_to_module = self.get_column_value(cabinet_details_left_cont_rows[0], "Distance_SM_SC_UIO/DIO_modules")
            self.extended_temp = self.get_column_value(cabinet_details_left_cont_rows[0], "Extended_Temperature")
            self.conformally_coated = self.get_column_value(cabinet_details_right_cont_rows[0], "Conformally_Coated")
            self.cabinet_feeder = self.get_column_value(cabinet_details_left_cont_rows[0], "Cabinet_Feeder_Voltage")
            self.power_supply = self.get_column_value(cabinet_details_left_cont_rows[0], "Power_Supply")
            self.sdo7_line_mon_uio_rd_is = self.get_value(io_count_do_cont_rows, "Digital Output Type", "SDO(7) 24Vdc Line Mon UIO (0-5000)", "Red (IS)")
            self.sdo7_line_mon_uio_nrd_is = self.get_value(io_count_do_cont_rows, "Digital Output Type", "SDO(7) 24Vdc Line Mon UIO (0-5000)", "Non Red (IS)")
            self.sdo7_line_mon_uio_rd_nis = self.get_value(io_count_do_cont_rows, "Digital Output Type", "SDO(7) 24Vdc Line Mon UIO (0-5000)", "Red (NIS)")
            self.sdo7_line_mon_uio_nrd_nis = self.get_value(io_count_do_cont_rows, "Digital Output Type", "SDO(7) 24Vdc Line Mon UIO (0-5000)", "Non Red (NIS)")

            if self.Marshalling_Opt_cg == "Hardware_Marshalling_with_P+F":
                # AI
                try:
                    self.type_uio_ai_rd = int(self.get_column_value(io_count_ai_cont_rows[1], "Red (IS)"))

                except:
                    self.type_uio_ai_rd = 0
                try:
                    self.type_uio_ai_nrd = int(self.get_column_value(io_count_ai_cont_rows[1], "Non Red (IS)"))
                except:
                    self.type_uio_ai_nrd = 0
                # AO
                try:
                    self.type_uio_ao_rd = int(self.get_column_value(io_count_ao_cont_rows[1], "Red (IS)"))
                except:
                    self.type_uio_ao_rd = 0
                try:
                    self.type_uio_ao_nrd = int(self.get_column_value(io_count_ao_cont_rows[1], "Non Red (IS)"))
                except:
                    self.type_uio_ao_nrd = 0
                # DI
                try:
                    self.sil2_uio_di_rd = int(self.get_column_value(io_count_di_cont_rows[1], "Red (IS)"))
                except:
                    self.sil2_uio_di_rd = 0
                try:
                    self.sil2_uio_di_nrd = int(self.get_column_value(io_count_di_cont_rows[1], "Non Red (IS)"))
                except:
                    self.sil2_uio_di_nrd = 0
                try:
                    self.sil3_uio_di_rd = int(self.get_column_value(io_count_di_cont_rows[2], "Red (IS)"))
                except:
                    self.sil3_uio_di_rd = 0
                try:
                    self.sil3_uio_di_nrd = int(self.get_column_value(io_count_di_cont_rows[2], "Non Red (IS)"))
                except:
                    self.sil3_uio_di_nrd = 0
                # DO
                try:
                    self.sil3_uio_do_rd = int(self.get_column_value(io_count_do_cont_rows[1], "Red (IS)"))
                except:
                    self.sil3_uio_do_rd = 0
                try:
                    self.sil3_uio_do_nrd = int(self.get_column_value(io_count_do_cont_rows[1], "Non Red (IS)"))
                except:
                    self.sil3_uio_do_nrd = 0

        if Product.Name == "SM Remote Group":
            # Remote Group
            self.Marshalling_Opt_rg = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').Value
            self.SIC_length= Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('SIC_Length').DisplayValue

            io_count_ai_cont_rows = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows
            io_count_ao_cont_rows = Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows
            io_count_do_cont_rows = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows
            io_count_di_cont_rows = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows
            #general_que_cont_rows = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows
            cabinet_details_left_cont_rows = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows
            cabinet_details_right_cont_rows = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows
            atex_compliance_enclosure_cont_rows = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows

            self.saftey_io_switch = Product.Attr("SM_CG_Safety_IO_Link").GetValue()
            self.distance_to_module = self.get_column_value(cabinet_details_left_cont_rows[0], "Distance_SM_SC_UIO/DIO_modules")
            self.extended_temp = self.get_column_value(cabinet_details_left_cont_rows[0], "Extended_Temperature")
            self.enclosure_type = self.get_column_value(atex_compliance_enclosure_cont_rows[0], "Enclosure_Type")
            self.conformally_coated = self.get_column_value(cabinet_details_right_cont_rows[0], "SM_Conformally_Coated")
            self.cabinet_feeder = self.get_column_value(cabinet_details_left_cont_rows[0], "Cabinet_Feeder_Voltage")
            self.power_supply = self.get_column_value(cabinet_details_left_cont_rows[0], "Power_Supply")
            self.sdo7_line_mon_uio_rd_is = self.get_value(io_count_do_cont_rows, "Digital_Output_Type", "SDO(7) 24Vdc Line Mon UIO  (0-5000)", "Red_IS")
            self.sdo7_line_mon_uio_nrd_is = self.get_value(io_count_do_cont_rows, "Digital_Output_Type", "SDO(7) 24Vdc Line Mon UIO  (0-5000)", "Non_Red_IS")
            self.sdo7_line_mon_uio_rd_nis = self.get_value(io_count_do_cont_rows, "Digital_Output_Type", "SDO(7) 24Vdc Line Mon UIO  (0-5000)", "Red_NIS")
            self.sdo7_line_mon_uio_nrd_nis = self.get_value(io_count_do_cont_rows, "Digital_Output_Type", "SDO(7) 24Vdc Line Mon UIO  (0-5000)", "Non_Red_NIS")

            if self.Marshalling_Opt_rg == "Hardware_Marshalling_with_P+F":
                # AI
                try:
                    self.type_uio_ai_rd = int(self.get_column_value(io_count_ai_cont_rows[1], "Red_IS"))

                except:
                    self.type_uio_ai_rd = 0
                try:
                    self.type_uio_ai_nrd = int(self.get_column_value(io_count_ai_cont_rows[1], "Non_Red_IS"))
                except:
                    self.type_uio_ai_nrd = 0
                # AO
                try:
                    self.type_uio_ao_rd = int(self.get_column_value(io_count_ao_cont_rows[1], "Red_IS"))
                except:
                    self.type_uio_ao_rd = 0
                try:
                    self.type_uio_ao_nrd = int(self.get_column_value(io_count_ao_cont_rows[1], "Non_Red_IS"))
                except:
                    self.type_uio_ao_nrd = 0
                # DI
                try:
                    self.sil2_uio_di_rd = int(self.get_column_value(io_count_di_cont_rows[1], "Red_IS"))
                except:
                    self.sil2_uio_di_rd = 0
                try:
                    self.sil2_uio_di_nrd = int(self.get_column_value(io_count_di_cont_rows[1], "Non_Red_IS"))
                except:
                    self.sil2_uio_di_nrd = 0
                try:
                    self.sil3_uio_di_rd = int(self.get_column_value(io_count_di_cont_rows[2], "Red_IS"))
                except:
                    self.sil3_uio_di_rd = 0
                try:
                    self.sil3_uio_di_nrd = int(self.get_column_value(io_count_di_cont_rows[2], "Non_Red_IS"))
                except:
                    self.sil3_uio_di_nrd = 0
                # DO
                try:
                    self.sil3_uio_do_rd = int(self.get_column_value(io_count_do_cont_rows[1], "Red_IS"))
                except:
                    self.sil3_uio_do_rd = 0
                try:
                    self.sil3_uio_do_nrd = int(self.get_column_value(io_count_do_cont_rows[1], "Non_Red_IS"))
                except:
                    self.sil3_uio_do_nrd = 0