start_date = ''
end_date = ''
from System import DateTime
from System.Globalization import CultureInfo

def getDateTimeOBJ(dateString, dateFormat):
    try:
        return DateTime.Parse(dateString,dateFormat)
    except:
        return
if Quote:
    #start_date = DateTime.Parse(Quote.GetCustomField('EGAP_Contract_Start_Date').Content)
    #end_date = DateTime.Parse(Quote.GetCustomField('EGAP_Contract_End_Date').Content)
    pass

productType = Product.Attr('SC_Product_Type').GetValue()
if productType == "New":
    prev_c_start_date = Product.Attr('PreviousQuoteCStartDate_EnabledServices').GetValue()
    prev_c_end_date = Product.Attr('PreviousQuoteCEndDate_EnabledServices').GetValue()

    currnt_start_date = Product.Attr('ContractStartDate_EnabledService').GetValue()
    current_end_date = Product.Attr('ContractEndDate_EnabledService').GetValue()

    ps = DateTime.ParseExact(prev_c_start_date,"M/d/yyyy",CultureInfo.InvariantCulture)
    pe = DateTime.ParseExact(prev_c_end_date,"M/d/yyyy",CultureInfo.InvariantCulture)

    cs = DateTime.ParseExact(currnt_start_date,"M/d/yyyy",CultureInfo.InvariantCulture)
    ce = DateTime.ParseExact(current_end_date,"M/d/yyyy",CultureInfo.InvariantCulture)

    com_be_PE_CE = DateTime.Compare(ce,pe)
    com_be_CS_CE = DateTime.Compare(ce,cs)

    if com_be_CS_CE < 0 :
        Product.Messages.Add('Please Note the Entered Date is outside of the parent Contract Date')
        Product.Attr('ContractEndDate_EnabledService').AssignValue(prev_c_end_date)
    elif com_be_PE_CE > 0:
        Product.Messages.Add('Please Note the Entered Date is outside of the parent Contract Date')
        Product.Attr('ContractEndDate_EnabledService').AssignValue(prev_c_end_date)