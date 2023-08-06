# comrade
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Build Status](https://travis-ci.org/erikmhauck/comrade.svg?branch=master)](https://travis-ci.org/erikmhauck/comrade)
[![Coverage Status](https://coveralls.io/repos/github/erikmhauck/comrade/badge.svg?branch=master)](https://coveralls.io/github/erikmhauck/comrade?branch=master)

[![PyPI Version](https://img.shields.io/pypi/v/Comrade.svg)](https://pypi.python.org/pypi/Comrade)
[![Python Versions](https://img.shields.io/pypi/pyversions/Comrade.svg)](https://pypi.python.org/pypi/Comrade)

A generic and configurable command executor.

# Installation

`pip install comrade`

# Configuration

Run comrade once to copy the sample config into the current user's home directoy.

Then you can edit and extend ~/comrade-config.json to your liking.


# Example 

Here is a bare-bones comrade-config.json that uses ffmpeg to transcode a file, and then print "success" to the command line.
```javascript
{
    "choices": [
        {
          "name": "example command",
          "commands": [
              "ffmpeg -i {input filename} -vcodec h264 -acodec mp2 {output filename}",
              "echo success"
          ]
        }
    ]
}
```

The above produces this user experience:
```
Comrade

Choose a command to execute.

1. example command
2. Exit

>>> 1
```
Once the user chooses which command to execute, it starts asking the user to populate the {variables} from the config.
```
Requesting variables for command:
ffmpeg -i {input filename} -vcodec h264 -acodec mp2 {output filename}

Set input filename: file.avi
Set output filename: file.mp4
```
It then shows the user what the compiled commands look like.
```
Comrade

Commands to execute:

ffmpeg -i file.avi -vcodec h264 -acodec mp2 file.mp4
echo success


1. Execute
2. Cancel

>>> 1
```
and then the commands run, using the user's input.
