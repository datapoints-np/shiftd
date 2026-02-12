from shiftd import Engine

engine = Engine()


csv_path = "data/users.csv"

engine.convert(csv_path, "output.xlsx")
