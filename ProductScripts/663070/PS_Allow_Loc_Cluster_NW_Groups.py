Loc_Clus_Nw_Grp_cnt = Product.GetContainerByName('List of Locations/Clusters/Network Groups')
row_cnt = Loc_Clus_Nw_Grp_cnt.Rows.Count

def disallow_loc_clus_nw(attr):
    if row_cnt > 0:
        attr_vals = Product.Attributes.GetByName(attr).Values
        for i in attr_vals:
            #Trace.Write(i.ValueCode)
            x = int(filter(str.isdigit, i.ValueCode))
            #Trace.Write("X = "+str(x))
            if x > row_cnt:
                i.Allowed = False

#CXCPQ-34882
disallow_loc_clus_nw('Orion Station Location/Cluster/Network Group')