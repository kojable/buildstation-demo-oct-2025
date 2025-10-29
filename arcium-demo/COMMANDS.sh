#!/bin/bash
# Quick Command Reference - Copy/paste these commands

# ============================================
# SETUP (Run once)
# ============================================

# 1. Configure Solana for localnet
solana config set --url localhost
solana config get

# 2. Start validator (in separate terminal, keep running)
solana-test-validator

# 3. Check/airdrop balance
solana balance
solana airdrop 100  # if needed

# 4. Build and deploy program
cd ~/arcium-demo/anonymization_mxe
anchor build
anchor deploy

# 5. Start backend server
cd ~/arcium-demo/backend
yarn start

# ============================================
# TESTING
# ============================================

# Watch logs (in separate terminal)
solana logs

# Check balance before
solana balance

# Test the API
curl -X POST http://localhost:3000/api/anonymize \
  -H "Content-Type: application/json" \
  -d '{"url":"https://en.wikipedia.org/wiki/Albert_Einstein"}'

# Check balance after (should be lower)
solana balance

# ============================================
# MONITORING
# ============================================

# Check server health
curl http://localhost:3000/health | jq .

# View wallet info
curl http://localhost:3000/api/wallet | jq .

# View transaction history
curl http://localhost:3000/api/transactions | jq .

# Watch server logs
tail -f ~/arcium-demo/backend/server.log

# ============================================
# TROUBLESHOOTING
# ============================================

# Verify configuration
echo "Solana CLI:"
solana config get | grep RPC

echo ""
echo "Backend .env:"
cat ~/arcium-demo/backend/.env | grep ANCHOR

echo ""
echo "Anchor.toml:"
cat ~/arcium-demo/anonymization_mxe/Anchor.toml | grep cluster

echo ""
echo "Server health:"
curl -s http://localhost:3000/health | jq '.rpc_url'

# Restart everything
pkill solana-test-validator
sleep 2
solana-test-validator &
sleep 5
cd ~/arcium-demo/anonymization_mxe && anchor deploy
cd ~/arcium-demo/backend && pkill -f "node.*server" && yarn start

# ============================================
# SWITCH TO DEVNET (if needed)
# ============================================

# Update config files:
# backend/.env: ANCHOR_PROVIDER_URL=https://api.devnet.solana.com
# Anchor.toml: cluster = "devnet"

# Then:
solana config set --url devnet
solana airdrop 2
cd ~/arcium-demo/anonymization_mxe && anchor build && anchor deploy
cd ~/arcium-demo/backend && pkill -f "node.*server" && yarn start
solana logs
