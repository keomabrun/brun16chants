In this file we describe the data we will analyse
There are 3 Health Reports (HR): HR_DEVICE, HR_NEIGHBORS and HR_DISCOVERED

#-----------------------------------------------------------------------------#
### DUST_NOTIF_HR_DEVICE
{
    charge : charge du noeud en mC
    queueOcc : Mean and max queue occupancy. Bits 0-3 are the mean queue occupancy, and bits 4-7 are the max queue occupancy.
    temperature : in C
    batteryVoltage : en mV
    numTxOk : Number of packets sent from NET to MAC
    numTxFail : Number of packets not sent due to congestion or failure to allocate a packet
    numRxOk : Number of received packets
    numRxLost : Number of packets lost (discarded by NET layer due to misc errors)
    numMacDropped : Number of packets dropped by MAC (due to retry count or age or no route)
    numTxBad : Transmit failure counter for bad link
    badLinkFrameId : Frame id of link with the worst performance over the last health report interval
    badLinkSlot : Slot of link with the worst performance over the last health report interval
    badLinkOffset : Offset of link with the worst performance over the last health report interval
}

##### Dust documentation
The Device Health Report reports on the device's statistics accumulated since the last device health report.


The availability of the mote, in percent, is:
`100*(1-numTxFail/(numTxFail+numTxOk))`

For calculating the overall network availability, we define two new variables and initialize them to zero.
Call them appTxPk and appTxFail.
To keep a running tally with each Device HR:
`appTxPk += numTxOk + numTxFail`
`appTxFail += numTxFail`


#-----------------------------------------------------------------------------#
### DUST_NOTIF_HR_NEIGHBORS
{
    "neighbors": [
        {
            'neighborId',
            'neighborFlag': Existing path failure condition if == 1
            'rssi':
            'numTxPackets':
            'numTxFailures':
            'numRxPackets':
        },
        ...
    ]
}

##### Dust documentation
The Neighbors' Health Report contains a report of current statistics about communication with each neighbor of a mote.

In order to have enough statistical significance in a path stability, we
should consider only paths for which `numTxPackets > 10`

The neighbor stability can be calculated as follow:
`100*(1-numTxFailures/numTxPackets)`


#-----------------------------------------------------------------------------#
### DUST_NOTIF_HR_DISCOVERED
{
    'numJoinParents':  Number of parent motes
    'discoveredNeighbors': [
        {
            'neighborId':
            'rssi':
            'numRx':  Number of times a neighbor was heard
        },
        ...
    ]
}

##### Dust documentation
The Discovered Neighbor Health Report contains a list of neighbors discovered in this health report interval.


