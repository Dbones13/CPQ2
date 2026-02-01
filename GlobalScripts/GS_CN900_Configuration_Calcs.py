def GS_CN900_Configuration_Calcs(attrs):
    opcnodes = int(attrs.opcnodes)
    points = int(attrs.points)
    hrs = "{0:.2f}".format((8.0 * opcnodes) + (0.1 * points))
    return float(hrs)