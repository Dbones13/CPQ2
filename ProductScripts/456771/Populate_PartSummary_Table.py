clr.AddReference('System.Core')
import System
clr.ImportExtensions(System.Linq)
def setAtvQty(AttrName,sv,qty):
    pvs=Product.Attr(AttrName).Values
    for av in pvs:
        if av.Display == sv:
            av.IsSelected=True
            av.Quantity=qty
            Trace.Write('Selected ' + sv + ' in  attribute ' + AttrName + ' at Qty ' + str(qty))
            break
Model_ID=""
Doors=Product.Attr('Spare_Parts_Cabinet_Door_Type').GetValue()
DepthSize=Product.Attr('Spare_Parts_Cabinet_Depth').GetValue()
PowerSupplyVoltage=Product.Attr('Spare_Parts_Power_Supply_Voltage').GetValue()
if DepthSize == '1 meter':
    if PowerSupplyVoltage == '120V':
        if Doors == 'Standard':
            Model_ID="MP-C1MCB1-100"
        elif  Doors == 'Reverse Front':
            Model_ID="MP-C1MCB1-103"
        elif  Doors == 'Reverse Rear':
            Model_ID="MP-C1MCB1-102"
        elif  Doors == 'Reverse Front & Rear':
            Model_ID="MP-C1MCB1-101"
    if PowerSupplyVoltage == '240V':
        if Doors == 'Standard':
            Model_ID="MP-C1MCB1-200"
        elif  Doors == 'Reverse Front':
            Model_ID="MP-C1MCB1-203"
        elif  Doors == 'Reverse Rear':
            Model_ID="MP-C1MCB1-202"
        elif  Doors == 'Reverse Front & Rear':
            Model_ID="MP-C1MCB1-201"
if DepthSize == '800 mm':
    if PowerSupplyVoltage == '120V':
        if Doors == 'Standard':
            Model_ID="MP-C8LCB1-100"
        elif  Doors == 'Reverse Front':
            Model_ID="MP-C8LCB1-103"
        elif  Doors == 'Reverse Rear':
            Model_ID="MP-C8LCB1-102"
        elif  Doors == 'Reverse Front & Rear':
            Model_ID="MP-C8LCB1-101"
    if PowerSupplyVoltage == '240V':
        if Doors == 'Standard':
            Model_ID="MP-C8LCB1-200"
        elif  Doors == 'Reverse Front':
            Model_ID="MP-C8LCB1-203"
        elif  Doors == 'Reverse Rear':
            Model_ID="MP-C8LCB1-202"
        elif  Doors == 'Reverse Front & Rear':
            Model_ID="MP-C8LCB1-201"
Trace.Write(Model_ID)
SP_PS_Con=Product.GetContainerByName('Spare_Parts_Cabinet_PartSummary')
SPARE_PARTS_SERVER_CABINET_LIST=SqlHelper.GetList("Select * from Spare_Parts_server_Cabinet Where Model_Number ='{}'".format(Model_ID)).ToList()
List_TobePopulated=SPARE_PARTS_SERVER_CABINET_LIST.Where(lambda x:(x.Attribute == 'Spare_Parts_Cabinet_Thermostat_Required' and x.Option == Product.Attr('Spare_Parts_Cabinet_Thermostat_Required').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Door_Type' and x.Option == Product.Attr('Spare_Parts_Cabinet_Door_Type').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Keylock_Type' and x.Option == Product.Attr('Spare_Parts_Cabinet_Keylock_Type').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_TDI_Power_Supply_Cable_Length' and x.Option == Product.Attr('Spare_Parts_Cabinet_TDI_Power_Supply_Cable_Length').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Color' and x.Option == Product.Attr('Spare_Parts_Cabinet_Color').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Hinge_Type' and x.Option == Product.Attr('Spare_Parts_Cabinet_Hinge_Type').GetValue()) or (x.Attribute == 'Spare_Parts_Cabinet_Base_Required' and x.Option == Product.Attr('Spare_Parts_Cabinet_Base_Required').GetValue()) or x.Attribute == "Default").Select(lambda y: y)
Trace.Write(str(List_TobePopulated))
Product.GetContainerByName('Spare_Parts_Cabinet_PartSummary').Clear()
Product.DisallowAttr('Spare_Parts_Server_Cabinet_PartSummary')
for Row in List_TobePopulated:
    Trace.Write(Row.Part_Number)
    if Row.Part_Number!= "" and Row.Qty and int(Row.Qty):
        setAtvQty('Spare_Parts_Server_Cabinet_PartSummary',Row.Part_Number,int(Row.Qty))
val_1u = Product.Attr('Cabinet_5_Slot_Space_1U').GetValue()
part_1u = {"51201248-100" : "BLANK PANEL, 1U 1.72IN  (4,4CM) BLACK", "51303521-100": "BAFFLE, AIR DUCT 1.72X15.80IN","51306194-100": "BRACKET, CABINET REAR RAIL, 1U FOR LCN R"}
panel_1U=SPARE_PARTS_SERVER_CABINET_LIST.Where(lambda x:(x.Panel_Unit == '1')).Select(lambda y:y)

val_2u = Product.Attr('Cabinet_5_Slot_Space_2U').GetValue()
part_2u = {"51201248-200" : "BLANK PANEL, 1U 1.72IN  (4,4CM) BLACK", "51303521-200": "BAFFLE, AIR DUCT 1.72X15.80IN","51306194-200": "BRACKET, CABINET REAR RAIL, 1U FOR LCN R"}
panel_2U=SPARE_PARTS_SERVER_CABINET_LIST.Where(lambda x:(x.Panel_Unit == '2')).Select(lambda y:y)

val_3u = Product.Attr('Cabinet_5_Slot_Space_3U').GetValue()
part_3u = {"51201248-300" : "BLANK PANEL, 1U 1.72IN  (4,4CM) BLACK", "51303521-300": "BAFFLE, AIR DUCT 1.72X15.80IN","51306194-300": "BRACKET, CABINET REAR RAIL, 1U FOR LCN R"}
panel_3U=SPARE_PARTS_SERVER_CABINET_LIST.Where(lambda x:(x.Panel_Unit == '3')).Select(lambda y:y)

val_4u = Product.Attr('Cabinet_5_Slot_Space_4U').GetValue()
part_4u = {"51201248-400" : "BLANK PANEL, 1U 1.72IN  (4,4CM) BLACK", "51303521-400": "BAFFLE, AIR DUCT 1.72X15.80IN","51306194-400": "BRACKET, CABINET REAR RAIL, 1U FOR LCN R"}
panel_4U=SPARE_PARTS_SERVER_CABINET_LIST.Where(lambda x:(x.Panel_Unit == '4')).Select(lambda y:y)

SP_PS_Con=Product.GetContainerByName('Spare_Parts_Cabinet_PartSummary')
pannel_partnum_qty = dict()
if val_1u != 0 and val_1u != "":
    for part in panel_1U:
        l = pannel_partnum_qty.get(part.Part_Number,0)
        if l > 0:
            pannel_partnum_qty[part.Part_Number] = l + int(val_1u)
        else:
            pannel_partnum_qty[part.Part_Number] = int(val_1u)
if val_2u != 0 and val_2u != "":
    for part in panel_2U:
        l = pannel_partnum_qty.get(part.Part_Number,0)
        if l > 0:
            pannel_partnum_qty[part.Part_Number] = l + int(val_2u)
        else:
            pannel_partnum_qty[part.Part_Number] = int(val_2u)
if val_3u != 0 and val_3u != "":
    for part in panel_3U:
        l = pannel_partnum_qty.get(part.Part_Number,0)
        if l > 0:
            pannel_partnum_qty[part.Part_Number] = l + int(val_3u)
        else:
            pannel_partnum_qty[part.Part_Number] = int(val_3u)
if val_4u != 0 and val_4u != "":
    for part in panel_4U:
        l = pannel_partnum_qty.get(part.Part_Number,0)
        if l > 0:
            pannel_partnum_qty[part.Part_Number] = l + int(val_4u)
        else:
            pannel_partnum_qty[part.Part_Number] = int(val_4u)
for partn in pannel_partnum_qty:
    setAtvQty('Spare_Parts_Server_Cabinet_PartSummary',partn,pannel_partnum_qty[partn])