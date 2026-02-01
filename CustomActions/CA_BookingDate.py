Quote.GetCustomField('Booking Date').Content = TagParserQuote.ParseString('<*CTX( Date)*>')
Quote.Save(False)