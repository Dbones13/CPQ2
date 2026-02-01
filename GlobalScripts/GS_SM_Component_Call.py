#CXCPQ-31183
import math as m
'''import GS_SMIOComponents
IOComp = GS_SMIOComponents.IOComponents(Product)
SUMUIONPF, SUMUIORPF = IOComp.getUniversalIOCountRedNonRed()'''
def get_column_value(row, col):
    try:
        val = row.GetColumnByName(col).Value
    except Exception,e:
        val = 0
    return val
def getInt(var):
    if var:
        return int(var)
    return 0.0
#31146
def get_int(var):
    if var:
        return int(var)
    return 0

def getFloat(var):
    if var:
        return float(var)
    return 0

def get_float(var):
    if var:
        return float(var)
    return 0
#Trace.Write(get_comp_c(Product))

#CXCPQ 30841
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
def get_SUMUIONIS(Product):
    if Product.Name == "SM Control Group":
        IOComp = IOComponents(Product)
        Trace.Write("SM Control Group")
        SUMUIONIS = 0.0
        iota=Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Universal_IOTA').DisplayValue
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont')  #DI
        row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
        uio_di_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc Line Mon UIO (0-5000)')
        line_mon_uio_di_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        #AI
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)mA type Current UIO (0-5000)')
        current_uio_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)FIRE 2 wire current UIO (0-5000)')
        fire2_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)FIRE 3-4 wire current UIO (0-5000)')
        fire3and4_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1)FIRE 3-4 wire current Sink UIO (0-5000)')
        fire3and4_sink_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type', 'SAI(1) GAS current UIO (0-5000)')
        gas_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        Trace.Write(current_uio_NRD_IS)
        Trace.Write(fire2_NRD_IS)
        Trace.Write(fire3and4_NRD_IS)
        Trace.Write(fire3and4_sink_NRD_IS)
        Trace.Write(gas_NRD_IS)
        # AO
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog Output Type', 'SAO(1)mA Type UIO (0-5000)')
        type_uio_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        #DO
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA UIO (0-5000)')
        dao_24vdc_500mA_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(7) 24Vdc Line Mon UIO (0-5000)')
        line_mon_uio_do_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non Red (IS)")
        try:
            percent_spare_space = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("Percent_Installed_Spare_IOs").Value
        except:
            percent_spare_space = 0
        if not percent_spare_space:
            percent_spare_space = 0
        Trace.Write("Per spare = "+str(percent_spare_space))
        if iota=="PUIO":
        	cal=D.Ceiling((current_uio_NRD_IS) + (fire2_NRD_IS) + (fire3and4_NRD_IS) + (fire3and4_sink_NRD_IS) + (gas_NRD_IS) + (type_uio_NRD_IS) + (dao_24vdc_500mA_NRD_IS)+ (uio_di_NRD_IS) + (line_mon_uio_di_NRD_IS)  +(16*( D.Ceiling(line_mon_uio_do_NRD_IS/7))))
        	Trace.Write(cal)
        	Shivani=float(1.00 + float(percent_spare_space)/100.00)
        	Trace.Write(Shivani)
        	SUMUIONIS = float(cal) * Shivani
        return round(SUMUIONIS)
    elif Product.Name == "SM Remote Group":
        IOComp = IOComponents(Product)
        Trace.Write("SM Remote Group")
        SUMUIONIS = 0.0
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont')  #DI
        row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc UIO  (0-5000)')
        uio_di_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc Line Mon UIO  (0-5000)')
        line_mon_uio_di_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        Trace.Write(uio_di_NRD_IS)
        Trace.Write(line_mon_uio_di_NRD_IS)
        #AI
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)mA type Current  UIO  (0-5000)')
        current_uio_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)FIRE 2 wire current  UIO   (0-5000)')
        fire2_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)FIRE 3-4 wire current  UIO  (0-5000)')
        fire3and4_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)FIRE 3-4 wire current  Sink UIO  (0-5000)')
        fire3and4_sink_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1) GAS current  UIO  (0-5000)')
        gas_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        Trace.Write(current_uio_NRD_IS)
        Trace.Write(fire2_NRD_IS)
        Trace.Write(fire3and4_NRD_IS)
        Trace.Write(fire3and4_sink_NRD_IS)
        Trace.Write(gas_NRD_IS)
        # AO
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog_Output_Type', 'SAO(1)mA Type UIO   (0-5000)')
        type_uio_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        Trace.Write(type_uio_NRD_IS)
        #DO
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital_Output_Type', 'SDO(1) 24Vdc 500mA UIO  (0-5000)')
        dao_24vdc_500mA_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        row_index = IOComp.getRowIndex(cont, 'Digital_Output_Type', 'SDO(7) 24Vdc Line Mon UIO  (0-5000)')
        line_mon_uio_do_NRD_IS = IOComp.getColumnValue(cont, row_index, "Non_Red_IS")
        Trace.Write(dao_24vdc_500mA_NRD_IS)
        Trace.Write(line_mon_uio_do_NRD_IS)
        try:
            percent_spare_space = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_Percent_Installed_Spare_IO").Value
        except:
            percent_spare_space = 0
        if not percent_spare_space:
            percent_spare_space = 0
        Trace.Write("Per spare = "+str(percent_spare_space))
        if iota=="PUIO":
        	cal=D.Ceiling((current_uio_NRD_IS) + (fire2_NRD_IS) + (fire3and4_NRD_IS) + (fire3and4_sink_NRD_IS) + (gas_NRD_IS) + (type_uio_NRD_IS) + (dao_24vdc_500mA_NRD_IS)+ (uio_di_NRD_IS) + (line_mon_uio_di_NRD_IS)  +(16*( D.Ceiling(line_mon_uio_do_NRD_IS/7))))
        	Trace.Write(cal)
        	Shivani=float(1.00 + float(percent_spare_space)/100.00)
        	Trace.Write(Shivani)
        	SUMUIONIS = float(cal) * Shivani
        return round(SUMUIONIS, 2)
    else:
        Trace.Write("Product is neither SM Control Group nor SM Remote Group")
        return 0.0

    
    
    
    

    
def getNum(n):
    return 0 if n=="" or n==0 else int(n)
def GS_SM_SUMUIOR_Calc(Product,SUMUIORPF):
    if Product.Name=="SM Control Group":
        IOComp = IOComponents(Product)
        Trace.Write("SM Control Group")
        SUMUIOR_cg = 0.0
        iota=Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Universal_IOTA').DisplayValue
        try:
            percent_spare_space = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("Percent_Installed_Spare_IOs").Value
        except:
            percent_spare_space = 0
        if not percent_spare_space:
            percent_spare_space = 0
        Trace.Write("Per spare = "+str(percent_spare_space))
        # AI
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type','SAI(1)mA type Current UIO (0-5000)')
        SUMUIOR_cg+= IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        Trace.Write(SUMUIOR_cg)
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type','SAI(1)FIRE 2 wire current UIO (0-5000)')
        SUMUIOR_cg+=IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        Trace.Write(SUMUIOR_cg)
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type','SAI(1)FIRE 3-4 wire current UIO (0-5000)')
        SUMUIOR_cg+= IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        Trace.Write(SUMUIOR_cg)
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type','SAI(1)FIRE 3-4 wire current Sink UIO (0-5000)')
        SUMUIOR_cg+=IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        Trace.Write(SUMUIOR_cg)
        row_index = IOComp.getRowIndex(cont, 'Analog Input Type','SAI(1) GAS current UIO (0-5000)')
        SUMUIOR_cg+=IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        Trace.Write(SUMUIOR_cg)
        # AO
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog Output Type', 'SAO(1)mA Type UIO (0-5000)')
        SUMUIOR_cg+=IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        Trace.Write(SUMUIOR_cg)
        #DO
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA UIO (0-5000)')
        SUMUIOR_cg+=IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        Trace.Write(SUMUIOR_cg)
        row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(7) 24Vdc Line Mon UIO (0-5000)')
        SUMUIOR_cg+=(16*(D.Ceiling(IOComp.getColumnValue(cont, row_index, "Red (NIS)")/7)))
        Trace.Write(SUMUIOR_cg)
        row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(16) SIL 2/3 250Vac/Vdc UIO (0-5000)')
        SUMUIOR_cg+=IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        Trace.Write(SUMUIOR_cg)
        row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(16) SIL 2/3 250Vac/Vdc COM UIO (0-5000)')
        SUMUIOR_cg+= IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        Trace.Write(SUMUIOR_cg)
        row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA UIO (0-5000)')
        SUMUIOR_cg+= IOComp.getColumnValue(cont, row_index, "Red (RLY)")
        Trace.Write(SUMUIOR_cg)
        #DI
        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
        SUMUIOR_cg+= IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        Trace.Write(SUMUIOR_cg)
        row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc Line Mon UIO (0-5000)')
        SUMUIOR_cg+= IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        Trace.Write(SUMUIOR_cg)
        row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc with 5K Resistor UIO (0-5000)')
        SUMUIOR_cg+= IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        Trace.Write(SUMUIOR_cg)
        row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
        SUMUIOR_cg+= IOComp.getColumnValue(cont, row_index, "Red (RLY)")
        Trace.Write(SUMUIOR_cg)
        try:
            dinmr=Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName('DI/DO_SIL2/3_Relay_Adapter_UMC').DisplayValue
            donmr=Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName('DI_NAMUR_proximity_Switches_Adapter_UMC').DisplayValue
        except:
            dinmr=0
            donmr=0
        if dinmr=="Yes" or donmr=="Yes":
            #DONMR
            cont = IOComp.Product.GetContainerByName('SM_CG_DO_RLY_NMR_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA UIO (0-5000)')
            SUMUIOR_cg+=IOComp.getColumnValue(cont, row_index, "Red_SIL2_RLY")
            Trace.Write(SUMUIOR_cg)
            row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA UIO (0-5000)')
            SUMUIOR_cg+=IOComp.getColumnValue(cont, row_index, "Red_SIL3_RLY")
            Trace.Write(SUMUIOR_cg)
            #DINMR
            cont = IOComp.Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
            SUMUIOR_cg+=IOComp.getColumnValue(cont, row_index, "Red_SIL3_RLY")
            Trace.Write(SUMUIOR_cg)
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
            SUMUIOR_cg+=IOComp.getColumnValue(cont, row_index, "Red_NMR")
            Trace.Write(SUMUIOR_cg)
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
            SUMUIOR_cg+=IOComp.getColumnValue(cont, row_index, "Red_NMR_Safety")
            Trace.Write(SUMUIOR_cg)
        if iota=="PUIO":
        	cal = SUMUIOR_cg+(16*(D.Ceiling(SUMUIORPF/16.0)))
        	SUMUIOR_cg =D.Ceiling(cal * float(1.00 +(getNum(percent_spare_space)/100.00)))
        return (round(SUMUIOR_cg))
    elif Product.Name == "SM Remote Group":
        IOComp = IOComponents(Product)
        Trace.Write("SM Remote Group")
        SUMUIOR_rg = 0.0
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        # AI
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type', 'SAI(1)mA type Current  UIO  (0-5000)')
        SUMUIOR_rg+= IOComp.getColumnValue(cont, row_index, "Red_NIS")
        Trace.Write(SUMUIOR_rg)
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type','SAI(1)FIRE 2 wire current  UIO   (0-5000)')
        SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_NIS")
        Trace.Write(SUMUIOR_rg)
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type','SAI(1)FIRE 3-4 wire current  UIO  (0-5000)')
        SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_NIS")
        Trace.Write(SUMUIOR_rg)
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type','SAI(1)FIRE 3-4 wire current  Sink UIO  (0-5000)')
        SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_NIS")
        Trace.Write(SUMUIOR_rg)
        row_index = IOComp.getRowIndex(cont, 'Analog_Input_Type','SAI(1) GAS current  UIO  (0-5000)')
        SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_NIS")
        Trace.Write(SUMUIOR_rg)
        # AO
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Analog_Output_Type', 'SAO(1)mA Type UIO   (0-5000)')
        SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_NIS")
        Trace.Write(SUMUIOR_rg)
        #DI
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc UIO  (0-5000)')
        SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_NIS")
        Trace.Write(SUMUIOR_rg)
        row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc Line Mon UIO  (0-5000)')
        SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_NIS")
        Trace.Write(SUMUIOR_rg)
        row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc with 5K Resistor UIO  (0-5000)')
        SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_NIS")
        Trace.Write(SUMUIOR_rg)
        row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc UIO  (0-5000)')
        SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_RLY")
        Trace.Write(SUMUIOR_rg)
        #DO
        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital_Output_Type', 'SDO(1) 24Vdc 500mA UIO  (0-5000)')
        SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_NIS")
        Trace.Write(SUMUIOR_rg)
        row_index = IOComp.getRowIndex(cont, 'Digital_Output_Type', 'SDO(7) 24Vdc Line Mon UIO  (0-5000)')
        SUMUIOR_rg+=(16*(D.Ceiling(IOComp.getColumnValue(cont, row_index, "Red_NIS")/7)))
        Trace.Write(SUMUIOR_rg)
        row_index = IOComp.getRowIndex(cont, 'Digital_Output_Type', 'SDO(16) SIL 2/3 250Vac/Vdc UIO   (0-5000)')
        SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_NIS")
        Trace.Write(SUMUIOR_rg)
        row_index = IOComp.getRowIndex(cont, 'Digital_Output_Type', 'SDO(16) SIL 2/3 250Vac/Vdc COM UIO  (0-5000)')
        SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_NIS")
        Trace.Write(SUMUIOR_rg)
        row_index = IOComp.getRowIndex(cont, 'Digital_Output_Type', 'SDO(1) 24Vdc 500mA UIO  (0-5000)')
        SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_RLY")
        Trace.Write(SUMUIOR_rg)
        try:
            dinmr1=Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName('SM_DI_DORelay_Adapter_UMC').DisplayValue
            donmr1=Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName('SM_DI_NAMUR_Switches_Adapter_UMC').DisplayValue
        except:
            dinmr1=0
            donmr1=0
        if dinmr1=="Yes" and donmr1=="Yes":
            #DONMR
            cont = IOComp.Product.GetContainerByName('SM_RG_DO_RLY_NMR_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Output Type','SDO(1) 24Vdc 500mA UIO (0-5000)')
            SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_SIL2_RLY")
            Trace.Write(SUMUIOR_rg)
            row_index = IOComp.getRowIndex(cont, 'Digital Output Type','SDO(1) 24Vdc 500mA UIO (0-5000)')
            SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_SIL3_RLY")
            Trace.Write(SUMUIOR_rg)
            #DINMR
            cont = IOComp.Product.GetContainerByName('SM_RG_DI_RLY_NMR_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type','SDI(1) 24Vdc UIO (0-5000)')
            SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_SIL3_RLY")
            Trace.Write(SUMUIOR_rg)
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
            SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_NMR")
            Trace.Write(SUMUIOR_rg)
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
            SUMUIOR_rg+=IOComp.getColumnValue(cont, row_index, "Red_NMR_Safety")
            Trace.Write(SUMUIOR_rg)
        try:
            percent_spare_space = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_Percent_Installed_Spare_IO").Value
        except:
            percent_spare_space = 0
        if not percent_spare_space:
            percent_spare_space = 0
        Trace.Write("Per spare = "+str(percent_spare_space))
        if iota=="PUIO":
        	cal = SUMUIOR_rg+(16*(D.Ceiling(SUMUIORPF/16.0)))
        	SUMUIOR_rg =D.Ceiling(cal * float(1.00 +(getNum(percent_spare_space)/100.00)))
        return (round(SUMUIOR_rg))
    else:
        Trace.Write("Product is neither SM Control Group nor SM Remote Group")
        return 0.0
#SUMUIOR=IOComponentsNIS(Product)
'''x=GS_SM_SUMUIOR_Calc(Product,SUMUIORPF)
Trace.Write("sumu = "+str(x))
y=get_SUMUIONIS(Product)
Trace.Write("sumuionis:"+str(y))'''