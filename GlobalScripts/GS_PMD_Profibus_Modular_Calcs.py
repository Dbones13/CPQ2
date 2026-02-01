def calc_profibus_modular(parts_dict, attrs):
    parts_dict['PB-FGFP01'] = float(1) if ('PMD_GEFanucSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FGFP02'] = float(1) if ('PMD_GEFanucMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FGFP03'] = float(1) if ('PMD_GEFanucLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FMTL04'] = float(1) if ('PMD_MTLSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FMTL05'] = float(1) if ('PMD_MTLMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FMTL06'] = float(1) if ('PMD_MTLLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FETD01'] = float(1) if ('PMD_SiemensETSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FETD02'] = float(1) if ('PMD_SiemensETMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FETD03'] = float(1) if ('PMD_SiemensETLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FETM01'] = float(1) if ('PMD_SmETSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FETM02'] = float(1) if ('PMD_SmETMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FETM03'] = float(1) if ('PMD_SmETLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FETD07'] = float(1) if ('PMD_ET200SSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FETD08'] = float(1) if ('PMD_ET200SMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FETD09'] = float(1) if ('PMD_ET200SLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FGVX01'] = float(1) if ('PMD_VersamaxSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FGVX02'] = float(1) if ('PMD_VersamaxMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FGVX03'] = float(1) if ('PMD_VersamaxLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FBCH01'] = float(1) if ('PMD_BechoffSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FBCH02'] = float(1) if ('PMD_BechoffMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FBCH03'] = float(1) if ('PMD_BechoffLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FWAG01'] = float(1) if ('PMD_WagoSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FWAG02'] = float(1) if ('PMD_WagoMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FWAG03'] = float(1) if ('PMD_WagoLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FPIL01'] = float(1) if ('PMD_PhoenixSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FPIL02'] = float(1) if ('PMD_PhoenixMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FPIL03'] = float(1) if ('PMD_PhoenixLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FPIL04'] = float(1) if ('PMD_PhoenixILSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FPIL05'] = float(1) if ('PMD_PhoenixILMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FPIL06'] = float(1) if ('PMD_PhoenixILLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FSAC01'] = float(1) if ('PMD_SattConSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FSAC02'] = float(1) if ('PMD_SattConMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FSAC03'] = float(1) if ('PMD_SattConLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FETB01'] = float(1) if ('PMD_SiemSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FETB02'] = float(1) if ('PMD_SiemMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FETB03'] = float(1) if ('PMD_SiemLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FCEA01'] = float(1) if ('PMD_CEAGSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FCEA02'] = float(1) if ('PMD_CEAGMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FCEA03'] = float(1) if ('PMD_CEAGLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FTUR01'] = float(1) if ('PMD_TURCKSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FTUR02'] = float(1) if ('PMD_TURCKMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FTUR03'] = float(1) if ('PMD_TURCKLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FCPT01'] = float(1) if ('PMD_CerabarPT' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FMCT01'] = float(1) if ('PMD_ValmetCT' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FINL01'] = float(1) if ('PMD_PnixSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FINL02'] = float(1) if ('PMD_PnixMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FINL03'] = float(1) if ('PMD_PnixLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FABS01'] = float(1) if ('PMD_ABBS800SS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FABS02'] = float(1) if ('PMD_ABBS800MS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FABS03'] = float(1) if ('PMD_ABBS800LS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FHON01'] = float(1) if ('PMD_HoneywellSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FHON02'] = float(1) if ('PMD_HoneywellMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FHON03'] = float(1) if ('PMD_HoneywellLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FHML01'] = float(1) if ('PMD_HoneywellML' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FSET01'] = float(1) if ('PMD_SIETCSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FSET02'] = float(1) if ('PMD_SIETCMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FSET03'] = float(1) if ('PMD_SIETCLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FSHF01'] = float(1) if ('PMD_DPV1SS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FSHF02'] = float(1) if ('PMD_DPV1MS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FSHF03'] = float(1) if ('PMD_DPV1LS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FRPI01'] = float(1) if ('PMD_PepperlSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FRPI02'] = float(1) if ('PMD_PepperlMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FRPI03'] = float(1) if ('PMD_PepperlLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FSPI01'] = float(1) if ('PMD_ET200iSPSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FSPI02'] = float(1) if ('PMD_ET200iSPMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FSPI03'] = float(1) if ('PMD_ET200iSPLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FTEX01'] = float(1) if ('PMD_EXCOMSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FTEX02'] = float(1) if ('PMD_EXCOMMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FTEX03'] = float(1) if ('PMD_EXCOMLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FBK301'] = float(1) if ('PMD_BK31XXXSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FBK302'] = float(1) if ('PMD_BK31XXXMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FBK303'] = float(1) if ('PMD_BK31XXXLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FPAX01'] = float(1) if ('PMD_AXIOLINESS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FPAX02'] = float(1) if ('PMD_AXIOLINEMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FPAX03'] = float(1) if ('PMD_AXIOLINELS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FSSE01'] = float(1) if ('PMD_EXTSS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FSSE02'] = float(1) if ('PMD_EXTMS' in attrs.prof_mod_io_devs.keys()) else float(0)
    parts_dict['PB-FSSE03'] = float(1) if ('PMD_EXTLS' in attrs.prof_mod_io_devs.keys()) else float(0)
    
    return parts_dict