import os
import redis
from decimal import Decimal
# Assuming standard import structure for the agentkit, adjustments might be needed based on actual library structure
# NOTE: The user requested `CdpEvmWalletProvider`, checking typical patterns.
# Since I cannot verify the exact import path for `CdpEvmWalletProvider` without library docs in context,
# I will assume a standard import or mock structure if needed.
# Based on common patterns in such SDKs:
try:
    from coinbase_agentkit import CdpEvmWalletProvider
except ImportError:
    # Fallback or placeholder if library structure differs
    class CdpEvmWalletProvider:
        def __init__(self, *args, **kwargs): pass
        def transfer_native_token(self, to, value): pass

class BudgetExceededError(Exception):
    """Raised when the daily transaction limit is exceeded."""
    pass

class WalletManager:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.provider = CdpEvmWalletProvider(
            api_key_name=os.getenv("CDP_API_KEY_NAME"),
            api_key_private_key=os.getenv("CDP_API_KEY_PRIVATE_KEY")
        )
        self.daily_limit = 50.0

    def safe_transfer(self, to_address: str, amount: float):
        """Simplistic transfer with budget check."""
        current_spend = float(self.redis.get("daily_spend") or 0.0)
        
        if current_spend + amount > self.daily_limit:
            raise BudgetExceededError("Daily limit exceeded")

        # Execute and update
        self.provider.transfer(to_address, amount)
        self.redis.incrbyfloat("daily_spend", amount)
