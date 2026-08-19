import pytest

from utils.validator import validate_document_id


class TestValidateDocumentId:
    """
    Regression suite for the document_id path-traversal fix.

    Before this fix, document_id (a raw URL path segment) was used
    directly in `os.path.join(METADATA_PATH, f"{document_id}.json")`
    across services/document_service.py and api/{delete,download,rename,
    documents}.py with no validation at all -- a value like
    "../../../secrets" would escape storage/metadata entirely, enabling
    arbitrary file read (GET /api/documents/{id}, download), delete
    (DELETE /api/documents/{id}), and write (PUT rename) outside the
    intended storage directories, chainable through any reachable .json
    file. Since every real document_id is a uuid4() (see
    services/storage_service.py), validating against the UUID format
    both closes the traversal and rejects garbage IDs early.
    """

    def test_valid_uuid_is_accepted(self):
        valid = "3124856a-9c07-4e47-b6a1-6e79f3b17b26"
        assert validate_document_id(valid) == valid

    def test_valid_uuid_is_normalized(self):
        # UUID() lowercases and reformats -- confirms callers get back a
        # canonical string safe to interpolate into a path.
        mixed_case = "3124856A-9C07-4E47-B6A1-6E79F3B17B26"
        assert validate_document_id(mixed_case) == mixed_case.lower()

    @pytest.mark.parametrize("payload", [
        "../../../etc/passwd",
        "..\\..\\windows\\win.ini",
        "../secrets",
        "..",
        "%2e%2e%2fsecrets",
        "not-a-uuid",
        "",
        "   ",
        "3124856a-9c07-4e47-b6a1-6e79f3b17b26; rm -rf /",
        "/etc/passwd",
    ])
    def test_path_traversal_and_garbage_payloads_are_rejected(self, payload):
        with pytest.raises(ValueError):
            validate_document_id(payload)

    def test_none_is_rejected_not_crashed(self):
        with pytest.raises(ValueError):
            validate_document_id(None)

    def test_non_string_is_rejected_not_crashed(self):
        with pytest.raises(ValueError):
            validate_document_id(12345)

    def test_traversal_payload_cannot_reach_the_filesystem_via_get_document(self):
        """
        End-to-end confirmation at the service layer (not just the
        validator in isolation): services/document_service.get_document()
        must return None for a traversal payload rather than attempting
        to open a path built from it.
        """
        import asyncio
        from services.document_service import get_document

        result = asyncio.run(get_document("../../../etc/passwd"))
        assert result is None

    def test_traversal_payload_cannot_reach_the_filesystem_via_get_uploaded_file(self):
        """
        services/storage_service.get_uploaded_file() is only reachable
        today via orchestration_service.py, after backend/api/analyze.py
        has already validated the same document_id through get_document()
        -- but that's caller discipline, not a property of this function.
        Validating directly inside get_uploaded_file() too means a future
        caller can't reintroduce traversal by skipping that upstream
        check.
        """
        from services.storage_service import get_uploaded_file

        with pytest.raises(ValueError):
            get_uploaded_file("../../../etc/passwd")
