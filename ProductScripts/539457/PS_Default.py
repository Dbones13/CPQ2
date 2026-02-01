if Product.Name == "Virtualization System":
    import GS_Labor_Utils
    labor_cont = Product.GetContainerByName('Virtualization_Additional_Custom_Deliverables')
    if labor_cont.Rows.Count == 0:
        labor_cont.AddNewRow(False)
    row = labor_cont.Rows[0]
    attr = row.GetColumnByName("FO Eng").SetAttributeValue("SYS LE1-Lead Eng")
    row["FO Eng"] = "SYS LE1-Lead Eng"
    row["Execution Year"] = str(DateTime.Now.Year)
    row["Execution Country"] = GS_Labor_Utils.getExecutionCountry(Quote)
    if Product.Attr('Virtualization_Number_of_Clusters_in_the_network').GetValue() == '':
        Product.Attr('Virtualization_Number_of_Clusters_in_the_network').AssignValue('0')
    labor_cont.Calculate()