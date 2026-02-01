reqDocument=len(list(Product.Attr('FSC_to_SM_Which_documentation_is_required').SelectedValues))
if reqDocument < 3:
    Product.Attr('IncompleteFSCtoSMDocumentRequired').AssignValue('False')
else:
    Product.Attr('IncompleteFSCtoSMDocumentRequired').AssignValue('True')