from ds1054z import DS1054Z

scope = DS1054Z('USB0::6833::1230::DS1ZA182511136::0::INSTR')
print("Connected to: ", scope.idn)