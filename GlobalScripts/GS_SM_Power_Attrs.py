import math as m
import re

class AttrStorage:
    def get_float(val):
        if val:
            return float(val)
        return 0

    def get_container(self, product, name):
        return product.GetContainerByName(name)

    def get_column_value(self, row, col):
        return row.GetColumnByName(col).Value

    def fix_space(self, val):
        return " ".join(val.split())

    def process_container(self, cont, key_column_map, type_prefix_map, suffix_key='name'):
        key = key_column_map.get(cont.Name)
        if not key:
            return
        for row in cont.Rows:
            key_val = self.get_column_value(row, key)
            key_val = self.fix_space(key_val)
            prefix = type_prefix_map.get(key_val)
            for col in row.Columns:
                if suffix_key == "headerLabel":
                    suffix = self.get_suffix(col.HeaderLabel)
                else:
                    suffix = self.get_suffix(col.Name)
                attr_name = '{}_{}'.format(prefix, suffix)
                setattr(self, attr_name, col.Value)

    def get_suffix(self, colName):
        suffix = list()
        suffix.append('nrd' if colName.startswith('Non Red') else 'rd')

        #regex to find substr between brakcets
        reg = r'\((.*?)\)'
        reg_search = re.search(reg, colName)
        if reg_search:
            substr = reg_search.group(1)
            substr = substr.strip()
            substr = substr.replace(" ", "_")
            substr = substr.lower()
            suffix.append(substr)

        return "_".join(suffix)

    def __init__(self, Product):
        type_prefix_map = {
            "SDI(1) 24Vdc UIO (0-5000)" : "sdi1_uio",
            "SDI(1) 24Vdc SIL2 P+F UIO (0-5000)" : "sdi1_sil2_pf_uio",
            "SDI(1) 24Vdc SIL3 P+F UIO (0-5000)" : "sdi1_sil3_pf_uio",
            "SDI(1) 24Vdc Line Mon UIO (0-5000)" : "sdi1_line_mon_uio",
            "SDI(1) 24Vdc with 5K Resistor UIO (0-5000)" : "sdi1_5k_resistor_uio",
            "SDI(1) 24Vdc DIO (0-5000)" : "sdi1_dio",
            "SDI(1) 24Vdc Line Mon DIO (0-5000)" : "sdi1_line_mon_dio",
            "SDI(1) 24Vdc with 5K Resistor DIO (0-5000)" : "sdi1_5k_resistor_dio",
            "SDO(1) 24Vdc 500mA UIO (0-5000)" : "sdo1_uio",
            "SDO(2)24Vdc 1A UIO (0-5000)" : "sdo2_1a_uio",
            "SDO(4)24Vdc 2A UIO (0-5000)" : "sdo4_2a_uio",
            "SDO(7) 24Vdc Line Mon UIO (0-5000)" : "sdo7_line_mon_uio",
            "SDO(16) SIL 2/3 250Vac/Vdc UIO (0-5000)" : "sdo16_sil23_uio",
            "SDO(16) SIL 2/3 250Vac/Vdc COM UIO (0-5000)" : "sdo12_sil23_com_uio",
            "SDO(1) 24Vdc 500mA DIO (0-5000)" : "sdo1_dio",
            "SDO(16) SIL 2/3 250Vac/Vdc DIO (0-5000)" : "sdo16_sil23_dio",
            "SDO(16) SIL 2/3 250Vac/Vdc COM DIO (0-5000)" : "sdo16_sil23_com_dio",
            "SAI(1)mA type Current UIO (0-5000)" : "sai1_uio",
            "SAI(1)FIRE 2 wire current UIO (0-5000)" : "sai1_fire2_wire_uio",
            "SAI(1)FIRE 3-4 wire current UIO (0-5000)" : "sai1_fire34_wire_uio",
            "SAI(1)FIRE 3-4 wire current Sink UIO (0-5000)" : "sai1_fire34_wire_sink_uio",
            "SAI(1) GAS current UIO (0-5000)" : "sai1_gas_uio",
            "SAO(1)mA Type UIO (0-5000)" : "sao1_uio"
        }
        if Product.Name == "SM Control Group":
            process_containers = {
                "SM_IO_Count_Digital_Input_Cont" : 'name',
                "SM_IO_Count_Digital_Output_Cont" : 'name',
                "SM_IO_Count_Analog_Input_Cont" : 'name',
                "SM_IO_Count_Analog_Output_Cont" : 'name',
                "SM_CG_DI_RLY_NMR_Cont" : 'headerLabel',
                "SM_CG_DO_RLY_NMR_Cont" : 'headerLabel'
            }
            key_column_map = {
                "SM_IO_Count_Digital_Input_Cont" : "Digital Input Type",
                "SM_IO_Count_Digital_Output_Cont" : "Digital Output Type",
                "SM_IO_Count_Analog_Input_Cont" : "Analog Input Type",
                "SM_IO_Count_Analog_Output_Cont" : "Analog Output Type",
                "SM_CG_DI_RLY_NMR_Cont" : 'Digital Input Type',
                "SM_CG_DO_RLY_NMR_Cont" : 'Digital Output Type'
            }
            cabinet_left_cont_rows = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows
            cabinet_right_cont_rows = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows

            unit_load_col_name = "SDO_24Vdc_500mA_UIO_DIO_UnitLoad1mA-500mA"

            try:
                Marshalling_Option = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
            except:
                Marshalling_Option = ""
            if Marshalling_Option == "Hardware Marshalling with P+F":
                try:
                    self.power_supply = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName("Power_Supply").DisplayValue
                except:
                    self.power_supply = ""
                try:
                    self.uio_di_sil2 =(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Red (IS)").Value)
                except:
                    self.uio_di_sil2 = 0
                try:
                    self.uio_di_sil2_nr =(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Non Red (IS)").Value)
                except:
                    self.uio_di_sil2_nr =0
                try:
                    self.uio_di_sil3 =(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Red (IS)").Value)
                except:
                    self.uio_di_sil3 =0
                try:
                    self.uio_di_sil3_nr =(Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Non Red (IS)").Value)
                except:
                    self.uio_di_sil3_nr =0

                # AI
                try:
                    self.uio_ai_pf =(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Red (IS)").Value)
                except:
                    self.uio_ai_pf =0
                try:
                    self.uio_ai_pf_nr =(Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Non Red (IS)").Value)
                except:
                    self.uio_ai_pf_nr =0
                # AO
                try:
                    self.uio_ao_pf =(Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont').Rows[1].GetColumnByName("Red (IS)").Value)
                except:
                    self.uio_ao_pf =0
                try:
                    self.uio_ao_pf_nr =(Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont').Rows[1].GetColumnByName("Non Red (IS)").Value)
                except:
                    self.uio_ao_pf_nr =0
                # DO
                try:
                    self.uio_do_sil3 =(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName("Red (IS)").Value)
                except:
                    self.uio_do_sil3 =0
                try:
                    self.uio_do_sil3_nr =(Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName("Non Red (IS)").Value)
                except:
                    self.uio_do_sil3_nr =0
        elif Product.Name == "SM Remote Group":
            process_containers = {
                "SM_RG_IO_Count_Digital_Input_Cont" : 'headerLabel',
                "SM_RG_IO_Count_Digital_Output_Cont" : 'headerLabel',
                "SM_RG_IO_Count_Analog_Input_Cont" : 'headerLabel',
                "SM_RG_IO_Count_Analog_Output_Cont" : 'headerLabel',
				"SM_RG_DI_RLY_NMR_Cont" : 'headerLabel',
                "SM_RG_DO_RLY_NMR_Cont" : 'headerLabel'
            }
            key_column_map = {
                "SM_RG_IO_Count_Digital_Input_Cont" : "Digital_Input_Type",
                "SM_RG_IO_Count_Digital_Output_Cont" : "Digital_Output_Type",
                "SM_RG_IO_Count_Analog_Input_Cont" : "Analog_Input_Type",
                "SM_RG_IO_Count_Analog_Output_Cont" : "Analog_Output_Type",
                "SM_RG_DI_RLY_NMR_Cont" : 'Digital Input Type',
                "SM_RG_DO_RLY_NMR_Cont" : 'Digital Output Type'
            }
            cabinet_left_cont_rows = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows
            cabinet_right_cont_rows = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows

            unit_load_col_name = "SM_SDO_UIO_DIO"

            try:
                Marshalling_Option = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
            except:
                Marshalling_Option = ""
            if Marshalling_Option == "Hardware Marshalling with P+F":
                try:
                    self.power_supply = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Power_Supply').DisplayValue
                except:
                    self.power_supply = ""
                try:
                    self.uio_di_sil2 =(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Red_IS").Value)
                except:
                    self.uio_di_sil2 =0
                try:
                    self.uio_di_sil2_nr =(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Non_Red_IS").Value)
                except:
                    self.uio_di_sil2_nr =0

                try:
                    self.uio_di_sil3 =(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Red_IS").Value)
                except:
                    self.uio_di_sil3 =0
                try:
                    self.uio_di_sil3_nr =(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Non_Red_IS").Value)
                except:
                    self.uio_di_sil3_nr =0

                # AI
                try:
                    self.uio_ai_pf =(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Red_IS").Value)
                except:
                    self.uio_ai_pf =0
                try:
                    self.uio_ai_pf_nr =(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Non_Red_IS").Value)
                except:
                    self.uio_ai_pf_nr =0
                # AO
                try:
                    self.uio_ao_pf =(Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows[1].GetColumnByName("Red_IS").Value)
                except:
                    self.uio_ao_pf =0
                try:
                    self.uio_ao_pf_nr =(Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows[1].GetColumnByName("Non_Red_IS").Value)
                except:
                    self.uio_ao_pf_nr =0
                # DO
                try:
                    self.uio_do_sil3 =(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName("Red_IS").Value)
                except:
                    self.uio_do_sil3 =0
                try:
                    self.uio_do_sil3_nr =(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName("Non_Red_IS").Value)
                except:
                    self.uio_do_sil3_nr =0

        for cont_name, suffix_key in process_containers.items():
            cont = self.get_container(Product, cont_name)
            self.process_container(cont, key_column_map, type_prefix_map, suffix_key)
        #power supply
        try:
            self.power_supply = cabinet_left_cont_rows[0].GetColumnByName("Power_Supply").DisplayValue
        except:
            self.power_supply = ""
        try:
            self.unit_load = cabinet_right_cont_rows[0][unit_load_col_name]
        except:
            self.unit_load = ""