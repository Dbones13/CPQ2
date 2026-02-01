def calc_display(parts_dict, attrs):
    #CXCPQ-21343
    parts_dict['PB-FSIE01'] = float(1) if ('PMD_Siebert' in attrs.prof_disp_devs.keys()) else float(0)
    parts_dict['PB-FESA01'] = float(1) if ('PMD_ESAVT' in attrs.prof_disp_devs.keys()) else float(0)
    parts_dict['PB-FSPP01'] = float(1) if ('PMD_PP17' in attrs.prof_disp_devs.keys()) else float(0)
    parts_dict['PB-FPRO01'] = float(1) if ('PMD_ProFace' in attrs.prof_disp_devs.keys()) else float(0)
    parts_dict['PB-FSID01'] = float(1) if ('PMD_SiebertS302' in attrs.prof_disp_devs.keys()) else float(0)
    parts_dict['PB-FSPP07'] = float(1) if ('PMD_SiemPP7' in attrs.prof_disp_devs.keys()) else float(0)
    parts_dict['PB-FSPA01'] = float(1) if ('PMD_SiemOP' in attrs.prof_disp_devs.keys()) else float(0)
        
    #CXCPQ-21340
    
    parts_dict['PB-FABIG01'] = float(1) if ('PMD_ABBINSUM' in attrs.prof_motor_start_cd_devs.keys()) else float(0)
    parts_dict['PB-FSSC01'] = float(1) if ('PMD_SiemensSc' in attrs.prof_motor_start_cd_devs.keys()) else float(0)
    parts_dict['PB-FABU02'] = float(1) if ('PMD_UMC22' in attrs.prof_motor_start_cd_devs.keys()) else float(0)
    parts_dict['PB-FSPD01'] = float(1) if ('PMD_SiemensSPD' in attrs.prof_motor_start_cd_devs.keys()) else float(0)
    parts_dict['PB-FABU03'] = float(1) if ('PMD_UMC22V2' in attrs.prof_motor_start_cd_devs.keys()) else float(0)
    parts_dict['PB-FMVC01'] = float(1) if ('PMD_Metso' in attrs.prof_motor_start_cd_devs.keys()) else float(0)
    parts_dict['PB-FNRV01'] = float(1) if ('PMD_Norgren' in attrs.prof_motor_start_cd_devs.keys()) else float(0)
    parts_dict['PB-FMNS01'] = float(1) if ('PMD_ABBMNS' in attrs.prof_motor_start_cd_devs.keys()) else float(0)
    parts_dict['PB-FSSS01'] = float(1) if ('PMD_SiemensSSS' in attrs.prof_motor_start_cd_devs.keys()) else float(0)
    parts_dict['PB-FMNS02'] = float(1) if ('PMD_MNSIS' in attrs.prof_motor_start_cd_devs.keys()) else float(0)
    
    
    #CXCPQ-21336
    
    parts_dict['PB-FABD01'] = float(1) if ('PMD_ABB' in attrs.prof_drives_devs.keys()) else float(0)
    parts_dict['PB-FSMD02'] = float(1) if ('PMD_Siemans' in attrs.prof_drives_devs.keys()) else float(0)
    parts_dict['PB-FDVD01'] = float(1) if ('PMD_Danfoss' in attrs.prof_drives_devs.keys()) else float(0)
    parts_dict['PB-FSLD01'] = float(1) if ('PMD_Lenze' in attrs.prof_drives_devs.keys()) else float(0)
    parts_dict['PB-FVCD01'] = float(1) if ('PMD_VaconNX' in attrs.prof_drives_devs.keys()) else float(0)
    parts_dict['PB-FVCX01'] = float(1) if ('PMD_VaconCX' in attrs.prof_drives_devs.keys()) else float(0)
    parts_dict['PB-FTOD01'] = float(1) if ('PMD_Toshiba' in attrs.prof_drives_devs.keys()) else float(0)
    parts_dict['PB-FCTD01'] = float(1) if ('PMD_Control' in attrs.prof_drives_devs.keys()) else float(0)
    parts_dict['PB-FEUD01'] = float(1) if ('PMD_Eurotherm' in attrs.prof_drives_devs.keys()) else float(0)
    parts_dict['PB-FSSP01'] = float(1) if ('PMD_SIEISPA' in attrs.prof_drives_devs.keys()) else float(0)
    parts_dict['PB-FPDL01'] = float(1) if ('PMD_PDL' in attrs.prof_drives_devs.keys()) else float(0)
    parts_dict['PB-FTMD01'] = float(1) if ('PMD_Telemecanique' in attrs.prof_drives_devs.keys()) else float(0)
    parts_dict['PB-FPED01'] = float(1) if ('PMD_SD700' in attrs.prof_drives_devs.keys()) else float(0)
    
    return parts_dict