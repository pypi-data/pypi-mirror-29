===========================
xDot and mDot flash utility
===========================

It is a simple Shell script intended to help MacOS users to easily compile and flash Multitech Dot boards.

Features
--------

- Create a virtualenv with Mbed toolchain
- Deploy Mbed, installing the required Mbed libs in ARM Mbed projects
- Compile with ARM Compiler 5
- Flash the binary to your xDot or mDot devices

Install it globally
-------------------

``sudo pip install multitech_dot_flash``

How to use it
-------------

Make sure you run this inside an ARM Mbed project.
Checkout this example https://hackmd.io/s/r196eUWBG

Compile and flash an xdot

``flashit -t=xdot``

Flash previous build, already compiled for an mdot

``flashit -t=mdot -p``
