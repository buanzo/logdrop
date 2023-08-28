# LogDrop
## Covert C2 using public HTTP access logs / Indexed Command and Control / Ekoparty 2023

by Buanzo

### Abstract

LogDrop is a proof-of-concept tool developed by Buanzo and to be presented
at Ekoparty 2023.  This tool exploits publicly accessible `access_log` files
as a unique means for passive command-and-control propagation.

### The Problem
The Internet is full of web servers with bad security settings. One common mistake is making server
access logs public and easy to find. LogDrop shines a light on this issue by showing how these logs
can be used for hidden data storage and remote control operations.

LogDrop is a demo tool that proves you can use access_log files for sneaky command-and-control (C2)
actions. But, to keep it from being used for bad stuff, we've skipped adding any encryption features.
This guide walks you through what LogDrop can do and its limitations.

**Note:** This tool and method are original ideas by Buanzo, created for educational and demo use at Ekoparty 2023.

### Key Commands

#### `logdrop find`

##### Description
Scours the web using Google Dork to find `access_log` files containing a specific hash derived from a campaign
identifier (needle). Lists the most recent entries first. These could be responses, commands, etc.

##### Usage

```bash
logdrop find --needle "CAMPAIGN_IDENTIFIER"
```

Sends a predefined command to selected `access_log` files. This will hash the needle and the command, allowing
clients to find and recognize it.

##### Usage
```bash
logdrop push --needle "CAMPAIGN_IDENTIFIER" --command PING
```

Pushes the PING command into the campaign. Confirmation that the command was inserted into the targeted `access_log` files.

### List of Valid Commands
- `PING`: Ask clients to identify themselves by sending PONGs to the campaign.
- `PONG`: Response to PING from client[s].
- `DATA_DUMP`: Request data (not implemented).
- `SLEEP`: Put client to sleep for a specific duration (not implemented).
- `EXIT`: Terminate client (not implemented).


### Ethical Considerations and Limitations

1. **No Cryptographic Security**: This PoC avoids using cryptographic techniques to help clients validate commands, hence...:
2. **Anyone Can Inject Commands**: Given that there's no authentication or cryptographic integrity checks, anyone can issue commands to a campaign if they know the campaign identifier (needle).
3. **Purpose and Intent**: The primary aim is to demonstrate that the technique is feasible. It is not intended for actual C2 operations but for educational and research purposes.
4. **Legal Concerns**: Be aware of the legal implications and make sure you have proper authorization before using LogDrop.
