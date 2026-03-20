import uuid
from collections import Counter
from typing import Dict, Any


class FeedbackService:

    def process_feedback(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the feedback for a conversation.

        Args:
            conversation (Dict[str, Any]): The conversation data

        Returns:
            Dict[str, Any]: A dictionary containing the processed feedback
        """
        feedback = conversation.get("feedback", {})

        user_rating = feedback.get("user_rating")
        ops_review = feedback.get("ops_review", {})
        annotations = feedback.get("annotations", [])

        annotation_result = self.handle_annotations(annotations)

        weighted_score = self.compute_weighted_score(
            user_rating, ops_review, annotation_result
        )

        routing = self.routing_decision(annotation_result)

        return {
            "feedback_id": str(uuid.uuid4()),
            "user_rating": user_rating,
            "ops_quality": ops_review.get("quality"),
            "annotation_summary": annotation_result,
            "weighted_score": weighted_score,
            "routing": routing,
        }

    # ---------------------------
    # HANDLE ANNOTATOR DISAGREEMENT
    # ---------------------------
    def handle_annotations(self, annotations):
        """
        Handle annotator disagreement.

        If no annotations are provided, return {"agreement_score": None, "final_label": None}.

        If no labels are found in the annotations, return {"agreement_score": None, "final_label": None}.

        Otherwise, count the labels and compute the agreement score as the ratio of the most common label to the total number of labels.

        Returns a dictionary containing the agreement score, final label, and label distribution.
        """
        if not annotations:
            return {"agreement_score": None, "final_label": None}

        labels = [ann["label"] for ann in annotations if "label" in ann]

        if not labels:
            return {"agreement_score": None, "final_label": None}

        counter = Counter(labels)
        majority_label, majority_count = counter.most_common(1)[0]

        agreement_score = majority_count / len(labels)

        return {
            "agreement_score": agreement_score,
            "final_label": majority_label,
            "label_distribution": dict(counter),
        }

    # ---------------------------
    # WEIGHTED SCORE
    # ---------------------------
    def compute_weighted_score(self, user_rating, ops_review, annotation_result):
        """
        Compute the weighted score of the conversation.

        The weighted score is a combination of the user rating, ops review, and
        annotation agreement score. The weights are as follows:

        - User rating: 0.5
        - Ops review: 0.2
        - Annotation agreement: 0.3

        The scores are normalized as follows:

        - User rating: 0–5 → normalize
        - Ops review: bad → 0.2, average → 0.5, good → 0.8

        Returns the weighted score of the conversation, or None if the total weight is 0.
        """
        score = 0
        total_weight = 0

        # User rating (0–5 → normalize)
        if user_rating is not None:
            score += (user_rating / 5) * 0.5
            total_weight += 0.5

        # Ops review
        ops_quality = ops_review.get("quality") if ops_review else None
        if ops_quality:
            ops_map = {"bad": 0.2, "average": 0.5, "good": 0.8}
            score += ops_map.get(ops_quality, 0.5) * 0.2
            total_weight += 0.2

        # Annotation agreement
        if annotation_result.get("agreement_score") is not None:
            score += annotation_result["agreement_score"] * 0.3
            total_weight += 0.3

        return score / total_weight if total_weight > 0 else None

    # ---------------------------
    # ROUTING DECISION
    # ---------------------------
    def routing_decision(self, annotation_result):
        """
        Make a routing decision based on the annotation agreement score.

        If the agreement score is None, return "no_annotations".
        If the agreement score is less than 0.6, return "human_review_required".
        Otherwise, return "auto_approved".
        """
        agreement = annotation_result.get("agreement_score")

        if agreement is None:
            return "no_annotations"

        if agreement < 0.6:
            return "human_review_required"

        return "auto_approved"
