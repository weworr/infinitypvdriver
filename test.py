import serial
import time


def send_command(command: int) -> list:
    print(f'-------------------%s-------------------' % hex(command))

    packet = bytearray()
    packet.append(0x66)
    packet.append(command)
    packet.append(0x00)
    packet.append(0x00)
    packet.append(0x00)
    packet.append(0x34)

    serial.write(packet)
    return [int(byte) for byte in bytearray(serial.readline())]


def convert_to_si(value, q):
    return value * pow(2, -1 * q) if value <= pow(2, 31) - 1 else -1 * (pow(2, 32) - value) * pow(2, -1 * q)


def hex_string_to_bytes(hex_string: str) -> bytes:
    hex_string = hex_string.strip()
    bytes_list = [int(hex_string[i:i + 2], 16) for i in range(0, len(hex_string), 2)]

    return bytes(bytes_list)


serial = serial.Serial(
    'COM11',
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

time.sleep(2)

response = send_command(0x29)
print(response)

response = send_command(0x34)
print(response)

vMin = (response[3] << 24) | (response[4] << 16) | (response[5] << 8) | response[6]
# print(vMin)
# packet = bytearray()
# packet.append(0x66)
# packet.append(0x10)
# packet.append(0x00)
# packet.append(0x00)
# packet.append(0x00)
# packet.append(0x34)

# # 1100 0000 0111 0100 1001 1010 0000 0000
# # C0749A00
# serial.write(packet)

# response = [int(byte) for byte in bytearray(serial.readline())]
# print(response)

# print('-----------------------------------------------')

# print(serial.name)

#1000010

# try:
# command = '10'
# xd = hex_string_to_bytes(command + '0D0A')
# serial.write(xd)
# response = serial.readline()
# while response:
#     print(response.strip())
# print(response)
# except :

# print(serial.isOpen)
# for i in range(10):
#     print('xdd')
#     print(response)
#     time.sleep(1)
# # finally:
# serial.close()
response = send_command(0x3E)

qVmin = int(response[3])
print(qVmin)
print(response)
# exit()
data = (response[3] << 24) | (response[4] << 16) | (response[5] << 8) | response[6]
print(data)
if response:
    print(vMin)
    print(qVmin)
    print(convert_to_si(vMin, qVmin))
    print(vMin * pow(2, -1 * qVmin) if vMin <= pow(2, 31) - 1 else -1 * (pow(2, 32) - vMin) * pow(2, -1 * qVmin))
# print(response)

# print(str(response, 'UTF-8'))
# print(str(response, 'ASCII'))

response = send_command(0x2E)
print(response)

# V
response = send_command(0x3C)  # GAIN - default 1
print(response)
gain = 1

# CURR
response = send_command(0x3D)  # GAIN - default 1
print(response)

response = send_command(0x2C)
print(response)

adc_volts = (response[3] << 8) | (response[4])
adc_curr = (response[5] << 8) | response[6]

print("v")
print(adc_volts)

# if adc_volts < pow(2, 15):
#     adc_volts = (62.5 * (pow(10, -6) / gain) * adc_volts)
# else:
#     adc_volts = (-(pow(2, 16) - adc_volts) * 62.5 * (pow(10, -6) / gain))

# Get VSLOPE
response = send_command(0x38)
print(response)
vslope_xGAIN = (response[3] << 24) | (response[4] << 16) | (response[5] << 8) | response[6]

# Get VINTER
response = send_command(0x39)
print(response)
vinter_xGAIN = (response[3] << 24) | (response[4] << 16) | (response[5] << 8) | response[6]

print(adc_volts * vslope_xGAIN + vinter_xGAIN)

print("A")
print(adc_curr)

if adc_curr < pow(2, 15):
    adc_curr = (62.5 * (pow(10, -6) / gain) * adc_curr)
else:
    adc_curr = (-(pow(2, 16) - adc_curr) * 62.5 * (pow(10, -6) / gain))

# Get CSLOPE
response = send_command(0x3A)
print(response)
cslope_xGAIN = (response[3] << 24) | (response[4] << 16) | (response[5] << 8) | response[6]
# cslope_xGAIN /= pow(10, 9)
print(cslope_xGAIN)

# Get CINTER
response = send_command(0x3B)
print(response)
cinter_xGAIN = (response[3] << 24) | (response[4] << 16) | (response[5] << 8) | response[6]
print(cinter_xGAIN)
# cinter_xGAIN /= pow(10, 9)

print(adc_curr * cslope_xGAIN + cinter_xGAIN)

# GET QVSLOPE
response = send_command(0x3F)
print(response)
# qvslope = (response[3] << 24) | (response[4] << 16) | (response[5] << 8) | response[6]
qvslope = 30
print(qvslope)

# GET QVINTER
response = send_command(0x41)
print(response)
qvinter = (response[3] << 24) | (response[4] << 16) | (response[5] << 8) | response[6]
qvinter = 31
print(qvinter)

print(vslope_xGAIN)
print(vinter_xGAIN)
vslope_xGAIN = convert_to_si(vslope_xGAIN, qvslope)
vinter_xGAIN = convert_to_si(vinter_xGAIN, qvinter)

if adc_volts < pow(2, 15):
    adc_volts = (62.5 * (pow(10, -6) / gain) * adc_volts)
else:
    adc_volts = (-(pow(2, 16) - adc_volts) * 62.5 * (pow(10, -6) / gain))

print(vslope_xGAIN)
print(vinter_xGAIN)
print(adc_volts * vslope_xGAIN + vinter_xGAIN)

# -------------------0x29-------------------
# [102, 1, 1, 0, 0, 0, 0, 0, 41, 52]
# -------------------0x34-------------------
# [102, 1, 2, 191, 235, 254, 226, 0, 52, 52]
# -------------------0x3e-------------------
# 28
# [102, 1, 2, 28, 28, 30, 25, 0, 62, 52]
# 471604761
# 3219914466
# 28
# -4.004883877933025
# -4.004883877933025
# -------------------0x2e-------------------
# [102, 1, 1, 0, 16, 0, 0, 0, 46, 52]
# -------------------0x3c-------------------
# [102, 1, 1, 0, 1, 0, 0, 0, 60, 52]
# -------------------0x3d-------------------
# [102, 1, 1, 0, 1, 0, 0, 0, 61, 52]
# -------------------0x2c-------------------
# [102, 1, 2, 0, 59, 0, 0, 0, 44, 52]
# v
# 59
# -------------------0x38-------------------
# [102, 1, 2, 125, 240, 194, 48, 0, 56, 52]
# -------------------0x39-------------------
# [102, 1, 2, 255, 163, 64, 33, 0, 57, 52]
# 128951779633
# A
# 0
# -------------------0x3a-------------------
# [102, 1, 2, 78, 228, 26, 25, 0, 58, 52]
# 1323571737
# -------------------0x3b-------------------
# [102, 1, 2, 255, 91, 116, 80, 0, 59, 52]
# 4284183632
# 4284183632.0
# -------------------0x3f-------------------
# [102, 1, 2, 30, 30, 30, 29, 0, 63, 52]
# 30
# -------------------0x41-------------------
# [102, 1, 2, 31, 31, 31, 31, 0, 65, 52]
# 31
# 2112930352
# 4288888865
# 1.9678197354078293
# -0.002830490004271269
# 0.004425845270045102
