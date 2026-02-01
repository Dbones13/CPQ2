sc_cont = Product.GetContainerByName("SC_ServiceContract_P1P2_Cont")
sc_cont.Rows.Clear()

sc_module = Product.GetContainerByName("Service Contract Modules")
if sc_module.Rows.Count:
    for row in sc_module.Rows:
        if row["Module"] == "Parts Management":
            p1p2_cont = row.Product.GetContainerByName("SC_P1P2_Parts_Details")
            p1p2_invalid_cont = row.Product.GetContainerByName("SC_P1P2_Invalid_Parts")
            if p1p2_cont.Rows.Count > 0:
                for prow in p1p2_cont.Rows:
                    scrow = sc_cont.AddNewRow(False)
                    scrow["Service_Product"] = prow["Service_Product"]
                    scrow["Part_Number"] = prow["Part_Number"]
                    scrow["Part_Status"] = prow["Part_Status"]
                    scrow["Description"] = prow["Description"]
                    scrow["Qty"] = prow["Qty"] if prow["Qty"] != "" else "0"
                    scrow["Unit_Price"] = prow["Unit_Price"] if prow["Unit_Price"] != "" else "0"
                    scrow["Ext_Price"] = prow["Ext_Price"] if prow["Ext_Price"] != "" else "0"
                    scrow["Replacement_Status"] = prow["Replacement_Status"]
                    scrow["Replacement_Part"] = prow["Replacement_Part"]
                    scrow["Comments"] = prow["Comments"]
                    scrow["PY_Quantity"] = prow["PY_Quantity"] if prow["PY_Quantity"] != "" else "0"
                    scrow["CY_Quantity"] = prow["CY_Quantity"] if prow["CY_Quantity"] != "" else "0"
                    scrow["PY_UnitPrice"] = prow["PY_UnitPrice"] if prow["PY_UnitPrice"] != "" else "0"
                    scrow["PY_ExtPrice"] = prow["PY_ExtPrice"] if prow["PY_ExtPrice"] != "" else "0"
                    scrow["CY_ExtPrice"] = prow["CY_ExtPrice"] if prow["CY_ExtPrice"] != "" else "0"
                    scrow["Status"] = "Valid"
                sc_cont.Calculate()
            if row.Product.Attr('SC_Product_Type').GetValue() == "Renewal":
                if p1p2_invalid_cont.Rows.Count > 0:
                    for prow in p1p2_invalid_cont.Rows:
                        scrow = sc_cont.AddNewRow(False)
                        scrow["Service_Product"] = prow["Service_Product"]
                        scrow["Part_Number"] = prow["Part_Number"]
                        scrow["Description"] = prow["Description"]
                        scrow["PY_Quantity"] = prow["PY_Quantity"] if prow["PY_Quantity"] != "" else "0"
                        scrow["CY_Quantity"] = prow["CY_Quantity"] if prow["CY_Quantity"] != "" else "0"
                        reason = prow["Reason"].replace('<br>',',')[0:-1] if prow["Reason"] != "" else ""
                        scrow["Comments"] = reason
                        scrow["Status"] = "Invalid"
                    sc_cont.Calculate()