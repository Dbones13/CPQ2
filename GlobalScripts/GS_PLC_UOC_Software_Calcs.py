def calc_software_plc_system(attrs, parts_dict,product):

    #CXCPQ-20417--Added by Adarsh
    if attrs.plc_soft_q_med_deliv == "PD" and attrs.plc_soft_q_soft_release in ("172","R172"):
        parts_dict['SP-EMD172'] = 1
    if attrs.plc_soft_q_med_deliv == "PD" and attrs.plc_soft_q_soft_release in ("171","R171"):
        parts_dict['SP-EMD171'] = 1
    if attrs.plc_soft_q_med_deliv == "PD" and attrs.plc_soft_q_soft_release in("170","R170"):
        parts_dict['SP-EMD170'] = 1
    if attrs.plc_soft_q_med_deliv == "PD" and attrs.plc_soft_q_soft_release in("174" ,"R174"):
        parts_dict['SP-EMD174'] = 1
    if attrs.plc_soft_q_med_deliv == "PD" and attrs.plc_soft_q_soft_release in("180","R180"):
        parts_dict['SP-EMD180'] = 1
    if attrs.plc_soft_q_med_deliv == "ED" and attrs.plc_soft_q_soft_release in("172","R172"):
        parts_dict['SP-EMD172-ESD'] = 1
    if attrs.plc_soft_q_med_deliv == "ED" and attrs.plc_soft_q_soft_release in("171","R171"):
        parts_dict['SP-EMD171-ESD'] = 1
    if attrs.plc_soft_q_med_deliv == "ED" and attrs.plc_soft_q_soft_release in("170","R170"):
        parts_dict['SP-EMD170-ESD'] = 1
    if attrs.plc_soft_q_med_deliv == "ED" and attrs.plc_soft_q_soft_release in ("174","R174"):
        parts_dict['SP-EMD174-ESD'] = 1
    if attrs.plc_soft_q_med_deliv == "ED" and attrs.plc_soft_q_soft_release in("180","R180"):
        parts_dict['SP-EMD180-ESD'] = 1

    #CCEECOMMBR-5295--Added by Abhijeet
    if attrs.plc_eng_station_qty != '':
        if attrs.plc_eng_station_model == 'STN_STD_DELL_Tower_NonRAID' and int(attrs.plc_eng_station_qty) > 0:
            parts_dict['TP-FPW242'] = attrs.plc_eng_station_qty
            parts_dict['MZ-PCWS15'] = attrs.plc_eng_station_qty
        if attrs.plc_eng_station_model == 'STN_PER_DELL_Tower_RAID2' and int(attrs.plc_eng_station_qty) > 0:
            parts_dict['MZ-PCWT02'] = attrs.plc_eng_station_qty
            parts_dict['EP-COAS19'] = attrs.plc_eng_station_qty
            parts_dict['MZ-SQLCL4'] = attrs.plc_eng_station_qty
            parts_dict['TP-FPW242'] = attrs.plc_eng_station_qty
        if attrs.plc_eng_station_model == "STN_PER_HP_Tower_RAID1" and int(attrs.plc_eng_station_qty) > 0:
            parts_dict['MZ-PCWS86'] = attrs.plc_eng_station_qty
        if attrs.plc_eng_station_model == "STN_PER_DELL_Rack_RAID1" and int(attrs.plc_eng_station_qty) > 0:
            parts_dict['MZ-PCWR01'] = attrs.plc_eng_station_qty
        if attrs.plc_eng_station_model == "STN_PER_DELL_Tower_RAID1" and int(attrs.plc_eng_station_qty) > 0:
            parts_dict['MZ-PCWT01'] = attrs.plc_eng_station_qty
        if attrs.plc_eng_station_model in ["STN_PER_DELL_Tower_RAID1","STN_PER_DELL_Rack_RAID1","STN_PER_HP_Tower_RAID1"] and int(attrs.plc_eng_station_qty) > 0:
            parts_dict['TP-FPW242'] = attrs.plc_eng_station_qty
            parts_dict['EP-COAW21'] = attrs.plc_eng_station_qty

    
    #CXCPQ-20411--Added by Satya
    if attrs.plc_soft_q_ce_build_client != "" and attrs.plc_soft_q_ce_build_client != 0:
        parts_dict['SP-EBLDR1'] = attrs.plc_soft_q_ce_build_client
    #CXCPQ-20413--Added by Satya
    if attrs.plc_soft_q_mig_tool_usr_lic != "" and attrs.plc_soft_q_mig_tool_usr_lic != 0:
        parts_dict['SP-MAPLC1'] = attrs.plc_soft_q_mig_tool_usr_lic
    #CXCPQ-20414--Added by Satya
    if attrs.plc_soft_q_subsea_mdis_intf != "" and attrs.plc_soft_q_subsea_mdis_intf != 0:
        parts_dict['SP-IMDIS1'] = attrs.plc_soft_q_subsea_mdis_intf
        
    return parts_dict

def calc_software_plc_cg(attrs, parts_dict):
    #CXCPQ-20415--Added by Satya
    if attrs.grp_software_ce_elmm_license != "" and attrs.grp_software_ce_elmm_license != 0:
        parts_dict['SP-CELMM1'] = attrs.grp_software_ce_elmm_license
    #CXCPQ-20416--Added by Satya
    if attrs.grp_software_ce_pl_profinet_usage != "" and attrs.grp_software_ce_pl_profinet_usage!= 0:
        parts_dict['SP-IPROF1'] = attrs.grp_software_ce_pl_profinet_usage
    #CXCPQ-20412--Added by Satya
    try:
        #parts_dict['SP-CSPLC1'] = parts_dict['900CP1-0200']
        #parts_dict['SP-CSPLC1'] = parts_dict['900CP2-0100']
        if attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
            parts_dict['SP-CSPLC1'] = parts_dict['900CP1-0200']
        elif attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
            parts_dict['SP-CSPLC1'] = parts_dict['900CP1-0300'] # 900CP2-0100 has been replaced with 900CP1-0300
    except:
        pass
    return parts_dict

#CCEECOMMBR-7014
def calc_software_uoc_system(attrs,parts_dict):
    if attrs.UOC_comm_q_starter_kit == 'Yes' and attrs.UOC_comm_q_starter_kit_with_experion_license == 'No':
        parts_dict['CE-UOC-01'] = 1
        parts_dict['EP-PKS520-ESD'] = 1
        parts_dict['CF-MSD000'] = 2
    if attrs.UOC_comm_q_starter_kit == 'Yes' and attrs.UOC_comm_q_starter_kit_with_experion_license == 'Yes':
        parts_dict['CE-UOC-02'] = 1
        parts_dict['EP-PKS520-ESD'] = 1
        parts_dict['CF-MSD000'] = 2
    return parts_dict