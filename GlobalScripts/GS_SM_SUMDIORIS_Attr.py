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
                #CXCPQ-CXCPQ-30846
                #DI
                try:
                    self.percent_spare_io = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName('Percent_Installed_Spare_IOs').Value
                except:
                    self.percent_spare_io = 0
                try:
                    self.dio_di_rdis = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[4].GetColumnByName('Red (IS)').Value
                except:
                    self.dio_di_rdis = 0
                try:
                    self.line_mon_dio_di_rdis = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[5].GetColumnByName('Red (IS)').Value
                except:
                    self.line_mon_dio_di_rdis = 0
                #DO
                try:
                    self.dio_do_rdis = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[5].GetColumnByName('Red (IS)').Value
                except:
                    self.dio_do_rdis = 0
                # Marshalling_Option =="Hardware Marshalling with P+F"
            elif Marshalling_Option =="Universal Marshalling":
                #CXCPQ-CXCPQ-30846
                #DI
                try:
                    self.percent_spare_io = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName('Percent_Installed_Spare_IOs').Value
                except:
                    self.percent_spare_io = 0
                try:
                    self.dio_di_rdis = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[3].GetColumnByName('Red (IS)').Value
                except:
                    self.dio_di_rdis = 0
                try:
                    self.line_mon_dio_di_rdis = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[4].GetColumnByName('Red (IS)').Value
                except:
                    self.line_mon_dio_di_rdis = 0
                #DO
                try:
                    self.dio_do_rdis = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[4].GetColumnByName('Red (IS)').Value
                except:
                    self.dio_do_rdis = 0
            elif Marshalling_Option =="Hardware Marshalling with Other":
                #CXCPQ-CXCPQ-30846
                #DI
                try:
                    self.percent_spare_io = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName('Percent_Installed_Spare_IOs').Value
                except:
                    self.percent_spare_io = 0
                try:
                    self.dio_di_rdis = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName('Red (IS)').Value
                except:
                    self.dio_di_rdis = 0
                try:
                    self.line_mon_dio_di_rdis = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[3].GetColumnByName('Red (IS)').Value
                except:
                    self.line_mon_dio_di_rdis = 0
                #DO
                try:
                    self.dio_do_rdis = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[4].GetColumnByName('Red (IS)').Value
                except:
                    self.dio_do_rdis = 0
        if Product.Name=="SM Remote Group":
            Enclosure_Type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
            if Enclosure_Type == "Cabinet":
                Marshalling_Option = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
                if Marshalling_Option =="Hardware Marshalling with P+F":
                    #CXCPQ-CXCPQ-30846
                    try:
                        self.percent_spare_io = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName('SM_Percent_Installed_Spare_IO').Value
                    except:
                        self.percent_spare_io = 0
                    #DI
                    try:
                        self.dio_di_rdis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[4].GetColumnByName('Red_IS').Value
                    except:
                        self.dio_di_rdis = 0
                    try:
                        self.line_mon_dio_di_rdis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[5].GetColumnByName('Red_IS').Value
                    except:
                        self.line_mon_dio_di_rdis = 0
                    #DO
                    try:
                        self.dio_do_rdis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[5].GetColumnByName('Red_IS').Value
                    except:
                        self.dio_do_rdis = 0
                # Marshalling_Option =="Hardware Marshalling with P+F"
                elif Marshalling_Option =="Universal Marshalling":
                    #CXCPQ-CXCPQ-30846
                    #DI
                    try:
                        self.percent_spare_io = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName('SM_Percent_Installed_Spare_IO').Value
                    except:
                        self.percent_spare_io = 0
                    try:
                        self.dio_di_rdis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[3].GetColumnByName('Red_IS').Value
                    except:
                        self.dio_di_rdis = 0
                    try:
                        self.line_mon_dio_di_rdis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[4].GetColumnByName('Red_IS').Value
                    except:
                        self.line_mon_dio_di_rdis = 0
                    #DO
                    try:
                        self.dio_do_rdis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[4].GetColumnByName('Red_IS').Value
                    except:
                        self.dio_do_rdis = 0
                elif Marshalling_Option =="Hardware Marshalling with Other":
                    #CXCPQ-CXCPQ-30846
                    #DI
                    try:
                        self.percent_spare_io = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName('SM_Percent_Installed_Spare_IO').Value
                    except:
                        self.percent_spare_io = 0
                    try:
                        self.dio_di_rdis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName('Red_IS').Value
                    except:
                        self.dio_di_rdis = 0
                    try:
                        self.line_mon_dio_di_rdis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[3].GetColumnByName('Red_IS').Value
                    except:
                        self.line_mon_dio_di_rdis = 0
                    #DO
                    try:
                        self.dio_do_rdis = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[4].GetColumnByName('Red_IS').Value
                    except:
                        self.dio_do_rdis = 0