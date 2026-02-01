# Added this logic to hide the "One time upgrade" attribute when Quote type is renewal as per the requirement
Quote_Type = TagParserQuote.ParseString('<* QuoteProperty (Quote Type) *>')
if Quote_Type == "Contract Renewal":
    Product.Attributes.GetByName("One time upgrade").Allowed=False
else:
    Product.Attributes.GetByName("One time upgrade").Allowed=True