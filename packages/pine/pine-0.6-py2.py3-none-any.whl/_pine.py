#!/usr/bin/env python3

from dataclasses import dataclass, field
from datetime import datetime
from urllib.parse import urljoin
import argparse
import asyncio
import json
import os
import ssl
import statistics
import sys

import aiohttp
import certifi
import yaml

SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())


@dataclass
class Context:
    times: list
    failures: list
    status: int = field(default=200)


@dataclass
class Details:
    name: str
    version: str = field(default="")


@dataclass
class Defaults:
    root: str = field(default="")
    warmup: int = field(default=0)
    iterations: int = field(default=5)


@dataclass
class Test(Defaults):
    name: str = field(default="")
    description: str = field(default="")
    url: str = field(default="")
    status: int = field(default=200)
    method: str = field(default="get")
    headers: dict = field(default=None)
    json: dict = field(default=None)
    timeout: int = field(default=5*60) # This is the aiohttp default anyway.


@dataclass
class Result:
    timeouts: int
    failures: list
    name: str = field(default="")
    description: str = field(default="")
    version: str = field(default="")
    mean: float = field(default=0.0)
    median: float = field(default=0.0)
    stdev: float = field(default=0.0)


async def on_request_start(session, trace, params):
    trace.start = session.loop.time()


async def on_request_end(session, trace, params):
    elapsed = session.loop.time() - trace.start
    if params.response.status == trace.trace_request_ctx.status:
        trace.trace_request_ctx.times.append(elapsed)
    else:
        trace.trace_request_ctx.failures.append(params.response.status)


async def do_request(method, url, headers=None, data=None, context=None):
    response = await method(url, headers=headers, data=data, ssl=SSL_CONTEXT,
                            trace_request_ctx=context)
    return response.status


async def run_one_test(loop, test):
    tc = aiohttp.TraceConfig()
    tc.on_request_start.append(on_request_start)
    tc.on_request_end.append(on_request_end)

    timeouts = 0
    times = []
    failures = []

    async with aiohttp.ClientSession(
            loop=loop, trace_configs=[tc],
            read_timeout=test.timeout) as session:
        method = getattr(session, test.method)
        context = Context(times, failures)

        for _ in range(test.warmup + test.iterations):
            try:
                await do_request(method, test.url, headers=test.headers,
                                 data=test.json, context=context)
            except asyncio.TimeoutError:
                timeouts += 1

    result = Result(timeouts, failures)
    num_times = len(times)

    # Need at least two runs to calculate any of this.
    if num_times >= 2:
        runs = times[slice(test.warmup, num_times)]
        result.mean = statistics.mean(runs)
        result.median = statistics.median(runs)
        result.stdev = statistics.stdev(runs)
    elif num_times == 1:
        # If we only had one succeed, just use it directly.
        result.mean = times[0]
        result.median = times[0]
        result.stdev = 0

    return result



def run_tests(loop, tests):
    for test in tests:
        result = loop.run_until_complete(run_one_test(loop, test))
        result.name = test.name
        result.description = test.description
        yield result


def write_output(details, results, cli_args):
    report = {"results": [],
              "name": details.name,
              "version": details.version,
              "id": cli_args.run_id}
    for result in results:
        report["results"].append(result.__dict__)

    output = json.dumps(report)

    if cli_args.output_path is None:
        sys.stdout.write(output)
    else:
        # If we're given a directory, use the run_id to create the name.
        if os.path.isdir(cli_args.output_path):
            cli_args.output_path = os.path.join(
                cli_args.output_path, cli_args.run_id + ".json")

        with open(cli_args.output_path, "w") as out:
            out.write(output)


def make_test_name(path):
    base = os.path.basename(path)
    parts = base.split(os.path.extsep)
    return parts[0]


def process_details(config, path):
    try:
        details = config.pop("details")
    except KeyError:
        return Details(name=make_test_name(path))

    if "name" not in details:
        details["name"] = make_test_name(path)

    return Details(**details)


def process_defaults(config):
    try:
        defaults = config.pop("defaults")
    except KeyError:
        return Defaults()

    return Defaults(**defaults)


def read_config(path, test_names):
    with open(path, "r") as config_file:
        config = yaml.load(config_file.read())

    details = process_details(config, path)
    defaults = process_defaults(config)

    return details, get_tests(defaults, config, test_names)


def get_tests(defaults, config, test_names):
    check_test_name = True if test_names else False

    for test_name, values in config.items():
        if check_test_name and test_name not in test_names:
            continue

        # If there's a configured root url, join it up, otherwise
        # we'll assume the url is fully formed.
        if defaults.root:
            values["url"] = urljoin(defaults.root, values["url"])

        test = dict(defaults.__dict__)
        test["name"] = test_name

        # Fill in templated header values from environment variables
        if "headers" in values:
            for key, value in values["headers"].items():
                values["headers"][key] = value.format(**os.environ)

        # If we get json in here, dump it to a real JSON-encoded string
        # now rather than making aiohttp do it.
        if "json" in values:
            values["json"] = json.dumps(values["json"])

        test.update(values)

        yield Test(**test)


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config", dest="config_path",
                        help="Path to the configuraton file",
                        required=True)
    parser.add_argument(
        "-o", "--output", dest="output_path",
        # Technically the default here is None, but we later interpret
        # None to be sys.stdout
        help=("Path to write the output file (default: sys.stdout). "
              "If this is a directory, the `-i` run id  will be "
              "the name of the file in that directory (with a '.json' "
              "suffix). If this is a complete file path, the file "
              "will be written there."))
    parser.add_argument(
        "-i", "--id", dest="run_id",
        default=datetime.strftime(datetime.now(), "%Y%m%d%H%M%S%f"),
        help="The run ID, likely a branch checksum")

    parser.add_argument("test_names", nargs=argparse.REMAINDER,
                        help="The names of any specific tests to be run")

    return parser.parse_args()


def main():
    args = get_args()

    loop = asyncio.get_event_loop()

    details, tests = read_config(args.config_path, args.test_names)
    results = run_tests(loop, tests)
    write_output(details, results, args)

    loop.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
