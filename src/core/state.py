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
        """Simplistic optimistic locking commit."""
        with self.redis.pipeline() as pipe:
            pipe.watch(self.state_key)
            
            # Check version
            current_data = pipe.get(self.state_key)
            current_version = GlobalState.model_validate_json(current_data).version if current_data else 0

            if current_version != expected_version:
                raise StateConflictError(f"Version mismatch: {current_version} != {expected_version}")

            # Update and Execute
            new_state.version = current_version + 1
            pipe.multi()
            pipe.set(self.state_key, new_state.model_dump_json())
            pipe.execute()
