import logging
import json
from ..models import Task, TaskStatus
from ..core.state import StateManager, StateConflictError

class Judge:
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager

    def review_task(self, task: Task, result_artifact: str) -> str:
        """
        Validates task results based on confidence scores.
        
        Args:
            task: The task being reviewed.
            result_artifact: JSON string containing the result details.
            
        Returns:
            A string signal: 'finalized', 'rejected', 'hitl', or 'retry_needed'.
        """
        try:
            result_data = json.loads(result_artifact)
            confidence_score = result_data.get('confidence_score', 0.0)
        except json.JSONDecodeError:
            logging.error(f"Invalid result artifact for task {task.id}")
            confidence_score = 0.0

        try:
            # We fetch the current state to have a base for modification/version checking
            current_state = self.state_manager.get_state()
            current_version = current_state.version

            if confidence_score > 0.9:
                # In a real scenario, we might update campaign goals or active agents here 
                # based on task completion. For now, we commit the state to simulate finalization.
                task.status = TaskStatus.COMPLETED
                
                # NOTE: In a robust system, we would incorporate task changes into the GlobalState 
                # object effectively. Here we just commit the state to prove the flow.
                self.state_manager.commit_state(current_state, current_version)
                logging.info(f"Task {task.id} finalized with score {confidence_score}")
                return 'finalized'

            elif confidence_score < 0.7:
                task.status = TaskStatus.REJECTED
                logging.warning(f"Task {task.id} rejected with low score {confidence_score}")
                return 'rejected'

            else:
                task.status = TaskStatus.HITL_REVIEW
                logging.info(f"Task {task.id} flagged for HITL review with score {confidence_score}")
                return 'hitl'

        except StateConflictError:
            logging.warning(f"State conflict during review of task {task.id}. Retry needed.")
            return 'retry_needed'
