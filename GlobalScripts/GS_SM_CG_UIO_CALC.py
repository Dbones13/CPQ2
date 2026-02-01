from math import ceil
import GS_SM_SUMUIONPF_Calc
#import GS_SM_SUMUIORPF_Calc

def get_int(val):
    if val:
        return int(val)
    return 0

def get_float(val):
    if val:
        return float(val)
    return 0

def try_get_attr(attr, key, default):
    try:
        return getattr(attr, key)
    except AttributeError, e:
        return default

def get_sum_non_red_is_io(attrs):
    SUMUIONIS = 0
    SUMUIONIS += get_int(attrs.sai1_uio_nrd_is)
    SUMUIONIS += get_int(attrs.sai1_fire2_wire_uio_nrd_is)
    SUMUIONIS += get_int(try_get_attr(attrs, "sai1_fire34_wire_uio_nrd_is", 0))
    SUMUIONIS += get_int(try_get_attr(attrs, "sai1_fire34_wire_sink_uio_nrd_is", 0))
    SUMUIONIS += get_int(attrs.sai1_gas_uio_nrd_is)
    SUMUIONIS += get_int(attrs.sao1_uio_nrd_is)
    SUMUIONIS += get_int(attrs.sdi1_uio_nrd_is)
    SUMUIONIS += get_int(try_get_attr(attrs, "sdi1_line_mon_uio_nrd_is", 0))
    SUMUIONIS += get_int(attrs.sdo1_uio_nrd_is)
    SUMUIONIS += ceil(get_float(try_get_attr(attrs, "sdo7_line_mon_uio_nrd_is", 0)) / 7)
    SUMUIONIS *= get_float(1.00 + get_float(attrs.percent_spare_io)/100.00)
    return SUMUIONIS

def get_sum_red_io(attrs, sumuiorpf):
    if attrs.universal_iota != "RUSIO":
        return 0
    SUMUIOR = 0
    SUMUIOR += get_int(attrs.sai1_uio_rd_nis)
    SUMUIOR += get_int(attrs.sai1_fire2_wire_uio_rd_nis)
    SUMUIOR += get_int(try_get_attr(attrs, "sai1_fire34_wire_uio_rd_nis", 0))
    SUMUIOR += get_int(try_get_attr(attrs, "sai1_fire34_wire_sink_uio_rd_nis", 0))
    SUMUIOR += get_int(attrs.sai1_gas_uio_rd_nis)
    SUMUIOR += get_int(attrs.sao1_uio_rd_nis)
    SUMUIOR += get_int(attrs.sdo1_uio_rd_nis)
    SUMUIOR += get_int(try_get_attr(attrs, "sdo2_1a_uio_rd_nis", 0))
    SUMUIOR += get_int(try_get_attr(attrs, "sdo4_2a_uio_rd_nis", 0))
    SUMUIOR += 16 * ceil(get_int(attrs.sdo7_line_mon_uio_rd_nis)/7.0)
    SUMUIOR += get_int(attrs.sdo16_sil23_uio_rd_nis)
    SUMUIOR += get_int(attrs.sdo12_sil23_com_uio_rd_nis)
    SUMUIOR += get_int(attrs.sdi1_uio_rd_nis)
    SUMUIOR += get_int(try_get_attr(attrs, "sdi1_line_mon_uio_rd_nis", 0))
    SUMUIOR += get_int(try_get_attr(attrs, "sdi1_5k_resistor_uio_rd_nis", 0))
    SUMUIOR += get_int(try_get_attr(attrs, "sdo1_uio_rd_rly", 0))
    SUMUIOR += get_int(try_get_attr(attrs, "sdi1_uio_rd_rly", 0))
    SUMUIOR += get_int(try_get_attr(attrs, "sdo1_uio_rd_sil2_rly", 0))
    SUMUIOR += get_int(try_get_attr(attrs, "sdo1_uio_rd_sil3_rly", 0))
    SUMUIOR += get_int(try_get_attr(attrs, "sdi1_uio_rd_sil2_rly", 0))
    SUMUIOR += get_int(try_get_attr(attrs, "sdi1_uio_rd_sil3_rly", 0))
    SUMUIOR += get_int(try_get_attr(attrs, "sdi1_uio_rd_nmr", 0))
    SUMUIOR += get_int(try_get_attr(attrs, "sdi1_uio_rd_nmr_safety", 0))
    SUMUIOR += 16 * ceil(sumuiorpf / 16.0)
    SUMUIOR = SUMUIOR * (1 + get_float(attrs.percent_spare_io)/100.00)
    return SUMUIOR

# CXCPQ-31791
def get_sum_marsh_uio(attrs):
    if attrs.universal_iota == "RUSIO" or attrs.marshalling_option != "Hardware Marshalling with Other":
        return 0
    if attrs.universal_iota=="PUIO" and attrs.marshalling_option=="Hardware Marshalling with Other":
        SUMMARSHUIO = 0
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sai1_uio_rd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sai1_fire2_wire_uio_rd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sai1_fire34_wire_uio_rd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sai1_gas_uio_rd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sao1_uio_rd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sdi1_uio_rd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sdi1_line_mon_uio_rd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sdo1_uio_rd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sdo2_1a_uio_rd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sdo4_2a_uio_rd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sai1_uio_nrd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sai1_fire2_wire_uio_nrd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sai1_fire34_wire_uio_nrd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sai1_gas_uio_nrd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sao1_uio_nrd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sdi1_uio_nrd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sdi1_line_mon_uio_nrd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sdo1_uio_nrd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sdo2_1a_uio_nrd_nis", 0))
        SUMMARSHUIO += get_int(try_get_attr(attrs, "sdo4_2a_uio_nrd_nis", 0))
        SUMMARSHUIO = SUMMARSHUIO * (1 + get_float(attrs.percent_spare_io)/100.00)
        return SUMMARSHUIO

#CXCPQ-30834
def get_sum_redpf(attrs):
    SUMUIORPF = 0
    cal = get_int(attrs.sil2_red) + get_int(attrs.sil3_red) + get_int(attrs.currentmA_red) + get_int(attrs.currentmAPF_red) + get_int(attrs.sil3pf_red)
    SUMUIORPF = cal * float(1.00 + (get_float(attrs.percent_spare_io)/100.00))
    return SUMUIORPF

# CXCPQ-30835
def get_sum_red_is_io(attrs):
    SUMUIORIS = 0
    cal = get_int(attrs.current_uio_RD_IS) + get_int(attrs.fire2_RD_IS) + get_int(attrs.fire3and4_RD_IS) + get_int(attrs.fire3and4_sink_RD_IS) + get_int(attrs.gas_RD_IS) + get_int(attrs.type_uio_RD_IS) + get_int(attrs.uio_di_RD_IS) + get_int(attrs.line_mon_uio_di_RD_IS) + get_int(attrs.uio_do_RD_IS) + 16.0 * ceil(attrs.line_mon_uio_do_RD_IS/7.0)
    SUMUIORIS = cal * (1.00 + get_float(attrs.percent_spare_io)/100.00)
    return SUMUIORIS


#CXCPQ-30847
'''def get_sum_non_red_is_dio(attrs):
    SUMDIONIS = 0
    cal = (attrs.dio_di_24vdc_NRD_IS)+(attrs.dio_di_24vdc_Lin_Mon_NRD_IS)+(attrs.dao_24vdc_500mA_NRD_IS)
    SUMDIONIS = cal * float(1.00 + (get_float(attrs.percent_spare_io)/100.00))
    return SUMDIONIS'''

#CXCPQ-30869
def get_sum_red_nis_io(attrs):
    SUMDIOR = 0
    cal = get_int(attrs.dio_di_24vdc_rnis)+get_int(attrs.dio_di_24vdc_Lin_Mon_rnis)+get_int(attrs.vdc24_with_5k_resistor_dio_di_rnis)+get_int(attrs.dio_24vdc_500mA_rnis)+get_int(attrs.sil_2_3_dio_rnis)+get_int(attrs.sil_2_3_com_dio_rnis)+get_int(attrs.dio_di_24vdc_rdrly)+get_int(attrs.dio_24vdc_500mA_rdrly)+get_int(attrs.dio_di_24vdc_r3rly)+get_int(attrs.dio_24vdc_500mA_r3rly)+get_int(attrs.dio_24vdc_500mA_r2rly)+get_int(attrs.dio_di_24vdc_rnmr)+get_int(attrs.dio_di_24vdc_rnmrs)
    SUMDIOR = cal * float(1.00 + (get_float(attrs.percent_spare_io)/100.00))
    return SUMDIOR

'''#CXCPQ-30864
def get_SUMUION(attrs,SUMUIONPF):
    SUMUION = 0
    cal = get_int(attrs.sai1_uio_nrd_nis)+ get_int(attrs.sai1_fire2_wire_uio_nrd_nis)+ get_int(attrs.sai1_fire34_wire_uio_nrd_nis)+ get_int(attrs.sai1_fire34_wire_sink_uio_nrd_nis)+ get_int(attrs.sai1_gas_uio_nrd_nis)+ get_int(attrs.sao1_uio_nrd_nis)+ get_int(attrs.sdi1_uio_nrd_nis)+ get_int(attrs.sdi1_line_mon_uio_nrd_nis)+ get_int(attrs.sdi1_5k_resistor_uio_nrd_nis)+ get_int(attrs.sdo1_uio_nrd_nis)+ get_int(attrs.sdo16_sil23_uio_nrd_nis)+ get_int(attrs.sdo12_sil23_com_uio_nrd_nis)+ get_int(attrs.sdi1_uio_nrd_rly)+ get_int(attrs.sdo1_uio_nrd_rly)+ get_int(attrs.sdo1_uio_nrd_sil2_rly)+ get_int(attrs.sdi1_uio_nrd_sil3_rly)+ get_int(attrs.sdo1_uio_nrd_sil3_rly)+ get_int(attrs.sdi1_uio_nrd_nmr)+ get_int(attrs.sdi1_uio_nrd_nmr_safety)+ (16.0*(get_int(attrs.sdo7_line_mon_uio_nrd_nis)/7.0))+ (16.0 * (get_int(SUMUIONPF/16)))
    SUMUION = cal * float(1.00 + (get_float(attrs.percent_spare_io)/100.00))
    return SUMUION'''

#30862


SUMUIORPF = 0
def get_sum_NonRed_nis_io(attrs,SUMUIORPF):
    SUMUIOR = 0
    cal = get_float(attrs.current_uio_RD_NIS)+get_float(attrs.fire2_RD_NIS) +get_float(attrs.fire3and4_RD_NIS)+get_float(attrs.fire3and4_sink_RD_NIS)+get_float(attrs.gas_RD_NIS)+get_float(attrs.type_uio_RD_NIS)+ get_float(attrs.uio_do_RD_NIS)+get_float(attrs.uio_di_RD_NIS)+get_float(attrs.line_mon_uio_di_RD_NIS)+get_float(attrs.with_5k_resistor_uio_di_RD_NIS)+get_float(attrs.uio_di_rly)+get_float(attrs.uio_do_rly)+get_float(attrs.uio_do_sil2_rly)+get_float(attrs.uio_di_sil3_rly)+get_float(attrs.uio_do_sil3_rly)+get_float(attrs.uio_di_nmr)+get_float(attrs.uio_di_nmr_safety)+16*(m.ceil(get_float(attrs.line_mon_uio_do_RD_NIS)/7.00)+get_int(attrs.sil_2_3_uio_do_RD_NIS)+get_int(attrs.sil_2_3_com_uio_do_RD_NIS))+16*(m.ceil(get_float(SUMUIORPF)/16.00))
    SUMUIOR =cal * float(1.00 + (get_float(attrs.percent_spare_io)/100.00))
    return (m.ceil(SUMUIOR))