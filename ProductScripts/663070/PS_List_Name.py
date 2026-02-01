import Gs_Exp_Ent_Cabinet_Calcs,GS_PS_Exp_Ent_BOM
"""Loc_Clus_Nw_Grp_cnt = Product.GetContainerByName('List of Locations/Clusters/Network Groups')
row_cnt = Loc_Clus_Nw_Grp_cnt.Rows.Count
if Loc_Clus_Nw_Grp_cnt.Rows.Count>0:
    i=1
    for row in Loc_Clus_Nw_Grp_cnt.Rows:
        Network_Group_Name = row.Product.Attr('List of Locations/Clusters/ Network_Groups').GetValue()
        if str(row["List of Locations/Clusters/ Network Groups"]) != Network_Group_Name:
            row.Product.Attr('List of Locations/Clusters/ Network_Groups').AssignValue(str(row["List of Locations/Clusters/ Network Groups"]))
        row.Product.Attr('List_Of_Location_Clusters_Number').AssignValue(str(i))
        i=i+1
        row.ApplyProductChanges()"""
        #row.Calculate()
#Loc_Clus_Nw_Grp_cnt.Calculate()
'''Loc_Clus_Nw_Grp_cnt = Product.GetContainerByName('List of Locations/Clusters/Network Groups')
row_cnt = Loc_Clus_Nw_Grp_cnt.Rows.Count
for row in Loc_Clus_Nw_Grp_cnt.Rows:
    Network_Group_Name = row.Product.Attr('List of Locations/Clusters/ Network_Groups').GetValue()
    if str(row["List of Locations/Clusters/ Network Groups"]) != Network_Group_Name:
        row.Product.Attr('List of Locations/Clusters/ Network_Groups').AssignValue(str(row["List of Locations/Clusters/ Network Groups"]))
        Trace.Write(row["List of Locations/Clusters/ Network Groups"])
        row.Calculate()
Loc_Clus_Nw_Grp_cnt.Calculate()'''
U,cab=Gs_Exp_Ent_Cabinet_Calcs.Cab_qnt(Product)
Product.Attr('exp_ent_Total_U_size').AssignValue(str(U))
Product.Attr('exp_ent_cab_qnt').AssignValue(str(cab))
if Quote.GetCustomField("isR2QRequest").Content:
    door = Product.Attr('Cabinet Doors').GetValue()
    depth = Product.Attr('Cabinet Depth').GetValue()
    voltage = Product.Attr('CE_Site_Voltage').GetValue()
    Product.Attr('CE_Site_Frequency').SelectValue('60Hz')
    frequency = Product.Attr('CE_Site_Frequency').GetValue()
    if door == "Standard" and depth == "1M" and voltage == "120V" and frequency == "60Hz" and cab > 0:
        Trace.Write("getting Inside partnumber loop---->"+str(cab))
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MP-C1MCB1-100",cab)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","MP-C1MCB1-100",0)