import math
#CXCPQ-51339,CXCPQ-51369
def get_MARK_RLY(Product):
	if Product.Name == 'Series-C Control Group':
		H=I=0
		col_val = ['Red_RLY','Future_Red_RLY','Non_Red_RLY']
		cg_per = int(Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()) if Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()!='' else 0
		#cont-col mapping
		Cont_IO_H = {'C300_C IO MS3':['SCM: DI (32) 24VDC (0-5000)','SCM: DI (32) 24VDC SOE (0-5000)'],'C300_CG_Universal_IO_Mark_2':['SCM: UIO (32) Digital Input (0-5000)'],'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1':'SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'}
		Cont_IO_I = {'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1':['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)'],'C300_C IO MS3':['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'],'C300_CG_Universal_IO_Mark_2':'SCM: UIO (32) Digital Output (0-5000)'}
		for cont,IO_vals in Cont_IO_H.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_h = int(row[str(col)]) if row[str(col)] != '' else 0
						H += (1+(cg_per/100.0))*temp_h

		for cont,IO_vals in Cont_IO_I.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_i = int(row[str(col)]) if row[str(col)] != '' else 0
						I += (1+(cg_per/100.0))*temp_i
	elif Product.Name == 'Series-C Remote Group':
		H=I=0
		col_val = ['Red_RLY','Future_Red_RLY','Non_Red_RLY']
		rg_per = int(Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()) if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()!='' else 0
		#cont-col mapping
		Cont_IO_H = {'C300_C IO_RG MS3':['SCM: DI (32) 24VDC (0-5000)','SCM: DI (32) 24VDC SOE (0-5000)'],'C300_CG_Universal_IO_Mark_2':['SCM: UIO (32) Digital Input (0-5000)'],'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1':'SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)'}
		Cont_IO_I = {'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1':['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)'],'C300_C IO_RG MS3':['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'],'C300_CG_Universal_IO_Mark_2':'SCM: UIO (32) Digital Output (0-5000)'}

		for cont,IO_vals in Cont_IO_H.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_h = int(row[str(col)]) if row[str(col)] != '' else 0
						H += (1+(rg_per/100.0))*temp_h
		for cont,IO_vals in Cont_IO_I.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_i = int(row[str(col)]) if row[str(col)] != '' else 0
						I += (1+(rg_per/100.0))*temp_i
	return int(H),int(I)
#Trace.Write(get_MARK_RLY(Product))
#CXCPQ-50903,CXCPQ-51334,CXCPQ-51337
def get_MARK_IS(Product):
	if Product.Name == 'Series-C Control Group':
		B=D=F=G=0
		col_val = ['Red_IS','Future_Red_IS','Non_Red_IS']
		cg_per = int(Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()) if Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()!='' else 0
		#cont-col mapping
		Cont_IO_B = {'C300_C IO MS2':['SCM: HLAI (16) 4-20mA (0-5000)','SCM: HLAI (16) HART Config/Status (0-5000)'],'C300_CG_Universal_IO_Mark_1':'SCM: UIO (32) Analog Input (HLAI Adapt) (0-5000)','C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont':['SCM: HLAI (16) with HART with differential inputs (0-5000)','SCM: HLAI (16) without HART with differential inputs (0-5000)','SCM: HLAI (13-16) differential inputs (0-5000)']}
		Cont_IO_D = {'C300_C IO MS2':['SCM: AO (16) (0-5000)','SCM: AO (16) HART Config/Status (0-5000)'],'C300_CG_Universal_IO_Mark_1':'SCM: UIO (32) Analog Output (0-5000)','C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont':'SCM: AO (16) HART (0-5000)'}
		Cont_IO_F = {'C300_C IO MS3':['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'],'C300_CG_Universal_IO_Mark_2':['SCM: UIO (32) Digital Output (0-5000)']}
		en_red_is = ['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)']
		#CXDEV-8311
		Cont_IO_G = {'C300_C IO MS3':['SCM: DI (32) 24VDC (0-5000)','SCM: DI (32) 24VDC SOE (0-5000)'],'C300_CG_Universal_IO_Mark_2':['SCM: UIO (32) Digital Input (0-5000)']}
		IO_G  = ['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)']
		for cont,IO_vals in Cont_IO_B.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_b = int(row[str(col)]) if row[str(col)] != '' else 0
						B += (1+(cg_per/100.0))*temp_b
		for cont,IO_vals in Cont_IO_D.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_d = int(row[str(col)]) if row[str(col)] != '' else 0
						D += (1+(cg_per/100.0))*temp_d
		for cont,IO_vals in Cont_IO_F.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_f = int(row[str(col)]) if row[str(col)] != '' else 0
						F += (1+(cg_per/100.0))*temp_f
		for row in Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1').Rows:
			if row['IO_Type'] in en_red_is:
				temp_ff = int(row['Red_IS']) if row['Red_IS'] != '' else 0
				F+=(1+(cg_per/100.0))*temp_ff
		#CXDEV-8311       
		for cont,IO_vals in Cont_IO_G.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_f = int(row[str(col)]) if row[str(col)] != '' else 0
						G += (1+(cg_per/100.0))*temp_f
		for row in Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1').Rows:
			if row['IO_Type'] in IO_G:
				temp_ff = int(row['Red_IS']) if row['Red_IS'] != '' else 0
				G+=(1+(cg_per/100.0))*temp_ff
	elif Product.Name == 'Series-C Remote Group':
		B=D=F=G=0
		col_val = ['Red_IS','Future_Red_IS','Non_Red_IS']
		rg_per = int(Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()) if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()!='' else 0
		#cont-col mapping
		Cont_IO_B = {'C300_C IO_RG MS2':['SCM: HLAI (16) 4-20mA (0-5000)','SCM: HLAI (16) HART Config/Status (0-5000)'],'C300_CG_Universal_IO_Mark_1':'SCM: UIO (32) Analog Input (HLAI Adapt) (0-5000)','C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont':['SCM: HLAI (16) with HART with differential inputs (0-5000)','SCM: HLAI (16) without HART with differential inputs (0-5000)','SCM: HLAI (13-16) differential inputs (0-5000)']}
		Cont_IO_D = {'C300_C IO_RG MS2':['SCM: AO (16) (0-5000)','SCM: AO (16) HART Config/Status (0-5000)'],'C300_CG_Universal_IO_Mark_1':'SCM: UIO (32) Analog Output (0-5000)','C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont':'SCM: AO (16) HART (0-5000)'}
		Cont_IO_F = {'C300_C IO_RG MS3':['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)'],'C300_CG_Universal_IO_Mark_2':['SCM: UIO (32) Digital Output (0-5000)']}
		en_red_is = ['SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)']
		#CXDEV-8311
		Cont_IO_G = {'C300_C IO_RG MS3':['SCM: DI (32) 24VDC (0-5000)','SCM: DI (32) 24VDC SOE (0-5000)'],'C300_CG_Universal_IO_Mark_2':['SCM: UIO (32) Digital Input (0-5000)']}
		IO_G  = ['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)']
		for cont,IO_vals in Cont_IO_B.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_b = int(row[str(col)]) if row[str(col)] != '' else 0
						B += (1+(rg_per/100.0))*temp_b
		for cont,IO_vals in Cont_IO_D.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_d = int(row[str(col)]) if row[str(col)] != '' else 0
						D += (1+(rg_per/100.0))*temp_d
		for cont,IO_vals in Cont_IO_F.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_f = int(row[str(col)]) if row[str(col)] != '' else 0
						F += (1+(rg_per/100.0))*temp_f
		for row in Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1').Rows:
			if row['IO_Type'] in en_red_is:
				temp_ff = int(row['Red_IS']) if row['Red_IS'] != '' else 0
				F+=(1+(rg_per/100.0))*temp_ff
				
		for cont,IO_vals in Cont_IO_G.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_f = int(row[str(col)]) if row[str(col)] != '' else 0
						G += (1+(rg_per/100.0))*temp_f
		for row in Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1').Rows:
			if row['IO_Type'] in IO_G:
				temp_ff = int(row['Red_IS']) if row['Red_IS'] != '' else 0
				G+=(1+(rg_per/100.0))*temp_ff
	return int(B),int(D),int(F),int(G)
#CXCPQ-51338,CXCPQ-51336,CXCPQ-50912
def get_MARK_ISLTR(Product):
	if Product.Name == 'Series-C Control Group':
		G=E=C=0
		col_val = ['Red_ISLTR','Future_Red_ISLTR','Non_Red_ISLTR']
		col_val2 = ['Future_Red_IS','Non_Red_IS']
		cg_per = int(Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()) if Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()!='' else 0
		#cont-col mapping
		Cont_IO_G = {'C300_CG_Universal_IO_Mark_2':['SCM: UIO (32) Digital Input (0-5000)','SCM: UIO (32) Digital Output (0-5000)'],'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1':['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)','SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)'],'C300_C IO MS3':['SCM: DI (32) 24VDC (0-5000)','SCM: DI (32) 24VDC SOE (0-5000)','SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)']}
		IO_G2 = ['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)','SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)']
		Cont_IO_E = {'C300_C IO MS2':['SCM: AO (16) (0-5000)','SCM: AO (16) HART Config/Status (0-5000)'],'C300_CG_Universal_IO_Mark_1':'SCM: UIO (32) Analog Output (0-5000)','C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont':'SCM: AO (16) HART (0-5000)'}
		Cont_IO_C = {'C300_C IO MS2':['SCM: HLAI (16) 4-20mA (0-5000)','SCM: HLAI (16) HART Config/Status (0-5000)'],'C300_CG_Universal_IO_Mark_1':'SCM: UIO (32) Analog Input (HLAI Adapt) (0-5000)','C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont':['SCM: HLAI (16) with HART with differential inputs (0-5000)','SCM: HLAI (16) without HART with differential inputs (0-5000)', 'SCM: HLAI (13-16) differential inputs (0-5000)']}

		for cont,IO_vals in Cont_IO_G.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_g= int(row[str(col)]) if row[str(col)] != '' else 0
						G += (1+(cg_per/100.0))*temp_g
		for row in Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1').Rows:
			if row['IO_Type'] in IO_G2:
				for col in col_val2:
					temp_gg= int(row[str(col)]) if row[str(col)] != '' else 0
					G += (1+(cg_per/100.0))*temp_gg

		for cont,IO_vals in Cont_IO_E.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_e= int(row[str(col)]) if row[str(col)] != '' else 0
						E += (1+(cg_per/100.0))*temp_e
		for cont,IO_vals in Cont_IO_C.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_c= int(row[str(col)]) if row[str(col)] != '' else 0
						C += (1+(cg_per/100.0))*temp_c

	elif Product.Name == 'Series-C Remote Group':
		G=E=C=0
		col_val = ['Red_ISLTR','Future_Red_ISLTR','Non_Red_ISLTR']
		col_val2 = ['Future_Red_IS','Non_Red_IS']
		rg_per = int(Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()) if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()!='' else 0
		#cont-col mapping
		Cont_IO_G = {'C300_CG_Universal_IO_Mark_2':['SCM: UIO (32) Digital Input (0-5000)','SCM: UIO (32) Digital Output (0-5000)'],'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1':['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)','SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)'],'C300_C IO_RG MS3':['SCM: DI (32) 24VDC (0-5000)','SCM: DI (32) 24VDC SOE (0-5000)','SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply  (0-5000)']}
		IO_G2 = ['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)','SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)']
		Cont_IO_E = {'C300_C IO_RG MS2':['SCM: AO (16) (0-5000)','SCM: AO (16) HART Config/Status (0-5000)'],'C300_CG_Universal_IO_Mark_1':'SCM: UIO (32) Analog Output (0-5000)','C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont':'SCM: AO (16) HART (0-5000)'}
		Cont_IO_C = {'C300_C IO_RG MS2':['SCM: HLAI (16) 4-20mA (0-5000)','SCM: HLAI (16) HART Config/Status (0-5000)'],'C300_CG_Universal_IO_Mark_1':'SCM: UIO (32) Analog Input (HLAI Adapt) (0-5000)','C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont':['SCM: HLAI (16) with HART with differential inputs (0-5000)','SCM: HLAI (16) without HART with differential inputs (0-5000)', 'SCM: HLAI (13-16) differential inputs (0-5000)']}

		for cont,IO_vals in Cont_IO_G.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_g= int(row[str(col)]) if row[str(col)] != '' else 0
						G += (1+(rg_per/100.0))*temp_g
		for row in Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1').Rows:
			if row['IO_Type'] in IO_G2:
				for col in col_val2:
					temp_gg= int(row[str(col)]) if row[str(col)] != '' else 0
					G += (1+(rg_per/100.0))*temp_gg

		for cont,IO_vals in Cont_IO_E.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_e= int(row[str(col)]) if row[str(col)] != '' else 0
						E += (1+(rg_per/100.0))*temp_e
		for cont,IO_vals in Cont_IO_C.items():
			for row in Product.GetContainerByName(str(cont)).Rows:
				if row['IO_Type'] in IO_vals:
					for col in col_val:
						temp_c= int(row[str(col)]) if row[str(col)] != '' else 0
						C += (1+(rg_per/100.0))*temp_c
	return int(G),int(E),int(C)
#CXCPQ-50900
def get_MARK_NIS(Product):
	if Product.Name == 'Series-C Control Group':
		A=0
		col_val = ['Red_NIS','Future_Red_NIS','Non_Red_NIS']
		cg_per = int(Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()) if Product.Attr('SerC_CG_Percent_Installed_Spare').GetValue()!='' else 0
		cg_cont_list= ['C300_C IO MS2','C300_C IO MS3','C300_CG_Universal_IO_Mark_1','C300_CG_Universal_IO_Mark_2','C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont']
		IO_val=['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)','SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)']
		for cont in cg_cont_list:
			for row in Product.GetContainerByName(str(cont)).Rows:
				for col in col_val:
					temp_a = int(row[str(col)]) if row[str(col)] != '' else 0
					A += (1+(cg_per/100.0))*temp_a
		for row in Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1').Rows:
			if row['IO_Type'] in IO_val:
				for col in col_val:
					temp_aa = int(row[str(col)]) if row[str(col)] != '' else 0
					A += (1+(cg_per/100.0))*temp_aa
	elif Product.Name == 'Series-C Remote Group':
		A=0
		col_val = ['Red_NIS','Future_Red_NIS','Non_Red_NIS']
		rg_per = int(Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()) if Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()!='' else 0
		cg_cont_list= ['C300_C IO_RG MS2','C300_C IO_RG MS3','C300_CG_Universal_IO_Mark_1','C300_CG_Universal_IO_Mark_2','C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont']
		IO_val=['SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)','SCM: DO (32) 24VDC Bus External Power Supply (0-5000)','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)']
		for cont in cg_cont_list:
			for row in Product.GetContainerByName(str(cont)).Rows:
				for col in col_val:
					temp_a = int(row[str(col)]) if row[str(col)] != '' else 0
					A += (1+(rg_per/100.0))*temp_a
		for row in Product.GetContainerByName('C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1').Rows:
			if row['IO_Type'] in IO_val:
				for col in col_val:
					temp_aa = int(row[str(col)]) if row[str(col)] != '' else 0
					A += (1+(rg_per/100.0))*temp_aa
	return int(A)