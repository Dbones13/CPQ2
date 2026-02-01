#CXCPQ-40211
import System.Decimal as D
import GS_Get_Set_AtvQty
class IOComponents:
    def __init__(self, Product):
        self.Product  = Product
        self.cont_col_mapping = dict()
        self.container_mapping = dict()
        if Product.Name == "Series-C Remote Group":
            self.cont_col_mapping = {'C300_RAIL_Universal_IO_cont_RG_1':'IO_Type', 'C300_RAIL_Universal_io_RG_cont_2': 'IO_Type'}
            self.container_mapping = {'Analog': 'C300_RAIL_Universal_IO_cont_RG_1', 'Digital':'C300_RAIL_Universal_io_RG_cont_2'}

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
        if self.Product.Name == "Series-C Remote Group": 
            container_mapping = {'Series-C: UIO (32) Analog': 'C300_RAIL_Universal_IO_cont_RG_1', 'Series-C: UIO (32) Digita':'C300_RAIL_Universal_io_RG_cont_2'}
        if len(questions):
            for qn in questions:
                prefix = qn[0:25]
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

    def C300_Rail(self):
        AA61A=AA61=AA81A=AA81=AA91A=AA91=DD11A=DD11=BB61A=BB61=BB81A=BB81=BB91A=BB91=EE11A=EE11=CC61A=CC61=CC81A=CC81=CC91A=CC91=FF11A=FF11=0  #FOR IS
        AA62A=AA62=AA82A=AA82=AA92A=AA92=DD12A=DD12=BB62A=BB62=BB82A=BB82=BB92A=BB92=EE12A=EE12=CC62A=CC62=CC82A=CC82=CC92A=CC92=FF12A=FF12=0  #FOR NIS
        AA63A=AA63=AA83A=AA83=AA93A=AA93=DD13A=DD13=BB63A=BB63=BB83A=BB83=BB93A=BB93=EE13A=EE13=CC63A=CC63=CC83A=CC83=CC93A=CC93=FF13A=FF13=0  #FOR ISLTR
        AA64A=AA64=AA84A=AA84=AA94A=AA94=DD14A=DD14=BB64A=BB64=BB84A=BB84=BB94A=BB94=EE14A=EE14=CC64A=CC64=CC84A=CC84=CC94A=CC94=FF14A=FF14=0 #for RLy
        GG31=HH31=II31=GG41=HH41=II41=0 #for HvRLy
        XX61=XX62=XX63=XX71=XX72=XX73=XX81=XX82=XX83=0 #FOR MINMAX CALCS
        var1=var2=var3=var4=var5=var7=var8=var9=var10=var11=var6=var12=var13=var14=var15=var16=var17=var18=0 # cals var
        cal1=cal2=cal3=cal4=cal5=cal7=cal8=cal9=cal10=cal11=cal6=cal12=cal13=cal14=cal15=cal16=cal17=cal18=0 #calcs Var minmax
        MDUR18=MDUN12=TUIO11=TUIO01=Amp_A=0 # part qnt var
        questions = []
        column_name = ''
        if self.Product.Name == "Series-C Remote Group":
            Percent_Installed_Spare=float(self.Product.Attributes.GetByName("SerC_RG_Percent_Installed_Spare(0-100%)").GetValue()) if self.Product.Attributes.GetByName("SerC_RG_Percent_Installed_Spare(0-100%)").GetValue() !='' else 0.0
            Trace.Write('Percent_Installed_Spare'+str(Percent_Installed_Spare))
            Do_point= self.Product.Attr('General_Question_Average_current_DO').GetValue() if self.Product.Attr('General_Question_Average_current_DO').GetValue() !='' else 0
            Trace.Write("Do_point "+str(Do_point))
            try:
                family = self.Product.Attr('SerC_CG_IO_Family_Type').GetValue()
            except:
                family= 'No'
            if family=="Series C" and self.Product.Attr('SerC_IO_Mounting_Solution').GetValue() !="Universal Process Cab - 1.3M":
                ## Assigning user inputed value to pertivular veriable
                #A/D Part IS
                AA61A = self.getrailvalue(['Series-C: UIO (32) Analog Input (0-5000)'], ['Red_IS'])
                AA61=D.Ceiling(float(AA61A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA61A)
                AA81A= self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Red_IS'])
                AA81=D.Ceiling(float(AA81A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA81A)
                AA91A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Red_IS'])
                AA91=D.Ceiling(float(AA91A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA91A)
                DD11A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Red_IS'])
                DD11=D.Ceiling(float(DD11A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(DD11A)

                #B/E part IS
                BB61A = self.getrailvalue(['Series-C: UIO (32) Analog Input (0-5000)'], ['Future_Red_IS'])
                BB61=D.Ceiling(float(BB61A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB61A)
                BB81A = self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Future_Red_IS'])
                BB81=D.Ceiling(float(BB81A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB81A)
                BB91A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Future_Red_IS'])
                BB91=D.Ceiling(float(BB91A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB91A)
                EE11A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Future_Red_IS'])
                EE11=D.Ceiling(float(EE11A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(EE11A)

                #C/F  part IS
                CC61A = self.getrailvalue(['Series-C: UIO (32) Analog Input (0-5000)'], ['Non_Red_IS'])
                CC61=D.Ceiling(float(CC61A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC61A)
                CC81A= self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Non_Red_IS'])
                CC81=D.Ceiling(float(CC81A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC81A)
                CC91A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Non_Red_IS'])
                CC91=D.Ceiling(float(CC91A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC91A)
                FF11A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Non_Red_IS'])
                FF11=D.Ceiling(float(FF11A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(FF11A)

                ##NIS
                #A/D Part NIS
                AA62A = self.getrailvalue(['Series-C: UIO (32) Analog Input (0-5000)'], ['Red_NIS'])
                AA62=D.Ceiling(float(AA62A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA62A)
                AA82A = self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Red_NIS'])
                AA82=D.Ceiling(float(AA82A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA82A)
                AA92A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Red_NIS'])
                AA92=D.Ceiling(float(AA92A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA92A)
                DD12A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Red_NIS'])
                DD12=D.Ceiling(float(DD12A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(DD12A)

                #B/E part NIS
                BB62A = self.getrailvalue(['Series-C: UIO (32) Analog Input (0-5000)'], ['Future_Red_NIS'])
                BB62=D.Ceiling(float(BB62A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB62A)
                BB82A= self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Future_Red_NIS'])
                BB82=D.Ceiling(float(BB82A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB82A)
                BB92A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Future_Red_NIS'])
                BB92=D.Ceiling(float(BB92A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB92A)
                EE12A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Future_Red_NIS'])
                EE12=D.Ceiling(float(EE12A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(EE12A)

                #C/F part NIS
                CC62A = self.getrailvalue(['Series-C: UIO (32) Analog Input (0-5000)'], ['Non_Red_NIS'])
                CC62=D.Ceiling(float(CC62A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC62A)
                CC82A = self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Non_Red_NIS'])
                CC82=D.Ceiling(float(CC82A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC82A)
                CC92A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Non_Red_NIS'])
                CC92=D.Ceiling(float(CC92A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC92A)
                FF12A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Non_Red_NIS'])
                FF12=D.Ceiling(float(FF12A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(FF12A)

                ##ISLTR
                #A/D Part ISLTR
                AA63A = self.getrailvalue(['Series-C: UIO (32) Analog Input (0-5000)'], ['Red_ISLTR'])
                AA63=D.Ceiling(float(AA63A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA63A)
                AA83A= self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Red_ISLTR'])
                AA83=D.Ceiling(float(AA83A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA83A)
                AA93A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Red_ISLTR'])
                AA93=D.Ceiling(float(AA93A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA93A)
                DD13A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Red_ISLTR'])
                DD13=D.Ceiling(float(DD13A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(DD13A)

                #B/E Part ISLTR
                BB63A = self.getrailvalue(['Series-C: UIO (32) Analog Input (0-5000)'], ['Future_Red_ISLTR'])
                BB63=D.Ceiling(float(BB63A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB63A)
                BB83A = self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Future_Red_ISLTR'])
                BB83=D.Ceiling(float(BB83A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB83A)
                BB93A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Future_Red_ISLTR'])
                BB93=D.Ceiling(float(BB93A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB93A)
                EE13A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Future_Red_ISLTR'])
                EE13=D.Ceiling(float(EE13A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(EE13A)

                #C/F Part ISLTR
                CC63A = self.getrailvalue(['Series-C: UIO (32) Analog Input (0-5000)'], ['Non_Red_ISLTR'])
                CC63=D.Ceiling(float(CC63A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC63A)
                CC83A = self.getrailvalue(['Series-C: UIO (32) Analog Output (0-5000)'], ['Non_Red_ISLTR'])
                CC83=D.Ceiling(float(CC83A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC83A)
                CC93A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Non_Red_ISLTR'])
                CC93=D.Ceiling(float(CC93A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC93A)
                FF13A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Non_Red_ISLTR'])
                FF13=D.Ceiling(float(FF13A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(FF13A)

                #RLY only container
                #A/D part
                AA94A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Red_RLY'])
                AA94=D.Ceiling(float(AA94A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(AA94A)
                DD14A= self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Red_RLY'])
                DD14=D.Ceiling(float(DD14A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(DD14A)

                #B/E part
                BB94A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Future_Red_RLY'])
                BB94=D.Ceiling(float(BB94A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(BB94A)
                EE14A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Future_Red_RLY'])
                EE14=D.Ceiling(float(EE14A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(EE14A)

                #D/F part
                CC94A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Non_Red_RLY'])
                CC94=D.Ceiling(float(CC94A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(CC94A)
                FF14A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Non_Red_RLY'])
                FF14=D.Ceiling(float(FF14A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(FF14A)

                #HV RLY
                #G part Red
                GG31A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Red_HV_RLY'])
                GG31=D.Ceiling(float(GG31A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(GG31A)
                GG41A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Red_HV_RLY'])
                GG41=D.Ceiling(float(GG41A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(GG41A)
                
                #H part Future Red
                HH31A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Future_Red_HV_RLY'])
                HH31=D.Ceiling(float(HH31A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(HH31A)
                HH41A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Future_Red_HV_RLY'])
                HH41=D.Ceiling(float(HH41A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(HH41A)
                
                #I part Non Red
                II31A = self.getrailvalue(['Series-C: UIO (32) Digital Input (0-5000)'], ['Non_Red_HV_RLY'])
                II31=D.Ceiling(float(II31A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(II31A)
                II41A = self.getrailvalue(['Series-C: UIO (32) Digital Output (0-5000)'], ['Non_Red_HV_RLY'])
                II41=D.Ceiling(float(II41A)*(1+(Percent_Installed_Spare/100)))
                #Trace.Write(II41A)
                
                #calcs for min max
                # XX61 calcs
                var1 =(AA61+AA81+AA91)*25
                var2 =DD11* int(Do_point)
                cal1 =D.Ceiling((var1 + var2)/9600.0)
                cal2 =D.Ceiling((AA61+AA81+AA91+DD11)/32.0)
                XX61=max(cal1,cal2)
                # XX62 calcs
                var3=(AA62+AA82+AA92+AA94+GG31)*25
                var4=(DD12+DD14+GG41)* int(Do_point)
                cal3 = D.Ceiling((var3 + var4)/9600.0)
                cal4 = D.Ceiling ((AA62+AA82+AA92+AA94+DD12+DD14+GG31+GG41)/32.0)
                XX62= max(cal3,cal4)
                # XX63 calcs
                var5=(AA63+AA83+AA93)*25
                var6 =DD13* int(Do_point)
                cal5 =D.Ceiling((var5 + var6)/9600.0)
                cal6 =D.Ceiling((AA63+AA83+AA93+DD13)/32.0)
                XX63=max(cal5,cal6)
                # XX81 calcs
                var7=(CC61+CC81+CC91)*25
                var8=FF11* int(Do_point)
                cal7 = D.Ceiling((var7 + var8)/9600.0)
                cal8 = D.Ceiling ((CC61+CC81+CC91+FF11)/32.0)
                XX81= max(cal7,cal8)
                # XX82 calcs
                var9=(CC62+CC82+CC92+CC94+II31)*25
                var10=(FF12+FF14+II41)* int(Do_point)
                cal9 = D.Ceiling((var9 + var10)/9600.0)
                cal10 = D.Ceiling ((CC62+CC82+CC92+CC94+FF12+FF14+II31+II41)/32.0)
                XX82= max(cal9,cal10)
                # XX83 calcs
                var11=(CC63+CC83+CC93)*25
                var12=FF13* int(Do_point)
                cal11 = D.Ceiling((var11 + var12)/9600.0)
                cal12 = D.Ceiling ((CC63+CC83+CC93+FF13)/32.0)
                XX83= max(cal11,cal12)
                # XX71 calcs
                var13=(BB61+BB81+BB91)*25
                var14=EE11* int(Do_point)
                cal13= D.Ceiling((var13 + var14)/9600.0)
                cal14= D.Ceiling ((BB61+BB81+BB91+EE11)/32.0)
                XX71= max(cal13,cal14)
                # XX72 calcs
                var15=(BB62+BB82+BB92+BB94+HH31)*25
                var16=(EE12+EE14+HH41)* int(Do_point)
                cal15 = D.Ceiling((var15 + var16)/9600.0)
                cal16 = D.Ceiling ((BB62+BB82+BB92+EE12+EE14+BB94+HH31+HH41)/32.0)
                XX72= max(cal15,cal16)
                # XX73 calcs
                var17=(BB63+BB83+BB93)*25
                var18=EE13* int(Do_point)
                Trace.Write("var18 "+str(var18))
                Trace.Write("var17 "+str(var17))
                cal17 = D.Ceiling((var17 + var18)/9600.0)
                Trace.Write("calcs17 "+str(cal17))
                cal18 = D.Ceiling ((BB63+BB83+BB93+EE13)/32.0)
                Trace.Write("calcs18 "+str(cal18))
                XX73= max(cal17,cal18)
                Trace.Write("XX73 "+str(XX73))
                #Trace.Write("ab "+str(XX61))
                #Trace.Write("ab "+str(XX62))
                #Trace.Write("ab "+str(XX63))
                #Trace.Write("ab "+str(XX81))
                #Trace.Write("ab "+str(XX82))
                #Trace.Write("ab "+str(XX83))
                #Trace.Write("ab "+str(XX71))
                #Trace.Write("ab "+str(XX72))
                #Trace.Write("ab "+str(XX73))
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'XX61', XX61)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'XX62', XX62)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'XX63', XX63)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'XX81', XX81)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'XX82', XX82)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'XX83', XX83)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'XX71', XX71)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'XX72', XX72)
                GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'XX73', XX73)
                #Parts qnt calcs using above calcs
                Amp_A = D.Ceiling((var1+var2)/1000.0)+D.Ceiling((var3+var4)/1000.0)+D.Ceiling((var5+var6)/1000.0)+D.Ceiling((var7+var8)/1000.0)+D.Ceiling((var9+var10)/1000.0)+D.Ceiling((var11+var12)/1000.0)+D.Ceiling((var13+var14)/1000.0)+D.Ceiling((var15+var16)/1000.0)+D.Ceiling((var17+var18)/1000.0)
                MDUR18 = 2*(XX61+XX62+XX63)
                MDUN12 = XX71 + XX72 + XX73 + XX81 + XX82 + XX83
                TUIO11 = (XX61+XX62+XX63) + ( XX71+ XX72+ XX73)
                TUIO01 = XX81+ XX82+ XX83

        return MDUR18,MDUN12,TUIO11,TUIO01,Amp_A