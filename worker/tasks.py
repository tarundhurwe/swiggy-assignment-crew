from worker.celery_app import celery_app
from app.models.database import SessionLocal
from app.models.conversation import Conversation
from app.services.evaluation_service import EvaluationService
from app.services.feedback_service import FeedbackService


@celery_app.task
def process_conversation(conversation_id: str):
    """
    Process a conversation and evaluate its responses.

    The conversation is fetched from the database by its ID.

    If the conversation is not found, an error is returned.

    Otherwise, the responses are evaluated using the EvaluationService.

    The result of the evaluation is returned as a dictionary.

    :param conversation_id: The ID of the conversation to be processed.
    :return: A dictionary containing the evaluation result.
    """
    db = SessionLocal()

    conversation = db.query(Conversation).filter_by(id=conversation_id).first()

    if not conversation:
        return {"error": "Conversation not found"}

    raw_data = conversation.raw_json

    # Evaluation
    eval_service = EvaluationService()
    eval_result = eval_service.run_evaluation(raw_data)

    # Feedback processing
    feedback_service = FeedbackService()
    feedback_result = feedback_service.process_feedback(raw_data)

    print("Evaluation:", eval_result)
    print("Feedback:", feedback_result)

    return {"evaluation": eval_result, "feedback": feedback_result}
