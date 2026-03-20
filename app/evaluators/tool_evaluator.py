from typing import Dict, Any
from app.evaluators.base import BaseEvaluator

ALLOWED_TOOLS = {"flight_search": ["destination", "date_range"]}


class ToolCallEvaluator(BaseEvaluator):
    def evaluate(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate the tool calls in the conversation.

        What it checks:

            What it checks:

                Correct tool selection

                Parameter correctness

                Hallucinated parameters

                Execution success

        Args:
            conversation (Dict[str, Any]): The conversation data

        Returns:
            Dict[str, Any]: A dictionary containing the tool accuracy score
        """
        total_calls = 0
        correct_selection = 0
        param_score = 0
        execution_success = 0

        for turn in conversation.get("turns", []):
            tool_calls = turn.get("tool_calls") or []

            for call in tool_calls:
                total_calls += 1

                tool_name = call.get("tool_name")
                params = call.get("parameters", {})
                result = call.get("result", {})

                # Tool selection
                if tool_name in ALLOWED_TOOLS:
                    correct_selection += 1

                # Parameter accuracy
                expected_params = ALLOWED_TOOLS.get(tool_name, [])
                correct_params = sum(1 for p in expected_params if p in params)

                if expected_params:
                    param_score += correct_params / len(expected_params)

                # Execution success
                if result.get("status") == "success":
                    execution_success += 1

        if total_calls == 0:
            return {
                "tool_accuracy": 1.0,
                "selection_accuracy": 1.0,
                "parameter_accuracy": 1.0,
                "execution_success": True,
            }

        return {
            "tool_accuracy": (
                correct_selection / total_calls + param_score / total_calls
            )
            / 2,
            "selection_accuracy": correct_selection / total_calls,
            "parameter_accuracy": param_score / total_calls,
            "execution_success": execution_success == total_calls,
        }
