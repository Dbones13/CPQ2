Quote.SetGlobal('PerformanceUpload', "Yes")
con = Product.GetContainerByName('TPS_PRDContainerSys')
lst = []
if con:
    for row in con.Rows:
        prod = row.Product
        con2 = prod.GetContainerByName('TPC_PRDContainer')
        if con2:
            for row in con2.Rows:
                lst.append(str(row.UniqueIdentifier))
#Trace.Write('TPCPLSGs from TPC Product Import -- '+str(lst))
Quote.SetGlobal('TPCPLSGs', str(lst))