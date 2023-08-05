pyEagleSCR
--
pyEagleSCR is a pure Python parser for the scripting language used by [AutoDesk/CADSoft Eagle's PCB schematic/layout tool](https://www.autodesk.com/products/eagle).

For now, it aims to support only the functionality needed to parse symbols and packages, to ease use of part specifications in other tools like [KiCad](http://kicad-pcb.org/).

Status
--
Basic functionality working, including (probably not quite full) support for these commands:
* Edit, with support for Symbols, Packages and Devices
* Prefix
* Pin
* Wire
* Layer
* Connect
* Description
* Attribute
* Add
* Package
* Smd
* Grid
* Set

Example
--
Running this tool against the .SCR file found in [this ZIP on farnell.com](http://www.farnell.com/cad/1724597.zip) (for the component [STM32F405RGT6](http://uk.farnell.com/stmicroelectronics/stm32f405rgt6/mcu-32bit-cortex-m4-168mhz-lqfp/dp/2064363?st=stm32F405rgt6), farnell stock number 2064363) produces this result:

```python
{'devices': {'STM32F405RGT6': <Device STM32F405RGT6>},
 'grid': 'mil',
 'layer': '96',
 'packages': {'QFP50P1200X1200X160-64N': <Package QFP50P1200X1200X160-64N lines=278 smd_pads=64>},
 'settings': {'Wire_Bend': '2'},
 'symbols': {'STM32F405RGT6': <Symbol STM32F405RGT6, 64 pins, 4 lines>}}
```

It doesn't look like much, but this is a bare summary of the rich information inside this tree of objects. The parsed symbol here, a ```STM32F405RGT6```, has a listing of all 64 pins, correctly mapped to the 64 SMD pads in the ```QFP50P1200X1200X160-64N``` package via the connections specified by the device ```STM32F405RGT6```.

Usage
--
Create a Parser object, and feed the SCR in, line-by-line, then read the information you want out of the Parser.context object:
```python
scrparser = parser.Parser()

for line in open("yourfile.scr"):
    scrparser.handle_line(line)
    
print scrparser.context['symbols']
# {'STM32F405RGT6': <Symbol STM32F405RGT6, 64 pins, 4 lines>}
```

You can fetch information about the pins on this symbol, like what type of pin it is, and the co-ordinates that the pin should be displayed at when drawing the symbol:
```python
pins = scrparser.context['symbols']['STM32F405RGT6'].pins
print pins.keys()[:10]
# ['PB11', 'PB10', 'PB13', 'PB12', 'PB15', 'PB14', 'VDDA', 'PC14', 'PC15', 'VSS_2']
print pins['PB11']
# <Pin PB11 type=I/O rotation=0 position=-700,-1600 device=STM32F405RGT6.30> 
print pins['VDDA']
# <Pin VDDA type=Pwr rotation=0 position=-700,1800 device=STM32F405RGT6.13>
```

If this script file had information about the package and the device for this symbol, you can also get the physical pad information for any pin by looking up the corresponding pin in the package spec:
```python
pin_number = pins['VDDA'].device_pin_number
# '13'
scrparser.context['packages']['QFP50P1200X1200X160-64N'].smd_pads[pin_number]
# <Smd 13 x=11 y=58 width=270 height=-221 rotation=-89>
```

Contributing
--
Contributions are welcome! Please open a PR!

TODO
--

* The API is a little janky:
  * Names of attributes could be more obvious
  * Pins should have references to their corresponding pads on the package
* Support more Eagle SCR commands, like:
  * Change (applies to Package and Symbol)
  * Text (applies to Package and Symbol)
  * Value (applies to Device?)
  * Pad (through hole components, applies to Package?)
  * Technology (applies to Device?)
  * Wire (four-tuple variant, probably for rectangles?)
* Support stripping comments after the end of a command.
  * More examples in https://github.com/sparkfun/SparkFun_Eagle_Settings/blob/master/scr/eagle.scr
* Set up sensible defaults in the context, to match what Eagle does.
  * layer
  * grid
  * Any other default settings that should be initialised here?
* Support case-insensitive commands
* Python 3 support
* Tests!
* Support for processing a whole file so we don't have to feed it in line-by-line, which is silly.
