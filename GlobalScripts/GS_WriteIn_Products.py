from GS_PrdUpldCommon import fnEscpUniode
class writein_product_upload():
    def __init__(self, quote, pproduct, wrkbook):
        self.quote = quote
        self.prduct = pproduct
        Trace.Write("Write-In Product")
        self.cells = wrkbook.GetSheet("Write In").Cells
        self.TotalRows = self.cells.GetRowCount
        self.end = wrkbook.GetSheet("Write In").Cells.GetLastColumnPosition + str(self.TotalRows)
        self.data = wrkbook.GetSheet("Write In").Cells.GetRange("A1", self.end)
        self.validPartsCon = self.prduct.GetContainerByName("WriteInProduct")
        self.invalidPartsCon = self.prduct.GetContainerByName("WriteIn_Invalid_Parts")

        self.write_in_upload()

    def getWriteInProductInfo(self, writeInPartNumber):
        writeInProduct = SqlHelper.GetFirst("SELECT Description, ProductLine, ProductLineDescription, ProductLineSubGroupDescription, ProductLineSubGroup, UnitofMeasure from WriteInProducts(nolock) where Product = '"+writeInPartNumber+"'")
        # if writeInProduct is not None:
        #     return writeInProduct
        return writeInProduct


    def PopulateChildProduct(self, containerRow,category):
        containerRow.Product.Attributes.GetByName("Writein_Category").SelectValue(category)
        containerRow.Product.Attributes.GetByName("Selected_WriteIn").AssignValue(str(containerRow["Selected_WriteIn"]))
        #containerRow.Product.Attributes.GetByName("WriteInProductsChoices").SelectDisplayValue(str(containerRow["WriteInProducts"]))
        containerRow.Product.Attributes.GetByName("ItemQuantity").AssignValue(str(containerRow["ItemQuantity"]))
        containerRow.Product.Attributes.GetByName("Extended Description").AssignValue(containerRow["ExtendedDescription"])
        #containerRow.Product.Attributes.GetByName("Extended Description").AssignValue(str(containerRow["ExtendedDescription"]))
        containerRow.Product.Attributes.GetByName("Price").AssignValue(str(containerRow["Price"]))
        containerRow.Product.Attributes.GetByName("cost").AssignValue(str(containerRow["Cost"]))
        #containerRow.Product.Attributes.GetByName("Description").AssignValue(str(containerRow["Description"]))
        containerRow.Product.Attributes.GetByName("Description").AssignValue(containerRow["Description"])
        containerRow.Product.Attributes.GetByName("Product Line").AssignValue(str(containerRow["Product Line"]))
        containerRow.Product.Attributes.GetByName("Product Line Description").AssignValue(str(containerRow["Product Line Description"]))
        containerRow.Product.Attributes.GetByName("Product line sub group").AssignValue(str(containerRow["Product Line Sub Group"]))
        containerRow.Product.Attributes.GetByName("PLSG description").AssignValue(str(containerRow["PLSG Description"]))
        containerRow.Product.Attributes.GetByName("Unit of Measure").AssignValue(str(containerRow["Unit of Measure"]))
        containerRow.Product.Attributes.GetByName("LCM_WriteIn_Year").AssignValue(str(containerRow["Year"]))
        containerRow.Product.Attributes.GetByName("LCM_WriteIn_Area").AssignValue(str(containerRow["Area"]))


    def PopulateValidPartsCon(self, category,partNumber, quantity, extendedDescription, unitListPrice, unitRegionalCost, writeInProductInfo,Area, Year):
        try:
            containerRow = self.validPartsCon.AddNewRow('WriteIn_cpq')
            containerRow.GetColumnByName('Category').SetAttributeValue(category)
            containerRow["Selected_WriteIn"]     = partNumber
            containerRow["ItemQuantity"]        = quantity
            containerRow["ExtendedDescription"] = extendedDescription
            containerRow["Price"]               = unitListPrice
            containerRow["Cost"]                = unitRegionalCost
            containerRow["Description"]			= writeInProductInfo.Description
            containerRow["Product Line"]		= writeInProductInfo.ProductLine
            containerRow["Product Line Description"] = writeInProductInfo.ProductLineDescription
            containerRow["Product Line Sub Group"] 	 = writeInProductInfo.ProductLineSubGroup
            containerRow["PLSG Description"]	= writeInProductInfo.ProductLineSubGroupDescription
            containerRow["Unit of Measure"]		= writeInProductInfo.UnitofMeasure
            containerRow["Year"]                = Year
            containerRow["Area"]                = Area
            self.PopulateChildProduct(containerRow,category)
            #Log.Info("{},{},{},{},{},{}".format(containerRow["Description"],containerRow["Product Line"],containerRow["Product Line Description"],containerRow["Product Line Sub Group"],containerRow["PLSG Description"],containerRow["Unit of Measure"]))
            containerRow.Product.ApplyRules()
            containerRow.ApplyProductChanges()
            # containerRow.Calculate()
        except Exception as e:
            Log.Error("WriteIn:: Valid Parts Exception: {}".format(str(e)))
    
    
    def PopulateInValidCon(self, partNumber, quantity, extendedDescription, unitListPrice, unitRegionalCost, message):
        try:
            row = self.invalidPartsCon.AddNewRow(False)
            #Trace.Write("quantity" + str(quantity))
            row["Write In Part Number"]     = partNumber
            row["Quantity"]                 = quantity
            row["Extended Description"]     = extendedDescription
            row["Unit List Price"]          = unitListPrice
            row["Unit Regional Cost"]       = unitRegionalCost
            row["Message"]                  = message
        except Exception as e:
            Log.Error("WriteIn:: Invalid Parts Exception: {} at line {}".format(sys.exc_info()[-1].tb_lineno, str(e)))
    
    def write_in_upload(self):
        try:
            sheet_data = fnEscpUniode(self.data,self.TotalRows,6)
            for i in range(1,self.TotalRows):
                empty_col = 0
                for col_index in range(0,10):
                    if sheet_data[i,col_index].strip() == '':
                        empty_col += 1
                if empty_col < 10:
                    category            = sheet_data[i,0].strip().encode('unicode_escape') if sheet_data[i,0] else ''
                    partNumber          = sheet_data[i,1].strip().encode('unicode_escape')
                    quantity            = sheet_data[i,2] if sheet_data[i,2] else '0'
                    extendedDescription = sheet_data[i,3].strip().encode('unicode_escape') if sheet_data[i,3] else ''
                    #Log.Write("extendedDescriptiontest" +  extendedDescription)
                    
                    unitListPrice       = sheet_data[i,4] if sheet_data[i,4] else '0'
                    unitRegionalCost    = sheet_data[i,5] if sheet_data[i,5] else '0'
                    Area                = sheet_data[i,8] if sheet_data[i,8] else '0'
                    Year                = sheet_data[i,9] if sheet_data[i,9] else '0'
                    message = ""
                    if partNumber != "":
                        writeInProductInfo = self.getWriteInProductInfo(partNumber)
                        if writeInProductInfo is not None:
                            WriteIn_LP_VAL = SqlHelper.GetFirst("Select MinimumListPrice, MaximumListPrice from WriteIn_ListPriceValidation(nolock) where Product ='"+ partNumber +"'")
                            if WriteIn_LP_VAL is not None:
                                #Gas WriteIn product
                                if float(unitListPrice) > float(WriteIn_LP_VAL.MinimumListPrice) and float(unitListPrice) <= float(WriteIn_LP_VAL.MaximumListPrice):
                                #Gas WriteIn product List price in min and max range
                                    self.PopulateValidPartsCon(category,partNumber, quantity, extendedDescription, unitListPrice, unitRegionalCost, writeInProductInfo, Area, Year)
                                else:
                                #Gas WriteIn product List price not in min and max range
                                    message = "List price not in range"
                                    #PopulateInValidCon(partNumber, quantity, extendedDescription, unitListPrice, unitRegionalCost, message)
                            else:
                            #Not Gas WriteIn product
                                self.PopulateValidPartsCon(category,partNumber, quantity, extendedDescription, unitListPrice, unitRegionalCost, writeInProductInfo,Area, Year)
                        else:
                            message = "This is not a Valid Write-In"
                    else:
                        message = "Write In Part Number is empty"
                    if message != "":
                        self.PopulateInValidCon(partNumber, quantity, extendedDescription, unitListPrice, unitRegionalCost, message)
        except Exception as e:
            Log.Error("WriteIn:: Exception: {}".format(str(e)))
        self.validPartsCon.MakeAllRowsSelected()
        # validPartsCon.Calculate()