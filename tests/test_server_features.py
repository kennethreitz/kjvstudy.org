"""Tests for framework-level features wired up in server.py.

Covers the Responder 8.x features adopted from the feature tour:
conditional requests (auto ETag), security headers, Prometheus metrics,
aggregated health checks, typed query-parameter validation, branded
404/500 handling, and the orjson JSON backend.
"""


class TestConditionalRequests:
    """auto_etag=True: GET responses carry an ETag and honor If-None-Match."""

    def test_chapter_page_has_etag(self, client):
        response = client.get("/book/Genesis/chapter/1")
        assert response.status_code == 200
        assert response.headers.get("etag")

    def test_matching_if_none_match_returns_304(self, client):
        first = client.get("/book/Genesis/chapter/1")
        etag = first.headers["etag"]

        second = client.get(
            "/book/Genesis/chapter/1", headers={"If-None-Match": etag}
        )
        assert second.status_code == 304
        assert second.content == b""

    def test_api_responses_get_etags_too(self, client):
        response = client.get("/api/verse/John/3/16")
        assert response.status_code == 200
        assert response.headers.get("etag")

    def test_stale_etag_returns_full_response(self, client):
        response = client.get(
            "/book/Genesis/chapter/1", headers={"If-None-Match": '"stale"'}
        )
        assert response.status_code == 200
        assert len(response.content) > 0


class TestSecurityHeaders:
    """security_headers=True adds the standard hardening headers."""

    def test_security_headers_present(self, client):
        response = client.get("/")
        assert response.headers.get("x-content-type-options") == "nosniff"
        assert response.headers.get("x-frame-options") == "DENY"
        assert response.headers.get("referrer-policy") == "strict-origin-when-cross-origin"

    def test_security_headers_on_api_routes(self, client):
        response = client.get("/api/health")
        assert response.headers.get("x-content-type-options") == "nosniff"


class TestMetrics:
    """metrics_route exposes Prometheus text exposition."""

    def test_metrics_endpoint(self, client):
        # Make at least one request first so counters exist.
        client.get("/api/health")
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "responder_requests_total" in response.text

    def test_metrics_not_cached(self, client):
        response = client.get("/metrics")
        assert "no-store" in response.headers.get("cache-control", "")


class TestHealthChecks:
    """Aggregated readiness checks registered via add_health_check."""

    def test_health_aggregates_checks(self, client):
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "ok"
        assert data["checks"]["bible"]["status"] == "ok"
        assert data["checks"]["books"]["status"] == "ok"


class TestQueryValidation:
    """Typed Query() markers return 422 on invalid input instead of 500."""

    def test_search_rejects_non_integer_limit(self, client):
        response = client.get("/api/search?q=love&limit=abc")
        assert response.status_code == 422

    def test_search_accepts_valid_limit(self, client):
        response = client.get("/api/search?q=love&limit=3")
        assert response.status_code == 200
        assert len(response.json()["results"]) <= 3

    def test_universal_search_rejects_out_of_range_limit(self, client):
        response = client.get("/api/universal-search?q=love&limit=0")
        assert response.status_code == 422

    def test_red_letter_rejects_non_integer_offset(self, client):
        response = client.get("/api/red-letter?offset=abc")
        assert response.status_code == 422

    def test_red_letter_rejects_out_of_range_limit(self, client):
        response = client.get("/api/red-letter?limit=1000")
        assert response.status_code == 422

    def test_strongs_index_rejects_invalid_page(self, client):
        response = client.get("/strongs/hebrew?page=abc")
        assert response.status_code == 422


class TestErrorHandlers:
    """Status-code exception handlers: JSON for the API, branded HTML for web."""

    def test_api_404_is_json(self, client):
        response = client.get("/api/this-does-not-exist")
        assert response.status_code == 404
        assert response.json() == {"detail": "Not Found"}
        assert "application/json" in response.headers.get("content-type", "")

    def test_web_404_is_branded_html(self, client):
        response = client.get("/this-page-does-not-exist")
        assert response.status_code == 404
        assert "text/html" in response.headers.get("content-type", "")
        # The branded error page renders the site chrome, not a bare error.
        assert "KJV" in response.text


class TestJSONBackend:
    """The orjson extra is installed and picked up by Responder."""

    def test_orjson_is_active(self):
        from responder import formats

        assert formats._orjson is not None


class TestRateLimiter:
    """The shared limiter exempts local/monitoring traffic; the test client
    (host "testclient") is exempt, so hammering an endpoint never 429s."""

    def test_test_client_is_exempt(self, client):
        for _ in range(30):
            response = client.get("/api/health")
            assert response.status_code == 200

    def test_limiter_blocks_after_budget_exhausted(self):
        """Drive the RateLimiter directly to confirm 429 semantics."""
        import asyncio

        from responder.ext.ratelimit import RateLimiter

        limiter = RateLimiter(requests=2, period=60)

        class FakeReq:
            client = ("203.0.113.9", 1234)
            headers = {}

        class FakeResp:
            def __init__(self):
                self.status_code = None
                self.media = None
                self.headers = {}

        async def run():
            outcomes = []
            for _ in range(3):
                resp = FakeResp()
                outcomes.append(await limiter.acheck(FakeReq(), resp))
                last = resp
            return outcomes, last

        outcomes, last = asyncio.run(run())
        assert outcomes == [True, True, False]
        assert last.status_code == 429
        assert last.headers.get("Retry-After")
