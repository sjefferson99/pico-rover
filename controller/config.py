## Logging
# Level 0-4: 0 = Disabled, 1 = Critical, 2 = Error, 3 = Warning, 4 = Info
LOG_LEVEL = 2
# Handlers: Populate list with zero or more of the following log output handlers (case sensitive): "Console", "File"
LOG_HANDLERS = ["Console", "File"]
# Max log file size in bytes, there will be a maximum of 2 files at this size created
LOG_FILE_MAX_SIZE = 10240

## IO
FWD_BUTTON = 12
REV_BUTTON = 15
LEFT_BUTTON = 14
RIGHT_BUTTON = 13

## NRF24L01
SPI_ID = 0
SCK = 2
MOSI = 3
MISO = 4
CSN = 5
CE = 6
