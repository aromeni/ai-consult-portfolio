"""Tests for src/rag_engine.py — Phase 6.

All tests use fake numpy arrays and monkeypatching — no model downloads required.
Requires faiss-cpu to be installed — skipped otherwise.
"""

import numpy as np
import pytest

faiss = pytest.importorskip("faiss")

from src.rag_engine import (
    validate_rag_inputs,
    detect_question_intent,
    generate_grounded_answer,
    generate_evidence_summary,
    get_rag_limitations,
    generate_rag_markdown,
    generate_rag_response,
)
from src.vector_store import create_vector_store


# ── Fake helpers ───────────────────────────────────────────────────────────────

def _fake_matrix(n=5, dim=4):
    rng = np.random.default_rng(42)
    m = rng.random((n, dim)).astype(np.float32)
    norms = np.linalg.norm(m, axis=1, keepdims=True)
    return m / norms


def _fake_chunks_raw(n=5):
    return [
        {
            "chunk_id": f"doc-{i % 2}__chunk_{i:03d}",
            "document_name": f"doc-{i % 2}.md",
            "chunk_index": i,
            "text": f"Synthetic policy chunk number {i} for testing purposes only.",
            "word_count": 10,
            "character_count": 55,
            "embedding_index": i,
            "embedding_vector": [0.1, 0.2, 0.3, 0.4],
        }
        for i in range(n)
    ]


def _fake_vector_store(n=5, dim=4):
    matrix = _fake_matrix(n, dim)
    chunks = _fake_chunks_raw(n)
    return create_vector_store(chunks, matrix, metric="cosine")


def _fake_search_results(n=3):
    return [
        {
            "rank": i + 1,
            "score": round(0.9 - i * 0.1, 2),
            "chunk_id": f"doc-0__chunk_{i:03d}",
            "document_name": "doc-0.md",
            "chunk_index": i,
            "text": f"Synthetic policy chunk {i} about safeguarding procedures.",
            "word_count": 10,
            "character_count": 50,
            "embedding_index": i,
            "source_label": f"From doc-0.md · chunk {i}",
            "preview_text": f"Synthetic policy chunk {i} about safeguarding procedures.",
        }
        for i in range(n)
    ]


def _fake_semantic_search_return(results=None):
    r = results if results is not None else _fake_search_results(3)
    return {
        "query": "test question",
        "model_name": "test/model",
        "top_k": 5,
        "results": r,
        "result_count": len(r),
        "query_embedding_dimension": 4,
        "metric": "cosine",
        "limitations": [],
    }


# ── TestValidateRagInputs ─────────────────────────────────────────────────────

class TestValidateRagInputs:

    def test_rejects_empty_question(self):
        vs = _fake_vector_store()
        valid, _ = validate_rag_inputs("", vs)
        assert not valid

    def test_empty_question_message_is_readable(self):
        vs = _fake_vector_store()
        _, msg = validate_rag_inputs("", vs)
        assert "empty" in msg.lower()

    def test_rejects_whitespace_question(self):
        vs = _fake_vector_store()
        valid, _ = validate_rag_inputs("   ", vs)
        assert not valid

    def test_rejects_none_vector_store(self):
        valid, msg = validate_rag_inputs("test question", None)
        assert not valid
        assert "vector store" in msg.lower()

    def test_rejects_empty_dict_vector_store(self):
        valid, _ = validate_rag_inputs("test question", {})
        assert not valid

    def test_rejects_vector_store_with_none_index(self):
        valid, _ = validate_rag_inputs("test question", {"index": None, "embedded_chunks": []})
        assert not valid

    def test_rejects_vector_store_with_no_chunks(self):
        fake_index = faiss.IndexFlatIP(4)
        valid, _ = validate_rag_inputs("test question", {"index": fake_index, "embedded_chunks": []})
        assert not valid

    def test_accepts_valid_question_and_vector_store(self):
        vs = _fake_vector_store()
        valid, msg = validate_rag_inputs("What is the safeguarding policy?", vs)
        assert valid


# ── TestDetectQuestionIntent ──────────────────────────────────────────────────

class TestDetectQuestionIntent:

    def test_returns_dict_with_required_keys(self):
        result = detect_question_intent("test question")
        assert set(result.keys()) == {
            "detected_topics", "question_type", "needs_caution", "caution_reason"
        }

    def test_detected_topics_is_list(self):
        result = detect_question_intent("test")
        assert isinstance(result["detected_topics"], list)

    def test_detects_learner_data_topic(self):
        result = detect_question_intent("Can staff put learner names into ChatGPT?")
        assert "learner data" in result["detected_topics"]

    def test_learner_question_type_is_data_protection(self):
        result = detect_question_intent("Can staff put learner names into ChatGPT?")
        assert result["question_type"] == "data_protection"

    def test_learner_question_needs_caution(self):
        result = detect_question_intent("Can staff use learner data in AI tools?")
        assert result["needs_caution"] is True

    def test_learner_caution_reason_mentions_personal_data(self):
        result = detect_question_intent("Can staff use learner data in AI tools?")
        assert "personal" in result["caution_reason"].lower() or "learner" in result["caution_reason"].lower()

    def test_detects_safeguarding_topic(self):
        result = detect_question_intent("What should staff do with safeguarding information?")
        assert "safeguarding" in result["detected_topics"]

    def test_safeguarding_question_type(self):
        result = detect_question_intent("What should staff do with safeguarding information?")
        assert result["question_type"] == "safeguarding"

    def test_safeguarding_question_needs_caution(self):
        result = detect_question_intent("What should staff do with safeguarding information?")
        assert result["needs_caution"] is True

    def test_detects_human_review_topic(self):
        result = detect_question_intent("How should AI-generated lesson plans be checked?")
        assert "human review" in result["detected_topics"]

    def test_output_quality_question_type(self):
        result = detect_question_intent("How should AI-generated lesson plans be checked?")
        assert result["question_type"] == "output_quality"

    def test_output_quality_no_caution(self):
        result = detect_question_intent("How should AI-generated lesson plans be checked?")
        assert result["needs_caution"] is False

    def test_unknown_question_type_for_unrelated(self):
        result = detect_question_intent("What is the weather like today?")
        assert result["question_type"] == "unknown"

    def test_unrelated_question_no_caution(self):
        result = detect_question_intent("What is the weather like today?")
        assert result["needs_caution"] is False

    def test_detects_approved_tools_topic(self):
        result = detect_question_intent("Which AI tools are staff allowed to use?")
        assert "approved tools" in result["detected_topics"]

    def test_approved_use_question_type(self):
        result = detect_question_intent("Which AI tools are staff allowed to use?")
        assert result["question_type"] == "approved_use"

    def test_detects_accountability_topic(self):
        result = detect_question_intent("Who is responsible for AI-assisted outputs?")
        assert "accountability" in result["detected_topics"]

    def test_accountability_question_type(self):
        result = detect_question_intent("Who is responsible for AI-assisted outputs?")
        assert result["question_type"] == "accountability"


# ── TestGenerateGroundedAnswer ────────────────────────────────────────────────

class TestGenerateGroundedAnswer:

    def test_returns_string(self):
        chunks = _fake_search_results(3)
        assert isinstance(generate_grounded_answer("test", chunks), str)

    def test_returns_no_chunks_message_when_empty(self):
        result = generate_grounded_answer("test question", [])
        assert "no relevant evidence" in result.lower()

    def test_learner_answer_mentions_learner_data(self):
        intent = detect_question_intent("Can staff put learner names into ChatGPT?")
        chunks = _fake_search_results(3)
        answer = generate_grounded_answer(
            "Can staff put learner names into ChatGPT?", chunks, intent=intent
        )
        assert "learner" in answer.lower()

    def test_safeguarding_answer_mentions_safeguarding(self):
        intent = detect_question_intent("What should staff do with safeguarding information?")
        chunks = _fake_search_results(3)
        answer = generate_grounded_answer(
            "What should staff do with safeguarding information?", chunks, intent=intent
        )
        assert "safeguarding" in answer.lower()

    def test_output_quality_answer_mentions_checking(self):
        intent = detect_question_intent("How should AI-generated lesson plans be checked?")
        chunks = _fake_search_results(3)
        answer = generate_grounded_answer(
            "How should AI-generated lesson plans be checked?", chunks, intent=intent
        )
        assert "check" in answer.lower() or "review" in answer.lower()

    def test_answer_starts_with_based_on(self):
        chunks = _fake_search_results(3)
        answer = generate_grounded_answer("test", chunks)
        assert answer.lower().startswith("based on")

    def test_uses_intent_when_provided(self):
        intent = {"question_type": "safeguarding", "detected_topics": ["safeguarding"],
                  "needs_caution": True, "caution_reason": ""}
        chunks = _fake_search_results(3)
        answer = generate_grounded_answer("test", chunks, intent=intent)
        assert "safeguarding" in answer.lower()

    def test_handles_empty_chunks_with_no_retrieved_message(self):
        answer = generate_grounded_answer("any question", [])
        assert "no relevant evidence" in answer.lower() or "broaden" in answer.lower()


# ── TestGenerateEvidenceSummary ───────────────────────────────────────────────

class TestGenerateEvidenceSummary:

    def test_returns_list(self):
        assert isinstance(generate_evidence_summary([]), list)

    def test_empty_input_returns_empty_list(self):
        assert generate_evidence_summary([]) == []

    def test_returns_expected_keys(self):
        results = _fake_search_results(3)
        summary = generate_evidence_summary(results)
        expected = {"rank", "score", "document_name", "chunk_id", "chunk_index",
                    "evidence_text", "source_label"}
        for item in summary:
            assert expected.issubset(item.keys())

    def test_respects_max_items(self):
        results = _fake_search_results(5)
        summary = generate_evidence_summary(results, max_items=2)
        assert len(summary) == 2

    def test_preserves_rank_and_score(self):
        results = _fake_search_results(3)
        summary = generate_evidence_summary(results)
        assert summary[0]["rank"] == 1
        assert summary[0]["score"] == 0.9

    def test_evidence_text_matches_chunk_text(self):
        results = _fake_search_results(3)
        summary = generate_evidence_summary(results)
        assert summary[0]["evidence_text"] == results[0]["text"]

    def test_source_label_contains_document_name(self):
        results = _fake_search_results(3)
        summary = generate_evidence_summary(results)
        assert "doc-0.md" in summary[0]["source_label"]


# ── TestGetRagLimitations ─────────────────────────────────────────────────────

class TestGetRagLimitations:

    def test_returns_list(self):
        assert isinstance(get_rag_limitations(), list)

    def test_returns_non_empty_list(self):
        assert len(get_rag_limitations()) > 0

    def test_includes_synthetic_docs_notice(self):
        limitations = get_rag_limitations()
        assert any("synthetic" in lim.lower() for lim in limitations)

    def test_includes_human_judgement_notice(self):
        limitations = get_rag_limitations()
        assert any("human" in lim.lower() for lim in limitations)

    def test_includes_no_advice_disclaimer(self):
        limitations = get_rag_limitations()
        assert any("advice" in lim.lower() for lim in limitations)


# ── TestGenerateRagMarkdown ───────────────────────────────────────────────────

class TestGenerateRagMarkdown:

    def _sample_response(self):
        return {
            "question": "Can staff use learner data in AI?",
            "answer": "Based on the retrieved synthetic policy evidence, staff should not use learner data.",
            "detected_topics": ["learner data", "approved tools"],
            "question_type": "data_protection",
            "needs_caution": True,
            "caution_reason": "This question involves learner or personal data.",
            "retrieved_chunks": _fake_search_results(2),
            "evidence_summary": generate_evidence_summary(_fake_search_results(2)),
            "top_k": 5,
            "model_name": "test/model",
            "metric": "cosine",
            "limitations": get_rag_limitations(),
        }

    def test_returns_string(self):
        assert isinstance(generate_rag_markdown(self._sample_response()), str)

    def test_contains_question_header(self):
        md = generate_rag_markdown(self._sample_response())
        assert "## Question" in md

    def test_contains_short_answer_header(self):
        md = generate_rag_markdown(self._sample_response())
        assert "## Short Answer" in md

    def test_contains_detected_topics_header(self):
        md = generate_rag_markdown(self._sample_response())
        assert "## Detected Topics" in md

    def test_contains_question_type_header(self):
        md = generate_rag_markdown(self._sample_response())
        assert "## Question Type" in md

    def test_contains_retrieved_evidence_header(self):
        md = generate_rag_markdown(self._sample_response())
        assert "## Retrieved Evidence" in md

    def test_contains_limitations_header(self):
        md = generate_rag_markdown(self._sample_response())
        assert "## Limitations and Responsible Use" in md

    def test_contains_caution_header_when_needed(self):
        md = generate_rag_markdown(self._sample_response())
        assert "## Caution Notes" in md

    def test_no_caution_header_when_not_needed(self):
        response = self._sample_response()
        response["needs_caution"] = False
        md = generate_rag_markdown(response)
        assert "## Caution Notes" not in md

    def test_contains_question_text(self):
        md = generate_rag_markdown(self._sample_response())
        assert "Can staff use learner data in AI?" in md

    def test_contains_answer_text(self):
        md = generate_rag_markdown(self._sample_response())
        assert "synthetic policy evidence" in md


# ── TestGenerateRagResponse ───────────────────────────────────────────────────

class TestGenerateRagResponse:

    def _mock_search(self, monkeypatch, results=None):
        r = results if results is not None else _fake_search_results(3)
        monkeypatch.setattr(
            "src.rag_engine.semantic_search",
            lambda *a, **kw: _fake_semantic_search_return(r),
        )

    def test_returns_dict(self, monkeypatch):
        vs = _fake_vector_store()
        self._mock_search(monkeypatch)
        result = generate_rag_response("What is the safeguarding policy?", vs)
        assert isinstance(result, dict)

    def test_returns_expected_keys(self, monkeypatch):
        vs = _fake_vector_store()
        self._mock_search(monkeypatch)
        result = generate_rag_response("test question about policy", vs)
        expected = {
            "question", "answer", "detected_topics", "question_type",
            "needs_caution", "caution_reason", "retrieved_chunks",
            "evidence_summary", "top_k", "model_name", "metric", "limitations",
        }
        assert expected.issubset(result.keys())

    def test_stores_original_question(self, monkeypatch):
        vs = _fake_vector_store()
        self._mock_search(monkeypatch)
        q = "Can staff use learner data in AI tools?"
        result = generate_rag_response(q, vs)
        assert result["question"] == q

    def test_answer_is_string(self, monkeypatch):
        vs = _fake_vector_store()
        self._mock_search(monkeypatch)
        result = generate_rag_response("test question", vs)
        assert isinstance(result["answer"], str)

    def test_limitations_is_non_empty_list(self, monkeypatch):
        vs = _fake_vector_store()
        self._mock_search(monkeypatch)
        result = generate_rag_response("test question", vs)
        assert isinstance(result["limitations"], list)
        assert len(result["limitations"]) > 0

    def test_raises_on_empty_question(self, monkeypatch):
        vs = _fake_vector_store()
        self._mock_search(monkeypatch)
        with pytest.raises(ValueError):
            generate_rag_response("", vs)

    def test_raises_on_missing_vector_store(self, monkeypatch):
        self._mock_search(monkeypatch)
        with pytest.raises(ValueError):
            generate_rag_response("test question", None)

    def test_evidence_summary_matches_retrieved_chunks_count(self, monkeypatch):
        vs = _fake_vector_store()
        self._mock_search(monkeypatch, results=_fake_search_results(3))
        result = generate_rag_response("test question", vs, top_k=5)
        assert len(result["evidence_summary"]) == len(result["retrieved_chunks"])

    def test_no_chunks_answer_when_empty_results(self, monkeypatch):
        vs = _fake_vector_store()
        self._mock_search(monkeypatch, results=[])
        result = generate_rag_response("obscure question xyz", vs)
        assert "no relevant evidence" in result["answer"].lower() or "broaden" in result["answer"].lower()
