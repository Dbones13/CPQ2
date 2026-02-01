import math
def getattrvalue(a):
    if a == "":
        a = 0
    return float(a)

def isFloat(val):
    if val is not None and val != '':
        try:
            float(val)
            return True
        except:
            return False
    return False
Count=nscab=oc=Plan=Design=0
sim_cx=0
tps = 0
mdb = 0
ld = 0
stn = 0
svr = 0
cab_flex = 0
cab_con = 0
cab_con_ext = 0
cab_tps = 0
desk_flex = 0
desk_con = 0
desk_con_ext = 0
desk_tps = 0
orion_flex = 0
orion_con = 0
orion_con_ext = 0
orion_tps = 0
add_station = 0
ace_ser_tower = 0
ace_ser_rack = 0
acet_ser_tower = 0
acet_ser_rack = 0
exp_ser_tower = 0
exp_ser_rack = 0
mob_server = 0
add_servers = 0
server_red =nscab=oc=0

Ct=int(TagParserProduct.ParseString('[IF]([GT](<*XValue(../EX_Labor_CT_Qty)*>,0)){<*XValue(../EX_Labor_CT_Qty)*>}{0}[ENDIF]'))
It=int(TagParserProduct.ParseString('[IF]([GT](<*XValue(../EX_Labor_IT_Qty)*>,0)){<*XValue(../EX_Labor_IT_Qty)*>}{0}[ENDIF]'))
Urp=1 if TagParserProduct.ParseString('<*XValue(../Labor_Unreleased_Product)*>')=="Yes" else 0
uio=float(TagParserProduct.ParseString('[IF]([GT](<*XValue(../C300_Exp_Labor_Uni_qntCG)*>,0)){1}{0}[ENDIF]'))
MS=float(TagParserProduct.ParseString('[IF]([GT](<*XValue(../C300_Exp_Labor_Uni_qntmarsh)*>,0)){0.9}{1}[ENDIF]'))
auxcab = float(Product.Attr("Auxiliary Cabinet Count").GetValue())
hc = float(Product.Attr("Number of Console Sections with Hardwired IO").GetValue())
com=getattrvalue(Product.Attr("Number of Physical Communication Links").GetValue())
spi=1 if Product.Attr("Use of SPI (Intools) in Scope?").GetValue()=="Yes" else 0
ScopeN=1 if Product.Attr("New_Expansion").GetValue()=="Expansion" else 0
if Product.Attr("Labor_Marshalling_Database").GetValue() == "Yes":
    mdb = 1
if Product.Attr("Labor_Loop_Drawings").GetValue() == "Yes":
    ld = 1

if Product.Attr("New_Expansion").GetValue() == "Expansion":
    exp_groups = Product.GetContainerByName('Experion_Enterprise_Cont').Rows
    for exp in exp_groups:
        exp_product = exp.Product
        x = exp_product.Attr('Interface with TPS Required?').GetValue()
        if x == "Yes":
            tps = 1
            break
else:
    tps = 0
    
exp_groups = Product.GetContainerByName('Experion_Enterprise_Cont').Rows
for row in exp_groups:
    try:
        nscab +=getattrvalue(row['Network_Cabinet_Qty'])
        oc +=getattrvalue(row['Number of Operator Console Sections'])
    except:
        nscab = nscab
        oc = orion

Count=exp_groups.Count if exp_groups.Count else 0
for exp in exp_groups:
    exp_product = exp.Product
    try:
        cab_flex = cab_flex + getattrvalue(exp_product.Attr('CMS Flex Station Qty 0_60').GetValue()) if exp_product.Attr('CMS Node Supplier').GetValue()=="Honeywell" else 0
    except:
        cab_flex = cab_flex
    try:
        cab_con  = cab_con + getattrvalue(exp_product.Attr('CMS Console Station Qty 0_20').GetValue()) if exp_product.Attr('CMS Node Supplier').GetValue()=="Honeywell" else 0
    except:
        cab_con = cab_con
    try:
        cab_con_ext  = cab_con_ext + getattrvalue(exp_product.Attr('CMS Console Station Extension Qty 0_15').GetValue()) if exp_product.Attr('CMS Node Supplier').GetValue()=="Honeywell" else 0
    except:
        cab_con_ext = cab_con_ext
    try:
        cab_tps = cab_tps + getattrvalue(exp_product.Attr('CMS TPS Station Qty 0_20').GetValue()) if exp_product.Attr('CMS Node Supplier').GetValue()=="Honeywell" else 0
    except:
        cab_tps = cab_tps
    try:
        desk_flex = desk_flex + getattrvalue(exp_product.Attr('DMS Flex Station Qty 0_60').GetValue()) if exp_product.Attr('DMS Node Supplier').GetValue()=="Honeywell" else 0
    except:
        desk_flex = desk_flex
    try:
        desk_con = desk_con + getattrvalue(exp_product.Attr('DMS Console Station Qty 0_20').GetValue()) if exp_product.Attr('DMS Node Supplier').GetValue()=="Honeywell" else 0
    except:
        desk_con = desk_con
    try:
        desk_con_ext = desk_con_ext + getattrvalue(exp_product.Attr('DMS Console Station Extension Qty 0_15').GetValue()) if exp_product.Attr('DMS Node Supplier').GetValue()=="Honeywell" else 0
    except:
        desk_con_ext = desk_con_ext
    try:
        desk_tps = desk_tps + getattrvalue(exp_product.Attr('DMS TPS Station Qty 0_20').GetValue()) if exp_product.Attr('DMS Node Supplier').GetValue()=="Honeywell" else 0
    except:
        desk_tps = desk_tps
    try:
        orion_flex = orion_flex + getattrvalue(exp_product.Attr('Flex Station Qty (0-60)').GetValue()) if exp_product.Attr('Node Supplier').GetValue()=="Honeywell" else 0
    except:
        orion_flex = orion_flex
    try:
        orion_con = orion_con + getattrvalue(exp_product.Attr('Console Station Qty (0-20)').GetValue()) if exp_product.Attr('Node Supplier').GetValue()=="Honeywell" else 0
    except:
        orion_con = orion_con
    try:
        orion_con_ext = orion_con_ext + getattrvalue(exp_product.Attr('Console Station Extension Qty  (0-15)').GetValue()) if exp_product.Attr('Node Supplier').GetValue()=="Honeywell" else 0
    except:
        orion_con_ext = orion_con_ext
    try:
        orion_tps = orion_tps + getattrvalue(exp_product.Attr('TPS Station Qty (0-20)').GetValue()) if exp_product.Attr('Node Supplier').GetValue()=="Honeywell" else 0
    except:
        orion_tps = orion_tps
    try:
        add_station = add_station + getattrvalue(exp_product.Attr('Additional Stations').GetValue()) if exp_product.Attr('Node Supplier Server').GetValue()=="Honeywell" else 0
    except:
        add_station = add_station
    try:
        ace_ser_tower = ace_ser_tower + getattrvalue(exp_product.Attr('ACE Node Tower Mount Desk').GetValue()) if exp_product.Attr('Node Supplier_ACE1').GetValue()=="Honeywell" else 0
    except:
        ace_ser_tower = ace_ser_tower
    try:
        ace_ser_rack = ace_ser_rack + getattrvalue(exp_product.Attr('ACE Node Rack Mount Cabinet').GetValue()) if exp_product.Attr('Node Supplier_ACE1').GetValue()=="Honeywell" else 0
    except:
        ace_ser_rack = ace_ser_rack
    try:
        acet_ser_tower = acet_ser_tower + getattrvalue(exp_product.Attr('ACE_T_Node _Tower_Mount_Desk').GetValue()) if exp_product.Attr('Node Supplier_ACE1').GetValue()=="Honeywell" else 0
    except:
        acet_ser_tower = acet_ser_tower
    try:
        acet_ser_rack = acet_ser_rack + getattrvalue(exp_product.Attr('ACE_T_Node _Rack_Mount_Cabinet').GetValue()) if exp_product.Attr('Node Supplier_ACE1').GetValue()=="Honeywell" else 0
    except:
        acet_ser_rack = acet_ser_rack
    try:
        exp_ser_tower = exp_ser_tower + getattrvalue(exp_product.Attr('Experion APP Node - Tower Mount').GetValue()) if exp_product.Attr('Node Supplier_EAPP').GetValue()=="Honeywell" else 0
    except:
        exp_ser_tower = exp_ser_tower
    try:
        exp_ser_rack = exp_ser_rack + getattrvalue(exp_product.Attr('Experion APP Node - Rack Mount').GetValue()) if exp_product.Attr('Node Supplier_EAPP').GetValue()=="Honeywell" else 0
    except:
        exp_ser_rack = exp_ser_rack
    try:
        mob_server = mob_server + getattrvalue(exp_product.Attr('Mobile Server Nodes (0-1)').GetValue()) if exp_product.Attr('Node Supplier Server1').GetValue()=="Honeywell" else 0
    except:
        mob_server = mob_server
    try:
        add_servers = add_servers + getattrvalue(exp_product.Attr('Additional Servers').GetValue()) if exp_product.Attr('Node Supplier Server').GetValue()=="Honeywell" else 0
    except:
        add_servers = add_servers
    try:
        sim_cx = (getattrvalue(exp_product.Attr('SIM-ACE Licenses (0-7)').GetValue())+getattrvalue(exp_product.Attr('Sim-Cx00 PC Licenses (0-20)').GetValue())+getattrvalue(exp_product.Attr('SIM-FFD Licenses (0-125)').GetValue()) if exp_product.Attr('Node Supplier (Sim PC)').GetValue()=="Honeywell" else 0)
    except:
        sim_cx = sim_cx
    try:
        red = Count
        if red:
            server_red = server_red + 1
        if red and sim_cx>0:
            server_red = server_red + 1
    except:
        server_red = server_red

stn = float(cab_flex) + float(cab_con) + float(cab_con_ext) + float(cab_tps) + float(desk_flex) + float(desk_con) + float(desk_con_ext) + float(desk_tps) + float(orion_flex) + float(orion_con) + float(orion_con_ext) + float(orion_tps) + float(add_station)
svr = float(ace_ser_tower) + float(ace_ser_rack) + float(acet_ser_tower) + float(acet_ser_rack) + float(mob_server) + float(add_servers) + float(server_red)

Trace.Write(str(stn))
Trace.Write(str(svr))

Hrs1 = 0.76*(6+6*(nscab+oc+auxcab)+16*tps)
Product.Attr("SHE Site Installation").AssignValue(str(Hrs1))

Integration = 0.82*(2 + 6 * ( nscab + oc+ auxcab) + 8 * tps)
IntTest = (1-uio*0.1)*0.12*(24*nscab+(10+8*oc)+80*hc*0.5+50*auxcab)
Trace.Write("uio {} nscab {} oc {} hc {} auxcab {} tps {}".format(uio,nscab,oc,hc,auxcab,tps))
Hrs2 = Integration + IntTest
Product.Attr("SHE System Integration & Internal Test").AssignValue(str(Hrs2))

BOM_Hrs =(1-uio*0.15)*1.9*(0.1*(nscab+oc+hc+auxcab) +2*(nscab+oc+hc+auxcab)/(nscab+oc+hc+auxcab+1)+0.25*svr+0.25*stn+2*Ct)
IPR_Hrs = (1-uio*0.05)*(0.5*oc+2*oc/(oc+1)+0.25*svr + 0.25*stn+2*Ct+4*Urp)*1.05
OPR_Hrs = (nscab+3*nscab/(nscab+1)+hc*4+auxcab*4+ 0.25 * svr + 0.25*stn)*0.8
Hrs3 = BOM_Hrs + IPR_Hrs + OPR_Hrs
Trace.Write(Hrs3)
Product.Attr("SHE Procure Materials & Services").AssignValue(str(Hrs3))

CD_Hrs = (1-uio*0.2)*0.7*((0.25*hc*40)*mdb)*1.05*MS
LD_Hrs = (1-uio*0.35)*0.38*ld*((0.25*hc*40)*mdb)*1.05
CS_Hrs = (1-uio*0.15)*1.6*(0.5*nscab+1.5*hc+auxcab+0.08 * svr +  0.08*stn)
Design= (1-uio*0.25)*((1.2*MS*(48+2*com+hc*4/(hc+1)+0.5+math.pow(Ct,2)+4*Urp+8*spi))+20*ScopeN)*0.66
if Product.Attr("Implementation Methodology").GetValue() == "Non-Standard Build Estimate":
    CS_Hrs = CS_Hrs
    Design=Design
else:
    CS_Hrs = CS_Hrs * 0.9
    Design=Design*0.7
Hrs4 = CS_Hrs + CD_Hrs + LD_Hrs
Plan= (0.19*(1.1*(48+2*com+hc*(4/(hc+1)+0.5)+math.pow(Ct,2)+4*Urp+8*spi)))+10*ScopeN

Product.Attr("SHE Hardware Implementation").AssignValue(str(Hrs4))
Product.Attr('Number of Operator Console Sections').AssignValue(str(oc))
Product.Attr('SHE Engineering Plan').AssignValue(str(Plan))
Product.Attr('SHE Functional Design Specification').AssignValue(str(Design))
Product.Attr('Network and Server Cabinet Count').AssignValue(str(nscab))
scope = Product.Attr('CE_Scope_Choices').GetValue()
if Product.Attr('isProductLoaded').GetValue() == 'True' and scope == 'HW/SW + LABOR':
    Product.ApplyRules()
    tableLabor = SqlHelper.GetList('Select Deliverable,Calculated_Hrs from HARDWARE_ENGINEERING_DELIVERABLE')
    laborCont = Product.GetContainerByName('Hardware Engineering Labour Container')
    calc_dict = {}
    for x in tableLabor:
        calc_dict[x.Deliverable] = x.Calculated_Hrs
    for row in laborCont.Rows:
        deliverable = row.GetColumnByName("Deliverable").Value
        if deliverable in calc_dict.keys() and not isFloat(calc_dict[deliverable]):
            calc_name = calc_dict[deliverable]
            try:
                row.GetColumnByName("Calculated Hrs").Value = Product.Attr(calc_name).GetValue()
            except Exception,e:
                pass
    laborCont.Calculate()