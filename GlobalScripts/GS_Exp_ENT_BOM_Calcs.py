import System.Decimal as D
def Node_server(Product):
    Node_flex=""
    Redundancy=""
    attr_mapping =[]
    question=[]
    if Product.Name == "Experion Enterprise Group":
        network_type=Product.Attr('Supervisory Network Type').GetValue()
        svr_Node_nonflex=svr_nonNode_nonflex=svr_nonNode_flex=svr_Node_flex=serever_nodeqnt_mix=serever_qnt_mix=svr_Node_flex37545=0
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        Trace.Write(Redundancy)
        #CXCPQ-37198
        question=['Server Node Type_desk','Server_NodeType']
        node=['Node Supplier_server','Node_Supplier_Server']
        attr_mapping1 = ['SVR_PER_HP_Rack_RAID5','SVR_PER_DELL_Rack_RAID1_RUG','SVR_PER_DELL_Tower_RAID1','SVR_PER_DELL_Rack_RAID1','SVR_STD_DELL_Tower_RAID1','SVR_STD_DELL_Rack_RAID1','SVR_PER_DELL_Rack_RAID5','SVR_F_PER_DELL_Tower_RAID1','SVR_F_PER_DELL_Rack_RAID1','SVR_F_PER_HP_Tower_RAID1','SVR_PER_DELL_Rack_RAID1_XE']
        # for CXCPQ-37543,CXCPQ-37544
        attr_mapping = ['SVR_PER_HP_Rack_RAID5','SVR_PER_DELL_Rack_RAID1_RUG','SVR_PER_DELL_Tower_RAID1','SVR_PER_DELL_Rack_RAID1','SVR_STD_DELL_Tower_RAID1','SVR_STD_DELL_Rack_RAID1','SVR_PER_DELL_Rack_RAID5','SVR_PER_DELL_Rack_RAID1_XE']
        attr_mapping_nNode=['STN_PER_DELL_Tower_RAID1','STN_PER_DELL_Rack_RAID1','STN_PER_HP_Tower_RAID1','SVR_F_PER_DELL_Tower_RAID1','SVR_F_PER_DELL_Rack_RAID1','SVR_F_PER_HP_Tower_RAID1','SVR_PER_DELL_Rack_RAID1_XE']
        for (i,k) in zip(question,node):
            Node_flex=Product.Attr(str(i)).GetValue()
            Node=Product.Attr(str(k)).GetValue()
            if Redundancy=="Redundant" and Node_flex in attr_mapping and Node=="Honeywell":
                Trace.Write("test")
                svr_Node_nonflex=2
            elif Redundancy=="Non Redundant" and Node_flex in attr_mapping and Node=="Honeywell":
                Trace.Write("test")
                svr_Node_nonflex=1
            #CXCPQ-37198
            if Redundancy=="Redundant" and Node_flex in attr_mapping1:
                Trace.Write("test2")
                svr_nonNode_nonflex=2
            elif Redundancy=="Non Redundant" and Node_flex in attr_mapping1:
                Trace.Write("test2")
                svr_nonNode_nonflex=1
        #CXCPQ-37198
        question1=['FlexServer_NodeType','Flex Server Node Type']
        node1=['NodeSupplier_FlexServer','Node Supplier (Flex Server)']
        for (j,b) in zip(question1,node1):
            Node_flex=Product.Attr(str(j)).GetValue()
            Node_svr=Product.Attr(str(b)).GetValue()
            Trace.Write(Node_svr)
            #Trace.Write(Node_flex)CXCPQ-37198,
            if Redundancy=="Redundant" and Node_flex in attr_mapping1:
                svr_nonNode_flex=2
            elif Redundancy=="Non Redundant" and Node_flex in attr_mapping1:
                svr_nonNode_flex=1
            #CXCPQ-37200
            if Redundancy=="Redundant" and Node_flex in attr_mapping_nNode and network_type=="FTE":
                Trace.Write("test")
                svr_Node_flex=2
            elif Redundancy=="Non Redundant" and Node_flex in attr_mapping_nNode and network_type=="FTE":
                Trace.Write("test")
                svr_Node_flex=1
            #CXCPQ-37546,CXCPQ-37545
            if Redundancy=="Redundant" and Node_flex in attr_mapping_nNode and Node_svr=="Honeywell":
                Trace.Write("test")
                svr_Node_flex37545=2
            elif Redundancy=="Non Redundant" and Node_flex in attr_mapping_nNode and Node_svr=="Honeywell":
                Trace.Write("test")
                svr_Node_flex37545=1
        svr_nodeqnt_mix=svr_Node_nonflex+svr_Node_flex
        svr_qnt_mix=svr_nonNode_nonflex+svr_nonNode_flex  #for #CXCPQ-37198
    return svr_Node_nonflex,svr_nonNode_nonflex,svr_nonNode_flex,svr_Node_flex,svr_nodeqnt_mix,svr_qnt_mix,svr_Node_flex37545
#for Pc calculation
def Simulation_PC(Product):
    pcserever_qnt_nonnode=PCserever_qntnode=PCserever_qntnode1=0
    Node_flex=""
    Redundancy=""
    attr_mapp=[]
    question2=[]
    if Product.Name == "Experion Enterprise Group":
        Release=Product.Attr('Experion Software Release').GetValue()
        u2serever_qnt=PCserever_qntnode1=0
        server1=['Hardware Design Selection - Sim PC Node','Hardware Design Selection - Sim PC Node1']
        Node1=['Node Supplier (Sim PC)1','Node Supplier (Sim PC)']
        hard_disk=['Additional Hard Disk (Sim PC Cab)','Additional Hard Disk (Sim PC Desk)']
        #CXDEV-8013 - kaousalya Adala
        if Release in ["R511", "R510"]:
            attr_mapp =['SVR_PER_DELL_Rack_RAID1_RUG','SVR_PER_DELL_Tower_RAID1','SVR_PER_DELL_Rack_RAID1','SVR_STD_DELL_Tower_RAID1','SVR_STD_DELL_Rack_RAID1','SVR_PER_DELL_Rack_RAID5','SVR_F_PER_DELL_Tower_RAID1','SVR_F_PER_DELL_Rack_RAID1','SVR_F_PER_HP_Tower_RAID1','SVR_PER_DELL_Rack_RAID1_XE']
        else:
            attr_mapp =['SVR_PER_HP_Rack_RAID5','SVR_PER_DELL_Rack_RAID1_RUG','SVR_PER_DELL_Tower_RAID1','SVR_PER_DELL_Rack_RAID1','SVR_STD_DELL_Tower_RAID1','SVR_STD_DELL_Rack_RAID1','SVR_PER_DELL_Rack_RAID5','SVR_F_PER_DELL_Tower_RAID1','SVR_F_PER_DELL_Rack_RAID1','SVR_F_PER_HP_Tower_RAID1','SVR_PER_DELL_Rack_RAID1_XE']
        #CXCPQ-37198
        for i in server1:
            Node_flex=Product.Attr(str(i)).GetValue()
            if Node_flex in attr_mapp:
                #Trace.Write('test1')
                qnt1=int(Product.Attr('SIM-ACE Licenses (0-7)').GetValue()) if Product.Attr('SIM-ACE Licenses (0-7)').GetValue()!='' else 0
                qnt2=int(Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()) if Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()!='' else 0
                qnt3=int(Product.Attr('SIM-FFD Licenses (0-125)').GetValue()) if Product.Attr('SIM-FFD Licenses (0-125)').GetValue()!='' else 0
                pcserever_qnt_nonnode=D.Ceiling((qnt1+D.Ceiling(0.4*qnt2)+D.Ceiling(0.1*qnt3))/4.0) #for CXCPQ-37198
        for (j,k,l) in zip(server1,Node1,hard_disk):
            Node_flex1=Product.Attr(str(j)).GetValue()
            Trace.Write(j)
            Node1=Product.Attr(str(k)).GetValue()
            hard_disk=Product.Attr(str(l)).GetValue()
            Trace.Write(Node1)
            if Node_flex1 in attr_mapp and Node1=='Honeywell':
                Trace.Write('test1')
                qnt11=int(Product.Attr('SIM-ACE Licenses (0-7)').GetValue()) if Product.Attr('SIM-ACE Licenses (0-7)').GetValue()!='' else 0
                qnt12=int(Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()) if Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()!='' else 0
                qnt13=int(Product.Attr('SIM-FFD Licenses (0-125)').GetValue()) if Product.Attr('SIM-FFD Licenses (0-125)').GetValue()!='' else 0
                PCserever_qntnode=D.Ceiling((qnt11+D.Ceiling(0.4*qnt12)+D.Ceiling(0.1*qnt13))/4.0)
            if Node_flex1=="SVR_PER_DELL_Rack_RAID5" and Node1=="Honeywell" and hard_disk=="Yes":
                Trace.Write('test1')
                qnt11=int(Product.Attr('SIM-ACE Licenses (0-7)').GetValue()) if Product.Attr('SIM-ACE Licenses (0-7)').GetValue()!='' else 0
                qnt12=int(Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()) if Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()!='' else 0
                qnt13=int(Product.Attr('SIM-FFD Licenses (0-125)').GetValue()) if Product.Attr('SIM-FFD Licenses (0-125)').GetValue()!='' else 0
                PCserever_qntnode1=D.Ceiling((qnt11+D.Ceiling(0.4*qnt12)+D.Ceiling(0.1*qnt13))/4.0)
        return pcserever_qnt_nonnode,PCserever_qntnode,PCserever_qntnode1
def server_qnt1(Product):
    VLE=0
    Node_flex=""
    Redundancy=""
    attr_mapping =[]
    question1=[]
    if Product.Name == "Experion Enterprise Group":
        network_type=Product.Attr('Supervisory Network Type').GetValue()
        #above both function import
        svr_Node_nonflex,svr_nonNode_nonflex,svr_nonNode_flex,svr_Node_flex,svr_nodeqnt_mix,svr_qnt_mix,svr_Node_flex37545=Node_server(Product)
        pcserever_qnt_nonnode,PCserever_qntnode,PCserever_qntnode1=Simulation_PC(Product)

        serever_qnt_T=station_37200=serever_qntnode_T=station_qnt_t=station_37546=serever_qnt_26=0
        #server Qustion mapping
        server=['Hardware Design Selection_ ACE_Node','Hardware Design Selection_ACE Node','Hardware Design Selection_ACE_T_Node','Hardware Design Selection','Hardware Design Selection - EAPP Node','Hardware_Design_Selection - EAPP Node','Hardware Selection','Server Type1']
        #node type
        server_node=['Node Supplier_ACE1','Node Supplier_ACE','Node_Supplier_ACE_T','Node Supplier_ACE_T','Node Supplier_EAPP','Node_Supplier_EAPP','Node Supplier Server1','Node Supplier Server']
        #CXDEV-8013 - kaousalya Adala
        #server Values mapping
        Release=Product.Attr('Experion Software Release').GetValue()
        if Release in ["R510", "R511"]:
            Value_mapp_se = ['SVR_PER_DELL_Rack_RAID1_RUG','SVR_PER_DELL_Tower_RAID1','SVR_PER_DELL_Rack_RAID1','SVR_STD_DELL_Tower_RAID1','SVR_STD_DELL_Rack_RAID1','SVR_PER_DELL_Rack_RAID5','SVR_F_PER_DELL_Tower_RAID1','SVR_F_PER_DELL_Rack_RAID1','SVR_F_PER_HP_Tower_RAID1','SVR_PER_DELL_Rack_RAID1_XE']
            Value_mapp_se1 = ['SVR_PER_DELL_Rack_RAID1_RUG','SVR_PER_DELL_Tower_RAID1','SVR_PER_DELL_Rack_RAID1','SVR_STD_DELL_Tower_RAID1','SVR_STD_DELL_Rack_RAID1','SVR_PER_DELL_Rack_RAID5','SVR_PER_DELL_Rack_RAID1_XE']
        else:
            Value_mapp_se = ['SVR_PER_HP_Rack_RAID5','SVR_PER_DELL_Rack_RAID1_RUG','SVR_PER_DELL_Tower_RAID1','SVR_PER_DELL_Rack_RAID1','SVR_STD_DELL_Tower_RAID1','SVR_STD_DELL_Rack_RAID1','SVR_PER_DELL_Rack_RAID5','SVR_F_PER_DELL_Tower_RAID1','SVR_F_PER_DELL_Rack_RAID1','SVR_F_PER_HP_Tower_RAID1','SVR_PER_DELL_Rack_RAID1_XE']
            Value_mapp_se1 = ['SVR_PER_HP_Rack_RAID5','SVR_PER_DELL_Rack_RAID1_RUG','SVR_PER_DELL_Tower_RAID1','SVR_PER_DELL_Rack_RAID1','SVR_STD_DELL_Tower_RAID1','SVR_STD_DELL_Rack_RAID1','SVR_PER_DELL_Rack_RAID5','SVR_PER_DELL_Rack_RAID1_XE']
        #server question quntity mapping
        Server_mapping=['ACE Node Tower Mount Desk','ACE Node Rack Mount Cabinet','ACE_T_Node _Tower_Mount_Desk','ACE_T_Node _Rack_Mount_Cabinet','Experion APP Node - Tower Mount','Experion APP Node - Rack Mount','Mobile Server Nodes (0-1)','Additional Servers']
        #CXCPQ-37198
        for (i,j) in zip(server ,Server_mapping):
            attr_name = str(j)
            Node_flex=Product.Attr(str(i)).GetValue()
            if Node_flex in Value_mapp_se:
                serever_qnt_T +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        serever_qnt_T=serever_qnt_T+svr_qnt_mix+pcserever_qnt_nonnode #for CXCPQ-37198 final
        #Trace.Write('svr_qnt_mix :'+str(svr_qnt_mix))
        #for CXCPQ-37543,CXCPQ-37544
        for (i,j,k) in zip(server ,Server_mapping,server_node):
            attr_name = str(j)
            Node_flex=Product.Attr(str(i)).GetValue()
            Trace.Write(Node_flex)
            Node=Product.Attr(str(k)).GetValue()
            Trace.Write(Node)
            if Node_flex in Value_mapp_se1 and Node=="Honeywell":
                Trace.Write("testing")
                serever_qntnode_T +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        serever_qntnode_T=serever_qntnode_T+svr_Node_nonflex+PCserever_qntnode #for CXCPQ-37543,CXCPQ-37544 final

        # station cals start
        #station Question
        station=['CMS Flex Station Hardware Selection','CMS Console Station Hardware Selection','CMS TPS Station Hardware Selection','CMS Console Station Extension Hardware Selection','DMS Flex Station Hardware Selection','DMS Console Station Hardware Selection','DMS TPS Station Hardware Selection','DMS Console Station Extension Hardware Selection','Flex Station Hardware Selection TPS','Console Station Hardware Selection','TPS Station Hardware Selection','Console Station Extension Hardware Selection','Station Type']
        #station Question Quantity mapping
        station_mapping=['CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15','DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15','Flex Station Qty (0-60)','Console Station Qty (0-20)','TPS Station Qty (0-20)','Console Station Extension Qty  (0-15)','Additional Stations']
        #station Value mapping
        station_mapp_st = ['STN_PER_DELL_Tower_RAID2','STN_PER_DELL_Tower_RAID1','STN_PER_DELL_Rack_RAID1','STN_PER_HP_Tower_RAID1','STN_STD_DELL_Tower_NonRAID']
        attr_mapping_nNode = ['STN_PER_DELL_Tower_RAID2','STN_PER_DELL_Tower_RAID1','STN_PER_DELL_Rack_RAID1','STN_PER_HP_Tower_RAID1','SVR_F_PER_DELL_Tower_RAID1','SVR_F_PER_DELL_Rack_RAID1','SVR_F_PER_HP_Tower_RAID1']
        #CXCPQ-37545,CXCPQ-37546
        #node_type=['CMS Node Supplier','CMS Node Supplier','CMS Node Supplier','CMS Node Supplier','DMS Node Supplier','DMS Node Supplier','DMS Node Supplier','DMS Node Supplier','Node Supplier','Node Supplier','Node Supplier','Node Supplier','Node Supplier (Additional Station)']

        #CXCPQ-37198
        for (i,j) in zip(station ,station_mapping):
            attr_name = str(j)
            Node_flex=Product.Attr(str(i)).GetValue()
            value=Product.Attr(str(j)).GetValue()
            if Node_flex in station_mapp_st:
                station_qnt_t +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        serever_qnt_T=station_qnt_t+serever_qnt_T #for CXCPQ-37198
        #CXCPQ-37200
        for (i,j) in zip(station ,station_mapping):
            attr_name = str(j)
            Node_flex=Product.Attr(str(i)).GetValue()
            if Node_flex in attr_mapping_nNode and network_type=="FTE":
                station_37200 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        station_37200=station_37200+svr_Node_flex #final for CXCPQ-37200
        #qnt 26 condition for #CXCPQ-37198 if 2 is selected
        for (i,j) in zip(station ,station_mapping):
            attr_name = str(j)
            Node_flex=Product.Attr(str(i)).GetValue()
            value=Product.Attr(str(j)).GetValue()
            if Node_flex in station_mapp_st:
                if str(value)=="2":
                    VLE+=1
                    Trace.Write("VLE "+str(VLE))
                if VLE==12:
                    serever_qnt_T=26
                else:
                    serever_qnt_T=serever_qnt_T
    return serever_qnt_T,serever_qntnode_T,station_37200
#CXCPQ-37545,CXCPQ-37546
def QNTCXCPQ_37545(Product):
    svr_Node_nonflex,svr_nonNode_nonflex,svr_nonNode_flex,svr_Node_flex,svr_nodeqnt_mix,svr_qnt_mix,svr_Node_flex37545=Node_server(Product)
    station_svr37545=station_svr4=station_svr3=station_svr2=station_svr1=0
    Node_flex=[]
    station1=[]
    station_mapping1=[]
    attr_mapping_nNode1=[]
    if Product.Name == "Experion Enterprise Group":
        cms_node=Product.Attr('CMS Node Supplier').GetValue()
        dms_node=Product.Attr('DMS Node Supplier').GetValue()
        or_node=Product.Attr('Node Supplier').GetValue()
        Station_node=Product.Attr('Node Supplier (Additional Station)').GetValue()
        station1=['CMS Flex Station Hardware Selection','CMS Console Station Hardware Selection','CMS TPS Station Hardware Selection','CMS Console Station Extension Hardware Selection']
        station2=['DMS Flex Station Hardware Selection','DMS Console Station Hardware Selection','DMS TPS Station Hardware Selection','DMS Console Station Extension Hardware Selection']
        station3=['Flex Station Hardware Selection TPS','Console Station Hardware Selection','TPS Station Hardware Selection','Console Station Extension Hardware Selection']
        station4=['Station Type']
        attr_mapping_nNode1 = ['STN_PER_DELL_Tower_RAID1','STN_PER_DELL_Rack_RAID1','STN_PER_HP_Tower_RAID1','SVR_F_PER_DELL_Tower_RAID1','SVR_F_PER_DELL_Rack_RAID1','SVR_F_PER_HP_Tower_RAID1']
        station_mapping1=['CMS Flex Station Qty 0_60','CMS Console Station Qty 0_20','CMS TPS Station Qty 0_20','CMS Console Station Extension Qty 0_15']
        station_mapping2=['DMS Flex Station Qty 0_60','DMS Console Station Qty 0_20','DMS TPS Station Qty 0_20','DMS Console Station Extension Qty 0_15']
        station_mapping3=['Flex Station Qty (0-60)','Console Station Qty (0-20)','TPS Station Qty (0-20)','Console Station Extension Qty  (0-15)']
        station_mapping4=['Additional Stations']
        for (i,j) in zip(station1,station_mapping1):
            attr_name = str(j)
            Node_flex=Product.Attr(str(i)).GetValue()
            if Node_flex in attr_mapping_nNode1 and cms_node=="Honeywell":
                station_svr1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        for (i1,j1) in zip(station2,station_mapping2):
            attr_name = str(j1)
            Node_flex=Product.Attr(str(i1)).GetValue()
            if Node_flex in attr_mapping_nNode1 and dms_node=="Honeywell":
                station_svr2 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        for (i2,j2) in zip(station3,station_mapping3):
            attr_name = str(j2)
            Node_flex=Product.Attr(str(i2)).GetValue()
            if Node_flex in attr_mapping_nNode1 and or_node=="Honeywell":
                station_svr3 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        for (i3,j3) in zip(station4,station_mapping4):
            attr_name = str(j3)
            Node_flex=Product.Attr(str(i3)).GetValue()
            if Node_flex in attr_mapping_nNode1 and Station_node=="Honeywell":
                station_svr4 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        svr_Node_flex37545=svr_Node_flex37545+station_svr37545+station_svr4+station_svr2+station_svr3+station_svr1
    return svr_Node_flex37545
#CXCPQ-37547
def Qnt37547(Product):
    svr_hardt37547=svr_hardnodet37547=0
    if Product.Name == "Experion Enterprise Group":
        pcserever_qnt_nonnode,PCserever_qntnode,PCserever_qntnode1=Simulation_PC(Product)
        svr_hardt37547=svr_hardnodet37547=0
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        #Trace.Write(Redundancy)
        #CXCPQ-37198
        question=['Server Node Type_desk','Server_NodeType']
        node=['Node Supplier_server','Node_Supplier_Server']
        hard_disk1=['Additional Hard Disk1','AdditionalHard_Disk']
        server=['Hardware Design Selection_ ACE_Node','Hardware Design Selection_ACE Node','Hardware Design Selection_ACE_T_Node','Hardware Design Selection','Hardware Design Selection - EAPP Node','Hardware_Design_Selection - EAPP Node','Hardware Selection']
        Server_mapping=['ACE Node Tower Mount Desk','ACE Node Rack Mount Cabinet','ACE_T_Node _Tower_Mount_Desk','ACE_T_Node _Rack_Mount_Cabinet','Experion APP Node - Tower Mount','Experion APP Node - Rack Mount','Mobile Server Nodes (0-1)']
        server_node=['Node Supplier_ACE1','Node Supplier_ACE','Node_Supplier_ACE_T','Node Supplier_ACE_T','Node Supplier_EAPP','Node_Supplier_EAPP','Node Supplier Server1']
        server_Hard=['Additional Hard Disk ACE desk pre','Additional Hard Disk _ACE','Additional Hard Disk (ACE-T)','Additional Hard Disk_ACE_T','Additional Hard Disk_EAPP','Additional_Hard_Disk_EAPP','Additional Hard Disk (Mobile Server)']
        for (m,n,p) in zip(question,node,hard_disk1):
            Node_flex1=Product.Attr(str(m)).GetValue()
            Node1=Product.Attr(str(n)).GetValue()
            hard_disk1=Product.Attr(str(p)).GetValue()
            #Trace.Write(hard_disk1)
            if Redundancy=="Redundant" and Node_flex1=="SVR_PER_DELL_Rack_RAID5" and hard_disk1=="Yes" and Node1=="Honeywell":
                svr_hardnodet37547=2
            elif Redundancy=="Non Redundant" and Node_flex1=="SVR_PER_DELL_Rack_RAID5" and hard_disk1=="Yes" and Node1=="Honeywell":
                svr_hardnodet37547=1
        for (i,j,k,l) in zip(server,Server_mapping,server_node,server_Hard):
            attr_name = str(j)
            Node_flex=Product.Attr(str(i)).GetValue()
            Node=Product.Attr(str(k)).GetValue()
            hard_disk=Product.Attr(str(l)).GetValue()
            if Node_flex=="SVR_PER_DELL_Rack_RAID5" and Node=="Honeywell" and hard_disk=="Yes":
                svr_hardt37547 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        svr_hardt37547=svr_hardt37547+svr_hardnodet37547+PCserever_qntnode1
    return svr_hardt37547

#CXCPQ-43301
def EXP_Bom_TPM(Product):
    svr=svr1=svr2=svr3=svr4=svr5=svr6=svr7=svr8=svr9=Qnt1=Qnt2=Qnt3=Qnt4=Qnt5=Qnt6=Qnt7=Qnt8=Qnt9=0
    svrs=svrs11=svrs12=svrs13=svrs14=svrs15=svrs16=svrs17=svrs18=svrs19=0
    svrs=svrs1=svrs2=svrs3=svrs4=svrs5=svrs6=svrs7=svrs8=svrs9=PCserever_qntnode2=0
    Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
    question=['Server Node Type_desk','Server_NodeType']
    node=['Node Supplier_server','Node_Supplier_Server']
    tpm=['Trusted Platform Module1','TrustedPlatformModule_TPM']
    server=['Hardware Design Selection_ ACE_Node','Hardware Design Selection_ACE Node','Hardware Design Selection_ACE_T_Node','Hardware Design Selection','Hardware Design Selection - EAPP Node','Hardware_Design_Selection - EAPP Node','Hardware Selection','Server Type1']
    Server_mapping=['ACE Node Tower Mount Desk','ACE Node Rack Mount Cabinet','ACE_T_Node _Tower_Mount_Desk','ACE_T_Node _Rack_Mount_Cabinet','Experion APP Node - Tower Mount','Experion APP Node - Rack Mount','Mobile Server Nodes (0-1)','Additional Servers']
    server_node=['Node Supplier_ACE1','Node Supplier_ACE','Node_Supplier_ACE_T','Node Supplier_ACE_T','Node Supplier_EAPP','Node_Supplier_EAPP','Node Supplier Server1','Node Supplier Server']
    tpm1=['Trusted Platform Module_TPM_ACE_desk','Trusted Platform Module_TPM_ACE_Node','Trusted Platform Module_TPM_ACE_T','Ent_ace_t_Cab_tpm','Ent_app_desk_tpm','Ent_app_cab_tpm','Ent_ace_t_desk_tpm','Trusted Platform Module_TPM']
    servSim=['Hardware Design Selection - Sim PC Node','Hardware Design Selection - Sim PC Node1']
    NodeSim=['Node Supplier (Sim PC)1','Node Supplier (Sim PC)']
    tpmSim=['Ent_sim_cab_tpm','Ent_sim_desk_tpm']
    if Redundancy=="Redundant":
        svr=2
    elif Redundancy=="Non Redundant":
        svr=1
    for (i,j,k) in zip(question,node,tpm):
        Node_flex1=Product.Attr(str(i)).GetValue()
        Node1=Product.Attr(str(j)).GetValue()
        Tpm=Product.Attr(str(k)).GetValue()
        if Node_flex1=="SVR_PER_HP_Rack_RAID5" and Tpm=="Yes" and Node1=="Honeywell":
            svr1=svr
            Trace.Write(svr1)
        elif Node_flex1=="SVR_STD_DELL_Rack_RAID1" and Tpm and Node1=="Honeywell":
            svr2=svr
            Trace.Write(svr2)
        elif Node_flex1=="SVR_PER_DELL_Rack_RAID1" and Tpm and Node1=="Honeywell":
            svr3=svr
            Trace.Write(svr3)
        elif Node_flex1=="SVR_PER_DELL_Rack_RAID1" and Tpm=="No" and Node1=="Honeywell":
            svr4=svr
            Trace.Write(svr4)
        elif Node_flex1=="SVR_PER_DELL_Rack_RAID5" and Tpm=="Yes" and Node1=="Honeywell":
            svr5=svr
            Trace.Write(svr5)
        elif Node_flex1=="SVR_PER_DELL_Rack_RAID1_RUG" and Tpm=="Yes" and Node1=="Honeywell":
            svr6=svr
            Trace.Write(svr6)
        elif Node_flex1=="SVR_STD_DELL_Tower_RAID1" and Tpm and Node1=="Honeywell":
            svr7=svr
            Trace.Write(svr7)
        elif Node_flex1=="SVR_PER_DELL_Tower_RAID1" and Tpm and Node1=="Honeywell":
            svr8=svr
            Trace.Write(svr8)
        elif Node_flex1=="SVR_PER_DELL_Tower_RAID1" and Tpm=="No" and Node1=="Honeywell":
            svr9=svr
            Trace.Write(svr9)
    for (i,j,k,l) in zip(server,server_node,tpm1,Server_mapping):
        Node_flex=Product.Attr(str(i)).GetValue()
        Node=Product.Attr(str(j)).GetValue()
        Tpm1=Product.Attr(str(k)).GetValue()
        attr_name = str(l)
        if Node_flex=="SVR_PER_HP_Rack_RAID5" and Tpm1=="Yes" and Node=="Honeywell":
            svrs1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        elif Node_flex=="SVR_STD_DELL_Rack_RAID1" and Tpm1 and Node=="Honeywell":
            svrs2 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        elif Node_flex=="SVR_PER_DELL_Rack_RAID1" and Tpm1 and Node=="Honeywell":
            svrs3 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        elif Node_flex=="SVR_PER_DELL_Rack_RAID1" and Tpm1=="No" and Node=="Honeywell":
            svrs4 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        elif Node_flex=="SVR_PER_DELL_Rack_RAID5" and Tpm1=="Yes" and Node=="Honeywell":
            svrs5 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        elif Node_flex=="SVR_PER_DELL_Rack_RAID1_RUG" and Tpm1=="Yes" and Node=="Honeywell":
            svrs6 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        elif Node_flex=="SVR_STD_DELL_Tower_RAID1" and Tpm1 and Node=="Honeywell":
            svrs7 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        elif Node_flex=="SVR_PER_DELL_Tower_RAID1" and Tpm1 and Node=="Honeywell":
            svrs8 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        elif Node_flex=="SVR_PER_DELL_Tower_RAID1" and Tpm1=="No" and Node=="Honeywell":
            svrs9 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
    qnt11=int(Product.Attr('SIM-ACE Licenses (0-7)').GetValue()) if Product.Attr('SIM-ACE Licenses (0-7)').GetValue()!='' else 0
    qnt12=int(Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()) if Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()!='' else 0
    qnt13=int(Product.Attr('SIM-FFD Licenses (0-125)').GetValue()) if Product.Attr('SIM-FFD Licenses (0-125)').GetValue()!='' else 0
    PCserever_qntnode2=D.Ceiling((qnt11+D.Ceiling(0.4*qnt12)+D.Ceiling(0.1*qnt13))/4.0)
    for m,n,o in zip(servSim,NodeSim,tpmSim):
        Node_flex=Product.Attr(str(m)).GetValue()
        Node=Product.Attr(str(n)).GetValue()
        Tpm1=Product.Attr(str(o)).GetValue()
        if Node_flex=="SVR_PER_HP_Rack_RAID5" and Tpm1=="Yes" and Node=="Honeywell":
            svrs11 =PCserever_qntnode2
        elif Node_flex=="SVR_STD_DELL_Rack_RAID1" and Tpm1 and Node=="Honeywell":
            svrs12 =PCserever_qntnode2
        elif Node_flex=="SVR_PER_DELL_Rack_RAID1" and Tpm1 and Node=="Honeywell":
            svrs13 =PCserever_qntnode2
        elif Node_flex=="SVR_PER_DELL_Rack_RAID1" and Tpm1=="No" and Node=="Honeywell":
            svrs14 =PCserever_qntnode2
        elif Node_flex=="SVR_PER_DELL_Rack_RAID5" and Tpm1=="Yes" and Node=="Honeywell":
            svrs15 =PCserever_qntnode2
        elif Node_flex=="SVR_PER_DELL_Rack_RAID1_RUG" and Tpm1=="Yes" and Node=="Honeywell":
            svrs16 =PCserever_qntnode2
        elif Node_flex=="SVR_STD_DELL_Tower_RAID1" and Tpm1 and Node=="Honeywell":
            svrs17 =PCserever_qntnode2
        elif Node_flex=="SVR_PER_DELL_Tower_RAID1" and Tpm1 and Node=="Honeywell":
            svrs18 =PCserever_qntnode2
        elif Node_flex=="SVR_PER_DELL_Tower_RAID1" and Tpm1=="No" and Node=="Honeywell":
            svrs19 =PCserever_qntnode2
    Qnt1=int(svr1)+int(svrs1)+int(svrs11)
    Qnt2=int(svr2)+int(svrs2)+int(svrs12)
    Qnt3=int(svr3)+int(svrs3)+int(svrs13)
    Qnt4=int(svr4)+int(svrs4)+int(svrs14)
    Qnt5=int(svr5)+int(svrs5)+int(svrs15)
    Qnt6=int(svr6)+int(svrs6)+int(svrs16)
    Qnt7=int(svr7)+int(svrs7)+int(svrs17)
    Qnt8=int(svr8)+int(svrs8)+int(svrs18)
    Qnt9=int(svr9)+int(svrs9)+int(svrs19)
    
    return Qnt1,Qnt2,Qnt3,Qnt4,Qnt5,Qnt6,Qnt7,Qnt8,Qnt9

def Node_station(Product,que):
    Node_flex=""
    Redundancy=""
    attr_mapping =[]
    question=[]
    if Product.Name == "Experion Enterprise Group":
        server_qnt=0
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        Trace.Write(Redundancy)
        ServerType=Product.Attr('Experion Server Type').GetValue()
        question=['Server_NodeType','Server Node Type_desk']
        # node supplier
        node_supplier = ['Node_Supplier_Server','Node Supplier_server']
     
        #CXCPQ-37560,37562,37563,37564
        for (i,j) in zip(question,node_supplier):
            Node_flex=Product.Attr(str(i)).GetValue()
            ns = Product.Attr(str(j)).GetValue()
            #Trace.Write(Node_flex)
            if Redundancy=="Redundant" and Node_flex == que and ns == "Honeywell" and ServerType in ('Server', 'Server TPS', 'Flex Server'):
                server_qnt=2
            elif Redundancy=="Non Redundant" and Node_flex == que and ns == "Honeywell" and ServerType in ('Server', 'Server TPS', 'Flex Server'):
                server_qnt=1
    return server_qnt
    
def station_qnt1(Product,que,que1):
    Node_flex=""
    question1=[]
    station_qnt_cms=station_qnt_dms=station_qnt_ori=station_qnt_add=station_qnt_mobile=station_qnt_additional=station_qnt_EAAP_Tower=station_qnt_EAAP_Rack=station_qnt_Sim_PC_Lic=0
    if Product.Name == "Experion Enterprise Group":
        server_qnt=Node_station(Product,que)
        station_qnt = 0
        Trace.Write("server_qnt---:"+str(server_qnt))
        #station Question
        station1=['ACE Node Tower Mount Desk']
        station2=['ACE Node Rack Mount Cabinet']
        station3=['ACE_T_Node _Tower_Mount_Desk']
        station4=['ACE_T_Node _Rack_Mount_Cabinet']
        station5=['Mobile Server Nodes (0-1)']
        station6=['Additional Servers']
        station7=['Experion APP Node - Tower Mount']
        station8=['Experion APP Node - Rack Mount']
        #station Question Quantity mapping
        station_mapping1=['Hardware Design Selection_ ACE_Node']
        station_mapping2=['Hardware Design Selection_ACE Node']
        station_mapping3=['Hardware Design Selection_ACE_T_Node']
        station_mapping4=['Hardware Design Selection']
        station_mapping5=['Hardware Selection']
        station_mapping6=['Server Type1']
        station_mapping7=['Hardware Design Selection - EAPP Node']
        station_mapping8=['Hardware_Design_Selection - EAPP Node']
        #Node Supplier
        ACE_Tower_node=Product.Attr('Node Supplier_ACE1').GetValue()
        ACE_Rack_node=Product.Attr('Node Supplier_ACE').GetValue()
        ACE_T_Tower_node=Product.Attr('Node_Supplier_ACE_T').GetValue()
        ACE_T_Rack_node=Product.Attr('Node Supplier_ACE_T').GetValue()
        Mobile_node=Product.Attr('Node Supplier Server1').GetValue()
        Add_node=Product.Attr('Node Supplier Server').GetValue()
        EAAP_Tower_node=Product.Attr('Node Supplier_EAPP').GetValue()
        EAAP_Rack_node=Product.Attr('Node_Supplier_EAPP').GetValue()
       
        for (i1,j1) in zip(station1 ,station_mapping1):
            attr_name = str(i1)
            Node_flex=Product.Attr(str(j1)).GetValue()
            #Trace.Write("Node_flex: "+str(Node_flex))
            if Node_flex == que1 and ACE_Tower_node=="Honeywell":
                Trace.Write("val : "+str(Node_flex))
                station_qnt_cms +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

        for (i2,j2) in zip(station2 ,station_mapping2):
            attr_name = str(i2)
            Node_flex=Product.Attr(str(j2)).GetValue()
            #Trace.Write("Node_flex: "+str(Node_flex))
            if Node_flex == que1 and ACE_Rack_node=="Honeywell":
                Trace.Write("val : "+str(Node_flex))
                station_qnt_dms +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

        for (i3,j3) in zip(station3 ,station_mapping3):
            attr_name = str(i3)
            Node_flex=Product.Attr(str(j3)).GetValue()
            #Trace.Write("Node_flex: "+str(Node_flex))
            if Node_flex == que1 and ACE_T_Tower_node=="Honeywell":
                Trace.Write("val : "+str(Node_flex))
                station_qnt_ori +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0

        for (i4,j4) in zip(station4 ,station_mapping4):
            attr_name = str(i4)
            Node_flex=Product.Attr(str(j4)).GetValue()
            #Trace.Write("Node_flex: "+str(Node_flex))
            if Node_flex == que1 and ACE_T_Rack_node=="Honeywell":
                Trace.Write("val : "+str(Node_flex))
                station_qnt_add +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        for (i5,j5) in zip(station5 ,station_mapping5):
            attr_name = str(i5)
            Node_flex=Product.Attr(str(j5)).GetValue()
            #Trace.Write("Node_flex: "+str(Node_flex))
            if Node_flex == que1 and Mobile_node=="Honeywell":
                Trace.Write("val : "+str(Node_flex))
                station_qnt_mobile +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        for (i6,j6) in zip(station6 ,station_mapping6):
            attr_name = str(i6)
            Node_flex=Product.Attr(str(j6)).GetValue()
            #Trace.Write("Node_flex: "+str(Node_flex))
            if Node_flex == que1 and Add_node=="Honeywell":
                Trace.Write("val : "+str(Node_flex))
                station_qnt_additional +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        for (i7,j7) in zip(station7 ,station_mapping7):
            attr_name = str(i7)
            Node_flex=Product.Attr(str(j7)).GetValue()
            #Trace.Write("Node_flex: "+str(Node_flex))
            if Node_flex == que1 and EAAP_Tower_node=="Honeywell":
                Trace.Write("val : "+str(Node_flex))
                station_qnt_EAAP_Tower +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        for (i8,j8) in zip(station8 ,station_mapping8):
            attr_name = str(i8)
            Node_flex=Product.Attr(str(j8)).GetValue()
            #Trace.Write("Node_flex: "+str(Node_flex))
            if Node_flex == que1 and EAAP_Rack_node=="Honeywell":
                Trace.Write("val : "+str(Node_flex))
                station_qnt_EAAP_Rack +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        Sim_PC_Lic_node=Product.Attr('Node Supplier (Sim PC)').GetValue()
        Node_flex=Product.Attr(str('Hardware Design Selection - Sim PC Node1')).GetValue()
        Sim_PC_Lic_node_cab=Product.Attr('Node Supplier (Sim PC)1').GetValue()
        Node_flex_cab=Product.Attr(str('Hardware Design Selection - Sim PC Node')).GetValue()
        if (Node_flex == que1 and Sim_PC_Lic_node=="Honeywell") or (Node_flex_cab == que1 and Sim_PC_Lic_node_cab=="Honeywell"):
            qnt_SIM_ACE = qnt_Sim_Cx = qnt_SIM_FFD = 0
            if int(Product.Attr(str('SIM-ACE Licenses (0-7)')).GetValue()) > 0:
                qnt_SIM_ACE = int(Product.Attr(str('SIM-ACE Licenses (0-7)')).GetValue())
            if int(Product.Attr(str('Sim-Cx00 PC Licenses (0-20)')).GetValue()) > 0:
                qnt_Sim_Cx = int(Product.Attr(str('Sim-Cx00 PC Licenses (0-20)')).GetValue())
            if int(Product.Attr(str('SIM-FFD Licenses (0-125)')).GetValue()) > 0:
                qnt_SIM_FFD = int(Product.Attr(str('SIM-FFD Licenses (0-125)')).GetValue())
            station_qnt_Sim_PC_Lic = D.Ceiling((qnt_SIM_ACE+D.Ceiling(0.4*qnt_Sim_Cx)+D.Ceiling(0.1*qnt_SIM_FFD))/4.0)
        station_qnt = station_qnt_cms + station_qnt_dms + station_qnt_ori + station_qnt_add + station_qnt_mobile + station_qnt_additional+station_qnt_EAAP_Tower+station_qnt_EAAP_Rack+station_qnt_Sim_PC_Lic
        
    return int(server_qnt + station_qnt)