import System.Decimal as D
def Node_server(Product,que,TPM):
	Node_flex=""
	Redundancy=""
	attr_mapping =[]
	question=[]
	if Product.Name == "Experion Enterprise Group":
		server_qnt=0
		Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
		Trace.Write(Redundancy)
		question=['Server_NodeType','Server Node Type_desk']
		# node supplier and TPM
		node_supplier = ['Node_Supplier_Server','Node Supplier_server']
		trusted_platform_module = ['TrustedPlatformModule_TPM','Trusted Platform Module1']

		#CXCPQ-37560,37562,37563,37564
		for (i,j,k) in zip(question,node_supplier,trusted_platform_module):
			Node_flex=Product.Attr(str(i)).GetValue()
			ns = Product.Attr(str(j)).GetValue()
			tpm = Product.Attr(str(k)).GetValue()
			#Trace.Write(Node_flex)
			if Redundancy=="Redundant" and Node_flex == que and ns == "Honeywell" and tpm == TPM:
				server_qnt=2
			elif Redundancy=="Non Redundant" and Node_flex == que and ns == "Honeywell" and tpm == TPM:
				server_qnt=1
	return server_qnt

#CXCPQ-37562,CXCPQ-37564
def server_qnt1(Product,que,TPM):
	Node_flex=""
	Redundancy=""
	Value_mapp_se={}
	question1=[]
	if Product.Name == "Experion Enterprise Group":
		server_qnt=Node_server(Product,que,TPM)
		Trace.Write("server_qnt---:"+str(server_qnt))
		#server Qustion mapping
		server=['Hardware Design Selection_ ACE_Node','Hardware Design Selection_ACE Node','Hardware Design Selection_ACE_T_Node','Hardware Design Selection','Server Type1','Hardware Design Selection - EAPP Node','Hardware_Design_Selection - EAPP Node','Hardware Selection']

		#server question quntity mapping
		Server_mapping=['ACE Node Tower Mount Desk','ACE Node Rack Mount Cabinet','ACE_T_Node _Tower_Mount_Desk','ACE_T_Node _Rack_Mount_Cabinet','Additional Servers','Experion APP Node - Tower Mount','Experion APP Node - Rack Mount','Mobile Server Nodes (0-1)']

		#Node Supplier and TPM
		node_supplier = ['Node Supplier_ACE1','Node Supplier_ACE','Node_Supplier_ACE_T','Node Supplier_ACE_T','Node Supplier Server','Node Supplier_EAPP','Node_Supplier_EAPP','Node Supplier Server1']
		trusted_platform_module = ['Trusted Platform Module_TPM_ACE_desk','Trusted Platform Module_TPM_ACE_Node','Trusted Platform Module_TPM_ACE_T','Ent_ace_t_Cab_tpm','Trusted Platform Module_TPM','Ent_app_desk_tpm','Ent_app_cab_tpm','Ent_ace_t_desk_tpm']

		for (i,j,k,l) in zip(server ,Server_mapping, node_supplier, trusted_platform_module):
			attr_name = str(j)
			Node_flex=Product.Attr(str(i)).GetValue()
			ns = Product.Attr(str(k)).GetValue()
			tpm = Product.Attr(str(l)).GetValue()
			#Trace.Write("Node_flex: "+str(Node_flex))
			if Node_flex == que and ns == "Honeywell" and tpm == TPM:
				Trace.Write("val : "+str(Node_flex))
				server_qnt +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
	return server_qnt
#CXCPQ-37560,CXCPQ-37563
def server_qnt2(Product,que,TPM):
	Node_flex=""
	Redundancy=""
	Value_mapp_se={}
	question1=[]
	if Product.Name == "Experion Enterprise Group":
		server_qnt=Node_server(Product,que,TPM)
		Trace.Write("server_qnt---:"+str(server_qnt))
		#server Qustion mapping
		server=['Hardware Design Selection_ ACE_Node','Hardware Design Selection_ACE Node','Server Type1']

		#server question quntity mapping
		Server_mapping=['ACE Node Tower Mount Desk','ACE Node Rack Mount Cabinet','Additional Servers']

		#Node Supplier and TPM
		node_supplier = ['Node Supplier_ACE1','Node Supplier_ACE','Node Supplier Server']
		trusted_platform_module = ['Trusted Platform Module_TPM_ACE_desk','Trusted Platform Module_TPM_ACE_Node','Trusted Platform Module_TPM']

		for (i,j,k,l) in zip(server ,Server_mapping, node_supplier, trusted_platform_module):
			attr_name = str(j)
			Node_flex=Product.Attr(str(i)).GetValue()
			ns = Product.Attr(str(k)).GetValue()
			tpm = Product.Attr(str(l)).GetValue()
			#Trace.Write("Node_flex: "+str(Node_flex))
			if Node_flex == que and ns == "Honeywell" and tpm == TPM:
				Trace.Write("val : "+str(Node_flex))
				server_qnt +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
	return server_qnt
#CXCPQ-37567,68,69
def Node_station(Product,que):
	Node_flex=""
	Redundancy=""
	question=[]
	if Product.Name == "Experion Enterprise Group":
		server_qnt=0
		Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
		Trace.Write(Redundancy)
		question=['FlexServer_NodeType','Flex Server Node Type']
		# node supplier
		node_supplier = ['NodeSupplier_FlexServer','Node Supplier (Flex Server)']

		#CXCPQ-37567,37568,37569,37572
		for (i,j) in zip(question,node_supplier):
			Node_flex=Product.Attr(str(i)).GetValue()
			ns = Product.Attr(str(j)).GetValue()
			#Trace.Write(Node_flex)
			if Redundancy=="Redundant" and Node_flex == que and ns == "Honeywell":
				server_qnt=2
			elif Redundancy=="Non Redundant" and Node_flex == que and ns == "Honeywell":
				server_qnt=1
	return server_qnt
#CXCPQ-37567,37568
def station_qnt1(Product,que,que1):
	Node_flex=""
	question1=[]
	station_qnt_cms=station_qnt_dms=station_qnt_ori=station_qnt_add=0
	if Product.Name == "Experion Enterprise Group":
		server_qnt=Node_station(Product,que)
		station_qnt = 0
		Trace.Write("server_qnt---:"+str(server_qnt))
		#station Question
		station1=['CMS Flex Station Hardware Selection','CMS Console Station Hardware Selection','CMS TPS Station Hardware Selection','CMS Console Station Extension Hardware Selection']
		station2=['DMS Flex Station Hardware Selection','DMS Console Station Hardware Selection','DMS TPS Station Hardware Selection','DMS Console Station Extension Hardware Selection']
		station3=['Flex Station Hardware Selection TPS','Console Station Hardware Selection','TPS Station Hardware Selection','Console Station Extension Hardware Selection']
		station4=['Station Type']
		#station Question Quantity mapping
		station_mapping1=['CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15']
		station_mapping2=['DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15']
		station_mapping3=['Flex Station Qty (0-60)','Console Station Qty (0-20)','TPS Station Qty (0-20)','Console Station Extension Qty  (0-15)']
		station_mapping4=['Additional Stations']
		#Node Supplier and TPM
		cms_node=Product.Attr('CMS Node Supplier').GetValue()
		dms_node=Product.Attr('DMS Node Supplier').GetValue()
		ori_node=Product.Attr('Node Supplier').GetValue()
		add_node=Product.Attr('Node Supplier (Additional Station)').GetValue()

		for (i1,j1) in zip(station1 ,station_mapping1):
			attr_name = str(j1)
			Node_flex=Product.Attr(str(i1)).GetValue()
			#Trace.Write("Node_flex: "+str(Node_flex))
			if Node_flex == que1 and cms_node=="Honeywell":
				Trace.Write("val : "+str(Node_flex))
				station_qnt_cms +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

		for (i2,j2) in zip(station2 ,station_mapping2):
			attr_name = str(j2)
			Node_flex=Product.Attr(str(i2)).GetValue()
			#Trace.Write("Node_flex: "+str(Node_flex))
			if Node_flex == que1 and dms_node=="Honeywell":
				Trace.Write("val : "+str(Node_flex))
				station_qnt_dms +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

		for (i3,j3) in zip(station3 ,station_mapping3):
			attr_name = str(j3)
			Node_flex=Product.Attr(str(i3)).GetValue()
			#Trace.Write("Node_flex: "+str(Node_flex))
			if Node_flex == que1 and ori_node=="Honeywell":
				Trace.Write("val : "+str(Node_flex))
				station_qnt_ori +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

		for (i4,j4) in zip(station4 ,station_mapping4):
			attr_name = str(j4)
			Node_flex=Product.Attr(str(i4)).GetValue()
			#Trace.Write("Node_flex: "+str(Node_flex))
			if Node_flex == que1 and add_node=="Honeywell":
				Trace.Write("val : "+str(Node_flex))
				station_qnt_add +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
		station_qnt = station_qnt_cms + station_qnt_dms + station_qnt_ori + station_qnt_add
	return int(server_qnt + station_qnt)

#CXCPQ-37569
def station_qnt2(Product,que,que1):
	Node_flex=""
	question1=[]
	station_qnt_dms=station_qnt_ori=station_qnt_add=0
	if Product.Name == "Experion Enterprise Group":
		server_qnt=Node_station(Product,que)
		station_qnt = 0
		Trace.Write("server_qnt---:"+str(server_qnt))
		#station Question
		station2=['DMS Flex Station Hardware Selection','DMS Console Station Hardware Selection','DMS TPS Station Hardware Selection','DMS Console Station Extension Hardware Selection']
		station3=['Flex Station Hardware Selection TPS','Console Station Hardware Selection','TPS Station Hardware Selection','Console Station Extension Hardware Selection']
		station4=['Station Type']
		#station Question Quantity mapping
		station_mapping2=['DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15']
		station_mapping3=['Flex Station Qty (0-60)','Console Station Qty (0-20)','TPS Station Qty (0-20)','Console Station Extension Qty  (0-15)']
		station_mapping4=['Additional Stations']
		#Node Supplier
		dms_node=Product.Attr('DMS Node Supplier').GetValue()
		ori_node=Product.Attr('Node Supplier').GetValue()
		add_node=Product.Attr('Node Supplier (Additional Station)').GetValue()

		for (i2,j2) in zip(station2 ,station_mapping2):
			attr_name = str(j2)
			Node_flex=Product.Attr(str(i2)).GetValue()
			#Trace.Write("Node_flex: "+str(Node_flex))
			if Node_flex == que1 and dms_node=="Honeywell":
				Trace.Write("val : "+str(Node_flex))
				station_qnt_dms +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

		for (i3,j3) in zip(station3 ,station_mapping3):
			attr_name = str(j3)
			Node_flex=Product.Attr(str(i3)).GetValue()
			#Trace.Write("Node_flex: "+str(Node_flex))
			if Node_flex == que1 and ori_node=="Honeywell":
				Trace.Write("val : "+str(Node_flex))
				station_qnt_ori +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

		for (i4,j4) in zip(station4 ,station_mapping4):
			attr_name = str(j4)
			Node_flex=Product.Attr(str(i4)).GetValue()
			#Trace.Write("Node_flex: "+str(Node_flex))
			if Node_flex == que1 and add_node=="Honeywell":
				Trace.Write("val : "+str(Node_flex))
				station_qnt_add +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
		station_qnt = station_qnt_dms + station_qnt_ori + station_qnt_add
	return int(server_qnt + station_qnt)
def station_qnt3(Product,que,que1):
	Node_flex=""
	question1=[]
	station_qnt_cms=station_qnt_dms=station_qnt_ori=station_qnt_add=0
	if Product.Name == "Experion Enterprise Group":
		server_qnt=Node_station(Product,que)
		station_qnt = 0
		Trace.Write("server_qnt---:"+str(server_qnt))
		#station Question
		station1=['CMS Flex Station Hardware Selection','CMS Console Station Hardware Selection','CMS TPS Station Hardware Selection','CMS Console Station Extension Hardware Selection']
		station2=['DMS Flex Station Hardware Selection','DMS Console Station Hardware Selection','DMS TPS Station Hardware Selection','DMS Console Station Extension Hardware Selection']  
		station3=['Station Type']
		#station Question Quantity mapping
		station_mapping1=['CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15']
		station_mapping2=['DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15']
		station_mapping3=['Additional Stations']
		#Node Supplier and TPM
		cms_node=Product.Attr('CMS Node Supplier').GetValue()
		dms_node=Product.Attr('DMS Node Supplier').GetValue()
		add_node=Product.Attr('Node Supplier (Additional Station)').GetValue()

		for (i1,j1) in zip(station1 ,station_mapping1):
			attr_name = str(j1)
			Node_flex=Product.Attr(str(i1)).GetValue()
			#Trace.Write("Node_flex: "+str(Node_flex))
			if Node_flex == que1 and cms_node=="Honeywell":
				Trace.Write("val : "+str(Node_flex))
				station_qnt_cms +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

		for (i2,j2) in zip(station2 ,station_mapping2):
			attr_name = str(j2)
			Node_flex=Product.Attr(str(i2)).GetValue()
			#Trace.Write("Node_flex: "+str(Node_flex))
			if Node_flex == que1 and dms_node=="Honeywell":
				Trace.Write("val : "+str(Node_flex))
				station_qnt_dms +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0


		for (i3,j3) in zip(station3 ,station_mapping3):
			attr_name = str(j3)
			Node_flex=Product.Attr(str(i3)).GetValue()
			#Trace.Write("Node_flex: "+str(Node_flex))
			if Node_flex == que1 and add_node=="Honeywell":
				Trace.Write("val : "+str(Node_flex))
				station_qnt_add +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
		station_qnt = station_qnt_cms + station_qnt_dms + station_qnt_add
	return int(server_qnt + station_qnt)

#CXCPQ-38407,38321,38405
def Node_station1(Product):
	Node_flex=""
	Redundancy=""
	question=[]
	server_qnt1 = server_qnt2 = server_qnt3 = server_qnt4 = 0
	if Product.Name == "Experion Enterprise Group":
		server_qnt=0
		Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
		Trace.Write(Redundancy)
		question=['FlexServer_NodeType','Flex Server Node Type']
		# Remote Peripheral Solution Type -- Wyse 5070 for 5+Displays
		RPS = ['Remote_Peripheral_Solution_Type_RPS','Remote Peripheral Solution Type (RPS) - (Flex Server -Cabinet)']
		# hardware question
		hwd_que = ['SVR_F_PER_DELL_Tower_RAID1','SVR_F_PER_DELL_Rack_RAID1','SVR_F_PER_HP_Tower_RAID1']

		#CXCPQ-38407 -- Wyse 5070 for 5+Displays
		for (i,j) in zip(question,RPS):
			Node_flex=Product.Attr(str(i)).GetValue()
			rps = Product.Attr(str(j)).GetValue()
			Trace.Write(Node_flex)
			if Redundancy=="Redundant" and Node_flex in hwd_que and rps=="Wyse 5070 for 5+Displays":
				server_qnt1=2
			elif Redundancy=="Non Redundant" and Node_flex in hwd_que and rps=="Wyse 5070 for 5+Displays":
				server_qnt1=1
		#CXCPQ-38407 -- 
		for (i,j) in zip(question,RPS):
			Node_flex=Product.Attr(str(i)).GetValue()
			rps = Product.Attr(str(j)).GetValue()
			Trace.Write(Node_flex)
			if Redundancy=="Redundant" and Node_flex in hwd_que and rps=="Wyse 5070 Optiplex 3000":
				server_qnt4=2
			elif Redundancy=="Non Redundant" and Node_flex in hwd_que and rps=="Wyse 5070 Optiplex 3000":
				server_qnt4=1
		#CXCPQ-38321 -- Pepperl+Fuchs BTC22 -- BTC12 replaced with BTC 22 (CXCPQ-119670)
		for (i,j) in zip(question,RPS):
			Node_flex=Product.Attr(str(i)).GetValue()
			rps = Product.Attr(str(j)).GetValue()
			#Trace.Write(Node_flex)
			if Redundancy=="Redundant" and Node_flex in hwd_que and rps=="Pepperl+Fuchs BTC22":
				server_qnt2=2
			elif Redundancy=="Non Redundant" and Node_flex in hwd_que and rps=="Pepperl+Fuchs BTC22":
				server_qnt2=1
		#CXCPQ-38405 -- Pepperl+Fuchs BTC24 -- BTC14 replaced with BTC 24 (CXCPQ-119670)
		for (i,j) in zip(question,RPS):
			Node_flex=Product.Attr(str(i)).GetValue()
			rps = Product.Attr(str(j)).GetValue()
			#Trace.Write(Node_flex)
			if Redundancy=="Redundant" and Node_flex in hwd_que and rps=="Pepperl+Fuchs BTC24":
				server_qnt3=2
			elif Redundancy=="Non Redundant" and Node_flex in hwd_que and rps=="Pepperl+Fuchs BTC24":
				server_qnt3=1
	return server_qnt1,server_qnt2,server_qnt3,server_qnt4

#CXCPQ-38407,38321,38405
def station_1(Product):
	Node_flex=""
	station_qnt_cms1=station_qnt_cms2=station_qnt_cms3=station_qnt_cms4=0
	station_qnt_dms1=station_qnt_dms2=station_qnt_dms3=station_qnt_dms4=0
	station_qnt1=station_qnt2=station_qnt3=server_qnt4 = 0
	if Product.Name == "Experion Enterprise Group":
		server_qnt1,server_qnt2,server_qnt3,server_qnt4 = Node_station1(Product)
		#station Question
		station1=['CMS Flex Station Hardware Selection','CMS Console Station Hardware Selection','CMS TPS Station Hardware Selection','CMS Console Station Extension Hardware Selection']
		station2=['DMS Flex Station Hardware Selection','DMS Console Station Hardware Selection','DMS TPS Station Hardware Selection','DMS Console Station Extension Hardware Selection']
		#station Question Quantity mapping
		station_mapping1=['CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15']
		station_mapping2=['DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15']
		# Remote Peripheral Solution Type -- Wyse 5070 for 5+Displays
		cms_RPS = Product.Attr('CMS Remote Peripheral Solution Type RPS').GetValue()
		dms_RPS = Product.Attr('DMS Remote Peripheral Solution Type RPS').GetValue()
		# hardware question
		hwd_que = ['STN_PER_DELL_Tower_RAID1','STN_PER_DELL_Rack_RAID1','STN_PER_HP_Tower_RAID1','STN_STD_DELL_Tower_NonRAID']
		# Required
		cms_required = Product.Attr('CMS Cabinet Mounting Stations required').GetValue()
		dms_required = Product.Attr('DMS Desk Mounting Stations required').GetValue()

		#CMS
		if cms_required != "No":
			#CXCPQ-38407 -- Wyse 5070 for 5+Displays
			for (i1,j1) in zip(station1 ,station_mapping1):
				attr_name = str(j1)
				Node_flex=Product.Attr(str(i1)).GetValue()
				#Trace.Write("Node_flex: "+str(Node_flex))
				if Node_flex in hwd_que and cms_RPS=="Wyse 5070 for 5+Displays":
					Trace.Write("val : "+str(Node_flex))
					station_qnt_cms1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
			#CXCPQ-38321 -- Pepperl+Fuchs BTC12
			for (i1,j1) in zip(station1 ,station_mapping1):
				attr_name = str(j1)
				Node_flex=Product.Attr(str(i1)).GetValue()
				#Trace.Write("Node_flex: "+str(Node_flex))  -- BTC14 replaced with BTC 24 (CXCPQ-119670)
				if Node_flex in hwd_que and cms_RPS=="Pepperl+Fuchs BTC22":
					Trace.Write("val : "+str(Node_flex))
					station_qnt_cms2 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
			#CXCPQ-38405 -- Pepperl+Fuchs BTC14
			for (i1,j1) in zip(station1 ,station_mapping1):
				attr_name = str(j1)
				Node_flex=Product.Attr(str(i1)).GetValue()
				#Trace.Write("Node_flex: "+str(Node_flex))  -- BTC14 replaced with BTC 24 (CXCPQ-119670)
				if Node_flex in hwd_que and cms_RPS=="Pepperl+Fuchs BTC24":
					Trace.Write("val : "+str(Node_flex))
					station_qnt_cms3 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

			for (i1,j1) in zip(station1 ,station_mapping1):
				attr_name = str(j1)
				Node_flex=Product.Attr(str(i1)).GetValue()
				#Trace.Write("Node_flex: "+str(Node_flex))
				if Node_flex in hwd_que and cms_RPS=="Wyse 5070 Optiplex 3000":
					Trace.Write("val : "+str(Node_flex))
					station_qnt_cms4 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
		#CMS
		if dms_required != "No":
			#CXCPQ-38407 -- Wyse 5070 for 5+Displays
			for (i2,j2) in zip(station2 ,station_mapping2):
				attr_name = str(j2)
				Node_flex=Product.Attr(str(i2)).GetValue()
				#Trace.Write("Node_flex: "+str(Node_flex))
				if Node_flex in hwd_que and dms_RPS=="Wyse 5070 for 5+Displays":
					Trace.Write("val : "+str(Node_flex))
					station_qnt_dms1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
			#CXCPQ-38321 -- Pepperl+Fuchs BTC12
			for (i2,j2) in zip(station2 ,station_mapping2):
				attr_name = str(j2)
				Node_flex=Product.Attr(str(i2)).GetValue()
				#Trace.Write("Node_flex: "+str(Node_flex))
				if Node_flex in hwd_que and dms_RPS=="Pepperl+Fuchs BTC22":
					Trace.Write("val : "+str(Node_flex))
					station_qnt_dms2 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
			#CXCPQ-38405 -- Pepperl+Fuchs BTC14
			for (i2,j2) in zip(station2 ,station_mapping2):
				attr_name = str(j2)
				Node_flex=Product.Attr(str(i2)).GetValue()
				#Trace.Write("Node_flex: "+str(Node_flex))
				if Node_flex in hwd_que and dms_RPS=="Pepperl+Fuchs BTC24":
					Trace.Write("val : "+str(Node_flex))
					station_qnt_dms3 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

			for (i2,j2) in zip(station2 ,station_mapping2):
				attr_name = str(j2)
				Node_flex=Product.Attr(str(i2)).GetValue()
				#Trace.Write("Node_flex: "+str(Node_flex))
				if Node_flex in hwd_que and dms_RPS=="Wyse 5070 Optiplex 3000":
					Trace.Write("val : "+str(Node_flex))
					station_qnt_dms4 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
		station_qnt1 = station_qnt_cms1 + station_qnt_dms1
		station_qnt2 = station_qnt_cms2 + station_qnt_dms2
		station_qnt3 = station_qnt_cms3 + station_qnt_dms3
		station_qnt4 = station_qnt_cms4 + station_qnt_dms4
	return server_qnt1 + station_qnt1,server_qnt2 + station_qnt2,server_qnt3 + station_qnt3,server_qnt4 + station_qnt4
#Trace.Write(str(station_1(Product)))

#CXCPQ-39498
#station1=station_1(Product)
#node_1=Node_station1(Product)

def orion_con(Product):
	orion_consol4=0
	if Product.Name == "Experion Enterprise Group":
		#server_qnt1=Node_station1(Product)[0]
		#Trace.Write("DRN:"+str(server_qnt1))
		station_qnt1=station_1(Product)[0]
		#Trace.Write("DRN1:"+str(station_qnt1))
		cms_required = Product.Attr('Node Supplier').GetValue()
		#Trace.Write(cms_required)
		dms_required = Product.Attr('Orion Console Remote Periph Sol Type (RPS)').GetValue()
		#Trace.Write(dms_required)
		bms_required = Product.Attr('Orion Console 2Position Base Unit (0-20)').GetValue()
		#Trace.Write(bms_required)
		fms_required = Product.Attr('Orion Console 3Position Base Unit (0-20)').GetValue()
		#Trace.Write(fms_required)
		if cms_required == "Honeywell" and dms_required == "Wyse 5070 for 5+Displays":
			orion_consol4=(((int(bms_required)*2)+(int(fms_required)*3))+(station_qnt1))
			#Trace.Write("Dhana2"+str(orion_consol4))
		else:
			orion_consol4=station_qnt1
			#Trace.Write("Dhana2"+str(orion_consol4))
	return orion_consol4
#Trace.Write(str(orion_con(Product)))

#cxcpq-39485
#station1=station_1(Product)
#node_1=Node_station1(Product)
def orion_consol(Product):
	orion_consol1=0
	if Product.Name == "Experion Enterprise Group":
		#server_qnt3=Node_station1(Product)[2]
		#Trace.Write("Anju1:"+str(server_qnt3))
		station_qnt3=station_1(Product)[2]
		#Trace.Write("Anju2:"+str(station_qnt3))
		cms_required = Product.Attr('Node Supplier').GetValue()
		#Trace.Write(cms_required)
		dms_required = Product.Attr('Orion Console Remote Periph Sol Type (RPS)').GetValue()
		#Trace.Write(dms_required)
		bms_required = Product.Attr('Orion Console 2Position Base Unit (0-20)').GetValue()
		#Trace.Write(bms_required)
		fms_required = Product.Attr('Orion Console 3Position Base Unit (0-20)').GetValue()
		#Trace.Write(fms_required)
		if cms_required == "Honeywell" and dms_required == "Pepperl+Fuchs BTC24":
			orion_consol1=(((int(bms_required)*2)+(int(fms_required)*3))+(station_qnt3))
			#Trace.Write("Dhana"+str(orion_consol1))
		else:
			orion_consol1=station_qnt3
			#Trace.Write("...."+str(orion_consol1))
	return orion_consol1
#Trace.Write(str(orion_consol(Product)))

#CXCPQ-37570
def station_2(Product):
	Node_flex=""
	station_qnt_dms=station_qnt_add=0
	if Product.Name == "Experion Enterprise Group":
		station_qnt = 0
		#station Question
		station2=['DMS Flex Station Hardware Selection','DMS Console Station Hardware Selection','DMS TPS Station Hardware Selection','DMS Console Station Extension Hardware Selection']
		station4=['Station Type']
		#station Question Quantity mapping
		station_mapping2=['DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15']
		station_mapping4=['Additional Stations']
		#Node Supplier
		dms_node=Product.Attr('DMS Node Supplier').GetValue()
		add_node=Product.Attr('Node Supplier (Additional Station)').GetValue()
		# HArdware Que
		que1 = 'STN_STD_DELL_Tower_NonRAID'
		# DMS req
		dms_required = Product.Attr('DMS Desk Mounting Stations required').GetValue()

		if dms_required != "No":
			for (i2,j2) in zip(station2 ,station_mapping2):
				attr_name = str(j2)
				Node_flex=Product.Attr(str(i2)).GetValue()
				#Trace.Write("Node_flex: "+str(Node_flex))
				if Node_flex == que1 and dms_node == "Honeywell":
					Trace.Write("val : "+str(Node_flex))
					station_qnt_dms +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

		for (i4,j4) in zip(station4 ,station_mapping4):
			attr_name = str(j4)
			Node_flex=Product.Attr(str(i4)).GetValue()
			#Trace.Write("Node_flex: "+str(Node_flex))
			if Node_flex == que1 and add_node =="Honeywell":
				Trace.Write("val : "+str(Node_flex))
				station_qnt_add +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
		station_qnt = station_qnt_dms + station_qnt_add
	return int(station_qnt)

#CXCPQ-37579, CXCPQ-37581
def station_3(Product):
	Node_flex=""
	station_qnt1 = station_qnt2 = 0
	if Product.Name == "Experion Enterprise Group":
		#station Question
		station1=['CMS Flex Station Hardware Selection','CMS Console Station Hardware Selection','CMS TPS Station Hardware Selection','CMS Console Station Extension Hardware Selection']
		station2=['DMS Flex Station Hardware Selection','DMS Console Station Hardware Selection','DMS TPS Station Hardware Selection','DMS Console Station Extension Hardware Selection']
		#station Question Quantity mapping
		station_mapping1=['CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15']
		station_mapping2=['DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15']
		# Remote Peripheral Solution Type -- Wyse 5070 for 5+Displays
		cms_RPS = Product.Attr('CMS Remote Peripheral Solution Type RPS').GetValue()
		dms_RPS = Product.Attr('DMS Remote Peripheral Solution Type RPS').GetValue()
		# RPS - Mounting Furniture
		cms_furniture = Product.Attr('CMS RPS Mounting Furniture').GetValue()
		dms_furniture = Product.Attr('DMS RPS Mounting Furniture').GetValue()
		# hardware question
		hwd_que = ['STN_PER_DELL_Tower_RAID1','STN_PER_DELL_Rack_RAID1','STN_PER_HP_Tower_RAID1','STN_STD_DELL_Tower_NonRAID']
		# Required
		cms_required = Product.Attr('CMS Cabinet Mounting Stations required').GetValue()
		dms_required = Product.Attr('DMS Desk Mounting Stations required').GetValue()

		# CMS
		if cms_required != "No":
			for (i,j) in zip(station1 ,station_mapping1):
				attr_name = str(j)
				Node_flex=Product.Attr(str(i)).GetValue()
				#Trace.Write("Node_flex: "+str(Node_flex))
				if Node_flex in hwd_que and cms_RPS=="Extio3-Single Mode Fiber" and cms_furniture == "Orion Console":
					# CXCPQ-37579
					station_qnt1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
				elif Node_flex in hwd_que and cms_RPS=="Extio3-Multi Mode Fiber" and cms_furniture == "Orion Console":
					# CXCPQ-37581
					station_qnt2 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
		# DMS
		if dms_required != "No":
			for (i,j) in zip(station2 ,station_mapping2):
				attr_name = str(j)
				Node_flex=Product.Attr(str(i)).GetValue()
				#Trace.Write("Node_flex: "+str(Node_flex))
				if Node_flex in hwd_que and dms_RPS=="Extio3-Single Mode Fiber" and dms_furniture == "Orion Console":
					# CXCPQ-37579
					station_qnt1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
				elif Node_flex in hwd_que and dms_RPS=="Extio3-Multi Mode Fiber" and dms_furniture == "Orion Console":
					# CXCPQ-37581
					station_qnt2 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

	return int(station_qnt1), int(station_qnt2)
#Trace.Write(str(station_3(Product)))

#CXCPQ-39499

def orion_consol2(Product):
	orion_consol3=0
	if Product.Name == "Experion Enterprise Group":
		'''server_qnt3=Node_station1(Product)[2]
		Trace.Write("Anju10:"+str(server_qnt3))'''
		station_qnt1=station_3(Product)[0]
		#Trace.Write("Anj:"+str(station_qnt1))
		cms_required = Product.Attr('Node Supplier').GetValue()
		#Trace.Write(cms_required)
		dms_required = Product.Attr('Orion Console Remote Periph Sol Type (RPS)').GetValue()
		#Trace.Write(dms_required)
		bms_required = Product.Attr('Orion Console 2Position Base Unit (0-20)').GetValue()
		#Trace.Write(bms_required)
		fms_required = Product.Attr('Orion Console 3Position Base Unit (0-20)').GetValue()
		#Trace.Write(fms_required)
		if cms_required == "Honeywell" and dms_required == "Extio3-Single Mode Fiber":
			orion_consol3=(((int(bms_required)*2)+(int(fms_required)*3))+(int(station_qnt1)))
			#Trace.Write("Nagane2"+str(orion_consol3))
		else:
			orion_consol3=int(station_qnt1)
	return orion_consol3
#Trace.Write(str(orion_consol2(Product)))

#CXCPQ-39500
def orion_consol8(Product):
	orion_consol9=0
	if Product.Name == "Experion Enterprise Group":
		'''server_qnt3=Node_station1(Product)[2]
		Trace.Write("Anju1:"+str(server_qnt3))'''
		station_qnt2=station_3(Product)[1]
		#Trace.Write("Anju3:"+str(station_qnt2))
		cms_required = Product.Attr('Node Supplier').GetValue()
		#Trace.Write(cms_required)
		dms_required = Product.Attr('Orion Console Remote Periph Sol Type (RPS)').GetValue()
		#Trace.Write(dms_required)
		bms_required = Product.Attr('Orion Console 2Position Base Unit (0-20)').GetValue()
		#Trace.Write(bms_required)
		fms_required = Product.Attr('Orion Console 3Position Base Unit (0-20)').GetValue()
		#Trace.Write(fms_required)
		if cms_required == "Honeywell" and dms_required == "Extio3-Multi Mode Fiber":
			orion_consol9=(((int(bms_required)*2)+(int(fms_required)*3))+(int(station_qnt2)))
			#Trace.Write("Nagane5"+str(orion_consol9))
		else:
			orion_consol9=int(station_qnt2)
	return orion_consol9
#Trace.Write(str(orion_consol8(Product)))

#CXCPQ-37577, CXCPQ-37578
def station_4(Product):
	Node_flex=""
	station_qnt1 = station_qnt2 = 0
	if Product.Name == "Experion Enterprise Group":
		Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
		#server Question
		question=Product.Attr('Flex Server Node Type').GetValue()
		#Trace.Write("Q:"+str(question))
		# Remote Peripheral Solution Type 
		RPS = Product.Attr('Remote Peripheral Solution Type (RPS) - (Flex Server -Cabinet)').GetValue()
		#Trace.Write("rps:"+str(RPS))
		# hardware question
		hwd_svr = ['SVR_F_PER_DELL_Tower_RAID1','SVR_F_PER_DELL_Rack_RAID1','SVR_F_PER_HP_Tower_RAID1']
		# RPS Mounting Furniture (Flex Server Cabinet)
		RPS_furniture = Product.Attr('RPS Mounting Furniture (Flex Server Cabinet)').GetValue()
		#Trace.Write("RPS_furniture:"+str(RPS_furniture))

		if question in hwd_svr:
			if RPS == "Extio3-Single Mode Fiber" and RPS_furniture == "Desk":
				Trace.Write("cond 1 worker")
				if Redundancy == "Redundant":
					station_qnt1 += 2
				elif Redundancy == "Non Redundant":
					station_qnt1 += 1
			elif RPS == "Extio3-Multi Mode Fiber" and RPS_furniture == "Desk":
				Trace.Write("cond 2 worker")
				if Redundancy == "Redundant":
					station_qnt2 += 2
				elif Redundancy == "Non Redundant":
					station_qnt2 += 1

		#station Question
		station1=['CMS Flex Station Hardware Selection','CMS Console Station Hardware Selection','CMS TPS Station Hardware Selection','CMS Console Station Extension Hardware Selection']
		station2=['DMS Flex Station Hardware Selection','DMS Console Station Hardware Selection','DMS TPS Station Hardware Selection','DMS Console Station Extension Hardware Selection']
		#station Question Quantity mapping
		station_mapping1=['CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15']
		station_mapping2=['DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15']
		# Remote Peripheral Solution Type 
		cms_RPS = Product.Attr('CMS Remote Peripheral Solution Type RPS').GetValue()
		dms_RPS = Product.Attr('DMS Remote Peripheral Solution Type RPS').GetValue()
		# RPS - Mounting Furniture
		cms_furniture = Product.Attr('CMS RPS Mounting Furniture').GetValue()
		dms_furniture = Product.Attr('DMS RPS Mounting Furniture').GetValue()
		# hardware question
		hwd_que = ['STN_PER_DELL_Tower_RAID1','STN_PER_DELL_Rack_RAID1','STN_PER_HP_Tower_RAID1','STN_STD_DELL_Tower_NonRAID']
		# Required
		cms_required = Product.Attr('CMS Cabinet Mounting Stations required').GetValue()
		dms_required = Product.Attr('DMS Desk Mounting Stations required').GetValue()

		# CMS
		if cms_required != "No":
			for (i,j) in zip(station1 ,station_mapping1):
				attr_name = str(j)
				Node_flex=Product.Attr(str(i)).GetValue()
				#Trace.Write("Node_flex: "+str(Node_flex))
				if Node_flex in hwd_que and cms_RPS=="Extio3-Single Mode Fiber" and cms_furniture == "Desk Console":
					# CXCPQ-37579
					station_qnt1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
				elif Node_flex in hwd_que and cms_RPS=="Extio3-Multi Mode Fiber" and cms_furniture == "Desk Console":
					# CXCPQ-37581
					station_qnt2 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
		# DMS
		if dms_required != "No":
			for (i,j) in zip(station2 ,station_mapping2):
				attr_name = str(j)
				Node_flex=Product.Attr(str(i)).GetValue()
				Trace.Write("Node_flex: "+str(Node_flex))
				if Node_flex in hwd_que and dms_RPS=="Extio3-Single Mode Fiber" and dms_furniture == "Desk Console":
					# CXCPQ-37579
					station_qnt1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
				elif Node_flex in hwd_que and dms_RPS=="Extio3-Multi Mode Fiber" and dms_furniture == "Desk Console":
					# CXCPQ-37581
					station_qnt2 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

	return int(station_qnt1), int(station_qnt2)