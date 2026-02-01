clr.AddReference('System.Core')
import System
clr.ImportExtensions(System.Linq)
Model_ID=""
pannel_partnum_qty = dict()
part_desc_dict = dict()
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

val_1u = Product.Attr('Cabinet_5_Slot_Space_1U').GetValue()
if val_1u != '' and val_1u != 0:
    panel_1U=SPARE_PARTS_SERVER_CABINET_LIST.Where(lambda x:(x.Panel_Unit == '1')).Select(lambda y:y)
    for pn in panel_1U:
        l = pannel_partnum_qty.get(pn.Part_Number,0)
        if l > 0:
            pannel_partnum_qty[pn.Part_Number] = l + int(val_1u)
        else:
            pannel_partnum_qty[pn.Part_Number] = int(val_1u)
        part_desc_dict[str(pn.Part_Number)] = pn.Description
val_2u = Product.Attr('Cabinet_5_Slot_Space_2U').GetValue()
if val_2u != '' and val_2u != 0:
    panel_2U=SPARE_PARTS_SERVER_CABINET_LIST.Where(lambda x:(x.Panel_Unit == '2')).Select(lambda y:y)
    for pn in panel_2U:
        l = pannel_partnum_qty.get(pn.Part_Number,0)
        if l > 0:
            pannel_partnum_qty[pn.Part_Number] = l + int(val_2u)
        else:
            pannel_partnum_qty[pn.Part_Number] = int(val_2u)
        part_desc_dict[str(pn.Part_Number)] = pn.Description
val_3u = Product.Attr('Cabinet_5_Slot_Space_3U').GetValue()
if val_3u != '' and val_3u != 0:
    panel_3U=SPARE_PARTS_SERVER_CABINET_LIST.Where(lambda x:(x.Panel_Unit == '3')).Select(lambda y:y)
    for pn in panel_3U:
        l = pannel_partnum_qty.get(pn.Part_Number,0)
        if l > 0:
            pannel_partnum_qty[pn.Part_Number] = l + int(val_3u)
        else:
            pannel_partnum_qty[pn.Part_Number] = int(val_3u)
        part_desc_dict[str(pn.Part_Number)] = pn.Description
val_4u = Product.Attr('Cabinet_5_Slot_Space_4U').GetValue()
if val_4u != '' and val_4u != 0:
    panel_4U=SPARE_PARTS_SERVER_CABINET_LIST.Where(lambda x:(x.Panel_Unit == '4')).Select(lambda y:y)
    for pn in panel_4U:
        l = pannel_partnum_qty.get(pn.Part_Number,0)
        if l > 0:
            pannel_partnum_qty[pn.Part_Number] = l + int(val_4u)
        else:
            pannel_partnum_qty[pn.Part_Number] = int(val_4u)
        part_desc_dict[str(pn.Part_Number)] = pn.Description
cont = Product.GetContainerByName('Spare_Parts_Cabinet_PartSummary')
attr_map = dict()
Price_map = dict()
Description_map = dict()
for av in Product.Attr('Spare_Parts_Server_Cabinet_PartSummary').SelectedValues:
    attr_map[av.Display] = av.Quantity
for p in List_TobePopulated:
    Price_map[p.Part_Number] = p.Price
    Description_map[p.Part_Number] = p.Description
if cont.Rows.Count > 0:
    for row in cont.Rows:
        qty=0
        row.IsSelected = True
        if pannel_partnum_qty.get(row['PartNumber']):
            row['Quantity'] = str(pannel_partnum_qty[row['PartNumber']])
            row['Price'] = "Yes"
            row['Part_Number_Description'] = part_desc_dict[row['PartNumber']]
            qty = str(pannel_partnum_qty[row['PartNumber']])
        else:
            row['Quantity'] = str(attr_map[row['PartNumber']])
            row['Price'] = str(Price_map[row['PartNumber']])
            row['Part_Number_Description'] = str(Description_map[row['PartNumber']])
            qty = str(attr_map[row['PartNumber']])
        row.Calculate()
        for attr in filter(lambda a : a.DisplayType != "Container", row.Product.Attributes):
            if attr.Name == "ItemQuantity":
                attr.AssignValue(qty)
        row.ApplyProductChanges()
    cont.Calculate()