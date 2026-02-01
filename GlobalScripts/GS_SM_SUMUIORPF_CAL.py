import math as m
class AttrStorage:
    def get_column_value(self, row, col):
        return row.GetColumnByName(col).Value
        Trace.Write(row.GetColumnByName(col).Value)
    # CONTROL GROUP LEVEL
    def __init__(self, Product):
        if Product.Name=="SM Control Group":
            Marshalling_Option = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
            if Marshalling_Option =="Hardware Marshalling with P+F":
                #CXCPQ-30834
                try:
                    self.percent_spare_io = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName('Percent_Installed_Spare_IOs').Value
                except:
                    self.percent_spare_io = 0
                try:
                    self.sil2_red = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName('Red (IS)').Value
                except:
                    self.sil2_red = 0
                try:
                    self.sil3_red = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName('Red (IS)').Value
                except:
                    self.sil3_red = 0
                try:
                    self.currentmA_red = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName('Red (IS)').Value
                except:
                    self.currentmA_red = 0
                try:
                    self.currentmAPF_red = Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont').Rows[1].GetColumnByName('Red (IS)').Value
                except:
                    self.currentmAPF_red = 0
                try:
                    self.sil3pf_red = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName('Red (IS)').Value
                except:
                    self.sil3pf_red = 0
        if Product.Name=="SM Remote Group":
            Enclosure_Type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
            if Enclosure_Type == "Cabinet":
                Marshalling_Option = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
                if Marshalling_Option =="Hardware Marshalling with P+F":
                    try:
                        self.percent_spare_io = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName('SM_Percent_Installed_Spare_IO').Value
                    except:
                        self.percent_spare_io = 0
                    try:
                        self.sil2_red = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName('Red_IS').Value
                    except:
                        self.sil2_red = 0
                    try:
                        self.sil3_red = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName('Red_IS').Value
                    except:
                        self.sil3_red = 0
                    try:
                        self.currentmA_red = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName('Red_IS').Value
                    except:
                        self.currentmA_red = 0
                    try:
                        self.currentmAPF_red = Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows[1].GetColumnByName('Red_IS').Value
                    except:
                        self.currentmAPF_red = 0
                    try:
                        self.sil3pf_red = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName('Red_IS').Value
                    except:
                        self.sil3pf_red = 0