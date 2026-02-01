#CXCPQ-44051
import System.Decimal as D
import GS_Get_Set_AtvQty
class IOComponents:
    def __init__(self, Product):
        self.Product = Product
        self.cont_col_mapping = dict()
        self.container_mapping = dict()
        if Product.Name == "Series-C Control Group":
            self.cont_col_mapping = {'C300_SerC_GIIS_PMIO_CG_Cont':'IO_Type'}
            self.container_mapping = {'Analog': 'C300_SerC_GIIS_PMIO_CG_Cont'}
        elif Product.Name == "Series-C Remote Group":
            self.cont_col_mapping = {'SerC_PMIO_CG_Group':'IO_Type'}
            self.container_mapping = {'Analog': 'SerC_PMIO_CG_Group'}

    def getRowIndex(self, container, column_name, column_value):
        row_index = -1
        for cont_row in container.Rows:
            if column_value == cont_row.GetColumnByName(column_name).Value:
                row_index = cont_row.RowIndex
                break
                #Trace.Write(row_index)
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
            #Trace.Write(str(e))
            return 0
        return val

    def getContainerNameByQuestion(self, ui_question):
        prefix = ui_question[0:7]
        try:
            return self.container_mapping[prefix]
        except Exception as e:
            return ''

    def getContainerNameByKeyword(self, keyword):
        try:
            return self.container_mapping[keyword]
        except Exception as e:
            #Trace.Write(str(e))
            return ''

    def getKeyColumnName(self, container):
        try:
            return self.cont_col_mapping[container]
        except Exception as e:
            #Trace.Write("{} {}".format(container, str(e)))
            return ''

    #Intermediate calculation for the C300 rail cont RG
    def getrailvalue(self,  questions, columns):
        QSN = 0
        container_mapping = {}
        if self.Product.Name == "Series-C Control Group":
            container_mapping = {'PMIO GI/IS STI Aux PMIO Current (16)  (0-5000)': 'C300_SerC_GIIS_PMIO_CG_Cont','PMIO GI/IS STI Aux PMIO Current External HART (16)  (0-5000)': 'C300_SerC_GIIS_PMIO_CG_Cont','PMIO GI/IS STI Aux & Hi V (16)  (0-5000)': 'C300_SerC_GIIS_PMIO_CG_Cont','PMIO HLAI (16) (0-5000)': 'C300_SerC_GIIS_PMIO_CG_Cont','PMIO HLAI Enhanced Power (16) (0-5000)': 'C300_SerC_GIIS_PMIO_CG_Cont','PMIO HLAI (16) w/ External HART Mux (0-5000)': 'C300_SerC_GIIS_PMIO_CG_Cont','PMIO GI/IS AO (16) Active HART  (0-5000)': 'C300_SerC_GIIS_PMIO_CG_Cont','PMIO GI/IS HLAI Aux PMIO Cur (16)  (0-5000)': 'C300_SerC_GIIS_PMIO_CG_Cont','PMIO GI/IS HLAI Aux PMIO Cur External HART (16)  (0-5000)': 'C300_SerC_GIIS_PMIO_CG_Cont','PMIO GI/IS HLAI Aux & Hi V (16)  (0-5000)': 'C300_SerC_GIIS_PMIO_CG_Cont','PMIO GI/IS DO (32) Via non red combine panel  (0-5000)': 'C300_SerC_GIIS_PMIO_CG_Cont','PMIO GI/IS HLAI Active HART Aux Current (16)  (0-5000)': 'C300_SerC_GIIS_PMIO_CG_Cont','PMIO GI/IS HLAI Active HART Aux & Hi V (16)  (0-5000)': 'C300_SerC_GIIS_PMIO_CG_Cont','PMIO GI/IS AO (16) External HART  (0-5000)': 'C300_SerC_GIIS_PMIO_CG_Cont'}
        if self.Product.Name == "Series-C Remote Group":
            container_mapping = {'PMIO GI/IS STI Aux PMIO Current (16)  (0-5000)': 'SerC_PMIO_CG_Group','PMIO GI/IS STI Aux PMIO Current External HART (16)  (0-5000)': 'SerC_PMIO_CG_Group','PMIO GI/IS STI Aux & Hi V (16)  (0-5000)': 'SerC_PMIO_CG_Group','PMIO HLAI (16) (0-5000)': 'SerC_PMIO_CG_Group','PMIO HLAI Enhanced Power (16) (0-5000)': 'SerC_PMIO_CG_Group','PMIO HLAI (16) w/ External HART Mux (0-5000)': 'SerC_PMIO_CG_Group','PMIO GI/IS AO (16) Active HART  (0-5000)': 'SerC_PMIO_CG_Group','PMIO GI/IS HLAI Aux PMIO Cur (16)  (0-5000)': 'SerC_PMIO_CG_Group','PMIO GI/IS HLAI Aux PMIO Cur External HART (16)  (0-5000)': 'SerC_PMIO_CG_Group','PMIO GI/IS HLAI Aux & Hi V (16)  (0-5000)': 'SerC_PMIO_CG_Group','PMIO GI/IS DO (32) Via non red combine panel  (0-5000)': 'SerC_PMIO_CG_Group','PMIO GI/IS HLAI Active HART Aux Current (16)  (0-5000)': 'SerC_PMIO_CG_Group','PMIO GI/IS HLAI Active HART Aux & Hi V (16)  (0-5000)': 'SerC_PMIO_CG_Group','PMIO GI/IS AO (16) External HART  (0-5000)': 'SerC_PMIO_CG_Group'}
        if len(questions):
            for qn in questions:
                prefix = qn[0:100]
                container_name = container_mapping[prefix]
                try:
                    container = self.Product.GetContainerByName(container_name)
                    #Trace.Write(container_name)
                    key_column_name = self.getKeyColumnName(container_name)
                    #Trace.Write(key_column_name)
                    row_index = self.getRowIndex(container, key_column_name, qn)
                    for column_name in columns:
                        QSN = self.getColumnValue(container, row_index, column_name)
                except Exception as e:
                    Trace.Write("{} is may not be visible".format(container_name))
                    Trace.Write(str(e))
        return QSN

    def SerC_PMIO_CG(self):
        A1811=C1811=A2011=C2011=A1911=B1911=0
        QX81=QX83=RX81=RX82=SX81=SX83=DX82=DX81=0
        A511=B511=A1611=C1611=A1711=C1711=0
        A1311=C1311=A1411=C1411=A1511=C1511=A411=B411=CX81=CX82=0
        NX83=LX81=LX83=MX81=MX83=NX81=OX81=OX83=PX81=PX83=CX82=0
        C1211=KX83=KX82=0
        questions = []
        column_name = ''
        if self.Product.Name == "Series-C Control Group":
            Percent_Installed_Spare=float(self.Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue()) if self.Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue() !='' else 0.0
            Trace.Write('Percent_Installed_Spare'+str(Percent_Installed_Spare))
            #Do_point = int(self.Product.Attr('General_Question_Average_current_DO').GetValue()) if self.Product.Attr('General_Question_Average_current_DO').GetValue() !='' else 0
            #Trace.Write("Do_point "+str(Do_point))
            SerC_CG_PM_IO_Solution_required=self.Product.Attr('SerC_CG_PM_IO_Solution_required').GetValue()
            Trace.Write("SerC_CG_PM_IO_Solution_required  "+str(SerC_CG_PM_IO_Solution_required))
            family = self.Product.Attr('SerC_CG_IO_Family_Type').GetValue()
            if family=="Series C" and SerC_CG_PM_IO_Solution_required=="Yes":
                ## UI Fields
                #Calculation of Part For first Row
                A18111 = self.getrailvalue(['PMIO GI/IS STI Aux PMIO Current (16)  (0-5000)'], ['Red_IS'])
                A1811=D.Ceiling(float(A18111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("18C11 "+str(A1811))
                C18111 = self.getrailvalue(['PMIO GI/IS STI Aux PMIO Current (16)  (0-5000)'], ['Non_Red_IS'])
                C1811=D.Ceiling(float(C18111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("18C11 "+str(C1811))
                A19111 = self.getrailvalue(['PMIO GI/IS STI Aux PMIO Current External HART (16)  (0-5000)'], ['Red_IS'])
                A1911=D.Ceiling(float(A19111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("19A11 "+str(A1911))
                B19111 = self.getrailvalue(['PMIO GI/IS STI Aux PMIO Current External HART (16)  (0-5000)'], ['Future_Red_IS'])
                B1911=D.Ceiling(float(B19111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("19B11 "+str(B1911))
                A20111 = self.getrailvalue(['PMIO GI/IS STI Aux & Hi V (16)  (0-5000)'], ['Red_IS'])
                A2011=D.Ceiling(float(A20111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("20A11 "+str(A2011))
                C20111 = self.getrailvalue(['PMIO GI/IS STI Aux & Hi V (16)  (0-5000)'], ['Non_Red_IS'])
                C2011=D.Ceiling(float(C20111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("20C11 "+str(C2011))

                #CXCPQ-53159
                A5111 = self.getrailvalue(['PMIO GI/IS AO (16) Active HART  (0-5000)'], ['Red_IS'])
                A511=D.Ceiling(float(A5111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A511 "+str(A511))
                B5111 = self.getrailvalue(['PMIO GI/IS AO (16) Active HART  (0-5000)'], ['Future_Red_IS'])
                B511=D.Ceiling(float(B5111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("B511 "+str(B511))

                #CXCPQ-52972
                A13111 = self.getrailvalue(['PMIO GI/IS HLAI Aux PMIO Cur (16)  (0-5000)'], ['Red_IS'])
                A1311=D.Ceiling(float(A13111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A1311 "+str(A1311))
                C13111 = self.getrailvalue(['PMIO GI/IS HLAI Aux PMIO Cur (16)  (0-5000)'], ['Non_Red_IS'])
                C1311=D.Ceiling(float(C13111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("C1311 "+str(C1311))
                A14111 = self.getrailvalue(['PMIO GI/IS HLAI Aux PMIO Cur External HART (16)  (0-5000)'], ['Red_IS'])
                A1411=D.Ceiling(float(A14111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A1411 "+str(A1411))
                C14111 = self.getrailvalue(['PMIO GI/IS HLAI Aux PMIO Cur External HART (16)  (0-5000)'], ['Non_Red_IS'])
                C1411=D.Ceiling(float(C14111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("C1411 "+str(C1411))
                A15111 = self.getrailvalue(['PMIO GI/IS HLAI Aux & Hi V (16)  (0-5000)'], ['Red_IS'])
                A1511=D.Ceiling(float(A15111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A1511 "+str(A1511))
                C15111 = self.getrailvalue(['PMIO GI/IS HLAI Aux & Hi V (16)  (0-5000)'], ['Non_Red_IS'])
                C1511=D.Ceiling(float(C15111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("C1511 "+str(C1511))

                #CXCPQ-52972
                C12111 = self.getrailvalue(['PMIO GI/IS DO (32) Via non red combine panel  (0-5000)'], ['Non_Red_IS'])
                C1211=D.Ceiling(float(C12111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(C1211)

                #CXCPQ-53013
                A16110 = self.getrailvalue(['PMIO GI/IS HLAI Active HART Aux Current (16)  (0-5000)'], ['Red_IS'])
                A1611=D.Ceiling(float(A16110)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A1611 "+str(A1611))
                C16111 = self.getrailvalue(['PMIO GI/IS HLAI Active HART Aux Current (16)  (0-5000)'], ['Non_Red_IS'])
                C1611=D.Ceiling(float(C16111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("C1611 "+str(C1611))

                A17111 = self.getrailvalue(['PMIO GI/IS HLAI Active HART Aux & Hi V (16)  (0-5000)'], ['Red_IS'])
                A1711=D.Ceiling(float(A17111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A1711 "+str(A1711))
                C17111 = self.getrailvalue(['PMIO GI/IS HLAI Active HART Aux & Hi V (16)  (0-5000)'], ['Non_Red_IS'])
                C1711=D.Ceiling(float(C17111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("C1711 "+str(C1711))
                
                #CXCPQ-53129
                A4111 = self.getrailvalue(['PMIO GI/IS AO (16) External HART  (0-5000)'], ['Red_IS'])
                A411=D.Ceiling(float(A4111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A411 "+str(A411))
                B4111 = self.getrailvalue(['PMIO GI/IS AO (16) External HART  (0-5000)'], ['Future_Red_IS'])
                B411=D.Ceiling(float(B4111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("B411 "+str(B411))

                CX81 = D.Ceiling(A411/16.0)
                CX82 = D.Ceiling(B411/16.0)
                Trace.Write('CX81 '+str(CX81))
                Trace.Write('CX82 '+str(CX82))
                QX81 = D.Ceiling(A1811/16.0)
                QX83 = D.Ceiling(C1811/16.0)
                RX81 = D.Ceiling(A1911/16.0)
                RX82 = D.Ceiling(B1911/16.0)
                SX81 = D.Ceiling(A2011/16.0)
                SX83 = D.Ceiling(C2011/16.0)
                LX81 = D.Ceiling(A1311/16.0)
                LX83 = D.Ceiling(C1311/16.0)
                MX81 = D.Ceiling(A1411/16.0)
                MX83 = D.Ceiling(C1411/16.0)
                NX81 = D.Ceiling(A1511/16.0)
                NX83 = D.Ceiling(C1511/16.0)
                OX81 = D.Ceiling(A1611/16.0)
                OX83 = D.Ceiling(C1611/16.0)
                PX81 = D.Ceiling(A1711/16.0)
                PX83 = D.Ceiling(C1711/16.0)
                DX81 = D.Ceiling(A511/16.0)
                DX82 = D.Ceiling(B511/16.0)
                KX83 = D.Ceiling(C1211/32.0)
                KX82 = D.Ceiling(C1211/16.0)
                #commented on 26/07/23
                """GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'CX82', CX82)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'DX82', DX82)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'LX83', LX83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'MX83', MX83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'NX83', NX83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'OX83', OX83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'PX83', PX83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'QX83', QX83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'RX82', RX82)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'SX83', SX83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'LX81', LX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'MX81', MX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'NX81', NX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'OX81', OX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'PX81', PX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'QX81', QX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'RX81', RX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'SX81', SX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'CX81', CX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'DX81', DX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'KX83', KX83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'KX82', KX82)"""

        elif self.Product.Name == "Series-C Remote Group":
            Percent_Installed_Spare=float(self.Product.Attributes.GetByName("SerC_RG_Percent_Installed_Spare(0-100%)").GetValue()) if self.Product.Attributes.GetByName("SerC_RG_Percent_Installed_Spare(0-100%)").GetValue() !='' else 0.0
            Trace.Write('Percent_Installed_Spare'+str(Percent_Installed_Spare))
            Do_point = int(self.Product.Attr('General_Question_Average_current_DO').GetValue()) if self.Product.Attr('General_Question_Average_current_DO').GetValue() !='' else 0
            Trace.Write('Do_point'+str(Do_point))
            SerC_RG_PM_IO_Solution_required=self.Product.Attr('SerC_CG_PM_IO_Solution_required').GetValue()
            Trace.Write("SerC_RG_PM_IO_Solution_required  "+str(SerC_RG_PM_IO_Solution_required))
            family = self.Product.Attr('SerC_CG_IO_Family_Type').GetValue()
            Trace.Write("family:"+str(family))
            if family=="Series C" and SerC_RG_PM_IO_Solution_required=="Yes":
                ## Assigning user inputed value to pertivular veriable
                ## UI Fields
                #Part IS
                A18111 = self.getrailvalue(['PMIO GI/IS STI Aux PMIO Current (16)  (0-5000)'], ['Red_IS'])
                A1811=D.Ceiling(float(A18111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("18C11 "+str(A1811))
                C18111 = self.getrailvalue(['PMIO GI/IS STI Aux PMIO Current (16)  (0-5000)'], ['Non_Red_IS'])
                C1811=D.Ceiling(float(C18111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("18C11 "+str(C1811))
                A19111 = self.getrailvalue(['PMIO GI/IS STI Aux PMIO Current External HART (16)  (0-5000)'], ['Red_IS'])
                A1911=D.Ceiling(float(A19111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("19A11 "+str(A1911))
                B19111 = self.getrailvalue(['PMIO GI/IS STI Aux PMIO Current External HART (16)  (0-5000)'], ['Future_Red_IS'])
                B1911=D.Ceiling(float(B19111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("19B11 "+str(B1911))
                A20111 = self.getrailvalue(['PMIO GI/IS STI Aux & Hi V (16)  (0-5000)'], ['Red_IS'])
                A2011=D.Ceiling(float(A20111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("20A11 "+str(A2011))
                C20111 = self.getrailvalue(['PMIO GI/IS STI Aux & Hi V (16)  (0-5000)'], ['Non_Red_IS'])
                C2011=D.Ceiling(float(C20111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("20C11 "+str(C2011))

                #CXCPQ-53159
                A5111 = self.getrailvalue(['PMIO GI/IS AO (16) Active HART  (0-5000)'], ['Red_IS'])
                A511=D.Ceiling(float(A5111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A511 "+str(A511))
                B5111 = self.getrailvalue(['PMIO GI/IS AO (16) Active HART  (0-5000)'], ['Future_Red_IS'])
                B511=D.Ceiling(float(B5111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("B511 "+str(B511))

                #CXCPQ-52972
                A13111 = self.getrailvalue(['PMIO GI/IS HLAI Aux PMIO Cur (16)  (0-5000)'], ['Red_IS'])
                A1311=D.Ceiling(float(A13111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A1311 "+str(A1311))
                C13111 = self.getrailvalue(['PMIO GI/IS HLAI Aux PMIO Cur (16)  (0-5000)'], ['Non_Red_IS'])
                C1311=D.Ceiling(float(C13111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("C1311 "+str(C1311))
                A14111 = self.getrailvalue(['PMIO GI/IS HLAI Aux PMIO Cur External HART (16)  (0-5000)'], ['Red_IS'])
                A1411=D.Ceiling(float(A14111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A1411 "+str(A1411))
                C14111 = self.getrailvalue(['PMIO GI/IS HLAI Aux PMIO Cur External HART (16)  (0-5000)'], ['Non_Red_IS'])
                C1411=D.Ceiling(float(C14111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("C1411 "+str(C1411))
                A15111 = self.getrailvalue(['PMIO GI/IS HLAI Aux & Hi V (16)  (0-5000)'], ['Red_IS'])
                A1511=D.Ceiling(float(A15111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A1511 "+str(A1511))
                C15111 = self.getrailvalue(['PMIO GI/IS HLAI Aux & Hi V (16)  (0-5000)'], ['Non_Red_IS'])
                C1511=D.Ceiling(float(C15111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("C1511 "+str(C1511))

                #CXCPQ-52972
                C12111 = self.getrailvalue(['PMIO GI/IS DO (32) Via non red combine panel  (0-5000)'], ['Non_Red_IS'])
                C1211=D.Ceiling(float(C12111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(C1211)
                
                #CXCPQ-53013
                A16110 = self.getrailvalue(['PMIO GI/IS HLAI Active HART Aux Current (16)  (0-5000)'], ['Red_IS'])
                A1611=D.Ceiling(float(A16110)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A1611 "+str(A1611))
                C16111 = self.getrailvalue(['PMIO GI/IS HLAI Active HART Aux Current (16)  (0-5000)'], ['Non_Red_IS'])
                C1611=D.Ceiling(float(C16111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("C1611 "+str(C1611))

                A17111 = self.getrailvalue(['PMIO GI/IS HLAI Active HART Aux & Hi V (16)  (0-5000)'], ['Red_IS'])
                A1711=D.Ceiling(float(A17111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A1711 "+str(A1711))
                C17111 = self.getrailvalue(['PMIO GI/IS HLAI Active HART Aux & Hi V (16)  (0-5000)'], ['Non_Red_IS'])
                C1711=D.Ceiling(float(C17111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("C1711 "+str(C1711))
                
                #CXCPQ-53129
                A4111 = self.getrailvalue(['PMIO GI/IS AO (16) External HART  (0-5000)'], ['Red_IS'])
                A411=D.Ceiling(float(A4111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A411 "+str(A411))
                B4111 = self.getrailvalue(['PMIO GI/IS AO (16) External HART  (0-5000)'], ['Future_Red_IS'])
                B411=D.Ceiling(float(B4111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("B411 "+str(B411))

                CX81 = D.Ceiling(A411/16.0)
                CX82 = D.Ceiling(B411/16.0)
                QX81 = D.Ceiling(A1811/16.0)
                QX83 = D.Ceiling(C1811/16.0)
                RX81 = D.Ceiling(A1911/16.0)
                RX82 = D.Ceiling(B1911/16.0)
                SX81 = D.Ceiling(A2011/16.0)
                SX83 = D.Ceiling(C2011/16.0)
                LX81 = D.Ceiling(A1311/16.0)
                LX83 = D.Ceiling(C1311/16.0)
                MX81 = D.Ceiling(A1411/16.0)
                MX83 = D.Ceiling(C1411/16.0)
                NX81 = D.Ceiling(A1511/16.0)
                NX83 = D.Ceiling(C1511/16.0)
                OX81 = D.Ceiling(A1611/16.0)
                OX83 = D.Ceiling(C1611/16.0)
                PX81 = D.Ceiling(A1711/16.0)
                PX83 = D.Ceiling(C1711/16.0)
                DX81 = D.Ceiling(A511/16.0)
                DX82 = D.Ceiling(B511/16.0)
                KX83 = D.Ceiling(C1211/32.0)
                KX82 = D.Ceiling(C1211/16.0)
                #commented on 26/07/23
                """GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'CX82', CX82)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'DX82', DX82)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'LX83', LX83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'MX83', MX83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'NX83', NX83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'OX83', OX83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'PX83', PX83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'QX83', QX83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'RX82', RX82)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'SX83', SX83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'LX81', LX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'MX81', MX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'NX81', NX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'OX81', OX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'PX81', PX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'QX81', QX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'RX81', RX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'SX81', SX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'CX81', CX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'DX81', DX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'KX83', KX83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'KX82', KX82)

        return int(A1811),int(C1811),int(A2011),int(C2011),int(A1911),int(B1911),int(A511),int(B511),int(QX81),int(QX83),int(RX81),int(RX82),int(SX81),int(SX83),int(DX82),int(DX81),int(A1311),int(C1311),int(A1411),int(C1411),int(A1511),int(C1511),int(NX83),int(LX81),int(LX83),int(MX81),int(MX83),int(NX81),int(C1211),int(KX83),int(KX82),int(A1611),int(C1611),int(A1711),int(C1711),int(OX81),int(OX83),int(PX81),int(PX83),int(A411),int(B411),int(CX81),int(CX82)"""
        res = dict()
        for key in ['A1811','C1811','A2011','C2011','A1911','B1911','A511','B511','QX81','QX83','RX81','RX82','SX81','SX83','DX82','DX81','A1311','C1311','A1411','C1411','A1511','C1511','NX83','LX81','LX83','MX81','MX83','NX81','C1211','KX83','KX82','A1611','C1611','A1711','C1711','OX81','OX83','PX81','PX83','A411','B411','CX81','CX82']:
            res[key] = int(locals()[key])
        return res

#test = IOComponents(Product)
#val = test.SerC_PMIO_CG()
#Trace.Write(val)