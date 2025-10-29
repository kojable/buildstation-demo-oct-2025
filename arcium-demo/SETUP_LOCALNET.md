# Setup Guide for Localnet Testing

## What Was Wrong?

Your configuration was pointing to **devnet** (`https://api.devnet.solana.com`), but you were running `solana logs` on **localnet** (localhost:8899). The transactions were happening on devnet, so you couldn't see logs and your local balance wasn't changing.

## Quick Fix - Use Localnet

I've updated your configuration to use **localnet** for development. This is faster, free, and easier to debug.

## Setup Steps (Run on Ubuntu Server)

### 1. Make sure Solana test validator is running

```bash
# In a separate terminal, start the validator if not already running
solana-test-validator

# Keep this running!
```

### 2. Configure Solana CLI for localnet

```bash
# Set to localnet
solana config set --url localhost

# Verify it's set correctly
solana config get

# You should see: RPC URL: http://localhost:8899
```

### 3. Check your wallet balance (should be 500M SOL on localnet)

```bash
solana balance
```

### 4. Build and deploy the program to localnet

```bash
cd ~/arcium-demo/anonymization_mxe

# Build the program
anchor build

# Deploy to localnet
anchor deploy
```

### 5. Restart your backend server

```bash
cd ~/arcium-demo/backend

# Kill the old server
pkill -f "node.*server.ts"

# Start fresh
yarn start
```

### 6. Now open a NEW terminal to watch logs

```bash
# This will show transactions in real-time
solana logs
```

### 7. Test the API

```bash
# In another terminal
curl -X POST http://localhost:3000/api/anonymize \
  -H "Content-Type: application/json" \
  -d '{"url":"https://en.wikipedia.org/wiki/Albert_Einstein"}'
```

## Expected Result

Now you should see:
- ✅ Logs appearing in `solana logs` terminal
- ✅ Balance decreasing slightly (transaction fees)
- ✅ Transaction signatures being logged
- ✅ Explorer links working

## Troubleshooting

### If balance still doesn't change:

```bash
# Airdrop more SOL to your wallet
solana airdrop 10

# Check balance
solana balance
```

### If you still don't see logs:

```bash
# Make sure validator is running
ps aux | grep solana-test-validator

# Check that CLI is pointing to localnet
solana config get

# Make sure backend is using correct RPC
cat ~/arcium-demo/backend/.env | grep ANCHOR
```

### To switch back to Devnet later:

1. Update `.env`:
   ```bash
   ANCHOR_PROVIDER_URL=https://api.devnet.solana.com
   ```

2. Update `Anchor.toml`:
   ```toml
   [provider]
   cluster = "devnet"
   ```

3. Set Solana CLI:
   ```bash
   solana config set --url devnet
   solana logs
   ```

## Cost Comparison

- **Localnet**: FREE, instant, ~500M SOL available
- **Devnet**: FREE, but requires airdrops (limited to 2 SOL per request)
- **Mainnet**: Real SOL costs money

For development and testing, **always use localnet first**!

## Next Steps

Once everything works on localnet:
1. Test thoroughly
2. Then deploy to devnet for staging
3. Finally deploy to mainnet for production

---

**Current Configuration**: 
- ✅ Backend `.env` → `ANCHOR_PROVIDER_URL=http://localhost:8899`
- ✅ `Anchor.toml` → `cluster = "localnet"`
- ✅ Ready to use localnet!
