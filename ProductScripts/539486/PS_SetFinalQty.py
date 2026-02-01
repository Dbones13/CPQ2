def getFloat(Var):
    if Var:
        return float(Var)
    return 0

con = Product.GetContainerByName('Generic_System_Mig_Uploaded_Parts_Cont')
for row in con.Rows:
    row['Final Quantity'] = str(int(getFloat(row['Quantity'])) + int(getFloat(row['Adj Quantity'])))
    #Trace.Write(row['Final Quantity'])