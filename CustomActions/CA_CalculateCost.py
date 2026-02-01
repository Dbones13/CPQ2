import GS_ItemCalculations

BookingLob = Quote.GetCustomField("Booking LOB").Content
Quotetype = Quote.GetCustomField("Quote Type").Content

for Item in Quote.Items:
    GS_ItemCalculations.calculateCosts(Quote , BookingLob, Quotetype , Item, TagParserQuote)
    Item.ExtendedCost = Item.Quantity * Item.Cost