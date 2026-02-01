IO_Section_query = SqlHelper.GetList("select IO_Section from IO_Section_of_PlantCruise_Group")
IO_Section_container =  Product.GetContainerByName('PlantCruise_IO_Section_of_PlantCruise_Group')
for row in IO_Section_query:
    new_row=IO_Section_container.AddNewRow(False)
    new_row['IO_Section'] = row.IO_Section
    new_row['IO_Point_Required'] = '0'
    new_row['Modules_Configured'] = '0'
    new_row['IO_Point_Configured'] = '0'
IO_Section_container.Calculate()