tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Immersive Field Simulator' in tabs:
    validModelsCont = Product.GetContainerByName('SC_WEP_Models_Scope_IFS')
    entitlement = Product.GetContainerByName('SC_WEP_Entitlement_IFS')
elif 'HALO OA' in tabs:
    validModelsCont = Product.GetContainerByName('SC_WEP_Models_Scope_Halo')
    entitlement = Product.GetContainerByName('SC_WEP_Entitlement_Halo')
elif 'Training' in tabs:
    validModelsCont = Product.GetContainerByName('SC_WEP_Models_Scope_Training')
    entitlement = Product.GetContainerByName('SC_WEP_Entitlement_Training')
elif 'Training Needs Assessment' in tabs:
    validModelsCont = Product.GetContainerByName('SC_WEP_Models_Scope_TNA')
    entitlement = Product.GetContainerByName('SC_WEP_Entitlement_TNA')

validModelsCont.Calculate()

flag_20 = False
if validModelsCont.Name in ('SC_WEP_Models_Scope_Halo','SC_WEP_Models_Scope_IFS'):
    if entitlement.Rows.Count:
        for row in entitlement.Rows:
            if row["Entitlement"] == "Software Updates" or row["Entitlement"] == "Software Upgrades":
                if row.IsSelected == True:
                    flag_20 = True
                    break

if Product.Attr('SC_Product_Type').GetValue() == "New":
    if flag_20 == True:
        if validModelsCont.Rows.Count:
            for row in validModelsCont.Rows:
                if row["Unit_Price"] != "":
                    row["UI_Price"] = str(float(float(row["Unit_Price"])*20/100))
                    row["Hidden_UnitPrice"] = str(float(float(row["Unit_Price"])*20/100))
                    if row["Quantity"] != "":
                        row["List_Price"] = str(float(row["UI_Price"])*float(row["Quantity"]))
                        row["Hidden_ListPrice"] = str(float(row["UI_Price"])*float(row["Quantity"]))
                if row["Unit_Cost"] != "":
                    row["UI_Cost"] = str(float(float(row["Unit_Cost"])*20/100))
                    row["Hidden_UnitCost"] = str(float(float(row["Unit_Cost"])*20/100))
                    if row["Quantity"] != "":
                        row["Cost_Price"] = str(float(row["UI_Cost"])*float(row["Quantity"]))
                        row["Hidden_CostPrice"] = str(float(row["UI_Cost"])*float(row["Quantity"]))
    else:
        if validModelsCont.Name in ('SC_WEP_Models_Scope_Halo','SC_WEP_Models_Scope_IFS'):
            if validModelsCont.Rows.Count:
                for row in validModelsCont.Rows:
                    if row["Unit_Price"] != "":
                        row["UI_Price"] = row["Unit_Price"]
                        row["Hidden_UnitPrice"] = row["Unit_Price"]
                        if row["Quantity"] != "":
                            row["List_Price"] = str(float(row["UI_Price"])*float(row["Quantity"]))
                            row["Hidden_ListPrice"] = str(float(row["UI_Price"])*float(row["Quantity"]))
                    if row["Unit_Cost"] != "":
                        row["UI_Cost"] = row["Unit_Cost"]
                        row["Hidden_UnitCost"] = row["Unit_Cost"]
                        if row["Quantity"] != "":
                            row["Cost_Price"] = str(float(row["UI_Cost"])*float(row["Quantity"]))
                            row["Hidden_CostPrice"] = str(float(row["UI_Cost"])*float(row["Quantity"]))
        else:
            if validModelsCont.Rows.Count:
                for row in validModelsCont.Rows:
                    if row["Unit_Price"] != "":
                        row["Hidden_UnitPrice"] = row["Unit_Price"]
                        if row["Quantity"] != "":
                            row["List_Price"] = str(float(row["Unit_Price"])*float(row["Quantity"]))
                            row["Hidden_ListPrice"] = str(float(row["Unit_Price"])*float(row["Quantity"]))
                    if row["Unit_Cost"] != "":
                        row["Hidden_UnitCost"] = row["Unit_Cost"]
                        if row["Quantity"] != "":
                            row["Cost_Price"] = str(float(row["Unit_Cost"])*float(row["Quantity"]))
                            row["Hidden_CostPrice"] = str(float(row["Unit_Cost"])*float(row["Quantity"]))
    validModelsCont.Calculate()

elif Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    if flag_20 == True:
        if validModelsCont.Rows.Count:
            for row in validModelsCont.Rows:
                if row["Unit_Price"] != "":
                    row["CY_UnitPrice"] = str(float(float(row["Unit_Price"])*20/100))
                    row["Hidden_UnitPrice"] = str(float(float(row["Unit_Price"])*20/100))
                    if row["CY_Quantity"] != "":
                        row["CY_ListPrice"] = str(float(row["CY_UnitPrice"])*float(row["CY_Quantity"]))
                        row["Hidden_ListPrice"] = str(float(row["CY_UnitPrice"])*float(row["CY_Quantity"]))
                if row["Unit_Cost"] != "":
                    row["CY_UnitCost"] = str(float(float(row["Unit_Cost"])*20/100))
                    row["Hidden_UnitCost"] = str(float(float(row["Unit_Cost"])*20/100))
                    if row["CY_Quantity"] != "":
                        row["CY_CostPrice"] = str(float(row["CY_UnitCost"])*float(row["CY_Quantity"]))
                        row["Hidden_CostPrice"] = str(float(row["CY_UnitCost"])*float(row["CY_Quantity"]))
    else:
        if validModelsCont.Rows.Count:
            for row in validModelsCont.Rows:
                if row["Unit_Price"] != "":
                    row["CY_UnitPrice"] = row["Unit_Price"]
                    row["Hidden_UnitPrice"] = row["Unit_Price"]
                    if row["CY_Quantity"] != "":
                        row["CY_ListPrice"] = str(float(row["CY_UnitPrice"])*float(row["CY_Quantity"]))
                        row["Hidden_ListPrice"] = str(float(row["CY_UnitPrice"])*float(row["CY_Quantity"]))
                if row["Unit_Cost"] != "":
                    row["CY_UnitCost"] = row["Unit_Cost"]
                    row["Hidden_UnitCost"] = row["Unit_Cost"]
                    if row["CY_Quantity"] != "":
                        row["CY_CostPrice"] = str(float(row["CY_UnitCost"])*float(row["CY_Quantity"]))
                        row["Hidden_CostPrice"] = str(float(row["CY_UnitCost"])*float(row["CY_Quantity"]))
    validModelsCont.Calculate()