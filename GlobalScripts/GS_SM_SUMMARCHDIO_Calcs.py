#CXCPQ-30828
import System.Decimal as D
class IOComponents:
    def __init__(self, Product):
        self.Product  = Product
    def getRowIndex(self, container, column_name, column_value):
        row_index = -1
        for cont_row in container.Rows:
            if column_value == cont_row.GetColumnByName(column_name).Value:
                row_index = cont_row.RowIndex
                break
        return row_index
    def getColumnValue(self, container, row_index, column_name):
        val = 0
        if row_index < 0:
            return 0
        try:
            if container.Rows.Count:
                val = container.Rows[row_index].GetColumnByName(column_name).Value
                if val:
                    val = float(val)
                else:
                    val = 0
        except Exception as e:
            Trace.Write(str(e))
            return 0
        return val
def get_int(value):
    if value:
        return int(value)
    else:
        return 0

def getFloat(value):
    if value:
        return float(value)
    else:
        return 0.0
def getNum(n):
    return 0 if n=="" or n==0 else int(n)
def getSUMMARCHDIOValue(Product):
    SUMMARCHDIO=0
    if Product.Name=="SM Control Group":
        IOComp = IOComponents(Product)
        Marshalling_Option=Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName("Marshalling_Option").DisplayValue
        iota=Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Universal_IOTA').DisplayValue
        if Marshalling_Option == 'Hardware Marshalling with Other' and iota == 'PUIO':
            #DI
            cont = IOComp.Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type','SDI(1) 24Vdc DIO (0-5000)')
            sdi1_di_nrd_nis = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type','SDI(1) 24Vdc DIO (0-5000)')
            sdi1_di_rd_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type','SDI(1) 24Vdc Line Mon DIO (0-5000)')
            sdi1_di_line_nrd_nis = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type','SDI(1) 24Vdc Line Mon DIO (0-5000)')
            sdi1_di_line_rd_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
            #DO
            cont = IOComp.Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Output Type','SDO(1) 24Vdc 500mA DIO (0-5000)')
            sdo1_do_nrd_nis = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
            row_index = IOComp.getRowIndex(cont, 'Digital Output Type','SDO(1) 24Vdc 500mA DIO (0-5000)')
            sdo1_do_rd_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
            try:
            	percent_spare_space = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("Percent_Installed_Spare_IOs").Value
            except:
            	percent_spare_space = 0
            if not percent_spare_space:
            	percent_spare_space = 0
            Trace.Write("1:"+str(sdi1_di_nrd_nis))
            Trace.Write("2:"+str(sdi1_di_line_nrd_nis))
            Trace.Write("3:"+str(sdo1_do_nrd_nis))
            Trace.Write("4:"+str(sdi1_di_rd_nis))
            Trace.Write("5:"+str(sdi1_di_line_rd_nis))
            Trace.Write("6:"+str(sdo1_do_rd_nis))
            SUMMARCHDIO =((D.Ceiling(((sdi1_di_nrd_nis)+(sdi1_di_line_nrd_nis)+(sdo1_do_nrd_nis))*float(1.00 +(getNum(percent_spare_space)/100.00))))+(D.Ceiling(((sdi1_di_rd_nis)+(sdi1_di_line_rd_nis)+(sdo1_do_rd_nis))*float(1.00 +(getNum(percent_spare_space)/100.00)))))
    elif Product.Name=="SM Remote Group":
        IOComp = IOComponents(Product)
        Marshalling_Option=Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        iota=Product.Attr("SM_Universal_IOTA_Type").GetValue()
        if Marshalling_Option == 'Hardware Marshalling with Other' and iota == 'PUIO':
            #DI
            cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type','SDI(1) 24Vdc DIO  (0-5000)')
            sdi1_di_nrd_nis = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
            row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type','SDI(1) 24Vdc DIO  (0-5000)')
            sdi1_di_rd_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
            row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type','SDI(1) 24Vdc Line Mon DIO (0-5000)')
            sdi1_di_line_nrd_nis = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
            row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type','SDI(1) 24Vdc Line Mon DIO (0-5000)')
            sdi1_di_line_rd_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
            #DO
            cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital_Output_Type','SDO(1) 24Vdc 500mA DIO  (0-5000)')
            sdo1_do_nrd_nis = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
            row_index = IOComp.getRowIndex(cont, 'Digital_Output_Type','SDO(1) 24Vdc 500mA DIO  (0-5000)')
            sdo1_do_rd_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
            try:
            	percent_spare_space = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_Percent_Installed_Spare_IO").Value
            except:
            	percent_spare_space = 0
            if not percent_spare_space:
            	percent_spare_space = 0
            Trace.Write("1:"+str(sdi1_di_nrd_nis))
            Trace.Write("2:"+str(sdi1_di_line_nrd_nis))
            Trace.Write("3:"+str(sdo1_do_nrd_nis))
            Trace.Write("4:"+str(sdi1_di_rd_nis))
            Trace.Write("5:"+str(sdi1_di_line_rd_nis))
            Trace.Write("6:"+str(sdo1_do_rd_nis))
            SUMMARCHDIO =((D.Ceiling(((sdi1_di_nrd_nis)+(sdi1_di_line_nrd_nis)+(sdo1_do_nrd_nis))*float(1.00 +(getNum(percent_spare_space)/100.00))))+(D.Ceiling(((sdi1_di_rd_nis)+(sdi1_di_line_rd_nis)+(sdo1_do_rd_nis))*float(1.00 +(getNum(percent_spare_space)/100.00)))))
    return SUMMARCHDIO
#Trace.Write(getSUMMARCHDIOValue(Product))