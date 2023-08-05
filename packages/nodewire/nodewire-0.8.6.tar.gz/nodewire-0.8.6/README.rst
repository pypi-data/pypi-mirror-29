NodeWire is an open source framework for building connected devices.
It is a system for connecting appliances to the internet and then allowing them
to be programmed through the use of schematic diagrams (NodeWire sketch).

Each appliance is called a node. And there are different types of nodes.
Some are sensors such as motion sensors, and some are actuators such as motor speed controller or a relay
that can switch on a light bulb or trigger an alarm.

Nodes have ports which can be input or output. You can program a node by manipulating its ports in the NodeWire sketch environment.
When you connect nodes to each other or connect constant values or variables to input nodes,
you control the appliances connected to the node.
For example, if a motion sensor node's output is connected to the input of a relay whose output
port is also connected to a light bulb, the light bulb will automatically switch on when motion is sensed.

This is where the name NodeWire comes from. Nodes are controlled by interconnecting them together on the Sketch environment.

The objective of NodeWire are to:

  1. Enable hobbyists to create connected devices in minutes and provide an easy path for them to go commercial.
  2. Provide a full stack that is free (as in freedom) and mostly free (as in free beer), that developers can adopt and extend.
  3. Provide easy inter-operability with other leading products and frameworks
  4. Provide highly innovative features such as the schematic-based programming tool, zero-configuration, auto-layout and auto-networking.

NodeWire runs on Arduino, NodeMCU and various linux based SBCs such as Raspberry Pi.