import os
import pytest
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8787")
TIMEOUT = 60

@pytest.fixture(scope="module")
def api_url():
    """Fixture to provide the base URL for the API."""
    return BASE_URL


def test_health_check(api_url):
    """Test the health check endpoint."""
    response = requests.get(f"{api_url}/health", timeout=TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "ok"
    assert data.get("service") == "learnpilot-ai"


def test_cors_options(api_url):
    """Test CORS preflight response."""
    response = requests.options(f"{api_url}/ai/chat", timeout=TIMEOUT)
    assert response.status_code == 204
    assert response.headers.get("Access-Control-Allow-Origin") == "*"


def test_not_found(api_url):
    """Test unknown endpoint returns 404."""
    response = requests.get(f"{api_url}/unknown-endpoint", timeout=TIMEOUT)
    assert response.status_code == 404
    data = response.json()
    assert data.get("error") == "Not found"


def test_explain_valid(api_url):
    """Test /ai/explain endpoint with valid data."""
    payload = {
        "concept": "recursion",
        "skill_level": "beginner",
        "learning_style": "visual"
    }
    response = requests.post(f"{api_url}/ai/explain", json=payload, timeout=TIMEOUT)
    assert response.status_code == 200
    # The endpoint returns a raw string response body, not JSON
    assert len(response.text) > 0


def test_explain_missing_concept(api_url):
    """Test /ai/explain missing the concept field."""
    response = requests.post(f"{api_url}/ai/explain", json={"skill_level": "beginner"}, timeout=TIMEOUT)
    assert response.status_code == 400
    assert response.json().get("error") == "concept is required"


def test_chat_valid(api_url):
    """Test /ai/chat endpoint with valid messages."""
    payload = {
        "messages": [{"role": "user", "content": "Hello, AI tutor!"}],
        "max_tokens": 50
    }
    response = requests.post(f"{api_url}/ai/chat", json=payload, timeout=TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0


def test_chat_missing_messages(api_url):
    """Test /ai/chat missing the messages field."""
    response = requests.post(f"{api_url}/ai/chat", json={}, timeout=TIMEOUT)
    assert response.status_code == 400
    assert response.json().get("error") == "messages is required"


def test_practice_valid(api_url):
    """Test /ai/practice endpoint with a valid topic."""
    payload = {
        "topic": "Python loops",
        "difficulty": "beginner",
        "question_type": "open-ended"
    }
    response = requests.post(f"{api_url}/ai/practice", json=payload, timeout=TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert "question" in data
    assert len(data["question"]) > 0


def test_practice_missing_topic(api_url):
    """Test /ai/practice missing the topic field."""
    response = requests.post(f"{api_url}/ai/practice", json={"difficulty": "beginner"}, timeout=TIMEOUT)
    assert response.status_code == 400
    assert response.json().get("error") == "topic is required"


def test_evaluate_valid(api_url):
    """Test /ai/evaluate endpoint with valid question and answer."""
    payload = {
        "question": "What is a variable in programming?",
        "answer": "A variable is like an empty box that can hold a value.",
        "expected_answer": "A named storage location in memory."
    }
    response = requests.post(f"{api_url}/ai/evaluate", json=payload, timeout=TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "feedback" in data
    assert "correct_answer" in data


def test_evaluate_missing_fields(api_url):
    """Test /ai/evaluate missing the question/answer field."""
    payload = {"question": "What is a variable?"}
    response = requests.post(f"{api_url}/ai/evaluate", json=payload, timeout=TIMEOUT)
    assert response.status_code == 400
    assert response.json().get("error") == "question and answer are required"


def test_path_valid(api_url):
    """Test /ai/path endpoint for generating learning path."""
    payload = {
        "topic": "Python Programming",
        "skill_level": "beginner",
        "learning_style": "auditory",
        "available_lessons": [
            {"id": 1, "title": "Variables", "type": "theory", "difficulty": "beginner"},
            {"id": 2, "title": "Loops", "type": "practice", "difficulty": "beginner"}
        ]
    }
    response = requests.post(f"{api_url}/ai/path", json=payload, timeout=TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert "ordered_lesson_ids" in data
    assert isinstance(data["ordered_lesson_ids"], list)


def test_path_missing_topic(api_url):
    """Test /ai/path missing the topic field."""
    payload = {
        "skill_level": "beginner",
        "available_lessons": []
    }
    response = requests.post(f"{api_url}/ai/path", json=payload, timeout=TIMEOUT)
    assert response.status_code == 400
    assert response.json().get("error") == "topic is required"


def test_progress_valid(api_url):
    """Test /ai/progress endpoint for generating progress insights."""
    payload = {
        "learner_name": "Andy",
        "topic": "Python Programming",
        "progress_data": [
            {"lesson": "Variables", "score": 0.9, "completed": True, "attempts": 1}
        ]
    }
    response = requests.post(f"{api_url}/ai/progress", json=payload, timeout=TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert "insights" in data


def test_progress_missing_fields(api_url):
    """Test /ai/progress missing the progress_data field."""
    payload = {
        "learner_name": "Andy",
        "topic": "Python Programming"
    }
    response = requests.post(f"{api_url}/ai/progress", json=payload, timeout=TIMEOUT)
    assert response.status_code == 400
    assert response.json().get("error") == "progress_data is required"


def test_adapt_valid(api_url):
    """Test /ai/adapt endpoint for predicting difficulty."""
    payload = {
        "topic": "Python Programming",
        "current_difficulty": "beginner",
        "recent_scores": [0.9, 0.95, 0.85]
    }
    response = requests.post(f"{api_url}/ai/adapt", json=payload, timeout=TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert "new_difficulty" in data
    assert "action" in data
    assert "reasoning" in data


def test_adapt_missing_topic(api_url):
    """Test /ai/adapt missing the topic field."""
    payload = {
        "current_difficulty": "beginner",
        "recent_scores": [0.9, 0.95]
    }
    response = requests.post(f"{api_url}/ai/adapt", json=payload, timeout=TIMEOUT)
    assert response.status_code == 400
    assert response.json().get("error") == "topic is required"


def test_summary_valid(api_url):
    """Test /ai/summary endpoint for summarizing session."""
    payload = {
        "lesson_title": "Python Basics",
        "conversation": [
            {"role": "user", "content": "What is a variable?"},
            {"role": "assistant", "content": "A variable is an object in memory..."}
        ]
    }
    response = requests.post(f"{api_url}/ai/summary", json=payload, timeout=TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data


def test_summary_missing_conversation(api_url):
    """Test /ai/summary missing the conversation field."""
    payload = {
        "lesson_title": "Python Basics"
    }
    response = requests.post(f"{api_url}/ai/summary", json=payload, timeout=TIMEOUT)
    assert response.status_code == 400
    assert response.json().get("error") == "conversation is required"
