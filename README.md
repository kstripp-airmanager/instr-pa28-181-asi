# Piper PA28-181 Arrow II Airspeed Indicator

## Dependencies

This uses the DIN 1451 font, which may not be installed on most systems
by default.
Another similar font is OCR-B.

They can be obtained here:
https://www.dafontfree.io/alte-din-1451-mittelschrift-font/
https://fontesk.com/ocr-b-font/

## Directory Structure

```
├── README.md
├── LICENSE
├── python: Code for generating resource images
├── Reference: Reference images
└── <UUID>: Instrument files
    ├── info.xml: metadata
    ├── resources
    │   └── instrument appearance images
    ├── preview.png: instrument thumbnail
    └── logic.lua: instrument behavior
```

## Developing
