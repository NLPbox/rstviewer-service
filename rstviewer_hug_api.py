#!/usr/bin/env python3
import os
import sys

import hug
import sh


CONVERTER_EXECUTABLE = 'codra.sh'
INPUT_FILEPATH = '/tmp/input.rs3'


@hug.response_middleware()
def process_data(request, response, resource):
    """This is a middleware function that gets called for every request a hug API processes.
    It will allow Javascript clients on other hosts / ports to access the API (CORS request).
    """
    response.set_header('Access-Control-Allow-Origin', '*')


@hug.post('/convert', output=hug.output_format.file)
def call_converter(body, output_format):
    converter = sh.Command(CONVERTER_EXECUTABLE)

    if 'input' in body:
        input_file_content = body['input']
        with open(INPUT_FILEPATH, 'wb') as input_file:
            input_file.write(input_file_content)

        if output_format == b'rstviewer-html':
            output_filepath = INPUT_FILEPATH+'.html'
            converter_stdout = converter('-f', 'html', input_file.name, output_filepath)
            return output_filepath
        
        else: # always fall back to default format rstviewer-png
            output_filepath = INPUT_FILEPATH+'.png'
            converter_stdout = converter('-f', 'png', input_file.name, output_filepath)
            return output_filepath
    
    else:
        return {'body': body}
