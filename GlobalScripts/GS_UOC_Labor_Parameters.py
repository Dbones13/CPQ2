class AttrStorage:
	def __init__(self, Product,TagParserProduct):

		#Inherited Parameters
		self.project_type = Product.Attr('New_Expansion').GetValue() if Product.Attr('New_Expansion').GetValue() else 0
		self.loop_drawings = Product.Attr('Labor_Loop_Drawings').GetValue() if Product.Attr('Labor_Loop_Drawings').GetValue() else 0
		self.unreleased_product = Product.Attr('Labor_Unreleased_Product').GetValue() if Product.Attr('Labor_Unreleased_Product').GetValue() else 0
		self.marshalling_db = Product.Attr('Labor_Marshalling_Database').GetValue() if Product.Attr('Labor_Marshalling_Database').GetValue() else 0
		self.perc_fat = Product.Attr('Labor_Percentage_FAT').GetValue()  if Product.Attr('Labor_Percentage_FAT').GetValue() else 0
		self.site_activities = Product.Attr('Labor_Site_Activities').GetValue() if Product.Attr('Labor_Site_Activities').GetValue() else 0
		self.operation_manual = Product.Attr('Labor_Operation_Manual_Scope').GetValue() if Product.Attr('Labor_Operation_Manual_Scope').GetValue() else 0 
		self.custom_scope = Product.Attr('Labor_Custom_Scope').GetValue() if Product.Attr('Labor_Custom_Scope').GetValue() else 0
		"""self.bpd = 0
		pdm = TagParserQuote.ParseString('<*CTX( Quote.CustomField(EGAP_Project_Duration_Months) )*>')
		if pdm:
			self.bpd = pdm"""

		#if Quote:
			#if Quote.GetCustomField('EGAP_Project_Duration_Months').Content != '':
			 #   self.bpd = Quote.GetCustomField('EGAP_Project_Duration_Months').Content


		#UOC System level Parameters
		self.process_type = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Process_Type_Labour").Value
		self.marshalling_cabinets = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Marshalling_Cabinet_Cont_Labour").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Marshalling_Cabinet_Cont_Labour").Value else 0
		self.loop_count = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Enter_Total_Count_Labour").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Enter_Total_Count_Labour").Value else 0
		#self.engineering_stations = Product.GetContainerByName('CE_UOC_System_Hardware').Rows[0].GetColumnByName("UOC_Engineering_Station_Qty").Value
		self.implementation_method = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Impl_Method_Labour").Value
		self.ges_location = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Ges_Location_Labour").Value
		self.peer_pcdi = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Peer_PCDI_Labour").Value  if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Peer_PCDI_Labour").Value else 0
		self.peer_cda = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Peer_CDA_Labour").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Peer_CDA_Labour").Value else 0
		self.new_typicals = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_New_Typicals").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_New_Typicals").Value else 0
		self.ttl_typicals = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Enter_Total_Count_Labour").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Enter_Total_Count_Labour").Value else 0
		self.complex_loop_labour = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Complex_Loops_Labour").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Complex_Loops_Labour").Value else 0
		self.profitnet = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_ProfiNet_Devices_Labour").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_ProfiNet_Devices_Labour").Value else 0
		self.profitnet_IO = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_ProfiNet_Devices_IO_Labour").Value  if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_ProfiNet_Devices_IO_Labour").Value  else 0
		self.ethernet = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_EtherNet_Devices_Labour").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_EtherNet_Devices_Labour").Value else 0
		self.ethernet_IO = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_EtherNet_Devices_IO_Labour").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_EtherNet_Devices_IO_Labour").Value else 0
		self.input_quality = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Input_Quality_Specific_Labour").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Input_Quality_Specific_Labour").Value else 0
		self.simple_complexity = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Simple_Complexity_QA_Labour").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Simple_Complexity_QA_Labour").Value else 0
		self.medium_complexity = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Medium_Complexity_QA_Labour").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Medium_Complexity_QA_Labour").Value else 0
		self.complex_complexity = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Complex_Complexity_QA_Labour").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Complex_Complexity_QA_Labour").Value else 0
		self.batch_unit = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Batch_Units_Master_Labour").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Batch_Units_Master_Labour").Value else 0
		self.batch_unit_copies = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Batch_Units_Copies_Replica_Master_Labour").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Batch_Units_Copies_Replica_Master_Labour").Value else 0
		self.product_master_recipes = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Product_Master_Recipes_Labour").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Product_Master_Recipes_Labour").Value else 0
		self.product_replicated = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Product_Copy_Unit_Product_Replicated_Unit").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Product_Copy_Unit_Product_Replicated_Unit").Value else 0
		self.complex_scms = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Complex_SCMs_Per_Unit_Labour").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Complex_SCMs_Per_Unit_Labour").Value else 0
		self.complex_ops = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Complex_Operations_Per_Product_Labour").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Complex_Operations_Per_Product_Labour").Value else 0
		self.percentage_pre_fat = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Percentage_Pre_FAT").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Percentage_Pre_FAT").Value else 0
		self.peer_to_peer_io = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Peer_to_Peer").Value if Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_Peer_to_Peer").Value else 0
		self.scada_node_type = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_SCADA_Node_Type").Value
		self.Thirdparty_Serial_Scada = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Num_ThirdParty_Serial_Scada").Value
		group_count = TagParserProduct.ParseString('<*XValue(../Experion_EnterpriseGroup_Cont_count)*>')
		self.NumServ = group_count if group_count else 0
		cont = Product.GetContainerByName('UOC_Labor_Base_Details')
		deliverable_map = {
			'Base Hours for Control Eng Plan if IO>5000': 'mEP',
			'Base Hours for Control FDS if IO>5000': 'mFDS',
			'Base Hours for Control DDS if IO>5000': 'mDDS',
			'Base Hours for SoftIO Conf if IO>5000': 'mSIOConf',
			'Base Hours for Control Conf if IO> 5000': 'mConf',
			'Base Hours for FAT if IO>5000': 'mFAT',
			'Base Hours for SAT if IO>5000': 'mSAT'
		}
		result = {}
		for val in cont.Rows:
			key = deliverable_map.get(val['Labor_Deliverable'])
			if key:
				result[key] = int(val['Base_Values'])
		self.mEP = result.get('mEP', 0)
		self.mFDS = result.get('mFDS', 0)
		self.mDDS = result.get('mDDS', 0)
		self.mSIOConf = result.get('mSIOConf', 0)
		self.mConf = result.get('mConf', 0)
		self.mFAT = result.get('mFAT', 0)
		self.mSAT = result.get('mSAT', 0)



		#Section to read from Control and Remote Groups
		AI = AO = DI = DO = MODBUS = self.num_switches = self.num_rg = self.ctr = self.sys = self.is_ios = self.uio = 0.0
		cg_labor_data = SqlHelper.GetList("Select * from UOC_LABOR_PARAMETERS where Product = 'UOC Control Group' ")
		rg_labor_data = SqlHelper.GetList("Select * from UOC_LABOR_PARAMETERS where Product = 'UOC Remote Group' ")
		control_groups = Product.GetContainerByName('UOC_ControlGroup_Cont').Rows
		for control_group in control_groups:
			control = control_group.Product
			#This is to read UI inputs
			for record in cg_labor_data:
				Value = control.GetContainerByName(record.Container).Rows[int(record.Row)].GetColumnByName(record.Column).Value
				locals()[record.Parameter] += int(Value) if Value else 0
			# Is/Isolated Quantity
			is_io_cg_data = SqlHelper.GetList("Select * from UOC_LABOR_PARAMETERS where Container = 'UOC_CG_PF_IO_Cont' ")
			for record in is_io_cg_data:
				Value = control.GetContainerByName(record.Container).Rows[int(record.Row)].GetColumnByName(record.Column).Value
				self.is_ios += int(Value) if Value else 0
			#Universal I/O Container data Control group
			uio_cg_data = SqlHelper.GetList("Select * from UOC_LABOR_PARAMETERS where Container = 'UOC_CG_UIO_Cont' ")
			for record in uio_cg_data:
				Value = control.GetContainerByName(record.Container).Rows[int(record.Row)].GetColumnByName(record.Column).Value
				self.uio += int(Value) if Value else 0

			#This is to read from Part Summary table
			parts = control.GetContainerByName('UOC_CG_PartSummary_Cont').Rows
			cpu_type = control.GetContainerByName('UOC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName('UOC_Controller_Type').Value
			for part in parts:
				name = part.GetColumnByName('CE_Part_Number').Value
				if name == '900CP1-0300': #replaced part 900CP1-0200 with  900CP2-0100 and 900CP2-0100 is replaced with 900CP1-0300
					if cpu_type == 'NonRedundant':
						self.ctr += int(part.GetColumnByName('CE_Part_Qty').Value)
					elif cpu_type == 'Redundant':
						qty = float(part.GetColumnByName('CE_Part_Qty').Value)
						if qty % 2 == 0: #This is used just so we don't have to import any modules here. It is really just dividing by 2 and rounding to ceiling.
							self.ctr += int(qty / 2)
						else:
							self.ctr += int(qty / 2 + 1)
				elif name == '900CP1-0200':
					if cpu_type == 'NonRedundant':
						self.ctr += int(part.GetColumnByName('CE_Part_Qty').Value)
					elif cpu_type == 'Redundant':
						qty = float(part.GetColumnByName('CE_Part_Qty').Value)
						if qty % 2 == 0:
							self.ctr += int(qty / 2)
				elif name == 'CC-CBDD01':
					if control.GetContainerByName('UOC_CG_Cabinet_Cont').Rows[0].GetColumnByName('UOC_Cabinet_Type').Value == 'Dual':
						self.sys += int(part.GetColumnByName('CE_Part_Qty').Value)
				elif name == 'CC-CBDS01':
					if not control.GetContainerByName('UOC_CG_Cabinet_Cont').Rows[0].GetColumnByName('UOC_Cabinet_Type').Value == 'Dual':
						qty = float(part.GetColumnByName('CE_Part_Qty').Value)
						if qty % 2 == 0: #This is used just so we don't have to import any modules here. It is really just dividing by 2 and rounding to ceiling.
							self.sys += int(qty / 2)
						else:
							self.sys += int(qty / 2 + 1)
			# Iterating through remote groups
			remote_groups = control.GetContainerByName('UOC_RemoteGroup_Cont').Rows
			if remote_groups.Count != 0:
				#This is to read UI inputs
				for remote_group in remote_groups:
					self.num_rg += 1
					remote = remote_group.Product
					for record in rg_labor_data:
						Value = remote.GetContainerByName(record.Container).Rows[int(record.Row)].GetColumnByName(record.Column).Value
						locals()[record.Parameter] += int(Value) if Value else 0
					# Is/Isolated Quantity
					is_io_rg_data = SqlHelper.GetList("Select * from UOC_LABOR_PARAMETERS where Container = 'UOC_RG_PF_IO_Cont' ")
					for record in is_io_rg_data:
						Value = remote.GetContainerByName(record.Container).Rows[int(record.Row)].GetColumnByName(record.Column).Value
						self.is_ios += int(Value) if Value else 0
					#Universal I/O Container data Remote group
					uio_rg_data = SqlHelper.GetList("Select * from UOC_LABOR_PARAMETERS where Container = 'UOC_RG_UIO_Cont' ")
					for record in uio_rg_data:
						Value = remote.GetContainerByName(record.Container).Rows[int(record.Row)].GetColumnByName(record.Column).Value
						self.uio += int(Value) if Value else 0
					#This is to read from Part Summary table
					parts = remote.GetContainerByName('UOC_RG_PartSummary_Cont').Rows
					for part in parts:
						name = part.GetColumnByName('CE_Part_Number').Value
						if name == 'CC-CBDD01':
							if remote.GetContainerByName('UOC_RG_Cabinet_Cont').Rows[0].GetColumnByName('UOC_Cabinet_Type').Value == 'Dual':
								self.sys += int(part.GetColumnByName('CE_Part_Qty').Value)
						elif name == 'CC-CBDS01':
							if not remote.GetContainerByName('UOC_RG_Cabinet_Cont').Rows[0].GetColumnByName('UOC_Cabinet_Type').Value == 'Dual':
								qty = float(part.GetColumnByName('CE_Part_Qty').Value)
								if qty % 2 == 0: #This is used just so we don't have to import any modules here. It is really just dividing by 2 and rounding to ceiling.
									self.sys += int(qty / 2)
								else:
									self.sys += int(qty / 2 + 1)
		self.AI = AI
		self.AO = AO
		self.DI = DI
		self.DO = DO
		self.MODBUS = MODBUS
		Trace.Write("AI: {0}, AO: {1}, DI: {2}, DO: {3}, MODBUS: {4}".format(AI, AO, DI, DO, MODBUS))
		Trace.Write("num_rg: {0}, ctr: {1}, sys: {2}, is_ios: {3}".format(self.num_rg, self.ctr, self.sys, self.is_ios))