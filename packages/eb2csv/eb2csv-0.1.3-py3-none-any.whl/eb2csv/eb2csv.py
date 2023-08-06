# -*- coding: utf-8 -*-

import os
import csv
import sys
import click
import time
import math
import arrow
import locale
import requests

from .fieldconfig import field_configs


LOCALE = None


def set_locale():
    global LOCALE
    if not LOCALE:
        keys = ['German', 'de_DE']
        for key in keys:
            try:
                LOCALE = locale.setlocale(locale.LC_ALL, key)
                return
            except locale.Error:
                pass


def print_progress(value, status):
    minutes = math.floor(value / 60)
    seconds = int(value) % 60
    sys.stdout.write(f'\rRemaining time: {minutes:02.0f}:{seconds:02.0f} status: {status or "OK"}')
    sys.stdout.flush()


def fetch_live_data(host, meter_ids):
    """Fetch live-data from Energy Box API"""
    r = requests.get(f'http://{host}/dataservice/live/', {
        'meterId[]': meter_ids,
    }, timeout=10)
    return r


def fmt_value(value, key):
    if value is None:
        return ''
    elif key == 'timestamp':
        return arrow.get(value).isoformat()
    elif type(value) == float:
        return locale.format('%.2f', value)
    return f'{value}'


class Excel1Dialect(csv.Dialect):
    """
    CSV-dialect for use in german MS-Excel.
    """
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL
    encoding = 'windows-1252'


def fmt_header(field_config):
    if field_config.name == 'timestamp':
        return 'Timestamp'
    return f'{field_config.verbose_name} [{field_config.unit}]'


def update_file(meter_id, data, files, writers, outputdir):
    file_key = str(meter_id)
    writer = writers.get(file_key)
    if not writer:
        # init file/csv-writer
        # compile all the keys that are in data in the order of the field_config
        field_names = [field_config.name for field_config in field_configs if field_config.name in data]
        # compile csv headers
        headers = {
            field_config.name: fmt_header(field_config) for field_config in field_configs
            if field_config.name in data
        }
        filename = f'measured_data_{meter_id}.csv'
        path = os.path.join(outputdir, filename) if outputdir else filename
        fp = open(path, 'w', newline='')
        files[file_key] = fp
        writer = csv.DictWriter(fp, field_names, extrasaction='ignore', dialect=Excel1Dialect)
        writer.writerow(headers)
        writers[file_key] = writer
    writer.writerow({key: fmt_value(value, key) for key, value in data.items()})


def close_files(files):
    for file in files.values():
        file.close()


@click.command()
@click.option('--host', '-h', prompt=True, help="Hostname of the Energy Box data logger.")
@click.option('--outputdir', '-o', help="Path for the output files.")
@click.option('--duration', '-d', prompt='Recording duration (minutes)', type=int, help="Recording duration in minutes.")
@click.option('--meterids', '-m', multiple=True, help="One or more meter IDs.", type=int)
def cli(host, outputdir, duration, meterids):
    set_locale()
    duration *= 60
    meter_ids = []
    if not meterids:
        index = 1
        while True:
            meter_id = input(f'{index}. meter ID (or end with "return"): ')
            if not meter_id:
                break
            elif not meter_id.isdigit():
                click.echo('Meter ID has to be a valid integer.')
                continue
            meter_ids.append(meter_id)
            index += 1
    else:
        meter_ids = [str(id) for id in meterids]
    if not meter_ids:
        click.echo('At least one meter ID must be entered.')
        sys.exit()
    click.echo('\r\n')

    files = {}
    writers = {}
    last_timestamp = {}
    schedule = 2
    start_time = time.time()
    status = 'OK'
    # main loop
    try:
        while (time.time() - start_time) <= duration:
            try:
                r = fetch_live_data(host, meter_ids)
            except requests.exceptions.ReadTimeout:
                status = 'Read Timeout Error'
            except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
                status = 'Connection error'
                time.sleep(10)
            else:
                if r.status_code == 200:
                    data = r.json()
                    if 'error' in data:
                        click.echo(data['error'])
                        sys.exit()
                    for meter_id in meter_ids:
                        meter_data = data[meter_id]
                        if not meter_data:
                            # ToDo: display error
                            continue
                        timestamp = meter_data.get('timestamp')
                        if last_timestamp.get(str(meter_id)) != timestamp:
                            # only write to file if timestamp has changed
                            update_file(meter_id, meter_data, files, writers, outputdir)
                        last_timestamp[str(meter_id)] = timestamp
                    status = 'OK'
                else:
                    status = f'HTTP error: {r.status_code}'
            now = time.time()
            print_progress(duration - (now - start_time), status)
            sleep_time = schedule - (now % schedule)
            if sleep_time > 0:
                time.sleep(sleep_time)
    except requests.exceptions.InvalidURL:
        click.echo(f'Invalid host: {host}')
    finally:
        close_files(files)
