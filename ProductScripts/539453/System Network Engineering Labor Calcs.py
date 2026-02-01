import GS_SG_Project_size
ProjectSize,ser,stn,swt=GS_SG_Project_size.getprojectsize(Product)
Product.Attributes.GetByName('Project size message').AssignValue("")
Product.Attributes.GetByName('ErrorMessage5').AssignValue("")
Product.Attributes.GetByName('ErrorMessageDDS').AssignValue("")

Trace.Write("ProjectSize: "+str(ProjectSize))
Trace.Write("ser: "+str(ser))
Trace.Write("stn: "+str(stn))
Trace.Write("swt: "+str(swt))

def getfloat(val):
	if val:
		try:
			return float(val)
		except:
			return 0
	return 0

ser=int(getfloat(ser))
stn=int(getfloat(stn))
swt=int(getfloat(swt))

ges=Product.Attributes.GetByName("Experion_HS_Ges_Location_Labour").SelectedValue.Display
fser=Product.Attributes.GetByName('Number of Non Factory Installed Servers').GetValue()
ts=Product.Attributes.GetByName('EXP Terminal Server').GetValue()
im=Product.Attributes.GetByName('Implementation Methodology').GetValue()

tc = getfloat(Product.Attr('Experion_sys_No_of_Thin_clients').GetValue())
dc = getfloat(Product.Attr('No of Domain Controller').GetValue())
opcsr = getfloat(Product.Attr('No of OPC Server').GetValue())
emdb = getfloat(Product.Attr('No of EMDB Servers').GetValue())
nodes = getfloat(Product.Attr('No of Firewall, Routers, Simulators, TOR').GetValue())
dh = getfloat(Product.Attr('No of Data highway').GetValue())
nodes = getfloat(Product.Attr('No of Firewall, Routers, Simulators, TOR').GetValue())
fser=int(getfloat(fser))

ts=int(ts) if ts.strip() != '' else 0

ebr="No"
cont=Product.GetContainerByName("Experion_Enterprise_Cont")
for row in cont.Rows:
    y=row.Product
    try:
    	if y.Attributes.GetByName("Experion Backup & Restore (Experion Server)").SelectedValue.Display == "Yes":
        	ebr="Yes"
    except:
        pass
    try:
    	if y.Attributes.GetByName("Experion Backup & Restore (ACE)").SelectedValue.Display == "Yes":
        	ebr="Yes"
    except:
        pass
    try:
    	if y.Attributes.GetByName("Experion Backup & Restore (Simulation PC)").SelectedValue.Display == "Yes":
        	ebr="Yes"
    except:
        pass
    try:
        if y.Attributes.GetByName("Experion Backup & Restore (Mobile Terminal Server)").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass
    try:
        if y.Attributes.GetByName("Experion Backup & Restore (Flex Station ES-F)").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass
    try:
        if y.Attributes.GetByName("Experion Backup & Restore (Console Station ES-C)").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass
    try:
        if y.Attributes.GetByName("Experion Backup & Restore (Console Station Extension: ES-CE)").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass
    try:
        if y.Attributes.GetByName("Experion Backup & Restore (ACE)1").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass
    try:
        if y.Attributes.GetByName("Experion Backup & Restore (Simulation PC)1").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass
    try:
        if y.Attributes.GetByName("Experion Backup & Restore (Flex Station ES-F)1").SelectedValue.Display == "Yes":
            ebr="Yes"
    except:
        pass
Trace.Write(ebr)
#CXCPQ-38353, #CXCPQ-117240
Trace.Write(str(['check val',nodes," ",ser," ",stn," ",swt," ",fser," ",dh," ",ts]))
if ProjectSize == "Small Project":
    NONF = 16 if nodes == 0 else 40
elif ProjectSize == "Medium Project":
    NONF = nodes * 8 + swt * 1.5 + (fser + ser + stn + dh + ts) * 1
elif ProjectSize == "Large Project":
    NONF= 0
    Product.Attributes.GetByName('ErrorMessage5').AssignValue("Hours needs to be entered manually when FTE Communities > 3")

#CXCPQ-38378 #CXCPQ-117240
fat = 100
nd=ser+stn+swt+fser
nd = getfloat(nd)
if ProjectSize == "Small Project":
    Hfat = 16 if nd == 0 else 40
elif ProjectSize == "Medium Project":
    Hfat = nd * 2 * fat/100
else:
    Hfat=0
    Product.Attributes.GetByName('ErrorMessage5').AssignValue("Hours needs to be entered manually when FTE Communities > 3")

#CXCPQ-38341
tser=Product.Attributes.GetByName('Number of Server Types').GetValue()
tstn=Product.Attributes.GetByName('Number of Station Types').GetValue()
fte=Product.Attributes.GetByName('Number of FTE Communities').GetValue()
tser=int(getfloat(tser))
tstn=int(getfloat(tstn))
fte=int(getfloat(fte))

Hrsdds=10
R=0
NC=0
SWC=0
Trace.Write(str(['check val--2-->',tser,ser,stn,tc,fte]))
if ProjectSize == "Small Project":
    R = 0
    NC = 24 
    SWC = (tser * 8 + ser * 8 + stn * 4 + tc * 1)
elif ProjectSize == "Medium Project":
    R = 24  if ges == "None" else 24 * 1.15
    if im == "Non-Standard Build Estimate" and ges == "None":
        NC = 50 + (fte - 1)*24 + 16
    elif im == "Standard Build Estimate" and ges == "None":
        NC = ( 50 + (fte - 1)*24 + 16) * 0.8
    elif ges != "None":
        NC = ( 40 + (fte - 1)*24+16 ) * 0.8 * 1.1
    if im == "Non-Standard Build Estimate" and ges == "None":
        SWC = tser * 16 + ser * 8 + stn * 8 + tc * 4
    elif im == "Standard Build Estimate" and ges == "None":
        SWC = (tser * 16 + ser * 8 + stn * 8 + tc * 4) * 0.85
    elif ges != "None":
        SWC = (tser * 16 + ser * 8 + stn * 8 + tc * 4) * 0.85 * 1.1
else:
    Hrsdds=0
    Product.Attributes.GetByName('ErrorMessage5').AssignValue("Hours needs to be entered manually when FTE Communities > 3")
if Hrsdds!=0:
    Hrsdds = (R + NC + SWC )

#CXCPQ-38354
tnd=Product.Attributes.GetByName('Number of Types of Network Devices').GetValue()
tnd=int(getfloat(tnd))


if ProjectSize == "Small Project":
    Hrsstp = 8 + 8
elif ProjectSize == "Medium Project":
    if im == "Non-Standard Build Estimate" and ges == "None":
        Hrsstp = tnd * (3 + 2)
    elif im == "Standard Build Estimate" and ges == "None":
        Hrsstp = tnd * (3 + 2) * 0.7
    elif ges != "None":
        Hrsstp = tnd * (3 + 2) * 0.7 * 1.1
else:
    Hrsstp = 0
    Product.Attributes.GetByName('ErrorMessage5').AssignValue("Hours needs to be entered manually when FTE Communities > 3")

    
#CXCPQ-38326
if ProjectSize == "Small Project":
    Hrep=4
elif ProjectSize == "Medium Project":
    if im == "Non-Standard Build Estimate" and ges == "None":
        Hrep= 16
    elif im == "Standard Build Estimate" and ges == "None":
        Hrep= 16*0.8
    elif ges != "None":
        Hrep= 16*1
else:
    Hrep=0
    Product.Attributes.GetByName('ErrorMessage5').AssignValue("Hours needs to be entered manually when FTE Communities > 3")
    
#CXCPQ-38327
lfte=Product.Attributes.GetByName('Number of FTE Community Locations').GetValue()
lfte= int(getfloat(lfte))
#Hrs = SS + R  +NI + SI 
if ProjectSize == "Small Project":
    Hrfds=24    #SS = 8, R = 0, NI = 8, SI = 16
elif ProjectSize == "Medium Project":
    if im == "Non-Standard Build Estimate" and ges == "None":
        Hrfds=(32 + lfte * 24 + ser * 10 + stn * 2 + tc * 0.5) #SS = 16, R = 16, NI = lfte * 24, SI = ser*10 + stn*2 + tc*0.5 
    elif im == "Standard Build Estimate" and ges == "None":
        Hrfds=(32+ lfte * 24 * 0.75)+(ser*10 + stn*2 + tc*0.5)*0.8 #SS = 16, R = 16, NI = lfte * 24*0.75, SI = (ser*10 + stn*2 + tc*0.5)*0.8
    elif im == "Standard Build Estimate" and ges != "None":
        Hrfds= (32 + lfte * 24 * 0.75 * 1.1) + (ser * 10 + stn * 2 + tc * 0.5) * 0.8 * 1.1 #SS = 16, R = 16, NI = lfte * 24*0.75*1.1, SI = (ser*10 + stn*2 + tc*0.5)*0.8*1.1
else:
    Hrfds=0
    Product.Attributes.GetByName('ErrorMessage5').AssignValue("Hours needs to be entered manually when FTE Communities > 3")

#CXCPQ-38352
'''
"If Project Size = Small Project then 
       Hrs = 8

Else If Project Size = Medium Project  AND im = Non-Standard Build AND GES = None Then 
       Hrs = lfte * 60

else if Project Size = Medium Project  AND im = Standard Build AND GES = None Then 
       Hrs = lfte * 60 * 0.85

Else if Project Size = Medium Project  AND GES != None Then 
       Hrs = lfte * 60 * 0.85 * 1.1

Else If Project Size = Large Project then 
          Hrs = 0 and display message
          Message = ""Hours needs to be entered manually when FTE Communities > 3"
'''
if ProjectSize == "Small Project":
    Hdr=8
elif ProjectSize == "Medium Project" :
    if im == "Non-Standard Build Estimate" and ges == "None":
        Hdr= lfte * 60
    elif im == "Standard Build Estimate" and ges == "None":
        Hdr= lfte * 60 * 0.85
    elif ges != "None":
        Hdr= lfte * 60 * 0.85 * 1.1
# elif ProjectSize == "Medium Project" :
#     Hdr=0
#     Product.Attributes.GetByName('ErrorMessageDDS').AssignValue("As disaster recovery is going to be done without using Experion Backup & Restore(EBR), Please add the required hours for Disaster Recovery DDS after consultation with expert.")
elif ProjectSize == "Large Project":
    Hdr= 0
    Product.Attributes.GetByName('ErrorMessage5').AssignValue("Hours needs to be entered manually when FTE Communities > 3")
    
#CXCPQ-38320
wlan=Product.Attributes.GetByName("Is WLAN in Scope?").GetValue()
lswt=Product.Attributes.GetByName("Number of Locations with FTE Switches").GetValue()
lswt=int(getfloat(lswt))
if wlan=="Yes":
    W=80
else:
    W=0
if ges == "None" and lswt<=5:
    Hsvr=W+40
elif ges == "None" and lswt>5:
    Hsvr=W+lswt*8*1.3
elif ges != "None" and lswt<=5:
    Hsvr=(W+40)*1.15
else:
    Hsvr=(W+lswt*8*1.3)*1.15
    
#CXCPQ-38377
if ProjectSize == "Small Project":
    Hspf= 16 if nodes == 0 else 40
elif ProjectSize == "Medium Project":
    Hspf= nd * 2
elif ProjectSize == "Large Project":
    Hspf=0
    Product.Attributes.GetByName('ErrorMessage5').AssignValue("Hours needs to be entered manually when FTE Communities > 3")

#CXCPQ-38325
if im=="Non-Standard Build Estimate" and ges=="None" and lfte<=10:
    Hnar=24+16+80
elif im=="Standard Build Estimate" and lfte<=10 and ges=="None":
    Hnar=24+16+80*0.85
elif ges=="None" and lfte>10:
    Hnar=24+16+(min(lswt*8,240))
elif ges != "None" and lfte<=10:
    Hnar=(24+16+80*0.85)*1.1
elif ges != "None" and lfte>10:
    Hnar=(24+16+(min(lswt*8,240)))*1.1
else:
    Hnar=0

#CXCPQ-117240
if ProjectSize == "Small Project":
    Hsa=8
elif ProjectSize == "Medium Project":
    if im=="Non-Standard Build Estimate" and ges =="None":
        Hsa=lfte*60
    elif im=="Standard Build Estimate" and ges=="None":
        Hsa= lfte * 60 * 0.85
    elif ges!="None":
        Hsa= lfte * 60 * 0.85 * 1.1
else:
    Hsa= 0
    Product.Attributes.GetByName('ErrorMessage5').AssignValue("Hours needs to be entered manually when FTE Communities > 3")
#CXCPQ-117240
if ProjectSize == "Small Project": 
    Hsi = 60
elif ProjectSize == "Medium Project":
    Hsi = ((ser) * 10) + ((stn) * 6) + ((tc) * 2) + ((dc) * 8) + ((opcsr) * 16) + ((emdb) * 24) 
elif ProjectSize == "Large Project":
    Hsi=0
    Product.Attributes.GetByName('ErrborMessage5').AssignValue("Hours needs to be entered manually when FTE Communities > 3")
#populate=======================================
con=Product.GetContainerByName("System_Network_Engineering_Labor_Container")
for row in con.Rows:
    if row.GetColumnByName("Deliverable").Value=="SNC Site Acceptance Test & Sign off":
        row.GetColumnByName("Calculated Hrs").Value="8"
    #38353
    elif row.GetColumnByName("Deliverable").Value=="SNC Network & Server Configuration":
        row.GetColumnByName("Calculated Hrs").Value=str(NONF)
    #38378
    elif row.GetColumnByName("Deliverable").Value=="SNC Factory Acceptance Test":
        row.GetColumnByName("Calculated Hrs").Value=str(Hfat)
    #38341
    elif row.GetColumnByName("Deliverable").Value=="SNC Detail Design Specifications":
        row.GetColumnByName("Calculated Hrs").Value=str(Hrsdds)
    #38354
    elif row.GetColumnByName("Deliverable").Value=="SNC Test Procedure (FAT & SAT)":
        row.GetColumnByName("Calculated Hrs").Value=str(Hrsstp)
    #38326
    elif row.GetColumnByName("Deliverable").Value=="SNC Engineering Plan":
        row.GetColumnByName("Calculated Hrs").Value=str(Hrep)
    #38327
    elif row.GetColumnByName("Deliverable").Value=="SNC Functional Design Specification":
        row.GetColumnByName("Calculated Hrs").Value=str(Hrfds)
    #38352
    elif row.GetColumnByName("Deliverable").Value=="SNC Disaster Recovery DDS":
        row.GetColumnByName("Calculated Hrs").Value=str(Hdr)
    #38320
    elif row.GetColumnByName("Deliverable").Value=="SNC Site Visit Report":
        row.GetColumnByName("Calculated Hrs").Value=str(Hsvr)
    #38377
    elif row.GetColumnByName("Deliverable").Value=="SNC Pre-FAT":
        row.GetColumnByName("Calculated Hrs").Value=str(Hspf)
    #38325
    elif row.GetColumnByName("Deliverable").Value=="SNC Network Assessment Report":
        row.GetColumnByName("Calculated Hrs").Value=str(Hnar)
    #117240
    elif row.GetColumnByName("Deliverable").Value=="SNC System Architecture":
        row.GetColumnByName("Calculated Hrs").Value=str(Hsa)
    elif row.GetColumnByName("Deliverable").Value=="SNC System Prototype":
        row.GetColumnByName("Calculated Hrs").Value=str('0')
    elif row.GetColumnByName("Deliverable").Value=="SNC System Implementation":
        row.GetColumnByName("Calculated Hrs").Value=str(Hsi)
Product.Attributes.GetByName('Project size message').AssignValue(ProjectSize)