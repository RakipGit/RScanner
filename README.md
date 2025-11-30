![Status](https://img.shields.io/badge/status-complete-brightgreen)

## RS Scanner – Python Port Automation Scanner

A fast Python port scanning tool designed to identify open network ports on a target domain, built for simplicity and clean terminal visualization.

---

## Project Summary
I built RS Scanner as a personal networking and cybersecurity tool to automate the process of scanning open ports on a target system.The scanner resolves domain names,fetches geolocation data and performs highly parallel threaded port scanning with a clean structured output using Rich CLI.

This project helped me better understand:
- Socket programming
- Multi-threading in Python
- Building interactive terminal CLI
- and strengthening my Python skills and applying them to real-world cybersecurity tasks
  
---

## What This Scanner Can Do
- Resolve domain names to IP addresses
- Display target city and country using ip-api
- Scan:Common ports (1–1023) and Full port range (1–65535)
- Detect open TCP ports
- Display the service of each port (80=http,22=ssh,etc.)
- Show results in styled tables using Rich
- Keep track of total scans completed and total open ports
- Loop mode (scan again without restarting app)

---

## How It Works
- You enter a domain (example: google.com)
- The program resolves it to an IP address
- It pulls basic geolocation information
- You choose a scan mode:Common ports:1–1023 or Full scan:1–65535
- A threaded scan starts
- All open ports are listed with detected services

---

## Screenshots

![Final Scan Visualization](images/Scan_Visualization.png)

<details>

</details>

---

## Tools & Technologies

- Python 
- Visual Studio Code
- In code:socket(network communication),concurrent.futures(multithreading),requests(geolocation API),rich(styled terminal CLI)
- Git & GitHub

---

## Skills & Lessons Learned 

- Automation 
- Networking fundamentals(Ports etc.)
- Thread pools and concurrency
- Domain resolution
- API integration
- Exception handling(socket.gaierror)
- Terminal UI design

---

## Legal Disclaimer
I made this tool for my own educational and authorized testing purposes only.Do not scan any system or network you do not own or have permission to test.You are fully responsible for how you use this software.

---

##Rakip 

Cyber Security Professional 

---
