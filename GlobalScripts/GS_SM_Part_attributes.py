class AttrStorage:
    def get_column_value(self, row, col):
        return row.GetColumnByName(col).Value

    def __init__(self, Product):
        if Product.Name == "SM Control Group":
            # Control Group
            self.Marshalling_Opt_cg = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').Value

            io_count_ai_cont_rows = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows
            io_count_ao_cont_rows = Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont').Rows
            io_count_do_cont_rows = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows
            io_count_di_cont_rows = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows

            #remote group row count
            #self.rg_row = Product.GetContainerByName('SM_RemoteGroup_Cont').Rows.Count
            if self.Marshalling_Opt_cg == "Hardware_Marshalling_with_P+F":
                # AI
                try:
                    self.type_uio_ai_rd = self.get_column_value(io_count_ai_cont_rows[1], "Red (IS)")
                except:
                    self.type_uio_ai_rd = 0
                try:
                    self.type_uio_ai_nrd = self.get_column_value(io_count_ai_cont_rows[1], "Non Red (IS)")
                except:
                    self.type_uio_ai_nrd = 0
                # AO
                try:
                    self.type_uio_ao_rd = self.get_column_value(io_count_ao_cont_rows[1], "Red (IS)")
                except:
                    self.type_uio_ao_rd = 0
                try:
                    self.type_uio_ao_nrd = self.get_column_value(io_count_ao_cont_rows[1], "Non Red (IS)")
                except:
                    self.type_uio_ao_nrd = 0
                # DI
                try:
                    self.sil2_uio_di_rd = self.get_column_value(io_count_di_cont_rows[1], "Red (IS)")
                except:
                    self.sil2_uio_di_rd = 0
                try:
                    self.sil2_uio_di_nrd = self.get_column_value(io_count_di_cont_rows[1], "Non Red (IS)")
                except:
                    self.sil2_uio_di_nrd = 0
                try:
                    self.sil3_uio_di_rd = self.get_column_value(io_count_di_cont_rows[2], "Red (IS)")
                except:
                    self.sil3_uio_di_rd = 0
                try:
                    self.sil3_uio_di_nrd = self.get_column_value(io_count_di_cont_rows[2], "Non Red (IS)")
                except:
                    self.sil3_uio_di_nrd = 0
                # DO
                try:
                    self.sil3_uio_do_rd = self.get_column_value(io_count_do_cont_rows[1], "Red (IS)")
                except:
                    self.sil3_uio_do_rd = 0
                try:
                    self.sil3_uio_do_nrd = self.get_column_value(io_count_do_cont_rows[1], "Non Red (IS)")
                except:
                    self.sil3_uio_do_nrd = 0

        if Product.Name == "SM Remote Group":
            # Remote Group
            Marshalling_Opt = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows
            self.Marshalling_Opt_rg = self.get_column_value(Marshalling_Opt[0], "Marshalling_Option")

            io_count_ai_cont_rows = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows
            io_count_ao_cont_rows = Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows
            io_count_do_cont_rows = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows
            io_count_di_cont_rows = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows

            #remote group row count
            #self.rg_row = Product.GetContainerByName('SM_RemoteGroup_Cont').Rows.Count
            if self.Marshalling_Opt_rg == "Hardware_Marshalling_with_P+F":
                # AI
                try:
                    self.type_uio_ai_rd = self.get_column_value(io_count_ai_cont_rows[1], "Red_IS")
                except:
                    self.type_uio_ai_rd = 0
                try:
                    self.type_uio_ai_nrd = self.get_column_value(io_count_ai_cont_rows[1], "Non_Red_IS")
                except:
                    self.type_uio_ai_nrd = 0
                # AO
                try:
                    self.type_uio_ao_rd = self.get_column_value(io_count_ao_cont_rows[1], "Red_IS")
                except:
                    self.type_uio_ao_rd = 0
                try:
                    self.type_uio_ao_nrd = self.get_column_value(io_count_ao_cont_rows[1], "Non_Red_IS")
                except:
                    self.type_uio_ao_nrd = 0
                # DI
                try:
                    self.sil2_uio_di_rd = self.get_column_value(io_count_di_cont_rows[1], "Red_IS")
                except:
                    self.sil2_uio_di_rd = 0
                try:
                    self.sil2_uio_di_nrd = self.get_column_value(io_count_di_cont_rows[1], "Non_Red_IS")
                except:
                    self.sil2_uio_di_nrd = 0
                try:
                    self.sil3_uio_di_rd = self.get_column_value(io_count_di_cont_rows[2], "Red_IS")
                except:
                    self.sil3_uio_di_rd = 0
                try:
                    self.sil3_uio_di_nrd = self.get_column_value(io_count_di_cont_rows[2], "Non_Red_IS")
                except:
                    self.sil3_uio_di_nrd = 0
                # DO
                try:
                    self.sil3_uio_do_rd = self.get_column_value(io_count_do_cont_rows[1], "Red_IS")
                except:
                    self.sil3_uio_do_rd = 0
                try:
                    self.sil3_uio_do_nrd = self.get_column_value(io_count_do_cont_rows[1], "Non_Red_IS")
                except:
                    self.sil3_uio_do_nrd = 0