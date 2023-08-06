# Converto [![Build Status](https://travis-ci.org/erikmhauck/converto.svg?branch=master)](https://travis-ci.org/erikmhauck/converto)

## Summary

Converto acts as a human-friendly wrapper around FFmpeg and also provides some productivity-enhancing features.

### Features

* Batch Processing

* FFmpeg command-chaining

* Configurable


### Requirements

* [Python 2.7](https://www.python.org/) must be installed.

* [FFmpeg](https://ffmpeg.org/) must be on your path

### Installation

* `pip install converto`

### Usage

First, you will want to configure Converto using the configuration.json file. Once you've configured it to your liking, run `converto` from a terminal and follow on-screen prompts.

Converto also accepts some command-line parameters. Run `converto --help` to display which options are available.

## Configuration

Configuration is done via a JSON file in {site_packages}/converto/configuration/configuration.json

You can find your {site-packages} location by running `pip show converto | grep "Location:"`.

### Schema

```python
{
  "options": [
    {
      "name": string, # The name to be displayed in the command-chooser list
      "valid-input-extensions": [ # an array of accepted file extensions
        string 
      ],
      "multi-input": boolean, # whether or not the files selected by the user will all be used in a single command
      "commands": [ # an array of FFmpeg commands to run
        {
          "input-options": string, # the FFmpeg parameters BEFORE the -i flag
          "output-options": string, # the FFmpeg parameters AFTER the -i flag and before the output file name
          "output-extension": string, # the desired output file extension
          "output-filename-format": string # optional output filename configuration. Requires {input_filename} and {extension} to be used somewhere in the string
        }
      ]
    }
  ]
}
```

### Simple Example

```json
{
  "options": [
    {
      "name": "Create Access Copy",
      "valid-input-extensions": [
        "avi",
        "mov"
      ],
      "commands": [
        {
          "input-options": "",
          "output-options": "-vcodec h264 -acodec aac -strict -2",
          "output-extension": "mp4"
        }
      ]
    }
  ]
}
```

The above configuration get interpreted as this ffmpeg command:

```shell
ffmpeg -i input.avi -vcodec h264 -acodec aac -strict -2 input.mp4
```

Where "input.avi" is a file that the user chose to be operated on.

### Command Chaining Example

You can put multiple commands in an option, and they will be processed in serial. Intermediary files are used during the chaining, and are deleted when the command completes.

```json
{
  "name": "Rescale Analog NTSC Source",
  "valid-input-extensions": [
    "mkv"
  ],
  "commands": [
    {
      "input-options": "",
      "output-options": "-vf scale=720x480 -c:v ffv1 -level 3 -c:a copy",
      "output-extension": "mkv"
    },
    {
      "input-options": "",
      "output-options": "-c:v libx264 -pix_fmt yuv420p -preset veryslow -crf 18 -c:a aac -ar 48000 -b:a 256k",
      "output-extension": "mp4"
    }
  ]
}
```

The above will run these ffmpeg commands, and produce a single .mp4:
```shell
ffmpeg -i {input_filename} -vf scale=720x480 -c:v ffv1 -level 3 -c:a copy {intermediary_filename}
ffmpeg -i {intermediary_filename} -c:v libx264 -pix_fmt yuv420p -preset veryslow -crf 18 -c:a aac -ar 48000 -b:a 256k {output_filename}
```
