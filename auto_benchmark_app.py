# This program requires OpenVINO 2022.1 or higher.

import sys
import glob
import re
import os
import datetime
import platform
import itertools

import cpuinfo
import psutil

import openvino
from openvino.tools.benchmark.main import main as benchmark_app

dry_run = False

def help():
    app_name = sys.argv[0]
    print('OpenVINO Benchmark_app extension - Parametric benchmark front end')
    print()
    print('You can specify variable parameters by adding following prefix to the parameters.')
    print('  $ : range     - $1,8,2 == range(1,8,2) => [1,3,5,7]')
    print('  % : list      - %CPU,GPU => [\'CPU\', \'GPU\'], %1,2,4,8 => [1,2,4,8]')
    print('  @ : ir-models - @models == IR models in the \'models\' dir => [\'resnet.xml\', \'googlenet.xml\', ...]')
    print('Example:')
    print(' python {} -cdir cache -m resnet.xml -nthreads $1,6,2 -nstreams %1,2,4,8 -d %CPU,GPU'.format(app_name))
    print(' python {} -m @models -niter 100 -nthreads %1,2,4,8 -nstreams %1,2 -d %CPU -cdir cache'.format(app_name))
    print()
    print('The program will generate a report file in CSV format. File name would be generated based on the time => \'result_DDmm-HHMMSS.csv\'')

def search_ir_models(dir):
    xmls = glob.glob(dir+'/**/*.xml', recursive=True)
    models = []
    for xml in xmls:
        path, filename = os.path.split(xml)
        base, ext      = os.path.splitext(filename)
        if os.path.isfile(os.path.join(path, base+'.bin')):
            models.append(xml)
    return models

def find_result(filename, item):
    with open(filename, 'rt') as f:
        for line in f:
            line = line.rstrip('\n')
            res = re.findall(item + r'\s+([0-9\.]+)', line)
            if len(res)>0:
                return res[0]
    return None       


def main():
    global dry_run
    if len(sys.argv)<2:
        help()
        return 0

    argstr = ''
    params = []
    for i, arg in enumerate(sys.argv):
        if arg == '-h' or sys.argv[1] == '--help':
            help()
            return 0
        if i == 0:
            argstr += 'benchmark_app.py'
        elif arg[0] == '$':
            params.append(list(eval('range({})'.format(arg[1:]))))
            argstr += ' {}'
        elif arg[0] == '%':
            params.append(list(arg[1:].split(',')))
            argstr += ' {}'
        elif arg[0] == '@':
            # search IR models
            ir_search_root_dir = arg[1:]
            if os.path.isdir(ir_search_root_dir):
                models = search_ir_models(ir_search_root_dir)
                print(models)
            else:
                print('The directory {} is not existing.'.format(ir_search_root_dir))
                return -1
            print('{} models found.'.format(len(models)))
            params.append(models)
            argstr += ' {}'
        else:
            argstr += ' '+arg
    print(argstr)

    combinations = tuple(itertools.product(*params, repeat=1))
    print('Total number of parameter combinations:', len(combinations))

    tmplog='tmplog.txt'
    now = datetime.datetime.now()
    with open(now.strftime('result_%d%m-%H%M%S.csv'), 'wt') as log:
        cpu_info = cpuinfo.get_cpu_info()
        print('#CPU:', cpu_info['brand_raw'], file=log)
        print('#MEM:', psutil.virtual_memory().total, file=log)
        print('#OS:', platform.platform(), file=log)
        print('#OpenVINO:', openvino.runtime.get_version(), file=log)
        print('#Last 4 items in the lines : test count, duration (ms), latency AVG (ms), and throughput (fps)')
        for combination in combinations:
            cmd_str = argstr.format(*combination)

            argv = cmd_str.split(' ')
            print(*argv, sep=',', end='', file=log)
            print(',', end='', file=log)

            if dry_run == True:
                continue

            sys.argv = argv
            with open(tmplog, 'wt') as htmplog:
                sys.stdout = htmplog            # redirect output
                sys.stderr = None
                benchmark_app()                 # call benchmark_app
                sys.stderr = sys.__stderr__
                sys.stdout = sys.__stdout__

            count      = find_result(tmplog, 'Count:')
            duration   = find_result(tmplog, 'Duration:')
            latency    = find_result(tmplog, '\s+AVG:')         # Latency = Median, AVG, MAX, MIN
            throughput = find_result(tmplog, 'Throughput:')

            print(count, duration, latency, throughput, sep=',', file=log)

if __name__ == '__main__':
    sys.exit(main())
