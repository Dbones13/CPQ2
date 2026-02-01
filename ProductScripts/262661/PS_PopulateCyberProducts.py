cyberPartCon = Product.GetContainerByName("Cyber_Parts_Container")
addcyberPartCon = Product.GetContainerByName("Add_Cyber_Parts_Container")
cyberPartCon.Rows.Clear()

def resetAttr(name):
    Product.DisallowAttr(name)
    Product.AllowAttr(name)

selectedVC = dict()
for row in addcyberPartCon.Rows:
    item = Quote.GetItemByUniqueIdentifier(row.UniqueIdentifier)
    if row.IsSelected and item:
        row["Quantity"] = str(item.Quantity)
        selectedVC[row["Product"]] = row["Quantity"]

resetAttr("VC_SearchByVCModel")
resetAttr("VC_SearchByDescription")

def populateCyberParts(part):
    Row = cyberPartCon.AddNewRow()
    Row["Product"] = part.PartNumber
    Row["Description"] = part.Product_Name
    Row["Quantity"] = "1"

    qty = selectedVC.get(Row["Product"])
    if qty:
        Row.IsSelected = True
        Row["Quantity"] = qty
PLSG=[]
query = ("select H.PartNumber,H.PLSG,P.Product_Name from HPS_PRODUCTS_MASTER as H join Products as P on H.PartNumber= P.PRODUCT_CATALOG_CODE  where H.PLSG in ('7754-7000','7734-7000','7754-7F44','7734-7F43','7734-7F45','7734-G471','7734-Y381','G451-Y943','7754-Y868','7734-Y869','G451-Y510','G451-Y859','G451-Y857','G451-Y858','G451-Y952') OR (H.PLSG in ('7073-7272','7681-7B35','7073-7733','7681-7B37','7073-7732','7681-7B36') and H.PartNumber like 'SVC%')")

cyberPartsData = SqlHelper.GetList(query)

if cyberPartsData is not None:
    for part in cyberPartsData:
        populateCyberParts(part)