# hologram-modem-debug

Log for hologram.io debug

Based on https://support.hologram.io/hc/en-us/articles/360035697393-Modem-SIM-annotated-diagnostic-test

Code from https://support.hologram.io/hc/en-us/articles/4417363338647

## Quick usage

```bash
python3 modem_diagnostics.py --port /dev/ttyUSB2 --baud 115200
# or you can directly run w/o params and it will let you pick which port to use
```
 
### Notes

- `--port` argument is optional. If not specified, a menu will pop up with the available serial ports.
- `--baud` argument is optional. If not specified, a value of 115200 is used by default.
