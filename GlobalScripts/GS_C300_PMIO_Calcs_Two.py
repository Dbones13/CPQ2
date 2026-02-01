#CXCPQ-44051
import System.Decimal as D
import GS_Get_Set_AtvQty
class IOComponents:
    def __init__(self, Product):
        self.Product = Product
        self.cont_col_mapping = dict()
        self.container_mapping = dict()
        if Product.Name == "Series-C Control Group":
            self.cont_col_mapping = {'C300_SerC_PointCount_PMIO_CG_RlyCont':'IO_Type'}
            self.container_mapping = {'Analog': 'C300_SerC_PointCount_PMIO_CG_RlyCont'}
        elif Product.Name == "Series-C Remote Group":
            self.cont_col_mapping = {'C300_SerC_PointCount_PMIO_RG_RlyCont':'IO_Type'}
            self.container_mapping = {'Analog': 'C300_SerC_PointCount_PMIO_RG_RlyCont'}

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
            container_mapping = {'PMIO DI 24 HD VDC (32) (0-5000)': 'C300_SerC_PointCount_PMIO_CG_RlyCont','PMIO DO 24 VDC HD (32) (0-5000)': 'C300_SerC_PointCount_PMIO_CG_RlyCont','PMIO DO HD Relay (32) (0-5000)': 'C300_SerC_PointCount_PMIO_CG_RlyCont'}
        if self.Product.Name == "Series-C Remote Group":
            container_mapping = {'PMIO DI 24 HD VDC (32) (0-5000)': 'C300_SerC_PointCount_PMIO_RG_RlyCont','PMIO DO 24 VDC HD (32) (0-5000)': 'C300_SerC_PointCount_PMIO_RG_RlyCont','PMIO DO HD Relay (32) (0-5000)': 'C300_SerC_PointCount_PMIO_RG_RlyCont'}
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

    def c300_PIMO_RLY(self):
        PA11=PB11=PA12=PB12=0
        Y71=Y72=Z51=Z52=Z91=Z92=0
        WA11=WB11=WA12=WB12=0
        A111=B111=A112=B112=0
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
                PA111 = self.getrailvalue(['PMIO DI 24 HD VDC (32) (0-5000)'], ['Red_IS'])
                PA11=D.Ceiling(float(PA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("PA11 "+str(PA11))
                PB111 = self.getrailvalue(['PMIO DI 24 HD VDC (32) (0-5000)'], ['Future_Red_IS'])
                PB11=D.Ceiling(float(PB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("PB11 "+str(PB11))
                PA121 = self.getrailvalue(['PMIO DI 24 HD VDC (32) (0-5000)'], ['Red_NIS'])
                PA12=D.Ceiling(float(PA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("PA12 "+str(PA12))
                PB121 = self.getrailvalue(['PMIO DI 24 HD VDC (32) (0-5000)'], ['Future_Red_NIS'])
                PB12=D.Ceiling(float(PB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("PB12 "+str(PB12))
                
                WA111 = self.getrailvalue(['PMIO DO 24 VDC HD (32) (0-5000)'], ['Red_IS'])
                WA11=D.Ceiling(float(WA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("WA11 "+str(WA11))
                WB111 = self.getrailvalue(['PMIO DO 24 VDC HD (32) (0-5000)'], ['Future_Red_IS'])
                WB11=D.Ceiling(float(WB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("WB11 "+str(WB11))
                WA121 = self.getrailvalue(['PMIO DO 24 VDC HD (32) (0-5000)'], ['Red_NIS'])
                WA12=D.Ceiling(float(WA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("WA12 "+str(WA12))
                WB121 = self.getrailvalue(['PMIO DO 24 VDC HD (32) (0-5000)'], ['Future_Red_NIS'])
                WB12=D.Ceiling(float(WB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("WB12 "+str(WB12))

                #CXCPQ-53159
                A1111 = self.getrailvalue(['PMIO DO HD Relay (32) (0-5000)'], ['Red_IS'])
                A111=D.Ceiling(float(A1111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A111 "+str(A111))
                B1111 = self.getrailvalue(['PMIO DO HD Relay (32) (0-5000)'], ['Future_Red_IS'])
                B111=D.Ceiling(float(B1111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("B111 "+str(B111))
                A1121 = self.getrailvalue(['PMIO DO HD Relay (32) (0-5000)'], ['Red_NIS'])
                A112=D.Ceiling(float(A1121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A112 "+str(A112))
                B1121 = self.getrailvalue(['PMIO DO HD Relay (32) (0-5000)'], ['Future_Red_NIS'])
                B112=D.Ceiling(float(B1121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("B112 "+str(B112))

                Z51 = D.Ceiling(WA11/32.0) + D.Ceiling(WA12/32.0)
                Z52 = D.Ceiling(WB11/32.0) + D.Ceiling(WB12/32.0)
                Z91 = D.Ceiling(A111/32.0) + D.Ceiling(A112/32.0)
                Z92 = D.Ceiling(B111/32.0) + D.Ceiling(B112/32.0)
                Trace.Write('A'+str(Z51))
                Trace.Write('B'+str(Z52))
                Trace.Write('C'+str(Z91))
                Trace.Write('D'+str(Z92))

                Y71 = D.Ceiling(PA11/32.0) + D.Ceiling(PA12/32.0)
                Y72 = D.Ceiling(PB11/32.0) + D.Ceiling(PB12/32.0)
                Trace.Write('Y71 '+str(Y71))
                Trace.Write('Y72 '+str(Y72))
                #commented on 26/07/23
                """GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Z51', Z51)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Z52', Z52)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Z91', Z91)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Z92', Z92)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y71', Y71)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y72', Y72)"""
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
                PA111 = self.getrailvalue(['PMIO DI 24 HD VDC (32) (0-5000)'], ['Red_IS'])
                PA11=D.Ceiling(float(PA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("PA11 "+str(PA11))
                PB111 = self.getrailvalue(['PMIO DI 24 HD VDC (32) (0-5000)'], ['Future_Red_IS'])
                PB11=D.Ceiling(float(PB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("PB11 "+str(PB11))
                PA121 = self.getrailvalue(['PMIO DI 24 HD VDC (32) (0-5000)'], ['Red_NIS'])
                PA12=D.Ceiling(float(PA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("PA12 "+str(PA12))
                PB121 = self.getrailvalue(['PMIO DI 24 HD VDC (32) (0-5000)'], ['Future_Red_NIS'])
                PB12=D.Ceiling(float(PB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("PB12 "+str(PB12))
                
                WA111 = self.getrailvalue(['PMIO DO 24 VDC HD (32) (0-5000)'], ['Red_IS'])
                WA11=D.Ceiling(float(WA111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("WA11 "+str(WA11))
                WB111 = self.getrailvalue(['PMIO DO 24 VDC HD (32) (0-5000)'], ['Future_Red_IS'])
                WB11=D.Ceiling(float(WB111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("WB11 "+str(WB11))
                WA121 = self.getrailvalue(['PMIO DO 24 VDC HD (32) (0-5000)'], ['Red_NIS'])
                WA12=D.Ceiling(float(WA121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("WA12 "+str(WA12))
                WB121 = self.getrailvalue(['PMIO DO 24 VDC HD (32) (0-5000)'], ['Future_Red_NIS'])
                WB12=D.Ceiling(float(WB121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("WB12 "+str(WB12))

                #CXCPQ-53159
                A1111 = self.getrailvalue(['PMIO DO HD Relay (32) (0-5000)'], ['Red_IS'])
                A111=D.Ceiling(float(A1111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A111 "+str(A111))
                B1111 = self.getrailvalue(['PMIO DO HD Relay (32) (0-5000)'], ['Future_Red_IS'])
                B111=D.Ceiling(float(B1111)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("B111 "+str(B111))
                A1121 = self.getrailvalue(['PMIO DO HD Relay (32) (0-5000)'], ['Red_NIS'])
                A112=D.Ceiling(float(A1121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("A112 "+str(A112))
                B1121 = self.getrailvalue(['PMIO DO HD Relay (32) (0-5000)'], ['Future_Red_NIS'])
                B112=D.Ceiling(float(B1121)*(1+(Percent_Installed_Spare/100)))
                Trace.Write("B112 "+str(B112))

                Z51 = D.Ceiling(WA11/32.0) + D.Ceiling(WA12/32.0)
                Z52 = D.Ceiling(WB11/32.0) + D.Ceiling(WB12/32.0)
                Z91 = D.Ceiling(A111/32.0) + D.Ceiling(A112/32.0)
                Z92 = D.Ceiling(B111/32.0) + D.Ceiling(B112/32.0)
                Trace.Write('A'+str(Z51))
                Trace.Write('B'+str(Z52))
                Trace.Write('C'+str(Z91))
                Trace.Write('D'+str(Z92))

                Y71 = D.Ceiling(PA11/32.0) + D.Ceiling(PA12/32.0)
                Y72 = D.Ceiling(PB11/32.0) + D.Ceiling(PB12/32.0)
                Trace.Write('Y71 '+str(Y71))
                Trace.Write('Y72 '+str(Y72))
                #commented on 26/07/23
                """GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Z51', Z51)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Z52', Z52)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Z91', Z91)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Z92', Z92)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y71', Y71)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y72', Y72)
        return int(PA11),int(PB11),int(PA12),int(PB12),int(Y71),int(Y72),int(WA11),int(WB11),int(WA12),int(WB12),int(A111),int(B111),int(A112),int(B112),int(Z51),int(Z52),int(Z91),int(Z92)"""
        res = dict()
        for key in ['PA11','PB11','PA12','PB12','Y71','Y72','WA11','WB11','WA12','WB12','A111','B111','A112','B112','Z51','Z52','Z91','Z92']:
            res[key] = int(locals()[key])
        return res

#test = IOComponents(Product)
#val = test.c300_PIMO_RLY()
#Trace.Write(val)