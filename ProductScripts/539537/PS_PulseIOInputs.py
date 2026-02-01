#CXCPQ-50813
import GS_SerC_IO_Inputs
ioFamilyType = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
if ioFamilyType in ['Series C', 'Turbomachinery']:
    GS_SerC_IO_Inputs.pulseInputQuestions(Product)