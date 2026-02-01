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
def GS_SM_SUMUIORPF_Calc(Prod):
    if Prod.Name == "SM Control Group":
        IOComp = IOComponents(Prod)
        Trace.Write("SM Control Group")
        sumuiorpf_cg = 0.0
        iota=Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Universal_IOTA').DisplayValue
        if iota=="PUIO":
            #DI
            cont = IOComp.Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1)  24Vdc SIL2 P+F UIO (0-5000)')
            sil2_red = IOComp.getColumnValue(cont, row_index, "Red (IS)")
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1)  24Vdc SIL3 P+F UIO (0-5000)')
            sil3_red = IOComp.getColumnValue(cont, row_index, "Red (IS)")
            # AI
            cont = IOComp.Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont')
            row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)mA Type Current P+F UIO (0-5000)')
            currentmA_red = IOComp.getColumnValue(cont, row_index, "Red (IS)")
            # AO
            cont = IOComp.Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont')
            row_index = IOComp.getRowIndex(cont, 'Analog Output Type', 'SAO(1)mA Type P+F UIO (0-5000)')
            currentmAPF_red = IOComp.getColumnValue(cont, row_index, "Red (IS)")
            #DO
            cont = IOComp.Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc SIL3 P+F UIO (0-5000)')
            sil3pf_red = IOComp.getColumnValue(cont, row_index, "Red (IS)")
            try:
                percent_spare_space = Prod.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("Percent_Installed_Spare_IOs").Value
            except:
                percent_spare_space = 0
            if not percent_spare_space:
                percent_spare_space = 0
            Trace.Write("Per spare = "+str(percent_spare_space))
            sumuiorpf_cg = D.Ceiling((sil2_red + sil3_red + currentmA_red + currentmAPF_red + sil3pf_red)*(1 + (float(percent_spare_space)/float(100))))
            return round(sumuiorpf_cg, 2)
    elif Prod.Name == "SM Remote Group":
        IOComp = IOComponents(Prod)
        Trace.Write("SM Remote Group")
        sumuiorpf_rg = 0.0
        iota=Product.Attr("SM_Universal_IOTA_Type").GetValue()
        #DI
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1)  24Vdc SIL2 P+F UIO  (0-5000)')
        sil2_red = IOComp.getColumnValue(cont, row_index, "Red_IS")
        #Trace.Write(sil2_red)
        row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1)  24Vdc SIL3 P+F UIO  (0-5000)')
        sil3_red = IOComp.getColumnValue(cont, row_index, "Red_IS")
        #Trace.Write(sil3_red)
        # AI
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1) mA Type Current P+F UIO  (0-5000)')
        currentmA_red = IOComp.getColumnValue(cont, row_index, "Red_IS")
        #Trace.Write(currentmA_red)
        # AO
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog_Output_Type', 'SAO(1)mA Type P+F UIO  (0-5000)')
        currentmAPF_red = IOComp.getColumnValue(cont, row_index, "Red_IS")
        #Trace.Write(currentmAPF_red)
        #DO
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital_Output_Type', 'SDO(1) 24Vdc SIL3 P+F UIO  (0-5000)')
        sil3pf_red = IOComp.getColumnValue(cont, row_index, "Red_IS")
        #Trace.Write(sil3pf_red)
        try:
            percent_spare_space = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_Percent_Installed_Spare_IO").Value
        except:
            percent_spare_space = 0
        if not percent_spare_space:
            percent_spare_space = 0
        Trace.Write("Per spare = "+str(percent_spare_space))
        if iota=="PUIO":
        	sumuiorpf_rg = D.Ceiling((sil2_red + sil3_red + currentmA_red + currentmAPF_red + sil3pf_red)*(1 + (float(percent_spare_space)/float(100))))
        return round(sumuiorpf_rg, 2)
    else:
        Trace.Write("Product is neither SM Control Group nor SM Remote Group")
        return 0.0
#x=GS_SM_SUMUIORPF_Calc(Product)
#Trace.Write("sumuiorpf = "+str(x))