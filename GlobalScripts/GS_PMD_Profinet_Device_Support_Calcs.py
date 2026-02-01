def calc_profinet(parts_dict, attrs):
    parts_dict['PN-FGEN01'] = float(1) if ('PMD_DSBGEN' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FETD01'] = float(1) if ('PMD_ET200MPSS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FETD02'] = float(1) if ('PMD_ET200MPMS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FETD03'] = float(1) if ('PMD_ET200MPLS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FETS01'] = float(1) if ('PMD_ET200SSS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FETS02'] = float(1) if ('PMD_ET200SMS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FETS03'] = float(1) if ('PMD_ET200SLS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FETE01'] = float(1) if ('PMD_ET200SPSS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FETE02'] = float(1) if ('PMD_ET200SPMS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FETE03'] = float(1) if ('PMD_ET200SPLS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FSHF01'] = float(1) if ('PMD_ET200MSS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FSHF02'] = float(1) if ('PMD_ET200MMS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FSHF03'] = float(1) if ('PMD_ET200MLS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FTBL01'] = float(1) if ('PMD_BL20SS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FTBL02'] = float(1) if ('PMD_BL20MS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FTBL03'] = float(1) if ('PMD_BL20LS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FPAX01'] = float(1) if ('PMD_AXIOSS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FPAX02'] = float(1) if ('PMD_AXIOMS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FPAX03'] = float(1) if ('PMD_AXIOLS' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FSSC01'] = float(1) if ('PMD_ProV' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FVCD01'] = float(1) if ('PMD_VaconFC' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FCE901'] = float(1) if ('PMD_900IO' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FACD01'] = float(1) if ('PMD_ABBFC' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FPPR01'] = float(1) if ('PMD_IBPROXY' in attrs.profin_sb_devs.keys()) else float(0)
    parts_dict['PN-FPFA01'] = float(1) if ('PMD_PFCoupler' in attrs.profin_sb_devs.keys()) else float(0)
	
    return parts_dict