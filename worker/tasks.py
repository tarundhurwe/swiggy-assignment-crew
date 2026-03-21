import uuid

from worker.celery_app import celery_app
from app.models.database import SessionLocal

from app.models.conversation import Conversation
from app.services.evaluation_service import EvaluationService
from app.services.feedback_service import FeedbackService
from app.services.suggestion_service import SuggestionService
from app.services.meta_evaluation_service import MetaEvaluationService
from app.models.evaluation import Evaluation


def process_conversation(conversation_id: str):
    """
    Process a conversation by evaluating its quality, generating feedback, and generating suggestions.

    :param conversation_id: The ID of the conversation to process
    :return: A dictionary containing the evaluation result, feedback, and suggestions
    """
    try:
        print("triggering celery task")
        db = SessionLocal()

        conversation = db.query(Conversation).filter_by(id=conversation_id).first()

        if not conversation:
            return {"error": "Conversation not found"}

        raw_data = conversation.raw_json

        # Evaluation
        eval_service = EvaluationService()
        eval_result = eval_service.run_evaluation(raw_data)

        # Feedback
        feedback_service = FeedbackService()
        feedback_result = feedback_service.process_feedback(raw_data)

        # Suggestions
        conversations = (
            db.query(Conversation)
            .order_by(Conversation.created_at.desc())
            .limit(10)
            .all()
        )
        evaluations = (
            db.query(Evaluation).order_by(Evaluation.created_at.desc()).limit(10).all()
        )

        # Convert to raw format
        conversation_data = [c.raw_json for c in conversations]
        evaluation_data = [
            {
                "scores": e.scores,
                "tool_evaluation": e.tool_evaluation,
                "issues_detected": e.issues,
            }
            for e in evaluations
        ]
        suggestion_service = SuggestionService()
        suggestions = suggestion_service.generate_suggestions(
            conversation_data, evaluation_data
        )

        # Meta Evaluation
        meta_service = MetaEvaluationService()
        meta_result = meta_service.run_meta_evaluation([eval_result], [feedback_result])

        # SAVE EVERYTHING
        evaluation_entry = Evaluation(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            overall_score=eval_result["scores"]["overall"],
            scores=eval_result["scores"],
            tool_evaluation=eval_result["tool_evaluation"],
            issues=eval_result["issues_detected"],
            suggestions=suggestions,
            meta_evaluation=meta_result,
        )
        print(f"Evaluation entry: {evaluation_entry}")
        db.add(evaluation_entry)
        db.commit()

        return {"status": "stored"}
    except Exception as e:
        print(f"Error: {e}")
        raise e
