#33029
def get_DIDO_SL_Namur_DI(Product,parts_dict):
    if Product.Name=="SM Control Group":
        Red_SIL3RLY_SDi_24Vdc_500mA_UIO=0
        NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO=0
        Red_SIL3RLY_SDi_24Vdc_500mA_DIO=0
        NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO=0
        
        Marshalling_Option = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        if Marshalling_Option == "Universal Marshalling":
            if Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("DI_NAMUR_proximity_Switches_Adapter_UMC").DisplayValue=='Yes':
                do_cont_rly_nmr = Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont')
                for row in do_cont_rly_nmr.Rows:
                    if row.GetColumnByName("Digital Input Type").Value == "SDI(1) 24Vdc UIO (0-5000)":
                        Red_SIL3RLY_SDi_24Vdc_500mA_UIO = row.GetColumnByName("Red_NMR").Value
                        NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO = row.GetColumnByName("Non_Red_NMR").Value
                    if row.GetColumnByName("Digital Input Type").Value == "SDI(1) 24Vdc DIO (0-5000)":
                        Red_SIL3RLY_SDi_24Vdc_500mA_DIO = row.GetColumnByName("Red_NMR").Value
                        NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO = row.GetColumnByName("Non_Red_NMR").Value
            

        if Red_SIL3RLY_SDi_24Vdc_500mA_UIO=="":
	        Red_SIL3RLY_SDi_24Vdc_500mA_UIO=0
        if NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO=="":
	        NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO=0
        if Red_SIL3RLY_SDi_24Vdc_500mA_DIO=="":
	        Red_SIL3RLY_SDi_24Vdc_500mA_DIO=0
        if NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO=="":
	        NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO=0
    
        sumup= int(Red_SIL3RLY_SDi_24Vdc_500mA_UIO) + int(NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO) + int(Red_SIL3RLY_SDi_24Vdc_500mA_DIO) + int(NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO)


        Trace.Write(Red_SIL3RLY_SDi_24Vdc_500mA_UIO)
        Trace.Write(NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO)
        Trace.Write(Red_SIL3RLY_SDi_24Vdc_500mA_DIO)
        Trace.Write(NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO)
        Trace.Write(sumup)
        parts_dict["FC-UDIN01"] = {'Quantity' : sumup  , 'Description': 'SCA DIGITAL INPUT NAMUR'}
        
    elif Product.Name=="SM Remote Group":
        Red_SIL3RLY_SDi_24Vdc_500mA_UIO=0
        NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO=0
        Red_SIL3RLY_SDi_24Vdc_500mA_DIO=0
        NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO=0

        Marshalling_Option = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        if Marshalling_Option == "Universal Marshalling":
            if Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_DI_NAMUR_Switches_Adapter_UMC").DisplayValue=='Yes':
                do_cont_rly_nmr = Product.GetContainerByName('SM_RG_DI_RLY_NMR_Cont')
                for row in do_cont_rly_nmr.Rows:
                    if row.GetColumnByName("Digital Input Type").Value == "SDI(1) 24Vdc UIO (0-5000)":
                        Red_SIL3RLY_SDi_24Vdc_500mA_UIO = row.GetColumnByName("Red_NMR").Value
                        NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO = row.GetColumnByName("Non_Red_NMR").Value
                    if row.GetColumnByName("Digital Input Type").Value == "SDI(1) 24Vdc DIO (0-5000)":
                        Red_SIL3RLY_SDi_24Vdc_500mA_DIO = row.GetColumnByName("Red_NMR").Value
                        NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO = row.GetColumnByName("Non_Red_NMR").Value
            
        if Red_SIL3RLY_SDi_24Vdc_500mA_UIO=="":
	        Red_SIL3RLY_SDi_24Vdc_500mA_UIO=0
        if NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO=="":
	        NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO=0
        if Red_SIL3RLY_SDi_24Vdc_500mA_DIO=="":
	        Red_SIL3RLY_SDi_24Vdc_500mA_DIO=0
        if NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO=="":
	        NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO=0
    
        sumup= int(Red_SIL3RLY_SDi_24Vdc_500mA_UIO) + int(NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO) + int(Red_SIL3RLY_SDi_24Vdc_500mA_DIO) + int(NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO)


        Trace.Write(Red_SIL3RLY_SDi_24Vdc_500mA_UIO)
        Trace.Write(NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO)
        Trace.Write(Red_SIL3RLY_SDi_24Vdc_500mA_DIO)
        Trace.Write(NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO)
        Trace.Write(sumup)
        parts_dict["FC-UDIN01"] = {'Quantity' : sumup  , 'Description': 'SCA DIGITAL INPUT NAMUR'}
    return parts_dict

#33030
def get_UIO_SL_sftyNamur_DI(Product, parts_dict):
    if Product.Name=="SM Control Group":
        Red_SIL3RLY_SDi_24Vdc_500mA_UIO=0
        NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO=0
        Red_SIL3RLY_SDi_24Vdc_500mA_DIO=0
        NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO=0

        Marshalling_Option = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        if Marshalling_Option == "Universal Marshalling":
            if Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("DI_NAMUR_proximity_Switches_Adapter_UMC").DisplayValue=='Yes':
                do_cont_rly_nmr = Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont')
                for row in do_cont_rly_nmr.Rows:
                    if row.GetColumnByName("Digital Input Type").Value == "SDI(1) 24Vdc UIO (0-5000)":
                        Red_SIL3RLY_SDi_24Vdc_500mA_UIO = row.GetColumnByName("Red_NMR_Safety").Value
                        NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO = row.GetColumnByName("Non_Red_NMR_Safety").Value
                    if row.GetColumnByName("Digital Input Type").Value == "SDI(1) 24Vdc DIO (0-5000)":
                        Red_SIL3RLY_SDi_24Vdc_500mA_DIO = row.GetColumnByName("Red_NMR_Safety").Value
                        NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO = row.GetColumnByName("Non_Red_NMR_Safety").Value      
                    

        if Red_SIL3RLY_SDi_24Vdc_500mA_UIO=="":
            Red_SIL3RLY_SDi_24Vdc_500mA_UIO=0
        if NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO=="":
            NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO=0
        if Red_SIL3RLY_SDi_24Vdc_500mA_DIO=="":
            Red_SIL3RLY_SDi_24Vdc_500mA_DIO=0
        if NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO=="":
            NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO=0
            
        sumup= int(Red_SIL3RLY_SDi_24Vdc_500mA_UIO) + int(NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO) + int(Red_SIL3RLY_SDi_24Vdc_500mA_DIO) + int(NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO)


        Trace.Write(Red_SIL3RLY_SDi_24Vdc_500mA_UIO)
        Trace.Write(NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO)
        Trace.Write(Red_SIL3RLY_SDi_24Vdc_500mA_DIO)
        Trace.Write(NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO)
        Trace.Write(sumup)
        parts_dict["FC-UDNS01"] = {'Quantity' : int(sumup),'Description': 'SCA DIGITAL INPUT SAFETY NAMUR'}
    #Remote Group===============================
    elif Product.Name=="SM Remote Group":
        Red_SIL3RLY_SDi_24Vdc_500mA_UIO=0
        NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO=0
        Red_SIL3RLY_SDi_24Vdc_500mA_DIO=0
        NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO=0

        Marshalling_Option = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        if Marshalling_Option == "Universal Marshalling":
            if Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_DI_NAMUR_Switches_Adapter_UMC").DisplayValue=='Yes':
                do_cont_rly_nmr = Product.GetContainerByName('SM_RG_DI_RLY_NMR_Cont')
                for row in do_cont_rly_nmr.Rows:
                    if row.GetColumnByName("Digital Input Type").Value == "SDI(1) 24Vdc UIO (0-5000)":
                        Red_SIL3RLY_SDi_24Vdc_500mA_UIO = row.GetColumnByName("Red_NMR_Safety").Value
                        NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO = row.GetColumnByName("Non_Red_NMR_Safety").Value
                    if row.GetColumnByName("Digital Input Type").Value == "SDI(1) 24Vdc DIO (0-5000)":
                        Red_SIL3RLY_SDi_24Vdc_500mA_DIO = row.GetColumnByName("Red_NMR_Safety").Value
                        NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO = row.GetColumnByName("Non_Red_NMR_Safety").Value
                    
        if Red_SIL3RLY_SDi_24Vdc_500mA_UIO=="":
            Red_SIL3RLY_SDi_24Vdc_500mA_UIO=0
        if NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO=="":
            NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO=0
        if Red_SIL3RLY_SDi_24Vdc_500mA_DIO=="":
            Red_SIL3RLY_SDi_24Vdc_500mA_DIO=0
        if NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO=="":
            NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO=0
            
        sumup= int(Red_SIL3RLY_SDi_24Vdc_500mA_UIO) + int(NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO) + int(Red_SIL3RLY_SDi_24Vdc_500mA_DIO) + int(NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO)


        Trace.Write(Red_SIL3RLY_SDi_24Vdc_500mA_UIO)
        Trace.Write(NonRed_SIL3RLY_SDi_24Vdc_500mA_UIO)
        Trace.Write(Red_SIL3RLY_SDi_24Vdc_500mA_DIO)
        Trace.Write(NonRed_SIL3RLY_SDi_24Vdc_500mA_DIO)
        Trace.Write(sumup)
        parts_dict["FC-UDNS01"] = {'Quantity' : int(sumup),'Description': 'SCA DIGITAL INPUT SAFETY NAMUR'}
    return parts_dict

#33031
def get_UIO_SL_sftyNamur_DO(Product, parts_dict):
    if Product.Name=="SM Control Group":
        Red_SIL3RLY_SDO_24Vdc_500mA_UIO=0
        NonRed_SIL3RLY_SDO_24Vdc_500mA_UIO=0
        Red_SIL3RLY_SDO_24Vdc_500mA_DIO=0
        NonRed_SIL3RLY_SDO_24Vdc_500mA_DIO=0

        Marshalling_Option = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        if Marshalling_Option == "Universal Marshalling":
            if 1:
                if Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("DI/DO_SIL2/3_Relay_Adapter_UMC").DisplayValue=='Yes':
                    do_cont_rly_nmr = Product.GetContainerByName('SM_CG_DO_RLY_NMR_Cont')
                    for row in do_cont_rly_nmr.Rows:
                        if row.GetColumnByName("Digital Output Type").Value == "SDO(1) 24Vdc 500mA UIO (0-5000)":
                            Red_SIL3RLY_SDO_24Vdc_500mA_UIO = row.GetColumnByName("Red_SIL3_RLY").Value
                            NonRed_SIL3RLY_SDO_24Vdc_500mA_UIO = row.GetColumnByName("Non_Red_SIL3_RLY").Value
                        if row.GetColumnByName("Digital Output Type").Value == "SDO(1) 24Vdc 500mA DIO (0-5000)":
                            Red_SIL3RLY_SDO_24Vdc_500mA_DIO = row.GetColumnByName("Red_SIL3_RLY").Value
                            NonRed_SIL3RLY_SDO_24Vdc_500mA_DIO = row.GetColumnByName("Non_Red_SIL3_RLY").Value

        if Red_SIL3RLY_SDO_24Vdc_500mA_UIO=="":
            Red_SIL3RLY_SDO_24Vdc_500mA_UIO=0
        if NonRed_SIL3RLY_SDO_24Vdc_500mA_UIO=="":
            NonRed_SIL3RLY_SDO_24Vdc_500mA_UIO=0
        if Red_SIL3RLY_SDO_24Vdc_500mA_DIO=="":
            Red_SIL3RLY_SDO_24Vdc_500mA_DIO=0
        if NonRed_SIL3RLY_SDO_24Vdc_500mA_DIO=="":
            NonRed_SIL3RLY_SDO_24Vdc_500mA_DIO=0
            
        sumup= int(Red_SIL3RLY_SDO_24Vdc_500mA_UIO) + int(NonRed_SIL3RLY_SDO_24Vdc_500mA_UIO) + int(Red_SIL3RLY_SDO_24Vdc_500mA_DIO) + int(NonRed_SIL3RLY_SDO_24Vdc_500mA_DIO)


        Trace.Write(Red_SIL3RLY_SDO_24Vdc_500mA_UIO)
        Trace.Write(NonRed_SIL3RLY_SDO_24Vdc_500mA_UIO)
        Trace.Write(Red_SIL3RLY_SDO_24Vdc_500mA_DIO)
        Trace.Write(NonRed_SIL3RLY_SDO_24Vdc_500mA_DIO)
        Trace.Write(sumup)
        parts_dict["FC-UDOR01"] = {'Quantity' : int(sumup),'Description': 'SCA DIGITAL OUTPUT RELAY'}
    


    #Remote Group============================================
    elif Product.Name=="SM Remote Group":
        Red_SIL3RLY_SDO_24Vdc_500mA_UIO=0
        NonRed_SIL3RLY_SDO_24Vdc_500mA_UIO=0
        Red_SIL3RLY_SDO_24Vdc_500mA_DIO=0
        NonRed_SIL3RLY_SDO_24Vdc_500mA_DIO=0

        Marshalling_Option = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        if Marshalling_Option == "Universal Marshalling":
            if 1:
                if Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_DI_DORelay_Adapter_UMC").DisplayValue=='Yes':
                    do_cont_rly_nmr = Product.GetContainerByName('SM_RG_DO_RLY_NMR_Cont')
                    for row in do_cont_rly_nmr.Rows:
                        if row.GetColumnByName("Digital Output Type").Value == "SDO(1) 24Vdc 500mA UIO (0-5000)":
                            Red_SIL3RLY_SDO_24Vdc_500mA_UIO = row.GetColumnByName("Red_SIL3_RLY").Value
                            NonRed_SIL3RLY_SDO_24Vdc_500mA_UIO = row.GetColumnByName("Non_Red_SIL3_RLY").Value
                        if row.GetColumnByName("Digital Output Type").Value == "SDO(1) 24Vdc 500mA DIO (0-5000)":
                            Red_SIL3RLY_SDO_24Vdc_500mA_DIO = row.GetColumnByName("Red_SIL3_RLY").Value
                            NonRed_SIL3RLY_SDO_24Vdc_500mA_DIO = row.GetColumnByName("Non_Red_SIL3_RLY").Value

        if Red_SIL3RLY_SDO_24Vdc_500mA_UIO=="":
            Red_SIL3RLY_SDO_24Vdc_500mA_UIO=0
        if NonRed_SIL3RLY_SDO_24Vdc_500mA_UIO=="":
            NonRed_SIL3RLY_SDO_24Vdc_500mA_UIO=0
        if Red_SIL3RLY_SDO_24Vdc_500mA_DIO=="":
            Red_SIL3RLY_SDO_24Vdc_500mA_DIO=0
        if NonRed_SIL3RLY_SDO_24Vdc_500mA_DIO=="":
            NonRed_SIL3RLY_SDO_24Vdc_500mA_DIO=0
            
        sumup= int(Red_SIL3RLY_SDO_24Vdc_500mA_UIO) + int(NonRed_SIL3RLY_SDO_24Vdc_500mA_UIO) + int(Red_SIL3RLY_SDO_24Vdc_500mA_DIO) + int(NonRed_SIL3RLY_SDO_24Vdc_500mA_DIO)


        Trace.Write(Red_SIL3RLY_SDO_24Vdc_500mA_UIO)
        Trace.Write(NonRed_SIL3RLY_SDO_24Vdc_500mA_UIO)
        Trace.Write(Red_SIL3RLY_SDO_24Vdc_500mA_DIO)
        Trace.Write(NonRed_SIL3RLY_SDO_24Vdc_500mA_DIO)
        Trace.Write(sumup)
        parts_dict["FC-UDOR01"] = {'Quantity' : int(sumup),'Description': 'SCA DIGITAL OUTPUT RELAY'}
    return parts_dict

#33032
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

def get_FC_UDOF01(Product,parts_dict):
    if Product.Name=="SM Control Group":
        IOComp = IOComponents(Product)
        sil2 = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName('DI/DO_SIL2/3_Relay_Adapter_UMC').Value
        Marshalling_Option = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        Red_SIL2_RLY_uio=Non_Red_SIL2_RLY_uio=Red_SIL2_RLY_dio=Non_Red_SIL2_RLY_dio=total=0
        if sil2 == "Yes" and Marshalling_Option == "Universal Marshalling":
        
            cont = IOComp.Product.GetContainerByName('SM_CG_DO_RLY_NMR_Cont')
            row_index_red_uio = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA UIO (0-5000)')
            Red_SIL2_RLY_uio = IOComp.getColumnValue(cont, row_index_red_uio, "Red_SIL2_RLY")
            Trace.Write("Red_SIL2_RLY_uio ---------->"+str(Red_SIL2_RLY_uio))
            row_index_nred_uio = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA UIO (0-5000)')
            Non_Red_SIL2_RLY_uio = IOComp.getColumnValue(cont, row_index_nred_uio, "Non_Red_SIL2_RLY")
            Trace.Write("Non_Red_SIL2_RLY_uio ---------->"+str(Non_Red_SIL2_RLY_uio))
            row_index_red_dio = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA DIO (0-5000)')
            Red_SIL2_RLY_dio = IOComp.getColumnValue(cont, row_index_red_dio, "Red_SIL2_RLY")
            Trace.Write("Red_SIL2_RLY_dio ---------->"+str(Red_SIL2_RLY_dio))
            row_index_nred_dio = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA DIO (0-5000)')
            Non_Red_SIL2_RLY_dio = IOComp.getColumnValue(cont, row_index_nred_dio, "Non_Red_SIL2_RLY")
            Trace.Write("Non_Red_SIL2_RLY_dio ---------->"+str(Non_Red_SIL2_RLY_dio))
            total = Red_SIL2_RLY_uio + Non_Red_SIL2_RLY_uio + Red_SIL2_RLY_dio + Non_Red_SIL2_RLY_dio
            Trace.Write(total)

            parts_dict["FC-UDOF01"] = {'Quantity' : int(total),'Description': 'SCA DIGITAL OUTPUT RELAY SIL 2 F&G'}
            Trace.Write("parts_dict:"+str(parts_dict))
    elif Product.Name == "SM Remote Group":
        IOComp = IOComponents(Product)
        sil2 = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName('SM_DI_DORelay_Adapter_UMC').Value
        Marshalling_Option = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        Red_SIL2_RLY_uio=Non_Red_SIL2_RLY_uio=Red_SIL2_RLY_dio=Non_Red_SIL2_RLY_dio=total=0
        if sil2 == "Yes" and Marshalling_Option == "Universal Marshalling":
        
            cont = IOComp.Product.GetContainerByName('SM_RG_DO_RLY_NMR_Cont')
            row_index_red_uio = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA UIO (0-5000)')
            Red_SIL2_RLY_uio = IOComp.getColumnValue(cont, row_index_red_uio, "Red_SIL2_RLY")
            Trace.Write("Red_SIL2_RLY_uio ---------->"+str(Red_SIL2_RLY_uio))
            row_index_nred_uio = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA UIO (0-5000)')
            Non_Red_SIL2_RLY_uio = IOComp.getColumnValue(cont, row_index_nred_uio, "Non_Red_SIL2_RLY")
            Trace.Write("Non_Red_SIL2_RLY_uio ---------->"+str(Non_Red_SIL2_RLY_uio))
            row_index_red_dio = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA DIO (0-5000)')
            Red_SIL2_RLY_dio = IOComp.getColumnValue(cont, row_index_red_dio, "Red_SIL2_RLY")
            Trace.Write("Red_SIL2_RLY_dio ---------->"+str(Red_SIL2_RLY_dio))
            row_index_nred_dio = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA DIO (0-5000)')
            Non_Red_SIL2_RLY_dio = IOComp.getColumnValue(cont, row_index_nred_dio, "Non_Red_SIL2_RLY")
            Trace.Write("Non_Red_SIL2_RLY_dio ---------->"+str(Non_Red_SIL2_RLY_dio))
            total = Red_SIL2_RLY_uio + Non_Red_SIL2_RLY_uio + Red_SIL2_RLY_dio + Non_Red_SIL2_RLY_dio
            Trace.Write(total)

        parts_dict["FC-UDOF01"] = {'Quantity' : int(total),'Description': 'SCA DIGITAL OUTPUT RELAY SIL 2 F&G'}
        Trace.Write("parts_dict:"+str(parts_dict))
    return parts_dict
#Val=get_FC_UDOF01(Product,{})
#Trace.Write(str(Val))
#31596
def get_USC(Product,parts_dict):
    Enclosure_Type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').Value
    Safety_Cabinets = int(Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)').Value)
    if Enclosure_Type == "Universal Safety Cab-1.3M" and Safety_Cabinets > 0:
        parts_dict["50159475-200"] = {'Quantity' : Safety_Cabinets,'Description': 'TPC Common Parts Kit'}
        parts_dict["50159997-100"] = {'Quantity' : Safety_Cabinets,'Description': 'UNIVERSAL SAFETY CABINET WARNING LABEL'}
    return parts_dict

#32158
def getidpartsbracket(Product,parts_dict):
    if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Universal Safety Cab-1.3M":
        qty = Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)").Value
        if qty=="":
            qty=0
        if Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="Yes":
            code=Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value
            code=str(code)
            if len(code)>17:
                p4=code[3]
                if p4=="N" or  p4=="S" or  p4=="X" :
                    parts_dict["51202692-200"] = {'Quantity' : 2*int(qty)  , 'Description': 'U-Shaped Bracket with DIN Isolation'}
        elif Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="No":
            parts_dict["51202692-200"] = {'Quantity' : 2*int(qty)  , 'Description': 'U-Shaped Bracket with DIN Isolation'}
    return parts_dict

#32161
def getELDqnt(Product,parts_dict):
    if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Universal Safety Cab-1.3M":
        qty = Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)").Value
        if qty=="":
            qty=0
        if Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="Yes":
            code = str(Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value)
            if len(code)>17:
                if (code[5]=="M" or code[5]=="U") and (code [8]=="A" or code [8]=="B" or code [8]=="C") and (code[12]=="F"):
                    parts_dict["FC-TELD-0001"] = {'Quantity' : int(qty)  , 'Description': 'UIO EARTH LEAKAGE DETECTOR 24VDC CC'}
        elif Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="No":
            FTAP=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Field_Termination_Assembly_for_PUIO").DisplayValue
            PUIO=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PUIO_Count").DisplayValue
            ELD=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Earth_Leakage_Detector_TELD").DisplayValue
            if (FTAP=="Default Marshalling FC-TUIO51/52" or FTAP=="Universal Marshalling, PTA") and (PUIO=="32" or PUIO=="64" or PUIO=="96") and (ELD=="Floating Power(TELD)"):
                parts_dict["FC-TELD-0001"] = {'Quantity' : int(qty)  , 'Description': 'UIO EARTH LEAKAGE DETECTOR 24VDC CC'}
    return parts_dict

#34332
def getBCTDqnt(Product,parts_dict):
    if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Universal Safety Cab-1.3M":
        qty = Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)").Value
        if qty=="":
            qty=0
        if Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="Yes":
            code = str(Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value)
            if len(code)>17:
                if code[5]=="X":
                    parts_dict["51202676-100"] = {'Quantity' : int(qty)*4  , 'Description': 'Bracket Cable Tie Down'}
                if code[5]=="X" and code[6]=="C" and code[7]=="X" :
                    parts_dict["51202676-100"] = {'Quantity' : int(qty)*2  , 'Description': 'Bracket Cable Tie Down'}
                if code[5]=="X" and code[6]=="X" and code[7]=="C" :
                    parts_dict["51202676-100"] = {'Quantity' : int(qty)*2  , 'Description': 'Bracket Cable Tie Down'}
                if code[5]=="X" and code[6]=="A" and code[7]=="B" :
                    parts_dict["51202676-100"] = {'Quantity' : int(qty)*2  , 'Description': 'Bracket Cable Tie Down'}
                if code[5]=="X" and code[6]=="B" and code[7]=="A" :
                    parts_dict["51202676-100"] = {'Quantity' : int(qty)*2  , 'Description': 'Bracket Cable Tie Down'}

        elif Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="No":
            wro=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Wire_Routing_Options").DisplayValue
            PUIO=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PUIO_Count").DisplayValue
            pdio=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PDIO_Count").DisplayValue
            if wro=="No Panduit":
                parts_dict["51202676-100"] = {'Quantity' : int(qty)*4  , 'Description': 'Bracket Cable Tie Down'}
            if wro=="No Panduit" and PUIO=="96"and pdio=="0" :
                parts_dict["51202676-100"] = {'Quantity' : int(qty)*2  , 'Description': 'Bracket Cable Tie Down'}
            if wro=="No Panduit" and PUIO=="0"and pdio=="96" :
                parts_dict["51202676-100"] = {'Quantity' : int(qty)*2  , 'Description': 'Bracket Cable Tie Down'}
            if wro=="No Panduit" and PUIO=="32"and pdio=="64" :
                parts_dict["51202676-100"] = {'Quantity' : int(qty)*2  , 'Description': 'Bracket Cable Tie Down'}
            if wro=="No Panduit" and PUIO=="64"and pdio=="32" :
                parts_dict["51202676-100"] = {'Quantity' : int(qty)*2  , 'Description': 'Bracket Cable Tie Down'}
            if wro=="Panduit":
                parts_dict["51509194-500"] = {'Quantity' : int(qty)  , 'Description': 'Panduit-Wiring Duct and Cover'}
    return parts_dict

#32157
def getidparts(Product,parts_dict):
    '''if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Universal Safety Cab-1.3M":
        qty = Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)").Value
        if qty=="":
            qty=0
        if Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="Yes":
            code=Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value
            code=str(code)
            if len(code)>17:
                p4=code[3]
                if p4=="N":
                    parts_dict["50159655-002"] = {'Quantity' : int(qty)  , 'Description': 'Boot connector for S300 IOTA'}
        elif Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="No":
            if Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("S300").DisplayValue=="Non Redundant S300":
                parts_dict["50159655-002"] = {'Quantity' : int(qty)  , 'Description': 'Boot connector for S300 IOTA'}'''
    return parts_dict

#34320
def Bootconnectorqty(Product,parts_dict):
    if Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="No":
        red=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("S300").DisplayValue
        ftpuio=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Field_Termination_Assembly_for_PUIO").DisplayValue
        ftpdio=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("Field_Termination_Assembly_for_PDIO").DisplayValue
        puio=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PUIO_Count").DisplayValue
        pdio=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("PDIO_Count").DisplayValue
        iored=Product.GetContainerByName("SM_SC_Universal_Safety_Cab_1_3M_Details_cont").Rows[0].GetColumnByName("IO_Redundancy").DisplayValue
        qty=Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)").Value
        Trace.Write("selection")


        if (red=="Redundant S300" or red=="No S300")	 	and (ftpdio=="Default Marshalling FC-TDIO51/52") and (puio=="0")	and (pdio=="32")	and (iored=="Non Redundant IO"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-1-")
        if (red=="Redundant S300" or red=="No S300")	 	and (ftpdio=="Default Marshalling FC-TDIO51/52")	and (puio=="0")	and (pdio=="64")	and (iored=="Non Redundant IO"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)*2  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-2-")
        if (red=="Redundant S300" or red=="No S300")	and (ftpuio=="Default Marshalling FC-TUIO51/52")	and (ftpdio=="Default Marshalling FC-TDIO51/52")	and (puio=="32")	and (pdio=="32")	and (iored=="Non Redundant IO"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-3-")
        if (red=="Redundant S300" or red=="No S300")	and (ftpuio=="Default Marshalling FC-TUIO51/52")	and (ftpdio=="Default Marshalling FC-TDIO51/52")	and (puio=="32")	and (pdio=="64")	and (iored=="Non Redundant IO"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)*2  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-4-")
        if (red=="Redundant S300" or red=="No S300")	and (ftpuio=="Default Marshalling FC-TUIO51/52")	and (ftpdio=="Default Marshalling FC-TDIO51/52")	and (puio=="64")	and (pdio=="32")	and (iored=="Non Redundant IO"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-5-")
        if (red=="Redundant S300" or red=="No S300")	 	and (ftpdio=="Default Marshalling FC-TDIO51/52")	and (puio=="0")	and (pdio=="96")	and (iored=="Non Redundant IO"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)*3  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-6-")
        if (red=="Redundant S300" or red=="No S300")	and (ftpuio=="Universal Marshalling, PTA" or ftpuio=="Intrinsically Safe")	and (ftpdio=="Default Marshalling FC-TDIO51/52")	and (puio=="32")	and (pdio=="32")	and (iored=="Non Redundant IO"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-7-")
        if (red=="Redundant S300" or red=="No S300")	and (ftpuio=="Universal Marshalling, PTA" or ftpuio=="Intrinsically Safe")	and (ftpdio=="Default Marshalling FC-TDIO51/52")	and (puio=="32")	and (pdio=="64")	and (iored=="Non Redundant IO"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)*2  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-8-")
        if (red=="Redundant S300" or red=="No S300")	and (ftpuio=="Universal Marshalling, PTA" or ftpuio=="Intrinsically Safe" or ftpuio=="32 IS, 32 Non-IS")	and (ftpdio=="Default Marshalling FC-TDIO51/52")	and (puio=="64")	and (pdio=="32") and (iored=="Non Redundant IO"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-9-")


    elif Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").DisplayValue=="Yes":
        code = str(Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet").Value)
        red=code[3]
        ftpuio=code[5]
        ftpdio=code[6]
        puio=code[8]       
        pdio=code[9]
        iored=code[13]
        qty=Product.GetContainerByName("SM_RG_Universal_Safety_Cabinet_1.3M_Cont").Rows[0].GetColumnByName("Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)").Value
        Trace.Write("Code")

        if (red=="S" or red=="X")	 	and (ftpdio=="M") and (puio=="X")	and (pdio=="A")	and (iored=="X"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-1-")
        if (red=="S" or red=="X")	 	and (ftpdio=="M")	and (puio=="X")	and (pdio=="B")	and (iored=="X"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)*2  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-2-")
        if (red=="S" or red=="X")	and (ftpuio=="M")	and (ftpdio=="M")	and (puio=="A")	and (pdio=="A")	and (iored=="X"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-3-")
        if (red=="S" or red=="X")	and (ftpuio=="M")	and (ftpdio=="M")	and (puio=="A")	and (pdio=="B")	and (iored=="X"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)*2  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-4-")
        if (red=="S" or red=="X")	and (ftpuio=="M")	and (ftpdio=="M")	and (puio=="B")	and (pdio=="A")	and (iored=="X"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-5-")
        if (red=="S" or red=="X")	 	and (ftpdio=="M")	and (puio=="X")	and (pdio=="C")	and (iored=="X"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)*3  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-6-")
        if (red=="S" or red=="X")	and (ftpuio=="U" or ftpuio=="I")	and (ftpdio=="M")	and (puio=="A")	and (pdio=="A")	and (iored=="X"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-7-")
        if (red=="S" or red=="X")	and (ftpuio=="U" or ftpuio=="I")	and (ftpdio=="M")	and (puio=="A")	and (pdio=="B")	and (iored=="X"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)*2  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-8-")
        if (red=="S" or red=="X")	and (ftpuio=="U" or ftpuio=="I" or ftpuio=="C")	and (ftpdio=="M")	and (puio=="B")	and (pdio=="A") and (iored=="X"):
            parts_dict["50159655-003"] = {'Quantity' : int(qty)  , 'Description': 'Boot connector for PDIO IOTA'}
            Trace.Write("-9-")
    return parts_dict