#CXCPQ-33036
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

def Part_CC_USCA01_Calc(Prod, parts_dict):
    Trace.Write("Product Name : "+Prod.Name)
    if Prod.Name=="SM Control Group":
        IOComp = IOComponents(Prod)
        try:
            per_spare = Prod.GetContainerByName('SM_CG_Universal_Marshalling_Cabinet_Details').Rows[0].GetColumnByName("Percentage of Spare Space").Value
        except:
            per_spare = 0
        if not per_spare:
            per_spare = 0
        di_do_relay = Prod.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("DI/DO_SIL2/3_Relay_Adapter_UMC").DisplayValue
        namur = Prod.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("DI_NAMUR_proximity_Switches_Adapter_UMC").DisplayValue
        Trace.Write(str(per_spare) + " : " + str(di_do_relay) + " : " + str(namur))
        if di_do_relay == 'Yes' or namur == 'Yes':
            Trace.Write("DI/DO and Namur set to Yes")
            cont = IOComp.Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
            A_di_uio_sil3_rly = IOComp.getColumnValue(cont, row_index, "Red_SIL3_RLY")
            B_di_uio_sil3_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_SIL3_RLY")
            A_di_uio_nmr = IOComp.getColumnValue(cont, row_index, "Red_NMR")
            B_di_uio_nmr_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NMR")
            A_di_uio_nmr_safety = IOComp.getColumnValue(cont, row_index, "Red_NMR_Safety")
            B_di_uio_nmr_safety_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NMR_Safety")

            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc DIO (0-5000)')
            C_di_dio_sil3_rly = IOComp.getColumnValue(cont, row_index, "Red_SIL3_RLY")
            D_di_dio_sil3_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_SIL3_RLY")
            C_di_dio_nmr = IOComp.getColumnValue(cont, row_index, "Red_NMR")
            D_di_dio_nmr_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NMR")
            C_di_dio_nmr_safety = IOComp.getColumnValue(cont, row_index, "Red_NMR_Safety")
            D_di_dio_nmr_safety_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NMR_Safety")

            cont = IOComp.Product.GetContainerByName('SM_CG_DO_RLY_NMR_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA UIO (0-5000)')
            A_do_uio_sil3_rly = IOComp.getColumnValue(cont, row_index, "Red_SIL3_RLY")
            B_do_uio_sil3_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_SIL3_RLY")

            row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA DIO (0-5000)')
            C_do_dio_sil3_rly = IOComp.getColumnValue(cont, row_index, "Red_SIL3_RLY")
            D_do_dio_sil3_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_SIL3_RLY")

        else:
            A_di_uio_sil3_rly = 0
            B_di_uio_sil3_rly_nr = 0
            C_di_dio_sil3_rly = 0
            D_di_dio_sil3_rly_nr = 0
            A_do_uio_sil3_rly = 0
            B_do_uio_sil3_rly_nr = 0
            C_do_dio_sil3_rly = 0
            D_do_dio_sil3_rly_nr = 0
            A_di_uio_nmr = 0
            B_di_uio_nmr_nr = 0
            C_di_dio_nmr = 0
            D_di_dio_nmr_nr = 0
            A_di_uio_nmr_safety = 0
            B_di_uio_nmr_safety_nr = 0
            C_di_dio_nmr_safety = 0
            D_di_dio_nmr_safety_nr = 0

        cont = IOComp.Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc with 5K Resistor UIO (0-5000)')
        A_di_5k_resistor_uio_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        B_di_5k_resistor_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
        A_di_5k_resistor_uio_rly = IOComp.getColumnValue(cont, row_index, "Red (RLY)")
        B_di_5k_resistor_uio_rly_nr = IOComp.getColumnValue(cont, row_index, "Non Red (RLY)")

        row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc with 5K Resistor DIO (0-5000)')
        C_di_5k_resistor_dio_nis = IOComp.getColumnValue(cont, row_index, "Red (NIS)")
        D_di_5k_resistor_dio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non Red (NIS)")
        C_di_5k_resistor_dio_rly = IOComp.getColumnValue(cont, row_index, "Red (RLY)")
        D_di_5k_resistor_dio_rly_nr = IOComp.getColumnValue(cont, row_index, "Non Red (RLY)")

        A_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (A_di_uio_sil3_rly + A_di_uio_nmr + A_di_uio_nmr_safety + A_do_uio_sil3_rly + A_di_5k_resistor_uio_nis + A_di_5k_resistor_uio_rly))/float(16))
        B_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (B_di_uio_sil3_rly_nr + B_di_uio_nmr_nr + B_di_uio_nmr_safety_nr + B_do_uio_sil3_rly_nr + B_di_5k_resistor_uio_nis_nr + B_di_5k_resistor_uio_rly_nr))/float(16))
        C_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (C_di_dio_sil3_rly + C_di_dio_nmr + C_di_dio_nmr_safety + C_do_dio_sil3_rly + C_di_5k_resistor_dio_nis + C_di_5k_resistor_dio_rly))/float(16))
        D_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (D_di_dio_sil3_rly_nr + D_di_dio_nmr_nr + D_di_dio_nmr_safety_nr + D_do_dio_sil3_rly_nr + D_di_5k_resistor_dio_nis_nr + D_di_5k_resistor_dio_rly_nr))/float(16))
        Trace.Write(str(A_qty) + " : " + str(B_qty) + " : " + str(C_qty) + " : " +str(D_qty))
        part_qty = A_qty + B_qty + C_qty + D_qty
        Trace.Write("Parts qty = " + str(part_qty))
        if part_qty > 0:
            pass
            #parts_dict["CC-USCA01"] = {'Quantity' : int(part_qty), 'Description': 'SCA- SIGNAL CONDITIONING ASSEMBLY 24V'}
    elif Prod.Name=="SM Remote Group":
        IOComp = IOComponents(Prod)
        try:
            per_spare = Prod.GetContainerByName('SM_RG_Universal_Marshalling_Cabinet_Details').Rows[0].GetColumnByName("Percentage of Spare Space").Value
        except:
            per_spare = 0
        if not per_spare:
            per_spare = 0
        di_do_relay = Prod.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_DI_DORelay_Adapter_UMC").DisplayValue
        namur = Prod.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_DI_NAMUR_Switches_Adapter_UMC").DisplayValue
        Trace.Write(str(per_spare) + " : " + str(di_do_relay) + " : " + str(namur))
        if di_do_relay == 'Yes' or namur == 'Yes':
            Trace.Write("DI/DO and Namur set to Yes")
            cont = IOComp.Product.GetContainerByName('SM_RG_DI_RLY_NMR_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc UIO (0-5000)')
            A_di_uio_sil3_rly = IOComp.getColumnValue(cont, row_index, "Red_SIL3_RLY")
            B_di_uio_sil3_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_SIL3_RLY")
            A_di_uio_nmr = IOComp.getColumnValue(cont, row_index, "Red_NMR")
            B_di_uio_nmr_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NMR")
            A_di_uio_nmr_safety = IOComp.getColumnValue(cont, row_index, "Red_NMR_Safety")
            B_di_uio_nmr_safety_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NMR_Safety")

            row_index = IOComp.getRowIndex(cont, 'Digital Input Type', 'SDI(1) 24Vdc DIO (0-5000)')
            C_di_dio_sil3_rly = IOComp.getColumnValue(cont, row_index, "Red_SIL3_RLY")
            D_di_dio_sil3_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_SIL3_RLY")
            C_di_dio_nmr = IOComp.getColumnValue(cont, row_index, "Red_NMR")
            D_di_dio_nmr_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NMR")
            C_di_dio_nmr_safety = IOComp.getColumnValue(cont, row_index, "Red_NMR_Safety")
            D_di_dio_nmr_safety_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NMR_Safety")

            cont = IOComp.Product.GetContainerByName('SM_RG_DO_RLY_NMR_Cont')
            row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA UIO (0-5000)')
            A_do_uio_sil3_rly = IOComp.getColumnValue(cont, row_index, "Red_SIL3_RLY")
            B_do_uio_sil3_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_SIL3_RLY")

            row_index = IOComp.getRowIndex(cont, 'Digital Output Type', 'SDO(1) 24Vdc 500mA DIO (0-5000)')
            C_do_dio_sil3_rly = IOComp.getColumnValue(cont, row_index, "Red_SIL3_RLY")
            D_do_dio_sil3_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_SIL3_RLY")

        else:
            A_di_uio_sil3_rly = 0
            B_di_uio_sil3_rly_nr = 0
            C_di_dio_sil3_rly = 0
            D_di_dio_sil3_rly_nr = 0
            A_do_uio_sil3_rly = 0
            B_do_uio_sil3_rly_nr = 0
            C_do_dio_sil3_rly = 0
            D_do_dio_sil3_rly_nr = 0
            A_di_uio_nmr = 0
            B_di_uio_nmr_nr = 0
            C_di_dio_nmr = 0
            D_di_dio_nmr_nr = 0
            A_di_uio_nmr_safety = 0
            B_di_uio_nmr_safety_nr = 0
            C_di_dio_nmr_safety = 0
            D_di_dio_nmr_safety_nr = 0

        cont = IOComp.Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont')
        row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc with 5K Resistor UIO  (0-5000)')
        A_di_5k_resistor_uio_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
        B_di_5k_resistor_uio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
        A_di_5k_resistor_uio_rly = IOComp.getColumnValue(cont, row_index, "Red_RLY")
        B_di_5k_resistor_uio_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_RLY")

        row_index = IOComp.getRowIndex(cont, 'Digital_Input_Type', 'SDI(1) 24Vdc with 5K Resistor DIO  (0-5000)')
        C_di_5k_resistor_dio_nis = IOComp.getColumnValue(cont, row_index, "Red_NIS")
        D_di_5k_resistor_dio_nis_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_NIS")
        C_di_5k_resistor_dio_rly = IOComp.getColumnValue(cont, row_index, "Red_RLY")
        D_di_5k_resistor_dio_rly_nr = IOComp.getColumnValue(cont, row_index, "Non_Red_RLY")

        A_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (A_di_uio_sil3_rly + A_di_uio_nmr + A_di_uio_nmr_safety + A_do_uio_sil3_rly + A_di_5k_resistor_uio_nis + A_di_5k_resistor_uio_rly))/float(16))
        B_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (B_di_uio_sil3_rly_nr + B_di_uio_nmr_nr + B_di_uio_nmr_safety_nr + B_do_uio_sil3_rly_nr + B_di_5k_resistor_uio_nis_nr + B_di_5k_resistor_uio_rly_nr))/float(16))
        C_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (C_di_dio_sil3_rly + C_di_dio_nmr + C_di_dio_nmr_safety + C_do_dio_sil3_rly + C_di_5k_resistor_dio_nis + C_di_5k_resistor_dio_rly))/float(16))
        D_qty = D.Ceiling(((1+float(per_spare)/float(100)) * (D_di_dio_sil3_rly_nr + D_di_dio_nmr_nr + D_di_dio_nmr_safety_nr + D_do_dio_sil3_rly_nr + D_di_5k_resistor_dio_nis_nr + D_di_5k_resistor_dio_rly_nr))/float(16))
        Trace.Write(str(A_qty) + " : " + str(B_qty) + " : " + str(C_qty) + " : " +str(D_qty))
        part_qty = A_qty + B_qty + C_qty + D_qty
        Trace.Write("Parts qty = " + str(part_qty))
        if part_qty > 0:
            pass
            #parts_dict["CC-USCA01"] = {'Quantity' : int(part_qty), 'Description': 'SCA- SIGNAL CONDITIONING ASSEMBLY 24V'}
    return parts_dict

#part={}
#x=Part_CC_USCA01_Calc(Product, part)
#Trace.Write(str(part))