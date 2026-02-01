def calc_other_profibus(parts_dict, attrs):
    parts_dict['PB-FMAR01'] = float(1) if ('PMD_AiRanger' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FMCE01'] = float(1) if ('PMD_Eilersen' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FRWB01'] = float(1) if ('PMD_RAUTE' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FRDC01'] = float(1) if ('PMD_HNC100' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FVEP01'] = float(1) if ('PMD_VMAC260' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FAAC01'] = float(1) if ('PMD_Auma' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FSEM01'] = float(1) if ('PMD_EM277' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FSOP01'] = float(1) if ('PMD_DIRIS' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FSSD01'] = float(1) if ('PMD_SiemensS7_315' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FVPM01'] = float(1) if ('PMD_Vogel' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FNUM01'] = float(1) if ('PMD_Numatics' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FMRV01'] = float(1) if ('PMD_Rexroth' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FGWT01'] = float(1) if ('PMD_GWT' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FRDC02'] = float(1) if ('PMD_RexrothDC' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FELC01'] = float(1) if ('PMD_ELCIS' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FKBC01'] = float(1) if ('PMD_BurnerCon' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FTEA01'] = float(1) if ('PMD_ABBTE' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FAPC01'] = float(1) if ('PMD_applicom' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FVAM01'] = float(1) if ('PMD_VAMP255' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FGEN01'] = float(1) if ('PMD_DPSlaves' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FSDR01'] = float(1) if ('PMD_SiemensDR' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FACC01'] = float(1) if ('PMD_AtlasCC' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FBEI01'] = float(1) if ('PMD_IDEACOD' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FMTS01'] = float(1) if ('PMD_MTS' in attrs.prof_other_devs.keys()) else float(0)
    parts_dict['PB-FRDS01'] = float(1) if ('PMD_RauteDos' in attrs.prof_other_devs.keys()) else float(0)
    return parts_dict