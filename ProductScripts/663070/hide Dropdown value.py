import GS_DropDown_Implementation
GS_DropDown_Implementation.SetDropDownDefaultvalue(Product)
Loc_Clus_Nw_Grp_cnt = Product.GetContainerByName('List of Locations/Clusters/Network Groups')
row_cnt = Loc_Clus_Nw_Grp_cnt.Rows.Count
def disallow_loc_clus_nw(attr):
    if row_cnt > 0:
        attr_vals = Product.Attributes.GetByName(attr).Values
        for i in attr_vals:
            Trace.Write(i.ValueCode)
            x = int(filter(str.isdigit, i.ValueCode))
            Trace.Write("X = "+str(x))
            #Trace.Write("row_cnt "+str(row_cnt))
            if x > row_cnt:
                #Trace.Write("row_cnt lahu "+str(i.ValueCode))
                #Trace.Write("row_cnt lahu1 "+str(attr))
                Product.DisallowAttrValues(str(attr), str(i.ValueCode))
            else:
                Product.AllowAttrValues(str(attr), str(i.ValueCode))
                Trace.Write("row_cnt lahu "+str(i.ValueCode))
                Trace.Write("row_cnt lahu1 "+str(attr))
#CXCPQ-34599
disallow_loc_clus_nw('Server LocationClusterNetwork_desk mount  server1')
disallow_loc_clus_nw('Cluster_Name_Backbone')