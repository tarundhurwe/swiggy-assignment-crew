from typing import Dict, Any
from app.evaluators.base import BaseEvaluator


class LLMJudgeEvaluator(BaseEvaluator):
    def evaluate(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate the conversation based on the response quality.

        Heuristics are used to determine the quality of the responses:

        - If the response is longer than 50 characters, the score is increased by 0.05.

        The score is capped at 1.0.

        Args:
            conversation (Dict[str, Any]): The conversation data

        Returns:
            Dict[str, Any]: A dictionary containing the response quality score
        """
        turns = conversation.get("turns", [])

        score = 0.8  # base

        # Simple heuristic boost
        for turn in turns:
            if turn["role"] == "assistant":
                if len(turn["content"]) > 50:
                    score += 0.05

        return {"response_quality": min(score, 1.0)}
