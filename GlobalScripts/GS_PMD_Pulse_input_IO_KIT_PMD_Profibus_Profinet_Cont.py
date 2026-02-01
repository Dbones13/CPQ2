def calc_display(parts_dict, attrs):
    #CXCPQ-21349

    parts_dict['PFI-PI-2CH-PB'] = attrs.profib
    parts_dict['PFI-PI-2CH-PN'] = attrs.profin
    parts_dict['PFI-PI-PLUS2'] = attrs.add_2
    parts_dict['PFI-PI-24VDC'] = attrs.pi_card_pwr_supp
    parts_dict['PFI-PI-FO-PB'] = attrs.pfipb
    parts_dict['PFI-PI-FO-PN'] = attrs.pfipn

    return parts_dict