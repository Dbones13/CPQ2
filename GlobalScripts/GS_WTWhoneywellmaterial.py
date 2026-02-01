#----------------------------------------------
lst =[]
wtw_cost = 0
cost = 0
res = SqlHelper.GetList("SELECT Distinct * FROM SAP_PLSG_LOB_Mapping where Cost_Category = 'Honeywell Material' and Sub_LOB = 'P3'")
for row in res:
    lst.append(row.SAP_PL_PLSG)

qt = Quote.QuoteTables["Product_Line_Sub_Group_Details"]
for rw in qt.Rows:
    #Trace.Write(rw["Product_Line_Sub_Group"])
    if rw["Product_Line_Sub_Group"] in lst:
        #Trace.Write('******************************************')
        wtw_cost+=rw['PLSG_WTW_Cost']
        
#Trace.Write("Cost = " + str(cost))        
        
Trace.Write(wtw_cost)      
tb = Quote.QuoteTables["Cash_Outflow"]
for row in tb.Rows:
    if row["Cost_Category_Type"] == "Honeywell P3 Material":
        #Trace.Write("***************************")
        row["Cost"] = wtw_cost