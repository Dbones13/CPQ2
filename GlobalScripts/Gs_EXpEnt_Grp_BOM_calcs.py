import System.Decimal as D
#for Pc calculation
##CXCPQ-37552,#CXCPQ-37554,CXCPQ-37553
def Simulation_PC(Product):
    pcserever_qnt_nonnode=PCserever_qntnode=PCserever_qntnode1=PCserever_qntnode2=0
    Node_flex=""
    Redundancy=""
    attr_mapp=[]
    question2=[]
    if Product.Name == "Experion Enterprise Group":
        u2serever_qnt=PCserever_qntnode1=0
        server1=['Hardware Design Selection - Sim PC Node','Hardware Design Selection - Sim PC Node1']
        Node1=['Node Supplier (Sim PC)1','Node Supplier (Sim PC)']
        hard_disk=['Additional Hard Disk (Sim PC Cab)','Additional Hard Disk (Sim PC Desk)']
        add_memory=['Additional Memory (Sim PC Cab)','Additional Memory (Sim PC Desk)']
        attr_mapp =['SVR_PER_HP_Rack_RAID5','SVR_PER_DELL_Rack_RAID1_RUG','SVR_PER_DELL_Tower_RAID1','SVR_PER_DELL_Rack_RAID1','SVR_STD_DELL_Tower_RAID1','SVR_STD_DELL_Rack_RAID1','SVR_PER_DELL_Rack_RAID5','SVR_F_PER_DELL_Tower_RAID1','SVR_F_PER_DELL_Rack_RAID1','SVR_F_PER_HP_Tower_RAID1']
        #CXCPQ-37552
        for (j,k,l,m) in zip(server1,Node1,hard_disk,add_memory):
            Node_flex1=Product.Attr(str(j)).GetValue()
            Trace.Write(j)
            Node1=Product.Attr(str(k)).GetValue()
            hard_disk=Product.Attr(str(l)).GetValue()
            add_memory=Product.Attr(str(m)).GetValue()
            Trace.Write(add_memory)
            #CXCPQ-37552
            if Node_flex1=="SVR_PER_HP_Rack_RAID5" and Node1=="Honeywell" and hard_disk=="Yes":
                Trace.Write('test1')
                qnt11=int(Product.Attr('SIM-ACE Licenses (0-7)').GetValue()) if Product.Attr('SIM-ACE Licenses (0-7)').GetValue()!='' else 0
                qnt12=int(Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()) if Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()!='' else 0
                qnt13=int(Product.Attr('SIM-FFD Licenses (0-125)').GetValue()) if Product.Attr('SIM-FFD Licenses (0-125)').GetValue()!='' else 0
                pcserever_qnt_nonnode=D.Ceiling((qnt11+D.Ceiling(0.4*qnt12)+D.Ceiling(0.1*qnt13))/4.0)
            #CXCPQ-37554
            if Node_flex1=="SVR_PER_HP_Rack_RAID5" and Node1=="Honeywell" and add_memory=="16GB":
                Trace.Write('test1')
                qnt11=int(Product.Attr('SIM-ACE Licenses (0-7)').GetValue()) if Product.Attr('SIM-ACE Licenses (0-7)').GetValue()!='' else 0
                qnt12=int(Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()) if Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()!='' else 0
                qnt13=int(Product.Attr('SIM-FFD Licenses (0-125)').GetValue()) if Product.Attr('SIM-FFD Licenses (0-125)').GetValue()!='' else 0
                PCserever_qntnode1=D.Ceiling((qnt11+D.Ceiling(0.4*qnt12)+D.Ceiling(0.1*qnt13))/4.0)
            #CXCPQ-37553
            if Node_flex1=="SVR_PER_DELL_Rack_RAID5" and Node1=="Honeywell" and add_memory=="16GB":
                Trace.Write('test1')
                qnt11=int(Product.Attr('SIM-ACE Licenses (0-7)').GetValue()) if Product.Attr('SIM-ACE Licenses (0-7)').GetValue()!='' else 0
                qnt12=int(Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()) if Product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue()!='' else 0
                qnt13=int(Product.Attr('SIM-FFD Licenses (0-125)').GetValue()) if Product.Attr('SIM-FFD Licenses (0-125)').GetValue()!='' else 0
                PCserever_qntnode2=D.Ceiling((qnt11+D.Ceiling(0.4*qnt12)+D.Ceiling(0.1*qnt13))/4.0)
            Trace.Write('ab '+str(pcserever_qnt_nonnode))
            Trace.Write('ab '+str(PCserever_qntnode1))
    return pcserever_qnt_nonnode,PCserever_qntnode1,PCserever_qntnode2

#CXCPQ-37552,#CXCPQ-37554,CXCPQ-37553
def QNTCXCPQ_37552(Product):
    svr_hardt37547=svr_hardnodet37547=svr_hardt37552=svr_hardt16gb=svr_hardnodet1=svr_hardnodet2=svr_hardt16gb1=0
    if Product.Name == "Experion Enterprise Group":
        pcserever_qnt_nonnode,PCserever_qntnode1,PCserever_qntnode2=Simulation_PC(Product)
        svr_hardt37547=svr_hardnodet37547=svr_hardt37552=svr_hardnodet37552=svr_hardt16gb=0
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        #Trace.Write(Redundancy)
        question=['Server Node Type_desk','Server_NodeType']
        node=['Node Supplier_server','Node_Supplier_Server']
        hard_disk1=['Additional Hard Disk1','AdditionalHard_Disk']
        add_mem=['Additional Memory_Server Disk','AdditionalMemory_Server Disk']
        server=['Hardware Design Selection_ ACE_Node','Hardware Design Selection_ACE Node','Hardware Design Selection_ACE_T_Node','Hardware Design Selection','Hardware Design Selection - EAPP Node','Hardware_Design_Selection - EAPP Node','Hardware Selection']
        Server_mapping=['ACE Node Tower Mount Desk','ACE Node Rack Mount Cabinet','ACE_T_Node _Tower_Mount_Desk','ACE_T_Node _Rack_Mount_Cabinet','Experion APP Node - Tower Mount','Experion APP Node - Rack Mount','Mobile Server Nodes (0-1)']
        server_node=['Node Supplier_ACE1','Node Supplier_ACE','Node_Supplier_ACE_T','Node Supplier_ACE_T','Node Supplier_EAPP','Node_Supplier_EAPP','Node Supplier Server1']
        add_mem1=['Additional Memory ACE_desk_pre','Additional Memory_ACE','Additional Memory (ACE-T)','Additional Memory_ACE_T','Additional Memory_EAPP','Additional_Memory_EAPP','Additional Memory (Mobile Server)']
        server_Hard=['Additional Hard Disk ACE desk pre','Additional Hard Disk _ACE','Additional Hard Disk (ACE-T)','Additional Hard Disk_ACE_T','Additional Hard Disk_EAPP','Additional_Hard_Disk_EAPP','Additional Hard Disk (Mobile Server)']
        for (m,n,p,l) in zip(question,node,hard_disk1,add_mem):
            Node_flex1=Product.Attr(str(m)).GetValue()
            Node1=Product.Attr(str(n)).GetValue()
            hard_disk1=Product.Attr(str(p)).GetValue()
            add_mem=Product.Attr(str(l)).GetValue()
            #Trace.Write(hard_disk1)
            #CXCPQ-37552
            if Redundancy=="Redundant" and Node_flex1=="SVR_PER_HP_Rack_RAID5" and hard_disk1=="Yes" and Node1=="Honeywell":
                svr_hardnodet37547=2
            elif Redundancy=="Non Redundant" and Node_flex1=="SVR_PER_HP_Rack_RAID5" and hard_disk1=="Yes" and Node1=="Honeywell":
                svr_hardnodet37547=1
            #CXCPQ-37554
            if Redundancy=="Redundant" and Node_flex1=="SVR_PER_HP_Rack_RAID5" and add_mem=="16GB" and Node1=="Honeywell":
                svr_hardnodet1=2
            elif Redundancy=="Non Redundant" and Node_flex1=="SVR_PER_HP_Rack_RAID5" and add_mem=="16GB" and Node1=="Honeywell":
                svr_hardnodet1=1
            #CXCPQ-37553
            if Redundancy=="Redundant" and Node_flex1=="SVR_PER_DELL_Rack_RAID5" and add_mem=="16GB" and Node1=="Honeywell":
                svr_hardnodet2=2
            elif Redundancy=="Non Redundant" and Node_flex1=="SVR_PER_DELL_Rack_RAID5" and add_mem=="16GB" and Node1=="Honeywell":
                svr_hardnodet2=1
        for (i,j,k,l,m) in zip(server,Server_mapping,server_node,server_Hard,add_mem1):
            attr_name = str(j)
            Node_flex=Product.Attr(str(i)).GetValue()
            Node=Product.Attr(str(k)).GetValue()
            hard_disk=Product.Attr(str(l)).GetValue()
            add_mem1=Product.Attr(str(m)).GetValue()
            if Node_flex=="SVR_PER_HP_Rack_RAID5" and Node=="Honeywell" and hard_disk=="Yes":
                svr_hardt37547 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
            #CXCPQ-37554
            if Node_flex=="SVR_PER_HP_Rack_RAID5" and Node=="Honeywell" and add_mem1=="16GB":
                svr_hardt16gb +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
            #CXCPQ-37553
            if Node_flex=="SVR_PER_DELL_Rack_RAID5" and Node=="Honeywell" and add_mem1=="16GB":
                svr_hardt16gb1 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        svr_hardt16gb=svr_hardt16gb+svr_hardnodet1+PCserever_qntnode1
        svr_hardt16gb1=svr_hardt16gb1+svr_hardnodet2+PCserever_qntnode2
        svr_hardt37552=svr_hardt37547+svr_hardnodet37547+pcserever_qnt_nonnode
    return svr_hardt37552,svr_hardt16gb,svr_hardt16gb1

##CXCPQ-37556,#CXCPQ-37555,CXCPQ-37557,CXCPQ-37558,CXCPQ-37559
def MZ_PCIS02(Product):
    svr_MZ_PCIS02_1=svr_MZ_PCIS02_2=svr_MZ_PCIS02_3=svr_MZ_PCIS02_4=svr_MZ_PCIS02_5=svr_MZ_PCIS02_6=svr_MZ_PCIS02_7=svr_MZ_PCIS02_8=svr_MZ_PCIS02_9=svr_MZ_PCIS02_10=0
    if Product.Name == "Experion Enterprise Group":
        #CXCPQ-37556
        pcserever_qnt_nonnode,PCserever_qntnode1,PCserever_qntnode2=Simulation_PC(Product)
        svr_hardt37547=svr_hardnodet37547=svr_hardt37552=svr_hardnodet37552=svr_hardt16gb=0
        Redundancy=Product.Attr('Server Redundancy Requirement?').GetValue()
        #Trace.Write(Redundancy)
        question=['Server Node Type_desk','Server_NodeType']
        node=['Node Supplier_server','Node_Supplier_Server']
        tpm=['Trusted Platform Module1','TrustedPlatformModule_TPM']
        server=['Hardware Design Selection_ ACE_Node','Hardware Design Selection_ACE Node','Server Type1']
        Server_mapping=['ACE Node Tower Mount Desk','ACE Node Rack Mount Cabinet','Additional Servers']
        server_node=['Node Supplier_ACE1','Node Supplier_ACE','Node Supplier Server']
        tpm1=['Trusted Platform Module_TPM_ACE_desk','Trusted Platform Module_TPM_ACE_Node','Trusted Platform Module_TPM']
        #CXCPQ-37555
        server1=['Hardware Design Selection_ ACE_Node','Hardware Design Selection_ACE Node','Hardware Design Selection_ACE_T_Node','Server Type1']
        Server_mapping1=['ACE Node Tower Mount Desk','ACE Node Rack Mount Cabinet','ACE_T_Node _Tower_Mount_Desk','Additional Servers']
        server_node1=['Node Supplier_ACE1','Node Supplier_ACE','Node_Supplier_ACE_T','Node Supplier Server']
        tpm2=['Trusted Platform Module_TPM_ACE_desk','Trusted Platform Module_TPM_ACE_Node','Trusted Platform Module_TPM_ACE_T','Trusted Platform Module_TPM']
        #CXCPQ-37556,#CXCPQ-37555
        for (i,j,k) in zip(question,node,tpm):
            Node_flex1=Product.Attr(str(i)).GetValue()
            Node1=Product.Attr(str(j)).GetValue()
            Tpm=Product.Attr(str(k)).GetValue()
            #CXCPQ-37556
            if Node_flex1=="SVR_PER_DELL_Rack_RAID1_RUG" and Tpm=="Yes" and Node1=="Honeywell" and Redundancy=="Redundant":
                svr_MZ_PCIS02_1=2
            elif Node_flex1=="SVR_PER_DELL_Rack_RAID1_RUG" and Tpm=="Yes" and Node1=="Honeywell"and  Redundancy=="Non Redundant":
                svr_MZ_PCIS02_1=1
            #CXCPQ-37555
            if Node_flex1=="SVR_PER_HP_Rack_RAID5" and Tpm=="Yes" and Node1=="Honeywell"and  Redundancy=="Redundant":
                svr_MZ_PCIS02_3=2
            elif Node_flex1=="SVR_PER_HP_Rack_RAID5" and Tpm=="Yes" and Node1=="Honeywell" and Redundancy=="Non Redundant":
                svr_MZ_PCIS02_3=1
            #CXCPQ-37557
            if Node_flex1=="SVR_PER_DELL_Tower_RAID1" and Tpm=="Yes" and Node1=="Honeywell"and  Redundancy=="Redundant":
                svr_MZ_PCIS02_7=2
            elif Node_flex1=="SVR_PER_DELL_Tower_RAID1" and Tpm=="Yes" and Node1=="Honeywell" and Redundancy=="Non Redundant":
                svr_MZ_PCIS02_7=1
            #CXCPQ-37558
            if Node_flex1=="SVR_PER_DELL_Tower_RAID1" and Tpm=="No" and Node1=="Honeywell"and  Redundancy=="Redundant":
                svr_MZ_PCIS02_5=2
            elif Node_flex1=="SVR_PER_DELL_Tower_RAID1" and Tpm=="No" and Node1=="Honeywell" and Redundancy=="Non Redundant":
                svr_MZ_PCIS02_5=1
            #CXCPQ-37559
            if Node_flex1=="SVR_PER_DELL_Rack_RAID1" and Tpm=="Yes" and Node1=="Honeywell"and  Redundancy=="Redundant":
                svr_MZ_PCIS02_9=2
            elif Node_flex1=="SVR_PER_DELL_Rack_RAID1" and Tpm=="Yes" and Node1=="Honeywell" and Redundancy=="Non Redundant":
                svr_MZ_PCIS02_9=1
            Trace.Write('svr_MZ_PCIS02_5: '+str(svr_MZ_PCIS02_5))
        for (i,j,k,l) in zip(server,server_node,tpm1,Server_mapping):
            Node_flex1=Product.Attr(str(i)).GetValue()
            Node1=Product.Attr(str(j)).GetValue()
            Tpm=Product.Attr(str(k)).GetValue()
            attr_name = str(l)
            #CXCPQ-37556
            if Node_flex1=="SVR_PER_DELL_Rack_RAID1_RUG" and Tpm=="Yes" and Node1=="Honeywell":
                svr_MZ_PCIS02_2 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
            #CXCPQ-37559
            if Node_flex1=="SVR_PER_DELL_Rack_RAID1" and Tpm=="Yes" and Node1=="Honeywell":
                svr_MZ_PCIS02_10 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        for (i,j,k,l) in zip(server1,server_node1,tpm2,Server_mapping1):
            Node_flex1=Product.Attr(str(i)).GetValue()
            Node1=Product.Attr(str(j)).GetValue()
            Tpm=Product.Attr(str(k)).GetValue()
            attr_name = str(l)
            #CXCPQ-37555
            if Node_flex1=="SVR_PER_HP_Rack_RAID5" and Tpm=="Yes" and Node1=="Honeywell":
                svr_MZ_PCIS02_4 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
            #CXCPQ-37558
            if Node_flex1=="SVR_PER_DELL_Tower_RAID1" and Tpm=="No" and Node1=="Honeywell":
                svr_MZ_PCIS02_6 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
            #CXCPQ-37557
            if Node_flex1=="SVR_PER_DELL_Tower_RAID1" and Tpm=="Yes" and Node1=="Honeywell":
                svr_MZ_PCIS02_8 +=int(Product.Attr(str(attr_name)).GetValue()) if Product.Attr(str(attr_name)).GetValue()!='' else 0
        svr_MZ_PCIS02_2=svr_MZ_PCIS02_2+svr_MZ_PCIS02_1
        svr_MZ_PCIS02_4=svr_MZ_PCIS02_4+svr_MZ_PCIS02_3
        svr_MZ_PCIS02_6=svr_MZ_PCIS02_6+svr_MZ_PCIS02_5
        svr_MZ_PCIS02_8=svr_MZ_PCIS02_8+svr_MZ_PCIS02_7
        svr_MZ_PCIS02_10=svr_MZ_PCIS02_10+svr_MZ_PCIS02_9
    return svr_MZ_PCIS02_2,svr_MZ_PCIS02_4,svr_MZ_PCIS02_6,svr_MZ_PCIS02_8,svr_MZ_PCIS02_10