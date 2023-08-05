# enaml-native
Build native mobile apps in python using enaml and native widgets! [![Build Status](https://travis-ci.org/codelv/enaml-native.svg?branch=master)](https://travis-ci.org/codelv/enaml-native) [![codecov](https://codecov.io/gh/codelv/enaml-native/branch/master/graph/badge.svg)](https://codecov.io/gh/codelv/enaml-native) [![Help chat](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/enaml-native/Lobby)


[![Python Playground](https://img.youtube.com/vi/2IfRrqOWGPA/0.jpg)](https://youtu.be/2IfRrqOWGPA)

The goal of this project is to be an alternative to using [kivy](https://kivy.org/) for building mobile apps with python. 

I made this because wanted to have a more "React Native" like environment that: 
1. Uses python 
2. Uses native widgets (Android / iOS)
3. Can be run from Android Studio / XCode (ie no bootstraps)
4. Uses enaml's models, and declarative and dynamic widget framework instead of kvlang
5. Uses versioned "packages" and "recipes" than can be installed/updated/removed to make repeatable builds (like rnpm)

### Docs and Examples ###

See the [project site](https://www.codelv.com/projects/enaml-native/). There's also some short tutorials and examples on [youtube](https://www.youtube.com/playlist?list=PLXUaMWWFaOjT2WdIrJdTYjEMJmrjuvVz0).

> Need help? Try the gitter group https://gitter.im/enaml-native/Lobby

### Add-on Packages ###

Enaml-native was redesigned so separate "packages" can be created and installed to add new 
native widgets and other apis. Similar to the [kivy-garden](https://github.com/kivy-garden/) but
it borrows the concepts of the [react-native package manager](https://github.com/rnpm/rnpm).

Packages can be created using the `enaml-native init-package <your-package-name>` command. Once
made they can be installed with `pip` or the `enaml-native install` command (recommended).

#### Packages ####

- GoogleMap support via [enaml-native-maps](https://github.com/codelv/enaml-native-maps)
- MPAndroidChart graphing via [enaml-native-charts](https://github.com/codelv/enaml-native-charts)
- ZXing barcode scanning via [enaml-native-barcode](https://github.com/codelv/enaml-native-barcode)
- Iconfiy icons via [enaml-native-icons](https://github.com/codelv/enaml-native-icons)

Created a package? Send a PR and add it here!

### Features ###
1. Enaml's features: declarative syntax, conditional and looper rendering, automatic data binding
2. Layouts with flexbox
3. Live app code reloading (like react-native's live reload)
4. Versioned package management and native library linking
5. Remote debugging with your favorite IDE (like react-native's remote debugger)

### Apps ###

Apps using enaml-native can be found [here](https://www.codelv.com/projects/enaml-native/apps/).

### Demos ###
1. Try out the beta demo app here [on google play](https://play.google.com/store/apps/details?id=com.frmdstryr.enamlnative.demo)
2. Try out code without installing the android SDK or NDK via the [Python Playground](https://play.google.com/store/apps/details?id=com.frmdstryr.pythonplayground)!

### Status ###

##### Android

Currently enaml-native's Android support is good enough to make real usable app.  A lot of components are supported and several apps have already been relased using enaml-native.

##### iOS

Currently enaml-native's iOS support is not yet good enough to make a real app. Only a few components are implemented at the moment and a lot of work is needed to get it to the point where it's really usable, but my "proof of concept" demo shows that it does work. 

[![Enaml-native iOS Preview](https://img.youtube.com/vi/8woq4qsedss/0.jpg)](https://youtu.be/8woq4qsedss)


### Thanks to ###

This project is built on top of several existing projects:

1. [enaml](https://github.com/nucleic/enaml)
2. [python-for-android](https://github.com/kivy/python-for-android/)
3. [pybridge](https://github.com/joaoventura/pybridge)
4. [react-native](https://github.com/facebook/react-native) (inspiration)
5. [pyjnius](https://github.com/kivy/pyjnius/)
6. [kivy-ios](https://github.com/kivy/kivy-ios/)

### Contributions

Contributions of any kind are welcome. Please use the [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html) format
for docstrings and the [pep-8](https://www.python.org/dev/peps/pep-0008/) code style to be consistent with enaml.

### Donate

This is a project I develop in my free time. If you use enaml-native or simply like the project and want to help continue the development of it please consider [donating](https://www.codelv.com/projects/enaml-native/support/). 




