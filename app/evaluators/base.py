from typing import Dict, Any


class BaseEvaluator:
    def evaluate(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
