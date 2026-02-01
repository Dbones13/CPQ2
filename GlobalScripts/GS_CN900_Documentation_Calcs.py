def GS_CN900_Documentation_Calcs(attrs):
    opcnodes = int(attrs.opcnodes)
    hrs = "{0:.2f}".format(16.0 * opcnodes)
    return float(hrs)