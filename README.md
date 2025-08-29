# caldera‑opcua

**OPC‑UA Protocol Plugin for MITRE Caldera**
*Enhancing Caldera with support for the OPC‑UA industrial communication protocol.*

---

## Overview

**caldera-opcua** is a plugin designed to integrate OPC‑UA (Open Platform Communications Unified Architecture) protocol support into the MITRE Caldera adversary emulation platform. This enables users to simulate, analyze, monitor, or manipulate OPC‑UA-based systems directly through Caldera.

---

## Purpose & Motivation

* **Extend Caldera’s Native Capabilities:** Caldera does not currently support OPC‑UA, a common protocol in Industrial Control Systems (ICS). This plugin fills that gap.

---

## Features

* Connect to OPC‑UA endpoints
* Read and write node data
* Browse server nodes and namespaces
* Automate OPC‑UA-based scenarios within Caldera operations
* Proper authentication support (Anonymous, Username/Password, Certificates)


---

## Getting Started

### Prerequisites

* **Python** (version compatible with Caldera)
* Access to a running **Caldera instance** 


### Installation (example)

```bash
# Clone the repo
git clone https://github.com/wavestone-cdt/caldera-opcua.git
cd caldera-opcua


# Enable the plugin in Caldera
# (Specific steps depend on Caldera’s plugin system — e.g., adding to config)
mv caldera-opcua /path/to/caldera/plugins/
```

---

## Usage Example

Once installed, the plugin should appear within Caldera’s plugin library. You can leverage it in operations like:

1. Browsing OPC‑UA server nodes
2. Reading data from specific server paths
3. Modifying node values to simulate attacks or test resilience
4. Combining with other plugin-driven scenarios in Caldera



---

## Testing the Plugin

* Use a mock or real OPC‑UA server (e.g., with `python-opcua` demo server) 
* Create Caldera operations that invoke the plugin under controlled conditions
* Confirm functionality: authentication, browsing, reading, writing
* **A test demo Adversary is provided in the `adversaries` folder.**

---

## Contributing

Contributions are welcome!
Feel free to submit:

* Bug reports and feature requests
* Pull requests with improvements or documentation
* Tests and usage examples

---

## License

Licensed under the **Apache‑2.0** License. 

---

## Acknowledgements

This plugin template and concept follow Caldera’s plugin architecture. Refer to Caldera’s documentation for guidance on building plugins. 

### Contributors

* Baptiste Daumard - wavestone

