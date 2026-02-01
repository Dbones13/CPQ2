import ProductUtil as pu

def addProjectManagment(row):
    msidProduct = row.Product
    productContainer = msidProduct.GetContainerByName('MSID_Product_Container')
    productvirhiddenContainer = msidProduct.GetContainerByName('MSID_Product_Container_Virtualization_hidden')
    productgenhiddenContainer = msidProduct.GetContainerByName('MSID_Product_Container_Generic_hidden')
    if row["Scope"] in ('LABOR','HWSWLABOR') and (productContainer.Rows.Count > 0 or productvirhiddenContainer.Rows.Count > 0 or productgenhiddenContainer.Rows.Count > 0):
        if not productContainer.Rows.GetByColumnName("Product Name","Project Management"):
            newRow = productContainer.AddNewRow("Project_Management_cpq", False)
            newRow['Product Name'] = "Project Management"
            newRow.ApplyProductChanges()
    elif row["Scope"] in ('HWSW'):
        if productContainer.Rows.GetByColumnName("Product Name","Project Management"):
            index = productContainer.Rows.GetByColumnName("Product Name","Project Management").RowIndex
            productContainer.DeleteRow(index)
            msidProduct.GetContainerByName('MSID_Labor_Project_Management').Clear()
            row.ApplyProductChanges()

def applyProductSelection(Product):
    msidContainer = Product.GetContainerByName('Migration_MSID_Selection_Container') if Product.Name == 'Migration' else Product.GetContainerByName('Migration_MSID_Selection_ContainerNew')
    selectedProducts = Product.Attr('Migration_Product_Choices').SelectedValues

    for row in msidContainer.Rows:
        if row.IsSelected:
            msidProduct = row.Product
            productContainer = msidProduct.GetContainerByName('MSID_Product_Container')
            for value in selectedProducts:
                if value.Display == "Virtualization System":
                    producthiddenContainer = msidProduct.GetContainerByName('MSID_Product_Container_Virtualization_hidden')
                    newRowVir = producthiddenContainer.AddNewRow('Virtualization_System_Migration_cpq')
                    newRowVir['Product Name'] = "Virtualization System"
                    newRowVir.ApplyProductChanges()
                    continue
                if value.Display == "Generic System":
                    producthiddenContainer = msidProduct.GetContainerByName('MSID_Product_Container_Generic_hidden')
                    newRowVir = producthiddenContainer.AddNewRow('Generic_System_Migration_cpq')
                    newRowVir['Product Name'] = "Generic System"
                    index = newRowVir.RowIndex + 1
                    newRowVir.Product.Attr('Generic_System_Migration_System_Name').AssignValue("Generic System " + str(index))
                    newRowVir.ApplyProductChanges()
                    continue
                newRow = productContainer.AddNewRow(value.ValueCode + '_cpq')
                newRow['Product Name'] = value.Display
                newRow.ApplyProductChanges()
                if value.Display == "FSC to SM":
                    producthiddenContainer = msidProduct.GetContainerByName('MSID_Product_Container_FSC_hidden')
                    newRowfsc = producthiddenContainer.AddNewRow('FSC_to_SM_Audit_cpq')
                    newRowfsc['Product Name'] = "FSC to SM Audit"
                    newRowfsc.ApplyProductChanges()
                if value.Display == "FSC to SM IO Migration":
                    producthiddenContainer = msidProduct.GetContainerByName('MSID_Product_Container_FSC_IO_hidden')
                    newRowfsc = producthiddenContainer.AddNewRow('FSC_to_SM_IO_Audit_cpq')
                    newRowfsc['Product Name'] = "FSC to SM IO Audit"
                    newRowfsc.ApplyProductChanges()
            addProjectManagment(row)
            con = msidProduct.GetContainerByName('MSID_CommonQuestions')
            newRow = con.AddNewRow()
            con.DeleteRow(newRow.RowIndex)
            productContainer.Calculate()
            msidProduct.ApplyRules()
            row.ApplyProductChanges()
    msidContainer.Calculate()
    pu.addMessage(Product , 'Products are successfully applied against the Selected MSID')


def resetColumnValue(container , columnName , oldValue , rowIndex):
    for row in container.Rows:
        if row.RowIndex == rowIndex:
            row[columnName] = str(oldValue)


def getFloat(n):
    try:
        return float(n)
    except:
        return 0


def validateWriteInsEntry(EventArgs , Product):
    container = EventArgs.Container
    changedCell = EventArgs.ChangedCell
    oldValue = changedCell.OldValue
    newValue = changedCell.NewValue
    changedColumn = changedCell.ColumnName
    rowIndex = changedCell.RowIndex
    if rowIndex in [0, 1]:
        val = getFloat(newValue)
        if newValue.ToString() != val.ToString():
            resetColumnValue(container , changedColumn , val , rowIndex)


def validateEntry(EventArgs , Product):
    container = EventArgs.Container
    changedCell = EventArgs.ChangedCell
    oldValue = changedCell.OldValue
    newValue = changedCell.NewValue
    changedColumn = changedCell.ColumnName
    rowIndex = changedCell.RowIndex

    try:
        query = "select Max_Limit,Min_Limit from OPM_ATTRIBUTE_LIMITDEFN where Cont_ColumnName = '{0}' and (Min_Limit > '{1}' or Max_Limit < '{1}')".format(changedColumn ,newValue)
        Trace.Write("Query = " +str(query))
        res = SqlHelper.GetFirst(query)

        if res:
            if newValue and res.Max_Limit and float(newValue) > float(res.Max_Limit):
                pu.addMessage(Product , 'Max value allowed is {}'.format(res.Max_Limit))
            elif newValue and res.Max_Limit and float(newValue) < float(res.Min_Limit):
                pu.addMessage(Product , 'Min value allowed is {}'.format(res.Min_Limit))
            #Log.Write("test 09 " + str(oldValue))
            resetColumnValue(container , changedColumn , oldValue , rowIndex)
            return False
    except:
        pass
    return True

def validateNodeEntry(EventArgs , Product):
    container = EventArgs.Container
    changedCell = EventArgs.ChangedCell
    oldValue = changedCell.OldValue
    newValue = changedCell.NewValue
    changedColumn = changedCell.ColumnName
    rowIndex = changedCell.RowIndex
    row1 = container.Rows[0]
    row2 = container.Rows[2]

    query = "select Max_Limit,Min_Limit from OPM_ATTRIBUTE_LIMITDEFN where Cont_ColumnName = '{0}' and (Min_Limit > {1} or Max_Limit < {1})".format(changedColumn ,newValue)
    res = SqlHelper.GetFirst(query)

    if res:
        if newValue and res.Max_Limit and float(newValue) > float(res.Max_Limit):
            pu.addMessage(Product , 'Max value allowed is {}'.format(res.Max_Limit))
        elif newValue and res.Max_Limit and float(newValue) < float(res.Min_Limit):
            pu.addMessage(Product , 'Min value allowed is {}'.format(res.Min_Limit))
        resetColumnValue(container , changedColumn , oldValue , rowIndex)

    if rowIndex == 2 and float(row1[changedColumn]) < float(newValue):
        Trace.Write("row1122 = " +str(row1[changedColumn]))
        resetColumnValue(container , changedColumn , oldValue , rowIndex)
        pu.addMessage(Product , 'Provided H/W to be replaced Value cannot be greater than Installed')
        return
    elif rowIndex == 0 and row2[changedColumn] and float(row2[changedColumn]) > float(newValue):
        resetColumnValue(container , changedColumn , oldValue , rowIndex)
        pu.addMessage(Product , 'Installed cannot be smaller than H/W To Be replaced')
        return

def getContainerDict(product):
    res = dict()
    for attr in product.Attributes:
        if attr.DisplayType == "Container":
            count = pu.getContainer(product , attr.Name).Rows.Count
            if count:
                res[attr.Name] = pu.getContainer(product , attr.Name).Rows[0]
    return res

def getMinMaxDict():
    resDict = dict()
    query = "SELECT * FROM OPM_ATTRIBUTE_LIMITDEFN"
    res = SqlHelper.GetList(query)

    for r in res:
        l = resDict.get(r.Container_Name , list())
        l.append((r.Cont_ColumnName , r.Min_Limit , r.Max_Limit))
        resDict[r.Container_Name] = l
    return resDict

def populateHeaders(product):
    containerDict = getContainerDict(product)
    minMaxDict = getMinMaxDict()
    for container , columns in minMaxDict.items():
        if container in containerDict:
            row = containerDict[container]
            for colData in columns:
                col = row.GetColumnByName(colData[0])
                if product.ParseString("<*CTX( Product.RootProduct.SystemId )*>") != 'Migration2_cpq' and col and not col.HeaderLabel.endswith("({} - {})".format(int(colData[1]) if str(type(colData[1])) != "<type 'DBNull'>" else 0, int(colData[2]) if str(type(colData[2])) != "<type 'DBNull'>" else 0)) and not col.HeaderLabel.endswith("({}-{})".format(int(colData[1]) if str(type(colData[1])) != "<type 'DBNull'>" else 0, int(colData[2]) if str(type(colData[2])) != "<type 'DBNull'>" else 0)) and col.Name != 'Graphics_Migration_For_existing_US_GUS_DSP_what_percentage_of_Standard_Builds_will_be_used?':
                    col.HeaderLabel = "{} ({} - {})".format(col.HeaderLabel , int(colData[1]) if str(type(colData[1])) != "<type 'DBNull'>" else 0, int(colData[2]) if str(type(colData[2])) != "<type 'DBNull'>" else 0)

#to get final quantity populated in parts summary tab
def getInt(Var):
    if Var:
        return int(Var)
    return 0

def PopulateFinalQuantity(EventArgs , Product):
    container = EventArgs.Container
    changedCell = EventArgs.ChangedCell
    oldValue = changedCell.OldValue
    newValue = changedCell.NewValue
    changedColumn = changedCell.ColumnName
    rowIndex = changedCell.RowIndex
    row = container.Rows[rowIndex]
    if changedColumn == 'Adj Quantity':
        if (row['PartNumber']).StartsWith('SVC'):
            row['Adj Quantity'] = '0'
            row['Final Quantity'] = str(int(float(row['Quantity']) + float(row['Adj Quantity'])))
        else:
            adj_quantity = 0 if row['Adj Quantity'] == '' else float(row['Adj Quantity'])
            row['Final Quantity'] = str(int(float(row['Quantity']) + adj_quantity))
            if (int(row['Final Quantity'])) < 0:
                row['Adj Quantity'] = '0'
                row['Final Quantity'] = str(int(float(row['Quantity'])))
            else:
                adj_quantity = 0 if row['Adj Quantity'] == '' else float(row['Adj Quantity'])
                row['Final Quantity'] = str(int(float(row['Quantity']) + adj_quantity))
                                  
def setLastDefaultValue(Product,defaultValDict):
    VSContainer = Product.GetContainerByName('Virtualization_System_WorkLoad_Cont')
    count =VSContainer.Rows.Count
    rows =VSContainer.Rows
    for row in rows:
        rowindex=row.RowIndex+1
        if count == rowindex:
            VSDefDict={0:{'Work_Load_Name':'WorkLoad-'+str(count)+'','Cluster_Name':'Default','Work_Load_Type':'-','Number':'0'}}
            for col in row.Columns:
                valData = defaultValDict.get(col.Name)
                if col.Name in ('Work_Load_Type','Cluster_Name','Work_Load_Name', 'Number'):
                    value = VSDefDict[0][col.Name]
                    colType = col.DisplayType.upper()
                    if col.Name == 'Work_Load_Type':
                        row.Product.Attr('VS_WorkLoadType').SelectDisplayValue(value)
                else:
                    if valData is None :
                        continue
                    value = valData[0]
                    colType = valData[1]
                if colType == 'DROPDOWN':
                    col.SetAttributeValue(value)
                elif colType == 'TEXTBOX':
                    row.SetColumnValue(col.Name,value)
                elif colType == 'PRODATTR':
                    row.Product.Attr(col.Name).SelectDisplayValue(value)
                    row.ApplyProductChanges()
                if col.Name == "xPM_Migration_Scenario":
                    defaultMigScenario = checkDefaultMigrationScenario(product)
                    if defaultMigScenario :
                        row.Product.Attr(col.Name).SelectDisplayValue(defaultMigScenario)
                        row.ApplyProductChanges()
                row.Calculate()                                                                                                                                              

def  checkDefaultMigrationScenario(product):
    defaultMigScenario = ''
    if product.Name == 'MSID':
        migSelectionContainer = product.GetContainerByName('xPM_Migration_Scenario_Cont')
        row = migSelectionContainer.Rows[0]
        migrationScenario = row['xPM_Select_the_migration_scenario']    
    else:
        migrationScenario = product.Attr('xPM_Select_the_migration_scenario').GetValue()
    if migrationScenario == "xPM to EHPM":
        defaultMigScenario = "UPG PM/APM TO 7-SLOT EHPM Non RED With IOL"
    elif migrationScenario == "xPM to C300PM":
        defaultMigScenario = "Non-redundant PM/APM to C300PM in 7-slot chassis"
    elif migrationScenario == "xPM to EHPMX":
        defaultMigScenario = "Non-redundant PM/APM to EHPMX in 7-slot chassis"
    return defaultMigScenario

def setDefaultValue(product, configContainer, row, defaultValDict):
    rowIndicate = row.RowIndex+1
    VSDefDict = {1:{'Work_Load_Name':'vCenter','Cluster_Name':'Mgmt','Work_Load_Type':'vCenter Server', 'Number':'1'}, 2:{'Work_Load_Name':'vSphere Client','Cluster_Name':'Mgmt','Work_Load_Type':'vSphere Client', 'Number':'1',}, 3:{'Work_Load_Name':'Mgmt DC','Cluster_Name':'Mgmt','Work_Load_Type':'Domain Controller (Mgmt)', 'Number':'1'}, 4:{'Work_Load_Name':'Backup Manager EBR','Cluster_Name':'Mgmt','Work_Load_Type':'EBR Manager Server', 'Number':'1'}, 5:{'Work_Load_Name':'Backup Agent','Cluster_Name':'Mgmt','Work_Load_Type':'EBR Virtual Edition Agent', 'Number':'1'}, 0:{'Work_Load_Name':'WorkLoad-'+str(rowIndicate)+'','Cluster_Name':'Default','Work_Load_Type':'-','Number':'0'}}
    for col in row.Columns:
        valData = defaultValDict.get(col.Name)
        if col.Name in ('Work_Load_Type','Cluster_Name','Work_Load_Name', 'Number'):
            value = VSDefDict[rowIndicate][col.Name] if rowIndicate <= 5 else VSDefDict[0][col.Name]
            colType = col.DisplayType.upper()
            if col.Name == 'Work_Load_Type':
                row.Product.Attr('VS_WorkLoadType').SelectDisplayValue(value)
        else:
            if valData is None :
                continue
            value = valData[0]
            colType = valData[1]
        if colType == 'DROPDOWN':
            col.SetAttributeValue(value)
        elif colType == 'TEXTBOX':
            row.SetColumnValue(col.Name,value)
        elif colType == 'PRODATTR':
            row.Product.Attr(col.Name).SelectDisplayValue(value)
            row.ApplyProductChanges()
        if col.Name == "xPM_Migration_Scenario":
            defaultMigScenario = checkDefaultMigrationScenario(product)
            if defaultMigScenario :
                row.Product.Attr(col.Name).SelectDisplayValue(defaultMigScenario)
                row.ApplyProductChanges()
        if col.Name == 'Thin_Client_Requirements':
            if str(col.Value) =="":
                product.ParseString('<*CTX( Container({}).Row({}).Column({}).Set({}) )*>'.format("Virtualization_System_WorkLoad_Cont", rowIndicate,col.Name,"No"))
        if col.Name == 'Redundant':
            if str(col.Value) =="":
                product.ParseString('<*CTX( Container({}).Row({}).Column({}).Set({}) )*>'.format("Virtualization_System_WorkLoad_Cont", rowIndicate,col.Name,"No"))
        if col.Name == 'Release':
            if str(col.Value) =="":
                product.ParseString('<*CTX( Container({}).Row({}).Column({}).Set({}) )*>'.format("Virtualization_System_WorkLoad_Cont", rowIndicate,col.Name,"All"))
        if col.Name == 'Fault_Tolerance':
            if str(col.Value) =="":
                product.ParseString('<*CTX( Container({}).Row({}).Column({}).Set({}) )*>'.format("Virtualization_System_WorkLoad_Cont", rowIndicate,col.Name,"No"))
        if col.Name == 'Replicate':
            if str(col.Value) =="":
                product.ParseString('<*CTX( Container({}).Row({}).Column({}).Set({}) )*>'.format("Virtualization_System_WorkLoad_Cont", rowIndicate,col.Name,"No"))
        row.Calculate()


def getMigrationDefaultValueDict():
    query = "select * from MIGRATION_DEFAULTS"
    res = SqlHelper.GetList(query)

    resDict = dict()
    for r in res:
        resDict[r.COLUMN_NAME] = [r.DEFAULT_VALUE, r.COLUMN_TYPE]
    return resDict

def updateContainerTable(Product, container, configContainer, newValue):
    defaultValDict = getMigrationDefaultValueDict()
    listToDeleted = []
    if configContainer is not None:
        containerRows = configContainer.Rows.Count
        if newValue == 0:
            configContainer.Rows.Clear()
        elif containerRows > newValue:
            i = 1
            for row in configContainer.Rows:
                if i > newValue:
                    listToDeleted.append(row.RowIndex)
                i += 1
        elif containerRows < newValue:
            newRows =  newValue - containerRows
            while newRows > 0:
                row = configContainer.AddNewRow()
                setDefaultValue(Product, configContainer, row, defaultValDict)
                newRows -= 1
            configContainer.Calculate()
    listToDeleted.sort(reverse=True)
    if len(listToDeleted) > 0:
        for rowIndex in listToDeleted:
            configContainer.DeleteRow(rowIndex)
    

def chkEmptyVS(Product):
    VSContainer = Product.GetContainerByName('Virtualization_System_WorkLoad_Cont')
    emptyNumber = ''
    emptyType = ''
    for row in VSContainer.Rows:
        for col in row.Columns:
            if col.Value in ('','0') and col.Name == 'Number':
                emptyNumber = emptyNumber + str(row.RowIndex+1) +', '
            if col.DisplayValue == '-' and col.Name == 'Work_Load_Type':
                emptyType = emptyType + str(row.RowIndex+1) +', '
    Product.SetGlobal('Number_Missing', emptyNumber[:-2])
    Product.SetGlobal('Type_Missing', emptyType[:-2])

def VSAddRow(Product,count,isR2QRequest=None):
    configContainer = Product.GetContainerByName('Virtualization_System_WorkLoad_Cont')
    updateContainerTable(Product,'',configContainer,count)
    if Product.Name == 'Virtualization System Migration' and isR2QRequest == 'Yes':
        defaultValDict = getMigrationDefaultValueDict()
        setLastDefaultValue(Product,defaultValDict)
        chkEmptyVS(Product)

def populateContainer(EventArgs , Product):
    container = EventArgs.Container
    changedCell = EventArgs.ChangedCell
    oldValue = changedCell.OldValue
    newValue = changedCell.NewValue
    changedColumn = changedCell.ColumnName
    rowIndex = changedCell.RowIndex
    configContainer = None
    listToDeleted = []
    newValue = int(newValue)
    if container.Name == 'xPM_Migration_General_Qns_Cont' and changedColumn == 'xPM_How_many_xPMs_configurations_are_we_migrating' and newValue <=20:
        configContainer = Product.GetContainerByName('xPM_Migration_Config_Cont')
        updateContainerTable(Product, container, configContainer, newValue)
    elif container.Name == 'ENB_Migration_General_Qns_Cont' and changedColumn == 'xPM_Number_of_NIMs_configurations_to_be_migrated' and newValue <=10:
        configContainer = Product.GetContainerByName('ENB_Migration_Config_Cont')
        updateContainerTable(Product, container, configContainer, newValue)
    elif container.Name == 'C200_Migration_General_Qns_Cont' and changedColumn == 'C200_How_many_C200s_are_we_migrating' and newValue <=20:
        configContainer = Product.GetContainerByName('C200_Migration_Config_Cont')
        updateContainerTable(Product, container, configContainer, newValue)
    elif container.Name == 'xPM_C300_General_Qns_Cont' and changedColumn == 'xPM_C300_Number_of_xPMs_to_be_Migrated_to_C300_with_PMIO' and newValue <=90:
        configContainer = Product.GetContainerByName('xPM_C300_Migration_Configuration_Cont')
        updateContainerTable(Product, container, configContainer, newValue)
    elif container.Name == 'FSC_to_SM_General_Information' and changedColumn == 'FSC_to_SM_Number_of_configurations_to_be_migrated' and newValue <=10:
        Trace.Write("Here inside GS 1111")
        configContainer = Product.GetContainerByName('FSC_to_SM_Configuration')
        updateContainerTable(Product, container, configContainer, newValue)
    elif container.Name == 'FDM_Upgrade_General_questions' and changedColumn == 'FDM_Upgrade_Additional_Components_to_be_offered_for_number_of_FDMs_?' and newValue <=3:
        configContainer = Product.GetContainerByName('FDM_Upgrade_Additional_Configuration')
        updateContainerTable(Product, container, configContainer, newValue)
    elif container.Name == 'LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont' and changedColumn == 'LM_Qty_Of_LM_Pair_To_Be_Migrated' and newValue <=20:
        configContainer = Product.GetContainerByName('LM_to_ELMM_ControlEdge_PLC_Cont')
        updateContainerTable(Product, container, configContainer, newValue)
        configContainer = Product.GetContainerByName('LM_to_ELMM_ControlEdge_PLC_Local_IO_Cont')
        updateContainerTable(Product, container, configContainer, newValue)
        configContainer = Product.GetContainerByName('LM_to_ELMM_ControlEdge_PLC_Remote_IO_Cont')
        updateContainerTable(Product, container, configContainer, newValue)
        configContainer = Product.GetContainerByName('LM_to_ELMM_Migration_Additional_IO_Cont')
        updateContainerTable(Product, container, configContainer, newValue)