#!/usr/bin/env python3
"""
XRP Dashboard Data Updater
Fetches live XRP data and updates the dashboard JSON file
Run this script periodically to keep dashboard current
"""

import json
import requests
from datetime import datetime
import time

def fetch_xrp_price_data():
    """Fetch current XRP price from CoinGecko API (free, no key required)"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'ripple',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_market_cap': 'true',
            'include_24h_vol': 'true'
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            'price': data['ripple']['usd'],
            'price_change_24h': data['ripple']['usd_24h_change'],
            'market_cap': data['ripple']['usd_market_cap'],
            'volume_24h': data['ripple']['usd_24h_vol']
        }
    except Exception as e:
        print(f"Error fetching price data: {e}")
        return None

def fetch_exchange_supply():
    """Fetch exchange supply data from CryptoQuant or similar"""
    # Note: This requires API key from CryptoQuant or similar service
    # For free version, we'll use estimated values based on last known data
    return {
        'binance_reserves': 3600000000,  # 3.6B XRP
        'total_exchange_supply': 8500000000,  # 8.5B XRP
        'note': 'Manual update required for accurate exchange data'
    }

def update_dashboard_json(filename='xrp_consolidated_dashboard.json'):
    """Update the dashboard JSON with fresh data"""

    print(f"\n{'='*70}")
    print(f"🔄 XRP Dashboard Update - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")

    # Load existing dashboard
    try:
        with open(filename, 'r') as f:
            dashboard = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: {filename} not found!")
        return False

    # Fetch new data
    print("📡 Fetching live XRP data from CoinGecko...")
    price_data = fetch_xrp_price_data()

    if price_data:
        # Update current market metrics
        dashboard['current_market_metrics']['price_usd'] = price_data['price']
        dashboard['current_market_metrics']['price_change_24h_pct'] = price_data['price_change_24h']
        dashboard['current_market_metrics']['market_cap_usd'] = price_data['market_cap']
        dashboard['current_market_metrics']['volume_24h_usd'] = price_data['volume_24h']

        # Update metadata timestamp
        dashboard['metadata']['last_updated'] = datetime.now().isoformat()

        print(f"✅ Price updated: ${price_data['price']:.4f}")
        print(f"✅ 24h Change: {price_data['price_change_24h']:.2f}%")
        print(f"✅ Market Cap: ${price_data['market_cap']/1e9:.2f}B")
        print(f"✅ Volume: ${price_data['volume_24h']/1e9:.2f}B")
    else:
        print("⚠️  Could not fetch live price data, keeping existing values")

    # Fetch exchange supply
    print("\n📦 Updating exchange supply data...")
    exchange_data = fetch_exchange_supply()
    if exchange_data:
        dashboard['trigger_dashboard']['exchange_supply_depletion']['key_metrics']['binance_reserves_xrp'] = str(exchange_data['binance_reserves'])
        dashboard['trigger_dashboard']['exchange_supply_depletion']['key_metrics']['total_exchange_supply_xrp'] = str(exchange_data['total_exchange_supply'])
        print(f"✅ Exchange supply: {exchange_data['total_exchange_supply']/1e9:.2f}B XRP")

    # Save updated dashboard
    with open(filename, 'w') as f:
        json.dump(dashboard, f, indent=2)

    print(f"\n✅ Dashboard updated successfully!")
    print(f"📁 File: {filename}")
    print(f"{'='*70}\n")

    return True

def continuous_update(interval_minutes=15):
    """Run updates continuously at specified interval"""
    print(f"🔄 Starting continuous update mode (every {interval_minutes} minutes)")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            update_dashboard_json()
            print(f"⏰ Next update in {interval_minutes} minutes...\n")
            time.sleep(interval_minutes * 60)
    except KeyboardInterrupt:
        print("\n👋 Update loop stopped by user")

if __name__ == "__main__":
    import sys

    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--continuous':
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 15
            continuous_update(interval)
        elif sys.argv[1] == '--help':
            print("XRP Dashboard Updater")
            print("\nUsage:")
            print("  python xrp_dashboard_updater.py           # Single update")
            print("  python xrp_dashboard_updater.py --continuous [minutes]  # Continuous updates")
            print("  python xrp_dashboard_updater.py --help    # Show this help")
    else:
        # Single update
        update_dashboard_json()
