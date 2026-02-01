import System.Decimal as D
#CXCPQ-51523 This 
def USCA_Calcs1(Product):
	Is=['SCM: HLAI (16) 4-20mA (0-5000)','SCM: HLAI (16) HART Config/Status (0-5000)','SCM: UIO (32) Analog Input (HLAI Adapt) (0-5000)','SCM: HLAI (16) with HART with differential inputs (0-5000)','SCM: HLAI (16) without HART with differential inputs (0-5000)','SCM: AO (16) (0-5000)','SCM: AO (16) HART Config/Status (0-5000)','SCM: UIO (32) Analog Output (0-5000)','SCM: AO (16) HART (0-5000)','SCM: DI (32) 24VDC (0-5000)','SCM: DI (32) 24VDC SOE (0-5000)','SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)','SCM: UIO (32) Digital Input (0-5000)','SCM: UIO (32) Digital Output (0-5000)','SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)','SCM: HLAI (13-16) differential inputs (0-5000)']
	NIs=['SCM: HLAI (16) 4-20mA (0-5000)','SCM: HLAI (16) HART Config/Status (0-5000)','SCM: AO (16) (0-5000)','SCM: AO (16) HART Config/Status (0-5000)','SCM: LLAI (16) (0-5000)','SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)','SCM: UIO (32) Analog Input (HLAI Adapt) (0-5000)','SCM: UIO (32) Analog Output (0-5000)','SCM: UIO (32) Digital Input (0-5000)','SCM: UIO (32) Digital Output (0-5000)','SCM: HLAI (16) with HART with differential inputs (0-5000)','SCM: HLAI (16) without HART with differential inputs (0-5000)','SCM: AO (16) HART (0-5000)','SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)','SCM: DI (32) 24VDC (0-5000)','SCM: DI (32) 24VDC SOE (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)','SCM: HLAI (13-16) differential inputs (0-5000)']
	Sum1=Sum2=Sum3=Sum4=Sum5=Sum6=Sum_IsM=Sum_Is1M=Sum_NIsM=Sum_NIs1M=0
	Sum11=Sum22=Sum33=Sum44=Sum55=Sum66=a=0
	mssum1=mssum2=mssum3=mssum4=mssum5=mssum6=mssum7=mssum8=mssum9=mssum10=mssum11=0
	un1sum1=un1sum2=un1sum3=un1sum4=un1sum5=un1sum6=un1sum7=un1sum8=un1sum9=un1sum10=un1sum11=0
	un2sum1=un2sum2=un2sum3=un2sum4=un2sum5=un2sum6=un2sum7=un2sum8=un2sum9=un2sum10=un2sum11=0
	en1sum1=en1sum2=en1sum3=en1sum4=en1sum5=en1sum6=en1sum7=en1sum8=en1sum9=en1sum10=en1sum11=0
	en2sum1=en2sum2=en2sum3=en2sum4=en2sum5=en2sum6=en2sum7=en2sum8=en2sum9=en2sum10=en2sum11=0
	en22sum1=en22sum2=en22sum3=en22sum4=en22sum5=en22sum6=en22sum7=en22sum8=en22sum9=en22sum10=en22sum11=0
	mssum101=mssum22=mssum33=mssum44=mssum55=mssum66=mssum77=mssum88=mssum99=mssum010=mssum111=0
	un1sum101=un1sum22=un1sum33=un1sum44=un1sum55=un1sum66=un1sum77=un1sum88=un1sum99=un1sum010=un1sum111=0
	un2sum101=un2sum22=un2sum33=un2sum44=un2sum55=un2sum66=un2sum77=un2sum88=un2sum99=un2sum010=un2sum111=0
	en1sum101=en1sum22=en1sum33=en1sum44=en1sum55=en1sum66=en1sum77=en1sum88=en1sum99=en1sum010=en1sum111=0
	en2sum101=en2sum22=en2sum33=en2sum44=en2sum55=en2sum66=en2sum77=en2sum88=en2sum99=en2sum010=en2sum111=0 
	en22sum101=en22sum22=en22sum33=en22sum44=en22sum55=en22sum66=en22sum77=en22sum88=en22sum99=en22sum010=en22sum111=0  
	if Product.Name=="Series-C Control Group":
		ab=Product.GetContainerByName('C300_C IO MS2')
		bc=Product.GetContainerByName('C300_C IO MS3')
		cd=Product.GetContainerByName('C300_CG_Universal_IO_Mark_1')
		de=Product.GetContainerByName('C300_CG_Universal_IO_Mark_2')
		ef=Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont')
		fg=Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1')
		per=int(Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue())/100.0 if Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue() !="" else 0
	elif Product.Name=="Series-C Remote Group":
		ab=Product.GetContainerByName('C300_C IO_RG MS2')
		bc=Product.GetContainerByName('C300_C IO_RG MS3')
		cd=Product.GetContainerByName('C300_CG_Universal_IO_Mark_1')
		de=Product.GetContainerByName('C300_CG_Universal_IO_Mark_2')
		ef=Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont')
		fg=Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1')
		per=int(Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue())/100.0 if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue() !="" else 0
	if Product.Name=="Series-C Control Group" or Product.Name=="Series-C Remote Group":
		for row in ab.Rows:
			if row.GetColumnByName("IO_Type").Value in Is:
				#for IS
				Sum1 =int(row.GetColumnByName("Red_IS").Value) if row.GetColumnByName("Red_IS").Value !='' else 0
				Sum11 += D.Ceiling((Sum1/16.0)*(1+per))
				mssum1 =int(row.GetColumnByName("Future_Red_IS").Value) if row.GetColumnByName("Future_Red_IS").Value !='' else 0
				mssum101 += D.Ceiling((mssum1/16.0)*(1+per))
				mssum2 =int(row.GetColumnByName("Non_Red_IS").Value) if row.GetColumnByName("Non_Red_IS").Value !='' else 0
				mssum22 += D.Ceiling((mssum2/16.0)*(1+per))
				#for NIS
			if row.GetColumnByName("IO_Type").Value in NIs:
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
				#for Is
				Sum2 =int(row1.GetColumnByName("Red_IS").Value) if row1.GetColumnByName("Red_IS").Value !='' else 0
				Sum22 +=D.Ceiling((Sum2/16.0)*(1+per))
				un1sum1 =int(row1.GetColumnByName("Future_Red_IS").Value) if row1.GetColumnByName("Future_Red_IS").Value !='' else 0
				un1sum101 += D.Ceiling((un1sum1/16.0)*(1+per))
				un1sum2 =int(row1.GetColumnByName("Non_Red_IS").Value) if row1.GetColumnByName("Non_Red_IS").Value !='' else 0
				un1sum22 += D.Ceiling((un1sum2/16.0)*(1+per))
				#for Nis
			if row1.GetColumnByName("IO_Type").Value in NIs:
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
				un1sum9 =int(row1.GetColumnByName("Red_RLY").Value) if row1.GetColumnByName("Red_RLY").Value !='' else 0
				un1sum99 += D.Ceiling((un1sum9/16.0)*(1+per))
				un1sum10 =int(row1.GetColumnByName("Future_Red_RLY").Value) if row1.GetColumnByName("Future_Red_RLY").Value !='' else 0
				un1sum010 += D.Ceiling((un1sum10/16.0)*(1+per))
				un1sum11 =int(row1.GetColumnByName("Non_Red_RLY").Value) if row1.GetColumnByName("Non_Red_RLY").Value !='' else 0
				un1sum111 += D.Ceiling((un1sum11/16.0)*(1+per))
		for row2 in cd.Rows:
			if row2.GetColumnByName("IO_Type").Value in Is:
				#for is
				Sum3 =int(row2.GetColumnByName("Red_IS").Value) if row2.GetColumnByName("Red_IS").Value !='' else 0
				Sum33 += D.Ceiling((Sum3/16.0)*(1+per))
				un2sum1 =int(row2.GetColumnByName("Future_Red_IS").Value) if row2.GetColumnByName("Future_Red_IS").Value !='' else 0
				un2sum101 += D.Ceiling((un2sum1/16.0)*(1+per))
				un2sum2 =int(row2.GetColumnByName("Non_Red_IS").Value) if row2.GetColumnByName("Non_Red_IS").Value !='' else 0
				un2sum22 += D.Ceiling((un2sum2/16.0)*(1+per))
				#for Nis
			if row2.GetColumnByName("IO_Type").Value in NIs:
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
		for row3 in de.Rows:
			if row3.GetColumnByName("IO_Type").Value in Is:
				Sum4 =int(row3.GetColumnByName("Red_IS").Value) if row3.GetColumnByName("Red_IS").Value !='' else 0
				Sum44 += D.Ceiling((Sum4/16.0)*(1+per))
				en1sum1 =int(row3.GetColumnByName("Future_Red_IS").Value) if row3.GetColumnByName("Future_Red_IS").Value !='' else 0
				en1sum101 += D.Ceiling((en1sum1/16.0)*(1+per))
				en1sum2 =int(row3.GetColumnByName("Non_Red_IS").Value) if row3.GetColumnByName("Non_Red_IS").Value !='' else 0
				en1sum22 += D.Ceiling((en1sum2/16.0)*(1+per))
				#Trace.Write(Sum11)
				#for Non Is calcs
			if row3.GetColumnByName("IO_Type").Value in NIs:
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
				en1sum9 =int(row3.GetColumnByName("Red_RLY").Value) if row3.GetColumnByName("Red_RLY").Value !='' else 0
				en1sum99 += D.Ceiling((en1sum9/16.0)*(1+per))
				en1sum10 =int(row3.GetColumnByName("Future_Red_RLY").Value) if row3.GetColumnByName("Future_Red_RLY").Value !='' else 0
				en1sum010 += D.Ceiling((en1sum10/16.0)*(1+per))
				en1sum11 =int(row3.GetColumnByName("Non_Red_RLY").Value) if row3.GetColumnByName("Non_Red_RLY").Value !='' else 0
				en1sum111 += D.Ceiling((en1sum11/16.0)*(1+per))
		for row4 in ef.Rows:
			if row4.GetColumnByName("IO_Type").Value in Is:
				Sum5 =int(row4.GetColumnByName("Red_IS").Value) if row4.GetColumnByName("Red_IS").Value !='' else 0
				Sum55 += D.Ceiling((Sum5/16.0)*(1+per))
				en2sum1 =int(row4.GetColumnByName("Future_Red_IS").Value) if row4.GetColumnByName("Future_Red_IS").Value !='' else 0
				en2sum101 += D.Ceiling((en2sum1/16.0)*(1+per))
				en2sum2 =int(row4.GetColumnByName("Non_Red_IS").Value) if row4.GetColumnByName("Non_Red_IS").Value !='' else 0
				en2sum22 += D.Ceiling((en2sum2/16.0)*(1+per))
				#Trace.Write(Sum55)
				#for Non Is calcs
			if row4.GetColumnByName("IO_Type").Value in NIs:
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
		for row5 in fg.Rows:
			if row5.GetColumnByName("IO_Type").Value in Is:
				Sum6 =int(row5.GetColumnByName("Red_IS").Value) if row5.GetColumnByName("Red_IS").Value !='' else 0
				Sum66 += D.Ceiling((Sum6/16.0)*(1+per))
				en22sum1 =int(row5.GetColumnByName("Future_Red_IS").Value) if row5.GetColumnByName("Future_Red_IS").Value !='' else 0
				en22sum101 += D.Ceiling((en22sum1/16.0)*(1+per))
				en22sum2 =int(row5.GetColumnByName("Non_Red_IS").Value) if row5.GetColumnByName("Non_Red_IS").Value !='' else 0
				en22sum22 += D.Ceiling((en22sum2/16.0)*(1+per))
				#Trace.Write(Sum55)
				#for Non Is calcs
			if row5.GetColumnByName("IO_Type").Value in NIs:
				en22sum3 =int(row5.GetColumnByName("Red_NIS").Value) if row5.GetColumnByName("Red_NIS").Value !='' else 0
				en22sum33 += D.Ceiling((en22sum3/16.0)*(1+per))
				en22sum4 =int(row5.GetColumnByName("Future_Red_NIS").Value) if row5.GetColumnByName("Future_Red_NIS").Value !='' else 0
				en22sum44 += D.Ceiling((en22sum4/16.0)*(1+per))
				en22sum5 =int(row5.GetColumnByName("Non_Red_NIS").Value) if row5.GetColumnByName("Non_Red_NIS").Value !='' else 0
				en22sum55 += D.Ceiling((en22sum5/16.0)*(1+per))
				en22sum6 =int(row5.GetColumnByName("Red_ISLTR").Value) if row5.GetColumnByName("Red_ISLTR").Value !='' else 0
				en22sum66 += D.Ceiling((en22sum6/16.0)*(1+per))
				en22sum7 =int(row5.GetColumnByName("Future_Red_ISLTR").Value) if row5.GetColumnByName("Future_Red_ISLTR").Value !='' else 0
				en22sum77 += D.Ceiling((en22sum7/16.0)*(1+per))
				en22sum8 =int(row5.GetColumnByName("Non_Red_ISLTR").Value) if row5.GetColumnByName("Non_Red_ISLTR").Value !='' else 0
				en22sum88 += D.Ceiling((en22sum8/16.0)*(1+per))
				en22sum9 =int(row5.GetColumnByName("Red_RLY").Value) if row5.GetColumnByName("Red_RLY").Value !='' else 0
				en22sum99 += D.Ceiling((en22sum9/16.0)*(1+per))
				en22sum10 =int(row5.GetColumnByName("Future_Red_RLY").Value) if row5.GetColumnByName("Future_Red_RLY").Value !='' else 0
				en22sum010 += D.Ceiling((en22sum10/16.0)*(1+per))
				en22sum11 =int(row5.GetColumnByName("Non_Red_RLY").Value) if row5.GetColumnByName("Non_Red_RLY").Value !='' else 0
				en22sum111 += D.Ceiling((en22sum11/16.0)*(1+per))
	if Product.Name=="Series-C Control Group":
		if Product.Attr('SerC_CG_IO_Family_Type').GetValue()=="Series-C Mark II" and Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').GetValue()=="Yes":
			percent= int(Product.Attr('SerC_CG_Percentage_of_Spare_Space_required(0-100%)').GetValue())/100.0 if Product.Attr('SerC_CG_Percentage_of_Spare_Space_required(0-100%)').GetValue() !='' else 0
			#Trace.Write("per Per " +str(percent))
			a=mssum33+mssum44+mssum55+mssum66+mssum77+mssum88
			Sum_IsM=D.Ceiling((1+percent)*(D.Ceiling((Sum11+Sum22+Sum33+Sum44+Sum55+Sum66+mssum101+mssum22+un1sum101+un1sum22+un2sum101+un2sum22+en1sum101+en1sum22+en2sum101+en2sum22+en22sum101+en22sum22))))
			Sum_Is1M=(D.Ceiling((Sum11+Sum22+Sum33+Sum44+Sum55+Sum66+mssum101+mssum22+un1sum101+un1sum22+un2sum101+un2sum22+en1sum101+en1sum22+en2sum101+en2sum22+en22sum101+en22sum22)))
			Sum_NIsM=D.Ceiling((1+percent)*D.Ceiling(a+un1sum33+un1sum44+un1sum55+un1sum66+un1sum77+un1sum88+un2sum33+un2sum44+un2sum55+un2sum66+un2sum77+un2sum88+un2sum99+un2sum010+un2sum111+en1sum33+en1sum44+en1sum55+en1sum66+en1sum77+en1sum88+en2sum33+en2sum44+en2sum55+en2sum66+en2sum77+en2sum88+en2sum99+en2sum010+en2sum111+en22sum33+en22sum44+en22sum55+en22sum66+en22sum77+en22sum88+en22sum99+en22sum010+en22sum111+un1sum99+un1sum010+un1sum111+en1sum99+en1sum010+en1sum111))
			Sum_NIs1M=D.Ceiling(a+un1sum33+un1sum44+un1sum55+un1sum66+un1sum77+un1sum88+un2sum33+un2sum44+un2sum55+un2sum66+un2sum77+un2sum88+un2sum99+un2sum010+un2sum111+en1sum33+en1sum44+en1sum55+en1sum66+en1sum77+en1sum88+en2sum33+en2sum44+en2sum55+en2sum66+en2sum77+en2sum88+en2sum99+en2sum010+en2sum111+en22sum33+en22sum44+en22sum55+en22sum66+en22sum77+en22sum88+en22sum99+en22sum010+en22sum111+un1sum99+un1sum010+un1sum111+en1sum99+en1sum010+en1sum111)
	elif Product.Name=="Series-C Remote Group":
		if Product.Attr('SerC_CG_IO_Family_Type').GetValue()=="Series-C Mark II" and Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue()=="Yes":
			percent= int(Product.Attr('SeriesC_RG_Percentage').GetValue())/100.0 if Product.Attr('SeriesC_RG_Percentage').GetValue() !='' else 0
			#Trace.Write("per Per " +str(percent))
			a=mssum33+mssum44+mssum55+mssum66+mssum77+mssum88
			Sum_IsM=D.Ceiling((1+percent)*(D.Ceiling((Sum11+Sum22+Sum33+Sum44+Sum55+Sum66+mssum101+mssum22+un1sum101+un1sum22+un2sum101+un2sum22+en1sum101+en1sum22+en2sum101+en2sum22+en22sum101+en22sum22))))
			Sum_Is1M=(D.Ceiling((Sum11+Sum22+Sum33+Sum44+Sum55+Sum66+mssum101+mssum22+un1sum101+un1sum22+un2sum101+un2sum22+en1sum101+en1sum22+en2sum101+en2sum22+en22sum101+en22sum22)))
			Sum_NIsM=D.Ceiling((1+percent)*D.Ceiling(a+un1sum33+un1sum44+un1sum55+un1sum66+un1sum77+un1sum88+un2sum33+un2sum44+un2sum55+un2sum66+un2sum77+un2sum88+un2sum99+un2sum010+un2sum111+en1sum33+en1sum44+en1sum55+en1sum66+en1sum77+en1sum88+en2sum33+en2sum44+en2sum55+en2sum66+en2sum77+en2sum88+en2sum99+en2sum010+en2sum111+en22sum33+en22sum44+en22sum55+en22sum66+en22sum77+en22sum88+en22sum99+en22sum010+en22sum111+un1sum99+un1sum010+un1sum111+en1sum99+en1sum010+en1sum111))
			Sum_NIs1M=D.Ceiling(a+un1sum33+un1sum44+un1sum55+un1sum66+un1sum77+un1sum88+un2sum33+un2sum44+un2sum55+un2sum66+un2sum77+un2sum88+un2sum99+un2sum010+un2sum111+en1sum33+en1sum44+en1sum55+en1sum66+en1sum77+en1sum88+en2sum33+en2sum44+en2sum55+en2sum66+en2sum77+en2sum88+en2sum99+en2sum010+en2sum111+en22sum33+en22sum44+en22sum55+en22sum66+en22sum77+en22sum88+en22sum99+en22sum010+en22sum111+un1sum99+un1sum010+un1sum111+en1sum99+en1sum010+en1sum111)
	return Sum_IsM,Sum_Is1M,Sum_NIsM,Sum_NIs1M
def USCA_Calcs1_digital(Product):
	IO_familyType =Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	A=0
	col_val=[]
	IO_val ={}
	if IO_familyType=="Series-C Mark II":
		if Product.Name == 'Series-C Control Group':
			per_spareSpace=int(Product.Attr('SerC_CG_Percentage_of_Spare_Space_required(0-100%)').GetValue()) if Product.Attr('SerC_CG_Percentage_of_Spare_Space_required(0-100%)').GetValue()!='' else 0
			sparePercent = int(Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()) if Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()!='' else 0
			col_val = ['Red_HV_Rly','Future_HV_Rly','Non_Red_HV_Rly']
			IO_val={'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1':['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)','SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)'],'C300_C IO MS3':['SCM: DI (32) 24VDC (0-5000)','SCM: DI (32) 24VDC SOE (0-5000)','SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'],'C300_CG_Universal_IO_Mark_2':['SCM: UIO (32) Digital Output (0-5000)','SCM: UIO (32) Digital Input (0-5000)']}
		elif Product.Name == 'Series-C Remote Group':    
			per_spareSpace=int(Product.Attr('SeriesC_RG_Percentage').GetValue()) if Product.Attr('SeriesC_RG_Percentage').GetValue()!='' else 0
			sparePercent = int(Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()) if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()!='' else 0
			
			col_val = ['Red_HV_Rly','Future_HV_Rly','Non_Red_HV_Rly']
			IO_val={'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1':['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)','SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)'],'C300_C IO_RG MS3':['SCM: DI (32) 24VDC (0-5000)','SCM: DI (32) 24VDC SOE (0-5000)','SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'],'C300_CG_Universal_IO_Mark_2':['SCM: UIO (32) Digital Output (0-5000)','SCM: UIO (32) Digital Input (0-5000)']}
		if len(col_val)>0 and len(IO_val)>0:
			for cont,IO_vals in IO_val.items():
				for row in Product.GetContainerByName(str(cont)).Rows:
					if row['IO_Type'] in IO_vals:
						for col in col_val:
							val= int(row[str(col)]) if row[str(col)] != '' else 0   
							A += D.Ceiling ((1+(per_spareSpace/100.0)) * (D.Ceiling ((1+(sparePercent/100.0)) * val /16.0)))
	return A
def part_condition(Product):
	sic0=sic11=sic22=sic33=sic44=sic55=sic66=sic77=sic=0
	Sum_IsM,Sum_Is1M,Sum_NIsM,Sum_NIs1M=USCA_Calcs1(Product)
	if Product.Name=="Series-C Control Group":
		if Product.Attr('SerC_CG_IO_Family_Type').GetValue()=="Series-C Mark II" and Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').GetValue()=="Yes":
			sic=Product.Attr('SerC_CG_SIC_Length_for_UMC').GetValue()
	elif Product.Name=="Series-C Remote Group":
		if Product.Attr('SerC_CG_IO_Family_Type').GetValue()=="Series-C Mark II" and Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue()=="Yes":
			sic=Product.Attr('SeriesC_RG_SICLength').GetValue()
	if Product.Name=="Series-C Control Group" or Product.Name=="Series-C Remote Group":
		if sic=="1500MM":
			sic11=Sum_Is1M+Sum_NIs1M
		elif sic=="6000MM":
			sic22=Sum_Is1M+Sum_NIs1M
		elif sic=="10000MM":
			sic33=Sum_Is1M+Sum_NIs1M
		elif sic=="15000MM":
			sic44=Sum_Is1M+Sum_NIs1M
		elif sic=="20000MM":
			sic55=Sum_Is1M+Sum_NIs1M
		elif sic=="25000MM":
			sic66=Sum_Is1M+Sum_NIs1M
		elif sic=="30000MM":
			sic77=Sum_Is1M+Sum_NIs1M
	return sic0,sic11,sic22,sic33,sic44,sic55,sic66,sic77
def UmcPart(Product):
	var11=var22=var33=var44=var55=var66=var77=var88=var99=var100=var111=var122=var133=var144=var155=var166=var177=var188=var199=var200=var211=var222=var233=var244=var255=var266=var277=var288=var299=var300=var311=var322=var333=var344=var355=var366=0
	Cabinet_Type=Universal_lay=Cabinet_Power=Mounting_Option="none"
	Sum_IsM,Sum_Is1M,Sum_NIsM,Sum_NIs1M=USCA_Calcs1(Product)
	USCA_qty=USCA_Calcs1_digital(Product)
	if Product.Name=="Series-C Control Group":
		if Product.Attr('SerC_CG_IO_Family_Type').GetValue()=="Series-C Mark II" and Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').GetValue()=="Yes":
			Cabinet_Type = Product.Attr('SerC_CG_Cabinet_Type').GetValue()
			Trace.Write(Cabinet_Type)
			Universal_lay = Product.Attr('SerC_CG_Universal_Marshaling_Cabinet_layout').GetValue()
			Trace.Write(Universal_lay)
			Cabinet_Power = Product.Attr('SerC_Cabinet_Power').GetValue()
			Trace.Write(Cabinet_Power)
			Mounting_Option = Product.Attr('SerC_CG_Mounting_Option').GetValue()
			Trace.Write(Mounting_Option)
	elif Product.Name=="Series-C Remote Group":
		if Product.Attr('SerC_CG_IO_Family_Type').GetValue()=="Series-C Mark II" and Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue()=="Yes":
			Cabinet_Type = Product.Attr('SeriesC_RG_CabinetType').GetValue()
			Universal_lay = Product.Attr('SeriesC_RG_UniversalMarshallingCL').GetValue()
			Cabinet_Power = Product.Attr('SeriesC_RG_CabinetPower').GetValue()
			Mounting_Option = Product.Attr('SeriesC_RG_MountingOption').GetValue()
	if Product.Name=="Series-C Control Group" or Product.Name=="Series-C Remote Group":
		#CXCPQ-47002
		if Cabinet_Type=="Dual Sided" and Universal_lay=="2 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Plate Mounting":
			var11=D.Ceiling(Sum_NIsM/30.0)
			var22=D.Ceiling(Sum_IsM/30.0)
			var255=D.Ceiling(USCA_qty/26.0)
		#CXCPQ-47013
		elif Cabinet_Type=="Single Sided" and Universal_lay=="2 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Bracket Mounting":
			var33=D.Ceiling(Sum_NIsM/14.0)
			var44=D.Ceiling(Sum_IsM/14.0)
			var266=D.Ceiling(USCA_qty/12.0)
		#CXCPQ-47000
		elif Cabinet_Type=="Dual Sided" and Universal_lay=="2 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Plate Mounting":
			var55=D.Ceiling(Sum_NIsM/28.0)
			var66=D.Ceiling(Sum_IsM/28.0)
			var277=D.Ceiling(USCA_qty/24.0)
		#CXCPQ-47005
		elif Cabinet_Type=="Single Sided" and Universal_lay=="3 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Bracket Mounting":
			var77=D.Ceiling(Sum_NIsM/21.0)
			var88=D.Ceiling(Sum_IsM/21.0)
			var288=D.Ceiling(USCA_qty/18.0)
		#CXCPQ-47012
		elif Cabinet_Type=="Single Sided" and Universal_lay=="2 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Plate Mounting":
			var99=D.Ceiling(Sum_NIsM/14.0)
			var100=D.Ceiling(Sum_IsM/14.0)
			var299=D.Ceiling(USCA_qty/12.0)
		#CXCPQ-46993
		elif Cabinet_Type=="Dual Sided" and Universal_lay=="3 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Bracket Mounting":
			var111=D.Ceiling(Sum_NIsM/45.0)
			var122=D.Ceiling(Sum_IsM/45.0)
			var300=D.Ceiling(USCA_qty/39.0)
		#CXCPQ-47001
		elif Cabinet_Type=="Dual Sided" and Universal_lay=="2 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Bracket Mounting":
			var133=D.Ceiling(Sum_NIsM/28.0)
			var144=D.Ceiling(Sum_IsM/28.0)
			var311=D.Ceiling(USCA_qty/24.0)
		#CXCPQ-47003
		elif Cabinet_Type=="Dual Sided" and Universal_lay=="2 Column" and Cabinet_Power=="External Sourced 24VDC" and Mounting_Option=="Bracket Mounting":
			var155=D.Ceiling(Sum_NIsM/30.0)
			var166=D.Ceiling(Sum_IsM/30.0)
			var322=D.Ceiling(USCA_qty/26.0)
		#CXCPQ-47006
		elif Cabinet_Type=="Single Sided" and Universal_lay=="2 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Plate Mounting":
			var177=D.Ceiling(Sum_NIsM/12.0)
			var188=D.Ceiling(Sum_IsM/12.0)
			var333=D.Ceiling(USCA_qty/10.0)
		#CXCPQ-46119
		elif Cabinet_Type=="Dual Sided" and Universal_lay=="3 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Bracket Mounting":
			var199=D.Ceiling(Sum_NIsM/42.0)
			var200=D.Ceiling(Sum_IsM/42.0)
			var344=D.Ceiling(USCA_qty/36.0)
		#CXCPQ-47011
		elif Cabinet_Type=="Single Sided" and Universal_lay=="2 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Bracket Mounting":
			var211=D.Ceiling(Sum_NIsM/12.0)
			var222=D.Ceiling(Sum_IsM/12.0)
			var355=D.Ceiling(USCA_qty/10.0)
		#CXCPQ-47004
		elif Cabinet_Type=="Single Sided" and Universal_lay=="3 Column" and Cabinet_Power=="120/230/VAC Power Supply" and Mounting_Option=="Bracket Mounting":
			var233=D.Ceiling(Sum_NIsM/18.0)
			var244=D.Ceiling(Sum_IsM/18.0)
			var366=D.Ceiling(USCA_qty/15.0)
	return var11,var22,var33,var44,var55,var66,var77,var88,var99,var100,var111,var122,var133,var144,var155,var166,var177,var188,var199,var200,var211,var222,var233,var244,var255,var266,var277,var288,var299,var300,var311,var322,var333,var344,var355,var366