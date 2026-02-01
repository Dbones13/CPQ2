# Initialize a dictionary to store the counts for each category
counts = {
    "C300_controlerrequred300_for_proposal": 0,
    "C300_controler_100_for_proposal": 0,
    "C300_100controlerrequred300_for_proposal": 0,
    "C300_Contro_vertual_for_proposal": 0,
    "C300_contro_physical_for_proposal": 0,
    "C300_universal_marshling_for_proposal": 0,
    "C300_IO_FamilY1_for_proposal": 0,
    "C300_IO_FamilY2_for_proposal": 0,
    "IO_Family_document": 0,
    "Foundation_Fieldbus_document": 0,
    "Profibus_Gateway_Interface_document": 0,
    "Ethernet_Interface_document": 0,
    "PM_IO_Solution_required_document": 0
}

cont = Product.GetContainerByName("CE_SystemGroup_Cont")
for row in cont.Rows:
    for key in counts:
        if int(row[key]) > 0:
            counts[key] += 1
for key, value in counts.items():
    Product.Attr(key).AssignValue(str(value))