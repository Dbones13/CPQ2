#This Script is used to calculate total costs based on ARO's and totals are populated in EGAP_Cash_Outflo #w_Calculations Quote table under honeywell p3 column corresponding to each Month ARO
def getFloat(Var):
   if Var:
       return float(Var)
   return 0
flag = 0
check = 0
if Quote.GetCustomField('Quote Type').Content == "Projects":
    tbl = Quote.QuoteTables["Cash_Outflow"]
    tbl2 = Quote.QuoteTables["EGAP_Cash_Outflow_Calculations"]
    for row in tbl.Rows:
        if row["Cost_Category_Type"] == "Honeywell P3 Material":
            check=1
    prj_dur = Quote.GetCustomField('EGAP_Milestone_Project_Duration_Months').Content
    if prj_dur is not None:
        flag = 1
        var = getFloat(prj_dur) + 1
if flag == 1 and check == 1:
    Trace.Write("*************************")
    for i in range(0,int(var)):
        aro = 0
        for row in tbl.Rows:
            if row["P3_Product_Type"]:
                if row["ARO_Labor"] == i:
                    aro += row["Labor_Cost"]    
                if row["ARO_Burden"] == i:
                    aro+= row["Burden_Cost"]
                if row["ARO_Material"] == i:
                    aro+= row["Material_Cost"]
                if row["ARO_Purchasing"] == i:
                    aro+= row["Purchasing_Cost"]    
                if row["ARO_Freight"] == i:
                    aro+= row["Freight_Cost"]   
                for rw in tbl2.Rows:
                    if rw["Cash_Outflow_Month_ARO"] == i:
                        rw["Honeywell_P3_Material"] = aro