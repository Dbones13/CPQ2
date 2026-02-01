if Product.Attr('PERF_ExecuteScripts').GetValue() != '':
	import GS_BOM_exp_ent_grp, GS_Exp_grp_parts, GS_Exp_grp_parts2
	import GS_PS_Exp_Ent_BOM
	import GS_BOM_Multi_Window_Sup
	import GS_Exp_ENT_BOM_Calcs,GS_Exp_ENT_BOM_Calcs1
	import Gs_EXpEnt_Grp_BOM_calcs
	import GS_EXP_NetworkStorage
	#Product.ExecuteRulesOnce = True

	Product.Attr('qty_405').AssignValue('0')
	Product.Attr('qty_407').AssignValue('0')
	Product.Attr('qty_579').AssignValue('0')
	Product.Attr('qty_581').AssignValue('0')

	FSNT = Product.Attr("Flex Server Node Type").GetValue()
	ESR =  Product.Attr('Experion Software Release').GetValue()
	DMSR = Product.Attr('DMS Desk Mounting Stations required').GetValue()
	OSR  =  Product.Attr('Orion Stations required').GetValue()
	CMSR = Product.Attr('CMS Cabinet Mounting Stations required').GetValue()
	EST = Product.Attr('Experion Server Type').GetValue()
	LOB = Quote.GetCustomField('Booking Lob').Content
	SM  = Product.Attr('Server Mounting').GetValue()
	FSNT = Product.Attr("Flex Server Node Type").GetValue()
	#Added By Ravika for ----->CCEECOMMBR-7729
	try:
		SNTD= Product.Attr("Server Node Type_desk").GetValue()
	except:
		SNTD = ""
	try:
		SNTC= Product.Attr("Server_NodeType").GetValue()
	except:
		SNTC = ""

	Tower_station_qty=GS_BOM_exp_ent_grp.station_qnt1(Product,'SVR_F_PER_DELL_Tower_RAID1','STN_PER_DELL_Tower_RAID1')
	Rack_station_qty =GS_BOM_exp_ent_grp.station_qnt1(Product,'SVR_F_PER_DELL_Rack_RAID1','STN_PER_DELL_Rack_RAID1')
	HP_Tower_station_qty=GS_BOM_exp_ent_grp.station_qnt1(Product,'SVR_F_PER_HP_Tower_RAID1','STN_PER_HP_Tower_RAID1')
	CMS_DMS_Rack_station_qty=GS_BOM_exp_ent_grp.station_qnt3(Product,'SVR_F_PER_DELL_Rack_RAID1','STN_PER_DELL_Rack_RAID1')

	#CXCPQ-44532
	qt10k,qt5k,qt2k,qt1k,qt100 = GS_Exp_grp_parts.get_QVCS(Product)
	if qt10k > 0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC10K",qt10k)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC10K",0)
	if qt5k > 0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC05K",qt5k)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC05K",0)
	if qt2k > 0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC02K",qt2k)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC02K",0)
	if qt1k > 0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC01K",qt1k)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC01K",0)
	if qt100 > 0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC100",qt100)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-QVC100",0)

	#CXCPQ-43659
	try:
		SNT=Product.Attributes.GetByName("Server Node Type EBR").GetValue()
		TPM=Product.Attributes.GetByName("Trusted Platform Module TPM EBR").GetValue()
		NS=Product.Attributes.GetByName("Node Supplier Server EBR").GetValue()
		DSS=Product.Attributes.GetByName("Display Size server EBR").GetValue()
		DSP=Product.Attributes.GetByName("Display Supplier EBR").GetValue()
		ADHD=Product.Attr('Additional Hard Disk Server EBR').GetValue()
		TPMT=Product.Attr('Trusted Platform Module_TPM').GetValue()
		#CXDEV-7720--RP
		Node_Sup_Desk=Product.Attributes.GetByName("Node Supplier_server").GetValue()
		Node_Sup_Cab=Product.Attributes.GetByName("Node_Supplier_Server").GetValue()
	except:
		SNT=""
		TPM=""
		NS=""
		DSS=""
		DSP=""
		TPMT=""
		Node_Sup_Desk=""
		Node_Sup_Cab=""

	SRR=Product.Attributes.GetByName("Server Redundancy Requirement?").GetValue()
	BackRelease=Product.Attr('Experion Backup Restore Software Release').GetValue()

	Trace.Write(SNT)
	Trace.Write(TPM)
	Trace.Write(NS)
	Trace.Write(SRR)

	MZ_PCSV85SR=0
	MZ_PCSR01SR=0 
	MZ_PCSR02SR=0 
	#MZ_PCSR82SR=0 
	MZ_PCSR04SR=0
	MZ_PCIS02SR=0
	MZ_PCST01SR=0 
	MZ_PCST02SR=0
	#MZ_PCST82SR=0
	MZ_PCEH15SR=0

	TP_FPD211_100SR=0
	TP_FPD211_200SR=0
	TP_FPW271SR=0
	TP_FPW241SR=0
	TP_FPW231SR=0

	EP_COAS16SR=0
	MZ_SQLCL4SR=0
	EP_COAS19SR=0

	serever_qntnode_Final=0
	serever_qntnode_FinalR520=0

	SR16=1
	SR19=1
	#CXCPQ-45056
	SR=1
	#CXCPQ-45056
	if Product.Attributes.GetByName("EBR_Server_Check").GetValue()=="No":
		SR=0

	if DSS=="21.33 inch NTS" and DSP=="Honeywell":
		TP_FPD211_100SR=SR
		TP_FPD211_200SR=SR
	if DSS=="27 inch NTS NEC" and DSP=="Honeywell":
		TP_FPW271SR=SR
	if DSS=="24 inch NTS NEC" and DSP=="Honeywell":
		TP_FPW241SR=SR
	if DSS=="23 inch NTS" and DSP=="Honeywell":
		TP_FPW231SR=SR

	if SNT=="SVR_PER_HP_Rack_RAID5" and TPM=="Yes" and NS=="Honeywell":
		MZ_PCSV85SR=SR

	if SNT=="SVR_STD_DELL_Rack_RAID1" and TPM and NS=="Honeywell":
		MZ_PCSR01SR=SR 

	if SNT=="SVR_PER_DELL_Rack_RAID1" and TPM and NS=="Honeywell":
		MZ_PCSR02SR=SR 

	# if SNT=="SVR_PER_DELL_Rack_RAID1" and TPM=="No" and NS=="Honeywell":
	# 	MZ_PCSR82SR=SR #cxcpq-103991

	if SNT=="SVR_PER_DELL_Rack_RAID5" and TPM=="Yes" and NS=="Honeywell":
		MZ_PCSR04SR=SR
	if SNT=="SVR_PER_DELL_Rack_RAID5" and TPM=="Yes" and NS=="Honeywell" and ADHD=="Yes":
		MZ_PCEH15SR=SR
	if SNT=="SVR_PER_DELL_Rack_RAID1_RUG" and TPM=="Yes" and NS=="Honeywell":
		MZ_PCIS02SR=SR

	if SNT=="SVR_STD_DELL_Tower_RAID1" and TPM and NS=="Honeywell":
		MZ_PCST01SR=SR

	if SNT=="SVR_PER_DELL_Tower_RAID1" and TPM and NS=="Honeywell":
		MZ_PCST02SR=SR
	# if SNT=="SVR_PER_DELL_Tower_RAID1" and TPM=="No" and NS=="Honeywell":
	# 	MZ_PCST82SR=SR

	if NS=="Honeywell" and (ESR=="R510" or ESR=="R511"):
		EP_COAS16SR=SR16
	if NS=="Honeywell" and ESR=="R520" and TPM and (TPM=="Yes" or SNT in ('SVR_STD_DELL_Rack_RAID1','SVR_PER_DELL_Rack_RAID1','SVR_STD_DELL_Tower_RAID1','SVR_PER_DELL_Tower_RAID1')):
		EP_COAS19SR=SR19

	if SNT!="" and NS=="Honeywell" and TPM and (TPM=="Yes" or SNT in ('SVR_STD_DELL_Rack_RAID1','SVR_PER_DELL_Rack_RAID1','SVR_STD_DELL_Tower_RAID1','SVR_PER_DELL_Tower_RAID1')):
		MZ_SQLCL4SR=SR

	#CXCPQ-41692,CXCPQ-41693,CXCPQ-41694,CXCPQ-41695
	qty_TP_DUIKBN_100,qty_TP_DUIKBT_101,qty_TP_DSOEP1_100,qty_TP_DIKBNA_100 = GS_Exp_grp_parts.get_Vals(Product)
	if qty_TP_DUIKBN_100 > 0:
		Trace.Write("41692")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-DUIKBN-100",qty_TP_DUIKBN_100)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-DUIKBN-100",0)
	if qty_TP_DUIKBT_101 > 0:
		Trace.Write("41693")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-DUIKBT-101",qty_TP_DUIKBT_101)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-DUIKBT-101",0)
	if qty_TP_DSOEP1_100 > 0:
		Trace.Write("41694")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-DSOEP1-100",qty_TP_DSOEP1_100)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-DSOEP1-100",0)
	if qty_TP_DIKBNA_100 > 0:
		Trace.Write("41695")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-DIKBNA-100",qty_TP_DIKBNA_100)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-DIKBNA-100",0)

	#CXCPQ-39211
	exp_qty = GS_Exp_grp_parts.get_Ext(Product)
	if exp_qty > 0:
		Trace.Write("39211")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-STACEX",exp_qty)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-STACEX",0)

	#CXCPQ-39210
	STAC10,STAC05,STAC01 = GS_Exp_grp_parts.get_Console(Product)
	if STAC10 > 0:
		Trace.Write("39210")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-STAC10",STAC10)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-STAC10",0)
	if STAC05 > 0:
		Trace.Write("39210")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-STAC05",STAC05)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-STAC05",0)
	if STAC01 > 0:
		Trace.Write("39210")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-STAC01",STAC01)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-STAC01",0)

	#CXCPQ-39206 + CXCPQ-45647
	STAT10,STAT05,STAT01 = GS_Exp_grp_parts.get_license(Product)
	if STAT10 > 0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-STAT10",STAT10)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-STAT10",0)
	if STAT05 > 0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-STAT05",STAT05)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-STAT05",0)
	if STAT01 > 0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-STAT01",STAT01)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-STAT01",0)

	#CXCPQ-39069,CXCPQ-39114
	ikb_qty = GS_Exp_grp_parts.get_IKB(Product)
	if Product.Attr('CE_Site_Voltage').GetValue() == "120V" and ikb_qty > 0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-OPADP1-100",ikb_qty)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-OPADP1-100",0)
	if Product.Attr('CE_Site_Voltage').GetValue() == "240V" and ikb_qty > 0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-OPADP1-200",ikb_qty)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-OPADP1-200",0)

	#CXCPQ-38883,CXCPQ-38879,7661-RP, CXDEV-8356
	qty_TP_FPWT01_100,qty_TP_FPW231 = GS_Exp_grp_parts2.get_23(Product,"24 inch Touch HP")
	if qty_TP_FPWT01_100>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPT241",qty_TP_FPWT01_100)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPT241",0)
	if qty_TP_FPW231+TP_FPW231SR>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPW231",qty_TP_FPW231+TP_FPW231SR)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPW231",0)
	#CXCPQ-38872
	qty_TP_FPH552 = GS_Exp_grp_parts2.get_55(Product)
	if qty_TP_FPH552>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPH552",qty_TP_FPH552)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPH552",0)

	#CXCPQ-38880, (CXCPQ-38876, CXCPQ-38875), CXCPQ-38882 + CXCPQ-43654 EBR addition.
	qty_TP_FPW271, qty_TP_FPD211_200, qty_TP_FPT211_100 = GS_Exp_grp_parts2.get_parts(Product,"27 inch NTS NEC")
	if qty_TP_FPW271 + TP_FPW271SR>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPW271",qty_TP_FPW271 + TP_FPW271SR)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPW271",0)
	if Product.Attr('CE_Site_Voltage').GetValue() == "240V" and qty_TP_FPD211_200 + TP_FPD211_200SR > 0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPD211-200",qty_TP_FPD211_200 + TP_FPD211_200SR)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPD211-200",0)
	if Product.Attr('CE_Site_Voltage').GetValue() == "120V" and qty_TP_FPD211_200 + TP_FPD211_100SR > 0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPD211-100",qty_TP_FPD211_200 + TP_FPD211_100SR)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPD211-100",0)
	if qty_TP_FPT211_100>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPT211-100",qty_TP_FPT211_100)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPT211-100",0)
	# Comment 233 to 245 as per CXCPQ-43807
	#CXCPQ-39104, CXCPQ-39105
	#CXCPQ-38881 + CXCPQ-43654 EBR Addition
	#TP_FPW241_qty = GS_Exp_grp_parts.get_part(Product)
	TP_FPW241_qty, qty_TP_FPD211_200, qty_TP_FPT211_100 = GS_Exp_grp_parts2.get_parts(Product,"24 inch NTS NEC")
	Trace.Write(TP_FPW241_qty)
	if TP_FPW241_qty + TP_FPW241SR > 0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPW241",TP_FPW241_qty + TP_FPW241SR)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-FPW241",0)
	#CXDEV-7725-RP
	if ESR=='R530':
		MZ_PCWS86_qty = GS_BOM_exp_ent_grp.station_qnt1(Product,'SVR_F_PER_HP_Tower_RAID1','STN_PER_HP_Tower_RAID1')
		if MZ_PCWS86_qty > 0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWS86",MZ_PCWS86_qty)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWS86",0)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWS86",0)
	#CCEECOMMBR-7730--RP
	if (CMSR == "Yes" or DMSR == "Yes" or EST == 'Flex Server'):
		qty1_TP_THNCL9_100, qty2_TP_THNCL9_100, qty3_TP_THNCL9_100,qty4_TP_THNCL9_100 = GS_BOM_exp_ent_grp.station_1(Product)
		if qty4_TP_THNCL9_100 >0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-THNCL9-100",qty4_TP_THNCL9_100)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-THNCL9-100",0)
	#for CCEECOMMBR-7724 by Kaousalya Adala
	if (ESR == "R530") and LOB=="PAS" and (CMSR == "Yes" or DMSR == "Yes" or EST == 'Flex Server'):
		if CMS_DMS_Rack_station_qty>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWR01",CMS_DMS_Rack_station_qty)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWR01",0)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWR01",0)

	#for CCEECOMMBR-7727 by Kaousalya Adala
	Total_station_qty=0
	if (ESR == "R530"):
		Total_station_qty=Tower_station_qty+Rack_station_qty+HP_Tower_station_qty
		if Total_station_qty>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-COAW21",Total_station_qty)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-COAW21",0)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-COAW21",0)

	#for 7721 story
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCSV85",0)

	#CXCPQ-37562.....implemented in CXCPQ-43301 no longer need this story.
	MZ_PCST01_qty = GS_BOM_exp_ent_grp.server_qnt1(Product,'SVR_STD_DELL_Tower_RAID1','Yes')
	Trace.Write(MZ_PCST01_qty) 
	#CXCPQ-37560.....implemented in CXCPQ-43301 no longer need this story.
	MZ_PCSR82_qty = GS_BOM_exp_ent_grp.server_qnt2(Product,'SVR_PER_DELL_Rack_RAID1','No')
	Trace.Write(MZ_PCSR82_qty)  
	#CXCPQ-37563.....implemented in CXCPQ-43301 no longer need this story.
	MZ_PCSR01_qty = GS_BOM_exp_ent_grp.server_qnt2(Product,'SVR_STD_DELL_Rack_RAID1','Yes')
	Trace.Write(MZ_PCSR01_qty)  
	#CXCPQ-37564.....implemented in CXCPQ-43301 no longer need this story.
	MZ_PCSV65_qty = GS_BOM_exp_ent_grp.server_qnt1(Product,'SVR_PER_DELL_Rack_RAID5','Yes')

	# for CCEECOMMBR-7716 Jira story.---By Saurabh Karale.
	MZ_PCWS85_qty = GS_BOM_exp_ent_grp.station_qnt2(Product,'SVR_F_PER_HP_Tower_RAID1','STN_PER_HP_Tower_RAID1')
	Trace.Write(MZ_PCWS85_qty)
	ESR = Product.Attr('Experion Software Release').GetValue()
	DMSR = Product.Attr('DMS Desk Mounting Stations required').GetValue()
	OSR = Product.Attr('Orion Stations required').GetValue()
	CMSR = Product.Attr('CMS Cabinet Mounting Stations required').GetValue()
	EST = Product.Attr('Experion Server Type').GetValue()
	'''if (ESR == 'R530') and (DMSR == 'Yes' or OSR == 'Yes' or EST == 'Flex Server'):
		if MZ_PCWS85_qty > 0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWS85",MZ_PCWS85_qty)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWS85",0)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWS85",0)'''

	#CXCPQ-7717
	MZ_PCWS14_qty = GS_BOM_exp_ent_grp.station_2(Product)
	Trace.Write(MZ_PCWS14_qty)
	'''if MZ_PCWS14_qty > 0:
		Trace.Write("37570")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWS14",MZ_PCWS14_qty)
	else:
		Trace.Write("37570")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWS14",0)'''

	# for CCEECOMMBR-7718 Jira story--- By Saurabh Karale.
	NE_NICS04_qty = GS_BOM_exp_ent_grp.station_qnt1(Product,'SVR_F_PER_DELL_Tower_RAID1','STN_PER_DELL_Tower_RAID1')
	Trace.Write(NE_NICS04_qty)
	if NE_NICS04_qty > 0:
		if (ESR == 'R520' or ESR == 'R510' or ESR == 'R511') and (DMSR == 'Yes' or OSR == 'Yes' or CMSR == 'Yes' or EST == 'Flex Server'):
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","NE-NICS04",NE_NICS04_qty)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","NE-NICS04",0)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","NE-NICS04",0)
	if ESR=='R530':
		NE_NICS04_qty = GS_BOM_exp_ent_grp.station_qnt1(Product,'','STN_STD_DELL_Tower_NonRAID')
		if NE_NICS04_qty > 0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","NE-NICS04",NE_NICS04_qty)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","NE-NICS04",0)
	if (ESR == 'R520' or ESR == 'R510' or ESR == 'R511'):
		NE_NICS04_qty = GS_BOM_exp_ent_grp.station_qnt1(Product,'SVR_F_PER_DELL_Tower_RAID1','STN_PER_DELL_Tower_RAID1')
		if NE_NICS04_qty > 0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","NE-NICS04",NE_NICS04_qty)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","NE-NICS04",0)
	# CCEECOMMBR-7723 Jira Story (For experion system release R530)-----by saurabh karale.
	MZ_PCWT01_qty = GS_BOM_exp_ent_grp.station_qnt1(Product,'SVR_F_PER_DELL_Tower_RAID1','STN_PER_DELL_Tower_RAID1')
	Trace.Write(MZ_PCWT01_qty)
	if MZ_PCWT01_qty > 0:
		if ESR == 'R530' and (DMSR == 'Yes' or OSR == 'Yes' or CMSR == 'Yes' or EST == 'Flex Server'):
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWT01",MZ_PCWT01_qty)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWT01",0)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWT01",0)
	# For CCEECOMMBR-7726 jira story(MZ-PCWS15 PartNumber)--- By Saurabh Karale.
	if ESR=='R530':
		MZ_PCWS15_qty = GS_BOM_exp_ent_grp.station_qnt1(Product,'','STN_STD_DELL_Tower_NonRAID')
		if MZ_PCWS15_qty > 0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWS15",MZ_PCWS15_qty)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWS15",0)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCWS15",0)

	if (ESR=='R530'or ESR=='R520'):
		MZ_PCSV85_qty = GS_Exp_ENT_BOM_Calcs1.station_qnt1(Product,'SVR_PER_HP_Rack_RAID5','SVR_PER_HP_Rack_RAID5')
		if  MZ_PCSV85_qty+MZ_PCSV85SR > 0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCSV85",MZ_PCSV85_qty+MZ_PCSV85SR)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCSV85",0)

	#CXCPQ-37577, CXCPQ-37578
	qty_77,qty_78 = GS_BOM_exp_ent_grp.station_4(Product)
	if qty_77 > 0:
		Trace.Write("37577")
		Trace.Write(qty_77)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-RPSF03-100",qty_77)
	else:
		Trace.Write("37577")
		Trace.Write(qty_77)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-RPSF03-100",0)
	if qty_78 > 0:
		Trace.Write("37578")
		Trace.Write(qty_78)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-RPSF03-110",qty_78)
	else:
		Trace.Write("37578")
		Trace.Write(qty_78)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-RPSF03-110",0)

	#CXCPQ-37579, CXCPQ-37581
	qty_79,qty_81 = GS_BOM_exp_ent_grp.station_3(Product)
	if qty_79 > 0:
		Product.Attr('qty_579').AssignValue(str(qty_79))
		Trace.Write("37579")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-RPSF03-400",qty_79)
	else:
		Trace.Write("37579")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-RPSF03-400",0)
	if qty_81 > 0:
		Product.Attr('qty_581').AssignValue(str(qty_81))
		Trace.Write("37581")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-RPSF03-410",qty_81)
	else:
		Trace.Write("37581")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-RPSF03-410",0)

	#CXCPQ-39499-DS
	orion_qty2=GS_BOM_exp_ent_grp.orion_consol2(Product)
	if orion_qty2>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-RPSF03-400",orion_qty2)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-RPSF03-400",0)

	#CXCPQ-39500-DS
	orion_qty3=GS_BOM_exp_ent_grp.orion_consol8(Product)
	if orion_qty3>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-RPSF03-410",orion_qty3)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-RPSF03-410",0)

	#CXCPQ-38407,38321,38405
	qty1,qty2,qty3,qty4 = GS_BOM_exp_ent_grp.station_1(Product)
	if qty1 > 0:
		Trace.Write(qty1)
		Product.Attr('qty_407').AssignValue(str(qty1))
		Trace.Write("38407")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-THNCL5-900",qty1)
	else:
		Trace.Write("38407")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-THNCL5-900",0)
	if qty2 > 0:
		Trace.Write(qty2)
		Trace.Write("38321")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-THNR01-100",qty2)
	else:
		Trace.Write("38321")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-THNR01-100",0)
	if qty3 > 0:
		Trace.Write(qty3)
		Product.Attr('qty_405').AssignValue(str(qty3))
		Trace.Write("38405")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-THNR02-100",qty3)
	else:
		Trace.Write("38405")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-THNR02-100",0)

	#CXCPQ-39498-DS
	orion_qty1=GS_BOM_exp_ent_grp.orion_con(Product)
	if orion_qty1>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-THNCL5-900",orion_qty1)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-THNCL5-900",0)

	#CXCPQ_39485-DS
	orion_qty=GS_BOM_exp_ent_grp.orion_consol(Product)
	if orion_qty>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-THNR02-100",orion_qty)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TP-THNR02-100",0)

	#CXCPQ-38410
	EP_SMWIN1_qty = GS_BOM_Multi_Window_Sup.Node_station(Product)
	Trace.Write(EP_SMWIN1_qty)
	if EP_SMWIN1_qty > 0:
		Trace.Write("38410")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-SMWIN1",EP_SMWIN1_qty)
	else:
		Trace.Write("38410")
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-SMWIN1",0)

	#Lahu Giri
	Qnt1,Qnt2,Qnt3,Qnt4,Qnt5,Qnt6,Qnt7,Qnt8,Qnt9=GS_Exp_ENT_BOM_Calcs.EXP_Bom_TPM(Product)

	serever_qnt_T,serever_qntnode_T,station_37200=GS_Exp_ENT_BOM_Calcs.server_qnt1(Product)
	station_svr37545=GS_Exp_ENT_BOM_Calcs.QNTCXCPQ_37545(Product)
	svr_hardt37547=GS_Exp_ENT_BOM_Calcs.Qnt37547(Product)
	svr_hardt37552,svr_hardt16gb,svr_hardt16gb1=Gs_EXpEnt_Grp_BOM_calcs.QNTCXCPQ_37552(Product)
	svr_MZ_PCIS02_2,svr_MZ_PCIS02_4,svr_MZ_PCIS02_6,svr_MZ_PCIS02_8,svr_MZ_PCIS02_10=Gs_EXpEnt_Grp_BOM_calcs.MZ_PCIS02(Product)
	'''if (Qnt2+MZ_PCSR01SR >0) :
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCSR01",Qnt2+MZ_PCSR01SR)
	if (Qnt3+MZ_PCSR02SR >0) :
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCSR02",Qnt3+MZ_PCSR02SR)
	if (Qnt4+MZ_PCSR82SR >0):
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCSR82",Qnt4+MZ_PCSR82SR) cxcpq-103991'''
	ex_qty = [Qnt1,Qnt2,Qnt3,Qnt4,Qnt5,Qnt6,Qnt7,Qnt8,Qnt9]
	qty = {'MZ-PCSR05':[1,MZ_PCSR01SR],'MZ-PCSR06':[2,MZ_PCSR02SR],'MZ-PCST03':[6,MZ_PCST01SR],'MZ-PCST04':[7,MZ_PCST02SR]}
	for partnum in qty.keys():
		Trace.Write('partnum '+str([partnum,qty.get(partnum)[1]]))
		if ex_qty[qty[partnum][0]] + qty[partnum][1] >0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary",partnum,ex_qty[qty[partnum][0]]+qty[partnum][1])
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary",partnum,0)
	if Qnt5+MZ_PCSR04SR >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCSR04",Qnt5+MZ_PCSR04SR)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCSR04",0)
	if Qnt6+MZ_PCIS02SR >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCIS02",Qnt6+MZ_PCIS02SR)
		try:
			MRC = Product.Attr("Marine_Requirement_Cabinet").GetValue()
			MRD = Product.Attr("Marine_Requirement_Desk").GetValue()
		except:
			MRC = ''
			MRD = ''
		if MRC == 'Yes' or MRD == 'Yes':
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCIS50",Qnt6+MZ_PCIS02SR)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCIS50",0)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCIS02",0)
	'''if (Qnt7+MZ_PCST01SR >0) :
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCST01",Qnt7+MZ_PCST01SR)
	if (Qnt8+MZ_PCST02SR >0):
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCST02",Qnt8+MZ_PCST02SR)
	if (Qnt9+MZ_PCST82SR >0):
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCST82",Qnt9+MZ_PCST82SR)'''
	#CXCPQ-37198 added by lahu + CXCPQ-43651 EBR Addon,CXDEV-7719-RP
	if serever_qnt_T + MZ_SQLCL4SR >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-SQLCL4",serever_qnt_T + MZ_SQLCL4SR)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-SQLCL4",0)

	#CXCPQ-37543,CXCPQ-37544 + CXCPQ-43652 and CXCPQ-43653 EBR Addon
	Release=Product.Attr('Experion Software Release').GetValue()
	if Release=='R510' or Release=='R511':
		serever_qntnode_Final=serever_qntnode_T
	if serever_qntnode_Final + EP_COAS16SR >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-COAS16",serever_qntnode_Final + EP_COAS16SR)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-COAS16",0)

	if Release=='R520':
		stn_qty= GS_BOM_exp_ent_grp.station_qnt1(Product,'','STN_PER_DELL_Tower_RAID2')
		serever_qntnode_FinalR520=serever_qntnode_T + stn_qty
	if serever_qntnode_FinalR520 + EP_COAS19SR >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-COAS19",serever_qntnode_FinalR520 + EP_COAS19SR)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-COAS19",0)
	#CXCPQ-37200,#38257
	Default_Crossover_Cable=Product.Attributes.GetByName("Default Crossover Cable").GetValue()
	backbone_switch = Product.Attributes.GetByName("Backbone Switch Required").GetValue()
	Trace.Write(Default_Crossover_Cable + ' Default_Crossover_Cable PGTest')
	Trace.Write(backbone_switch + ' PGTest')
	if station_37200 >0 and backbone_switch=="No" :
		Trace.Write(backbone_switch + ' backbone_switch Test')
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","51305786-502",station_37200)
	elif backbone_switch=="Yes" and Default_Crossover_Cable=="2M":
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","51305786-502",station_37200 + 1)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","51305786-502",0)
	#CXCPQ-37545,CXCPQ-37546
	if station_svr37545>0:
		Release=Product.Attr('Experion Software Release').GetValue()
		if Release=='R510' or Release=='R511':
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-COAW10",station_svr37545)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-COAW10",0)
		if Release=='R520':
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-COAW19",station_svr37545)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-COAW19",0)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-COAW10",0)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-COAW19",0)
	#CXCPQ-37547
	if svr_hardt37547+MZ_PCEH15SR >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCEH15",svr_hardt37547+MZ_PCEH15SR)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCEH15",0)
	'''if TPMT=="No" and TPM=="No":
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCST81",1)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCSR81",1)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCST81",0)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCSR81",0) cxcpq-103991'''

	#CXCPQ-37553
	if svr_hardt16gb1 >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCEM44",svr_hardt16gb1*2)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-PCEM44",0)

	#CXCPQ-44528
	EP_TQBLDR=int((Product.Attr("Quick Builder(0-11)").GetValue()))
	if EP_TQBLDR >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-TQBLDR",EP_TQBLDR)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-TQBLDR",0)

	EP_TDSPBD=int((Product.Attr("Windows Display Builder(0-100)").GetValue()))
	if EP_TDSPBD >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-TDSPBD",EP_TDSPBD)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-TDSPBD",0)

	TC_SWCB31=int((Product.Attr("Control Builder License(0-11)").GetValue()))
	if TC_SWCB31 >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-SWCB31",TC_SWCB31)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-SWCB31",0)

	TC_BKCF00=int((Product.Attr("Enhanced Bulk Configuration Tool(0-12)").GetValue()))
	if TC_BKCF00 >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-BKCF00",TC_BKCF00)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-BKCF00",0)

	TC_CADL02=int((Product.Attr("Exp CAB Developer License(0-12)").GetValue()))
	if TC_CADL02 >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-CADL02",TC_CADL02)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-CADL02",0)

	TC_EPLX02=int((Product.Attr("Ethernet/IP Interface for Series C(0-100)").GetValue()))
	if TC_EPLX02 >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-EPLX02",TC_EPLX02)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-EPLX02",0)

	EP_IHWTDC=int((Product.Attr("Honeywell TDC3000 Data Hiway Integration(0-1)").GetValue()))
	if EP_IHWTDC >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHWTDC",EP_IHWTDC)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHWTDC",0)

	EP_IHW620=int((Product.Attr("Honeywell 620 LCS Serial/ Ethernet Interface(0-1)").GetValue()))
	if EP_IHW620 >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHW620",EP_IHW620)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHW620",0)

	EP_IHWUDC=int((Product.Attr("Honeywell UDC 3000/5000/6300 Integration(0-1)").GetValue()))
	if EP_IHWUDC >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHWUDC",EP_IHWUDC)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHWUDC",0)

	EP_IADDVM=int((Product.Attr("Experion DVM Integration(0-1)").GetValue()))
	if EP_IADDVM >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IADDVM",EP_IADDVM)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IADDVM",0)

	EP_IHWDPR=int((Product.Attr("Honeywell DPR Recorders Interface(0-1)").GetValue()))
	if EP_IHWDPR >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHWDPR",EP_IHWDPR)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHWDPR",0)

	EP_IHWFSG=int((Product.Attr("Honeywell RM7800 Flame Safeguard Interface(0-1)").GetValue()))
	if EP_IHWFSG >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHWFSG",EP_IHWFSG)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHWFSG",0)

	EP_IHWUMB=int((Product.Attr("Honeywell Universal Modbus Interface(0-1)").GetValue()))
	if EP_IHWUMB >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHWUMB",EP_IHWUMB)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHWUMB",0)

	EP_IHWUMH=int((Product.Attr("Honeywell Universal Modbus History Backfill Option(0-1)").GetValue()))
	if EP_IHWUMH >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHWUMH",EP_IHWUMH)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHWUMH",0)

	EP_IHWMLS=int((Product.Attr("Honeywell Masterlogic Interface(0-1)").GetValue()))
	if EP_IHWMLS >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHWMLS",EP_IHWMLS)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHWMLS",0)

	EP_PMDE01=int((Product.Attr("Honeywell Experion PMD Integration(0-1)").GetValue()))
	if EP_PMDE01 >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-PMDE01",EP_PMDE01)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-PMDE01",0)

	EP_EHPMSP=int((Product.Attr("EHPM Peer to Experion, 1 eHPM usage(0-99)").GetValue()))
	if EP_EHPMSP >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-EHPMSP",EP_EHPMSP)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-EHPMSP",0)

	EP_EHPMS5=int((Product.Attr("EHPM Peer to Experion, 5 eHPM usage(0-99)").GetValue()))
	if EP_EHPMS5 >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-EHPMS5",EP_EHPMS5)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-EHPMS5",0)

	EP_IHWS9K=int((Product.Attr("Honeywell S9000 Integration(0-1)").GetValue()))
	if EP_IHWS9K >0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHWS9K",EP_IHWS9K)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-IHWS9K",0)
	#CXCPQ-44692
	rack =int(Product.Attr("ACE Node Rack Mount Cabinet").GetValue())if Product.Attr("ACE Node Rack Mount Cabinet").GetValue()!='' else 0
	tower =int(Product.Attr("ACE Node Tower Mount Desk").GetValue())if Product.Attr("ACE Node Tower Mount Desk").GetValue()!='' else 0
	if rack>0 or tower>0:
		TC_OPCL01=int(Product.Attr("ACE OPC Extension Library").GetValue())if Product.Attr("ACE OPC Extension Library").GetValue()!='' else 0
		if TC_OPCL01>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-OPCL01",TC_OPCL01)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-OPCL01",0)
		TC_UCNL01=int(Product.Attr("ACE UCN Output Extension Library").GetValue()) if Product.Attr("ACE UCN Output Extension Library").GetValue()!='' else 0
		if TC_UCNL01>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-UCNL01",TC_UCNL01)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-UCNL01",0)
		TC_HWIL01=int(Product.Attr("ACE Hiway Output Extension Library").GetValue()) if Product.Attr("ACE Hiway Output Extension Library").GetValue()!='' else 0
		if TC_HWIL01>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-HWIL01",TC_HWIL01)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-HWIL01",0)
		TC_ACERR1=Product.Attr("ACE Rapid Restart License").GetValue()
		if TC_ACERR1 == "Yes":
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-ACERR1",1)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-ACERR1",0)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-OPCL01",0)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-UCNL01",0)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-HWIL01",0)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-ACERR1",0)

	TC_SIMAC1=int(Product.Attr("SIM-ACE Licenses (0-7)").GetValue()) if Product.Attr("SIM-ACE Licenses (0-7)").GetValue()!='' else 0
	if TC_SIMAC1>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-SIMAC1",TC_SIMAC1)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-SIMAC1",0)
	TC_SIMCX1=int(Product.Attr("Sim-Cx00 PC Licenses (0-20)").GetValue()) if Product.Attr("Sim-Cx00 PC Licenses (0-20)").GetValue()!='' else 0
	if TC_SIMCX1>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-SIMCX1",TC_SIMCX1)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-SIMCX1",0)
	TC_SIMF01=int(Product.Attr("SIM-FFD Licenses (0-125)").GetValue()) if Product.Attr("SIM-FFD Licenses (0-125)").GetValue()!='' else 0
	if TC_SIMF01>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-SIMF01",TC_SIMF01)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-SIMF01",0)
	New_Expansion=Product.Attr("New_Expansion").GetValue()
	if New_Expansion == "New":
		TC_SIMHS1=int(Product.Attr("CN100 Control & I/O Solver - Simulation (0-60)").GetValue()) if Product.Attr("CN100 Control & I/O Solver - Simulation (0-60)").GetValue()!='' else 0
		if TC_SIMHS1>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-SIMHS1",TC_SIMHS1)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-SIMHS1",0)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","TC-SIMHS1",0)
	#CXCPQ-50181
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-QUAD13",0)
	qty_QUAD13 = GS_Exp_grp_parts2.get_QUAD13(Product)
	if qty_QUAD13>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-QUAD13",qty_QUAD13)
	#CXCPQ-49966
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","51305557-100",0)
	qty_555 = GS_Exp_grp_parts2.get_555(Product)
	if qty_555>0 and Product.Attr('CE_Site_Voltage').GetValue() == "240V":
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","51305557-100",qty_555)
	#CXCPQ-43748
	ebr,NSD,NSDP= GS_EXP_NetworkStorage.getebrvalues(Product)
	Log.Info('ebr--'+str(ebr)+'NSD--'+str(NSDP)+'--'+str(NSD))
	if ebr=="Yes":
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-NWSTR6",int(NSD))
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-NWSTR7",int(NSDP))
	elif ebr=="No":
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-NWSTR6",0)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MZ-NWSTR7",0)

	Product.ApplyRules()