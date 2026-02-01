import math

def getFloat(Var):
    if Var:
        return float(Var)
    return 0.0
def getPerc():
    attr_container = []
    try:
        attr_container = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[0].Columns
    except:
        pass
    PMD_IO_PERC = 0
    io_per = 0
    for cols in attr_container:
        if cols.Name in ['PMD_IO_Space_Req']:
            PMD_IO_PERC = float(getFloat(PMD_IO_PERC) + (getFloat(cols.Value) * 0.01))
            return(PMD_IO_PERC)

def get_IO_Per():
    attr_container = []
    try:
        attr_container = Item.SelectedAttributes.GetContainerByName('PMD_IO_ControlEdge_PLC_IO_Cards').Rows[0].Columns
    except:
        pass
    io_per = 0
    for cols in attr_container:
        if cols.Name in ['PMD_IO_Space_Req_2']:
            io_per = float(getFloat(io_per) + (getFloat(cols.Value) * 0.01))
            return(io_per)        
        
Cond = TagParserQuote.ParseString("[AND]([OR](([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PAS)),([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,LSS)),([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PMC))),[EQ](<*CTX( Quote.CustomField(Quote Type) )*>,Projects), [GT](<*Table(select COUNT(*) from cart_item i where i.CATALOGCODE = 'PRJT' and i.cart_id=<*CTX(Quote.CartId)*> and i.USERID=<*CTX(Quote.OwnerId)*>)*>,0))")

if Cond == '1':
    hierarchy = {"L1":"System Group","L2":"PMD System"}
    #Control and Cabinet
    sysgrp_columns_seq=['PMD_RFCE_ProfibusDP','PMD_NRFCE_ProfibusDP','PMD_NRFCE_ProfinetPN','PMD_FCECabinet_Max8','PMD_Cabinet_Max16','PMD_24VDC_Redundant_Power Supply']
    sysgrp_columns = ['PMD_RFCE_ProfibusDP','PMD_NRFCE_ProfibusDP','PMD_NRFCE_ProfinetPN','PMD_FCECabinet_Max','PMD_24VDC_Redundant_Power Supply']
    #System_grp = ['Controller_and_Cabinets_Information',' #Profibus_Interfaces','I/O_Information','Rack_and_Cabinet_Information','Profibus/Profinet_Components']
    sysgrp_columns1 = ['CE_System_Asset', 'CE_System_Number', 'New_Expansion']
    sysgrp_columns_seq1 = ['CE_System_Asset', 'CE_System_Number', 'New_Expansion']
    lst = ["CE_Site_Voltage", "PLC_IO_Filler_Module", "PLC_IO_Spare", "PLC_IO_Slot_Spare", "PLC_Shielded_Terminal_Strip", "CE_Selected_Products", "CE_Add_System_Rows", "CE_Apply_System_Number", "CE_Scope_Choices", "New_Expansion", "Sys_Group_Name", "PLC_Software_Release","PLC_CG_Name","PLC_RG_Name", "CE PLC Engineering Execution Year"]
    
    #proj_columns = ['PMD_System_Asset_MSID','PMD_System_Number']
    proj_columns = ['Labor_Loop_Drawings', 'Labor_Percentage_FAT', 'Labor_Marshalling_Database', 'New_Expansion']
    proj_columns_seq = ['Labor_Loop_Drawings', 'Labor_Percentage_FAT', 'Labor_Marshalling_Database', 'New_Expansion']

    #proj_columns = ['PMD_System_Asset_MSID','PMD_System_Number']
    #RC_Information
    #Added by Siddharth

    rack_cab_seq = ['PMD_ER_CCCT','PMD_ER_CCCT_R','PMD_IOC','PMD_IOC_Aldix','PMD_Dual_Sided_CC','PMD_Single_Sided_CC_600','PMD_Single_Sided_CC_400','PMD_Furnished_PIE','PMD_SSCCC','PMD_DSCCC','PMD_SSCC1200','PMD_DSCC1200','PMD_SSCC482','PMD_DSCC482','PMD_SSCCD400','PMD_FPS10A','PMD_FPS20A']
    
    rack_cab_req = ['IO_Racks_RC','IOC_CP_RC','PMD_Dual_Sided_CC','PMD_Single_Sided_CC_600','PMD_Single_Sided_CC_400','PMD_Furnished_PIE','PMD_SS','PMD_FPS']

    #Profibus/Profinet Components
    pb_pn_com_seq = ['PMD_Repeater_for_Profibus','PMD_Repeater_for_Profibus_Diagnosis','PMD_DP_Coupler_ProfibusDP_Networks','PMD_AB7646-F_Anybus_X-gateway','PMD_Anybus_X-gateway','PMD_DP_PA_Link','PMD_DP_PA_Coupler','PMD_OLM_G11_Glass_FO_Cable','PMD_OLM_G12_Glass_FO_Cable','PMD_OLM_P11_Plastic_FO_Cable','PMD_OLM_P12_Plastic_FO_Cable','PMD_SCALANCE_XC206-2_Switch','PMD_SCALANCE X101-1']

    pb_pn = ['PMD_Repeater','PMD_Coupler_gateway','Profibus_PA','PMD_OLM','PMD_Switches']
    #I/O information list
    
    io_info_lst = ['PMD_CC_Cards','PMD_CC_Cards','PMD_CC_Cards','PMD_CC_Cards','PMD_CC_Cards','PMD_CC_Cards','PMD_CC_Cards','PMD_CC_Cards','PMD_CC_Cards','PMD_CC_Cards']
    
    
    io_info_attrs_lst = ['PMD_Analog_OC','PMD_Analog_IC','PMD_Binary_OC','PMD_Power_BOC_115V','PMD_Power_BOC_230V','PMD_Binary_IC_16Channel','PMD_Binary_IC_24Channel','PMD_Power_BIC_115V','PMD_Power_BIC_230V','PMD_PROFIBUS','PMD_PRIFINET','PMD_Add+2','PMD_24VDC','PMD_PFIPB','PMD_PFIPN']
    
    io_info = ['PMD_Analog_OC','PMD_Analog_IC','PMD_Binary_OC','PMD_Power_BOC_115V','PMD_Power_BOC_230V','PMD_Binary_IC_16Channel','PMD_Binary_IC_24Channel','PMD_Power_BIC_115V','PMD_Power_BIC_230V','Pulse_Input']
    #I/O information Cards list
    #Added by Siddharth CXCPQ-25995
    io_info_attrs_lst_cc = ['PMD_Analog_OC','PMD_Analog_IC','PMD_Binary_OC','PMD_Power_BOC_115V','PMD_Power_BOC_230V','PMD_Binary_IC_16Channel','PMD_Binary_IC_24Channel','PMD_Power_BIC_115V','PMD_Power_BIC_230V','PMD_PROFIBUS','PMD_PRIFINET','PMD_Add+2','PMD_24VDC','PMD_PFIPB','PMD_PFIPN','PMD_IO_Space_Req']
    
    io_info_cc = ['PMD_Analog_OC','PMD_Analog_IC','PMD_Binary_OC','PMD_Power_BOC_115V','PMD_Power_BOC_230V','PMD_Binary_IC_16Channel','PMD_Binary_IC_24Channel','PMD_Power_BIC_115V','PMD_Power_BIC_230V']
    #Rack Cab info
    pmd_rc_lst = ['PMD_CE_PLC_8','PMD_CE_PLC_12','PMD_CE_PLC_IO','PMD_SSCCC','PMD_DSCCC','PMD_SSCC1200','PMD_DSCC1200','PMD_SSCC482','PMD_DSCC482','PMD_SSCCD400','PMD_FPS10A','PMD_FPS20A']
    pmd_rc_seq = ['IO_racks','PMD_CE_PLC_IO','Cross_CC','PMD_fps']
    
    # I/O's with ControlEdge PLC I/O Cards
    plc_io_cards = ['PMD_Uni_IO','PMD_Uni_AI','PMD_DI_16','PMD_DI_32','PMD_DO_8','PMD_DO_32']
    plc_io_cc = ['PMD_Uni_IO','PMD_Uni_AI','PMD_DI_16','PMD_DI_32','PMD_DO_8','PMD_DO_32','PMD_IO_Space_Req_2']
    
    pb_interface_col = ['Device','Devices','AI','AO','DI','DO']
    pb_cont_lst = ['PMD_Profibus_Drives_Cont1','PMD_Profibus_Links_and_Gateways_Cont1','PMD_Profibus_Motor_Starters and_CD_Cont','PMD_Other_Profibus_DP-Devices_Cont','PMD_Profibus_Modular_IO_Cont','PMD_Profibus_Displays_Cont','PMD_Profinet_Device_Support_blocks_Cont']
    
    Qt_Table = Quote.QuoteTables["PT_PMD_System"]
    Qt_Table.Rows.Clear()
    PMD = ''
    
    # Added CXCPQ-27845
    for Item in Quote.MainItems:
            if Item.ProductName == "New / Expansion Project":
                newRow = Qt_Table.AddNewRow()
                newRow["Project"] = Item.PartNumber
                newRow["Project_GUID"] = Item.QuoteItemGuid
                
    for Item in Quote.MainItems:
        if hierarchy["L1"] == Item.ProductName: 
            newRow = Qt_Table.AddNewRow()
            newRow["System_Group"] = Item.PartNumber
            newRow["System_Grp_GUID"] = Item.QuoteItemGuid 
            #newRow["System_Item_GUID_"] = Item.QuoteItemGuid
            
    for Item in Quote.MainItems:
        if hierarchy["L2"] == Item.ProductName:
            PMD ='Yes'
            newRow = Qt_Table.AddNewRow()
            newRow["System_Name"] = Item.ProductName
            newRow["System_Item_GUID_"] = Item.QuoteItemGuid
            newRow["System_Grp_GUID"] = Item.ParentItemGuid
    if PMD != 'Yes':
        Qt_Table.Rows.Clear()
    
    for row in Qt_Table.Rows:
        for Item in Quote.MainItems:
            if hierarchy["L1"] == Item.ProductName and row["System_Grp_GUID"] == Item.QuoteItemGuid:
                row["System_Group"] = Item.PartNumber    
                
    Qt_Table.Save()            
    
    for row in Qt_Table.Rows:
        for Item in Quote.Items:
            PMD_Max = 0
            io_racks_ext = 0
            pmd_ioc_ext = 0
            #Added
            pmd_ss_ext = 0
            #
            pmd_fps_ext = 0
            pmd_rep = 0
            pmd_coup = 0
            pmd_PA = 0
            pmd_olm = 0
            pmd_swt = 0
            PMD_IO = 0
            PMD_IO_Total = 0
            # IO Channel Cards
            PMD_IO_PERC = 0
            Perc = 0
            Channel_ten_Analog = 0
            ch_ten = 0
            Channel_sixtn_Binary = 0
            ch_sixtn = 0
            Channel_eight_Power = 0
            ch_eight = 0
            Channel_twfour_Binary = 0
            ch_twfour = 0
            slot_plc = 0
            cross_cc = 0
            plc_fps = 0
            io_space = 0
            IO_dict = {}
            IO_dict_cc = {}
            expected_Result_Total = []
            Sysgrpdic = {}
            rack_dict_et = {}
            pb_pn_dic = {}
            pmd_rc_dic ={}
            plc_io_dic = {}
            prob_dic = {}
            proj_columns_dic = {}
            Sysdic = {}
            io_cards_dic = {}
            
            if row['Project_GUID'] == Item.QuoteItemGuid and Item.ProductName == "New / Expansion Project" and row['System_Group'] == '' and row['System_Name'] == '':
                proj_columns_dic = {}    
                for attr in Item.SelectedAttributes:
                    try:
                        attr_containers = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[0].Columns
                        #Trace.Wite('----attts_selected'+str(attr_containers))
                        for column in attr_containers: 
                            if column.Name in proj_columns and Item.ProductName == "New / Expansion Project" and row["Project_GUID"] == Item.QuoteItemGuid:
                                proj_columns_dic[column.Name] = column.Value
                                proj_res = [proj_columns_dic[d] for d in proj_columns_seq if d in proj_columns_dic.keys()]
                                row['Project_info'] = "|".join(proj_res) 
                    except:
                        pass              
            elif row['System_Grp_GUID'] == Item.QuoteItemGuid and Item.ProductName == "System Group" and row['System_Name'] == '' :
                Sysdic = {}
                for attr in Item.SelectedAttributes:
                        try:
                            attr_containers = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[0].Columns
                            #Trace.Wite('----attts_selected'+str(attr_containers))
                        except:
                            pass
                        for column in attr_containers:
                            if column.Name in sysgrp_columns1:
                                Sysdic[column.Name] = column.Value
                            expectedResult = [Sysdic[d] for d in sysgrp_columns_seq1 if d in Sysdic.keys()]
                            #Trace.Write("System Group: "+str(expectedResult)+"	 Column Name: "+str(column.Name))
                            row['System_Grp'] = "|".join(expectedResult)
            
            elif row['System_Item_GUID_'] == Item.QuoteItemGuid and Item.ProductName == "PMD System":
                for attr in Item.SelectedAttributes:
                    try:
                        attr_containers = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[0].Columns
                        Trace.Wite('----attts_selected'+str(attr_containers))
                    except:
                        pass
                    for column in attr_containers:
                        if column.Name in sysgrp_columns_seq:
                            Trace.Write('column 99')
                            if column.Name in ['PMD_FCECabinet_Max8','PMD_Cabinet_Max16']:
                                PMD_Max = int(getFloat(PMD_Max) + getFloat(column.Value))
                                Sysgrpdic["PMD_FCECabinet_Max"] = str(PMD_Max)
                                
                            else:
                                Sysgrpdic[column.Name] = column.Value
                                #Trace.Write('----------Container2-------'+str(Sysgrpdic[column.Name]))
                            expectedResult = [Sysgrpdic[d] for d in sysgrp_columns if d in Sysgrpdic.keys()]
                            row['Controller_and_Cabinets_Information'] = "|".join(expectedResult)
                        elif column.Name in rack_cab_seq and attr.Name != 'PMD_Field Power Supply_Cont_PLCIO' and attr.Name != 'PMD_Cross_Connection_Cabinets_Cont_PLCIO':
                            #Trace.Write('Column')
                            if column.Name in ['PMD_ER_CCCT','PMD_ER_CCCT_R']:
                                io_racks_ext = int(getFloat(io_racks_ext) + getFloat(column.Value))
                                rack_dict_et["IO_Racks_RC"] = str(io_racks_ext)
                                #Trace.Write('----R1-----'+str(io_racks_ext))
                            if column.Name in ['PMD_IOC','PMD_IOC_Aldix']:
                                pmd_ioc_ext = int(getFloat(pmd_ioc_ext) + getFloat(column.Value))
                                rack_dict_et["IOC_CP_RC"] = str(pmd_ioc_ext)
                                #Trace.Write('----R2-----'+str(pmd_ioc_ext))
                            if column.Name in ['PMD_SSCCC','PMD_DSCCC','PMD_SSCC1200','PMD_DSCC1200','PMD_SSCC482','PMD_DSCC482','PMD_SSCCD400'] and attr.Name == 'PMD_Cross_Connection_Cabinets_Cont':
                                pmd_ss_ext = int(getFloat(pmd_ss_ext) + getFloat(column.Value))
                                rack_dict_et['PMD_SS'] = str(pmd_ss_ext)
                                #Trace.Write('----R3---'+str(pmd_ss_ext))
                                #Trace.Write('-------R3----'+str(type(pmd_ss_ext)))
                            if column.Name in ['PMD_FPS10A','PMD_FPS20A'] and attr.Name == 'PMD_Field Power Supply_Cont':
                                pmd_fps_ext = int(getFloat(pmd_fps_ext) + getFloat(column.Value))
                                rack_dict_et["PMD_FPS"] = str(pmd_fps_ext)
                                #Trace.Write('----R4---'+str(pmd_fps_ext))
                                #Trace.Write('-------R4----'+str(type(pmd_fps_ext)))
                            else:
                                rack_dict_et[column.Name] = column.Value
                            result_ext = [rack_dict_et[d] for d in rack_cab_req if d in rack_dict_et.keys()]
                            row['Rack_and_Cabinet_Information'] = '|'.join(result_ext)
                        elif column.Name in pb_pn_com_seq:
                            if column.Name in ['PMD_Repeater_for_Profibus','PMD_Repeater_for_Profibus_Diagnosis']:
                                #try:
                                pmd_rep = int(getFloat(pmd_rep) + getFloat(column.Value))
                                pb_pn_dic["PMD_Repeater"] = str(pmd_rep) 
                                #except:
                                    #pass
                                
                            elif column.Name in ['PMD_DP_Coupler_ProfibusDP_Networks','PMD_AB7646-F_Anybus_X-gateway','PMD_Anybus_X-gateway']:
                                #try:
                                    #Trace.Write("===============" + type(column.Value))
                                pmd_coup = int(getFloat(pmd_coup) + getFloat(column.Value))
                                pb_pn_dic["PMD_Coupler_gateway"] = str(pmd_coup)
                               # except:
                                    #pass
                            elif column.Name in ['PMD_DP_PA_Link','PMD_DP_PA_Coupler']:
                                #try:
                                pmd_PA = int(getFloat(pmd_PA) + getFloat(column.Value))
                                pb_pn_dic["Profibus_PA"] = str(pmd_PA) 
                                #except:
                                    #pass
                                
                            elif column.Name in ['PMD_OLM_G11_Glass_FO_Cable','PMD_OLM_G12_Glass_FO_Cable','PMD_OLM_P11_Plastic_FO_Cable','PMD_OLM_P12_Plastic_FO_Cable']:
                                #try:
                                pmd_olm = int(getFloat(pmd_olm) + getFloat(column.Value))
                                pb_pn_dic["PMD_OLM"] = str(pmd_olm)
                                #except:
                                  #  pass
                            elif column.Name in ['PMD_SCALANCE_XC206-2_Switch','PMD_SCALANCE X101-1']:
                                #try:
                                pmd_swt = int(getFloat(pmd_swt) +getFloat(column.Value))
                                pb_pn_dic["PMD_Switches"] = str(pmd_swt)
                                #except:
                                   # pass
                            else:
                                pb_pn_dic[column.Name]= column.Value    
                            pb_pn_res = [pb_pn_dic[d] for d in pb_pn if d in pb_pn_dic.keys()]    
                            row['Profibus_Profinet_Components'] = "|".join(pb_pn_res)
                        #Added CXCPQ-25995
                        elif column.Name in  io_info_attrs_lst:
                            if column.Name in ['PMD_PROFIBUS','PMD_PRIFINET','PMD_Add+2','PMD_24VDC','PMD_PFIPB','PMD_PFIPN']:
                                PMD_IO_Total = int(getFloat(PMD_IO_Total) + getFloat(column.Value))
                                PMD_IO = PMD_IO_Total * 2
                                IO_dict["Pulse_Input"] = str(PMD_IO)
                            else:
                                IO_dict[column.Name] = column.Value
                            result_io = [IO_dict[d] for d in io_info if d in IO_dict.keys()]
                            row['I_O_Information'] = "|".join(result_io)
                            if column.Name in ['PMD_Analog_OC','PMD_Analog_IC']:
                                ch_ten = 10
                                Channel_ten_Analog = int(math.ceil(float(getFloat(column.Value) * (1+getPerc())/ch_ten)))
                                IO_dict_cc[column.Name] = str(Channel_ten_Analog)
                                #Trace.Write('------IO_Dict---- Column Name -----' +str(Channel_ten_Analog))
                            if column.Name in ['PMD_Binary_OC','PMD_Binary_IC_16Channel','PMD_Power_BIC_115V','PMD_Power_BIC_230V']:
                                ch_sixtn = 16
                                Channel_sixtn_Binary = int(math.ceil(float(getFloat(column.Value) * (1+getPerc())/ch_sixtn)))
                                IO_dict_cc[column.Name] = str(Channel_sixtn_Binary)
                            if column.Name in ['PMD_Power_BOC_115V','PMD_Power_BOC_230V']:
                                ch_eight = 8
                                Channel_eight_Power = int(math.ceil(float(getFloat(column.Value) * (1+getPerc())/ch_eight)))
                                IO_dict_cc[column.Name] = str(Channel_eight_Power)
                            if column.Name in ['PMD_Binary_IC_24Channel']:
                                ch_twfour = 24
                                Channel_twfour_Binary = int(math.ceil(float(getFloat(column.Value) * (1+getPerc())/ch_twfour)))
                                IO_dict_cc[column.Name] = str(Channel_twfour_Binary)
                            result_io_cc = [IO_dict_cc[d] for d in io_info_cc if d in IO_dict_cc.keys()]
                            row['I_O_Information_Card'] = "|".join(result_io_cc)
                        
                        elif column.Name in plc_io_cards:
                            plc_io_dic[column.Name] = column.Value
                            result = [plc_io_dic[d] for d in plc_io_cards if d in plc_io_dic.keys()]                 
                            row['ControlEdge_PLC_I_O_Information'] = "|".join(result) 
                            if column.Name in ['PMD_Uni_IO','PMD_DI_16']:
                                io_16 = int(math.ceil(float(getFloat(column.Value) * (1+get_IO_Per())/16)))
                                io_cards_dic[column.Name] = str(io_16)
                            elif column.Name in ['PMD_Uni_AI','PMD_DO_8']:
                                io_8 = int(math.ceil(float(getFloat(column.Value) * (1+get_IO_Per())/8)))
                                io_cards_dic[column.Name] = str(io_8)
                            elif column.Name in  ['PMD_DI_32','PMD_DO_32']:
                                io_32 = int(math.ceil(float(getFloat(column.Value) * (1+get_IO_Per())/32)))
                                io_cards_dic[column.Name] = str(io_32) 
                            res = [io_cards_dic[d] for d in plc_io_cards if d in io_cards_dic.keys()]
                            row['CE_PLC_IO_Cards'] = "|".join(res)    
                        
                        elif column.Name in pmd_rc_lst and attr.Name != 'PMD_Cross_Connection_Cabinets_Cont' and attr.Name != 'PMD_Field Power Supply_Cont':
                            if column.Name in ['PMD_CE_PLC_8','PMD_CE_PLC_12']:
                                slot_plc = int(getFloat(slot_plc) + getFloat(column.Value))
                                pmd_rc_dic["IO_racks"] = str(slot_plc)
                            if column.Name in ['PMD_SSCCC','PMD_DSCCC','PMD_SSCC1200','PMD_DSCC1200','PMD_SSCC482','PMD_DSCC482','PMD_SSCCD400'] and attr.Name == 'PMD_Cross_Connection_Cabinets_Cont_PLCIO':
                                cross_cc = int(getFloat(cross_cc) + getFloat(column.Value))
                                pmd_rc_dic["Cross_CC"] = str(cross_cc)
                            if column.Name in ['PMD_FPS10A','PMD_FPS20A'] and attr.Name == 'PMD_Field Power Supply_Cont_PLCIO':
                                plc_fps = int(getFloat(plc_fps) + getFloat(column.Value))
                                pmd_rc_dic["PMD_fps"] = str(plc_fps)
                            else:
                                pmd_rc_dic[column.Name] = column.Value
                            result_plc = [pmd_rc_dic[d] for d in pmd_rc_seq if d in pmd_rc_dic.keys()]    
                            row['Rack_and_Cabinet_Info'] = "|".join(result_plc)
                                
    Qt_Table.Save()                    
    
    
    
    
    