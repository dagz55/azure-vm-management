# Azure VM Management Script

![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

A powerful and user-friendly Python script for managing Azure Virtual Machines using the Azure CLI.

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [CHANGELOG](#-changelog)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- 🔍 Scan and view status of multiple Azure VMs
- 🔢 Filter VMs by power state (All, Running, Deallocated)
- 🚀 Start deallocated VMs
- 🛑 Stop and deallocate running VMs
- 📊 Display VM information in a colorful, easy-to-read table
- 🔄 Efficient caching of VM status data for quick filtering
- 🎯 Interactive prompts for VM management actions

## 🛠 Requirements

- Python 3.6+
- Azure CLI (az)
- Rich library for Python
- Active Azure subscription
- Proper Azure credentials configured

## 📥 Installation

1. Clone this repository:
   ```
   git clone https://github.com/dagz55/azure-vm-management.git
   cd azure-vm-management
   ```

2. Install the required Python packages:
   ```
   pip install rich
   ```

3. Ensure you have the Azure CLI installed and are logged in:
   ```
   az login
   ```

## 🚀 Usage

1. Prepare a text file (default: `manage_vmlist.txt`) containing the resource IDs of the VMs you want to manage, one per line.

2. Run the script:
   ```
   python azure_vm_management.py
   ```

3. Follow the interactive prompts to:
   - Scan VM status
   - Filter VMs by power state
   - Start deallocated VMs
   - Stop and deallocate running VMs

## 📜 CHANGELOG

### Version 1.0.0 (Initial Release)
- Basic functionality to manage Azure VMs
- Options to view status, start, and deallocate VMs
- Simple command-line interface

### Version 1.1.0
- Added colorful output using Rich library
- Improved error handling and user feedback
- Implemented progress bar for VM scanning

### Version 1.2.0
- Introduced caching of VM status data for quicker filtering
- Added sub-menu for filtering options (All, Running, Deallocated)
- Removed the need to re-scan VMs for each filter change

### Version 1.3.0 (Current)
- Removed Resource ID from the display table for cleaner output
- Added interactive prompts to start VMs after displaying deallocated list
- Added interactive prompts to stop and deallocate VMs after displaying running list
- Streamlined main menu options
- Improved user interaction flow

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/dagz55/azure-vm-management/issues).

## 📄 License

This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.

---

Made with ❤️ by [rsuar29@albertsons.com]