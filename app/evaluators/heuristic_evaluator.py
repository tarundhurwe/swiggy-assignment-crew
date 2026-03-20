from typing import Dict, Any
from app.evaluators.base import BaseEvaluator

LATENCY_THRESHOLD = 1000  # ms


class HeuristicEvaluator(BaseEvaluator):
    def evaluate(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate the conversation for any issues.

        Currently checks the total latency of the conversation and
        returns a warning if it exceeds the threshold.

        Args:
            conversation (Dict[str, Any]): The conversation data

        Returns:
            Dict[str, Any]: A dictionary containing a list of issues
        """
        issues = []

        metadata = conversation.get("metadata", {})
        latency = metadata.get("total_latency_ms", 0)

        if latency > LATENCY_THRESHOLD:
            issues.append(
                {
                    "type": "latency",
                    "severity": "warning",
                    "description": f"Latency {latency}ms exceeds threshold",
                }
            )

        return {"issues": issues}
