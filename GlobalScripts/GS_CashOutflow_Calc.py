#--------------------------------------------------------------
#Script Created By Saqlain Malik
#This Script is used to calculate Material,burden,buying,freight,purchasing costs with ARO's
#and populate calculations in cash outflow Quote Table
#-----------------------------------------------

def getField(col,row):
    query = "select {} from HONEYWELLP3_CASH_OUTFLOW_CONSTANTS where Attribute_Value = '{}'".format(col,row)
    field = SqlHelper.GetFirst(query)
    return field

flag = 'No'
tb = Quote.QuoteTables["Cash_Outflow"]
for row in tb.Rows:
    if row["Cost_Category_Type"] =="Honeywell P3 Material":
        flag = 'Yes'
        
Trace.Write(flag) 
lst = ['Measurex','Da Vinci','Proline & MCS','MXOpen','Web Monitoring','CD Actuator','Alcont','Printa','Web Image & Insp','TMMS','QCS Parts']
lst_len = len(lst)
# Moved this logic from Custom_field_visibility script
if Quote.GetCustomField('MPA').Content in (None, '') and Quote.GetCustomField('Milestone').Content in ['Custom'] and Quote.GetCustomField('Booking LOB').Content in ['LSS']:
	Quote.GetCustomField('do_proposed_milestones_deviate_negatively').Visible = True
else:
	Quote.GetCustomField('do_proposed_milestones_deviate_negatively').Visible = False
if flag == "Yes":
    for row in tb.Rows:
        #Trace.Write(row.Cells.Item['P3_Product_Type'].AccessLevel)
        val = str(row.Cells.Item['P3_Product_Type'].AccessLevel)
        if row["P3_Product_Type"] == '' and val == 'Editable' and row["Cost_Category_Type"] == '':
            prod_type = 'Measurex'
        elif row["P3_Product_Type"] is not None:
            prod_type=row["P3_Product_Type"]
            #Trace.Write(prod_type)
            
        for i in range(lst_len):
            if prod_type == lst[i]:
                Trace.Write("*************************")
                d_lab = getField('direct_labor',prod_type)
                d_per = d_lab.direct_labor
                mat =  getField('material',prod_type)
                m_per = mat.material
                bur =  getField('burden',prod_type)
                bur_per = bur.burden
                buy =  getField('buying',prod_type)
                buy_per = buy.buying
                fre = getField('freight',prod_type)
                f_per = fre.freight
                inv =  getField('Inventory',prod_type)
                inv_val = inv.Inventory
                d_AP = getField('days_AP',prod_type)
                d_val = d_AP.days_AP
                lead = getField('lead_time',prod_type)
                lead_val = lead.lead_time
                mfg = getField('mfg_cycle',prod_type)
                mfg_val = mfg.mfg_cycle
                lag = getField('lag',prod_type)
                lag_val = lag.lag
                pres = getField('presumed',prod_type)
                pres_val = pres.presumed
                m_aro = row["Month_ARO"]
                #Trace.Write(m_aro)
                #Trace.Write("*******************************")
                Trace.Write(float(d_per))
                row["Labor_Cost"] = -1*(row["Cost"])*(float(d_per)/100)
                row["Burden_Cost"] = -1*(row["Cost"])*(float(bur_per)/100)
                row["Material_Cost"] = -1*(row["Cost"])*(float(m_per)/100)
                row["Purchasing_Cost"] = -1*(row["Cost"])*(float(buy_per)/100)
                row["Freight_Cost"] = -1*(row["Cost"])*(float(f_per)/100)
                #Trace.Write(row["Cost"])
                ARO = round(-float(mfg_val)/30 + float(lag_val)/30 + float(m_aro))
                #Trace.Write("+++++++++++++++++++++++++++++++++")
                #Trace.Write(ARO)
                if ARO > 0:
                    row["ARO_Labor"] = row["ARO_Burden"] = ARO
                else:
                    row["ARO_Labor"] = row["ARO_Burden"] = 0

                ARO_2 = round(-round(float(inv_val)/30,0)+round(float(d_val)/30,0) + (-float(mfg_val)/30) + float(m_aro))
                if ARO_2 > 0:
                    row["ARO_Material"]= row["ARO_Freight"] = ARO_2
                else:
                    row["ARO_Material"]= row["ARO_Freight"] = 0

                pur_aro =  round(-round(float(inv_val)/30,0)-round(float(lead_val)/30,0) + (-float(mfg_val)/30) + float(m_aro))
                if pur_aro > 0:
                    row["ARO_Purchasing"] = pur_aro
                else:
                    row["ARO_Purchasing"] = 0