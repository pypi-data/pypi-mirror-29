#!/usr/bin/env python3

import argparse
import io
import sys
import json
from datetime import datetime
import collections

from jsonschema.validators import Draft4Validator
import singer

logger = singer.get_logger()


def emit_state(state):
    if state is not None:
        line = json.dumps(state)
        logger.debug('Emitting state {}'.format(line))
        sys.stdout.write("{}\n".format(line))
        sys.stdout.flush()


def persist_lines(delimiter, lines, state_file=None, bq_file_name_hook=False):
    state = None
    stream = None
    schemas = {}
    key_properties = {}
    validators = {}
    
    now = datetime.now().strftime('%Y%m%dT%H%M%S')

    for line in lines:
        try:
            o = json.loads(line)
        except json.decoder.JSONDecodeError:
            logger.error("Unable to parse:\n{}".format(line))
            raise

        if 'type' not in o:
            raise Exception("Line is missing required key 'type': {}".format(line))
        t = o['type']

        if t == 'RECORD':
            if 'stream' not in o:
                raise Exception("Line is missing required key 'stream': {}".format(line))
            if o['stream'] not in schemas:
                raise Exception("A record for stream {} was encountered before a corresponding schema".format(o['stream']))

            validators[o['stream']].validate(o['record'])

            filename = o['stream'] + '-' + now + '.json'
            
            with open(filename, 'a') as json_file:
                record = bq_hook(o['record']) if bq_file_name_hook else o['record']
                json_file.write(json.dumps(record) + delimiter)

            state = None
        elif t == 'STATE':
            logger.debug('Setting state to {}'.format(o['value']))
            state = o['value']
            if state_file and stream:
                save_state(state_file, stream, state)
        elif t == 'SCHEMA':
            if 'stream' not in o:
                raise Exception("Line is missing required key 'stream': {}".format(line))
            stream = o['stream']
            schemas[stream] = o['schema']
            validators[stream] = Draft4Validator(o['schema'])
            if 'key_properties' not in o:
                raise Exception("key_properties field is required")
            key_properties[stream] = o['key_properties']
        else:
            raise Exception("Unknown message type {} in message {}"
                            .format(o['type'], o))
    
    return state


def save_state(state_file, stream, state):
    with open(state_file, 'r') as json_file:
        actual_state = json.load(json_file)
        updated_time = state["bookmarks"][stream]["updated_time"]
        actual_state["bookmarks"][stream]["updated_time"] = updated_time

    with open(state_file, 'w') as outfile:
        outfile.write(json.dumps(actual_state))


# Fields must contain only letters, numbers, and underscores, start
# with a letter or underscore, and be at most 128 characters long.
def bq_hook(obj):
    for key in obj.keys():
        new_key = key.replace(".", "_")
        if new_key[0].isdigit():
            new_key = "_" + new_key
        if new_key != key:
            obj[new_key] = obj[key]
            del obj[key]
    return obj


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file')
    parser.add_argument('-s', '--state', help='State file')
    args = parser.parse_args()

    if args.config:
        with open(args.config) as input:
            config = json.load(input)
    else:
        config = {}

    input = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    #with open('ads.json', 'r') as input:
    state = persist_lines(config.get('delimiter', ''),
                          input,
                          args.state,
                          config.get('bq_file_name_hook', False))
        
    emit_state(state)
    logger.debug("Exiting normally")


if __name__ == '__main__':
    main()
