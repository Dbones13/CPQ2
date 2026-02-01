#CXCPQ-44150
import System.Decimal as D
import GS_Get_Set_AtvQty

class IOComponents:
    def __init__(self, Product):
        self.Product = Product
        self.cont_col_mapping = dict()
        self.container_mapping = dict()
        if Product.Name == "Series-C Control Group":
            self.cont_col_mapping = {'C300_C IO MS3':'IO_Type'}
            self.container_mapping = {'Analog': 'C300_C IO MS3'}
        elif Product.Name == "Series-C Remote Group":
            self.cont_col_mapping = {'C300_C IO_RG MS3':'IO_Type'}
            self.container_mapping = {'Analog': 'C300_C IO_RG MS3'}

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
            container_mapping = {'SCM: DO (32) 24VDC Bus External Power Supply (0-5000)': 'C300_C IO MS3','SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)': 'C300_C IO MS3'}
        if self.Product.Name == "Series-C Remote Group":
            container_mapping = {'SCM: DO (32) 24VDC Bus External Power Supply (0-5000)': 'C300_C IO_RG MS3','SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)': 'C300_C IO_RG MS3'}
        if len(questions):
            for qn in questions:
                prefix = qn[0:54]
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

    def C300_Mark2(self):
        M11=N11=O11=P11=Q11=R11=0  #FOR IS
        M12=N12=O12=P12=Q12=R12=0  #FOR NIS
        M13=N13=O13=P13=Q13=R13=0  #FOR ISLTR
        M14=N14=O14=P14=Q14=R14=0  #FOR RLY
        M15=N15=O15=P15=Q15=R15=0  #FOR HV RLY

        W31=W32=W33=W41=W42=W43=0 #FOR MINMAX CALCS
        PDOD51=TDOD61=TDOD51=0 # part qnt var
        questions = []
        column_name = ''
        if self.Product.Name == "Series-C Control Group":
            Percent_Installed_Spare=float(self.Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue()) if self.Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue() !='' else 0.0
            Trace.Write('Percent_Installed_Spare'+str(Percent_Installed_Spare))
            #Do_point = int(self.Product.Attr('General_Question_Average_current_DO').GetValue()) if self.Product.Attr('General_Question_Average_current_DO').GetValue() !='' else 0
            #Trace.Write("Do_point "+str(Do_point))
            try:
                family = self.Product.Attr('SerC_CG_IO_Family_Type').GetValue()
            except:
                family= 'No'
            if family=="Series-C Mark II":
                ## UI Fields
                #Calculation of Part For first Row
                MM11 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Red_IS'])
                M11=D.Ceiling(float(MM11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(M11)
                NN11 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Future_Red_IS'])
                N11=D.Ceiling(float(NN11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(N11)
                OO11 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Non_Red_IS'])
                O11=D.Ceiling(float(OO11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(O11)
                PP11 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Red_IS'])
                P11=D.Ceiling(float(PP11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(P11)
                QQ11 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Future_Red_IS'])
                Q11=D.Ceiling(float(QQ11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(Q11)
                #C/F  part IS
                RR11 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Non_Red_IS'])
                R11=D.Ceiling(float(RR11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(R11)

                MM12 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Red_NIS'])
                M12=D.Ceiling(float(MM12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(M12)
                NN12 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Future_Red_NIS'])
                N12=D.Ceiling(float(NN12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(N12)
                #C/F  part NIS
                OO12 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Non_Red_NIS'])
                O12=D.Ceiling(float(OO12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(O12)
                PP12 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Red_NIS'])
                P12=D.Ceiling(float(PP12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(P12)
                QQ12 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Future_Red_NIS'])
                Q12=D.Ceiling(float(QQ12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(Q12)
                #C/F  part NIS
                RR12 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Non_Red_NIS'])
                R12=D.Ceiling(float(RR12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(R12)

                MM13 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Red_ISLTR'])
                M13=D.Ceiling(float(MM13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(M13)
                NN13 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Future_Red_ISLTR'])
                N13=D.Ceiling(float(NN13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(N13)
                OO13 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Non_Red_ISLTR'])
                O13=D.Ceiling(float(OO13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(O13)
                PP13 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Red_ISLTR'])
                P13=D.Ceiling(float(PP13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(P13)
                QQ13 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Future_Red_ISLTR'])
                Q13=D.Ceiling(float(QQ13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(Q13)
                RR13 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Non_Red_ISLTR'])
                R13=D.Ceiling(float(RR13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(R13)

                MM14 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Red_RLY'])
                M14=D.Ceiling(float(MM14)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(M14)
                NN14 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Future_Red_RLY'])
                N14=D.Ceiling(float(NN14)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(N14)
                OO14 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Non_Red_RLY'])
                O14=D.Ceiling(float(OO14)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(O14)
                PP14 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Red_RLY'])
                P14=D.Ceiling(float(PP14)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(P14)
                QQ14 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Future_Red_RLY'])
                Q14=D.Ceiling(float(QQ14)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(Q14)
                RR14 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Non_Red_RLY'])
                R14=D.Ceiling(float(RR14)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(R14)

                MM15 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Red_HV_Rly'])
                M15=D.Ceiling(float(MM15)*(1+(Percent_Installed_Spare/100)))
                              
                NN15 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Future_HV_Rly'])
                N15=D.Ceiling(float(NN15)*(1+(Percent_Installed_Spare/100)))
                
                OO15 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Non_Red_HV_Rly'])
                O15=D.Ceiling(float(OO15)*(1+(Percent_Installed_Spare/100)))
                
                PP15 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Red_HV_Rly'])
                P15=D.Ceiling(float(PP15)*(1+(Percent_Installed_Spare/100)))
                              
                QQ15 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Future_HV_Rly'])
                Q15=D.Ceiling(float(QQ15)*(1+(Percent_Installed_Spare/100)))
                
                RR15 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Non_Red_HV_Rly'])
                R15=D.Ceiling(float(RR15)*(1+(Percent_Installed_Spare/100)))

                #calcs for min max
                W31 = D.Ceiling(M11/32.0) + D.Ceiling(M12/32.0) + D.Ceiling(M13/32.0) + D.Ceiling(M14/32.0) + D.Ceiling(M15/32.0)
                W32 = D.Ceiling(N11/32.0) + D.Ceiling(N12/32.0) + D.Ceiling(N13/32.0) + D.Ceiling(N14/32.0) + D.Ceiling(N15/32.0)
                W33 = D.Ceiling(O11/32.0) + D.Ceiling(O12/32.0) + D.Ceiling(O13/32.0) + D.Ceiling(O14/32.0) + D.Ceiling(O15/32.0)
                W41 = D.Ceiling(P11/32.0) + D.Ceiling(P12/32.0) + D.Ceiling(P13/32.0) + D.Ceiling(P14/32.0) + D.Ceiling(P15/32.0)
                W42 = D.Ceiling(Q11/32.0) + D.Ceiling(Q12/32.0) + D.Ceiling(Q13/32.0) + D.Ceiling(Q14/32.0) + D.Ceiling(Q15/32.0)
                W43 = D.Ceiling(R11/32.0) + D.Ceiling(R12/32.0) + D.Ceiling(R13/32.0) + D.Ceiling(R14/32.0) + D.Ceiling(R15/32.0)

                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'W31', W31)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'W32', W32)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'W33', W33)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'W41', W41)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'W42', W42)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'W43', W43)

                #Parts qnt calcs using above calcs
                PDOD51=2*(int(W31) + int(W41)) + int(W32) + int(W42) + int(W33) + int(W43)
                TDOD61=int(W31) + int(W32) +int(W41) + int(W42)
                TDOD51=int(W33) + int(W43)
        elif self.Product.Name == "Series-C Remote Group":
            Percent_Installed_Spare=float(self.Product.Attributes.GetByName("SerC_RG_Percent_Installed_Spare(0-100%)").GetValue()) if self.Product.Attributes.GetByName("SerC_RG_Percent_Installed_Spare(0-100%)").GetValue() !='' else 0.0
            Trace.Write('Percent_Installed_Spare'+str(Percent_Installed_Spare))
            Do_point = int(self.Product.Attr('General_Question_Average_current_DO').GetValue()) if self.Product.Attr('General_Question_Average_current_DO').GetValue() !='' else 0
            Trace.Write('Do_point'+str(Do_point))
            try:
                family = self.Product.Attr('SerC_CG_IO_Family_Type').GetValue()
            except:
                family= 'No'
            Trace.Write("family:"+str(family))
            if family=="Series-C Mark II":
                ## Assigning user inputed value to pertivular veriable
                ## UI Fields
                #Part IS
                MM11 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Red_IS'])
                M11=D.Ceiling(float(MM11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(M11)
                NN11 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Future_Red_IS'])
                N11=D.Ceiling(float(NN11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(N11)
                OO11 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Non_Red_IS'])
                O11=D.Ceiling(float(OO11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(O11)
                PP11 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Red_IS'])
                P11=D.Ceiling(float(PP11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(P11)
                QQ11 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Future_Red_IS'])
                Q11=D.Ceiling(float(QQ11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(Q11)
                #C/F  part IS
                RR11 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Non_Red_IS'])
                R11=D.Ceiling(float(RR11)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(R11)

                MM12 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Red_NIS'])
                M12=D.Ceiling(float(MM12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(M12)
                NN12 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Future_Red_NIS'])
                N12=D.Ceiling(float(NN12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(N12)
                #C/F  part NIS
                OO12 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Non_Red_NIS'])
                O12=D.Ceiling(float(OO12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(O12)
                PP12 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Red_NIS'])
                P12=D.Ceiling(float(PP12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(P12)
                QQ12 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Future_Red_NIS'])
                Q12=D.Ceiling(float(QQ12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(Q12)
                #C/F  part NIS
                RR12 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Non_Red_NIS'])
                R12=D.Ceiling(float(RR12)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(R12)

                MM13 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Red_ISLTR'])
                M13=D.Ceiling(float(MM13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(M13)
                NN13 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Future_Red_ISLTR'])
                N13=D.Ceiling(float(NN13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(N13)
                OO13 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Non_Red_ISLTR'])
                O13=D.Ceiling(float(OO13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(O13)
                PP13 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Red_ISLTR'])
                P13=D.Ceiling(float(PP13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(P13)
                QQ13 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Future_Red_ISLTR'])
                Q13=D.Ceiling(float(QQ13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(Q13)
                RR13 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Non_Red_ISLTR'])
                R13=D.Ceiling(float(RR13)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(R13)

                MM14 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Red_RLY'])
                M14=D.Ceiling(float(MM14)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(M14)
                NN14 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Future_Red_RLY'])
                N14=D.Ceiling(float(NN14)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(N14)
                OO14 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Non_Red_RLY'])
                O14=D.Ceiling(float(OO14)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(O14)
                PP14 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Red_RLY'])
                P14=D.Ceiling(float(PP14)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(P14)
                QQ14 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Future_Red_RLY'])
                Q14=D.Ceiling(float(QQ14)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(Q14)
                RR14 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Non_Red_RLY'])
                R14=D.Ceiling(float(RR14)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(R14)
                
                MM15 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Red_HV_Rly'])
                M15=D.Ceiling(float(MM15)*(1+(Percent_Installed_Spare/100)))
                              
                NN15 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Future_HV_Rly'])
                N15=D.Ceiling(float(NN15)*(1+(Percent_Installed_Spare/100)))
                
                OO15 = self.getrailvalue(['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)'], ['Non_Red_HV_Rly'])
                O15=D.Ceiling(float(OO15)*(1+(Percent_Installed_Spare/100)))
                
                PP15 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Red_HV_Rly'])
                P15=D.Ceiling(float(PP15)*(1+(Percent_Installed_Spare/100)))
                              
                QQ15 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Future_HV_Rly'])
                Q15=D.Ceiling(float(QQ15)*(1+(Percent_Installed_Spare/100)))
                
                RR15 = self.getrailvalue(['SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'], ['Non_Red_HV_Rly'])
                R15=D.Ceiling(float(RR15)*(1+(Percent_Installed_Spare/100)))
                

                #calcs for min max
                W31 = D.Ceiling(M11/32.0) + D.Ceiling(M12/32.0) + D.Ceiling(M13/32.0) + D.Ceiling(M14/32.0) + D.Ceiling(M15/32.0)
                W32 = D.Ceiling(N11/32.0) + D.Ceiling(N12/32.0) + D.Ceiling(N13/32.0) + D.Ceiling(N14/32.0) + D.Ceiling(N15/32.0)
                W33 = D.Ceiling(O11/32.0) + D.Ceiling(O12/32.0) + D.Ceiling(O13/32.0) + D.Ceiling(O14/32.0) + D.Ceiling(O15/32.0)
                W41 = D.Ceiling(P11/32.0) + D.Ceiling(P12/32.0) + D.Ceiling(P13/32.0) + D.Ceiling(P14/32.0) + D.Ceiling(P15/32.0)
                W42 = D.Ceiling(Q11/32.0) + D.Ceiling(Q12/32.0) + D.Ceiling(Q13/32.0) + D.Ceiling(Q14/32.0) + D.Ceiling(Q15/32.0)
                W43 = D.Ceiling(R11/32.0) + D.Ceiling(R12/32.0) + D.Ceiling(R13/32.0) + D.Ceiling(R14/32.0) + D.Ceiling(R15/32.0)

                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'W31', W31)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'W32', W32)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'W33', W33)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'W41', W41)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'W42', W42)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'W43', W43)

                #Parts qnt calcs using above calcs
                PDOD51=2*(int(W31) + int(W41)) + int(W32) + int(W42) + int(W33) + int(W43)
                TDOD61=int(W31) + int(W32) +int(W41) + int(W42)
                TDOD51=int(W33) + int(W43)
        return int(PDOD51),int(TDOD61),int(TDOD51)
#test = IOComponents(Product)
#val = test.C300_Mark2()
#Trace.Write(val)