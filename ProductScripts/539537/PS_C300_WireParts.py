import GS_PS_Exp_Ent_BOM
import GS_Get_Set_AtvQty

#Product.ExecuteRulesOnce = True
comp24=0
comp36=0
comp48=0
comp60=0
comp84=0
comp2=0
comp5=0
comp10=0
comp20=0

ecomp24=0
ecomp36=0
ecomp48=0
ecomp60=0
ecomp84=0
ecomp2=0
ecomp5=0
ecomp10=0
ecomp20=0

fcomp24=0
fcomp36=0
fcomp48=0
fcomp60=0
fcomp84=0
fcomp2=0
fcomp5=0
fcomp10=0
fcomp20=0

CC_IP0101=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-IP0101')
CC_PEIM01=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-PEIM01')
CC_PFB402=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-PFB402')
CC_PFB802=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-PFB801')

Trace.Write("qnt CC_IP0101: "+str(CC_IP0101))
Trace.Write("qnt CC_PEIM01: "+str(CC_PEIM01))
Trace.Write("qnt CC_PFB402: "+str(CC_PFB402))
Trace.Write("qnt CC_PFB802: "+str(CC_PFB802))

Trace.Write("qnt"+str((comp84*int(CC_IP0101))+(ecomp84*int(CC_PEIM01))+(fcomp84*(int(CC_PFB402)+int(CC_PFB802)))))

PGML=Product.Attributes.GetByName("SerC_Control_Firewall_to_PGM_Cable_Length").GetValue()
Trace.Write("PGML :"+str(PGML))
if PGML=="24 Inch":
    comp24=comp24+1
elif PGML=="36 Inch":
    comp36=comp36+1
elif PGML=="48  Inch":
    comp48=comp48+1
elif PGML=="60  Inch":
    comp60=comp60+1
elif PGML=="84  Inch":
    comp84=comp84+1
elif PGML=="2m":
    comp2=comp2+1
elif PGML=="5m":
    comp5=comp5+1
elif PGML=="10m":
    comp10=comp10+1
elif PGML=="20m":
    comp20=comp20+1

EIML=Product.Attributes.GetByName("SerC_Control Firewall to EIM Cable Length").GetValue()
Trace.Write("EIML :"+str(EIML))
if EIML=="24 Inch":
    ecomp24=ecomp24+1
elif EIML=="36 Inch":
    ecomp36=ecomp36+1
elif EIML=="48  Inch":
    ecomp48=ecomp48+1
elif EIML=="60  Inch":
    ecomp60=ecomp60+1
elif EIML=="84  Inch":
    ecomp84=ecomp84+1
elif EIML=="2m":
    ecomp2=ecomp2+1
elif EIML=="5m":
    ecomp5=ecomp5+1
elif EIML=="10m":
    ecomp10=ecomp10+1
elif EIML=="20m":
    ecomp20=ecomp20+1

try:
    FIML=Product.Attributes.GetByName("FIM_Ctrl_Firewall_to_FIM_Cable_Len").GetValue()
except:
    FIML="0"

if FIML=="24 Inch":
    fcomp24=fcomp24+1
elif FIML=="36 Inch":
    fcomp36=fcomp36+1
elif FIML=="48 Inch":
    fcomp48=fcomp48+1
elif FIML=="60 Inch":
    fcomp60=fcomp60+1
elif FIML=="84 Inch":
    fcomp84=fcomp84+1
elif FIML=="2m":
    fcomp2=fcomp2+1
elif FIML=="5m":
    fcomp5=fcomp5+1
elif FIML=="10m":
    fcomp10=fcomp10+1
elif FIML=="20m":
    fcomp20=fcomp20+1
    
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-224",(comp24*int(CC_IP0101))+(ecomp24*int(CC_PEIM01))+(fcomp24*(int(CC_PFB402)+int(CC_PFB802))))
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-124",(comp24*int(CC_IP0101))+(ecomp24*int(CC_PEIM01))+(fcomp24*(int(CC_PFB402)+int(CC_PFB802))))

GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-236",(comp36*int(CC_IP0101))+(ecomp36*int(CC_PEIM01))+(fcomp36*(int(CC_PFB402)+int(CC_PFB802))))
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-136",(comp36*int(CC_IP0101))+(ecomp36*int(CC_PEIM01))+(fcomp36*(int(CC_PFB402)+int(CC_PFB802))))

GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-248",(comp48*int(CC_IP0101))+(ecomp48*int(CC_PEIM01))+(fcomp48*(int(CC_PFB402)+int(CC_PFB802))))
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-148",(comp48*int(CC_IP0101))+(ecomp48*int(CC_PEIM01))+(fcomp48*(int(CC_PFB402)+int(CC_PFB802))))

GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-260",(comp60*int(CC_IP0101))+(ecomp60*int(CC_PEIM01))+(fcomp60*(int(CC_PFB402)+int(CC_PFB802))))
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-160",(comp60*int(CC_IP0101))+(ecomp60*int(CC_PEIM01))+(fcomp60*(int(CC_PFB402)+int(CC_PFB802))))

GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-284",(comp84*int(CC_IP0101))+(ecomp84*int(CC_PEIM01))+(fcomp84*(int(CC_PFB402)+int(CC_PFB802))))
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305980-184",(comp84*int(CC_IP0101))+(ecomp84*int(CC_PEIM01))+(fcomp84*(int(CC_PFB402)+int(CC_PFB802))))

GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305482-202",(comp2*int(CC_IP0101))+(ecomp2*int(CC_PEIM01))+(fcomp2*(int(CC_PFB402)+int(CC_PFB802))))
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305482-102",(comp2*int(CC_IP0101))+(ecomp2*int(CC_PEIM01))+(fcomp2*(int(CC_PFB402)+int(CC_PFB802))))

GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305482-205",(comp5*int(CC_IP0101))+(ecomp5*int(CC_PEIM01))+(fcomp5*(int(CC_PFB402)+int(CC_PFB802))))
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305482-105",(comp5*int(CC_IP0101))+(ecomp5*int(CC_PEIM01))+(fcomp5*(int(CC_PFB402)+int(CC_PFB802))))

GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305482-210",(comp10*int(CC_IP0101))+(ecomp10*int(CC_PEIM01))+(fcomp10*(int(CC_PFB402)+int(CC_PFB802))))
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305482-110",(comp10*int(CC_IP0101))+(ecomp10*int(CC_PEIM01))+(fcomp10*(int(CC_PFB402)+int(CC_PFB802))))

GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305482-220",(comp20*int(CC_IP0101))+(ecomp20*int(CC_PEIM01))+(fcomp20*(int(CC_PFB402)+int(CC_PFB802))))
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51305482-120",(comp20*int(CC_IP0101))+(ecomp20*int(CC_PEIM01))+(fcomp20*(int(CC_PFB402)+int(CC_PFB802))))

Trace.Write("qnt CC_IP0101: "+str(CC_IP0101))
Trace.Write("qnt"+str((comp84*int(CC_IP0101))+(ecomp84*int(CC_PEIM01))+(fcomp84*(int(CC_PFB402)+int(CC_PFB802)))))