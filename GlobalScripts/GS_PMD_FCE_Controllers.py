#import math
import System.Decimal as d

def calc_fce_Controller(parts_dict, attrs):
    
    #CXCPQ-21324
    qty = int(attrs.nrfce_profib_dp) + (2 * (int(attrs.rfce_profib_dp))) 
    parts_dict['PD-CFFCE22'] = qty

    #CXCPQ-21326
    parts_dict['PD-CFFCE31'] = attrs.nrfce_profin_pn


    #CXCPQ-21329

    parts_dict['PD-CFFCE-100'] = int(attrs.nrfce_profib_dp) + int(attrs.nrfce_profin_pn)
    parts_dict['PD-CFFCE-200'] = attrs.rfce_profib_dp
    parts_dict['PD-FCRC03'] = d.Ceiling((parts_dict['PD-CFFCE22']+parts_dict['PD-CFFCE31'])/2)


    #CXCPQ-21331
    parts_dict['PD-FCAB05'] = attrs.fce_cab_max8
    parts_dict['PD-FCAB06'] = attrs.cab_max16
    parts_dict['PD-CABE01'] = attrs.cab_1000mm
    parts_dict['PD-AHEX90']  = attrs.air_exch_90W

    #CXCPQ-25593 - BFJ

    test1 = int(attrs.nrfce_profib_dp) + int(attrs.rfce_profib_dp) + int(attrs.nrfce_profin_pn)
    test2 = int(attrs.rfce_profib_dp)

    parts_dict['PD-SWFN01'] = test1
    parts_dict['PD-SWFN02'] = test2

    return parts_dict