#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Program entry point"""

import os
import re
import sys
from collections import namedtuple
import traceback
import time
import argparse

from kafkatos3.MessageArchiveKafka import MessageArchiveKafkaReader, MessageArchiveKafkaWriter

from kafkatos3.metadata import project, version

PartitionInfo = namedtuple("PartitionInfo",
                           ["header", "writer", "offset"])


def get_files(directory, extension):
    '''return a list of all files in a partition directory with a passed in extension'''
    file_list = []
    for dirpath, _, files in os.walk(directory):
        for filename in files:
            fname = os.path.join(dirpath, filename)
            filename, file_extension = os.path.splitext(fname)
            if file_extension == extension:
                file_list.append(fname)
    return file_list


def mkdirp(directory):
    '''equiv of a mkdir -p'''
    if not os.path.isdir(directory):
        os.makedirs(directory)


def rotate_partition(partitions, partition, working_dir):
    '''rotate out a partition'''
    work_dir = os.path.join(working_dir, "data")

    if int(partitions[partition].offset) == int(partitions[partition].header.get_start_offset()):
        print("Skipping rotate for partition " + partition + ". No new writes")
        return
    print("I need to rotate " + partition)
    partitions[partition].writer.close()

    start_offset = partitions[partition].header.get_start_offset()
    end_offset = partitions[partition].offset
    topic = partitions[partition].header.get_topic()
    part_number = partitions[partition].header.get_partition()

    dest_dir = os.path.join(work_dir, "tocompress", topic, str(part_number))

    date = time.strftime("%y%m%d")

    dest_filename = os.path.join(dest_dir, topic + "-" + str(part_number) + "_" + str(
        start_offset) + "-" + str(end_offset) + "_" + date + ".mak")

    print("mkdir " + dest_dir)
    mkdirp(dest_dir)

    print("rename " + partitions[partition].writer.get_filename() + " " + dest_filename)
    os.rename(partitions[partition].writer.get_filename(), dest_filename)


def main(argv):
    '''entry point'''
    arg_parser = argparse.ArgumentParser(
        prog=argv[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='rotate all kafkatos3 inprogress files tocompress')

    arg_parser.add_argument(
        '-V', '--version',
        action='version',
        version='{0} {1}'.format(project, version))

    arg_parser.add_argument('workingdir', help='kafkatos3 working directory')

    args = arg_parser.parse_args(args=argv[1:])

    working_dir = args.workingdir

    root_dir = os.path.join(working_dir, "inprogress")
    partitions = {}
    files = get_files(root_dir, ".mak")

    for filename in files:
        try:
            stripped_filename = re.sub(root_dir + "/", "", filename)

            match = re.search(r"([^\/]+)\/([^\/]+)/", stripped_filename)

            print("topic is " + match.group(1))
            print("partition is " + match.group(2))

            key = match.group(1) + ":" + str(match.group(2))

            bmr = MessageArchiveKafkaReader(filename)
            header = bmr.get_header()
            last_offset = bmr.get_last_offset()
            bmr.close()
            bmw = MessageArchiveKafkaWriter(filename)

            part_info = PartitionInfo(
                header=header, writer=bmw, offset=last_offset)
            partitions[key] = part_info
        except Exception as exe:  # pylint: disable=W0703
            print("Problem processing file [" + filename + "]: " + str(exe))
            print(traceback.format_exc())

    for partition in partitions:
        rotate_partition(partitions, partition, working_dir)


def entry_point():
    """Zero-argument entry point for use with setuptools/distribute."""
    raise SystemExit(main(sys.argv))


if __name__ == '__main__':
    entry_point()
