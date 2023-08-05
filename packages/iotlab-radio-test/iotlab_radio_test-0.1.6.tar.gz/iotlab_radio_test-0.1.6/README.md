# IoT-LAB Radio Test

This repository contains tools in oder to map nodes radio connectivity of IoT-LAB with M3 nodes.

The M3 nodes use the ``firmwares/radio_test_m3.elf`` firmware with sources available in:

* ``https://github.com/iot-lab/openlab/tree/master/appli/iotlab/radio_test``

And originally based on:

* ``https://github.com/adjih/openlab/tree/radio-exp/devel/radio_test``. 


## Pre-requisite

You must have succesfully completed an ``auth-cli`` on the ssh frontend you are considering testing. e.g:

```
$ ssh <login>@<site>.iot-lab.info
<login>@<site>$ auth-cli -u <login>
Password: ****
"Written"
<login>@<site>$
```

## Installation

```
pip install iotlab-radiotest
```

should be enough in most cases (when this package is deployed to pypi)

In order to work from the source code you can install it

```
python setup.py install [--user]]
```

If you want to install in a virtualenv, use pipenv ```pipenv install```
 enter the isolated virtualenv using ```pipenv shell``` before using the ```iotlab-radiotest``` commands


## Configuration

* Configuration is passed through a yaml file, there is an included nominal config [Nominal config](iotlab_radio_test/nominal_config.yaml)

You can start any of the included entry points passing a `--config <config file>` parameter where
the config file contains yaml instructions for values you want to modify, example

config.yaml:

    site : lille
    archi : m3
    nodes_str : 12-14
    radio:
      txpower_list : [2, 4, 6, 8, 10, 12]

Then,

    iotlab-radiotest start --config config.yaml

will keep the values for the rest of the parameters but change the site to lille and
query other nodes.

You can also modify a single value in the config by using its fully qualified name in the CLI arguments.
These command lines are equivalent:

```
    iotlab-radiotest start --config config.yaml
    iotlab-radiotest start --site lille --archiv m3 --node_list 12,13,14 --radio.txpower_list 2,4,6,8,10,12
```

The start entry point creates an experiments/experiment_id foled in the current working dir,
it will save in it a config.yaml. This config.yaml is used as the nominal config file for
entry points that take an experiment_id as parameter.

Be careful, it's possible to pass parameters that won't make sense, like attempting to parse
data files for a channel that wasn't actually tested, so be careful when overriding config when
using entry points

## Radio Test entry points:

* Start
```
    iotlab-radiotest start
```

Will start the appropriate experiment with the appropriate firmware,
run the background listening for the ouptuts on the serial link,
collect the outputs, and parses the results

    For the next commands, if you omit the experiment_id parameter it should
    default to the latest experiment_id in

* Run

```
    iotlab-radiotest run -i <experiment_id>
```

If you already have an experiment and a socat in the background,
start the collection of outputs

* Parser

```
    iotlab-radiotest raw_parser -i <experiment_id>
```

Parses the raw logs and merge them

* Connectivity Parser

```
    iotlab-radiotest raw_parser -i <experiment_id>
```

Parses the merged logs and identifies the good, unbalanced and bad links

* Aggregate

```
    iotlab-radiotest aggregate_avg -l <experiment_ids_list> -n <output_name>
    iotlab-radiotest aggregate_stability -l <experiment_ids_list> -n <output_name>
```

These will aggregate a number of experimental runs to average the connectivity/stability

* Draw

```
    iotlab-radiotest draw -i <experiment_id>
```

Draws the graph of connectivity using matplotlib

## Manually starting the radio test

* Submit the experiment using the ``firmware/radio_test_m3.elf`` firmware:

```
experiment-cli submit -d 60 -n test -l strasbourg,m3,1+5+9+29+33+37+53+57+61,firmwares/radio_test_m3.elf
```

* In one terminal, use socat to forward all nodes serial input/output with the following command

Don't forget to replace ``<login>`` with your IoT-LAB login and ``<site>`` with the remote testbed :

```
socat tcp-listen:9000,fork,reuseaddr "exec:ssh <login>@<site>.iot-lab.info 'serial_aggregator'"
```

* In another terminal, launch collect script, replace ``<experiment_id>`` with your given experiment id:

```
pipenv run python ./01_run_radio_test.py -i <experiment_id>
```

## Postprocess and display

* Process the raw log files with following commands

```
iotlab-radiotest raw_parser -i <experiment_id>
```

```
iotlab-radiotest connectivity_parser -i <experiment_id>
```

* Finally, plot results with command :

```
iotlab-radiotest draw_--help
usage: iotlab-radiotest draw [-h]
                             [[...] config arguments]
                             [--config CONFIG] [-i EXPERIMENT_ID]
                             [-m {connectivity,pdr,rssi,lqi}]
                             [-S STABILITY] [-r] [-c] [-n] [-w] [-s]
config arguments:
  --radio.packet_interval RADIO.PACKET_INTERVAL
  --radio.channel_list RADIO.CHANNEL_LIST
  --archi ARCHI
  --site SITE
  --node_list NODE_LIST
  --radio.packet_numbers RADIO.PACKET_NUMBERS
  --draw.azim DRAW.AZIM
  --draw.elev DRAW.ELEV
  --duration DURATION
  --radio.txpower_list RADIO.TXPOWER_LIST
  --radio.packet_size RADIO.PACKET_SIZE
  --draw.font_size DRAW.FONT_SIZE

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG
  -i EXPERIMENT_ID, --id EXPERIMENT_ID
                        IoT-LAB experiment id
  -m {connectivity,pdr,rssi,lqi}, --metric {connectivity,pdr,rssi,lqi}
                        metric to draw
  -S STABILITY, --show-stability STABILITY
                        show stability
  -r, --robot           show robots
  -c, --cluster         show clusters
  -n, --nodes           show nodes
  -w, --wifi            show Wi-Fi AP
  -s, --save            save image as file
```

For example :

```
iotlab-radiotest draw -m connectivity -i <experiment_id>
```



### **OPTIONAL:** results aggregation

You can aggregate results for multiple experiments. 

* Use following command in order to average pdr,rssi,lqi results:

```
iotlab-radiotest aggregate_avg -l 10,11,23,115 -n 4_exp_set
```

* Use following command find stable links accross multiple experiments

```
iotlab-radiotest aggregate_stability -l 10,11,23,115 -n 4_exp_set
```

Output will be set in ``stability/4_exp_set`` directory


* Draw results for pdr average:

```
iotlab-radiotest draw -m pdr -i 4_exp_set
```

* Draw good link for last experiment and stables links accross multiple experiments:

```
iotlab-radiotest draw -m connectivity -S 4_exp_set
```

## Limitations

* It takes 6 seconds per iteration. You can estimate your experiment run time with formula : ``experiment run time = nb_nodes * nb_channels * nb_txpower * 6s``
* Some options for plotting results work only if nodes are on the same z level, and not aligned (all nodes with same x or same y).

## Improvements

* Generate a config template per experiment instead of a global config.py file
* Integrate cli-tools python library in order to dynamically get NODE_LIST and topology from a running reservation
* Use RUN_SCRIPT feature from IoT-LAB in order to submit and automatically start ``run_radio_test_01.py``collect script

## Traces

As an example, you can download traces from previous experiments here :

* ``http://tracenet.u-strasbg.fr/datasets/iotlab/acm_pewasun16/acm_pewasun16_experiments.tar.gz``

Untar acm_pewasun16_experiments.tar.gz and copy files from ``acm_pewasun16_experiments`` to ``experiments`` directory.

Use following paremeters in ``nominal_config.yaml``

```
SITE="strasbourg"
ARCHI="m3"
NODE_LIST = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64]
CHANNEL_LIST = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
TXPOWER_LIST = [3]
```