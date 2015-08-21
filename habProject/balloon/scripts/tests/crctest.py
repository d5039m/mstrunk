import crcmod

crc16f = crcmod.predefined.mkCrcFun('crc-ccitt-false') 

string = 'test checksum string'

csum = str(hex(crc16f(string))).upper()[2:]
csum = csum.zfill(4)

print 'Checksum: ' + csum

