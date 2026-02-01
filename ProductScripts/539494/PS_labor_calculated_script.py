def getContainer(Product,Name):
    return Product.GetContainerByName(Name)
mxpro_laborCon = getContainer(Product,"MXPro_Labor_Container")
if mxpro_laborCon.Rows.Count > 0:
    # return deliverables
    for row in mxpro_laborCon.Rows:
        oldCalHrs = row["Calculated Hrs"]
        if row["Deliverable"] == "MXProLine Engineering Plan":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "MXProLine Functional Design Specification":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "MXProLine Procure Materials & Services":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "MXProLine Detail Design Specifications":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "MXProLine Test Procedure (FAT & SAT)":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "MXProLine Hardware Engineering":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "MXProLine Control Application Configuration":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "MXProLine System Integration & Internal Test":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "MXProLine Factory Acceptance Test & Sign off":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "MXProLine Site Installation":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "MXProLine Site Acceptance Test & Sign off":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "MXProLine Cut Over Procedure":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "MXProLine Operation Manual":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "MXProLine Customer Training":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "MXProLine Project Close Out Report":
            row["Calculated Hrs"] = "0"

    ScriptExecutor.Execute('Final_hr')
    ScriptExecutor.Execute('PS_Populate_Prices')