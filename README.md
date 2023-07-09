# BGP-SDN
This project controls BGP traffic using SDN to improve efficiency in announcing and maintaining BGP paths

# SDN Network Project

This repository contains the source code and documentation for an SDN (Software-Defined Networking) network project. The project simulates a network topology using Mininet, POX controller, and ExaBGP.

## Project Structure

The project is organized as follows:

- `pox/`: Contains the POX controller scripts.
- `mininet/`: Contains the Mininet topology script.
- `exabgp/`: Contains the ExaBGP configuration files and BGP simulation scripts.

## Prerequisites

Before running the project, ensure that you have the following dependencies installed:

- Python 3
- Mininet
- POX controller
- ExaBGP

## Running the Project

To run the project, follow these steps:

1. Start the POX controller: Change directory to the `pox` directory and run the command `./pox.py forwarding.l2_ddos`.

2. Run the Mininet topology: Change directory to the `mininet` directory and run the command `sudo python3 topo.py`.

3. Test connectivity: In the Mininet CLI, run the command `pingall` to test the connectivity between the hosts.

4. Start ExaBGP on h1 and h5: Open separate terminals for hosts h1 and h5 using the Mininet CLI command `xterm h1` and `xterm h5`, respectively. In each terminal, run the appropriate ExaBGP command.

5. Capture network traffic: Open Wireshark with the command `sudo wireshark` and capture traffic on the interfaces of the switches.

6. Observe the project behavior: Monitor the network traffic in Wireshark and observe the logs in the terminal where the POX controller is running.

## Results and Analysis

Analyze the captured network traffic in Wireshark and the logs from the POX controller to understand the behavior of the BGP traffic and the learning switch. Ensure that the BGP routes are correctly advertised and learned by the hosts.

