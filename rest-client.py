#!/usr/bin/env python3

from __future__ import print_function
import requests
import json
import time
import base64
import jsonpickle
import random
import argparse


def doRawImage(addr, debug=False):
    headers = {'content-type': 'image/png'}
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    image_url = addr + '/api/rawimage'
    response = requests.post(image_url, data=img, headers=headers)
    if debug:
        print("Response is", response)
        print(json.loads(response.text))


def doAdd(addr, debug=False):
    headers = {'content-type': 'application/json'}
    add_url = addr + "/api/add/5/10"
    response = requests.post(add_url, headers=headers)
    if debug:
        print("Response is", response)
        print(json.loads(response.text))


def doDotProduct(addr, debug=False):
    headers = {'content-type': 'application/json'}
    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]
    url = addr + '/api/dotproduct'
    response = requests.post(url, json={'a': a, 'b': b}, headers=headers)
    if debug:
        print("Response is", response)
        print(json.loads(response.text))


def doJsonImage(addr, debug=False):
    headers = {'content-type': 'application/json'}
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    encoded = base64.b64encode(img).decode('utf-8')
    url = addr + '/api/jsonimage'
    response = requests.post(url, json={'image': encoded}, headers=headers)
    if debug:
        print("Response is", response)
        print(json.loads(response.text))


parser = argparse.ArgumentParser(description='REST client for measuring server operations')
parser.add_argument('host', help='IP address or hostname of the REST server')
parser.add_argument('cmd', choices=['add', 'rawImage', 'dotProduct', 'jsonImage'],
                    help='Operation to perform')
parser.add_argument('reps', type=int, help='Number of repetitions for measurement')
parser.add_argument('-p', '--port', type=int, default=5000, help='Server port (default: 5000)')
parser.add_argument('-d', '--debug', action='store_true', help='Print the response from the server')
args = parser.parse_args()

addr = f"http://{args.host}:{args.port}"
print(f"Running {args.reps} reps against {addr}")

funcs = {'rawImage': doRawImage, 'add': doAdd,
         'jsonImage': doJsonImage, 'dotProduct': doDotProduct}
func = funcs[args.cmd]

start = time.perf_counter()
for x in range(args.reps):
    func(addr, debug=args.debug)
delta = ((time.perf_counter() - start) / args.reps) * 1000
print("Took", delta, "ms per operation")
