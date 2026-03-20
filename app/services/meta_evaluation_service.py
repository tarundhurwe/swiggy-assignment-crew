from typing import List, Dict, Any


class MetaEvaluationService:

    def run_meta_evaluation(
        self, evaluations: List[Dict[str, Any]], feedbacks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        calibration = self.calibrate_llm_judge(evaluations, feedbacks)
        accuracy = self.compute_evaluator_accuracy(evaluations, feedbacks)
        blind_spots = self.detect_blind_spots(evaluations, feedbacks)

        return {
            "calibration": calibration,
            "accuracy": accuracy,
            "blind_spots": blind_spots,
        }

    def calibrate_llm_judge(self, evaluations, feedbacks):
        deviations = []

        for eval_res, fb in zip(evaluations, feedbacks):

            llm_score = eval_res.get("scores", {}).get("response_quality")

            user_rating = fb.get("user_rating")
            annotation_label = fb.get("annotation_summary", {}).get("final_label")

            if llm_score is None:
                continue

            # Normalize human signal
            human_score = None

            if user_rating is not None:
                human_score = user_rating / 5
            elif annotation_label:
                human_score = 1.0 if annotation_label == "correct" else 0.0

            if human_score is None:
                continue

            deviation = abs(llm_score - human_score)
            deviations.append(deviation)

        if not deviations:
            return {"status": "insufficient_data"}

        avg_deviation = sum(deviations) / len(deviations)

        return {
            "avg_deviation": avg_deviation,
            "status": "needs_calibration" if avg_deviation > 0.2 else "aligned",
        }

    def compute_evaluator_accuracy(self, evaluations, feedbacks):
        tp = fp = fn = 0

        for eval_res, fb in zip(evaluations, feedbacks):

            predicted_issue = len(eval_res.get("issues_detected", [])) > 0

            human_flag = False
            if fb.get("annotation_summary", {}).get("final_label") == "incorrect":
                human_flag = True

            if predicted_issue and human_flag:
                tp += 1
            elif predicted_issue and not human_flag:
                fp += 1
            elif not predicted_issue and human_flag:
                fn += 1

        precision = tp / (tp + fp) if (tp + fp) else 0
        recall = tp / (tp + fn) if (tp + fn) else 0

        return {"precision": precision, "recall": recall}

    def detect_blind_spots(self, evaluations, feedbacks):
        blind_spots = []

        for idx, (eval_res, fb) in enumerate(zip(evaluations, feedbacks)):

            predicted_issue = len(eval_res.get("issues_detected", [])) > 0
            human_flag = (
                fb.get("annotation_summary", {}).get("final_label") == "incorrect"
            )

            if human_flag and not predicted_issue:
                blind_spots.append(
                    {
                        "conversation_index": idx,
                        "issue": "Evaluator missed a human-flagged issue",
                    }
                )

        return blind_spots
