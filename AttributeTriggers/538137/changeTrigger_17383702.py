if Product.Attr('SC_Labor_Entitlement').GetValue() == "A360 Contract Management":
    Product.Attributes.GetByName("SC_Labor_Resource_Type").SelectDisplayValue("A360 Contract Management",False)
    Product.Attributes.GetByName("SC_Labor_Related_Module").SelectValue("A360")
    Product.Attributes.GetByName("SC_Labor_Deliverable_Hours").AssignValue("1")