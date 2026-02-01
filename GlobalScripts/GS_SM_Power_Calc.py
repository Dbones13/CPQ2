from math import ceil

def get_int(val):
    if val:
        return int(val)
    return 0

def get_float(val):
    if val:
        return float(val)
    return 0


def get_attr_sum(attr, key_ls):
    res = 0
    for key in key_ls:
        try:
            res += get_int(getattr(attr, key))
        except:
            pass
    return res


def get_power_component_b(attr):
    unit_load = get_float(attr.unit_load)
    temp_nrd, temp_red = 0, 0

    temp_red += get_attr_sum(attr, [
        "sdi1_dio_rd_is", # Point 1
        "sdi1_dio_rd_nis", # Point 1
        "sdi1_dio_rd_nmr", # Point 1
        "sdi1_dio_rd_nmr_safety", # Point 1
        "sdi1_dio_rd_rly", # Point 1
        "sdi1_dio_rd_sil2_rly", # Point 1
        "sdi1_dio_rd_sil3_rly"
    ]) * 7
    temp_red += get_attr_sum(attr, [
        "sdi1_5k_resistor_dio_rd_is", # Point 1
        "sdi1_5k_resistor_dio_rd_nis", # Point 1
        "sdi1_5k_resistor_dio_rd_rly" # Point 1
    ]) * 7
    temp_red += get_attr_sum(attr, [
        "sdi1_line_mon_dio_rd_is", # Point 2
        "sdi1_line_mon_dio_rd_nis" # Point 2
    ]) * 7
    temp_red += get_attr_sum(attr, [
        "sdo1_dio_rd_is",
        "sdo1_dio_rd_nis",
        "sdo1_dio_rd_rly"
    ]) * unit_load
    temp_red += get_attr_sum(attr, [
        "sdo16_sil23_dio_rd_is", # Point 4
        "sdo16_sil23_dio_rd_nis", # Point 4
    ]) * 30
    temp_red += get_attr_sum(attr, [
        "sdo16_sil23_dio_rd_nis", # Point 5
        "sdo16_sil23_com_dio_rd_nis", #Point 6
    ]) * 40
    if temp_red:
        temp_red += 600

    temp_nrd += get_attr_sum(attr, [
        "sdi1_dio_nrd_is", # Point 1
        "sdi1_dio_nrd_nis", # Point 1
        "sdi1_dio_nrd_nmr", # Point 1
        "sdi1_dio_nrd_nmr_safety", # Point 1
        "sdi1_dio_nrd_rly", # Point 1
        "sdi1_dio_nrd_sil2_rly", # Point 1
        "sdi1_dio_nrd_sil3_rly" #Point 1
    ]) * 7
    temp_nrd += get_attr_sum(attr, [
        "sdi1_5k_resistor_dio_nrd_is", # Point 1
        "sdi1_5k_resistor_dio_nrd_nis", # Point 1
        "sdi1_5k_resistor_dio_nrd_rly", # Point 1
    ]) * 7
    temp_nrd += get_attr_sum(attr, [
        "sdi1_line_mon_dio_nrd_is", # Point 2
        "sdi1_line_mon_dio_nrd_nis" # Point 2
    ]) * 7
    temp_nrd += get_attr_sum(attr, [
        "sdo1_dio_nrd_is",
        "sdo1_dio_nrd_nis",
        "sdo1_dio_nrd_rly"
    ]) * unit_load
    temp_nrd += get_attr_sum(attr, [
        "sdo16_sil23_dio_nrd_is", # Point 4
        "sdo16_sil23_dio_nrd_nis", # Point 4
    ]) * 30
    temp_nrd += get_attr_sum(attr, [
        "sdo16_sil23_dio_nrd_nis", # Point 5
        "sdo16_sil23_com_dio_nrd_nis", #Point 6
    ]) * 40
    if temp_nrd:
        temp_nrd += 300
    return temp_red + temp_nrd