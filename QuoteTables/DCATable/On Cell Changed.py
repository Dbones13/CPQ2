if cell.ColumnName == "Sr":
        cell.Value=435

aa= Quote.QuoteTables["DCATable"]
count=1
for row in aa.Rows:
    row['Sr'] = count
    count += 1
Quote.Save()