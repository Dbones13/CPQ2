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
#parts_dict={}
#33026
def get_FC_UDI501(Product,parts_dict):
    if Product.Name=="SM Control Group":
        IOComp = IOComponents(Product)
        Trace.Write("SM Control Group")
        Marshalling_Option = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        if Marshalling_Option == "Universal Marshalling":
            
            cont = IOComp.Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc with 5K Resistor UIO (0-5000)')
            red_nis_uio = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc with 5K Resistor UIO (0-5000)')
            nonred_nis_uio = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc with 5K Resistor DIO (0-5000)')
            red_nis_dio = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc with 5K Resistor DIO (0-5000)')
            nonred_nis_dio = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
            total = red_nis_uio + nonred_nis_uio + red_nis_dio + nonred_nis_dio

            parts_dict["FC-UDI501"] = {'Quantity' : int(total),'Description': 'SCA DIGITAL INPUT  5KOHM'}
            #Trace.Write("parts_dict:"+str(parts_dict))
    elif Product.Name == "SM Remote Group":
        IOComp = IOComponents(Product)
        Trace.Write("SM Remote Group")
        Marshalling_Option = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        if Marshalling_Option == "Universal Marshalling":
            
            cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc with 5K Resistor UIO  (0-5000)')
            red_nis_uio = IOComp.getColumnValue(cont, row_index, "Red_NIS")
            Trace.Write(red_nis_uio)
            row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc with 5K Resistor UIO  (0-5000)')
            nonred_nis_uio = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
            row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc with 5K Resistor DIO  (0-5000)')
            red_nis_dio = IOComp.getColumnValue(cont, row_index, "Red_NIS")
            row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc with 5K Resistor DIO  (0-5000)')
            nonred_nis_dio = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
            total = red_nis_uio + nonred_nis_uio + red_nis_dio + nonred_nis_dio

            parts_dict["FC-UDI501"] = {'Quantity' : int(total),'Description': 'SCA DIGITAL INPUT  5KOHM'}
            Trace.Write("parts_dict:"+str(parts_dict))
    return parts_dict
#Val=get_FC_UDI501(Product,parts_dict)
#Trace.Write(str(Val))
#33027
def get_FC_UIR501(Product,parts_dict):
    if Product.Name=="SM Control Group":
        IOComp = IOComponents(Product)
        Trace.Write("SM Control Group")
        Marshalling_Option = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        if Marshalling_Option == "Universal Marshalling":
            cont = IOComp.Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc with 5K Resistor UIO (0-5000)')
            red_rly_uio = IOComp.getColumnValue(cont, row_index, "Red (RLY)")
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc with 5K Resistor UIO (0-5000)')
            nonred_rly_uio = IOComp.getColumnValue(cont, row_index, "Non Red (RLY)")
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc with 5K Resistor DIO (0-5000)')
            red_rly_dio = IOComp.getColumnValue(cont, row_index, "Red (RLY)")
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc with 5K Resistor DIO (0-5000)')
            nonred_rly_dio = IOComp.getColumnValue(cont, row_index, "Non Red (RLY)")
            total = red_rly_uio + nonred_rly_uio + red_rly_dio + nonred_rly_dio

            parts_dict["FC-UIR501"] = {'Quantity' : int(total),'Description': 'SCA DIGITAL INPUT RELAY 5KOHM'}
            #Trace.Write("parts_dict:"+str(parts_dict))
    elif Product.Name == "SM Remote Group":
        IOComp = IOComponents(Product)
        Trace.Write("SM Remote Group")
        Marshalling_Option = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        if Marshalling_Option == "Universal Marshalling":
            cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc with 5K Resistor UIO  (0-5000)')
            red_rly_uio = IOComp.getColumnValue(cont, row_index, "Red_RLY")
            row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc with 5K Resistor UIO  (0-5000)')
            nonred_rly_uio = IOComp.getColumnValue(cont, row_index, "Non_Red_RLY")
            row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc with 5K Resistor DIO  (0-5000)')
            red_rly_dio = IOComp.getColumnValue(cont, row_index, "Red_RLY")
            row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc with 5K Resistor DIO  (0-5000)')
            nonred_rly_dio = IOComp.getColumnValue(cont, row_index, "Non_Red_RLY")
            total = red_rly_uio + nonred_rly_uio + red_rly_dio + nonred_rly_dio

            parts_dict["FC-UIR501"] = {'Quantity' : int(total),'Description': 'SCA DIGITAL INPUT RELAY 5KOHM'}
            #Trace.Write("parts_dict:"+str(parts_dict))
    return parts_dict
#33028
def get_FC_UDIR01(Product,parts_dict):
    if Product.Name=="SM Control Group":
        IOComp = IOComponents(Product)
        Marshalling_Option = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        if Marshalling_Option == "Universal Marshalling":
            
            sil2 = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName('DI/DO_SIL2/3_Relay_Adapter_UMC').Value
            Red_SIL2_RLY_uio=Non_Red_SIL2_RLY_uio=Red_SIL2_RLY_dio=Non_Red_SIL2_RLY_dio=total=0
            if sil2 == "Yes":

                cont = IOComp.Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont')
                row_index_red_uio = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
                Red_SIL3_RLY_uio = IOComp.getColumnValue(cont, row_index_red_uio, "Red_SIL3_RLY")
                Trace.Write("Red_SIL3_RLY_uio ---------->"+str(Red_SIL3_RLY_uio))
                row_index_nred_uio = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
                Non_Red_SIL3_RLY_uio = IOComp.getColumnValue(cont, row_index_nred_uio, "Non_Red_SIL3_RLY")
                Trace.Write("Non_Red_SIL3_RLY_uio ---------->"+str(Non_Red_SIL3_RLY_uio))
                row_index_red_dio = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc DIO (0-5000)')
                Red_SIL3_RLY_dio = IOComp.getColumnValue(cont, row_index_red_dio, "Red_SIL3_RLY")
                Trace.Write("Red_SIL3_RLY_dio ---------->"+str(Red_SIL3_RLY_dio))
                row_index_nred_dio = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc DIO (0-5000)')
                Non_Red_SIL3_RLY_dio = IOComp.getColumnValue(cont, row_index_nred_dio, "Non_Red_SIL3_RLY")
                Trace.Write("Non_Red_SIL3_RLY_dio ---------->"+str(Non_Red_SIL3_RLY_dio))
                total = Red_SIL3_RLY_uio + Non_Red_SIL3_RLY_uio + Red_SIL3_RLY_dio + Non_Red_SIL3_RLY_dio
                Trace.Write(total)



                parts_dict["FC-UDIR01"] = {'Quantity' : int(total),'Description': 'SCA DIGITAL INPUT RELAY'}
                #Trace.Write("parts_dict:"+str(parts_dict))
    elif Product.Name == "SM Remote Group":
        IOComp = IOComponents(Product)
        Marshalling_Option = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
        if Marshalling_Option == "Universal Marshalling":
            sil2 = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName('SM_DI_DORelay_Adapter_UMC').Value
            Red_SIL2_RLY_uio=Non_Red_SIL2_RLY_uio=Red_SIL2_RLY_dio=Non_Red_SIL2_RLY_dio=total=0
            if sil2 == "Yes":

                cont = IOComp.Product.GetContainerByName('SM_RG_DI_RLY_NMR_Cont')
                row_index_red_uio = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
                Red_SIL3_RLY_uio = IOComp.getColumnValue(cont, row_index_red_uio, "Red_SIL3_RLY")
                Trace.Write("Red_SIL3_RLY_uio ---------->"+str(Red_SIL3_RLY_uio))
                row_index_nred_uio = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
                Non_Red_SIL3_RLY_uio = IOComp.getColumnValue(cont, row_index_nred_uio, "Non_Red_SIL3_RLY")
                Trace.Write("Non_Red_SIL3_RLY_uio ---------->"+str(Non_Red_SIL3_RLY_uio))
                row_index_red_dio = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc DIO (0-5000)')
                Red_SIL3_RLY_dio = IOComp.getColumnValue(cont, row_index_red_dio, "Red_SIL3_RLY")
                Trace.Write("Red_SIL3_RLY_dio ---------->"+str(Red_SIL3_RLY_dio))
                row_index_nred_dio = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc DIO (0-5000)')
                Non_Red_SIL3_RLY_dio = IOComp.getColumnValue(cont, row_index_nred_dio, "Non_Red_SIL3_RLY")
                Trace.Write("Non_Red_SIL3_RLY_dio ---------->"+str(Non_Red_SIL3_RLY_dio))
                total = Red_SIL3_RLY_uio + Non_Red_SIL3_RLY_uio + Red_SIL3_RLY_dio + Non_Red_SIL3_RLY_dio
                Trace.Write(total)



                parts_dict["FC-UDIR01"] = {'Quantity' : int(total),'Description': 'SCA DIGITAL INPUT RELAY'}
                #Trace.Write("parts_dict:"+str(parts_dict))
    return parts_dict