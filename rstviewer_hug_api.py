#!/usr/bin/env python3

import codecs
import os
import sys

import hug
import sh

CONVERTER_EXECUTABLE = 'rstviewer'
INPUT_FILEPATH = '/tmp/input.rs3'


@hug.response_middleware()
def process_data(request, response, resource):
    """This is a middleware function that gets called for every request a hug API processes.
    It will allow Javascript clients on other hosts / ports to access the API (CORS request).
    """
    response.set_header('Access-Control-Allow-Origin', '*')


@hug.post('/rs3_to_png', output=hug.output_format.png_image)
def rs3_to_png(body):
    """Convert an .rs3 file into a .png file."""
    return _rs3_to_png(body, output_format='png')

@hug.post('/rs3_to_png_base64', output=hug.output_format.file)
def rs3_to_png(body):
    """Convert an .rs3 file into a base64 encoded string representation of a .png file."""
    return _rs3_to_png(body, output_format='png-base64')


def _rs3_to_png(body, output_format='png-base64'):
    """Convert an .rs3 file into either a 'png' or a 'png-base64' file."""
    converter = sh.Command(CONVERTER_EXECUTABLE)

    if 'input' in body:
        input_file_content = body['input']
        with open(INPUT_FILEPATH, 'wb') as input_file:
            input_file.write(input_file_content)

        output_filepath = INPUT_FILEPATH+'.'+output_format
        converter_stdout = converter('-f', output_format, input_file.name, output_filepath)
        return output_filepath
    else:
        return {'body': body}
