from math import ceil
def get_total_rio_cabinet_summary(cmps):
    return ceil(float(int(cmps['A']) + int(cmps['B']) + int(cmps['C']) + int(cmps['D'])) / 1000.00)