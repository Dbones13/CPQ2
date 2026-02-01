def getContainer(Product,Name):
    return Product.GetContainerByName(Name)
mx_laborCon = getContainer(Product,"Experion_mx_Labor_Container")
if mx_laborCon.Rows.Count > 0:
    # return deliverables
    for row in mx_laborCon.Rows:
        oldCalHrs = row["Calculated Hrs"]
        if row["Deliverable"] == "Experion MX Engineering Plan":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "Experion MX Functional Design Specification":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "Experion MX Procure Materials & Services":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "Experion MX Detail Design Specifications":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "Experion MX Test Procedure (FAT & SAT)":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "Experion MX Hardware Engineering":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "Experion MX Software Configuration":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "Experion MX System Integration & Internal Test":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "Experion MX Factory Acceptance Test & Sign off":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "Experion MX Site Installation":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "Experion MX Site Acceptance Test & Sign off":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "Experion MX Cut Over Procedure":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "Experion MX Operation Manual":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "Experion MX Customer Training":
            row["Calculated Hrs"] = "0"

        elif row["Deliverable"] == "Experion MX Project Close Out Report":
            row["Calculated Hrs"] = "0"

    ScriptExecutor.Execute('final_hr')
    ScriptExecutor.Execute('PS_Populate_Prices')