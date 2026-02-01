partsQty = {}
validPartsCon = Product.GetContainerByName("WTW_Cost_Value")

if validPartsCon.Rows.Count > 0:
    for row in validPartsCon.Rows:
        partsQty[row["Part Number"]] = [int(row["Quantity"]), int(row["WTW Cost"])]
    Trace.Write(RestClient.SerializeToJson(partsQty))

for item in Quote.Items:
    if item.PartNumber in partsQty:
        Trace.Write("3333"+ str(partsQty))
        item.Quantity = partsQty[item.PartNumber][0]
        item["QI_UnitWTWCost"].Value= partsQty[item.PartNumber][1]
        Trace.Write("222222"+ str(item["QI_UnitWTWCost"].Value))
Quote.Calculate()
Quote.Save()