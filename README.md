# Distributed ICS Honeypot & Physical Process Simulator

This project implements a containerized farm of Modbus/TCP honeypots. It simulates industrial rectifiers with an integrated physics engine that ensures telemetry data responds realistically to control commands.

## Key Features
- Multi-Node Architecture: Deploys three independent sites (A, B, and C) using Docker Compose.
- Physical Process Simulation: Internal logic simulates battery discharge cycles. Turning off the virtual charger results in a calculated voltage decay in the registers.
- Interaction Logging: Automatically captures and timestamps all Modbus writes into CSV "traces" for forensic analysis.

## How to Run
```bash
docker-compose up --build -d

