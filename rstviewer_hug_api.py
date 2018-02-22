#!/usr/bin/env python3
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


@hug.post('/rs3_to_png', output=hug.output_format.file)
def rs3_to_png(body):
    converter = sh.Command(CONVERTER_EXECUTABLE)

    if 'input' in body:
        input_file_content = body['input']
        with open(INPUT_FILEPATH, 'wb') as input_file:
            input_file.write(input_file_content)

        output_filepath = INPUT_FILEPATH+'.png'
        converter_stdout = converter('-f', 'png', input_file.name, output_filepath)
        return output_filepath
    else:
        return {'body': body}


@hug.post('/rs3_to_html', output=hug.output_format.html)
def rs3_to_html(body):
    converter = sh.Command(CONVERTER_EXECUTABLE)

    if 'input' in body:
        input_file_content = body['input']
        with open(INPUT_FILEPATH, 'wb') as input_file:
            input_file.write(input_file_content)

        output_filepath = INPUT_FILEPATH+'.html'
        converter_stdout = converter('-f', 'html', input_file.name, output_filepath)
        return output_filepath
    else:
        return {'body': body}
