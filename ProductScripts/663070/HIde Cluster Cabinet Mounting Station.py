import math as m
MIB=Product.Attributes.GetByName('MIB Configuration Required?').GetValue()
CMS=Product.Attributes.GetByName('CMS Cabinet Mounting Stations required').GetValue()
try:
    IWT=Product.Attributes.GetByName('Interface with TPS Required?').SelectedValue.Display
except:
    IWT="No"
SupervisoryNT=Product.Attributes.GetByName('Supervisory Network Type').GetValue()
Trace.Write(str(SupervisoryNT))
FlexSQ=Product.Attributes.GetByName('CMS Flex Station Qty 0_60').GetValue()
Trace.Write(str(FlexSQ))

if Product.Attributes.GetByName('CMS Cabinet Mounting Stations required').SelectedValue.Display=="Yes":
    #1
    if (MIB =="No") and (IWT=="No") and (SupervisoryNT=="FTE"):
        Product.AllowAttr('CMS Console Station Qty 0_20')
    else:
        Product.SetOptional('CMS Console Station Qty 0_20')
        Product.DisallowAttr('CMS Console Station Qty 0_20')

    #2
    if (MIB =="No") and (SupervisoryNT=="FTE"):
        Product.AllowAttr('CMS Console Station Extension Qty 0_15')
    else:
        Product.SetOptional('CMS Console Station Extension Qty 0_15')
        Product.DisallowAttr('CMS Console Station Extension Qty 0_15')

    #3
    if FlexSQ=="":
        FlexSQ=0
    if int(FlexSQ)>0:
        Product.AllowAttr('CMS Flex Station Hardware Selection')
        #Product.AllowAttr('CMS Multi Window Support Option Required?')
    else:
        Product.SetOptional('CMS Flex Station Hardware Selection')
        #Product.SetOptional('CMS Multi Window Support Option Required?')
        Product.DisallowAttr('CMS Flex Station Hardware Selection')
        #Product.DisallowAttr('CMS Multi Window Support Option Required?')
    #5
    if IWT=="Yes":
        Product.AllowAttr('CMS TPS Station Qty 0_20')
        Product.AllowAttr('CMS TPS Station Hardware Selection')
    else:
        Product.SetOptional('CMS TPS Station Qty 0_20')
        Product.SetOptional('CMS TPS Station Hardware Selection')
        Product.DisallowAttr('CMS TPS Station Qty 0_20')
        Product.DisallowAttr('CMS TPS Station Hardware Selection')
    #6
    try:
        CSQ0_20=Product.Attributes.GetByName('CMS Console Station Qty 0_20').GetValue()
        if CSQ0_20=="":
            CSQ0_20=0
    except:
        CSQ0_20=0
    Trace.Write("CSQ0_20"+ str(CSQ0_20))

    if (MIB =="No") and (SupervisoryNT=="FTE") and (int(CSQ0_20)>0):
        Product.AllowAttr('CMS Console Station Hardware Selection')
    else:
        Product.DisallowAttr('CMS Console Station Hardware Selection')
    #7
    try:
        CSEQ0_15=Product.Attributes.GetByName('CMS Console Station Extension Qty 0_15').GetValue()
        if CSEQ0_15=="":
            CSEQ0_15=0
    except:
        CSEQ0_15=0

    if (MIB =="No") and (SupervisoryNT=="FTE") and (int(CSEQ0_15)>0):
        Product.AllowAttr('CMS Console Station Extension Hardware Selection')
    else:
        Product.DisallowAttr('CMS Console Station Extension Hardware Selection')


#Visibility 1:
if (CMS=="Yes") and (MIB=="Yes") and (IWT=="No"):
    Product.AllowAttr('MIB_CMS_Validation_Message')
else:
    Product.SetOptional('MIB_CMS_Validation_Message')
    Product.DisallowAttr('MIB_CMS_Validation_Message')

#visibility 2:
try:
    FSHS=Product.Attributes.GetByName('CMS Flex Station Hardware Selection').SelectedValue.Display
except:
    FSHS="0"

try:
    CSHS=Product.Attributes.GetByName('CMS Console Station Hardware Selection').SelectedValue.Display
except:
    CSHS="0"

try:
    CSEHS=Product.Attributes.GetByName('CMS Console Station Extension Hardware Selection').SelectedValue.Display
except:
    CSEHS="0"

if (FSHS=="STN_PER_DELL_Rack_RAID1")or(CSHS=="STN_PER_DELL_Rack_RAID1")or(CSEHS=="STN_PER_DELL_Rack_RAID1"):
    Product.AllowAttr('Remote Peripheral validation message')
else:
    Product.DisallowAttr('Remote Peripheral validation message')

#CXCPQ-38241
Usize=Product.Attributes.GetByName('exp_ent_Total_U_size').GetValue()
cabq=Product.Attributes.GetByName('exp_ent_cab_qnt').GetValue()
ncq=Product.Attributes.GetByName('Network_Cabinet_Qty').GetValue()

if Usize=="":
    Usize=0
if cabq=="":
    cabq=0
if ncq=="":
    ncq=0

Usize=int(Usize)
cabq=int(cabq)
ncq=int(ncq)

value=((cabq -1) * 8) + ((40 - (Usize - ((cabq -1) * 24)))/2.0) + (8*ncq)
Trace.Write(Usize)
Trace.Write(cabq)
Trace.Write(ncq)
val=m.ceil(value)
val=int(val)
Trace.Write("val "+str(val))
value=str(val)

Product.Attributes.GetByName('Cabinet_Usize_Calc').AssignValue(value)
Loc_Clus_Nw_Grp_cnt = Product.GetContainerByName('List of Locations/Clusters/Network Groups')
if Loc_Clus_Nw_Grp_cnt.Rows.Count ==1:
    i=1
    for row in Loc_Clus_Nw_Grp_cnt.Rows:
        Network_Group_Name = row.Product.Attr('List of Locations/Clusters/ Network_Groups').GetValue()
        if str(row["List of Locations/Clusters/ Network Groups"]) != Network_Group_Name:
            row.Product.Attr('List of Locations/Clusters/ Network_Groups').AssignValue(str(row["List of Locations/Clusters/ Network Groups"]))
            row.Product.Attr('List_Of_Location_Clusters_Number').AssignValue(str(i))
            i=i+1
            row.ApplyProductChanges()