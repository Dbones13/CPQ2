def hideQuoteTableColumns(table, columns):
    for column in columns:
        table.GetColumnByName(column).AccessLevel = table.AccessLevel.Hidden

def editableQuoteTableColumn(table,column):
    table.GetColumnByName(column).AccessLevel = table.AccessLevel.Editable

def getCfValue(cfName):
    return Quote.GetCustomField(cfName).Content

def setCountryOfOrigin(quote_table):
    factory_mapping = {
            "Pune": "India",
            "Juarez": "Mexico",
            "Kassel": "Germany",
            "Tianjin": "China",
            "Delft": "Netherlands",
            "Roswell/ TruStop": "UnitedStates",
            "": "",
            "Thirdparty": "TBH",
            "Mainz-Kassel": "Germany",
            "Nebraska City": "United States",
            "Stara Tura": "Slovakia",
            "Lognes": "France",
            "Melton Mowbray": "United Kingdom",
            "Liege": "Belgium"
        }
    for row in quote_table.Rows:
        factory = row["Factory"]
        row["Country_of_Origin_1"] = factory_mapping.get(factory)

table=Quote.QuoteTables["Country_of_Origin"]
editableQuoteTableColumn(table,"PLSG")

columns_to_hide = ["Country_of_Origin", "PLSG_Desc", "Product_Line_Sub_Group"]
hideQuoteTableColumns(table, columns_to_hide)

if getCfValue("Booking LOB") == "PMC":
    setCountryOfOrigin(table)