"""
PROJECT: NEXUS WATCH - CALIBRATION PROTOCOL (V2.1.1)
MODE: LIVE MONITORING (UTC SYNCHRONIZED)
OBJECTIVE: Proof of Concept generation with dynamic filtering and block auditing.
CONFIDENTIAL: INTERNAL USE ONLY - VERIOMNION SOLUTIONS
"""

import time
import logging
import sys
from web3 import Web3 # type: ignore

# --- INFRASTRUCTURE CONFIGURATION ---
RPC_URL = "https://arb-mainnet.g.alchemy.com/v2/fNwp7fwu5JXPCXHx-556N"

# Dynamic Scaling Phases
current_threshold = 10 
capture_count = 245    

# Log Configuration (Audit Trail - UTC Standard)
logging.Formatter.converter = time.gmtime 
logging.basicConfig(
    filename='NEXUS_CALIBRATION_LOG.txt',
    level=logging.INFO, 
    format='%(asctime)s UTC - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

DISCLAIMER = "NEXUS OMNIA DATA - CALIBRATION MODE. INTERNAL USE ONLY."

def connect_blockchain():
    """Secure Connection Handshake"""
    print("\nInitializing NEXUS WATCH Protocol v2.1.1...")
    print("------------------------------------------------")
    print(f"Target Network: ARBITRUM ONE")
    print(f"RPC Endpoint: SECURE_WSS_GATEWAY (Alchemy)")
    print(f"Time Sync: UTC ENABLED")
    print("------------------------------------------------")
    try:
        w3 = Web3(Web3.HTTPProvider(RPC_URL))
        if w3.is_connected():
            print(f"✅ [SYSTEM] Secure Connection Established!")
            print(f"📡 Current Block Height: {w3.eth.block_number}")
            logging.info(f"STARTING CALIBRATION SEQUENCE. {DISCLAIMER}")
            logging.info(f"--- PHASE 1 STARTED: Filter set to {current_threshold} ETH ---")
            return w3
        return None
    except Exception as e:
        print(f"❌ [CRITICAL ERROR] Connection Failed: {e}")
        return None

def check_phase_update():
    """Dynamic Phase Scaling Logic"""
    global current_threshold
    if capture_count >= 250 and current_threshold == 10:
        current_threshold = 50
        msg = f"\n🔄 [AUTO-SCALING] Threshold trigger reached (250). Elevating Filter to {current_threshold} ETH (PHASE 2).\n"
        print(msg)
        logging.info(msg)
    elif capture_count >= 500 and current_threshold == 50:
        current_threshold = 100
        msg = f"\n🔄 [AUTO-SCALING] Threshold trigger reached (500). Elevating Filter to {current_threshold} ETH (PHASE 3).\n"
        print(msg)
        logging.info(msg)

def monitor_transactions(w3):
    global capture_count
    print(f"\n🕵️ [NEXUS KERNEL] Starting Engine at Threshold: {current_threshold} ETH")
    print("⏳ Listening for pending blocks via RPC Stream...\n")
    last_block = w3.eth.block_number
    while True:
        try:
            current_block = w3.eth.block_number
            if current_block > last_block:
                try:
                    block_data = w3.eth.get_block(current_block, full_transactions=True)
                    tx_count = len(block_data.transactions)
                    print(f"   > [SCANNING] Block {current_block} | Parsing {tx_count} transactions...", end="\r")
                    sys.stdout.flush() 
                except:
                    time.sleep(1)
                    continue

                for tx in block_data.transactions:
                    if tx['value'] > 0:
                        eth_value = float(w3.from_wei(tx['value'], 'ether'))
                        if eth_value >= current_threshold:
                            capture_count += 1
                            evidence = (
                                f" >>> [ALERT] #{capture_count} | BLOCK: {current_block} | "
                                f"VAL: {eth_value:.2f} ETH | "
                                f"HASH: {tx['hash'].hex()}"
                            )
                            print(f"\n⚡ {evidence}")
                            logging.info(evidence)
                            check_phase_update()
                last_block = current_block
            time.sleep(2) 
        except Exception:
            time.sleep(3)

if __name__ == "__main__":
    w3_connection = connect_blockchain()
    if w3_connection:
        try:
            monitor_transactions(w3_connection)
        except KeyboardInterrupt:
            print("\n🛑 [SYSTEM] User Interrupt. Closing Secure Connection.")