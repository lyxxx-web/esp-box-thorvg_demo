# ThorVG Demos Example

| Board             | Support Status |
| ----------------- | -------------- |
| ESP32-S3-BOX      | YES            |
| ESP32-S3-BOX-Lite | YES            |
| ESP32-S3-BOX-3    | YES            |

This example is used to run ThorVG's demos. ThorVG is a platform-independent library for drawing vector-based graphics. This demo project showcases the rendering capabilities of ThorVG with various supported formats, including TVG, SVG, PNG, JPG, Lottie, and WebP.

## Supported Formats
ThorVG supports the following image formats in this demo:

 - TVG: ThorVG's native vector graphics format.
 - SVG: Scalable Vector Graphics, a widely-used vector image format.
 - PNG: Portable Network Graphics, a raster graphics format that supports lossless compression.
 - JPG: JPEG image format, commonly used for photos and other complex images.
 - Lottie: A JSON-based format for animations, compatible with Adobe After Effects.
 - WebP: A modern image format that provides superior compression for images on the web.
## How to use example

### Hardware Required

* A ESP32-S3-Box
* A USB-C cable for power supply and programming

### Build and Flash

Run `idf.py flash monitor` to build, flash and monitor the project.

Once a complete flash process has been performed, you can use `idf.py app-flash monitor` to reduce the flash time.

(To exit the serial monitor, type `Ctrl-]`. Please reset the development board f you cannot exit the monitor.)

