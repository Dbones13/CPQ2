#CXCPQ-44340
import System.Decimal as D
import GS_Get_Set_AtvQty
class IOComponents:
	def __init__(self, Product):
		self.Product = Product
		self.cont_col_mapping = dict()
		self.container_mapping = dict()
		if Product.Name == "Series-C Control Group":
			self.cont_col_mapping = {'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont':'IO_Type','SerC_CG_Enhanced_Function_IO_Cont':'IO_Type'}
			self.container_mapping = {'Analog': 'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont'}
		elif Product.Name == "Series-C Remote Group":
			self.cont_col_mapping = {'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont':'IO_Type','SerC_RG_Enhanced_Function_IO_Cont':'IO_Type'}
			self.container_mapping = {'Analog': 'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont'}

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
			container_mapping = {'SCM: HLAI (16) with HART': 'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont','SCM: HLAI (16) without H': 'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont','Series-C: HLAI (13-16) w':'SerC_CG_Enhanced_Function_IO_Cont','SCM: HLAI (13-16) differ':'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont'}
		if self.Product.Name == "Series-C Remote Group":
			container_mapping = {'SCM: HLAI (16) with HART': 'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont','SCM: HLAI (16) without H': 'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont','Series-C: HLAI (13-16) w':'SerC_RG_Enhanced_Function_IO_Cont','SCM: HLAI (13-16) differ':'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont'}
		if len(questions):
			for qn in questions:
				prefix = qn[0:24]
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

	def C300_Mark3(self):
		D21=E21=F21=D31=E31=F31=0  #FOR IS
		D22=E22=F22=D32=E32=F32=0  #FOR NIS
		D23=E23=F23=D33=E33=F33=0  #FOR ISLTR

		Y21=Y22=Y23=Y31=Y32=Y33=0 #FOR MINMAX CALCS
		PAIH02=PAIX02=TAID01=TAID11=0 # part qnt var
		questions = []
		column_name = ''
		if self.Product.Name == "Series-C Control Group":
			Percent_Installed_Spare=float(self.Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue()) if self.Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue() !='' else 0.0
			Trace.Write('Percent_Installed_Spare'+str(Percent_Installed_Spare))
			Do_point = int(self.Product.Attr('General_Question_Average_current_DO').GetValue()) if self.Product.Attr('General_Question_Average_current_DO').GetValue() !='' else 0
			Trace.Write("Do_point "+str(Do_point))
			try:
				family = self.Product.Attr('SerC_CG_IO_Family_Type').GetValue()
			except:
				family= 'No'
			if family!="No":
				scm_sc_text1 = 'Series-C: HLAI (13-16) with HART with differential inputs (0-5000)'
				scm_sc_text2 = 'Series-C: HLAI (13-16) without HART with differential inputs (0-5000)'
				if family == "Series C":
					scm_sc_text1 = "Series-C: HLAI (13-16) with HART with differential inputs (0-5000)"
					scm_sc_text2 = "Series-C: HLAI (13-16) without HART with differential inputs (0-5000)"
				if family == "Series-C Mark II":
					scm_sc_text1 = "SCM: HLAI (13-16) differential inputs (0-5000)"

				## UI Fields
				#Part IS
				DD21 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Red_IS'])
				D21=D.Ceiling(float(DD21)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(D21)
				EE21 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Future_Red_IS'])
				E21=D.Ceiling(float(EE21)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(E21)
				#C/F  part IS
				FF21 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Non_Red_IS'])
				F21=D.Ceiling(float(FF21)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(F21)

				DD31 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Red_IS'])
				D31=D.Ceiling(float(DD31)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(D31)
				EE31 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Future_Red_IS'])
				E31=D.Ceiling(float(EE31)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(E31)
				#C/F  part IS
				FF31 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Non_Red_IS'])
				F31=D.Ceiling(float(FF31)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(F31)

				DD22 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Red_NIS'])
				D22=D.Ceiling(float(DD22)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(D22)
				EE22 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Future_Red_NIS'])
				E22=D.Ceiling(float(EE22)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(E22)
				#C/F  part NIS
				FF22 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Non_Red_NIS'])
				F22=D.Ceiling(float(FF22)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(F22)

				DD32 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Red_NIS'])
				D32=D.Ceiling(float(DD32)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(D32)
				EE32 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Future_Red_NIS'])
				E32=D.Ceiling(float(EE32)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(E32)
				#C/F  part NIS
				FF32 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Non_Red_NIS'])
				F32=D.Ceiling(float(FF32)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(F32)

				DD23 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Red_ISLTR'])
				D23=D.Ceiling(float(DD23)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(D23)
				EE23 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Future_Red_ISLTR'])
				E23=D.Ceiling(float(EE23)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(E23)
				#ISLTR
				FF23 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Non_Red_ISLTR'])
				F23=D.Ceiling(float(FF23)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(F23)

				DD33 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Red_ISLTR'])
				D33=D.Ceiling(float(DD33)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(D33)
				EE33 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Future_Red_ISLTR'])
				E33=D.Ceiling(float(EE33)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(E33)
				#ISLTR
				FF33 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Non_Red_ISLTR'])
				F33=D.Ceiling(float(FF33)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(F33)

				JJ21 = self.getrailvalue([scm_sc_text1], ['Red_IS'])
				J21 = D.Ceiling(float(JJ21)*(1+(Percent_Installed_Spare/100)))
				JJ22 = self.getrailvalue([scm_sc_text1], ['Red_NIS'])
				J22 = D.Ceiling(float(JJ22)*(1+(Percent_Installed_Spare/100)))
				JJ23 = self.getrailvalue([scm_sc_text1], ['Red_ISLTR'])
				J23 = D.Ceiling(float(JJ23)*(1+(Percent_Installed_Spare/100)))
				KK21 = self.getrailvalue([scm_sc_text1], ['Future_Red_IS'])
				K21 = D.Ceiling(float(KK21)*(1+(Percent_Installed_Spare/100)))
				KK22 = self.getrailvalue([scm_sc_text1], ['Future_Red_NIS'])
				K22=D.Ceiling(float(KK22)*(1+(Percent_Installed_Spare/100)))
				KK23 = self.getrailvalue([scm_sc_text1], ['Future_Red_ISLTR'])
				K23=D.Ceiling(float(KK23)*(1+(Percent_Installed_Spare/100)))
				LL21 = self.getrailvalue([scm_sc_text1], ['Non_Red_IS'])
				L21=D.Ceiling(float(LL21)*(1+(Percent_Installed_Spare/100)))
				LL22 = self.getrailvalue([scm_sc_text1], ['Non_Red_NIS'])
				L22=D.Ceiling(float(LL22)*(1+(Percent_Installed_Spare/100)))
				LL23 = self.getrailvalue([scm_sc_text1], ['Non_Red_ISLTR'])
				L23=D.Ceiling(float(LL23)*(1+(Percent_Installed_Spare/100)))

				JJ31 = self.getrailvalue([scm_sc_text2], ['Red_IS'])
				J31 = D.Ceiling(float(JJ31)*(1+(Percent_Installed_Spare/100)))
				JJ32 = self.getrailvalue([scm_sc_text2], ['Red_NIS'])
				J32 = D.Ceiling(float(JJ32)*(1+(Percent_Installed_Spare/100)))
				JJ33 = self.getrailvalue([scm_sc_text2], ['Red_ISLTR'])
				J33 = D.Ceiling(float(JJ33)*(1+(Percent_Installed_Spare/100)))
				KK31 = self.getrailvalue([scm_sc_text2], ['Future_Red_IS'])
				K31 = D.Ceiling(float(KK31)*(1+(Percent_Installed_Spare/100)))
				KK32 = self.getrailvalue([scm_sc_text2], ['Future_Red_NIS'])
				K32=D.Ceiling(float(KK32)*(1+(Percent_Installed_Spare/100)))
				KK33 = self.getrailvalue([scm_sc_text2], ['Future_Red_ISLTR'])
				K33=D.Ceiling(float(KK33)*(1+(Percent_Installed_Spare/100)))
				LL31 = self.getrailvalue([scm_sc_text2], ['Non_Red_IS'])
				L31=D.Ceiling(float(LL31)*(1+(Percent_Installed_Spare/100)))
				LL32 = self.getrailvalue([scm_sc_text2], ['Non_Red_NIS'])
				L32=D.Ceiling(float(LL32)*(1+(Percent_Installed_Spare/100)))
				LL33 = self.getrailvalue([scm_sc_text2], ['Non_Red_ISLTR'])
				L33=D.Ceiling(float(LL33)*(1+(Percent_Installed_Spare/100)))

				YY21 = D.Ceiling(J21/16.0) + D.Ceiling(J22/16.0) + D.Ceiling(J23/16.0)
				YY22 = D.Ceiling(K21/16.0) + D.Ceiling(K22/16.0) + D.Ceiling(K23/16.0)
				YY23 = D.Ceiling(L21/16.0) + D.Ceiling(L22/16.0) + D.Ceiling(L23/16.0)
				YY31 = D.Ceiling(J31/16.0) + D.Ceiling(J32/16.0) + D.Ceiling(J33/16.0)
				YY32 = D.Ceiling(K31/16.0) + D.Ceiling(K32/16.0) + D.Ceiling(K33/16.0)
				YY33 = D.Ceiling(L31/16.0) + D.Ceiling(L32/16.0) + D.Ceiling(L33/16.0)

				#calcs for min max
				Y21 = D.Ceiling(D21/16.0) + D.Ceiling(D22/16.0) + D.Ceiling(D23/16.0)
				Y22 = D.Ceiling(E21/16.0) + D.Ceiling(E22/16.0) + D.Ceiling(E23/16.0)
				Y23 = D.Ceiling(F21/16.0) + D.Ceiling(F22/16.0) + D.Ceiling(F23/16.0)

				Y31 = D.Ceiling(D31/16.0) + D.Ceiling(D32/16.0) + D.Ceiling(D33/16.0)
				Y32 = D.Ceiling(E31/16.0) + D.Ceiling(E32/16.0) + D.Ceiling(E33/16.0)
				Y33 = D.Ceiling(F31/16.0) + D.Ceiling(F32/16.0) + D.Ceiling(F33/16.0)

				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y21', Y21)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y22', Y22)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y23', Y23)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y31', Y31)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y32', Y32)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y33', Y33)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY21', YY21)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY22', YY22)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY23', YY23)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY31', YY31)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY32', YY32)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY33', YY33)

				#Parts qnt calcs using above calcs
				#PAIH02 = ((2 * int(Y21))+int(Y22)+int(Y23)) + ((2 * int(YY21))+int(YY22)+int(YY23))
				#CC-PAIH02) = 2*(Y21+YY21) + Y22 + Y23+YY22+YY23
				PAIH02 = (2*(Y21+YY21) + Y22 + Y23+YY22+YY23) #CXCPQ - 118398
				PAIX02 = ((2 * int(Y31))+int(Y32)+int(Y33)) + ((2 * int(YY31))+int(YY32)+int(YY33))
				TAID01 = int(Y23) + int(Y33)
				TAID11 = int(Y21) + int(Y22) + int(Y31) + int(Y32)
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
			if family!="No":
				scm_sc_text1 = 'Series-C: HLAI (13-16) with HART with differential inputs (0-5000)'
				scm_sc_text2 = 'Series-C: HLAI (13-16) without HART with differential inputs (0-5000)'
				if family == "Series C":
					scm_sc_text1 = "Series-C: HLAI (13-16) with HART with differential inputs (0-5000)"
					scm_sc_text2 = "Series-C: HLAI (13-16) without HART with differential inputs (0-5000)"
				## Assigning user inputed value to pertivular veriable
				## UI Fields
				#Part IS
				DD21 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Red_IS'])
				D21=D.Ceiling(float(DD21)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(D21)
				EE21 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Future_Red_IS'])
				E21=D.Ceiling(float(EE21)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(E21)
				#C/F  part IS
				FF21 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Non_Red_IS'])
				F21=D.Ceiling(float(FF21)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(F21)

				DD31 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Red_IS'])
				D31=D.Ceiling(float(DD31)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(D31)
				EE31 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Future_Red_IS'])
				E31=D.Ceiling(float(EE31)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(E31)
				#C/F  part IS
				FF31 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Non_Red_IS'])
				F31=D.Ceiling(float(FF31)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(F31)

				DD22 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Red_NIS'])
				D22=D.Ceiling(float(DD22)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(D22)
				EE22 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Future_Red_NIS'])
				E22=D.Ceiling(float(EE22)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(E22)
				#C/F  part NIS
				FF22 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Non_Red_NIS'])
				F22=D.Ceiling(float(FF22)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(F22)

				DD32 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Red_NIS'])
				D32=D.Ceiling(float(DD32)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(D32)
				EE32 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Future_Red_NIS'])
				E32=D.Ceiling(float(EE32)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(E32)
				#C/F  part NIS
				FF32 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Non_Red_NIS'])
				F32=D.Ceiling(float(FF32)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(F32)

				DD23 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Red_ISLTR'])
				D23=D.Ceiling(float(DD23)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(D23)
				EE23 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Future_Red_ISLTR'])
				E23=D.Ceiling(float(EE23)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(E23)
				#ISLTR
				FF23 = self.getrailvalue(['SCM: HLAI (16) with HART with differential inputs (0-5000)'], ['Non_Red_ISLTR'])
				F23=D.Ceiling(float(FF23)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(F23)

				DD33 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Red_ISLTR'])
				D33=D.Ceiling(float(DD33)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(D33)
				EE33 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Future_Red_ISLTR'])
				E33=D.Ceiling(float(EE33)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(E33)
				#ISLTR
				FF33 = self.getrailvalue(['SCM: HLAI (16) without HART with differential inputs (0-5000)'], ['Non_Red_ISLTR'])
				F33=D.Ceiling(float(FF33)*(1+(Percent_Installed_Spare/100)))
				#Trace.Write(F33)

				
				JJ21 = self.getrailvalue([scm_sc_text1], ['Red_IS'])
				J21 = D.Ceiling(float(JJ21)*(1+(Percent_Installed_Spare/100)))
				JJ22 = self.getrailvalue([scm_sc_text1], ['Red_NIS'])
				J22 = D.Ceiling(float(JJ22)*(1+(Percent_Installed_Spare/100)))
				JJ23 = self.getrailvalue([scm_sc_text1], ['Red_ISLTR'])
				J23 = D.Ceiling(float(JJ23)*(1+(Percent_Installed_Spare/100)))
				KK21 = self.getrailvalue([scm_sc_text1], ['Future_Red_IS'])
				K21 = D.Ceiling(float(KK21)*(1+(Percent_Installed_Spare/100)))
				KK22 = self.getrailvalue([scm_sc_text1], ['Future_Red_NIS'])
				K22=D.Ceiling(float(KK22)*(1+(Percent_Installed_Spare/100)))
				KK23 = self.getrailvalue([scm_sc_text1], ['Future_Red_ISLTR'])
				K23=D.Ceiling(float(KK23)*(1+(Percent_Installed_Spare/100)))
				LL21 = self.getrailvalue([scm_sc_text1], ['Non_Red_IS'])
				L21=D.Ceiling(float(LL21)*(1+(Percent_Installed_Spare/100)))
				LL22 = self.getrailvalue([scm_sc_text1], ['Non_Red_NIS'])
				L22=D.Ceiling(float(LL22)*(1+(Percent_Installed_Spare/100)))
				LL23 = self.getrailvalue([scm_sc_text1], ['Non_Red_ISLTR'])
				L23=D.Ceiling(float(LL23)*(1+(Percent_Installed_Spare/100)))

				JJ31 = self.getrailvalue([scm_sc_text2], ['Red_IS'])
				J31 = D.Ceiling(float(JJ31)*(1+(Percent_Installed_Spare/100)))
				JJ32 = self.getrailvalue([scm_sc_text2], ['Red_NIS'])
				J32 = D.Ceiling(float(JJ32)*(1+(Percent_Installed_Spare/100)))
				JJ33 = self.getrailvalue([scm_sc_text2], ['Red_ISLTR'])
				J33 = D.Ceiling(float(JJ33)*(1+(Percent_Installed_Spare/100)))
				KK31 = self.getrailvalue([scm_sc_text2], ['Future_Red_IS'])
				K31 = D.Ceiling(float(KK31)*(1+(Percent_Installed_Spare/100)))
				KK32 = self.getrailvalue([scm_sc_text2], ['Future_Red_NIS'])
				K32=D.Ceiling(float(KK32)*(1+(Percent_Installed_Spare/100)))
				KK33 = self.getrailvalue([scm_sc_text2], ['Future_Red_ISLTR'])
				K33=D.Ceiling(float(KK33)*(1+(Percent_Installed_Spare/100)))
				LL31 = self.getrailvalue([scm_sc_text2], ['Non_Red_IS'])
				L31=D.Ceiling(float(LL31)*(1+(Percent_Installed_Spare/100)))
				LL32 = self.getrailvalue([scm_sc_text2], ['Non_Red_NIS'])
				L32=D.Ceiling(float(LL32)*(1+(Percent_Installed_Spare/100)))
				LL33 = self.getrailvalue([scm_sc_text2], ['Non_Red_ISLTR'])
				L33=D.Ceiling(float(LL33)*(1+(Percent_Installed_Spare/100)))

				YY21 = D.Ceiling(J21/16.0) + D.Ceiling(J22/16.0) + D.Ceiling(J23/16.0)
				YY22 = D.Ceiling(K21/16.0) + D.Ceiling(K22/16.0) + D.Ceiling(K23/16.0)
				YY23 = D.Ceiling(L21/16.0) + D.Ceiling(L22/16.0) + D.Ceiling(L23/16.0)
				YY31 = D.Ceiling(J31/16.0) + D.Ceiling(J32/16.0) + D.Ceiling(J33/16.0)
				YY32 = D.Ceiling(K31/16.0) + D.Ceiling(K32/16.0) + D.Ceiling(K33/16.0)
				YY33 = D.Ceiling(L31/16.0) + D.Ceiling(L32/16.0) + D.Ceiling(L33/16.0)


				#calcs for min max
				Y21 = D.Ceiling(D21/16.0) + D.Ceiling(D22/16.0) + D.Ceiling(D23/16.0)
				Y22 = D.Ceiling(E21/16.0) + D.Ceiling(E22/16.0) + D.Ceiling(E23/16.0)
				Y23 = D.Ceiling(F21/16.0) + D.Ceiling(F22/16.0) + D.Ceiling(F23/16.0)

				Y31 = D.Ceiling(D31/16.0) + D.Ceiling(D32/16.0) + D.Ceiling(D33/16.0)
				Y32 = D.Ceiling(E31/16.0) + D.Ceiling(E32/16.0) + D.Ceiling(E33/16.0)
				Y33 = D.Ceiling(F31/16.0) + D.Ceiling(F32/16.0) + D.Ceiling(F33/16.0)

				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y21', Y21)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y22', Y22)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y23', Y23)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y31', Y31)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y32', Y32)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'Y33', Y33)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY21', YY21)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY22', YY22)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY23', YY23)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY31', YY31)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY32', YY32)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY33', YY33)

				#Parts qnt calcs using above calcs
				#PAIH02 = ((2 * int(Y21))+int(Y22)+int(Y23)) + ((2 * int(YY21))+int(YY22)+int(YY23))
				PAIH02 = (2*(Y21+YY21) + Y22 + Y23+YY22+YY23) #CXCPQ - 118398
				PAIX02 = ((2 * int(Y31))+int(Y32)+int(Y33)) + ((2 * int(YY31))+int(YY32)+int(YY33))
				TAID01 = int(Y23) + int(Y33)
				TAID11 = int(Y21) + int(Y22) + int(Y31) + int(Y32)
		return int(PAIH02),int(PAIX02),int(TAID01),int(TAID11)
	#CXCPQ-118450
	def C300_Mark4(self):
		J21=K21=L21=J31=K31=L31=SJ21=SK21=SL21=0  #FOR IS
		J22=K22=L22=J32=K32=L32=SJ22=SK22=SL22=0  #FOR NIS
		J23=K23=L23=J33=K33=L33=SJ23=SK23=SL23=0  #FOR ISLTR

		YY21=YY22=YY23=YY31=YY32=YY33=SYY21=SYY22=SYY23=0 #FOR MINMAX CALCS

		TAIX11 = TAIX01 = STAIX11 = STAIX01 = 0 # part qnt var
		questions = []
		column_name = ''
		if self.Product.Name == "Series-C Control Group":
			Percent_Installed_Spare=float(self.Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue()) if self.Product.Attributes.GetByName("SerC_CG_Percent_Installed_Spare").GetValue() !='' else 0.0
			Trace.Write('Percent_Installed_Spare'+str(Percent_Installed_Spare))
			Do_point = int(self.Product.Attr('General_Question_Average_current_DO').GetValue()) if self.Product.Attr('General_Question_Average_current_DO').GetValue() !='' else 0
			Trace.Write("Do_point "+str(Do_point))
			try:
				family = self.Product.Attr('SerC_CG_IO_Family_Type').GetValue()
			except:
				family= 'No'
			if family=="Series-C Mark II" or family == "Series C":
				scm_sc_text1 = 'Series-C: HLAI (13-16) with HART with differential inputs (0-5000)'
				scm_sc_text2 = 'Series-C: HLAI (13-16) without HART with differential inputs (0-5000)'
				scm_sc_text3 = "SCM: HLAI (13-16) differential inputs (0-5000)"
				if family == "Series C":
					scm_sc_text1 = "Series-C: HLAI (13-16) with HART with differential inputs (0-5000)"
					scm_sc_text2 = "Series-C: HLAI (13-16) without HART with differential inputs (0-5000)"

				JJ21 = self.getrailvalue([scm_sc_text1], ['Red_IS'])
				J21 = D.Ceiling(float(JJ21)*(1+(Percent_Installed_Spare/100)))
				JJ22 = self.getrailvalue([scm_sc_text1], ['Red_NIS'])
				J22 = D.Ceiling(float(JJ22)*(1+(Percent_Installed_Spare/100)))
				JJ23 = self.getrailvalue([scm_sc_text1], ['Red_ISLTR'])
				J23 = D.Ceiling(float(JJ23)*(1+(Percent_Installed_Spare/100)))
				KK21 = self.getrailvalue([scm_sc_text1], ['Future_Red_IS'])
				K21 = D.Ceiling(float(KK21)*(1+(Percent_Installed_Spare/100)))
				KK22 = self.getrailvalue([scm_sc_text1], ['Future_Red_NIS'])
				K22=D.Ceiling(float(KK22)*(1+(Percent_Installed_Spare/100)))
				KK23 = self.getrailvalue([scm_sc_text1], ['Future_Red_ISLTR'])
				K23=D.Ceiling(float(KK23)*(1+(Percent_Installed_Spare/100)))
				LL21 = self.getrailvalue([scm_sc_text1], ['Non_Red_IS'])
				L21=D.Ceiling(float(LL21)*(1+(Percent_Installed_Spare/100)))
				LL22 = self.getrailvalue([scm_sc_text1], ['Non_Red_NIS'])
				L22=D.Ceiling(float(LL22)*(1+(Percent_Installed_Spare/100)))
				LL23 = self.getrailvalue([scm_sc_text1], ['Non_Red_ISLTR'])
				L23=D.Ceiling(float(LL23)*(1+(Percent_Installed_Spare/100)))

				JJ31 = self.getrailvalue([scm_sc_text2], ['Red_IS'])
				J31 = D.Ceiling(float(JJ31)*(1+(Percent_Installed_Spare/100)))
				JJ32 = self.getrailvalue([scm_sc_text2], ['Red_NIS'])
				J32 = D.Ceiling(float(JJ32)*(1+(Percent_Installed_Spare/100)))
				JJ33 = self.getrailvalue([scm_sc_text2], ['Red_ISLTR'])
				J33 = D.Ceiling(float(JJ33)*(1+(Percent_Installed_Spare/100)))
				KK31 = self.getrailvalue([scm_sc_text2], ['Future_Red_IS'])
				K31 = D.Ceiling(float(KK31)*(1+(Percent_Installed_Spare/100)))
				KK32 = self.getrailvalue([scm_sc_text2], ['Future_Red_NIS'])
				K32=D.Ceiling(float(KK32)*(1+(Percent_Installed_Spare/100)))
				KK33 = self.getrailvalue([scm_sc_text2], ['Future_Red_ISLTR'])
				K33=D.Ceiling(float(KK33)*(1+(Percent_Installed_Spare/100)))
				LL31 = self.getrailvalue([scm_sc_text2], ['Non_Red_IS'])
				L31=D.Ceiling(float(LL31)*(1+(Percent_Installed_Spare/100)))
				LL32 = self.getrailvalue([scm_sc_text2], ['Non_Red_NIS'])
				L32=D.Ceiling(float(LL32)*(1+(Percent_Installed_Spare/100)))
				LL33 = self.getrailvalue([scm_sc_text2], ['Non_Red_ISLTR'])
				L33=D.Ceiling(float(LL33)*(1+(Percent_Installed_Spare/100)))

				SJJ21 = self.getrailvalue([scm_sc_text3], ['Red_IS'])
				SJ21 = D.Ceiling(float(SJJ21)*(1+(Percent_Installed_Spare/100)))
				SJJ22 = self.getrailvalue([scm_sc_text3], ['Red_NIS'])
				SJ22 = D.Ceiling(float(SJJ22)*(1+(Percent_Installed_Spare/100)))
				SJJ23 = self.getrailvalue([scm_sc_text3], ['Red_ISLTR'])
				SJ23 = D.Ceiling(float(SJJ23)*(1+(Percent_Installed_Spare/100)))
				SKK21 = self.getrailvalue([scm_sc_text3], ['Future_Red_IS'])
				SK21 = D.Ceiling(float(SKK21)*(1+(Percent_Installed_Spare/100)))
				SKK22 = self.getrailvalue([scm_sc_text3], ['Future_Red_NIS'])
				SK22=D.Ceiling(float(SKK22)*(1+(Percent_Installed_Spare/100)))
				SKK23 = self.getrailvalue([scm_sc_text3], ['Future_Red_ISLTR'])
				SK23=D.Ceiling(float(SKK23)*(1+(Percent_Installed_Spare/100)))
				SLL21 = self.getrailvalue([scm_sc_text3], ['Non_Red_IS'])
				SL21=D.Ceiling(float(SLL21)*(1+(Percent_Installed_Spare/100)))
				SLL22 = self.getrailvalue([scm_sc_text3], ['Non_Red_NIS'])
				SL22=D.Ceiling(float(SLL22)*(1+(Percent_Installed_Spare/100)))
				SLL23 = self.getrailvalue([scm_sc_text3], ['Non_Red_ISLTR'])
				SL23=D.Ceiling(float(SLL23)*(1+(Percent_Installed_Spare/100)))

				YY21 = D.Ceiling(J21/16.0) + D.Ceiling(J22/16.0) + D.Ceiling(J23/16.0)
				YY22 = D.Ceiling(K21/16.0) + D.Ceiling(K22/16.0) + D.Ceiling(K23/16.0)
				YY23 = D.Ceiling(L21/16.0) + D.Ceiling(L22/16.0) + D.Ceiling(L23/16.0)
				YY31 = D.Ceiling(J31/16.0) + D.Ceiling(J32/16.0) + D.Ceiling(J33/16.0)
				YY32 = D.Ceiling(K31/16.0) + D.Ceiling(K32/16.0) + D.Ceiling(K33/16.0)
				YY33 = D.Ceiling(L31/16.0) + D.Ceiling(L32/16.0) + D.Ceiling(L33/16.0)

				SYY21 = D.Ceiling(SJ21/16.0) + D.Ceiling(SJ22/16.0) + D.Ceiling(SJ23/16.0)
				SYY22 = D.Ceiling(SK21/16.0) + D.Ceiling(SK22/16.0) + D.Ceiling(SK23/16.0)
				SYY23 = D.Ceiling(SL21/16.0) + D.Ceiling(SL22/16.0) + D.Ceiling(SL23/16.0)

				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY21', YY21)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY22', YY22)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY23', YY23)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY31', YY31)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY32', YY32)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY33', YY33)

				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'SYY21', SYY21)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'SYY22', SYY22)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'SYY23', SYY23)

				#Parts qnt calcs using above calcs
				TAIX01 = int(YY23) + int(YY33)
				TAIX11 = int(YY21) + int(YY22) + int(YY31) + int(YY32)

				STAIX11 = SYY21 +SYY22 #(DC-TAIX11) = YY21 +YY22
				STAIX01 = SYY23 # (DC-TAIX01) = YY23
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
			if family=="Series-C Mark II" or family == "Series C":
				scm_sc_text1 = 'Series-C: HLAI (13-16) with HART with differential inputs (0-5000)'
				scm_sc_text2 = 'Series-C: HLAI (13-16) without HART with differential inputs (0-5000)'
				scm_sc_text3 = "SCM: HLAI (13-16) differential inputs (0-5000)"
				if family == "Series C":
					scm_sc_text1 = "Series-C: HLAI (13-16) with HART with differential inputs (0-5000)"
					scm_sc_text2 = "Series-C: HLAI (13-16) without HART with differential inputs (0-5000)"

				JJ21 = self.getrailvalue([scm_sc_text1], ['Red_IS'])
				J21 = D.Ceiling(float(JJ21)*(1+(Percent_Installed_Spare/100)))
				JJ22 = self.getrailvalue([scm_sc_text1], ['Red_NIS'])
				J22 = D.Ceiling(float(JJ22)*(1+(Percent_Installed_Spare/100)))
				JJ23 = self.getrailvalue([scm_sc_text1], ['Red_ISLTR'])
				J23 = D.Ceiling(float(JJ23)*(1+(Percent_Installed_Spare/100)))
				KK21 = self.getrailvalue([scm_sc_text1], ['Future_Red_IS'])
				K21 = D.Ceiling(float(KK21)*(1+(Percent_Installed_Spare/100)))
				KK22 = self.getrailvalue([scm_sc_text1], ['Future_Red_NIS'])
				K22=D.Ceiling(float(KK22)*(1+(Percent_Installed_Spare/100)))
				KK23 = self.getrailvalue([scm_sc_text1], ['Future_Red_ISLTR'])
				K23=D.Ceiling(float(KK23)*(1+(Percent_Installed_Spare/100)))
				LL21 = self.getrailvalue([scm_sc_text1], ['Non_Red_IS'])
				L21=D.Ceiling(float(LL21)*(1+(Percent_Installed_Spare/100)))
				LL22 = self.getrailvalue([scm_sc_text1], ['Non_Red_NIS'])
				L22=D.Ceiling(float(LL22)*(1+(Percent_Installed_Spare/100)))
				LL23 = self.getrailvalue([scm_sc_text1], ['Non_Red_ISLTR'])
				L23=D.Ceiling(float(LL23)*(1+(Percent_Installed_Spare/100)))

				JJ31 = self.getrailvalue([scm_sc_text2], ['Red_IS'])
				J31 = D.Ceiling(float(JJ31)*(1+(Percent_Installed_Spare/100)))
				JJ32 = self.getrailvalue([scm_sc_text2], ['Red_NIS'])
				J32 = D.Ceiling(float(JJ32)*(1+(Percent_Installed_Spare/100)))
				JJ33 = self.getrailvalue([scm_sc_text2], ['Red_ISLTR'])
				J33 = D.Ceiling(float(JJ33)*(1+(Percent_Installed_Spare/100)))
				KK31 = self.getrailvalue([scm_sc_text2], ['Future_Red_IS'])
				K31 = D.Ceiling(float(KK31)*(1+(Percent_Installed_Spare/100)))
				KK32 = self.getrailvalue([scm_sc_text2], ['Future_Red_NIS'])
				K32=D.Ceiling(float(KK32)*(1+(Percent_Installed_Spare/100)))
				KK33 = self.getrailvalue([scm_sc_text2], ['Future_Red_ISLTR'])
				K33=D.Ceiling(float(KK33)*(1+(Percent_Installed_Spare/100)))
				LL31 = self.getrailvalue([scm_sc_text2], ['Non_Red_IS'])
				L31=D.Ceiling(float(LL31)*(1+(Percent_Installed_Spare/100)))
				LL32 = self.getrailvalue([scm_sc_text2], ['Non_Red_NIS'])
				L32=D.Ceiling(float(LL32)*(1+(Percent_Installed_Spare/100)))
				LL33 = self.getrailvalue([scm_sc_text2], ['Non_Red_ISLTR'])
				L33=D.Ceiling(float(LL33)*(1+(Percent_Installed_Spare/100)))

				SJJ21 = self.getrailvalue([scm_sc_text3], ['Red_IS'])
				SJ21 = D.Ceiling(float(SJJ21)*(1+(Percent_Installed_Spare/100)))
				SJJ22 = self.getrailvalue([scm_sc_text3], ['Red_NIS'])
				SJ22 = D.Ceiling(float(SJJ22)*(1+(Percent_Installed_Spare/100)))
				SJJ23 = self.getrailvalue([scm_sc_text3], ['Red_ISLTR'])
				SJ23 = D.Ceiling(float(SJJ23)*(1+(Percent_Installed_Spare/100)))
				SKK21 = self.getrailvalue([scm_sc_text3], ['Future_Red_IS'])
				SK21 = D.Ceiling(float(SKK21)*(1+(Percent_Installed_Spare/100)))
				SKK22 = self.getrailvalue([scm_sc_text3], ['Future_Red_NIS'])
				SK22=D.Ceiling(float(SKK22)*(1+(Percent_Installed_Spare/100)))
				SKK23 = self.getrailvalue([scm_sc_text3], ['Future_Red_ISLTR'])
				SK23=D.Ceiling(float(SKK23)*(1+(Percent_Installed_Spare/100)))
				SLL21 = self.getrailvalue([scm_sc_text3], ['Non_Red_IS'])
				SL21=D.Ceiling(float(SLL21)*(1+(Percent_Installed_Spare/100)))
				SLL22 = self.getrailvalue([scm_sc_text3], ['Non_Red_NIS'])
				SL22=D.Ceiling(float(SLL22)*(1+(Percent_Installed_Spare/100)))
				SLL23 = self.getrailvalue([scm_sc_text3], ['Non_Red_ISLTR'])
				SL23=D.Ceiling(float(SLL23)*(1+(Percent_Installed_Spare/100)))

				YY21 = D.Ceiling(J21/16.0) + D.Ceiling(J22/16.0) + D.Ceiling(J23/16.0)
				YY22 = D.Ceiling(K21/16.0) + D.Ceiling(K22/16.0) + D.Ceiling(K23/16.0)
				YY23 = D.Ceiling(L21/16.0) + D.Ceiling(L22/16.0) + D.Ceiling(L23/16.0)
				YY31 = D.Ceiling(J31/16.0) + D.Ceiling(J32/16.0) + D.Ceiling(J33/16.0)
				YY32 = D.Ceiling(K31/16.0) + D.Ceiling(K32/16.0) + D.Ceiling(K33/16.0)
				YY33 = D.Ceiling(L31/16.0) + D.Ceiling(L32/16.0) + D.Ceiling(L33/16.0)

				SYY21 = D.Ceiling(SJ21/16.0) + D.Ceiling(SJ22/16.0) + D.Ceiling(SJ23/16.0)
				SYY22 = D.Ceiling(SK21/16.0) + D.Ceiling(SK22/16.0) + D.Ceiling(SK23/16.0)
				SYY23 = D.Ceiling(SL21/16.0) + D.Ceiling(SL22/16.0) + D.Ceiling(SL23/16.0)

				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY21', YY21)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY22', YY22)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY23', YY23)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY31', YY31)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY32', YY32)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'YY33', YY33)

				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'SYY21', SYY21)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'SYY22', SYY22)
				GS_Get_Set_AtvQty.setAtvQty(self.Product, 'SerC_IO_Params', 'SYY23', SYY23)

				#Parts qnt calcs using above calcs
				TAIX01 = int(YY23) + int(YY33)
				TAIX11 = int(YY21) + int(YY22) + int(YY31) + int(YY32)

				STAIX11 = SYY21 +SYY22 #(DC-TAIX11) = YY21 +YY22
				STAIX01 = SYY23 # (DC-TAIX01) = YY23
		return int(TAIX01),int(TAIX11),int(STAIX11),int(STAIX01)
#test = IOComponents(Product)
#val = test.C300_Mark3()
#Trace.Write(val)