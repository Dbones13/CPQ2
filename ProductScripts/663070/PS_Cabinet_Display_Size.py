if Product.Attributes.GetByName('CMS Cabinet Mounting Stations required').SelectedValue.Display=="Yes":
    Noofdisplay=Product.Attributes.GetByName('Cabinet_No_of_Displays (0-4)').GetValue()
    #Noofdisplay=Product.Attributes.GetByName('DMS No of Displays 0_4').GetValue()
    MIB=Product.Attributes.GetByName('MIB Configuration Required?').GetValue()
    CMS=Product.Attributes.GetByName('CMS Cabinet Mounting Stations required').SelectedValue.Display
    Newexp=Product.Attributes.GetByName('New_Expansion').SelectedValue.Display
    try:
        IWT=Product.Attributes.GetByName('Interface with TPS Required?').SelectedValue.Display
    except:
        IWT="No"

    if IWT=="Yes" and Newexp=="Expansion":
        Product.AllowAttr('Cabinet_Industrial_KB_Mouse')
    else:
        Product.DisallowAttr('Cabinet_Industrial_KB_Mouse')

    '''try:
        MWSOR=Product.Attributes.GetByName('CMS Multi Window Support Option Required?').SelectedValue.Display
    except:
        MWSOR="No"
    if MWSOR=="No" and (Noofdisplay=="2" or Noofdisplay=="3" or Noofdisplay=="4"):
        Product.Attributes.GetByName('Cabinet_No_of_Displays (0-4)').AssignValue("0")
        Product.AllowAttr('CMS Message 8')
    else:
        Product.DisallowAttr('CMS Message 8')'''