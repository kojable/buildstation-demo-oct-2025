#!/bin/bash

# Quick test script to verify everything is working

echo "========================================"
echo "🧪 Testing Arcium Anonymization API"
echo "========================================"

# Check server health
echo ""
echo "1. Checking server health..."
HEALTH=$(curl -s http://localhost:3000/health)
if [ $? -eq 0 ]; then
    echo "✅ Server is running"
    echo "$HEALTH" | jq '.' 2>/dev/null || echo "$HEALTH"
else
    echo "❌ Server is not responding"
    exit 1
fi

# Check wallet balance before
echo ""
echo "2. Wallet balance BEFORE test..."
BALANCE_BEFORE=$(solana balance | awk '{print $1}')
echo "Balance: $BALANCE_BEFORE SOL"

# Run anonymization test
echo ""
echo "3. Running anonymization test..."
echo "URL: https://en.wikipedia.org/wiki/Albert_Einstein"
echo ""

RESPONSE=$(curl -s -X POST http://localhost:3000/api/anonymize \
    -H "Content-Type: application/json" \
    -d '{"url":"https://en.wikipedia.org/wiki/Albert_Einstein"}')

# Parse response
if echo "$RESPONSE" | jq -e '.anonymization_applied' > /dev/null 2>&1; then
    echo "✅ Anonymization completed!"
    echo ""
    echo "Results:"
    echo "$RESPONSE" | jq '{
        url,
        pii_detected,
        anonymization_applied,
        total_sol_cost,
        processing_time_ms,
        wallet_address,
        transactions: (.transactions | length)
    }' 2>/dev/null
    
    echo ""
    echo "Anonymized PII:"
    echo "$RESPONSE" | jq -r '.anonymization_map[]? | "  \(.type): \(.original_redacted) → \(.token)"' 2>/dev/null
    
    echo ""
    echo "Transaction Signatures:"
    echo "$RESPONSE" | jq -r '.anonymization_map[]?.transaction_signature // empty' 2>/dev/null | while read -r sig; do
        echo "  https://explorer.solana.com/tx/$sig?cluster=custom&customUrl=http://localhost:8899"
    done
else
    echo "❌ Anonymization failed"
    echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
fi

# Check wallet balance after
echo ""
echo "4. Wallet balance AFTER test..."
BALANCE_AFTER=$(solana balance | awk '{print $1}')
echo "Balance: $BALANCE_AFTER SOL"

# Calculate cost
COST=$(echo "$BALANCE_BEFORE - $BALANCE_AFTER" | bc)
echo ""
echo "💰 Total cost: $COST SOL"

# Check transaction history
echo ""
echo "5. Recent transactions..."
curl -s http://localhost:3000/api/transactions | jq '.transactions[-3:]' 2>/dev/null

echo ""
echo "========================================"
echo "✅ Test Complete!"
echo "========================================"
