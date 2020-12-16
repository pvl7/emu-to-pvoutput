#!/usr/bin/env python3
#
__author__      = "Pavel Lu"
__copyright__   = "Copyright 2020"
__license__     = "GPL"
__version__     = "0.1"
__maintainer__  = "Pavel Lu"
__email__       = "email@pavel.lu"
__status__      = "Development"

import logging
from logging.handlers import RotatingFileHandler
import time
import os
import sys
import asyncio
import aioserial
import requests

# pvoutput SID and KEY are mandatory parameters
# default values can be overridden by the defined environment variables
rf_serial_port      = os.getenv('RF_SERIAL_PORT', "/dev/ttyACM0") # EMU-2 device usb port
rf_serial_baudrate  = os.getenv('RF_SERIAL_BAUDRATE', 115200)  # don't change this one
rf_pvoutput_sid     = os.getenv('RF_PVOUTPUT_SID') # your system SID from pvoutput.org
rf_pvoutput_key     = os.getenv('RF_PVOUTPUT_KEY') # your API key from pvoutput.org
rf_pvoutput_server  = os.getenv('RF_PVOUTPUT_SERVER', "pvoutput.org:80")

# logging settings
rf_log_level        = os.getenv('RF_LOG_LEVEL', 9) # 0 - INFO, 9 - DEBUG

# pre-flight checks
# mandatory variables check
for env_var in ["RF_PVOUTPUT_SID", "RF_PVOUTPUT_KEY"]:
    if env_var not in os.environ:
        try:
            raise EnvironmentError("The variable {} must be set.".format(env_var))
        except:
            print ("The variable {} must be set.".format(env_var))
            sys.exit(3)

# serial port check
try:
    os.stat(rf_serial_port)
except OSError:
    print ("USB device {} does not exist".format(rf_serial_port))
    sys.exit(3)


rf_pvoutput_raven_url = f"http://{rf_pvoutput_server}/service/r2/ravenpost.jsp?sid={rf_pvoutput_sid}&key={rf_pvoutput_key}"

aioserial_instance: aioserial.AioSerial = aioserial.AioSerial(port=rf_serial_port, baudrate=rf_serial_baudrate, write_timeout=0)

# EMU serial port data read
async def emu_serial_read(aioserial_instance: aioserial.AioSerial):
    rf_xml_block = ''
    rf_enabled_write = 0

    # send command to the device to get instant demand data
    try:
        await aioserial_instance.write_async(b'<Command><Name>get_instantaneous_demand</Name>[<Refresh>Y</Refresh>]</Command>\n')
    except (OSError, IOError) as e:
        print ("Serial port error:", e)
        return

    # start device polling to read the XML data block line by line
    while True:
        try:
            line: bytes = await aioserial_instance.readline_async()
        except (OSError, IOError) as e:
            print ("Serial port error:", e)
            return
        # once the first line detected, we start recording all following lines
        if b'<InstantaneousDemand>\r\n' in line:
            rf_enabled_write = 1

        if rf_enabled_write:
            rf_xml_block = rf_xml_block + str(line, 'utf-8').rstrip('\r\n')
        # once the last line detected, we stop recording the lines and return the XML block
        if b'</InstantaneousDemand>\r\n' in line:
            logging.debug ("XML data block:\n {}".format(rf_xml_block))
            return (rf_xml_block)

# HTTP post method
def http_post (url, xml_data):
    # HTTP post to pvoutput
    headers = {'Content-Type': 'application/xml'}
    res = requests.post(url, data=xml_data, headers=headers).text
    logging.info(res)
    return res

# main routine
async def main():
        # configure logger
        logging.basicConfig(
            handlers = [
                logging.StreamHandler(sys.stdout)
            ],
            level = rf_log_level,
            format  = "[%(asctime)s][%(levelname)s] %(message)s",
            datefmt = '%Y-%m-%dT%H:%M:%S'
        )

        logging.info('Reading smart meter data')

        # serial data asynchronous read and post to pvoutput.org
        http_post ( rf_pvoutput_raven_url, await emu_serial_read(aioserial_instance) )
        
if __name__ == "__main__":
    asyncio.run(main())
