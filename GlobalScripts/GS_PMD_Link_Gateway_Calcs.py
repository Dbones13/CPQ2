def calc_link_gateway(parts_dict, attrs):
    parts_dict['PB-FDPA01'] = float(1) if ('PMD_SiemensPA' in attrs.prof_links_gates_devs.keys()) else float(0)
    parts_dict['PB-FSDP01'] = float(1) if ('PMD_SiemensDP' in attrs.prof_links_gates_devs.keys()) else float(0)
    parts_dict['PB-FSDL01'] = float(1) if ('PMD_Siemens_20E' in attrs.prof_links_gates_devs.keys()) else float(0)
    parts_dict['PB-FGDL01'] = float(1) if ('PMD_GEASi' in attrs.prof_links_gates_devs.keys()) else float(0)
    parts_dict['PB-FIAC01'] = float(1) if ('PMD_ASiDP' in attrs.prof_links_gates_devs.keys()) else float(0)
    parts_dict['PB-FCUS01'] = float(1) if ('PMD_CU9600' in attrs.prof_links_gates_devs.keys()) else float(0)
    parts_dict['PB-FCBM01'] = float(1) if ('PMD_CANCBM' in attrs.prof_links_gates_devs.keys()) else float(0)
    parts_dict['PB-FSCG01'] = float(1) if ('PMD_SiemensCPU' in attrs.prof_links_gates_devs.keys()) else float(0)
    parts_dict['PB-FTPL01'] = float(1) if ('PMD_ToshibaS3' in attrs.prof_links_gates_devs.keys()) else float(0)
    parts_dict['PB-FGPA01'] = float(1) if ('PMD_GEFanuc' in attrs.prof_links_gates_devs.keys()) else float(0)
    parts_dict['PB-FASC01'] = float(1) if ('PMD_ASiCon' in attrs.prof_links_gates_devs.keys()) else float(0)
    parts_dict['PB-FSCP01'] = float(1) if ('PMD_SiemensS7' in attrs.prof_links_gates_devs.keys()) else float(0)
    parts_dict['PB-FHMS01'] = float(1) if ('PMD_Anybus' in attrs.prof_links_gates_devs.keys()) else float(0)
    parts_dict['PB-FIMC01'] = float(1) if ('PMD_SiemensIM' in attrs.prof_links_gates_devs.keys()) else float(0)
    parts_dict['PB-FGEF01'] = float(1) if ('PMD_GE_FANUC' in attrs.prof_links_gates_devs.keys()) else float(0)
    return parts_dict