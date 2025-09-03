# Assets Directory

This directory contains application assets for ZenSort.

## Required Files

For proper building, you need to add the following icon files:

- **icon.ico** - Windows icon file (256x256 recommended)
- **icon.icns** - macOS icon file (generated from PNG)
- **icon.png** - Linux icon file (256x256 PNG)

## Creating Icons

You can create these from a single high-resolution PNG (512x512 or higher):

### Windows (.ico)
Use online converters or tools like ImageMagick:
```bash
convert icon.png -resize 256x256 icon.ico
```

### macOS (.icns)
Use the `iconutil` command on macOS:
```bash
mkdir icon.iconset
sips -z 16 16 icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32 icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32 icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64 icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128 icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256 icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256 icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512 icon.png --out icon.iconset/icon_256x256@2x.png
iconutil -c icns icon.iconset
```

### Linux (.png)
Simply use a 256x256 PNG file as icon.png.

## Note

The build scripts will work without icons, but the executables will use default system icons.