def getCalcValue(a):
    if a == "":
        a = 0.0
    return float(a)
def getDelCalHours(level1_prod, level2_cont, Deliverable_colname, Deliverable, CalculatedHrs_colname):
    level0_cont = 'CE_SystemGroup_Cont'
    level1_cont = 'CE_System_Cont'
    selected_prds = Product.GetContainerByName(level0_cont)
    x = 0.0
    for r1 in selected_prds.Rows:
        cp = r1.Product.GetContainerByName(level1_cont)
        for r2 in cp.Rows:
            if r2['Product Name'] == level1_prod:
                cpp=r2.Product.GetContainerByName(level2_cont)
                for r3 in cpp.Rows:
                    if Deliverable in r3[Deliverable_colname]:
                        x = getCalcValue(r3[CalculatedHrs_colname])
    return x
hr = 0
hrs = 0
tableLabor = SqlHelper.GetList('select Product,Container,Deliverable,Calculated_hrs from LABOR_DDS_CALCULATION_HRS')
for row in tableLabor:
    level1_prod= row.Product
    level2_cont = row.Container
    Deliverable_colname = 'Deliverable'
    Deliverable = row.Deliverable
    CalculatedHrs_colname= 'Final Hrs'
    hrs = hr + getDelCalHours(level1_prod,level2_cont,Deliverable_colname,Deliverable,CalculatedHrs_colname)
    hr = hrs if hrs !='' else 0
    Product.Attr('Total_DDS_hrs').AssignValue(str(hr))
Trace.Write(hr)