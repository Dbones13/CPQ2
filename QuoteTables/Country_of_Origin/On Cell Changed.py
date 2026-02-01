def hideQuoteTableColumn(table,column):
    table.GetColumnByName(column).AccessLevel = table.AccessLevel.Hidden

def editableQuoteTableColumn(table,column):
    table.GetColumnByName(column).AccessLevel = table.AccessLevel.Editable

CountryofOriginTable=Quote.QuoteTables["Country_of_Origin"]
hideQuoteTableColumn(CountryofOriginTable,"Country_of_Origin")
hideQuoteTableColumn(CountryofOriginTable,"Product_Line_Sub_Group")
hideQuoteTableColumn(CountryofOriginTable,"PLSG_Desc")
editableQuoteTableColumn(CountryofOriginTable,"PLSG")

city_country_mapdict={"Pune":"India","Juarez":"Mexico","Kassel":"Germany","Tianjin":"China","Delft":"Netherlands","Roswell/ TruStop":"UnitedStates","":"","Thirdparty":"TBH","Mainz-Kassel":"Germany","Nebraska City":"United States","Stara Tura":"Slovakia","Lognes":"France","Melton Mowbray":"United Kingdom","Liege":"Belgium"}

for row in CountryofOriginTable.Rows:
    row["Country_of_Origin_1"] = city_country_mapdict.get(row["Factory"])