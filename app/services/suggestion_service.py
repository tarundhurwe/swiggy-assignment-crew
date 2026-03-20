from typing import List, Dict, Any
from collections import defaultdict


class SuggestionService:

    def generate_suggestions(
        self, conversations: List[Dict[str, Any]], evaluations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate suggestions based on conversation and evaluation data.

        Suggestions are generated based on tool failures, latency issues, and coherence issues.

        :param conversations: A list of conversation data
        :param evaluations: A list of evaluation data
        :return: A list of suggestion data
        """
        suggestions = []

        tool_failures = self.detect_tool_failures(conversations, evaluations)
        suggestions.extend(tool_failures)

        latency_issues = self.detect_latency_issues(conversations)
        suggestions.extend(latency_issues)

        coherence_issues = self.detect_coherence_issues(evaluations)
        suggestions.extend(coherence_issues)

        return suggestions

    def detect_tool_failures(self, conversations, evaluations):
        """
        Detect tool failures based on conversation and evaluation data.

        Tool failures are detected based on the number of times a tool is called
        and the number of times it fails.

        :param conversations: A list of conversation data
        :param evaluations: A list of evaluation data
        :return: A list of suggestion data

        The suggestions are generated based on the tool failure rate.
        If the failure rate is above 15%, a suggestion is generated to add
        stricter parameter validation to the tool. The confidence of the
        suggestion is based on the failure rate, with a maximum of 1.0.
        """
        tool_error_counts = defaultdict(int)
        tool_total_counts = defaultdict(int)

        for conv, eval_res in zip(conversations, evaluations):
            for turn in conv.get("turns", []):
                tool_calls = turn.get("tool_calls") or []

                for call in tool_calls:
                    tool_name = call.get("tool_name")
                    tool_total_counts[tool_name] += 1

                    if call.get("result", {}).get("status") != "success":
                        tool_error_counts[tool_name] += 1

        suggestions = []

        for tool, total in tool_total_counts.items():
            failures = tool_error_counts.get(tool, 0)

            if total == 0:
                continue

            failure_rate = failures / total

            if failure_rate > 0.0:
                suggestions.append(
                    {
                        "type": "tool",
                        "tool_name": tool,
                        "suggestion": "High failure rate detected. Add stricter parameter validation.",
                        "rationale": f"{failure_rate*100:.1f}% failure rate observed",
                        "confidence": min(1.0, failure_rate + 0.5),
                    }
                )

        return suggestions

    def detect_latency_issues(self, conversations):
        """
        Detect conversations with high latency.

        Suggestions are generated based on the ratio of conversations with high latency to the total number of conversations.

        If the ratio exceeds 0.2, a suggestion is generated with a confidence score equal to the ratio.

        :param conversations: A list of conversation data
        :return: A list of suggestions
        """
        suggestions = []

        high_latency_count = 0
        total = len(conversations)

        for conv in conversations:
            latency = conv.get("metadata", {}).get("total_latency_ms", 0)

            if latency > 1000:
                high_latency_count += 1

        if total > 0:
            ratio = high_latency_count / total

            if ratio > 0.0:
                suggestions.append(
                    {
                        "type": "system",
                        "suggestion": "High latency observed. Optimize tool calls or parallelize execution.",
                        "rationale": f"{ratio*100:.1f}% conversations exceed latency threshold",
                        "confidence": ratio,
                    }
                )

        return suggestions

    def detect_coherence_issues(self, evaluations):
        """
        Detect conversations with low coherence.

        Suggestions are generated based on the ratio of conversations with low coherence to the total number of conversations.

        If the ratio exceeds 0.2, a suggestion is generated with a confidence score equal to the ratio.

        :param evaluations: A list of evaluation data
        :return: A list of suggestions
        """
        low_coherence = 0
        total = len(evaluations)

        for ev in evaluations:
            if ev.get("scores", {}).get("coherence", 1) < 0.7:
                low_coherence += 1

        suggestions = []

        if total > 0:
            ratio = low_coherence / total

            if ratio > 0.0:
                suggestions.append(
                    {
                        "type": "prompt",
                        "suggestion": "Improve prompt to reinforce context retention across turns.",
                        "rationale": f"{ratio*100:.1f}% conversations show low coherence",
                        "confidence": ratio,
                    }
                )

        return suggestions
