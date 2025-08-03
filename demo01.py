from micropyGPS import MicropyGPS
my_gps = MicropyGPS()
my_sentence = '$GPRMC,081836,A,3751.65,S,14507.36,E,000.0,360.0,130998,011.3,E*62'
for x in my_sentence:
     my_gps.update(x)
     
print(my_gps.latitude)
     