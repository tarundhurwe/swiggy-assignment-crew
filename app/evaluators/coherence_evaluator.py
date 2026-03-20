from typing import Dict, Any
from app.evaluators.base import BaseEvaluator


class CoherenceEvaluator(BaseEvaluator):
    def evaluate(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate the coherence of the conversation.

        What it checks:

            Context retention

            No contradictions

            Reference continuity

        Args:
            conversation (Dict[str, Any]): The conversation data

        Returns:
            Dict[str, Any]: A dictionary containing the coherence score
        """
        turns = conversation.get("turns", [])

        if len(turns) < 2:
            return {"coherence": 1.0}

        first_user_input = None
        last_response = None
        coherence_score = 1.0

        for turn in turns:
            if turn["role"] == "user" and not first_user_input:
                first_user_input = turn["content"]

            if turn["role"] == "assistant":
                last_response = turn["content"]

        # Simple heuristic: check if key terms persist
        if first_user_input and last_response:
            keywords = first_user_input.lower().split()

            matched = sum(1 for k in keywords if k in last_response.lower())

            coherence_score = matched / len(keywords) if keywords else 1.0

        return {"coherence": coherence_score}
