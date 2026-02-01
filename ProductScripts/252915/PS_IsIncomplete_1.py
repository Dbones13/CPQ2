def getContainer(containerName):
     return Product.GetContainerByName(containerName)
def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def getAttributeValue(Name):
    return Product.Attr(Name).GetValue()

def setAttrValue(Name,value):
    Product.Attr(Name).AssignValue(value)
selectedProducts = Product.Attr('MSID_Selected_Products').GetValue().split('<br>')
incomplete1 = []
if 'FSC to SM IO Migration' in selectedProducts:
    confscio = getContainer("FSC_to_SM_IO_Migration_General_Information")
    check = getFloat(confscio.Rows[0]["FSC_to_SM_IO_Migration_Total_FSC_SM_Systems"])
    flagFscRed = flagFscNonRed = 0
    if check > 0:
        for row in getContainer("FSC_to_SM_IO_Series_1_&_2_FSC_IO_configurations").Rows:
            if getFloat(row["FSC_to_SM_IO_Quantity_of_Cabinets_containing_IO_Rack"]) > 0:
                NonRed = getFloat(row["NON_RED_FSC_to_SM_IO_DI_24VDC"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DI_60VDC"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DI_48VDC"]) + getFloat(row["NON_RED_FSC_to_SM_IO_AI_4_20mA"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DI_IS_(Eex(i))"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DI_IS_(Eex(ii))"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DI_24VDC_10104/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DO 24VDC_10201/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_FDO_DS_24VDC_10203/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_FDO_DS_24VDC_10203/1/2"]) + getFloat(row["NON_RED_FSC_to_SM_IO_AO_4-20mA_10205/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DO_24VDC_10206/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DO_IS_10207/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_RO_10208/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DO_24VDC_10209/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DO_24VDC_10212/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DO_110VDC_10213/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDO_60VDC_10213/1/2"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SD_ 48VDC_10213/1/3"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDOL 220VDC_10214/1/2"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDO_24VDC_10215/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDOL_24VDC_10216/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDI_24VDC"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDI_60VDC_10101/2/2"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDI_48VDC_10101/2/3"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SAI_10102/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DI_24VDC_10104/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_AI_10105/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDIL_10106/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDO_24VDC_10201/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SAO_10205/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DO_24VDC_10206/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_RO_10208/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DO_24VDC_10209/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDO_110VDC_10213/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDO_60VDC_10213/2/2"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDO_48VDC_10213/2/3"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDOL_220VDC_10214/2/2"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDO_24VDC_10215/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDOL_24VDC_10216/2/1"])
                Red = getFloat(row["FSC_to_SM_IO_DI_24VDC"]) + getFloat(row["FSC_to_SM_IO_DI_60VDC"]) + getFloat(row["FSC_to_SM_IO_DI_48VDC"]) + getFloat(row["FSC_to_SM_IO_AI_4_20mA"]) + getFloat(row["FSC_to_SM_IO_DI_IS_(Eex(i))"]) + getFloat(row["FSC_to_SM_IO_DI_IS_(Eex(ii))"]) + getFloat(row["FSC_to_SM_IO_DI_24VDC_10104/1/1"]) + getFloat(row["FSC_to_SM_IO_DO 24VDC_10201/1/1"]) + getFloat(row["FSC_to_SM_IO_FDO_DS_24VDC_10203/1/1"]) + getFloat(row["FSC_to_SM_IO_FDO_DS_24VDC_10203/1/2"]) + getFloat(row["FSC_to_SM_IO_AO_4-20mA_10205/1/1"]) + getFloat(row["FSC_to_SM_IO_DO_24VDC_10206/1/1"]) + getFloat(row["FSC_to_SM_IO_DO_IS_10207/1/1"]) + getFloat(row["FSC_to_SM_IO_RO_10208/1/1"]) + getFloat(row["FSC_to_SM_IO_DO_24VDC_10209/1/1"]) + getFloat(row["FSC_to_SM_IO_DO_24VDC_10212/1/1"]) + getFloat(row["FSC_to_SM_IO_DO_110VDC_10213/1/1"]) + getFloat(row["FSC_to_SM_IO_SDO_60VDC_10213/1/2"]) + getFloat(row["FSC_to_SM_IO_SD_ 48VDC_10213/1/3"]) + getFloat(row["FSC_to_SM_IO_SDOL 220VDC_10214/1/2"]) + getFloat(row["FSC_to_SM_IO_SDO_24VDC_10215/1/1"]) + getFloat(row["FSC_to_SM_IO_SDOL_24VDC_10216/1/1"]) + getFloat(row["FSC_to_SM_IO_SDI_24VDC"]) + getFloat(row["FSC_to_SM_IO_SDI_60VDC_10101/2/2"]) + getFloat(row["FSC_to_SM_IO_SDI_48VDC_10101/2/3"]) + getFloat(row["FSC_to_SM_IO_SAI_10102/2/1"]) + getFloat(row["FSC_to_SM_IO_DI_24VDC_10104/2/1"]) + getFloat(row["FSC_to_SM_IO_AI_10105/2/1"]) + getFloat(row["FSC_to_SM_IO_SDIL_10106/2/1"]) + getFloat(row["FSC_to_SM_IO_SDO_24VDC_10201/2/1"]) + getFloat(row["FSC_to_SM_IO_SAO_10205/2/1"]) + getFloat(row["FSC_to_SM_IO_DO_24VDC_10206/2/1"]) + getFloat(row["FSC_to_SM_IO_RO_10208/2/1"]) + getFloat(row["FSC_to_SM_IO_DO_24VDC_10209/2/1"]) + getFloat(row["FSC_to_SM_IO_SDO_110VDC_10213/2/1"]) + getFloat(row["FSC_to_SM_IO_SDO_60VDC_10213/2/2"]) + getFloat(row["FSC_to_SM_IO_SDO_48VDC_10213/2/3"]) + getFloat(row["FSC_to_SM_IO_SDOL_220VDC_10214/2/2"]) + getFloat(row["FSC_to_SM_IO_SDO_24VDC_10215/2/1"]) + getFloat(row["FSC_to_SM_IO_SDOL_24VDC_10216/2/1"]) + getFloat(row["FSC_to_SM_IO_SDOL_48VDC_10216/2/3"])
                if getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) == 0 and Red>0:
                    flagFscRed += 1
                if getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"]) == 0 and NonRed>0:
                    flagFscNonRed += 1

    if flagFscRed > 0:
        incomplete1.append("flagFscRed")
    if flagFscNonRed > 0:
        incomplete1.append("flagFscNonRed")

Product.Attr('Incomplete1').AssignValue(",".join(incomplete1))