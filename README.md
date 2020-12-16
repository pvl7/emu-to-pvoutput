# Rainforest EMU device to pvoutput data exporter

A simple Python script to read data from the USB port of Rainforest EMU-2 device and post the XML block to [PVoutput](https://pvoutput.org) web site.

The idea is based on this project (https://github.com/zagnuts/RAVEnOUT) but Python and asynchronous serial port access worked much better for me.
Building and running from the Docker container makes it much easier to deploy the script into your solar home infrastructure.

## API keys

You must obtain your user id and access key pair from (https://pvoutput.org/help.html#api-getting-started) prior to using this script.

The following environment variables are mandatory:

* `RF_PVOUTPUT_SID` - This variable specifies the user id
* `RF_PVOUTPUT_KEY` - This variable contains the API secret key

## Other configuration variables

The following variables are available to customise your configuration:

* `RF_SERIAL_PORT` - path to the USB device name on the local system (/dev/ttyACM0 is default)
* `RF_SERIAL_BAUDRATE` - serial port connection speed (115200 is default)
* `RF_PVOUTPUT_SERVER` - pvoutput end point host name (http://pvoutput.org:80 is default)
* `RF_LOG_LEVEL` - log level (9 (DEBUG) is default )


## Build

```
docker build . -t rainforest-to-pvoutput:latest
```

## Usage

```
RF_PVOUTPUT_SID=<sid> RF_PVOUTPUT_KEY=<key> docker run --restart unless-stopped -d -e RF_PVOUTPUT_SID -e RF_PVOUTPUT_KEY --device "/dev/ttyACM0:/dev/ttyACM0" --name emu-to-pvoutput emu-to-pvoutput:latest
```

