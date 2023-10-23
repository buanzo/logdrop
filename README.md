# LogDrop
## Covert C2 using Public HTTP Access Logs / Indexed Command and Control / Ekoparty 2023

by Buanzo

# Abstract

Unveiled at Ekoparty 2023, LogDrop is a proof-of-concept tool. It highlights how an often-overlooked aspect of server security—publicly accessible access_log files—can be exploited for passive command and control (C2) operations.

# The Problem

Incorrectly configured web servers sometimes expose access logs to the public. LogDrop exposes this security flaw by demonstrating how these logs can be used for covert data storage and command execution.

Note: LogDrop is an original concept by Buanzo, created solely for educational purposes and will be featured at Ekoparty 2023. The technique was originally published in 2600 Magazine

# Key Commands

# logdrop write
## Description
Embeds data into a targeted access_log file by triggering a custom URL. You can modify the access_log_url variable so it is fed with appropriate targets for your testing environment. A "vulnerable_webserver.py" script is included that listens on http://localhost:8080 - This repo also includes htdocs folder, an index.html and the logs folder inside htdocs.

## Usage
logdrop write "NEEDLE" --data "DATA_TO_WRITE"

# logdrop search
## Description
Scans the specified access_log file for entries that match the hashed needle, decrypting and displaying any found data.

## Usage
logdrop search "NEEDLE"

# logdrop monitor
## Description
Continuously polls the specified access_log file for new entries that match the hashed needle. Decrypts and displays any found data at a specified interval.

## Usage
logdrop monitor "NEEDLE" --interval SECONDS

# Ethical Considerations and Limitations

1. Anyone Can Inject Commands: Without cryptographic integrity checks, anyone can issue commands if they know the needle.
2. Purpose and Intent: Designed for educational and research purposes, not for operational use.
3. Legal Concerns: This tool should only be used in authorized environments. Be aware of the legal implications.
