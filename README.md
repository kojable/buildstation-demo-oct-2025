# Arcium PII Anonymization Demo

Privacy-preserving data processing using Multi-Party Computation (MPC) on Solana. This demo shows how to anonymize personally identifiable information (PII) from web content without exposing sensitive data to any single party.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Solana](https://img.shields.io/badge/Solana-Devnet-blueviolet)](https://solana.com)
[![Arcium](https://img.shields.io/badge/Arcium-MPC-orange)](https://arcium.com)

## 🔐 What This Demo Does

Takes a URL, scrapes its content, detects PII (names, emails, phones), and anonymizes it using Arcium's Multi-Party Computation network—ensuring the original sensitive data is never exposed in plaintext to any single party.

### Example Flow:

```
Input:  "Albert Einstein was a theoretical physicist..."
Output: "ARX-73f2a9e4c5b6d8f1 was a theoretical physicist..."
```

**Key Innovation:** The name "Albert Einstein" is encrypted, split into shares, and processed by multiple MPC nodes. No single node ever sees the plaintext—yet they collaboratively compute an anonymized token.

---

## 🏗️ Architecture

```
┌─────────────────┐
│  Web Frontend   │ React (Optional)
│   (Browser)     │
└────────┬────────┘
         │ HTTP POST
         ↓
┌─────────────────┐
│  Backend API    │ Node.js + Express
│   (AWS EC2)     │ Port 3000
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ↓         ↓
┌────────┐ ┌──────────────┐
│Scraper │ │ PII Detector │
└────────┘ └──────┬───────┘
                  │ Encrypted Shares
                  ↓
         ┌────────────────┐
         │  Arcium MPC    │ Multi-Party Computation
         │    Network     │ (Distributed Nodes)
         └────────┬───────┘
                  │ ARX Token
                  ↓
         ┌────────────────┐
         │ Solana Devnet  │ Coordination Layer
         └────────────────┘
```

---

## 📋 Prerequisites

### System Requirements

- **OS:** Ubuntu 24.04 LTS (recommended)
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 30GB free space
- **Network:** Stable internet connection for RPC calls

### Required Software

- **Node.js:** v20.x or higher
- **Rust:** Latest stable (1.85.0+)
- **Solana CLI:** v1.18.x or higher
- **Anchor:** v0.30.1 or v0.31.1
- **Yarn:** Latest stable
- **Docker:** Latest (optional, for local Arx nodes)

---

## 🚀 Quick Start (30 Minutes)

### Step 1: System Setup

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install essential dependencies
sudo apt-get install -y \
  pkg-config \
  build-essential \
  libudev-dev \
  libssl-dev \
  curl \
  git \
  wget \
  ca-certificates
```

### Step 2: Install Rust

```bash
# Install Rust using rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Select option 1 (default installation)

# Add Rust to PATH
source $HOME/.cargo/env

# Verify installation
rustc --version
cargo --version
```

### Step 3: Install Solana CLI

```bash
# Install Solana CLI
sh -c "$(curl -sSfL https://release.solana.com/v1.18.22/install)"

# Add to PATH
export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"
echo 'export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"' >> ~/.bashrc

# Verify installation
solana --version

# Configure for Devnet
solana config set --url https://api.devnet.solana.com

# Create wallet
solana-keygen new --outfile ~/wallet-keypair.json

# IMPORTANT: Save the seed phrase shown!

# Request free Devnet SOL
solana airdrop 2

# Check balance
solana balance
```

### Step 4: Install Node.js v20

```bash
# Install Node.js 20.x LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version  # Should be v20.x.x
npm --version

# Install Yarn globally
sudo npm install -g yarn

# Verify Yarn
yarn --version
```

### Step 5: Install Arcium Tooling

```bash
# Install arcup (Arcium version manager)
curl --proto '=https' --tlsv1.2 -sSfL https://arcium-install.arcium.workers.dev/ | bash

# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Install Arcium CLI
arcup install

# Verify installation
arcium --version
arcup version
```

### Step 6: Install Anchor

```bash
# Install AVM (Anchor Version Manager)
cargo install --git https://github.com/coral-xyz/anchor avm --locked --force

# This takes 10-15 minutes - be patient!

# Install Anchor
avm install 0.31.1
avm use 0.31.1

# Verify installation
anchor --version
```

---

## 📦 Project Setup

### Clone the Repository

```bash
# Clone the project
git clone https://github.com/your-username/arcium-anonymization-demo.git
cd arcium-anonymization-demo
```

### Project Structure

```
arcium-anonymization-demo/
├── anonymization-mxe/          # Arcium MPC program
│   ├── programs/               # Solana program code
│   │   └── anonymization_mxe/
│   │       ├── src/
│   │       │   └── lib.rs      # Solana program entry point
│   │       └── Cargo.toml
│   ├── encrypted-ixs/          # Confidential instructions
│   │   └── anonymize_pii.rs    # MPC anonymization logic
│   ├── Arcium.toml             # Arcium configuration
│   ├── Anchor.toml             # Anchor configuration
│   └── Cargo.toml              # Rust dependencies
├── backend/                    # Node.js API server
│   ├── src/
│   │   └── server.ts           # Express API with 5-stage pipeline
│   ├── .env                    # Environment configuration
│   ├── package.json
│   └── tsconfig.json
├── frontend/                   # React web app (optional)
│   └── (React components)
├── diagrams/                   # Flow diagrams
│   └── arcium_flow_diagrams.html
└── README.md                   # This file
```

---

## 🔧 Build Instructions

### Part 1: Build Arcium MPC Program

```bash
cd anonymization-mxe

# Install dependencies
yarn install

# IMPORTANT: Handle Rust toolchain issues
# Remove rust-toolchain.toml to use your system Rust
rm -f rust-toolchain.toml

# Set Rust to latest stable
rustup default stable
rustc --version  # Should be 1.85.0 or higher

# Update Anchor.toml for Devnet
sed -i 's/\[programs.localnet\]/[programs.devnet]/' Anchor.toml
sed -i 's/cluster = "localnet"/cluster = "devnet"/' Anchor.toml
sed -i "s|wallet = \"~/.config/solana/id.json\"|wallet = \"$HOME/wallet-keypair.json\"|" Anchor.toml

# Build the encrypted instruction
arcium build
```

**Expected Output:**
```
✓ Built encrypted instruction at build/anonymize_pii.arcis
```

**Note:** If `anchor build` fails with Cargo.lock version errors, this is a known issue. The encrypted instruction (the MPC part) will still build successfully. You can continue to the backend setup.

### Part 2: Deploy to Solana Devnet (Optional)

```bash
# Deploy the program
arcium deploy --network devnet

# Save your Program ID from the output
# Example: 8xK7V2W3nRpQmYzBvDfE5gHjKlMnOpQ1rStUvWxYz123
```

### Part 3: Build Backend API

```bash
cd ../backend

# Install dependencies
npm install

# Create .env file
cat > .env << 'EOF'
# Solana Configuration
SOLANA_RPC_URL=https://api.devnet.solana.com
WALLET_KEYPAIR_PATH=/home/your-username/wallet-keypair.json

# Arcium Configuration
ARCIUM_PROGRAM_ID=6gvQzjsAbVy44Bnhw362r6HSVg9eT3bHknKS2YZ8JfTV

# Server Configuration
PORT=3000
NODE_ENV=development
EOF

# IMPORTANT: Update the wallet path with your actual username
nano .env  # Edit WALLET_KEYPAIR_PATH

# Build TypeScript
npm run build

# Verify build succeeded
ls dist/server.js  # Should exist
```

---

## ▶️ Running the Demo

### Start the Backend Server

```bash
cd backend

# Start the server
npm start
```

**Expected Output:**
```
========================================
🚀 Arcium Anonymization API
========================================
Server: http://localhost:3000
Health: http://localhost:3000/health
========================================
```

### Test the API

**In a new terminal:**

```bash
# Health check
curl http://localhost:3000/health

# Test anonymization with Albert Einstein Wikipedia page
curl -X POST http://localhost:3000/api/anonymize \
  -H "Content-Type: application/json" \
  -d '{"url":"https://en.wikipedia.org/wiki/Albert_Einstein"}' \
  | jq '.'
```

**Expected Response:**
```json
{
  "url": "https://en.wikipedia.org/wiki/Albert_Einstein",
  "timestamp": "2025-10-25T15:30:00Z",
  "anonymization_applied": true,
  "pii_detected": 7,
  "content": {
    "title": "Albert Einstein - Wikipedia",
    "body": "ARX-73f2a9e4c5b6d8f1 was a theoretical physicist..."
  },
  "anonymization_map": [
    {
      "position": 0,
      "type": "person_name",
      "token": "ARX-73f2a9e4c5b6d8f1",
      "original_redacted": "A***** E********"
    }
  ],
  "processing_time_ms": 4820,
  "demo_note": "This demo uses simulated Arcium MPC..."
}
```

### Run as Background Service (Production)

```bash
# Install PM2 globally
sudo npm install -g pm2

# Start backend with PM2
cd backend
pm2 start dist/server.js --name arcium-backend

# Check status
pm2 status

# View logs
pm2 logs arcium-backend

# Make it start on boot
pm2 startup
pm2 save

# Stop/restart commands
pm2 stop arcium-backend
pm2 restart arcium-backend
```

---

## 🌐 API Documentation

### Endpoints

#### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-25T15:30:00Z",
  "service": "Arcium Anonymization API",
  "version": "1.0.0"
}
```

#### `POST /api/anonymize`

Anonymize PII from a webpage.

**Request:**
```json
{
  "url": "https://example.com/page-with-pii"
}
```

**Response:**
```json
{
  "url": "string",
  "timestamp": "ISO8601",
  "original_content_hash": "sha256:...",
  "anonymization_applied": true,
  "pii_detected": 5,
  "content": {
    "title": "string",
    "body": "string (with ARX tokens)"
  },
  "anonymization_map": [
    {
      "position": 0,
      "type": "person_name | email | phone_number",
      "token": "ARX-...",
      "original_redacted": "J*** D**"
    }
  ],
  "arcium_computation_id": "comp_...",
  "processing_time_ms": 4820
}
```

**Error Response:**
```json
{
  "error": "Error message",
  "details": "Detailed error information"
}
```

---

## 🔍 Understanding the Code

### Five-Stage Pipeline

The backend (`backend/src/server.ts`) implements a 5-stage pipeline:

#### **Stage 1: URL Input**
User submits a URL via POST request to `/api/anonymize`.

#### **Stage 2: Content Extraction**
```typescript
async function scrapeWebpage(url: string): Promise<ScrapedContent> {
  const response = await axios.get(url);
  const $ = cheerio.load(response.data);
  // Extract and clean content
  return { url, title, body, timestamp };
}
```

#### **Stage 3: PII Detection**
```typescript
function detectPII(content: string): PiiDetection[] {
  // Regex patterns for names, emails, phones
  const namePattern = /\b[A-Z][a-z]+ [A-Z][a-z]+\b/g;
  const emailPattern = /\b[\w.%+-]+@[\w.-]+\.[A-Z|a-z]{2,}\b/g;
  // ... detect and return positions
}
```

#### **Stage 4: Arcium Anonymization**
```typescript
async function anonymizeWithArcium(piiValue: string): Promise<AnonymizationResult> {
  // In production: encrypt, send to Arcium MPC network
  // Demo version: simulate with deterministic hash
  const hash = crypto.createHash('sha256').update(piiValue).digest('hex');
  const token = `ARX-${hash.substring(0, 16)}`;
  return { anonymized_token: token, ... };
}
```

#### **Stage 5: JSON Assembly**
```typescript
async function assembleFinalJSON(...): Promise<FinalOutput> {
  // Replace PII with ARX tokens
  // Generate metadata and proof
  return { url, content, anonymization_map, ... };
}
```

### Confidential Instruction (MPC Logic)

The core anonymization happens in `anonymization-mxe/encrypted-ixs/anonymize_pii.rs`:

```rust
#[arcium::encrypted_ix]
pub fn anonymize_pii(
    input_ctxt: &InputContext,
    pii_data: Enc<Shared, PiiInput>,
) -> EncryptionOutput<PiiOutput> {
    // This runs in Multi-Party Computation
    // No single node sees the plaintext
    let encrypted_string = pii_data.get_field::<String>("value");
    
    // Compute on encrypted data
    let hash = encrypted_string.secure_hash();
    let token = format!("ARX-{}", hash.to_hex()[..16]);
    
    // Return encrypted result
    input_ctxt.owner.from_arcis(PiiOutput {
        anonymized_token: token,
    })
}
```

**Key Point:** This code runs across multiple MPC nodes. Each node only sees an encrypted share—never the plaintext "John Doe".

---

## 🐛 Troubleshooting

### Issue: `anchor build` fails with Cargo.lock version error

**Error:**
```
error: failed to parse lock file
lock file version 4 requires `-Znext-lockfile-bump`
```

**Solution:**
The encrypted instruction should still build successfully. If you need the full Solana program:

```bash
# Option 1: Use older Rust version
rustup install 1.82.0
rustup override set 1.82.0
rm Cargo.lock
cargo generate-lockfile
sed -i 's/version = 4/version = 3/' Cargo.lock
anchor build

# Option 2: Continue with backend only
# The demo works with simulated MPC for testing
```

### Issue: Solana airdrop fails

**Solution:**
```bash
# Use web faucet instead
echo "Visit: https://faucet.solana.com"
solana address  # Copy this address to faucet
```

### Issue: Backend fails to start

**Check:**
```bash
# 1. Port already in use
sudo lsof -i :3000
# Kill process if needed: sudo kill -9 <PID>

# 2. Verify .env file exists and has correct paths
cat backend/.env

# 3. Check wallet file exists
ls ~/wallet-keypair.json

# 4. View error logs
cd backend
npm start 2>&1 | tee error.log
```

### Issue: PII not detected

**Cause:** Website blocks scrapers or has no detectable PII.

**Solution:**
```bash
# Test with known-good URLs
curl -X POST http://localhost:3000/api/anonymize \
  -H "Content-Type: application/json" \
  -d '{"url":"https://en.wikipedia.org/wiki/Marie_Curie"}'
```

### Issue: "Cannot find module" errors

**Solution:**
```bash
cd backend
rm -rf node_modules package-lock.json
npm install
npm run build
npm start
```

---

## 🧪 Testing

### Run Backend Tests

```bash
cd backend

# Test health endpoint
curl http://localhost:3000/health

# Test with sample URL
curl -X POST http://localhost:3000/api/anonymize \
  -H "Content-Type: application/json" \
  -d '{"url":"https://en.wikipedia.org/wiki/Albert_Einstein"}' \
  | jq '.pii_detected'
```

### Test Different PII Types

```bash
# Test person names
curl -X POST http://localhost:3000/api/anonymize \
  -H "Content-Type: application/json" \
  -d '{"url":"https://en.wikipedia.org/wiki/Marie_Curie"}' \
  | jq '.anonymization_map[] | select(.type=="person_name")'

# Test multiple PII types
curl -X POST http://localhost:3000/api/anonymize \
  -H "Content-Type: application/json" \
  -d '{"url":"https://en.wikipedia.org/wiki/Steve_Jobs"}' \
  | jq '.anonymization_map'
```

---

## 📊 Viewing Flow Diagrams

Open the interactive flow diagrams in your browser:

```bash
# If on local machine
xdg-open diagrams/arcium_flow_diagrams.html

# If on remote server, copy to local machine
scp -i your-key.pem ubuntu@your-ec2-ip:~/arcium-demo/diagrams/arcium_flow_diagrams.html .
# Then open in browser
```

The diagrams show:
1. **User Flow** - 5-stage pipeline
2. **System Architecture** - Component interaction
3. **Data Flow** - PII transformation journey
4. **MPC Deep Dive** - How Multi-Party Computation works

---

## 🚀 Deployment to AWS EC2

### Launch EC2 Instance

1. **Instance Type:** t3.medium (2 vCPU, 4GB RAM)
2. **OS:** Ubuntu 22.04 or 24.04 LTS
3. **Storage:** 30GB gp3
4. **Security Group:**
   - SSH (22) from your IP
   - HTTP (80) from anywhere (optional)
   - Custom TCP (3000) from anywhere

### Setup on EC2

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Follow "Quick Start" steps 1-6 above
# Then clone and build project

# Allow external access to port 3000
sudo ufw allow 3000/tcp
```

### Access from External

```bash
# From your local machine
curl -X POST http://YOUR_EC2_PUBLIC_IP:3000/api/anonymize \
  -H "Content-Type: application/json" \
  -d '{"url":"https://en.wikipedia.org/wiki/Albert_Einstein"}'
```

---

## 💰 Cost Breakdown

### Development (Free Tier)

- **Solana Devnet:** FREE (unlimited)
- **Arcium Testnet:** FREE (no fees)
- **AWS EC2 t2.micro:** FREE (750 hours/month first year)
- **Total:** $0/month

### Production Estimate

- **AWS EC2 t3.medium:** ~$30-50/month
- **Arcium MPC (Mainnet):** ~$0.01-0.10 per computation
- **Solana transactions:** ~$0.00025 per transaction
- **Total for 10K operations/month:** ~$150-200

---

## 🔐 Security Considerations

### What's Private (MPC Protected)

- ✅ Original PII strings ("John Doe", emails, phones)
- ✅ Intermediate computation values
- ✅ Individual MPC node shares

### What's Public (Not Protected)

- ❌ ARX tokens (anonymized identifiers)
- ❌ PII positions in text
- ❌ PII types (name, email, etc.)
- ❌ Metadata (timestamps, URLs)

### Threat Model

**Protected Against:**
- Single node compromise
- AWS infrastructure compromise
- Backend server compromise (after encryption boundary)

**Requires 2/3 Nodes to Break:**
- Coordinated multi-party attack
- Collusion between MPC operators

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📚 Resources

- **Arcium Documentation:** https://docs.arcium.com
- **Solana Documentation:** https://docs.solana.com
- **Anchor Framework:** https://www.anchor-lang.com
- **Technical Pitch Deck:** See `docs/pitch.md`
- **Flow Diagrams:** See `diagrams/arcium_flow_diagrams.html`

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Arcium** for the MPC framework
- **Solana** for the blockchain coordination layer
- **Anchor** for the Solana development framework

---

## 📧 Support

- **Issues:** https://github.com/kojable/buildstation-demo-oct-2025/issues
- **Discussions:** https://github.com/kojable/buildstation-demo-oct-2025/discussions
- **Arcium Discord:** https://discord.gg/arcium

---

## 🎯 Next Steps

1. **Enhance PII Detection:** Add NLP models (spaCy, Hugging Face)
2. **Add More PII Types:** Addresses, credit cards, SSNs
3. **Build React Frontend:** User-friendly web interface
4. **Production Deployment:** Move to Mainnet with real MPC
5. **Add Authentication:** Secure API with JWT tokens
6. **Implement Caching:** Redis for frequently accessed data

---

**Built with ❤️ using Arcium, Solana, and Multi-Party Computation**