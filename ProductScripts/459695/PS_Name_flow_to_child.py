sensor_cont = Product.GetContainerByName('MX_Sensor_Group')

if sensor_cont.Rows.Count > 0:
    for row in sensor_cont.Rows:
        sensor_name = row.Product.Attr('Sensor_Group_Name').GetValue()
        if str(row['Sensor_Name']) != sensor_name:
            row.Product.Attr('Sensor_Group_Name').AssignValue(str(row["Sensor_Name"]))
            row.ApplyProductChanges()