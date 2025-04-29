import math as m

AU_to_km = 149597870.7
# 1 AU = 149,597,870.7 km
conv_au_to_km = float(input("AU Amount: ")) * AU_to_km
scient_notation = "{:e}".format(conv_au_to_km)
print("AU to km in scientific notation: ",scient_notation)
print("AU to km: ", conv_au_to_km)

