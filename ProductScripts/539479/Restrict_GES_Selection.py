non_editable_ges_deliverables = ["C300 User Requirement Specification", "C300 Engineering Plan", "C300 Customer Training", "C300 Procure Materials & Services"]
con = Product.GetContainerByName("C300_Engineering_Labor_Container")

for row in con.Rows:
    if row["Deliverable"] in non_editable_ges_deliverables:
        row.Product.DisallowAttrValues("C300 GES Eng", "HPS_GES_P350F_UZ", "HPS_GES_P350B_UZ", "HPS_GES_P350F_RO", "HPS_GES_P350B_RO", "HPS_GES_P350F_IN", "HPS_GES_P350B_IN", "HPS_GES_P350F_CN", "HPS_GES_P350B_CN")
        row.ApplyProductChanges()
con.Calculate()