import math as m
import re

class AttrStorage:

    def get_container(self, product, name):
        return product.GetContainerByName(name)

    def get_column_value(self, row, col):
        return row.GetColumnByName(col).Value

    def fix_space(self, val):
        return " ".join(val.split())

    def process_container(self, cont, suffix_key='name'):
        key_column_map = {
            "SM_IO_Count_Digital_Input_Cont" : "Digital Input Type",
            "SM_IO_Count_Digital_Output_Cont" : "Digital Output Type",
            "SM_IO_Count_Analog_Input_Cont" : "Analog Input Type",
            "SM_IO_Count_Analog_Output_Cont" : "Analog Output Type",
            "SM_CG_DI_RLY_NMR_Cont" : 'Digital Input Type',
            "SM_CG_DO_RLY_NMR_Cont" : 'Digital Output Type',
            "SM_RG_IO_Count_Digital_Input_Cont" : "Digital_Input_Type",
            "SM_RG_IO_Count_Digital_Output_Cont" : "Digital_Output_Type",
            "SM_RG_IO_Count_Analog_Input_Cont" : "Analog_Input_Type",
            "SM_RG_IO_Count_Analog_Output_Cont" : "Analog_Output_Type",
            "SM_RG_DI_RLY_NMR_Cont" : "Digital Input Type",
            "SM_RG_DO_RLY_NMR_Cont" : "Digital Output Type"
        }
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
        if Product.Name == "SM Control Group":
            process_containers = {
                "SM_IO_Count_Digital_Input_Cont" : 'name',
                "SM_IO_Count_Digital_Output_Cont" : 'name',
                "SM_IO_Count_Analog_Input_Cont" : 'name',
                "SM_IO_Count_Analog_Output_Cont" : 'name',
                "SM_CG_DI_RLY_NMR_Cont" : 'headerLabel',
                "SM_CG_DO_RLY_NMR_Cont" : 'headerLabel'
            }

            for cont_name, suffix_key in process_containers.items():
                cont = self.get_container(Product, cont_name)
                self.process_container(cont, suffix_key)

            io_count_ai_cont_rows = Product.GetContainerByName('SM_IO_Count_Analog_Input_Cont').Rows
            io_count_ao_cont_rows = Product.GetContainerByName('SM_IO_Count_Analog_Output_Cont').Rows
            io_count_do_cont_rows = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont').Rows
            io_count_di_cont_rows = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont').Rows
            rly_nmr_di_cont_rows = Product.GetContainerByName('SM_CG_DI_RLY_NMR_Cont').Rows
            rly_nmr_do_cont_rows = Product.GetContainerByName('SM_CG_DO_RLY_NMR_Cont').Rows
            cabinet_left_cont_rows = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows
            cabinet_right_cont_rows = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows
            common_que_cont_rows = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows
            universal_marshalling_cabinet = Product.GetContainerByName('SM_CG_Universal_Marshalling_Cabinet_Details').Rows

            #Power Supply
            self.power_supply = cabinet_left_cont_rows[0].GetColumnByName("Power_Supply").DisplayValue
            #Unit Load
            self.unit_load = cabinet_right_cont_rows[0].GetColumnByName("SDO_24Vdc_500mA_UIO_DIO_UnitLoad1mA-500mA").DisplayValue
            # percent
            self.percent_spare_io = cabinet_right_cont_rows[0].GetColumnByName("Percent_Installed_Spare_IOs").Value
            # Universal IOTA
            self.universal_iota = common_que_cont_rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue
            # Marshalling Option
            self.marshalling_option = cabinet_left_cont_rows[0].GetColumnByName("Marshalling_Option").DisplayValue
            ## Universal Marshalling cabinet cont
            if universal_marshalling_cabinet.Count > 0:
                # Cabinet access
                self.cabinet_access = universal_marshalling_cabinet[0].GetColumnByName("Cabinet").DisplayValue
                if not self.cabinet_access:
                    self.cabinet_access = "Dual Access"
                # Cabinet layout
                self.cabinet_layout = universal_marshalling_cabinet[0].GetColumnByName("Cabinet Layout").DisplayValue
                if not self.cabinet_layout:
                    self.cabinet_layout = "3 Column"
                # Cabinet power
                self.cabinet_power = universal_marshalling_cabinet[0].GetColumnByName("Cabinet Power").DisplayValue
                if not self.cabinet_power:
                    self.cabinet_power = "120/230 VAC"
                # Mounting Option
                self.mounting_option = universal_marshalling_cabinet[0].GetColumnByName("Mounting Option").DisplayValue
                if not self.mounting_option:
                    self.mounting_option = "Bracket Mounting"
                #SIC Cable Length
                self.sic_cable_length = universal_marshalling_cabinet[0].GetColumnByName("SIC cable length for RUSIO/PUIO/ PDIO").DisplayValue
            try:
                self.marshalling_percent_spare_io = universal_marshalling_cabinet[0].GetColumnByName("Percentage of Spare Space").Value
            except:
                self.marshalling_percent_spare_io = 0

        elif Product.Name == "SM Remote Group":
            process_containers = {
                "SM_RG_IO_Count_Digital_Input_Cont" : 'headerLabel',
                "SM_RG_IO_Count_Digital_Output_Cont" : 'headerLabel',
                "SM_RG_IO_Count_Analog_Input_Cont" : 'headerLabel',
                "SM_RG_IO_Count_Analog_Output_Cont" : 'headerLabel',
                "SM_RG_DI_RLY_NMR_Cont" : 'headerLabel',
                "SM_RG_DO_RLY_NMR_Cont" : 'headerLabel'
            }

            for cont_name, suffix_key in process_containers.items():
                cont = self.get_container(Product, cont_name)
                self.process_container(cont, suffix_key)

            io_count_ai_cont_rows = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows
            io_count_ao_cont_rows = Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows
            io_count_do_cont_rows = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows
            io_count_di_cont_rows = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows
            cabinet_left_cont_rows = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows
            atex_enclosure_cont_rows= Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows
            universal_marshalling_cabinet = Product.GetContainerByName('SM_RG_Universal_Marshalling_Cabinet_Details').Rows

            self.universal_iota = Product.Attr('SM_Universal_IOTA_Type').GetValue()
            self.enclosure_type = atex_enclosure_cont_rows[0].GetColumnByName('Enclosure_Type').DisplayValue
            self.marshalling_option = cabinet_left_cont_rows[0].GetColumnByName('Marshalling_Option').DisplayValue
            ## Universal Marshalling cabinet cont
            if universal_marshalling_cabinet.Count > 0:
                # Cabinet access
                self.cabinet_access = universal_marshalling_cabinet[0].GetColumnByName("Cabinet").DisplayValue
                if not self.cabinet_access:
                    self.cabinet_access = "Dual Access"
                # Cabinet layout
                self.cabinet_layout = universal_marshalling_cabinet[0].GetColumnByName("Cabinet Layout").DisplayValue
                if not self.cabinet_layout:
                    self.cabinet_layout = "3 Column"
                # Cabinet power
                self.cabinet_power = universal_marshalling_cabinet[0].GetColumnByName("Cabinet Power").DisplayValue
                if not self.cabinet_power:
                    self.cabinet_power = "120/230 VAC"
                # Mounting Option
                self.mounting_option = universal_marshalling_cabinet[0].GetColumnByName("Mounting Option").DisplayValue
                if not self.mounting_option:
                    self.mounting_option = "Bracket Mounting"
                #SIC Cable Length
                self.sic_cable_length = universal_marshalling_cabinet[0].GetColumnByName("SIC cable length for RUSIO/PUIO/ PDIO").DisplayValue
            try:
                self.marshalling_percent_spare_io = universal_marshalling_cabinet[0].GetColumnByName("Percentage of Spare Space").Value
            except:
                self.marshalling_percent_spare_io = 0
            #self.universal_iota = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue
            #self.marshalling_option =Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName("Marshalling_Option").DisplayValue
            '''if self.enclosure_type != "Cabinet":
                self.marshalling_option = ""'''
            #CXCPQ- 30841(Non Red(IS))
            # AI
            try:
                self.current_uio_NRD = io_count_ai_cont_rows[0].GetColumnByName("Non_Red_IS").Value
            except:
                self.current_uio_NRD = 0
            try:
                self.fire2_NRD = io_count_ai_cont_rows[1].GetColumnByName("Non_Red_IS").Value
            except:
                self.fire2_NRD = 0
            try:
                self.fire3and4_NRD = io_count_ai_cont_rows[2].GetColumnByName("Non_Red_IS").Value
            except:
                self.fire3and4_NRD = 0
            try:
                self.fire3and4_sink_NRD = io_count_ai_cont_rows[3].GetColumnByName("Non_Red_IS").Value
            except:
                self.fire3and4_sink_NRD = 0
            try:
                self.gas_NRD = io_count_ai_cont_rows[4].GetColumnByName("Non_Red_IS").Value
            except:
                self.gas_NRD = 0
            # AO
            try:
                self.type_uio_NRD = io_count_ao_cont_rows[0].GetColumnByName("Non_Red_IS").Value
            except:
                self.type_uio_NRD = 0
            # DO
            try:
                self.line_mon_uio_do_NRD = io_count_do_cont_rows[3].GetColumnByName("Non_Red_IS").Value
            except:
                self.line_mon_uio_do_NRD = 0
            try:
                self.dao_24vdc_500mA_NRD_IS = self.get_column_value(io_count_do_cont_rows[0], "Non_Red_IS")
            except:
                self.dao_24vdc_500mA_NRD_IS = 0
            # DI
            try:
                self.uio_di_NRD = io_count_di_cont_rows[0].GetColumnByName("Non_Red_IS)").Value
            except:
                self.uio_di_NRD = 0
            try:
               self.line_mon_uio_di_NRD = io_count_di_cont_rows[1].GetColumnByName("Non_Red_IS").Value
            except:
                self.line_mon_uio_di_NRD = 0
            # percent
            try:
                self.percent_spare_io_NRD = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("Percent_Installed_Spare_IOs").Value
            except:
                self.percent_spare_io_NRD =1
            #CXCPQ-30835
            #AI
            try:
                self.current_UIO_RD_IS = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName("Red (IS)").Value
            except:
                self.current_UIO_RD_IS=0
            try:
                self.fire2_RD_IS = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Red (IS)").Value
            except:
                self.fire2_RD_IS=0
            try:
                self.fire3and4_RD_IS = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName("Red (IS)").Value
            except:
                self.fire3and4_RD_IS=0
            try:
                self.gas_RD_IS = Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName("Red (IS)").Value
            except:
                self.gas_RD_IS=0
            #AO
            try:
                self.type_uio_NRD_IS = io_count_ao_cont_rows[0].GetColumnByName("Red (IS)").Value
            except:
                self.type_uio_NRD_IS=0
            #DI
            try:
                self.uio_di_RD_IS = io_count_di_cont_rows[0].GetColumnByName("Red (IS)").Value
            except:
                self.uio_di_RD_IS=0
            try:
                self.line_mon_uio_di_RD_IS = io_count_di_cont_rows[1].GetColumnByName("Red (IS)").Value
            except:
                self.line_mon_uio_di_RD_IS=0
            #DO
            try:
                self.uio_do_RD_IS = io_count_do_cont_rows[0].GetColumnByName("Red (IS)").Value
            except:
                self.uio_do_RD_IS=0
            try:
                self.line_mon_uio_do_RD_IS = io_count_do_cont_rows[1].GetColumnByName("Red (IS)").Value
            except:
                self.line_mon_uio_do_RD_IS=0
            #Percent
            try:
                self.percent_spare_io = Product.GetContainerByName('SM_RG_Universal_Marshalling_Cabinet_Details').Rows[0].GetColumnByName("Percentage of Spare Space").Value
            except:
                self.percent_spare_io = 0

            # CXCPQ-30846 (Red (IS))
		    # DO
            #self.dio_do_RD_IS = io_count_do_cont_rows[4].GetColumnByName("Red_IS").Value
            # DI
            #self.dio_di_RD_IS = io_count_di_cont_rows[3].GetColumnByName("Red_IS").Value
            #self.line_mon_dio_di_RD_IS = io_count_di_cont_rows[4].GetColumnByName("Red_IS").Value
            # percent
            #self.percent_spare_io = Product.GetContainerByName('SM_RG_Universal_Marshalling_Cabinet_Details').Rows[0].GetColumnByName("Percentage of Spare Space").Value

            #CXCPQ-30828(SUMUIONPF)
            #Remote Group
            try:
                self.di_sil2_val = str(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Non_Red_IS").Value)
            except:
                self.di_sil2_val = 0
            try:
                self.di_sil3_val = str(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[2].GetColumnByName("Non_Red_IS").Value)
            except:
                self.di_sil3_val = 0
            try:
                self.sai_pf_val = str(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Non_Red_IS").Value)
            except:
                self.sai_pf_val = 0
            try:
                self.sao_pf_val = str(Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows[1].GetColumnByName("Non_Red_IS").Value)
            except:
                self.sao_pf_val = 0
            try:
                self.sdo_sil3_val = str(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName("Non_Red_IS").Value)
            except:
                self.sdo_sil3_val = 0
            try:
                self.percent_spare_io = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_Percent_Installed_Spare_IO").Value
            except:
                self.percent_spare_io = 0
            #CXCPQ-31165(SUMRIONIS)
#Remote Group
            try:
                self.sai_current_uio_val = str(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[0].GetColumnByName("Non_Red_IS").Value)
            except:
                self.sai_current_uio_val = 0
            try:
                self.sai_fire2_val = str(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[1].GetColumnByName("Non_Red_IS").Value)
            except:
                self.sai_fire2_val = 0
            try:
                self.sai_fire34_val = str(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[2].GetColumnByName("Non_Red_IS").Value)
            except:
                self.sai_fire34_val = 0
            try:
                self.sai_fire34_sink_val = str(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[3].GetColumnByName("Non_Red_IS").Value)
            except:
                self.sai_fire34_sink_val = 0
            try:
                self.sai_gas_current_sink_uio_val = str(Product.GetContainerByName('SM_RG_IO_Count_Analog_Input_Cont').Rows[4].GetColumnByName("Non_Red_IS").Value)
            except:
                self.sai_gas_current_sink_uio_val = 0
            try:
                self.sao_uio_val = str(Product.GetContainerByName('SM_RG_IO_Count_Analog_Output_Cont').Rows[0].GetColumnByName("Non_Red_IS").Value)
            except:
                self.sao_uio_val = 0
            try:
                self.di_24v_uio_val = str(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[0].GetColumnByName("Non_Red_IS").Value)
            except:
                self.di_24v_uio_val = 0
            try:
                self.di_24v_linemon_uio_val = str(Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont').Rows[1].GetColumnByName("Non_Red_IS").Value)
            except:
                self.di_24v_linemon_uio_val = 0
            try:
                self.do_24v_uio_val = str(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[0].GetColumnByName("Non_Red_IS").Value)
            except:
                self.do_24v_uio_val = 0
            try:
                self.do_24v_linemon_uio_val = str(Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont').Rows[1].GetColumnByName("Non_Red_IS").Value)
            except:
                self.do_24v_linemon_uio_val = 0
            try:
                self.percent_spare_io = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_Percent_Installed_Spare_IO").Value
            except:
                self.percent_spare_io = 0