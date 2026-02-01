import GS_PS_Exp_Ent_BOM

Node_Device=TagParserProduct.ParseString('<* CTX( Container(Leak Detection System Interfaces).Row(1).Column(Nodes).Get ) *>')
Option_required=TagParserProduct.ParseString('<* CTX( Container(Leak Detection System Interfaces).Row(2).Column(Devices).Get ) *>')
EP_APLD25_qty=TagParserProduct.ParseString('<* Eval(0 - INT(0 - (<*CTX( Container(Leak Detection System Interfaces).Row(1).Column(Nodes).Get )*>/25))) *>')
try:
	EP_APLD25_qty = int(EP_APLD25_qty)
except:
	EP_APLD25_qty = 0
if int(EP_APLD25_qty)>0 and Option_required=="Yes":
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"SCADA_BOM_Items","EP-APLD25",int(EP_APLD25_qty))
else:
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"SCADA_BOM_Items","EP-APLD25",0)