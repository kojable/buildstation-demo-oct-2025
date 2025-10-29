#!/bin/bash

# Monitoring Script - Run this to see everything happening in real-time

echo "========================================"
echo "📊 Solana Transaction Monitor"
echo "========================================"
echo ""
echo "Cluster: $(solana config get | grep 'RPC URL' | awk '{print $3}')"
echo "Wallet: $(solana address)"
echo "Balance: $(solana balance)"
echo ""
echo "Watching transactions in real-time..."
echo "Press Ctrl+C to stop"
echo "========================================"
echo ""

# Watch solana logs with timestamps
solana logs --include-votes 2>&1 | while read -r line; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $line"
done
