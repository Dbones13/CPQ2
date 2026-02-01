def setAtvQty(AttrName,sv,qty):
    pvs=Product.Attr(AttrName).Values
    for av in pvs:
        if av.Display == sv:
            av.IsSelected=True
            av.Quantity=qty
            break

def resetAtvQty(AttrName):
    pvs=Product.Attr(AttrName).Values
    for av in pvs:
        av.IsSelected=False
        av.Quantity=0

resetAtvQty("MXP_Bom_Parts")

#MXP_Operator_station_transpose
#MXP_RAE_Thinclient_transpose

part_number = dict()
if Product.GetContainerByName("MXP_Operator_station_transpose"):
    for row in Product.GetContainerByName("MXP_Operator_station_transpose").Rows:
        if row["MXP_Type_of_station"] == "Desktop Computer, with Wide Screen Non touch monitor, UPS, keyboard,mouse and secondary Network Card.":
            if not part_number.get("3-4627-9N"):
                part_number["3-4627-9N"] = 1
            else:
                part_number["3-4627-9N"] += 1
            if not part_number.get("3-4627-BU"):
                part_number["3-4627-BU"] = 1
            else:
                part_number["3-4627-BU"] += 1
        if row["MXP_Type_of_station"] == "Desktop Computer, with Wide Screen Touchscreen monitor, UPS, keyboard, mouse and secondary Network Card.":
            if not part_number.get("3-4627-9T"):
                part_number["3-4627-9T"] = 1
            else:
                part_number["3-4627-9T"] += 1
            if not part_number.get("3-4627-BU"):
                part_number["3-4627-BU"] = 1
            else:
                part_number["3-4627-BU"] += 1
        if row["MXP_Type_of_station"] == "Op Station, with Wide Screen Non touch monitor,UPS,keyboard, & mouse and all required Software Licenses":
            if not part_number.get("3-4627-9ON"):
                part_number["3-4627-9ON"] = 1
            else:
                part_number["3-4627-9ON"] += 1
            if not part_number.get("3-5000-BU"):
                part_number["3-5000-BU"] = 1
            else:
                part_number["3-5000-BU"] += 1
        if row["MXP_Type_of_station"] == "Op Station, with Wide Screen Touchscreen monitor,UPS, keyboard, & mouse and all required Software Licenses":
            if not part_number.get("3-4627-9OT"):
                part_number["3-4627-9OT"] = 1
            else:
                part_number["3-4627-9OT"] += 1
            if not part_number.get("3-5000-BU"):
                part_number["3-5000-BU"] = 1
            else:
                part_number["3-5000-BU"] += 1
        if row["MXP_Type_of_station"] == "Desktop Computer(Tower model), with Wide Screen Non touch monitor, UPS and network switch,":
            if not part_number.get("3-5000-DT"):
                part_number["3-5000-DT"] = 1
            else:
                part_number["3-5000-DT"] += 1
            if not part_number.get("3-4627-BU"):
                part_number["3-4627-BU"] = 1
            else:
                part_number["3-4627-BU"] += 1
        if row["MXP_Experion_Monitor_Operator_station"] == "LCD Touch Screen Monitor":
            if not part_number.get("Q5095-65"):
                part_number["Q5095-65"] = 1
            else:
                part_number["Q5095-65"] += 1
        if row["MXP_Experion_Monitor_Operator_station"] == "Flat Panel Monitor 24in Wide Screen HD":
            if not part_number.get("Q5095-80"):
                part_number["Q5095-80"] = 1
            else:
                part_number["Q5095-80"] += 1
        if row["MXP_Experion_Monitor_Operator_station"] == "Pole Mount -Environmental Flat Panel Monitor with TouchScreen, Nema4":
            if not part_number.get("3-8187-20"):
                part_number["3-8187-20"] = 1
            else:
                part_number["3-8187-20"] += 1
        if row["MXP_Experion_Monitor_Operator_station"] == "Panel Mount-Environmental Flat Panel Monitor with TouchScreen, Nema4":
            if not part_number.get("3-8187-30"):
                part_number["3-8187-30"] = 1
            else:
                part_number["3-8187-30"] += 1
        if row["MXP_Environmental_User_Station"] == "EUS, 115 vac, NEMA 12, 50-95F (10-35C) temp range, fan cooled.":
            if not part_number.get("3-4629-00"):
                part_number["3-4629-00"] = 1
            else:
                part_number["3-4629-00"] += 1
        if row["MXP_Environmental_User_Station"] == "EUS,240vac, NEMA 12, 50-95F (10-35C) temp range, fan cooled.":
            if not part_number.get("3-4629-01"):
                part_number["3-4629-01"] = 1
            else:
                part_number["3-4629-01"] += 1
        if row["MXP_Environmental_User_Station"] == "EUS, 115 vac, NEMA 12, 50-122F (10-50C) temp range, water cooled.":
            if not part_number.get("3-4629-30"):
                part_number["3-4629-30"] = 1
            else:
                part_number["3-4629-30"] += 1
        if row["MXP_Environmental_User_Station"] == "EUS, 240 vac, NEMA 12, 50-122F (10-50C) temp range, water cooled.":
            if not part_number.get("3-4629-31"):
                part_number["3-4629-31"] = 1
            else:
                part_number["3-4629-31"] += 1
        if row["MXP_Environmental_User_Station"] == "EUS, 115 vac, NEMA 12, 50-122F (10-50C) temp range, A/C cooled.":
            if not part_number.get("3-4629-90"):
                part_number["3-4629-90"] = 1
            else:
                part_number["3-4629-90"] += 1
        if row["MXP_Environmental_User_Station"] == "EUS, 240 vac, NEMA 12, 50-122F (10-50C) temp range, A/C cooled.":
            if not part_number.get("3-4629-91"):
                part_number["3-4629-91"] = 1
            else:
                part_number["3-4629-91"] += 1
        if row["MXP_Additional_Backup"] == "Hard Drive Externa USB":
            if not part_number.get("3-8896-00"):
                part_number["3-8896-00"] = 1
            else:
                part_number["3-8896-00"] += 1
        if row["MXP_Additional_Backup"] == "Network Storage DELL NX440 1U Rack.8 GB":
            if not part_number.get("MZ-NWSTR6"):
                part_number["MZ-NWSTR6"] = 1
            else:
                part_number["MZ-NWSTR6"] += 1
        if row["MXP_Additional_Backup"] == "Network Storage DELL NX440 1U Rack 16 GB":
            if not part_number.get("MZ-NWSTR7"):
                part_number["MZ-NWSTR7"] = 1
            else:
                part_number["MZ-NWSTR7"] += 1
        if row["MXP_Long_Distance_Driver_for_Keyboard"] == "Yes":
            if not part_number.get("3-8895-00"):
                part_number["3-8895-00"] = 1
            else:
                part_number["3-8895-00"] += 1

if Product.GetContainerByName("MXP_RAE_Thinclient_transpose"):
    for row in Product.GetContainerByName("MXP_RAE_Thinclient_transpose").Rows:
        if row["MXP_Thin_client_operation"] == "TP-THNCL6-100":
            if not part_number.get("TP-THNCL6-100"):
                part_number["TP-THNCL6-100"] = 1
            else:
                part_number["TP-THNCL6-100"] += 1
        if row["MXP_Thin_client_operation"] == "TP-THNCL7-100":
            if not part_number.get("TP-THNCL7-100"):
                part_number["TP-THNCL7-100"] = 1
            else:
                part_number["TP-THNCL7-100"] += 1
        if row["MXP_Experion_monitor_Thin_Client"] == "LCD Touch Screen Monitor":
            if not part_number.get("Q5095-65"):
                part_number["Q5095-65"] = 1
            else:
                part_number["Q5095-65"] += 1
        if row["MXP_Experion_monitor_Thin_Client"] == "Flat Panel Monitor 24in Wide Screen HD":
            if not part_number.get("Q5095-80"):
                part_number["Q5095-80"] = 1
            else:
                part_number["Q5095-80"] += 1
        if row["MXP_Experion_monitor_Thin_Client"] == "Pole Mount -Environmental Flat Panel Monitor with TouchScreen, Nema4":
            if not part_number.get("3-8187-20"):
                part_number["3-8187-20"] = 1
            else:
                part_number["3-8187-20"] += 1
        if row["MXP_Experion_monitor_Thin_Client"] == "Panel Mount-Environmental Flat Panel Monitor with TouchScreen, Nema4":
            if not part_number.get("3-8187-30"):
                part_number["3-8187-30"] = 1
            else:
                part_number["3-8187-30"] += 1

for key in part_number:
    setAtvQty("MXP_Bom_Parts",key,part_number[key])