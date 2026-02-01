container = Product.GetContainerByName("CE_SystemGroup_Cont")
systems = set()
for row in container.Rows:
    systems.update(row["Selected_Products"].split("<br>"))
Product.Attr("CE_Unique_Selected_Systems").AssignValue('|'.join(systems))