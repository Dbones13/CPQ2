from math import ceil

def getCGParts(Product, parts_dict, cabinet_count, power_supply, switches):
    parts_dict['FS-MB-0002'] = {'Quantity' : cabinet_count, 'Description' : 'Power busbar max.200A 24/48/110Vdc, 60cm'}
    parts_dict['FC-TELD-0001'] = {'Quantity' : ceil(power_supply/4.0), 'Description' : 'UIO EARTH LEAKAGE DETECTOR 24VDC CC'}
    return parts_dict

def getRGParts(Product, parts_dict, cabinet_count, power_supply, switches):
    parts_dict['FS-MB-0002'] = {'Quantity' : cabinet_count, 'Description' : 'Power busbar max.200A 24/48/110Vdc, 60cm'}
    parts_dict['FC-TELD-0001'] = {'Quantity' : ceil(power_supply/4.0), 'Description' : 'UIO EARTH LEAKAGE DETECTOR 24VDC CC'}
    return parts_dict