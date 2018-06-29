#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <nlpbox.programming@arne.cl>

import base64
import io
import os

import pexpect
import pytest
import requests
import sh
from PIL import Image
import imagehash


TESTDIR = os.path.dirname(__file__)
RS3_FILEPATH = os.path.join(TESTDIR, 'test.rs3')
EXPECTED_PNG1 = os.path.join(TESTDIR, 'result1.png')
EXPECTED_PNG2 = os.path.join(TESTDIR, 'result2.png')


@pytest.fixture(scope="session", autouse=True)
def start_api():
    print("starting API...")
    child = pexpect.spawn('hug -f rstviewer_hug_api.py')
    # provide the fixture value (we don't need it, but it marks the
    # point when the 'setup' part of this fixture ends).
    yield child.expect('(?i)Serving on :8000')
    print("stopping API...")
    child.close()


def image_matches(produced_file, expected_files=[EXPECTED_PNG1, EXPECTED_PNG2]):
    """Return True, iff the average hash of the produced image matches any of the
    expected images.
    """
    produced_hash = imagehash.average_hash(Image.open(produced_file))

    expected_hashes = [imagehash.average_hash(Image.open(ef)) for ef in expected_files]
    return any([produced_hash == expected_hash for expected_hash in expected_hashes])


def test_rs3_to_png():
    """The rstviewer-service API converts an .rs3 file into the expected image."""
    with open(RS3_FILEPATH) as input_file:
        input_text = input_file.read()

    res = requests.post(
        'http://localhost:8000/rs3_to_png',
        files={'input': input_text})
    assert image_matches(io.BytesIO(res.content))


def test_rs3_to_png_base64():
    """The rstviewer-service API converts an .rs3 file into the expected base64 encoded image."""
    with open(RS3_FILEPATH) as input_file:
        input_text = input_file.read()

    res = requests.post(
        'http://localhost:8000/rs3_to_png_base64',
        files={'input': input_text})
    png_bytes = base64.b64decode(res.content)
    assert image_matches(io.BytesIO(png_bytes))
