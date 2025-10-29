#!/bin/bash

# Quick Setup Script for Localnet Testing
# Run this on your Ubuntu server

echo "========================================"
echo "🔧 Setting up Solana Localnet"
echo "========================================"

# Configure Solana CLI
echo "1. Configuring Solana CLI for localnet..."
solana config set --url localhost

# Show configuration
echo ""
echo "Current Solana Configuration:"
solana config get

# Check if validator is running
echo ""
echo "2. Checking if solana-test-validator is running..."
if pgrep -x "solana-test-val" > /dev/null; then
    echo "✅ Validator is running"
else
    echo "❌ Validator is NOT running!"
    echo ""
    echo "Please start it in a separate terminal:"
    echo "  solana-test-validator"
    echo ""
    read -p "Press Enter once validator is running..."
fi

# Check wallet balance
echo ""
echo "3. Checking wallet balance..."
BALANCE=$(solana balance 2>/dev/null | awk '{print $1}')
echo "Current balance: $BALANCE SOL"

if (( $(echo "$BALANCE < 10" | bc -l) )); then
    echo "⚠️  Balance is low, airdropping 100 SOL..."
    solana airdrop 100
fi

# Build and deploy program
echo ""
echo "4. Building and deploying Anchor program..."
cd ~/arcium-demo/anonymization_mxe || exit 1

echo "  Building..."
anchor build

echo "  Deploying to localnet..."
anchor deploy

# Restart backend
echo ""
echo "5. Restarting backend server..."
cd ~/arcium-demo/backend || exit 1

# Kill existing server
pkill -f "node.*server" 2>/dev/null || true
sleep 2

# Start server in background
echo "  Starting server..."
nohup yarn start > server.log 2>&1 &
SERVER_PID=$!
echo "  Server PID: $SERVER_PID"

# Wait for server to start
echo "  Waiting for server to initialize..."
sleep 5

# Check if server is running
if ps -p $SERVER_PID > /dev/null; then
    echo "  ✅ Server started successfully"
    echo "  Logs: tail -f ~/arcium-demo/backend/server.log"
else
    echo "  ❌ Server failed to start"
    echo "  Check logs: cat ~/arcium-demo/backend/server.log"
    exit 1
fi

echo ""
echo "========================================"
echo "✅ Setup Complete!"
echo "========================================"
echo ""
echo "📊 Status:"
echo "  Cluster: Localnet (http://localhost:8899)"
echo "  Wallet: $(solana address)"
echo "  Balance: $(solana balance)"
echo "  Backend: http://localhost:3000"
echo ""
echo "🔍 To watch transaction logs:"
echo "  solana logs"
echo ""
echo "🧪 To test the API:"
echo '  curl -X POST http://localhost:3000/api/anonymize \'
echo '    -H "Content-Type: application/json" \'
echo '    -d '"'"'{"url":"https://en.wikipedia.org/wiki/Albert_Einstein"}'"'"
echo ""
echo "📝 View server logs:"
echo "  tail -f ~/arcium-demo/backend/server.log"
echo ""
echo "========================================"
