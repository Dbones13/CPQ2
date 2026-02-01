import math as m
from GS_MigrationLaborHoursModule import getnumberOfjumpRealease,getRowData,getRowDataIndex,checkForMPACustomer,calculateTotals,getContainer,getFloat
from GS_MigrationLaborHoursModule_2 import calculateFinalHours1,reCalAdj

def getContainer(Product,Name):
    return Product.GetContainerByName(Name)

def getRowData(Product,container,column):
    Container = getContainer(Product,container)
    for row in Container.Rows:
        return row[column]

def getRowDataIndex(Product,container,column,index):
    Container = getContainer(Product,container)
    for row in Container.Rows:
        if row.RowIndex == index:
            return row[column]

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def getTotalEngHours(Product,container):
    totalFinalHours = 0
    for row in getContainer(Product,container).Rows:
        if row["Deliverable"] == "Total":
            totalFinalHours += getFloat(row["Final_Hrs"])
    return totalFinalHours

def calculateFinalHours1(row,oldCalHrs):
    if getFloat(oldCalHrs) == getFloat(row["Calculated_Hrs"]):
        return str(round(getFloat(row["Final_Hrs"])))
    else:
        return str(round(getFloat(row["Calculated_Hrs"]) * getFloat(row["Adjustment_Productivity"])))
def reCalAdj(row,oldCalHrs):
    if getFloat(oldCalHrs) != getFloat(row["Calculated_Hrs"]):
        return "1"
    else:
        return row["Adjustment_Productivity"]
def getTraceLabourHours(Product):

    con = getContainer(Product,'Trace_Software_License_Configuration_transpose')
    conrow = con.Rows[0]
    var_2 = conrow['Trace_Software_L4_Trace_Server_Option']
    var_1 = Product.Attr('Trace_Software_Number_of_Tags').GetValue()
    var_3 = Product.Attr('Trace_Software_Is_this_a_customized_installation').GetValue()
    var_4 = Product.Attr('Trace_Software_Architecture_drawing_update').GetValue()
    

    
#calculation
#IF(var_4="YES",4,0)
    Drawing_update = 0
    Drawing_update += 4 if(var_4 == "Yes") else 0
    Trace.Write(Drawing_update)
# Installation =IF(var_1<=50000,IF(var_2="YES",32,24),IF(var_2="YES",40,32))+IF(var_3="YES",8)  
    Installation =0

    if var_1 <= 50000:

      if var_2 == "YES":

        Installation = 32

      else:

        Installation =24

    else:

      if var_2 =="Yes":

        Installation = 40

      else:

        Installation = 32
    return Drawing_update,Installation