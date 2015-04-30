# Tuesday         

A Web Client of [OWI Robotic Edge Arm](http://www.owirobot.com/robotic-arm-edge-1/).  
based on [Roboarm](https://github.com/nvbn/roboarm) and [Flask](http://flask.pocoo.org/).

## Demo

![Screencapture GIF](https://dl.dropboxusercontent.com/u/5712604/screenshots/Screencast-tuesday.gif)

## Requirement
**Devices**:  
[OWI Robotic Edge Arm](http://www.owirobot.com/robotic-arm-edge-1/)   
[Raspberry Pi](https://www.raspberrypi.org/) (recommended)

**Environments**:  
GNU/Linux  
Python 2.7  
[Flask](http://flask.pocoo.org/)  
[PyUSB](https://github.com/walac/pyusb#installing-pyusb-on-gnulinux-systems)  
[Roboarm](https://github.com/nvbn/roboarm)   
...

## Install
```
$ sudo apt-get install python libusb-1.0-0
$ git clone git@github.com:mapler/tuesday.git
$ cd tuesday
$ pip install -r requirements.txt
```

## Usage
set Flask secret key for sessions.  

```
$ export ARM_APP_SECRET_KEY='[yoursecretkey]'
```
and run.

```
$ python runserver.py
```

## Licence

[MIT](https://github.com/mapler/tuesday/blob/master/LICENSE)

## Author

[mapler](https://github.com/mapler)
