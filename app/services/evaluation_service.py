import uuid
from typing import Dict, Any

from app.evaluators.tool_evaluator import ToolCallEvaluator
from app.evaluators.coherence_evaluator import CoherenceEvaluator
from app.evaluators.heuristic_evaluator import HeuristicEvaluator
from app.evaluators.llm_judge import LLMJudgeEvaluator


class EvaluationService:

    def __init__(self):
        """
        Initialize the EvaluationService.

        This service contains a list of evaluators which are
        responsible for evaluating different aspects of the conversation.
        The evaluators are:

        - ToolCallEvaluator: Evaluates the tool calls in the conversation.
        - CoherenceEvaluator: Evaluates the coherence of the conversation.
        - HeuristicEvaluator: Evaluates the conversation for any issues.
        - LLMJudgeEvaluator: Evaluates the responses based on the LLM model.

        The results of the evaluation are stored in a dictionary and
        can be accessed through the `run_evaluation` method.
        """
        self.evaluators = [
            ToolCallEvaluator(),
            CoherenceEvaluator(),
            HeuristicEvaluator(),
            LLMJudgeEvaluator(),
        ]

    def run_evaluation(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs the evaluation on the given conversation.

        The evaluation is performed by running each of the evaluators
        in the list of evaluators. The results of the evaluation are
        stored in a dictionary and can be accessed through the
        `scores` key in the returned dictionary.

        The dictionary contains the following keys:

        - "evaluation_id": A unique identifier for the evaluation.
        - "scores": A dictionary containing the scores for each of the evaluators.
        - "tool_evaluation": A dictionary containing the scores for the tool evaluation.
        - "issues_detected": A list of issues detected by the evaluators.

        The `scores` dictionary contains the following keys:

        - "overall": The overall score of the conversation.
        - "response_quality": The score for the response quality evaluator.
        - "tool_accuracy": The score for the tool accuracy evaluator.
        - "coherence": The score for the coherence evaluator.

        The `tool_evaluation` dictionary contains the following keys:

        - "selection_accuracy": The score for the tool selection accuracy evaluator.
        - "parameter_accuracy": The score for the tool parameter accuracy evaluator.
        - "execution_success": The score for the tool execution success evaluator.

        The `issues_detected` list contains the issues detected by the evaluators.
        """
        results = {}

        for evaluator in self.evaluators:
            results.update(evaluator.evaluate(conversation))

        overall_score = self.compute_overall(results)

        return {
            "evaluation_id": str(uuid.uuid4()),
            "scores": {
                "overall": overall_score,
                "response_quality": results.get("response_quality", 0),
                "tool_accuracy": results.get("tool_accuracy", 0),
                "coherence": results.get("coherence", 0),
            },
            "tool_evaluation": {
                "selection_accuracy": results.get("selection_accuracy"),
                "parameter_accuracy": results.get("parameter_accuracy"),
                "execution_success": results.get("execution_success"),
            },
            "issues_detected": results.get("issues", []),
        }

    def compute_overall(self, results: Dict[str, Any]) -> float:
        """
        Computes the overall score of the conversation.

        The overall score is a weighted average of the scores of the
        response quality, tool accuracy, and coherence evaluators.

        The weights are as follows:

        - response quality: 0.4
        - tool accuracy: 0.3
        - coherence: 0.3

        Args:
            results (Dict[str, Any]): A dictionary containing the scores of the evaluators.

        Returns:
            float: The overall score of the conversation.
        """
        return (
            0.4 * results.get("response_quality", 0)
            + 0.3 * results.get("tool_accuracy", 0)
            + 0.3 * results.get("coherence", 0)
        )
