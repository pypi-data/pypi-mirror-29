# AwesomeMiner API Wrapper

An easy way to get Access to your AwesomeMiner configured for GPUs Miners

Compatible with Python 2.7 >+

## Install

`pip install pyaweminerapi`

## Usage

### Create API Object

`from pyaweminerapi import pyaweminapi`

`t = pyaweminapi(<WebAccess URL>)`

### Methods available
`getGpusTemp()` --> Returns an Array with all the miners and GPUs Temps

`getMinersBriefing()` --> Returns an Array with the followin info:

    name -> Miners name
    mainpool -> Main Pool URL
    dualpool -> Dual Mining Pool URL
    timerunning -> Time Elapsed since last restart
    gpuhashrates -> Array of the GPUs Hashrates
    temps -> Array of the GPUs Hashrates
    fans -> Array of Fan Percentage Speeds
    totalhashrate -> Total Hashrate of the Miner
    totalhashratesecondary -> Total Secundary Hashrate
    
    

