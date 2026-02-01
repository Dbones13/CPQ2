import System.Decimal as D

def get_mcar(Product,IOTANR,IOTAR,parts_dict):
    #CXCPQ-31175
    iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue
    MCAR=D.Ceiling((IOTANR/3)+(IOTAR/2))
    if iota == "RUSIO":
        parts_dict["FC-MCAR-02"] = {'Quantity' :int(MCAR), 'Description':'SM RIO 36 inch carrier'}
        return parts_dict, MCAR

def get_rg_mcar(Product,IOTANR,IOTAR,parts_dict):
    #CXCPQ-31175
    iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
    Enclosure_type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
    if iota == "RUSIO" and Enclosure_type == "Cabinet":
        MCAR=D.Ceiling((IOTANR/3)+(IOTAR/2))
        parts_dict["FC-MCAR-02"] = {'Quantity' :int(MCAR), 'Description':'SM RIO 36 inch carrier'}
        return parts_dict, MCAR