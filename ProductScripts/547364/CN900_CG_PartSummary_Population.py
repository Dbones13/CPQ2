import System.Decimal as D
def setAtvQty(Product,AttrName,PartNumber,qty):
    Cont=Product.Attr(AttrName).Values
    for Parts in Cont:
        if Parts.Display == PartNumber:
            Parts.IsSelected=False
            Parts.Quantity = 0
            if qty > 0:
                Parts.IsSelected=True
                Parts.Quantity=qty
                Trace.Write('Selected ' + PartNumber + ' in attribute ' + AttrName + ' at Qty ' + str(qty))
                break

Contr_Type = Product.GetContainerByName('CN900_Cabinet_Controller_Cont').Rows[0].GetColumnByName('CN900_Controller_Type').Value
Contr_Mod = Product.GetContainerByName('CN900_Cabinet_Controller_Cont').Rows[0].GetColumnByName('CN900_Controller_Modules').Value if Product.GetContainerByName('CN900_Cabinet_Controller_Cont').Rows[0].GetColumnByName('CN900_Controller_Modules').Value else 0
PowerType = Product.GetContainerByName('CN900_Cabinet_Controller_Cont').Rows[0].GetColumnByName('CN900_Power_Input_Type').Value
Cabinet_racks = Product.GetContainerByName('CN900_Cabinet_Controller_Cont').Rows[0].GetColumnByName('CN900_Cabinet_Required').Value
Cabinet_access = Product.GetContainerByName('CN900_Cabinet_Controller_Cont').Rows[0].GetColumnByName('CN900_Cabinet_Access').Value

QtyController =SingleCabQty=DoubleCabQty=MSD000=QtyControllerTNF=QtyControllerP01=QtyControllerP24=QtyControllerP0107=0
if Contr_Type=="Redundant":
    QtyController= int(Contr_Mod) * 2
else:
    QtyController=QtyControllerTNF= int(Contr_Mod)

if PowerType =="AC":
    QtyControllerP01= QtyController
elif PowerType =="DC":
    QtyControllerP24= QtyController
elif PowerType =="ACE":
    QtyControllerP0107= QtyController

if float(QtyController) > 0:
    MSD000_QTY= 1 # for CF-MSD000
    if Cabinet_racks=="Yes" and Cabinet_access=="Single Access":
        SingleCabQty = D.Ceiling(float(QtyController)/5.0)
    elif Cabinet_racks=="Yes" and Cabinet_access=="Dual Access":
        DoubleCabQty = D.Ceiling(float(QtyController)/10.0)

SP0000_QTY = SingleCabQty + DoubleCabQty #for CF-SP0000,51198959-200,51196958-400
FAN611_QTY = SingleCabQty + (DoubleCabQty * 2) # for MC-FAN611
FTA_MTG_QTY = (SingleCabQty * 4)+ (DoubleCabQty * 8) #for  51304063-100

#Controller and Rack Parts
setAtvQty(Product,"CN900_Bom_Parts","900CN9-0100",QtyController)
setAtvQty(Product,"CN900_Bom_Parts","900E01-0100",QtyController)
setAtvQty(Product,"CN900_Bom_Parts","900R01-0300",QtyController)
setAtvQty(Product,"CN900_Bom_Parts","900TNF-0200",QtyControllerTNF)

#Power supply Parts
setAtvQty(Product,"CN900_Bom_Parts","900P01-0501",QtyControllerP01)
setAtvQty(Product,"CN900_Bom_Parts","900P24-0501",QtyControllerP24)
setAtvQty(Product,"CN900_Bom_Parts","900P01-0701",QtyControllerP0107)

#Cabinet Parts
setAtvQty(Product,"CN900_Bom_Parts","MU-C8SS01",SingleCabQty)
setAtvQty(Product,"CN900_Bom_Parts","MU-C8DS01",DoubleCabQty)
setAtvQty(Product,"CN900_Bom_Parts","MC-FAN611",FAN611_QTY)
setAtvQty(Product,"CN900_Bom_Parts","51304063-100",FTA_MTG_QTY)
setAtvQty(Product,"CN900_Bom_Parts","51198959-200",SP0000_QTY)

#Ship Crate and Pallet Part
setAtvQty(Product,"CN900_Bom_Parts","51196958-400",SP0000_QTY)
setAtvQty(Product,"CN900_Bom_Parts","CF-MSD000",MSD000_QTY)
setAtvQty(Product,"CN900_Bom_Parts","CF-SP0000",SP0000_QTY)