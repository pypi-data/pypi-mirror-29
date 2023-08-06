
# ServerStats
**Collect important system metrics from a server and log them**

We support collecting metrics for the following components:
* CPU
* Disk
* Network Traffic
* RAM
* Swap Memory

## Installation
### pip
> Prerequisites: Python2.7

```
$ sudo pip install serverstats
```
### docker
> Prerequisites: Docker >= 17.05
```
$ docker pull deepcompute/serverstats:1.0
```

## Usage
### Basic
```
$ serverstats run
```
Shows you the system metrics collected at every 5 sec (configurable) interval
To set the time interval of collection:
```
$ serverstats run --interval <int value>
```
![](https://i.imgur.com/vyuqL9G.gif)

##### In python interpreter


```
>>> from serverstats import get_system_metrics
>>> from pprint import pprint
>>> pprint(get_system_metrics())
{'cpu': {'avg_load_15_min': 0.88,
         'avg_load_1_min': 40.0,
         'avg_load_5_min': 24.25,
         'idle_percent': 78.0,
         'iowait': 3215.11,
         'usage_percent': 22.0},
 'disk': {'free': 889144725504,
          'free_percent': 90.75509294076929,
          'total': 979718819840,
          'usage': 40783671296,
          'usage_percent': 4.4},
 'network_traffic': {'enp4s0': {'received': 1881480065, 'sent': 93821861},
                     'lo': {'received': 704884, 'sent': 704884},
                     'wlp5s0': {'received': 262697, 'sent': 173003}},
 'ram': {'avail': 5829107712,
         'avail_percent': 70.53975885698708,
         'free': 504446976,
         'total': 8263577600,
         'usage': 1494208512,
         'usage_percent': 29.5},
 'swap': {'free': 3577421824,
          'free_percent': 85.31379457539636,
          'total': 4193251328,
          'usage': 615829504,
          'usage_percent': 14.7}}

```
![](https://i.imgur.com/64CwON7.gif)

### Docker run
```
$ docker run deepcompute/serverstats:1.0
```
```
$ docker run deepcompute/serverstats:1.0 serverstats run --interval 2
```
![docker_demo](https://user-images.githubusercontent.com/33823698/36727142-31ac6aca-1be2-11e8-89af-30d199d6d79b.gif)

