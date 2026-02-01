rowsDict = [
    {"SignalType" : "Non HART Analog Inputs(4-20mA / 1-5V)" , "IOModuleModel":"CC-PAIH01"},
    {"SignalType" : "HART Analog Inputs(4-20mA / 1-5V)" , "IOModuleModel":"CC-PAOH01"},
    {"SignalType" : "Non HART Analog Outputs(4-20mA)" , "IOModuleModel":"CC-xxxxx"},
    {"SignalType" : "HART Analog Outputs(4-20mA)" , "IOModuleModel":"CC-xxxxx"},
    {"SignalType" : "Digital Inputs (24VDC)" , "IOModuleModel":"CC-vvvvvvv"},
    {"SignalType" : "Digital Outputs (24VDC)" , "IOModuleModel":"CC-vvvvvvv"},
    {"SignalType" : "Pulse Inputs(5-10V}, 0 to 10 kHz)" , "IOModuleModel":"CC-vvvvvvv"},
    {"SignalType" : "Field ISA 100 Wireless devices" , "IOModuleModel":"CC-vvvvvvv"}
]
countsContainer = Product.GetContainerByName("IO Counts")
if countsContainer.Rows.Count == 0:
    for rowData in rowsDict:
        row = countsContainer.AddNewRow()
        row["SignalType"] = rowData["SignalType"]
        row["IOModuleModel"] = rowData["IOModuleModel"]

Product.GetContainerByName('RTU Field container').AddNewRow(False)
Product.GetContainerByName('RTU Software Field container').AddNewRow(False)