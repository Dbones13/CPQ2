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

resetAtvQty("MX_Platform_Bom_Parts")


part_number = dict()
for row in Product.GetContainerByName("MX_Operator_station_transpose").Rows:
    if row["MX_Operation_PowerSupply"] == "Yes":
        if not part_number.get("Q4732-50"):
            part_number["Q4732-50"] = 1
        else:
            part_number["Q4732-50"] += 1

    if row["MX_Operation_KVM"] == "Yes":
        if not part_number.get("Q8895-50"):
            part_number["Q8895-50"] = 1
        else:
            part_number["Q8895-50"] += 1

    if row["MX_Operation_Monitor"] == "LCD Monitor for Q5095-50 Operator Station":
        if not part_number.get("Q5095-60"):
            part_number["Q5095-60"] = 1
        else:
            part_number["Q5095-60"] += 1

    if row["MX_Operation_Monitor"] == "LCD Touch Screen Monitor for Q5095-50 Operator Station":
        if not part_number.get("Q5095-65"):
            part_number["Q5095-65"] = 1
        else:
            part_number["Q5095-65"] += 1

    if row["MX_Operation_Monitor"] == "Z, EZ 21 INCH FPD, TOUCH":
        if not part_number.get("TP-FPT214-100"):
            part_number["TP-FPT214-100"] = 1
        else:
            part_number["TP-FPT214-100"] += 1

    if row["MX_Operation_Monitor"] == "21.3  EZ FLAT PANEL DISPLAY":
        if not part_number.get("TP-FPD214-100"):
            part_number["TP-FPD214-100"] = 1
        else:
            part_number["TP-FPD214-100"] += 1

    if row["MX_Operation_Monitor"] == "ICON 21 INCH FPD, TOUCH":
        if not part_number.get("TP-FPT213-100"):
            part_number["TP-FPT213-100"] = 1
        else:
            part_number["TP-FPT213-100"] += 1

    if row["MX_Operation_Monitor"] == "FPD, 21.3IN ICON SERIES MONITOR":
        if not part_number.get("TP-FPD213-100"):
            part_number["TP-FPD213-100"] = 1
        else:
            part_number["TP-FPD213-100"] += 1

    if row["MX_Operation_Monitor"] == "DESKTOP 21 INCH FPD, TOUCH":
        if not part_number.get("TP-FPT211-100"):
            part_number["TP-FPT211-100"] = 1
        else:
            part_number["TP-FPT211-100"] += 1


for row in Product.GetContainerByName("MX_RAE_Thinclient_transpose").Rows:
    if row["Thin client Operator Station"] == "BTC12 THIN CLIENT UTC OS":
        if not part_number.get("TP-THNCL6-100"):
            part_number["TP-THNCL6-100"] = 1
        else:
            part_number["TP-THNCL6-100"] += 1

    if row["Thin client Operator Station"] == "BTC14 THIN CLIENT UTC OS":
        if not part_number.get("TP-THNCL7-100"):
            part_number["TP-THNCL7-100"] = 1
        else:
            part_number["TP-THNCL7-100"] += 1

    if row["Experion Monitor"] == "LCD Monitor for Q5095-50 Operator Station":
        if not part_number.get("Q5095-60"):
            part_number["Q5095-60"] = 1
        else:
            part_number["Q5095-60"] += 1

    if row["Experion Monitor"] == "LCD Touch Screen Monitor for Q5095-50 Operator Station":
        if not part_number.get("Q5095-65"):
            part_number["Q5095-65"] = 1
        else:
            part_number["Q5095-65"] += 1

    if row["Experion Monitor"] == "Z, EZ 21 INCH FPD, TOUCH":
        if not part_number.get("TP-FPT214-100"):
            part_number["TP-FPT214-100"] = 1
        else:
            part_number["TP-FPT214-100"] += 1

    if row["Experion Monitor"] == "21.3  EZ FLAT PANEL DISPLAY":
        if not part_number.get("TP-FPD214-100"):
            part_number["TP-FPD214-100"] = 1
        else:
            part_number["TP-FPD214-100"] += 1

    if row["Experion Monitor"] == "ICON 21 INCH FPD, TOUCH":
        if not part_number.get("TP-FPT213-100"):
            part_number["TP-FPT213-100"] = 1
        else:
            part_number["TP-FPT213-100"] += 1

    if row["Experion Monitor"] == "FPD, 21.3IN ICON SERIES MONITOR":
        if not part_number.get("TP-FPD213-100"):
            part_number["TP-FPD213-100"] = 1
        else:
            part_number["TP-FPD213-100"] += 1

    if row["Experion Monitor"] == "DESKTOP 21 INCH FPD, TOUCH":
        if not part_number.get("TP-FPT211-100"):
            part_number["TP-FPT211-100"] = 1
        else:
            part_number["TP-FPT211-100"] += 1

for key in part_number:
    setAtvQty("MX_Platform_Bom_Parts",key,part_number[key])