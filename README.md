# Netstate

## About
The goal of Netstate (from NETwork STAck TEsts) is to help in testing network stacks.
In its current state, it lets you define test suites using [packetdrill](https://code.google.com/p/packetdrill/) to generate traffic.
It was developed to test SNMP counters, and was only tested on Linux, but should be able to evolve to cover other scenarios.

## Writing tests
Currently only packetdrill based tests are supported. When running a test, Netstate will:

* perform a setup
* generate traffic with packet drill
* validate the results observed
* clean things up

Each test is made up of 2 files having the same name except for the extesion:

* one python with extension .py file defining a class derived from the BasedTest class. The steps of a test listed above correspond respectively to the methods setup(), gen_traffic(), validate() and cleanup(). If you overwrite gen_traffic(), call self.packet_drilling with the filename of the packetdrill script you want to run, or no argument to run the default packetdrill script for this test. 
* a packetdrill script with extension .drill

Defining a test is thus simply defining the test class, overriding only the methods needed, and writing a packetdrill script.
The examples directory contains example tests, you can run them with (change the path to packetdrill):
`sudo python run.py -p /your/path/to/packetdrill -t ./examples`

## Running tests
The script run.py is used to run the tests. 
It is invoked as

  `run.py [flags] tests_glob`

It supports these flags:

* `--tests <test_dir>` : the directory holding the test definitions
* `--packetdrill <path>` : which packetdrill executable to use.
* `--sudo` : invoke packetdrill with sudo
* `--no-sudo` : opposite

tests_glob is used to identify which tests to run. It can be:

* empty : run all tests in the directory specified by the --tests flag
* filename prefix: run all tests whose file name is located in the --tests dir and match tests_glob
* filename : run only the test defined in filename (without the extension)

The tests run halts at the first failing test.
