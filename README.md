# Semi-automated OpenVINO benchmark_app with variable parameters  

## Description  
This program allows the users to specify variable parameters in the OpenVINO benchmark_app and run the benchmark with all combinations of the given parameters automatically.  
The program will generate the report file in the CSV format with coded date and time file name ('`result_DDmm-HHMMSS.csv`'). You can analyze or visualize the benchmark result with MS Excel or a spreadsheet application.  

**The program is just a front-end for the OpenVINO official benchmark_app.**  
This program utilizes the benchmark_app as the benchmark core logic. So the performance result measured by this program must be consistent with the one measured by the benchmark_app.  
Also, the command line parameters and their meaning are compatible with the benchmark_app.  

### Requirements  
- OpenVINO 2022.1 or higher  
This program is not compatible with OpenVINO 2021.

### How to run  
1. Install required Python modules.  
```sh
python -m pip install --upgrade pip setuptools
python -m pip install -r requirements.txt
```

2. Run the auto benchmark (command line example)  
```sh
python auto_benchmark_app.py -m resnet.xml -niter 100 -nthreads %1,2,4,8 -nstreams %1,2 -d %CPU,GPU -cdir cache
```
With this command line, `-nthreads` has 4 options (1,2,4,8), `-nstreams` has 2 options (1,2), and `-d` option has 2 options (CPU,GPU). As the result, 16 (4x2x2) benchmarks will be performed in total.  

### Parameter options  
You can specify variable parameters by adding following prefix to the parameters.  
|Prefix|Type|Description/Example|
|---|---|---|
|$|range|`$1,8,2` == `range(1,8,2)` => `[1,3,5,7]`<br>All `range()` compatible expressions are possible. e.g. `$1,5` or `$5,1,-1`|
|%|list|`%CPU,GPU` => `['CPU', 'GPU']`, `%1,2,4,8` => `[1,2,4,8]`|
|@|ir-models|`@models` == IR models in the \'`./models`' dir => `['resnet.xml', 'googlenet.xml', ...]`<br>This option will recursively search the '.xml' files in the specified directory.|

### Examples of command line  
`python auto_benchmark_app.py -cdir cache -m resnet.xml -nthreads $1,6,2 -nstreams %1,2,4,8 -d %CPU,GPU`  
- Run benchmark with `-nthreads` = [1,3,5], `-nstreams`=[1,2,4,8], `-d`=['CPU','GPU']. Total 24 combinations.  

`python auto_benchmark_app.py -m @models -niter 100 -nthreads %1,2,4,8 -nstreams %1,2 -d CPU -cdir cache`
- Run benchmark with `-m`=[all .xml files in `models` directory], `-nthreads` = [1,2,4,8], `-nstreams`=[1,2].  

### Example of a result file  
The last 4 items in each line are the performance data in the order of 'count', 'duration (ms)', 'latency AVG (ms)', and 'throughput (fps)'.  
```
#CPU: Intel(R) Core(TM) i7-10700K CPU @ 3.80GHz
#MEM: 33947893760
#OS: Windows-10-10.0.22000-SP0
#OpenVINO: 2022.1.0-7019-cdb9bec7210-releases/2022/1
#Last 4 items in the lines : test count, duration (ms), latency AVG (ms), and throughput (fps)
benchmark_app.py,-m,models\FP16\googlenet-v1.xml,-niter,100,-nthreads,1,-nstreams,1,-d,CPU,-cdir,cache,100,772.55,30.20,129.44
benchmark_app.py,-m,models\FP16\resnet-50-tf.xml,-niter,100,-nthreads,1,-nstreams,1,-d,CPU,-cdir,cache,100,1917.62,75.06,52.15
benchmark_app.py,-m,models\FP16\squeezenet1.1.xml,-niter,100,-nthreads,1,-nstreams,1,-d,CPU,-cdir,cache,100,195.28,7.80,512.10
benchmark_app.py,-m,models\FP16-INT8\googlenet-v1.xml,-niter,100,-nthreads,1,-nstreams,1,-d,CPU,-cdir,cache,104,337.09,24.75,308.53
benchmark_app.py,-m,models\FP16-INT8\resnet-50-tf.xml,-niter,100,-nthreads,1,-nstreams,1,-d,CPU,-cdir,cache,100,1000.39,38.85,99.96
benchmark_app.py,-m,models\FP16-INT8\squeezenet1.1.xml,-niter,100,-nthreads,1,-nstreams,1,-d,CPU,-cdir,cache,104,64.22,4.69,1619.38
benchmark_app.py,-m,models\FP32\googlenet-v1.xml,-niter,100,-nthreads,1,-nstreams,1,-d,CPU,-cdir,cache,100,778.90,30.64,128.39
benchmark_app.py,-m,models\FP32\resnet-50-tf.xml,-niter,100,-nthreads,1,-nstreams,1,-d,CPU,-cdir,cache,100,1949.73,76.91,51.29
benchmark_app.py,-m,models\FP32\squeezenet1.1.xml,-niter,100,-nthreads,1,-nstreams,1,-d,CPU,-cdir,cache,100,182.59,7.58,547.69
benchmark_app.py,-m,models\FP32-INT8\googlenet-v1.xml,-niter,100,-nthreads,1,-nstreams,1,-d,CPU,-cdir,cache,104,331.73,24.90,313.51
benchmark_app.py,-m,models\FP32-INT8\resnet-50-tf.xml,-niter,100,-nthreads,1,-nstreams,1,-d,CPU,-cdir,cache,100,968.38,38.45,103.27
benchmark_app.py,-m,models\FP32-INT8\squeezenet1.1.xml,-niter,100,-nthreads,1,-nstreams,1,-d,CPU,-cdir,cache,104,67.70,5.04,1536.23
benchmark_app.py,-m,models\FP16\googlenet-v1.xml,-niter,100,-nthreads,2,-nstreams,1,-d,CPU,-cdir,cache,100,1536.14,15.30,65.10
benchmark_app.py,-m,models\FP16\resnet-50-tf.xml,-niter,100,-nthreads,2,-nstreams,1,-d,CPU,-cdir,cache,100,3655.59,36.50,27.36
benchmark_app.py,-m,models\FP16\squeezenet1.1.xml,-niter,100,-nthreads,2,-nstreams,1,-d,CPU,-cdir,cache,100,366.73,3.68,272.68
benchmark_app.py,-m,models\FP16-INT8\googlenet-v1.xml,-niter,100,-nthreads,2,-nstreams,1,-d,CPU,-cdir,cache,100,872.87,8.66,114.56
benchmark_app.py,-m,models\FP16-INT8\resnet-50-tf.xml,-niter,100,-nthreads,2,-nstreams,1,-d,CPU,-cdir,cache,100,1963.67,19.54,50.93
benchmark_app.py,-m,models\FP16-INT8\squeezenet1.1.xml,-niter,100,-nthreads,2,-nstreams,1,-d,CPU,-cdir,cache,100,242.28,2.34,412.74
benchmark_app.py,-m,models\FP32\googlenet-v1.xml,-niter,100,-nthreads,2,-nstreams,1,-d,CPU,-cdir,cache,100,1506.14,14.96,66.39
benchmark_app.py,-m,models\FP32\resnet-50-tf.xml,-niter,100,-nthreads,2,-nstreams,1,-d,CPU,-cdir,cache,100,3593.88,35.88,27.83
benchmark_app.py,-m,models\FP32\squeezenet1.1.xml,-niter,100,-nthreads,2,-nstreams,1,-d,CPU,-cdir,cache,100,366.28,3.56,273.01
benchmark_app.py,-m,models\FP32-INT8\googlenet-v1.xml,-niter,100,-nthreads,2,-nstreams,1,-d,CPU,-cdir,cache,100,876.52,8.69,114.09
benchmark_app.py,-m,models\FP32-INT8\resnet-50-tf.xml,-niter,100,-nthreads,2,-nstreams,1,-d,CPU,-cdir,cache,100,1934.72,19.25,51.69
```

END
