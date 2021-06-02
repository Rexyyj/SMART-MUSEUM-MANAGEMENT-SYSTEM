# ThingSpeak
## Introduction
ThingSpeak is an IoT analytics platform service that allows you to aggregate, visualize, and analyze live data streams in the cloud.
This folder contains the implementation of ThingSpeak related operations in the Smart Museum Management System project.

## Account configuration
Contains MQTT API key and REST API key, which are required to access the Thingspeak account.

## Channeal configuration
```
{
  "api_key": "XXXXXXXXXXXXXX",
  "name": "SMMS-test",
  "public_flag": "true",
  "field1": "crowd",
  "field2": "light"
}
```

## Functions implemented
Creat a new channel
Delete a channel
Upload data to an existing channel
Get list of existing channels
Get the last data of a channel
