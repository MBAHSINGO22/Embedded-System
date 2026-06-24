#!/usr/bin/env python3
"""
Smart Parking Sensor Monitor
Reads PCF8591 ADC (two channels), manages entry/exit state, writes to PostgreSQL.
"""
import time
import psycopg2
from smbus2 import SMBus
from datetime import datetime

# ===== CONFIGURABLE PARAMETERS =====
THRESHOLD = 130          # ADC value above which a car is considered present
ENTRY_TIME = 2.5         # seconds to confirm entry
EXIT_TIME = 3.0          # seconds to confirm exit
RATE_PER_MINUTE = 1000   # Rp per minute
MAX_FEE = 50000          # maximum fee in Rp
ADC_CHANNELS = {         # slot number -> PCF8591 analog channel
    1: 0,                # Slot 1 = AIN0
    2: 1                 # Slot 2 = AIN1
}
# ===================================

ADC_ADDRESS = 0x48
DB_CONN = "dbname=smart_parking user=parking_admin password=12345 host=localhost"

def read_adc(channel):
    """Read a single analog channel (0-255)."""
    bus.write_byte(ADC_ADDRESS, 0x40 | channel)
    bus.read_byte(ADC_ADDRESS)   # dummy read
    value = bus.read_byte(ADC_ADDRESS)
    return value

def calc_fee(entry_time, exit_time):
    """Calculate parking fee in Rupiah, capped at MAX_FEE."""
    duration_minutes = (exit_time - entry_time).total_seconds() / 60.0
    fee = duration_minutes * RATE_PER_MINUTE
    return min(fee, MAX_FEE)

def main():
    global bus
    bus = SMBus(1)

    # State per slot: 'state', 'above_start' (timer), 'car_id' (the active car)
    slots = {
        1: {'state': 'VACANT', 'above_start': None, 'car_id': None},
        2: {'state': 'VACANT', 'above_start': None, 'car_id': None}
    }

    # Global sequential car counter
    car_counter = 0

    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()

    try:
        while True:
            for slot_num, channel in ADC_CHANNELS.items():
                value = read_adc(channel)

                '''
                    DEBUG LINE
                '''

                value = read_adc(channel)

                voltage = value * (3.3 / 255)

                print(
                    f"Slot {slot_num}: {value:3} ({voltage:.2f}V) "
                    # f"State={slot['state']}"
                )

                '''
                    DEBUG LINE
                '''

                now = datetime.now()
                above = value > THRESHOLD
                slot = slots[slot_num]

                # -------- VACANT STATE --------
                if slot['state'] == 'VACANT':
                    if above:
                        slot['state'] = 'ENTERING'
                        slot['above_start'] = now

                # -------- ENTERING STATE --------
                elif slot['state'] == 'ENTERING':
                    if above:
                        if (now - slot['above_start']).total_seconds() >= ENTRY_TIME:
                            # Confirmed entry
                            car_counter += 1
                            car_id_str = f"CAR{car_counter}"
                            cur.execute(
                                "INSERT INTO parking_sessions (car_id, slot_number, entry_time) VALUES (%s, %s, %s)",
                                (car_id_str, slot_num, now)
                            )
                            conn.commit()
                            slot['car_id'] = car_id_str
                            slot['state'] = 'OCCUPIED'
                            print(f"Slot {slot_num}: {car_id_str} ENTERED")
                    else:
                        # False alarm, reset
                        slot['state'] = 'VACANT'
                        slot['above_start'] = None

                # -------- OCCUPIED STATE --------
                elif slot['state'] == 'OCCUPIED':
                    if not above:
                        slot['state'] = 'LEAVING'
                        slot['above_start'] = now

                # -------- LEAVING STATE --------
                elif slot['state'] == 'LEAVING':
                    if not above:
                        if (now - slot['above_start']).total_seconds() >= EXIT_TIME:
                            # Confirmed exit
                            cur.execute(
                                "UPDATE parking_sessions SET exit_time = %s WHERE car_id = %s",
                                (now, slot['car_id'])
                            )
                            # Fetch entry_time to compute fee
                            cur.execute(
                                "SELECT entry_time FROM parking_sessions WHERE car_id = %s",
                                (slot['car_id'],)
                            )
                            entry_time = cur.fetchone()[0]
                            fee = calc_fee(entry_time, now)
                            cur.execute(
                                "UPDATE parking_sessions SET fee = %s WHERE car_id = %s",
                                (fee, slot['car_id'])
                            )
                            conn.commit()
                            print(f"Slot {slot_num}: {slot['car_id']} EXITED, fee = Rp{fee:.2f}")
                            # Reset slot
                            slot['state'] = 'VACANT'
                            slot['above_start'] = None
                            slot['car_id'] = None
                    else:
                        # Car came back, cancel exit
                        slot['state'] = 'OCCUPIED'
                        slot['above_start'] = None

            time.sleep(0.1)  # poll every 100 ms

    except KeyboardInterrupt:
        print("Shutting down monitor...")
    finally:
        cur.close()
        conn.close()
        bus.close()

if __name__ == "__main__":
    main()