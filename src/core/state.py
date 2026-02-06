import redis
from redis.exceptions import WatchError
from ..models import GlobalState

class StateConflictError(Exception):
    """Raised when an optimistic locking conflict occurs."""
    pass

class StateManager:
    def __init__(self, redis_client: redis.Redis, state_key: str = "global_state"):
        self.redis = redis_client
        self.state_key = state_key

    def get_state(self) -> GlobalState:
        """Fetches the current state from Redis."""
        data = self.redis.get(self.state_key)
        if not data:
            return GlobalState()
        return GlobalState.model_validate_json(data)

    def commit_state(self, new_state: GlobalState, expected_version: int):
        """
        Commits a new state to Redis using Optimistic Concurrency Control.
        
        Args:
            new_state: The new state object to save.
            expected_version: The version we expect to exist in Redis.
            
        Raises:
            StateConflictError: If the Redis version doesn't match expected_version
                                or if a concurrent update occurs.
        """
        with self.redis.pipeline() as pipe:
            while True:
                try:
                    # WATCH the key for changes
                    pipe.watch(self.state_key)
                    
                    # Fetch current state (immediate mode in redis-py pipeline after watch)
                    current_data = pipe.get(self.state_key)
                    
                    if current_data:
                        current_state = GlobalState.model_validate_json(current_data)
                        current_version = current_state.version
                    else:
                        current_version = 0

                    if current_version != expected_version:
                        pipe.unwatch()
                        # If the versions don't match, we fail immediately.
                        # This happens if:
                        # 1. Caller is stale (logic error or race lost).
                        # 2. We retried after a WatchError and now see a newer version.
                        raise StateConflictError(
                            f"Version mismatch: expected {expected_version}, got {current_version}"
                        )

                    # Update version
                    new_state.version = current_version + 1
                    
                    # Execute transaction
                    pipe.multi()
                    pipe.set(self.state_key, new_state.model_dump_json())
                    pipe.execute()
                    
                    # If we reach here, success
                    return
                    
                except WatchError:
                    # Someone else modified the key between WATCH and EXEC.
                    # We continue the loop to check the new version.
                    # In the next iteration, specific check (current_version != expected_version)
                    # will likely raise StateConflictError unless the versions somehow match.
                    continue
