if Product.Name != "Service Contract Products":
    scopesummary_ent = Product.GetContainerByName('SC_ScopeSummary_entitlement_cont')
    scopesummary_ent.Rows.Clear()
    scopesummary_ent_hidden = Product.GetContainerByName('SC_TPS_RC_Entitlements_Scope_summary_hidden')
    attr_sel = Product.Attr("SC_TPS_RC_Selection").SelectedValues
    if scopesummary_ent_hidden.Rows.Count:
        for row in scopesummary_ent_hidden.Rows:
            for value in attr_sel:
                if value.Display == row["Comments"]:
                    scopesummary_entRow = scopesummary_ent.AddNewRow(False)
                    scopesummary_entRow['Entitlement'] = row['Entitlement']
                    scopesummary_entRow['3rd_Party_Models'] = row['3rd_Party_Models']
                    scopesummary_entRow['Description'] = row['Description']
                    scopesummary_entRow['PY_Quantity'] = row['PY_Quantity']
                    scopesummary_entRow['Quantity'] = row['Quantity']
                    scopesummary_entRow['PY_ListPrice'] = row['PY_ListPrice']
                    scopesummary_entRow['HW_ListPrice'] = row['HW_ListPrice']
                    scopesummary_entRow['SA_Price'] = row['SA_Price']
                    scopesummary_entRow['SR_Price'] = row['SR_Price']
                    scopesummary_entRow['Comments'] = row['Comments']