#!/usr/bin/python3

import datetime
import os
import subprocess
import sys
import tempfile
import time
from argparse import ArgumentParser

def parse_args():
  p = ArgumentParser(
    description='Simple sharding script',
    usage='%(prog)s --input TXTFILE --output TXTFILE --command STR --shard N',
  )

  p.add_argument(
    '--input',
    type=str, metavar='STR', nargs='?', required=True,
    help='input text file')
  p.add_argument(
    '--output',
    type=str, metavar='STR', nargs='?', required=True,
    help='output text file')
  p.add_argument(
    '--command',
    type=str, metavar='STR', nargs='?', required=True,
    help='command to be run, in which "@IN@" and "@OUT@" metavars should be included')
  p.add_argument(
    '--shard',
    type=int, metavar='INT', nargs='?', required=True,
    help='number of shards')

  args = p.parse_args()
  assert args.shard > 0
  return args

def poll_processes(process_list):
  running = 0
  succeeded = 0
  failed = 0
  for process in process_list:
    code = process.poll()
    if code is None:
      running += 1
    elif code == 0:
      succeeded += 1
    else:
      failed += 1
  return running, succeeded, failed

def main(args):
  # make file discriptors and file names
  prefix = 'shard.%d.' % time.time()
  in_filedesc_list, in_filename_list = zip(*(tempfile.mkstemp(prefix=prefix + '%04d.' % n) for n in range(args.shard)))
  out_filename_list = [x + '.out' for x in in_filename_list]

  print('making input shards ...')
  in_shard_fp_list = [os.fdopen(x, 'w') for x in in_filedesc_list]
  with open(args.input) as in_fp:
    for n, line in enumerate(in_fp):
      in_shard_fp_list[n % args.shard].write(line)
  for fp in in_shard_fp_list:
    fp.close()

  process_list = []
  begin_time = datetime.datetime.now()

  try:
    # run command
    for in_filename, out_filename in zip(in_filename_list, out_filename_list):
      command = args.command.replace('@IN@', in_filename).replace('@OUT@', out_filename)
      process = subprocess.Popen(command, shell=True)
      process_list.append(process)
    
    # wait
    while True:
      running, succeeded, failed = poll_processes(process_list)
      elapsed = datetime.datetime.now() - begin_time
      print('%s: %d running, %d succeeded, %d failed' % \
        (elapsed, running, succeeded, failed), end='\r')
      if succeeded + failed == args.shard:
        break
      time.sleep(0.2)

  except BaseException as ex:
    print()
    print('ERROR: %s: %s' % (type(ex).__name__, ex))
    # terminate all processes
    for process in process_list:
      try:
        process.terminate()
      except:
        pass
    print('all processes terminated.')
    return
  
  print()
  
  running, succeeded, failed = poll_processes(process_list)
  if succeeded == args.shard:
    print('merge results ...')
    out_shard_fp_list = [open(x) for x in out_filename_list]
    with open(args.output, 'w') as out_fp:
      try:
        n = 0
        while True:
          line = next(out_shard_fp_list[n])
          out_fp.write(line)
          n = (n + 1) % args.shard
      except StopIteration:
        pass
    for fp in out_shard_fp_list:
      fp.close()
  else:
    print('some processes failed.')

  print('removing input/output shards ...')
  for fn in in_filename_list:
    os.remove(fn)
  for fn in out_filename_list:
    os.remove(fn)

if __name__ == '__main__':
  args = parse_args()
  main(args)
