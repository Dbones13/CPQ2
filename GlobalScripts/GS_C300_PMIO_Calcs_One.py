#CXCPQ-44051
import System.Decimal as D
import GS_Get_Set_AtvQty
class IOComponents:
    def __init__(self, Product):
        self.Product = Product
        self.cont_col_mapping = dict()
        self.container_mapping = dict()
        if Product.Name == "Series-C Control Group":
            self.cont_col_mapping = {'C300_SerC_PointCount_PMIO_CG_Cont':'IO_Type'}
            self.container_mapping = {'Analog': 'C300_SerC_PointCount_PMIO_CG_Cont'}
        elif Product.Name == "Series-C Remote Group":
            self.cont_col_mapping = {'C300_SerC_PointCount_PMIO_RG_Cont':'IO_Type'}
            self.container_mapping = {'Analog': 'C300_SerC_PointCount_PMIO_RG_Cont'}

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
            container_mapping = {'PMIO STI (16) (0-5000)': 'C300_SerC_PointCount_PMIO_CG_Cont','PMIO STI Enhanced Power (16) (0-5000)': 'C300_SerC_PointCount_PMIO_CG_Cont','PMIO AO Active HART (0-5000)': 'C300_SerC_PointCount_PMIO_CG_Cont','PMIO HLAI (16) (0-5000)': 'C300_SerC_PointCount_PMIO_CG_Cont','PMIO HLAI Enhanced Power (16) (0-5000)': 'C300_SerC_PointCount_PMIO_CG_Cont','PMIO HLAI (16) w/ External HART Mux (0-5000)': 'C300_SerC_PointCount_PMIO_CG_Cont','PMIO HLAI Active HART (16) (0-5000)': 'C300_SerC_PointCount_PMIO_CG_Cont','PMIO LLAI (8) (0-5000)': 'C300_SerC_PointCount_PMIO_CG_Cont','PMIO AO HD (16) (0-5000)': 'C300_SerC_PointCount_PMIO_CG_Cont','PMIO AO HD w/ External HART Mux (16) (0-5000)': 'C300_SerC_PointCount_PMIO_CG_Cont','PMIO RHMUX (32)  w/NI Pwr Adptr (0-5000)': 'C300_SerC_PointCount_PMIO_CG_Cont','PMIO LLAI Mux PMIO Remote CJR (16) (0-5000)': 'C300_SerC_PointCount_PMIO_CG_Cont','PMIO LLAI Mux PMIO RTD (16) (0-5000)': 'C300_SerC_PointCount_PMIO_CG_Cont','PMIO LLAI Mux PMIO TC (16) (0-5000)': 'C300_SerC_PointCount_PMIO_CG_Cont'}
        if self.Product.Name == "Series-C Remote Group":
            container_mapping = {'PMIO STI (16) (0-5000)': 'C300_SerC_PointCount_PMIO_RG_Cont','PMIO STI Enhanced Power (16) (0-5000)': 'C300_SerC_PointCount_PMIO_RG_Cont','PMIO AO Active HART (0-5000)': 'C300_SerC_PointCount_PMIO_RG_Cont','PMIO HLAI (16) (0-5000)': 'C300_SerC_PointCount_PMIO_RG_Cont','PMIO HLAI Enhanced Power (16) (0-5000)': 'C300_SerC_PointCount_PMIO_RG_Cont','PMIO HLAI (16) w/ External HART Mux (0-5000)': 'C300_SerC_PointCount_PMIO_RG_Cont','PMIO HLAI Active HART (16) (0-5000)': 'C300_SerC_PointCount_PMIO_RG_Cont','PMIO LLAI (8) (0-5000)': 'C300_SerC_PointCount_PMIO_RG_Cont','PMIO AO HD (16) (0-5000)': 'C300_SerC_PointCount_PMIO_RG_Cont','PMIO AO HD w/ External HART Mux (16) (0-5000)': 'C300_SerC_PointCount_PMIO_RG_Cont','PMIO RHMUX (32)  w/NI Pwr Adptr (0-5000)': 'C300_SerC_PointCount_PMIO_RG_Cont','PMIO LLAI Mux PMIO Remote CJR (16) (0-5000)': 'C300_SerC_PointCount_PMIO_RG_Cont','PMIO LLAI Mux PMIO RTD (16) (0-5000)': 'C300_SerC_PointCount_PMIO_RG_Cont','PMIO LLAI Mux PMIO TC (16) (0-5000)': 'C300_SerC_PointCount_PMIO_RG_Cont'}
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

    def c300_PIMO(self):
        JA11=JB11=JC11=KB11=JA12=JB12=JC12=KB12=0
        NA11=NB11=NA12=NB12=0 #CXCPQ-53159
        AA11=AB11=AC11=AA12=AB12=AC12=DA11=DB11=DA12=DB12=BA11=BB11=BA12=BB12=0
        LA11=LB11=LA12=LB12=MA11=MB11=MA12=MB12=Y31=Y32=Y41=Y42=FC11=FC12=GC11=GC12=HC11=HC12=0
        X11=X12=X13=X22=X21=X41=X42=Y11=Y12=Y13=Y22=IC12=IC11=X93=X931=0
        Y51=Y52=CA11=CB11=CB11=CA12=CB12=CC12=CC11=X31=X32=X33=EC11=EC12=X53=X63=X73=X83=0
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
                JA111 = self.getrailvalue(['PMIO STI (16) (0-5000)'], ['Red_IS'])
                JA11=D.Ceiling(float(JA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("JA11 "+str(JA11))
                JB111 = self.getrailvalue(['PMIO STI (16) (0-5000)'], ['Future_Red_IS'])
                JB11=D.Ceiling(float(JB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("JB11 "+str(JB11))
                JC111 = self.getrailvalue(['PMIO STI (16) (0-5000)'], ['Non_Red_IS'])
                JC11=D.Ceiling(float(JC111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("JC11 "+str(JC11))
                KB111 = self.getrailvalue(['PMIO STI Enhanced Power (16) (0-5000)'], ['Future_Red_IS'])
                KB11=D.Ceiling(float(KB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("KB11 "+str(KB11))
                JA121 = self.getrailvalue(['PMIO STI (16) (0-5000)'], ['Red_NIS'])
                JA12=D.Ceiling(float(JA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("JA12 "+str(JA12))
                JB121 = self.getrailvalue(['PMIO STI (16) (0-5000)'], ['Future_Red_NIS'])
                JB12=D.Ceiling(float(JB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("JB12 "+str(JB12))
                JC121 = self.getrailvalue(['PMIO STI (16) (0-5000)'], ['Non_Red_NIS'])
                JC12=D.Ceiling(float(JC121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("JC12 "+str(JC12))
                KB121 = self.getrailvalue(['PMIO STI Enhanced Power (16) (0-5000)'], ['Future_Red_NIS'])
                KB12=D.Ceiling(float(KB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("KB12 "+str(KB12))

                #CXCPQ-53159
                NA111 = self.getrailvalue(['PMIO AO Active HART (0-5000)'], ['Red_IS'])
                NA11=D.Ceiling(float(NA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("NA11 "+str(NA11))
                NB111 = self.getrailvalue(['PMIO AO Active HART (0-5000)'], ['Future_Red_IS'])
                NB11=D.Ceiling(float(NB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("NB11 "+str(NB11))
                NA121 = self.getrailvalue(['PMIO AO Active HART (0-5000)'], ['Red_NIS'])
                NA12=D.Ceiling(float(NA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("NA12 "+str(NA12))
                NB121 = self.getrailvalue(['PMIO AO Active HART (0-5000)'], ['Future_Red_NIS'])
                NB12=D.Ceiling(float(NB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("NB12 "+str(NB12))

                #CXCPQ-52972
                AA111 = self.getrailvalue(['PMIO HLAI (16) (0-5000)'], ['Red_IS'])
                AA11=D.Ceiling(float(AA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(AA11)
                AB111 = self.getrailvalue(['PMIO HLAI (16) (0-5000)'], ['Future_Red_IS'])
                AB11=D.Ceiling(float(AB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(AB11)
                AC111 = self.getrailvalue(['PMIO HLAI (16) (0-5000)'], ['Non_Red_IS'])
                AC11=D.Ceiling(float(AC111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(AC11)
                AA121 = self.getrailvalue(['PMIO HLAI (16) (0-5000)'], ['Red_NIS'])
                AA12=D.Ceiling(float(AA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(AA12)
                AB121 = self.getrailvalue(['PMIO HLAI (16) (0-5000)'], ['Future_Red_NIS'])
                AB12=D.Ceiling(float(AB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(AB12)
                AC121 = self.getrailvalue(['PMIO HLAI (16) (0-5000)'], ['Non_Red_NIS'])
                AC12=D.Ceiling(float(AC121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(AC12)

                DA111 = self.getrailvalue(['PMIO HLAI Enhanced Power (16) (0-5000)'], ['Red_IS'])
                DA11=D.Ceiling(float(DA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(DA11)
                DB111 = self.getrailvalue(['PMIO HLAI Enhanced Power (16) (0-5000)'], ['Future_Red_IS'])
                DB11=D.Ceiling(float(DB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(DB11)
                DA121 = self.getrailvalue(['PMIO HLAI Enhanced Power (16) (0-5000)'], ['Red_NIS'])
                DA12=D.Ceiling(float(DA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(DA12)
                DB121 = self.getrailvalue(['PMIO HLAI Enhanced Power (16) (0-5000)'], ['Future_Red_NIS'])
                DB12=D.Ceiling(float(DB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(DB12)
                BA111 = self.getrailvalue(['PMIO HLAI (16) w/ External HART Mux (0-5000)'], ['Red_IS'])
                BA11=D.Ceiling(float(BA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(BA11)
                BB111 = self.getrailvalue(['PMIO HLAI (16) w/ External HART Mux (0-5000)'], ['Future_Red_IS'])
                BB11=D.Ceiling(float(BB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(BB11)
                BA121 = self.getrailvalue(['PMIO HLAI (16) w/ External HART Mux (0-5000)'], ['Red_NIS'])
                BA12=D.Ceiling(float(BA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(BA12)
                BB121 = self.getrailvalue(['PMIO HLAI (16) w/ External HART Mux (0-5000)'], ['Future_Red_NIS'])
                BB12=D.Ceiling(float(BB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(BB121)

                #CXCPQ-53013
                CA111 = self.getrailvalue(['PMIO HLAI Active HART (16) (0-5000)'], ['Red_IS'])
                CA11=D.Ceiling(float(CA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(CA11)
                CB111 = self.getrailvalue(['PMIO HLAI Active HART (16) (0-5000)'], ['Future_Red_IS'])
                CB11=D.Ceiling(float(CB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(CB11)
                CC111 = self.getrailvalue(['PMIO HLAI Active HART (16) (0-5000)'], ['Non_Red_IS'])
                CC11=D.Ceiling(float(CC111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(CC11)
                CA121 = self.getrailvalue(['PMIO HLAI Active HART (16) (0-5000)'], ['Red_NIS'])
                CA12=D.Ceiling(float(CA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(CA12)
                CB121 = self.getrailvalue(['PMIO HLAI Active HART (16) (0-5000)'], ['Future_Red_NIS'])
                CB12=D.Ceiling(float(CB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(CB12)
                CC121 = self.getrailvalue(['PMIO HLAI Active HART (16) (0-5000)'], ['Non_Red_NIS'])
                CC12=D.Ceiling(float(CC121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(CC12)

                #CXCPQ-53117
                EC111 = self.getrailvalue(['PMIO LLAI (8) (0-5000)'], ['Non_Red_IS'])
                EC11=D.Ceiling(float(EC111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(EC11)
                EC121 = self.getrailvalue(['PMIO LLAI (8) (0-5000)'], ['Non_Red_NIS'])
                EC12=D.Ceiling(float(EC121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(EC12)

                #CXCPQ-53129
                LA111 = self.getrailvalue(['PMIO AO HD (16) (0-5000)'], ['Red_IS'])
                LA11=D.Ceiling(float(LA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A"+str(LA11))
                LB111 = self.getrailvalue(['PMIO AO HD (16) (0-5000)'], ['Future_Red_IS'])
                LB11=D.Ceiling(float(LB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A1"+str(LB11))
                LA121 = self.getrailvalue(['PMIO AO HD (16) (0-5000)'], ['Red_NIS'])
                LA12=D.Ceiling(float(LA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A2"+str(LA12))
                LB121 = self.getrailvalue(['PMIO AO HD (16) (0-5000)'], ['Future_Red_NIS'])
                LB12=D.Ceiling(float(LB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A3"+str(LB12))
                MA111 = self.getrailvalue(['PMIO AO HD w/ External HART Mux (16) (0-5000)'], ['Red_IS'])
                MA11=D.Ceiling(float(MA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("B "+str(MA11))
                MB111 = self.getrailvalue(['PMIO AO HD w/ External HART Mux (16) (0-5000)'], ['Future_Red_IS'])
                MB11=D.Ceiling(float(MB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A1 "+str(MB11))
                MA121 = self.getrailvalue(['PMIO AO HD w/ External HART Mux (16) (0-5000)'], ['Red_NIS'])
                MA12=D.Ceiling(float(MA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A2 "+str(MA12))
                MB121 = self.getrailvalue(['PMIO AO HD w/ External HART Mux (16) (0-5000)'], ['Future_Red_NIS'])
                MB12=D.Ceiling(float(MB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A3 "+str(MB12))

                #CXCPQ-53122
                IC111 = self.getrailvalue(['PMIO RHMUX (32)  w/NI Pwr Adptr (0-5000)'], ['Non_Red_IS'])
                IC11=D.Ceiling(float(IC111)*(1+(Percent_Installed_Spare/100)))
                IC121 = self.getrailvalue(['PMIO RHMUX (32)  w/NI Pwr Adptr (0-5000)'], ['Non_Red_NIS'])
                IC12=D.Ceiling(float(IC121)*(1+(Percent_Installed_Spare/100)))
                X93 = D.Ceiling(IC11/32.0) + D.Ceiling(IC12/32.0)
                X931 = D.Ceiling(IC11/16.0) + D.Ceiling(IC12/16.0)
                
                #CXCPQ-53119
                FC111 = self.getrailvalue(['PMIO LLAI Mux PMIO Remote CJR (16) (0-5000)'], ['Non_Red_IS'])
                FC11=D.Ceiling(float(FC111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("FC11 "+str(FC11))
                FC121 = self.getrailvalue(['PMIO LLAI Mux PMIO Remote CJR (16) (0-5000)'], ['Non_Red_NIS'])
                FC12=D.Ceiling(float(FC121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("FC12 "+str(FC12))
                GC111 = self.getrailvalue(['PMIO LLAI Mux PMIO RTD (16) (0-5000)'], ['Non_Red_IS'])
                GC11=D.Ceiling(float(GC111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("GC11 "+str(GC11))
                GC121 = self.getrailvalue(['PMIO LLAI Mux PMIO RTD (16) (0-5000)'], ['Non_Red_NIS'])
                GC12=D.Ceiling(float(GC121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("GC12 "+str(GC12))
                HC111 = self.getrailvalue(['PMIO LLAI Mux PMIO TC (16) (0-5000)'], ['Non_Red_IS'])
                HC11=D.Ceiling(float(HC111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("HC11 "+str(HC11))
                HC121 = self.getrailvalue(['PMIO LLAI Mux PMIO TC (16) (0-5000)'], ['Non_Red_NIS'])
                HC12=D.Ceiling(float(HC121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("HC12 "+str(HC12))
                
                X63 = D.Ceiling(FC11/16.0) + D.Ceiling(FC12/16.0)
                Trace.Write("X63 "+str(X63))
                X73 = D.Ceiling(GC11/16.0) + D.Ceiling(GC12/16.0)
                Trace.Write("X73 "+str(X73))
                X83 = D.Ceiling(HC11/16.0) + D.Ceiling(HC12/16.0)
                Trace.Write("X83 "+str(X83))

                X11 = D.Ceiling(AA11/16.0) + D.Ceiling(AA12/16.0)
                X12 = D.Ceiling(AB11/16.0) + D.Ceiling(AB12/16.0)
                X13 = D.Ceiling(AC11/16.0) + D.Ceiling(AC12/16.0)
                X22 = D.Ceiling(BB11/16.0) + D.Ceiling(BB12/16.0)
                X21 = D.Ceiling(BA11/16.0) + D.Ceiling(BA12/16.0)
                X41 = D.Ceiling(DA11/16.0) + D.Ceiling(DA12/16.0)
                X42 = D.Ceiling(DB11/16.0) + D.Ceiling(DB12/16.0)
                Y11 = D.Ceiling(JA11/16.0) + D.Ceiling(JA12/16.0)
                Y12 = D.Ceiling(JB11/16.0) + D.Ceiling(JB12/16.0)
                Y13 = D.Ceiling(JC11/16.0) + D.Ceiling(JC12/16.0)
                Y22 = D.Ceiling(KB11/16.0) + D.Ceiling(KB12/16.0)

                Y31 = D.Ceiling(LA11/16.0) + D.Ceiling(LA12/16.0)
                Y32 = D.Ceiling(LB11/16.0) + D.Ceiling(LB12/16.0)
                Y41 = D.Ceiling(MA11/16.0) + D.Ceiling(MA12/16.0)
                Y42 = D.Ceiling(MB11/16.0) + D.Ceiling(MB12/16.0)

                Y51 = D.Ceiling(NA11/16.0) + D.Ceiling(NA12/16.0)
                Y52 = D.Ceiling(NB11/16.0) + D.Ceiling(NB12/16.0)
                X31 = D.Ceiling(CA11/16.0) + D.Ceiling(CA12/16.0)
                X32 = D.Ceiling(CB11/16.0) + D.Ceiling(CB12/16.0)
                X33 = D.Ceiling(CC11/16.0) + D.Ceiling(CC12/16.0)
                X53 = D.Ceiling(EC11/8.0) + D.Ceiling(EC12/8.0)
                #commented on 26/07/23
                """GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X63', X63)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X73', X73)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X83', X83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X11', X11)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X13', X13)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X12', X12)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X22', X22)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X21', X21)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X41', X41)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X42', X42)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y11', Y11)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y12', Y12)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y13', Y13)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y22', Y22)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y31', Y31)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y32', Y32)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y41', Y41)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y51', Y51)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y52', Y52)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X31', X31)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X32', X32)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X33', X33)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X53', X53)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y42', Y42)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X93', X93)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X931', X931)"""
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
                JA111 = self.getrailvalue(['PMIO STI (16) (0-5000)'], ['Red_IS'])
                JA11=D.Ceiling(float(JA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("JA11 "+str(JA11))
                JB111 = self.getrailvalue(['PMIO STI (16) (0-5000)'], ['Future_Red_IS'])
                JB11=D.Ceiling(float(JB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("JB11 "+str(JB11))
                JC111 = self.getrailvalue(['PMIO STI (16) (0-5000)'], ['Non_Red_IS'])
                JC11=D.Ceiling(float(JC111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("JC11 "+str(JC11))
                KB111 = self.getrailvalue(['PMIO STI Enhanced Power (16) (0-5000)'], ['Future_Red_IS'])
                KB11=D.Ceiling(float(KB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("KB11 "+str(KB11))
                JA121 = self.getrailvalue(['PMIO STI (16) (0-5000)'], ['Red_NIS'])
                JA12=D.Ceiling(float(JA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("JA12 "+str(JA12))
                JB121 = self.getrailvalue(['PMIO STI (16) (0-5000)'], ['Future_Red_NIS'])
                JB12=D.Ceiling(float(JB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("JB12 "+str(JB12))
                JC121 = self.getrailvalue(['PMIO STI (16) (0-5000)'], ['Non_Red_NIS'])
                JC12=D.Ceiling(float(JC121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("JC12 "+str(JC12))
                KB121 = self.getrailvalue(['PMIO STI Enhanced Power (16) (0-5000)'], ['Future_Red_NIS'])
                KB12=D.Ceiling(float(KB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("KB12 "+str(KB12))

                #CXCPQ-53159
                NA111 = self.getrailvalue(['PMIO AO Active HART (0-5000)'], ['Red_IS'])
                NA11=D.Ceiling(float(NA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("NA11 "+str(NA11))
                NB111 = self.getrailvalue(['PMIO AO Active HART (0-5000)'], ['Future_Red_IS'])
                NB11=D.Ceiling(float(NB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("NB11 "+str(NB11))
                NA121 = self.getrailvalue(['PMIO AO Active HART (0-5000)'], ['Red_NIS'])
                NA12=D.Ceiling(float(NA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("NA12 "+str(NA12))
                NB121 = self.getrailvalue(['PMIO AO Active HART (0-5000)'], ['Future_Red_NIS'])
                NB12=D.Ceiling(float(NB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("NB12 "+str(NB12))

                #CXCPQ-52972
                AA111 = self.getrailvalue(['PMIO HLAI (16) (0-5000)'], ['Red_IS'])
                AA11=D.Ceiling(float(AA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(AA11)
                AB111 = self.getrailvalue(['PMIO HLAI (16) (0-5000)'], ['Future_Red_IS'])
                AB11=D.Ceiling(float(AB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(AB11)
                AC111 = self.getrailvalue(['PMIO HLAI (16) (0-5000)'], ['Non_Red_IS'])
                AC11=D.Ceiling(float(AC111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(AC11)
                AA121 = self.getrailvalue(['PMIO HLAI (16) (0-5000)'], ['Red_NIS'])
                AA12=D.Ceiling(float(AA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(AA12)
                AB121 = self.getrailvalue(['PMIO HLAI (16) (0-5000)'], ['Future_Red_NIS'])
                AB12=D.Ceiling(float(AB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(AB12)
                AC121 = self.getrailvalue(['PMIO HLAI (16) (0-5000)'], ['Non_Red_NIS'])
                AC12=D.Ceiling(float(AC121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(AC12)

                DA111 = self.getrailvalue(['PMIO HLAI Enhanced Power (16) (0-5000)'], ['Red_IS'])
                DA11=D.Ceiling(float(DA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(DA11)
                DB111 = self.getrailvalue(['PMIO HLAI Enhanced Power (16) (0-5000)'], ['Future_Red_IS'])
                DB11=D.Ceiling(float(DB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(DB11)
                DA121 = self.getrailvalue(['PMIO HLAI Enhanced Power (16) (0-5000)'], ['Red_NIS'])
                DA12=D.Ceiling(float(DA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(DA12)
                DB121 = self.getrailvalue(['PMIO HLAI Enhanced Power (16) (0-5000)'], ['Future_Red_NIS'])
                DB12=D.Ceiling(float(DB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(DB12)
                BA111 = self.getrailvalue(['PMIO HLAI (16) w/ External HART Mux (0-5000)'], ['Red_IS'])
                BA11=D.Ceiling(float(BA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(BA11)
                BB111 = self.getrailvalue(['PMIO HLAI (16) w/ External HART Mux (0-5000)'], ['Future_Red_IS'])
                BB11=D.Ceiling(float(BB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(BB11)
                BA121 = self.getrailvalue(['PMIO HLAI (16) w/ External HART Mux (0-5000)'], ['Red_NIS'])
                BA12=D.Ceiling(float(BA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(BA12)
                BB121 = self.getrailvalue(['PMIO HLAI (16) w/ External HART Mux (0-5000)'], ['Future_Red_NIS'])
                BB12=D.Ceiling(float(BB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(BB121)

                #CXCPQ-53013
                CA111 = self.getrailvalue(['PMIO HLAI Active HART (16) (0-5000)'], ['Red_IS'])
                CA11=D.Ceiling(float(CA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(CA11)
                CB111 = self.getrailvalue(['PMIO HLAI Active HART (16) (0-5000)'], ['Future_Red_IS'])
                CB11=D.Ceiling(float(CB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(CB11)
                CC111 = self.getrailvalue(['PMIO HLAI Active HART (16) (0-5000)'], ['Non_Red_IS'])
                CC11=D.Ceiling(float(CC111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(CC11)
                CA121 = self.getrailvalue(['PMIO HLAI Active HART (16) (0-5000)'], ['Red_NIS'])
                CA12=D.Ceiling(float(CA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(CA12)
                CB121 = self.getrailvalue(['PMIO HLAI Active HART (16) (0-5000)'], ['Future_Red_NIS'])
                CB12=D.Ceiling(float(CB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(CB12)
                CC121 = self.getrailvalue(['PMIO HLAI Active HART (16) (0-5000)'], ['Non_Red_NIS'])
                CC12=D.Ceiling(float(CC121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write(CC12)

                #CXCPQ-53117
                EC111 = self.getrailvalue(['PMIO LLAI (8) (0-5000)'], ['Non_Red_IS'])
                EC11=D.Ceiling(float(EC111)*(1+(Percent_Installed_Spare/100)))
                EC121 = self.getrailvalue(['PMIO LLAI (8) (0-5000)'], ['Non_Red_NIS'])
                EC12=D.Ceiling(float(EC121)*(1+(Percent_Installed_Spare/100)))

                #CXCPQ-53129
                LA111 = self.getrailvalue(['PMIO AO HD (16) (0-5000)'], ['Red_IS'])
                LA11=D.Ceiling(float(LA111)*(1+(Percent_Installed_Spare/100)))
                LB111 = self.getrailvalue(['PMIO AO HD (16) (0-5000)'], ['Future_Red_IS'])
                LB11=D.Ceiling(float(LB111)*(1+(Percent_Installed_Spare/100)))
                LA121 = self.getrailvalue(['PMIO AO HD (16) (0-5000)'], ['Red_NIS'])
                LA12=D.Ceiling(float(LA121)*(1+(Percent_Installed_Spare/100)))
                LB121 = self.getrailvalue(['PMIO AO HD (16) (0-5000)'], ['Future_Red_NIS'])
                LB12=D.Ceiling(float(LB121)*(1+(Percent_Installed_Spare/100)))
                MA111 = self.getrailvalue(['PMIO AO HD w/ External HART Mux (16) (0-5000)'], ['Red_IS'])
                MA11=D.Ceiling(float(MA111)*(1+(Percent_Installed_Spare/100)))
                MB111 = self.getrailvalue(['PMIO AO HD w/ External HART Mux (16) (0-5000)'], ['Future_Red_IS'])
                MB11=D.Ceiling(float(MB111)*(1+(Percent_Installed_Spare/100)))
                MA121 = self.getrailvalue(['PMIO AO HD w/ External HART Mux (16) (0-5000)'], ['Red_NIS'])
                MA12=D.Ceiling(float(MA121)*(1+(Percent_Installed_Spare/100)))
                MB121 = self.getrailvalue(['PMIO AO HD w/ External HART Mux (16) (0-5000)'], ['Future_Red_NIS'])
                MB12=D.Ceiling(float(MB121)*(1+(Percent_Installed_Spare/100)))

                #CXCPQ-53122
                IC111 = self.getrailvalue(['PMIO RHMUX (32)  w/NI Pwr Adptr (0-5000)'], ['Non_Red_IS'])
                IC11=D.Ceiling(float(IC111)*(1+(Percent_Installed_Spare/100)))
                IC121 = self.getrailvalue(['PMIO RHMUX (32)  w/NI Pwr Adptr (0-5000)'], ['Non_Red_NIS'])
                IC12=D.Ceiling(float(IC121)*(1+(Percent_Installed_Spare/100)))
                X93 = D.Ceiling(IC11/32.0) + D.Ceiling(IC12/32.0)
                X931 = D.Ceiling(IC11/16.0) + D.Ceiling(IC12/16.0)
                
                #CXCPQ-53119
                FC111 = self.getrailvalue(['PMIO LLAI Mux PMIO Remote CJR (16) (0-5000)'], ['Non_Red_IS'])
                FC11=D.Ceiling(float(FC111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("FC11 "+str(FC11))
                FC121 = self.getrailvalue(['PMIO LLAI Mux PMIO Remote CJR (16) (0-5000)'], ['Non_Red_NIS'])
                FC12=D.Ceiling(float(FC121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("FC12 "+str(FC12))
                GC111 = self.getrailvalue(['PMIO LLAI Mux PMIO RTD (16) (0-5000)'], ['Non_Red_IS'])
                GC11=D.Ceiling(float(GC111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("GC11 "+str(GC11))
                GC121 = self.getrailvalue(['PMIO LLAI Mux PMIO RTD (16) (0-5000)'], ['Non_Red_NIS'])
                GC12=D.Ceiling(float(GC121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("GC12 "+str(GC12))
                HC111 = self.getrailvalue(['PMIO LLAI Mux PMIO TC (16) (0-5000)'], ['Non_Red_IS'])
                HC11=D.Ceiling(float(HC111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("HC11 "+str(HC11))
                HC121 = self.getrailvalue(['PMIO LLAI Mux PMIO TC (16) (0-5000)'], ['Non_Red_NIS'])
                HC12=D.Ceiling(float(HC121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("HC12 "+str(HC12))
                
                X63 = D.Ceiling(FC11/16.0) + D.Ceiling(FC12/16.0)
                Trace.Write("X63 "+str(X63))
                X73 = D.Ceiling(GC11/16.0) + D.Ceiling(GC12/16.0)
                Trace.Write("X73 "+str(X73))
                X83 = D.Ceiling(HC11/16.0) + D.Ceiling(HC12/16.0)
                Trace.Write("X83 "+str(X83))


                X11 = D.Ceiling(AA11/16.0) + D.Ceiling(AA12/16.0)
                X12 = D.Ceiling(AB11/16.0) + D.Ceiling(AB12/16.0)
                X13 = D.Ceiling(AC11/16.0) + D.Ceiling(AC12/16.0)
                X22 = D.Ceiling(BB11/16.0) + D.Ceiling(BB12/16.0)
                X21 = D.Ceiling(BA11/16.0) + D.Ceiling(BA12/16.0)
                X41 = D.Ceiling(DA11/16.0) + D.Ceiling(DA12/16.0)
                X42 = D.Ceiling(DB11/16.0) + D.Ceiling(DB12/16.0)
                Y11 = D.Ceiling(JA11/16.0) + D.Ceiling(JA12/16.0)
                Y12 = D.Ceiling(JB11/16.0) + D.Ceiling(JB12/16.0)
                Y13 = D.Ceiling(JC11/16.0) + D.Ceiling(JC12/16.0)
                Y22 = D.Ceiling(KB11/16.0) + D.Ceiling(KB12/16.0)

                Y31 = D.Ceiling(LA11/16.0) + D.Ceiling(LA12/16.0)
                Y32 = D.Ceiling(LB11/16.0) + D.Ceiling(LB12/16.0)
                Y41 = D.Ceiling(MA11/16.0) + D.Ceiling(MA12/16.0)
                Y42 = D.Ceiling(MB11/16.0) + D.Ceiling(MB12/16.0)

                Y51 = D.Ceiling(NA11/16.0) + D.Ceiling(NA12/16.0)
                Y52 = D.Ceiling(NB11/16.0) + D.Ceiling(NB12/16.0)
                X31 = D.Ceiling(CA11/16.0) + D.Ceiling(CA12/16.0)
                X32 = D.Ceiling(CB11/16.0) + D.Ceiling(CB12/16.0)
                X33 = D.Ceiling(CC11/16.0) + D.Ceiling(CC12/16.0)
                X53 = D.Ceiling(EC11/8.0) + D.Ceiling(EC12/8.0)
                #commented on 26/07/23
                """GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X63', X63)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X73', X73)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X83', X83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X11', X11)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X13', X13)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X12', X12)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X22', X22)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X21', X21)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X41', X41)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X42', X42)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y11', Y11)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y12', Y12)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y13', Y13)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y22', Y22)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y31', Y31)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y32', Y32)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y41', Y41)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y51', Y51)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y52', Y52)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X31', X31)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X32', X32)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X33', X33)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X53', X53)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y42', Y42)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X93', X93)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'X931', X931)
        return int(JA11),int(JB11),int(JC11),int(KB11),int(JA12),int(JB12),int(JC12),int(KB12),int(NA11),int(NB11),int(NA12),int(NB12),int(AA11),int(AB11),int(AC11),int(AA12),int(AB12),int(AC12),int(DA11),int(DB11),int(DA12),int(DB12),int(BA11),int(BB11),int(BA12),int(BB12),int(X11),int(X12),int(X13),int(X21),int(X22),int(Y51),int(Y52),int(X41),int(X42),int(Y11),int(Y12),int(Y13),int(Y22),int(CA11),int(CB11),int(CC11),int(CA12),int(CB12),int(CC12),int(X31),int(X32),int(X33),int(EC11),int(EC12),int(X53),int(Y31),int(Y32),int(Y41),int(Y42),int(LA11),int(LB11),int(LA12),int(LB12),int(MA11),int(MB11),int(MA12),int(MB12),int(IC11),int(IC12),int(X93),int(X931),int(FC11),int(FC12),int(GC11),int(GC12),int(HC11),int(HC12),int(X63),int(X73),int(X83)"""
        res = dict()
        for key in ['JA11','JB11','JC11','KB11','JA12','JB12','JC12','KB12','NA11','NB11','NA12','NB12','AA11','AB11','AC11','AA12','AB12','AC12','DA11','DB11','DA12','DB12','BA11','BB11','BA12','BB12','X11','X12','X13','X21','X22','Y51','Y52','X41','X42','Y11','Y12','Y13','Y22','CA11','CB11','CC11','CA12','CB12','CC12','X31','X32','X33','EC11','EC12','X53','Y31','Y32','Y41','Y42','LA11','LB11','LA12','LB12','MA11','MB11','MA12','MB12','IC11','IC12','X93','X931','FC11','FC12','GC11','GC12','HC11','HC12','X63','X73','X83']:
            res[key] = int(locals()[key])
        return res
#test = IOComponents(Product)
#val = test.c300_PIMO()
#Trace.Write(val)