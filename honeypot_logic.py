from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
import threading
import time
import csv
import datetime
import os

# --- LOGGING SETUP (Abstract 14: Analysis of Traces) ---
LOG_FILE = f"attack_log_{os.uname()[1]}.csv"

def log_interaction(address, value, action):
    with open(LOG_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now(), address, value, action])

# --- INDUSTRIAL LOGIC (Abstract 12) ---
class RectifierSim:
    def __init__(self):
        self.voltage = 5400 
        self.charger_on = True

    def physics_engine(self):
        while True:
            if not self.charger_on and self.voltage > 4200:
                self.voltage -= 10 
            elif self.charger_on and self.voltage < 5400:
                self.voltage += 5
            time.sleep(1)

sim = RectifierSim()
threading.Thread(target=sim.physics_engine, daemon=True).start()

# --- MODBUS REGISTER MAPPING ---
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*10),
    co=ModbusSequentialDataBlock(0, [1]*10), 
    hr=ModbusSequentialDataBlock(0, [0]*10),
    ir=ModbusSequentialDataBlock(0, [0]*10)
)
context = ModbusServerContext(slaves=store, single=True)

def update_registers():
    last_charger_state = True
    while True:
        store.setValues(4, 0, [sim.voltage]) 
        current_charger_state = bool(store.getValues(1, 0, 1)[0])
        
        # LOGGING: If the state changed, log the "Attack"
        if current_charger_state != last_charger_state:
            action = "CHARGER_ON" if current_charger_state else "CHARGER_OFF"
            log_interaction(0, int(current_charger_state), action)
            print(f"ALERT: Command Received - {action}")
            last_charger_state = current_charger_state
            
        sim.charger_on = current_charger_state
        time.sleep(0.5)

threading.Thread(target=update_registers, daemon=True).start()

print(f"Honeypot Active. Logging to {LOG_FILE}...")
StartTcpServer(context=context, address=("0.0.0.0", 5020))
