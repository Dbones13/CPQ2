import System.Decimal as D
#CXCPQ-46092
def USCA_Calcs(Product):
    Is=['Series-C: HLAI (16) 4-20mA (0-5000)','Series-C: HLAI (16) HART Config/Status (0-5000)','Series-C: AO (16) (0-5000)','Series-C: AO (16) HART Config/Status (0-5000)','Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)','Series-C: UIO (32) Analog Output (0-5000)','Series-C: UIO (32) Digital Input (0-5000)','Series-C: UIO (32) Digital Output (0-5000)','Series-C: HLAI (16) with HART with differential inputs (0-5000)','Series-C: HLAI (16) without HART with differential inputs (0-5000)','Series-C: AO (16) HART (0-5000)','Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)','Series-C: DI (32) 24VDC SOE (0-5000)','Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)','Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)','Series-C: HLAI (13-16) with HART with differential inputs (0-5000)','Series-C: HLAI (13-16) without HART with differential inputs (0-5000)']
    NIs=['Series-C: HLAI (16) 4-20mA (0-5000)','Series-C: HLAI (16) HART Config/Status (0-5000)','Series-C: AO (16) (0-5000)','Series-C: AO (16) HART Config/Status (0-5000)','Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)','Series-C: UIO (32) Analog Output (0-5000)','Series-C: UIO (32) Digital Input (0-5000)','Series-C: UIO (32) Digital Output (0-5000)','Series-C: HLAI (16) with HART with differential inputs (0-5000)','Series-C: HLAI (16) without HART with differential inputs (0-5000)','Series-C: AO (16) HART (0-5000)','Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)','Series-C: DI (32) 24VDC SOE (0-5000)','Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)','Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)','Series-C: LLAI (16) (0-5000)','Series-C: UIO (32) Analog Input (LLAI Adapt) (0-5000)','Series-C: HLAI (13-16) with HART with differential inputs (0-5000)','Series-C: HLAI (13-16) without HART with differential inputs (0-5000)']
    HV=['Series-C: UIO (32) Digital Input (0-5000)','Series-C: UIO (32) Digital Output (0-5000)','Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)','Series-C: DI (32) 24VDC SOE (0-5000)','Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)','Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)']
    Sum1=Sum2=Sum3=Sum4=Sum5=Sum_Is=Sum_NIs=Sum_NIs1=Sum_Is1=Sum_HV=0
    Sum11=Sum22=Sum33=Sum44=Sum55=0
    mssum1=mssum2=mssum3=mssum4=mssum5=mssum6=mssum7=mssum8=mssum9=mssum10=mssum11=0
    un1sum1=un1sum2=un1sum3=un1sum4=un1sum5=un1sum6=un1sum7=un1sum8=un1sum9=un1sum10=un1sum11=0
    un2sum1=un2sum2=un2sum3=un2sum4=un2sum5=un2sum6=un2sum7=un2sum8=un2sum9=un2sum10=un2sum11=un2sum12=un2sum13=un2sum14=0
    en1sum1=en1sum2=en1sum3=en1sum4=en1sum5=en1sum6=en1sum7=en1sum8=en1sum9=en1sum10=en1sum11=0
    en2sum1=en2sum2=en2sum3=en2sum4=en2sum5=en2sum6=en2sum7=en2sum8=en2sum9=en2sum10=en2sum11=en2sum12=en2sum13=en2sum14=0
    mssum101=mssum22=mssum33=mssum44=mssum55=mssum66=mssum77=mssum88=mssum99=mssum010=mssum111=0
    un1sum101=un1sum22=un1sum33=un1sum44=un1sum55=un1sum66=un1sum77=un1sum88=un1sum99=un1sum010=un1sum111=0
    un2sum101=un2sum22=un2sum33=un2sum44=un2sum55=un2sum66=un2sum77=un2sum88=un2sum99=un2sum010=un2sum111=un2sum112=un2sum113=un2sum114=0
    en1sum101=en1sum22=en1sum33=en1sum44=en1sum55=en1sum66=en1sum77=en1sum88=en1sum99=en1sum010=en1sum111=0
    en2sum101=en2sum22=en2sum33=en2sum44=en2sum55=en2sum66=en2sum77=en2sum88=en2sum99=en2sum010=en2sum111=en2sum112=en2sum113=en2sum114=0
    if Product.Name=="Series-C Control Group":
        ab=Product.GetContainerByName('C300_C IO MS')
        bc=Product.GetContainerByName('C300_CG_Universal_IO_cont_1')
        cd=Product.GetContainerByName('C300_CG_Universal_IO_cont_2')
        de=Product.GetContainerByName('SerC_CG_Enhanced_Function_IO_Cont')
        ef=Product.GetContainerByName('SerC_CG_Enhanced_Function_IO_Cont2')
        per=int(Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue())/100.0 if Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue() !="" else 0
        percent_spare= int(Product.Attr('SerC_CG_Percentage_of_Spare_Space_required(0-100%)').GetValue())/100.0 if Product.Attr('SerC_CG_Percentage_of_Spare_Space_required(0-100%)').GetValue() !='' else 0
    elif Product.Name=="Series-C Remote Group":
        ab=Product.GetContainerByName('C300_C IO_RG MS')
        bc=Product.GetContainerByName('C300_RG_Universal_IO_cont_1')
        cd=Product.GetContainerByName('C300_RG_Universal_IO_cont_2')
        de=Product.GetContainerByName('SerC_RG_Enhanced_Function_IO_Cont')
        ef=Product.GetContainerByName('SerC_RG_Enhanced_Function_IO_Cont2')
        per=int(Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue())/100.0 if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue() !="" else 0
        percent_spare= int(Product.Attr('SeriesC_RG_Percentage').GetValue())/100.0 if Product.Attr('SeriesC_RG_Percentage').GetValue() !='' else 0
        
    if Product.Name=="Series-C Control Group" or Product.Name=="Series-C Remote Group":
        for row in ab.Rows:
            if row.GetColumnByName("IO_Type").Value in Is:
                #for Is Calcs
                Sum1 =int(row.GetColumnByName("Red_IS").Value) if row.GetColumnByName("Red_IS").Value !='' else 0
                Sum11 += D.Ceiling((Sum1/16.0)*(1+per))
                #for Non Is calcs
            if row.GetColumnByName("IO_Type").Value in NIs:
                mssum1 =int(row.GetColumnByName("Future_Red_IS").Value) if row.GetColumnByName("Future_Red_IS").Value !='' else 0
                mssum101 += D.Ceiling((mssum1/16.0)*(1+per))
                mssum2 =int(row.GetColumnByName("Non_Red_IS").Value) if row.GetColumnByName("Non_Red_IS").Value !='' else 0
                mssum22 += D.Ceiling((mssum2/16.0)*(1+per))
                mssum3 =int(row.GetColumnByName("Red_NIS").Value) if row.GetColumnByName("Red_NIS").Value !='' else 0
                mssum33 += D.Ceiling((mssum3/16.0)*(1+per))
                mssum4 =int(row.GetColumnByName("Future_Red_NIS").Value) if row.GetColumnByName("Future_Red_NIS").Value !='' else 0
                mssum44 += D.Ceiling((mssum4/16.0)*(1+per))
                mssum5 =int(row.GetColumnByName("Non_Red_NIS").Value) if row.GetColumnByName("Non_Red_NIS").Value !='' else 0
                mssum55 += D.Ceiling((mssum5/16.0)*(1+per))
                mssum6 =int(row.GetColumnByName("Red_ISLTR").Value) if row.GetColumnByName("Red_ISLTR").Value !='' else 0
                mssum66 += D.Ceiling((mssum6/16.0)*(1+per))
                mssum7 =int(row.GetColumnByName("Future_Red_ISLTR").Value) if row.GetColumnByName("Future_Red_ISLTR").Value !='' else 0
                mssum77 += D.Ceiling((mssum7/16.0)*(1+per))
                mssum8 =int(row.GetColumnByName("Non_Red_ISLTR").Value) if row.GetColumnByName("Non_Red_ISLTR").Value !='' else 0
                mssum88 += D.Ceiling((mssum8/16.0)*(1+per))
        for row1 in bc.Rows:
            if row1.GetColumnByName("IO_Type").Value in Is:
                Sum2 =int(row1.GetColumnByName("Red_IS").Value) if row1.GetColumnByName("Red_IS").Value !='' else 0
                Sum22 +=D.Ceiling((Sum2/16.0)*(1+per))
                #for Non Is calcs
            if row1.GetColumnByName("IO_Type").Value in NIs:
                un1sum1 =int(row1.GetColumnByName("Future_Red_IS").Value) if row1.GetColumnByName("Future_Red_IS").Value !='' else 0
                un1sum101 += D.Ceiling((un1sum1/16.0)*(1+per))
                un1sum2 =int(row1.GetColumnByName("Non_Red_IS").Value) if row1.GetColumnByName("Non_Red_IS").Value !='' else 0
                un1sum22 += D.Ceiling((un1sum2/16.0)*(1+per))
                un1sum3 =int(row1.GetColumnByName("Red_NIS").Value) if row1.GetColumnByName("Red_NIS").Value !='' else 0
                un1sum33 += D.Ceiling((un1sum3/16.0)*(1+per))
                un1sum4 =int(row1.GetColumnByName("Future_Red_NIS").Value) if row1.GetColumnByName("Future_Red_NIS").Value !='' else 0
                un1sum44 += D.Ceiling((un1sum4/16.0)*(1+per))
                un1sum5 =int(row1.GetColumnByName("Non_Red_NIS").Value) if row1.GetColumnByName("Non_Red_NIS").Value !='' else 0
                un1sum55 += D.Ceiling((un1sum5/16.0)*(1+per))
                un1sum6 =int(row1.GetColumnByName("Red_ISLTR").Value) if row1.GetColumnByName("Red_ISLTR").Value !='' else 0
                un1sum66 += D.Ceiling((un1sum6/16.0)*(1+per))
                un1sum7 =int(row1.GetColumnByName("Future_Red_ISLTR").Value) if row1.GetColumnByName("Future_Red_ISLTR").Value !='' else 0
                un1sum77 += D.Ceiling((un1sum7/16.0)*(1+per))
                un1sum8 =int(row1.GetColumnByName("Non_Red_ISLTR").Value) if row1.GetColumnByName("Non_Red_ISLTR").Value !='' else 0
                un1sum88 += D.Ceiling((un1sum8/16.0)*(1+per))
        for row2 in cd.Rows:
            if row2.GetColumnByName("IO_Type").Value in Is:
                Sum3 =int(row2.GetColumnByName("Red_IS").Value) if row2.GetColumnByName("Red_IS").Value !='' else 0
                Sum33 += D.Ceiling((Sum3/16.0)*(1+per))
                #Trace.Write(Sum11)
                #for Non Is calcs
            if row2.GetColumnByName("IO_Type").Value in NIs:
                un2sum1 =int(row2.GetColumnByName("Future_Red_IS").Value) if row2.GetColumnByName("Future_Red_IS").Value !='' else 0
                un2sum101 += D.Ceiling((un2sum1/16.0)*(1+per))
                un2sum2 =int(row2.GetColumnByName("Non_Red_IS").Value) if row2.GetColumnByName("Non_Red_IS").Value !='' else 0
                un2sum22 += D.Ceiling((un2sum2/16.0)*(1+per))
                un2sum3 =int(row2.GetColumnByName("Red_NIS").Value) if row2.GetColumnByName("Red_NIS").Value !='' else 0
                un2sum33 += D.Ceiling((un2sum3/16.0)*(1+per))
                un2sum4 =int(row2.GetColumnByName("Future_Red_NIS").Value) if row2.GetColumnByName("Future_Red_NIS").Value !='' else 0
                un2sum44 += D.Ceiling((un2sum4/16.0)*(1+per))
                un2sum5 =int(row2.GetColumnByName("Non_Red_NIS").Value) if row2.GetColumnByName("Non_Red_NIS").Value !='' else 0
                un2sum55 += D.Ceiling((un2sum5/16.0)*(1+per))
                un2sum6 =int(row2.GetColumnByName("Red_ISLTR").Value) if row2.GetColumnByName("Red_ISLTR").Value !='' else 0
                un2sum66 += D.Ceiling((un2sum6/16.0)*(1+per))
                un2sum7 =int(row2.GetColumnByName("Future_Red_ISLTR").Value) if row2.GetColumnByName("Future_Red_ISLTR").Value !='' else 0
                un2sum77 += D.Ceiling((un2sum7/16.0)*(1+per))
                un2sum8 =int(row2.GetColumnByName("Non_Red_ISLTR").Value) if row2.GetColumnByName("Non_Red_ISLTR").Value !='' else 0
                un2sum88 += D.Ceiling((un2sum8/16.0)*(1+per))
                un2sum9 =int(row2.GetColumnByName("Red_RLY").Value) if row2.GetColumnByName("Red_RLY").Value !='' else 0
                un2sum99 += D.Ceiling((un2sum9/16.0)*(1+per))
                un2sum10 =int(row2.GetColumnByName("Future_Red_RLY").Value) if row2.GetColumnByName("Future_Red_RLY").Value !='' else 0
                un2sum010 += D.Ceiling((un2sum10/16.0)*(1+per))
                un2sum11 =int(row2.GetColumnByName("Non_Red_RLY").Value) if row2.GetColumnByName("Non_Red_RLY").Value !='' else 0
                un2sum111 += D.Ceiling((un2sum11/16.0)*(1+per))
            if row2.GetColumnByName("IO_Type").Value in HV:
                #CXDEV-8785
                un2sum12 =int(row2.GetColumnByName("Red_HV_RLY").Value) if row2.GetColumnByName("Red_HV_RLY").Value !='' else 0
                un2sum112 += D.Ceiling((1+percent_spare)*D.Ceiling((un2sum12/16.0)*(1+per)))
                un2sum13 =int(row2.GetColumnByName("Future_Red_HV_RLY").Value) if row2.GetColumnByName("Future_Red_HV_RLY").Value !='' else 0
                un2sum113 += D.Ceiling((1+percent_spare)*D.Ceiling((un2sum13/16.0)*(1+per)))
                un2sum14 =int(row2.GetColumnByName("Non_Red_HV_RLY").Value) if row2.GetColumnByName("Non_Red_HV_RLY").Value !='' else 0
                un2sum114 += D.Ceiling((1+percent_spare)*D.Ceiling((un2sum14/16.0)*(1+per)))
        for row3 in de.Rows:
            if row3.GetColumnByName("IO_Type").Value in Is:
                Sum4 =int(row3.GetColumnByName("Red_IS").Value) if row3.GetColumnByName("Red_IS").Value !='' else 0
                Sum44 += D.Ceiling((Sum4/16.0)*(1+per))
                #Trace.Write(Sum11)
                #for Non Is calcs
            if row3.GetColumnByName("IO_Type").Value in NIs:
                en1sum1 =int(row3.GetColumnByName("Future_Red_IS").Value) if row3.GetColumnByName("Future_Red_IS").Value !='' else 0
                en1sum101 += D.Ceiling((en1sum1/16.0)*(1+per))
                en1sum2 =int(row3.GetColumnByName("Non_Red_IS").Value) if row3.GetColumnByName("Non_Red_IS").Value !='' else 0
                en1sum22 += D.Ceiling((en1sum2/16.0)*(1+per))
                en1sum3 =int(row3.GetColumnByName("Red_NIS").Value) if row3.GetColumnByName("Red_NIS").Value !='' else 0
                en1sum33 += D.Ceiling((en1sum3/16.0)*(1+per))
                en1sum4 =int(row3.GetColumnByName("Future_Red_NIS").Value) if row3.GetColumnByName("Future_Red_NIS").Value !='' else 0
                en1sum44 += D.Ceiling((en1sum4/16.0)*(1+per))
                en1sum5 =int(row3.GetColumnByName("Non_Red_NIS").Value) if row3.GetColumnByName("Non_Red_NIS").Value !='' else 0
                en1sum55 += D.Ceiling((en1sum5/16.0)*(1+per))
                en1sum6 =int(row3.GetColumnByName("Red_ISLTR").Value) if row3.GetColumnByName("Red_ISLTR").Value !='' else 0
                en1sum66 += D.Ceiling((en1sum6/16.0)*(1+per))
                en1sum7 =int(row3.GetColumnByName("Future_Red_ISLTR").Value) if row3.GetColumnByName("Future_Red_ISLTR").Value !='' else 0
                en1sum77 += D.Ceiling((en1sum7/16.0)*(1+per))
                en1sum8 =int(row3.GetColumnByName("Non_Red_ISLTR").Value) if row3.GetColumnByName("Non_Red_ISLTR").Value !='' else 0
                en1sum88 += D.Ceiling((en1sum8/16.0)*(1+per))
        for row4 in ef.Rows:
            if row4.GetColumnByName("IO_Type").Value in Is:
                Sum5 =int(row4.GetColumnByName("Red_IS").Value) if row4.GetColumnByName("Red_IS").Value !='' else 0
                Sum55 += D.Ceiling((Sum5/16.0)*(1+per))
                #Trace.Write(Sum55)
                #for Non Is calcs
            if row4.GetColumnByName("IO_Type").Value in NIs:
                en2sum1 =int(row4.GetColumnByName("Future_Red_IS").Value) if row4.GetColumnByName("Future_Red_IS").Value !='' else 0
                en2sum101 += D.Ceiling((en2sum1/16.0)*(1+per))
                en2sum2 =int(row4.GetColumnByName("Non_Red_IS").Value) if row4.GetColumnByName("Non_Red_IS").Value !='' else 0
                en2sum22 += D.Ceiling((en2sum2/16.0)*(1+per))
                en2sum3 =int(row4.GetColumnByName("Red_NIS").Value) if row4.GetColumnByName("Red_NIS").Value !='' else 0
                en2sum33 += D.Ceiling((en2sum3/16.0)*(1+per))
                en2sum4 =int(row4.GetColumnByName("Future_Red_NIS").Value) if row4.GetColumnByName("Future_Red_NIS").Value !='' else 0
                en2sum44 += D.Ceiling((en2sum4/16.0)*(1+per))
                en2sum5 =int(row4.GetColumnByName("Non_Red_NIS").Value) if row4.GetColumnByName("Non_Red_NIS").Value !='' else 0
                en2sum55 += D.Ceiling((en2sum5/16.0)*(1+per))
                en2sum6 =int(row4.GetColumnByName("Red_ISLTR").Value) if row4.GetColumnByName("Red_ISLTR").Value !='' else 0
                en2sum66 += D.Ceiling((en2sum6/16.0)*(1+per))
                en2sum7 =int(row4.GetColumnByName("Future_Red_ISLTR").Value) if row4.GetColumnByName("Future_Red_ISLTR").Value !='' else 0
                en2sum77 += D.Ceiling((en2sum7/16.0)*(1+per))
                en2sum8 =int(row4.GetColumnByName("Non_Red_ISLTR").Value) if row4.GetColumnByName("Non_Red_ISLTR").Value !='' else 0
                en2sum88 += D.Ceiling((en2sum8/16.0)*(1+per))
                en2sum9 =int(row4.GetColumnByName("Red_RLY").Value) if row4.GetColumnByName("Red_RLY").Value !='' else 0
                en2sum99 += D.Ceiling((en2sum9/16.0)*(1+per))
                en2sum10 =int(row4.GetColumnByName("Future_Red_RLY").Value) if row4.GetColumnByName("Future_Red_RLY").Value !='' else 0
                en2sum010 += D.Ceiling((en2sum10/16.0)*(1+per))
                en2sum11 =int(row4.GetColumnByName("Non_Red_RLY").Value) if row4.GetColumnByName("Non_Red_RLY").Value !='' else 0
                en2sum111 += D.Ceiling((en2sum11/16.0)*(1+per))
            if row4.GetColumnByName("IO_Type").Value in HV:
                #CXDEV-8785
                en2sum12 =int(row4.GetColumnByName("Red_HV_RLY").Value) if row4.GetColumnByName("Red_HV_RLY").Value !='' else 0
                en2sum112 += D.Ceiling((1+percent_spare)*D.Ceiling((en2sum12/16.0)*(1+per)))
                en2sum13 =int(row4.GetColumnByName("Future_Red_HV_RLY").Value) if row4.GetColumnByName("Future_Red_HV_RLY").Value !='' else 0
                en2sum113 += D.Ceiling((1+percent_spare)*D.Ceiling((en2sum13/16.0)*(1+per)))
                en2sum14 =int(row4.GetColumnByName("Non_Red_HV_RLY").Value) if row4.GetColumnByName("Non_Red_HV_RLY").Value !='' else 0
                en2sum114 += D.Ceiling((1+percent_spare)*D.Ceiling((en2sum14/16.0)*(1+per)))
        if Product.Name=="Series-C Control Group":
            if Product.Attr('SerC_CG_IO_Family_Type').GetValue()=="Series C" and Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').GetValue()=="Yes":
                percent= int(Product.Attr('SerC_CG_Percentage_of_Spare_Space_required(0-100%)').GetValue())/100.0 if Product.Attr('SerC_CG_Percentage_of_Spare_Space_required(0-100%)').GetValue() !='' else 0
                #Trace.Write("per Per " +str(percent))
                Sum_Is=D.Ceiling((1+percent)*(D.Ceiling((Sum11+Sum22+Sum33+Sum44+Sum55+mssum101+mssum22+un1sum101+un1sum22+un2sum101+un2sum22+en1sum101+en1sum22+en2sum101+en2sum22))))
                Sum_Is1=(D.Ceiling((Sum11+Sum22+Sum33+Sum44+Sum55+mssum101+mssum22+un1sum101+un1sum22+un2sum101+un2sum22+en1sum101+en1sum22+en2sum101+en2sum22)))
                Sum_NIs=D.Ceiling((1+percent)*D.Ceiling(mssum33+mssum44+mssum55+mssum66+mssum77+mssum88+un1sum33+un1sum44+un1sum55+un1sum66+un1sum77+un1sum88+un2sum33+un2sum44+un2sum55+un2sum66+un2sum77+un2sum88+un2sum99+un2sum010+un2sum111+en1sum33+en1sum44+en1sum55+en1sum66+en1sum77+en1sum88+en2sum33+en2sum44+en2sum55+en2sum66+en2sum77+en2sum88+en2sum99+en2sum010+en2sum111))
                Sum_NIs1=D.Ceiling(mssum33+mssum44+mssum55+mssum66+mssum77+mssum88+un1sum33+un1sum44+un1sum55+un1sum66+un1sum77+un1sum88+un2sum33+un2sum44+un2sum55+un2sum66+un2sum77+un2sum88+un2sum99+un2sum010+un2sum111+en1sum33+en1sum44+en1sum55+en1sum66+en1sum77+en1sum88+en2sum33+en2sum44+en2sum55+en2sum66+en2sum77+en2sum88+en2sum99+en2sum010+en2sum111)
                #CXDEV-8785
                Sum_HV= D.Ceiling(un2sum112+un2sum113+un2sum114+en2sum112+en2sum113+en2sum114)
        elif Product.Name=="Series-C Remote Group":
            if Product.Attr('SerC_CG_IO_Family_Type').GetValue()=="Series C" and Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue()=="Yes":
                percent= int(Product.Attr('SeriesC_RG_Percentage').GetValue())/100.0 if Product.Attr('SeriesC_RG_Percentage').GetValue() !='' else 0
                #Trace.Write("per Per " +str(percent))
                Sum_Is=D.Ceiling((1+percent)*(D.Ceiling((Sum11+Sum22+Sum33+Sum44+Sum55+mssum101+mssum22+un1sum101+un1sum22+un2sum101+un2sum22+en1sum101+en1sum22+en2sum101+en2sum22))))
                Sum_Is1=(D.Ceiling((Sum11+Sum22+Sum33+Sum44+Sum55+mssum101+mssum22+un1sum101+un1sum22+un2sum101+un2sum22+en1sum101+en1sum22+en2sum101+en2sum22)))
                Sum_NIs=D.Ceiling((1+percent)*D.Ceiling(mssum33+mssum44+mssum55+mssum66+mssum77+mssum88+un1sum33+un1sum44+un1sum55+un1sum66+un1sum77+un1sum88+un2sum33+un2sum44+un2sum55+un2sum66+un2sum77+un2sum88+un2sum99+un2sum010+un2sum111+en1sum33+en1sum44+en1sum55+en1sum66+en1sum77+en1sum88+en2sum33+en2sum44+en2sum55+en2sum66+en2sum77+en2sum88+en2sum99+en2sum010+en2sum111))
                Sum_NIs1=D.Ceiling(mssum33+mssum44+mssum55+mssum66+mssum77+mssum88+un1sum33+un1sum44+un1sum55+un1sum66+un1sum77+un1sum88+un2sum33+un2sum44+un2sum55+un2sum66+un2sum77+un2sum88+un2sum99+un2sum010+un2sum111+en1sum33+en1sum44+en1sum55+en1sum66+en1sum77+en1sum88+en2sum33+en2sum44+en2sum55+en2sum66+en2sum77+en2sum88+en2sum99+en2sum010+en2sum111)
                Sum_HV=D.Ceiling(un2sum112+un2sum113+un2sum114+en2sum112+en2sum113+en2sum114)
    return Sum_Is,Sum_NIs,Sum_Is1,Sum_NIs1,Sum_HV

def part_condition(Product):
    sic=sic1=sic2=sic3=sic4=sic5=sic6=sic7=0
    Sum_Is,Sum_NIs,Sum_Is1,Sum_NIs1,Sum_HV=USCA_Calcs(Product)
    if Product.Name=="Series-C Control Group":
        if Product.Attr('SerC_CG_IO_Family_Type').GetValue()=="Series C" and Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').GetValue()=="Yes":
            sic=Product.Attr('SerC_CG_SIC_Length_for_UMC').GetValue()
    elif Product.Name=="Series-C Remote Group":
        if Product.Attr('SerC_CG_IO_Family_Type').GetValue()=="Series C" and Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue()=="Yes":
            sic=Product.Attr('SeriesC_RG_SICLength').GetValue()
    if Product.Name=="Series-C Control Group" or Product.Name=="Series-C Remote Group":
        if sic=="1500MM":
            sic1=Sum_Is1+Sum_NIs1
        elif sic=="6000MM":
            sic2=Sum_Is1+Sum_NIs1
        elif sic=="10000MM":
            sic3=Sum_Is1+Sum_NIs1
        elif sic=="15000MM":
            sic4=Sum_Is1+Sum_NIs1
        elif sic=="20000MM":
            sic5=Sum_Is1+Sum_NIs1
        elif sic=="25000MM":
            sic6=Sum_Is1+Sum_NIs1
        elif sic=="30000MM":
            sic7=Sum_Is1+Sum_NIs1
    return sic,sic1,sic2,sic3,sic4,sic5,sic6,sic7
def UmcPart(Product):
    var1=var2=var3=var4=var5=var6=var7=var8=var9=var10=var11=var12=var13=var14=var15=var16=var17=var18=var19=var20=var21=var22=var23=var24=var25=var26=var27=var28=var29=var30=var31=var32=var36=var34=var35=var37=0
    Cabinet_Type=Universal_lay=Cabinet_Power=Mounting_Option="none"
    Sum_Is,Sum_NIs,Sum_Is1,Sum_NIs1,Sum_HV=USCA_Calcs(Product)
    if Product.Name=="Series-C Control Group":
        if Product.Attr('SerC_CG_IO_Family_Type').GetValue()=="Series C" and Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').GetValue()=="Yes":
            Cabinet_Type = Product.Attr('SerC_CG_Cabinet_Type').GetValue()
            Universal_lay = Product.Attr('SerC_CG_Universal_Marshaling_Cabinet_layout').GetValue()
            Cabinet_Power = Product.Attr('SerC_Cabinet_Power').GetValue()
            Mounting_Option = Product.Attr('SerC_CG_Mounting_Option').GetValue()
    elif Product.Name=="Series-C Remote Group":
        if Product.Attr('SerC_CG_IO_Family_Type').GetValue()=="Series C" and Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue()=="Yes":
            Cabinet_Type = Product.Attr('SeriesC_RG_CabinetType').GetValue()
            Universal_lay = Product.Attr('SeriesC_RG_UniversalMarshallingCL').GetValue()
            Cabinet_Power = Product.Attr('SeriesC_RG_CabinetPower').GetValue()
            Mounting_Option = Product.Attr('SeriesC_RG_MountingOption').GetValue()
    if Product.Name=="Series-C Control Group" or Product.Name=="Series-C Remote Group":
        #CXCPQ-47002
        if Cabinet_Type=="Dual Sided" and Universal_lay=="2 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Plate Mounting":
            var1=D.Ceiling(Sum_NIs/30.0)
            var2=D.Ceiling(Sum_Is/30.0)
        #CXCPQ-47013
        elif Cabinet_Type=="Single Sided" and Universal_lay=="2 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Bracket Mounting":
            var3=D.Ceiling(Sum_NIs/14.0)
            var4=D.Ceiling(Sum_Is/14.0)
        #CXCPQ-47000
        elif Cabinet_Type=="Dual Sided" and Universal_lay=="2 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Plate Mounting":
            var5=D.Ceiling(Sum_NIs/28.0)
            var6=D.Ceiling(Sum_Is/28.0)
        #CXCPQ-47005
        elif Cabinet_Type=="Single Sided" and Universal_lay=="3 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Bracket Mounting":
            var7=D.Ceiling(Sum_NIs/21.0)
            var8=D.Ceiling(Sum_Is/21.0)
        #CXCPQ-47012
        elif Cabinet_Type=="Single Sided" and Universal_lay=="2 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Plate Mounting":
            var9=D.Ceiling(Sum_NIs/14.0)
            var10=D.Ceiling(Sum_Is/14.0)
        #CXCPQ-46993
        elif Cabinet_Type=="Dual Sided" and Universal_lay=="3 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Bracket Mounting":
            var11=D.Ceiling(Sum_NIs/45.0)
            var12=D.Ceiling(Sum_Is/45.0)
        #CXCPQ-47001
        elif Cabinet_Type=="Dual Sided" and Universal_lay=="2 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Bracket Mounting":
            var13=D.Ceiling(Sum_NIs/28.0)
            var14=D.Ceiling(Sum_Is/28.0)
        #CXCPQ-47003
        elif Cabinet_Type=="Dual Sided" and Universal_lay=="2 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Bracket Mounting":
            var15=D.Ceiling(Sum_NIs/30.0)
            var16=D.Ceiling(Sum_Is/30.0)
        #CXCPQ-47006
        elif Cabinet_Type=="Single Sided" and Universal_lay=="2 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Plate Mounting":
            var17=D.Ceiling(Sum_NIs/12.0)
            var18=D.Ceiling(Sum_Is/12.0)
        #CXCPQ-46119
        elif Cabinet_Type=="Dual Sided" and Universal_lay=="3 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Bracket Mounting":
            var19=D.Ceiling(Sum_NIs/42.0)
            var20=D.Ceiling(Sum_Is/42.0)
        #CXCPQ-47011
        elif Cabinet_Type=="Single Sided" and Universal_lay=="2 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Bracket Mounting":
            var21=D.Ceiling(Sum_NIs/12.0)
            var22=D.Ceiling(Sum_Is/12.0)
        #CXCPQ-47004
        elif Cabinet_Type=="Single Sided" and Universal_lay=="3 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Bracket Mounting":
            var23=D.Ceiling(Sum_NIs/18.0)
            var24=D.Ceiling(Sum_Is/18.0)
        #CXDEV-8785
        if Cabinet_Type=="Dual Sided" and Universal_lay=="2 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Plate Mounting":
            var25=D.Ceiling(Sum_HV/24.0)
        #CXDEV-8786
        elif Cabinet_Type=="Dual Sided" and Universal_lay=="2 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Bracket Mounting":
            var26=D.Ceiling(Sum_HV/24.0)
        #CXDEV-8787
        elif Cabinet_Type=="Dual Sided" and Universal_lay=="3 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Bracket Mounting":
            var27=D.Ceiling(Sum_HV/36.0)
        #CXDEV-8788
        elif Cabinet_Type=="Dual Sided" and Universal_lay=="2 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Plate Mounting":
            var29=D.Ceiling(Sum_HV/26.0)
        #CXDEV-8789
        elif Cabinet_Type=="Dual Sided" and Universal_lay=="2 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Bracket Mounting":
            var28=D.Ceiling(Sum_HV/26.0)
        #CXDEV-8790
        elif Cabinet_Type=="Dual Sided" and Universal_lay=="3 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Bracket Mounting":
            var30=D.Ceiling(Sum_HV/39.0)
        #CXDEV-8791
        elif Cabinet_Type=="Single Sided" and Universal_lay=="2 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Plate Mounting":
            var31=D.Ceiling(Sum_HV/10.0)
        #CXDEV-8792
        elif Cabinet_Type=="Single Sided" and Universal_lay=="2 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Bracket Mounting":
            var32=D.Ceiling(Sum_HV/10.0)
        #CXDEV-8794
        elif Cabinet_Type=="Single Sided" and Universal_lay=="2 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Plate Mounting":
            var36=D.Ceiling(Sum_HV/12.0)
        #CXDEV-8795
        elif Cabinet_Type=="Single Sided" and Universal_lay=="2 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Bracket Mounting":
            var34=D.Ceiling(Sum_HV/12.0)
        #CXDEV-8796
        elif Cabinet_Type=="Single Sided" and Universal_lay=="3 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Bracket Mounting":
            var35=D.Ceiling(Sum_HV/18.0)
        #CXDEV-8793
        elif Cabinet_Type=="Single Sided" and Universal_lay=="3 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Bracket Mounting":
            var37=D.Ceiling(Sum_HV/15.0)
    return var1,var2,var3,var4,var5,var6,var7,var8,var9,var10,var11,var12,var13,var14,var15,var16,var17,var18,var19,var20,var21,var22,var23,var24,var25,var26,var27,var28,var29,var30,var31,var32,var36,var34,var35,var37
#var1,var2,var3,var4,var5,var6,var7,var8,var9,var10,var11,var12,var13,var14,var15,var16,var17,var18,var19,var20,var21,var22,var23,var24=UmcPart(Product)
#Trace.Write(var6)