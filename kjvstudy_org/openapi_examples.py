"""OpenAPI examples and operation metadata for the public JSON API."""
from __future__ import annotations

from copy import deepcopy
from typing import Any

from .routes.api import BulkVerseRequest, BulkVerseResponse


JSON = "application/json"


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Merge nested OpenAPI metadata dictionaries without mutating inputs."""
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(merged.get(key), dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def _path_param(name: str, schema_type: str, example: Any, description: str) -> dict:
    return {
        "name": name,
        "in": "path",
        "required": True,
        "description": description,
        "schema": {"type": schema_type},
        "example": example,
    }


def _query_param(
    name: str,
    schema: dict[str, Any],
    example: Any,
    description: str,
    *,
    required: bool = False,
) -> dict:
    return {
        "name": name,
        "in": "query",
        "required": required,
        "description": description,
        "schema": schema,
        "example": example,
    }


def _json_examples(examples: dict[str, dict[str, Any]]) -> dict:
    return {"content": {JSON: {"examples": examples}}}


def _success_examples(examples: dict[str, dict[str, Any]], description: str) -> dict:
    response = {"description": description}
    response.update(_json_examples(examples))
    return {"responses": {"200": response}}


BOOK_PARAM = _path_param(
    "book",
    "string",
    "John",
    "Canonical KJV book name or supported abbreviation, such as John, Gen, or 1 Cor.",
)
CHAPTER_PARAM = _path_param("chapter", "integer", 3, "Chapter number within the book.")
VERSE_PARAM = _path_param("verse", "integer", 16, "Verse number within the chapter.")


OPENAPI_OPERATION_EXAMPLES: dict[str, dict[str, Any]] = {
    "/api/": {
        "tags": ["API"],
        "summary": "API index",
        "description": "Discover documentation links and the main JSON endpoints.",
        **_success_examples(
            {
                "index": {
                    "summary": "Documentation and endpoint index",
                    "value": {
                        "name": "KJV Study API",
                        "version": "1.0.0",
                        "documentation": {
                            "swagger_ui": "/api/docs",
                            "redoc": "/api/redoc",
                            "openapi_json": "/api/openapi.json",
                        },
                        "endpoints": {
                            "verse": "/api/verse/{book}/{chapter}/{verse}",
                            "search": "/api/search?q={query}",
                            "bulk_verses": "/api/verses/bulk",
                        },
                    },
                }
            },
            "API index with documentation and endpoint links.",
        ),
    },
    "/api/health": {
        "tags": ["API"],
        "summary": "API health check",
        "description": "Lightweight JSON health check for API monitors.",
        **_success_examples(
            {
                "healthy": {
                    "summary": "Healthy response",
                    "value": {
                        "status": "healthy",
                        "service": "KJV Study API",
                        "version": "1.0.0",
                    },
                }
            },
            "API health status.",
        ),
    },
    "/api/search": {
        "tags": ["Search"],
        "summary": "Search verses",
        "description": "Search KJV verses by word, phrase, or direct verse reference.",
        "parameters": [
            _query_param(
                "q",
                {"type": "string", "nullable": True},
                "love",
                "Search text or direct verse reference.",
            ),
            _query_param(
                "limit",
                {"type": "integer", "nullable": True},
                5,
                "Optional maximum number of verse results.",
            ),
        ],
        **_success_examples(
            {
                "word_search": {
                    "summary": "Search for a word",
                    "value": {
                        "query": "love",
                        "results": [
                            {
                                "book": "John",
                                "chapter": 3,
                                "verse": 16,
                                "reference": "John 3:16",
                                "text": "For God so loved the world...",
                                "score": 1.0,
                            }
                        ],
                        "total": 1,
                        "is_direct_verse": False,
                    },
                },
                "direct_reference": {
                    "summary": "Direct verse reference",
                    "value": {
                        "query": "John 3:16",
                        "results": [
                            {
                                "book": "John",
                                "chapter": 3,
                                "verse": 16,
                                "reference": "John 3:16",
                                "text": "For God so loved the world...",
                                "score": 100.0,
                            }
                        ],
                        "total": 1,
                        "is_direct_verse": True,
                    },
                },
            },
            "Search results.",
        ),
    },
    "/api/universal-search": {
        "tags": ["Search"],
        "summary": "Search all study content",
        "description": "Search across books, verses, topics, stories, reading plans, and resources.",
        "parameters": [
            _query_param(
                "q",
                {"type": "string", "nullable": True},
                "faith",
                "Search text.",
            ),
            _query_param(
                "limit",
                {"type": "integer", "minimum": 1, "maximum": 100, "default": 5},
                5,
                "Maximum results per content type.",
            ),
        ],
        **_success_examples(
            {
                "faith": {
                    "summary": "Search across content types",
                    "value": {
                        "query": "faith",
                        "results": {
                            "verses": [
                                {
                                    "reference": "Hebrews 11:1",
                                    "text": "Now faith is the substance...",
                                    "url": "/book/Hebrews/chapter/11/verse/1",
                                }
                            ],
                            "topics": [{"name": "Faith", "url": "/topics/faith"}],
                            "resources": [
                                {"name": "Prayer & Faith", "url": "/study-guides/prayer-faith"}
                            ],
                        },
                    },
                }
            },
            "Grouped universal search results.",
        ),
    },
    "/api/verse-of-the-day": {
        "tags": ["Verses"],
        "summary": "Get verse of the day",
        "description": "Return the daily featured KJV verse.",
        **_success_examples(
            {
                "daily_verse": {
                    "summary": "Daily verse",
                    "value": {
                        "book": "John",
                        "chapter": 3,
                        "verse": 16,
                        "reference": "John 3:16",
                        "text": "For God so loved the world...",
                        "url": "/book/John/chapter/3#verse-16",
                        "red_letter": "full",
                    },
                }
            },
            "Daily verse.",
        ),
    },
    "/api/verse/{book}/{chapter}/{verse}": {
        "tags": ["Verses"],
        "summary": "Get a single verse",
        "description": "Return one KJV verse with red-letter metadata. Add `?interlinear=true` to include word-level interlinear data when available.",
        "parameters": [
            BOOK_PARAM,
            CHAPTER_PARAM,
            VERSE_PARAM,
            _query_param(
                "interlinear",
                {"type": "boolean", "nullable": True},
                True,
                "Include interlinear word data when available.",
            ),
        ],
        **_success_examples(
            {
                "john_3_16": {
                    "summary": "John 3:16",
                    "value": {
                        "book": "John",
                        "chapter": 3,
                        "verse": 16,
                        "reference": "John 3:16",
                        "text": "For God so loved the world, that he gave his only begotten Son...",
                        "red_letter": "full",
                    },
                },
                "genesis_1_1": {
                    "summary": "Genesis 1:1 by abbreviation",
                    "value": {
                        "book": "Genesis",
                        "chapter": 1,
                        "verse": 1,
                        "reference": "Genesis 1:1",
                        "text": "In the beginning God created the heaven and the earth.",
                        "red_letter": None,
                    },
                },
            },
            "Verse response.",
        ),
    },
    "/api/verse-range/{book}/{chapter}/{start}/{end}": {
        "tags": ["Verses"],
        "summary": "Get a verse range",
        "description": "Return a contiguous range of verses from one chapter.",
        "parameters": [
            _path_param("book", "string", "Psalms", "Canonical book name or abbreviation."),
            _path_param("chapter", "integer", 23, "Chapter number within the book."),
            _path_param("start", "integer", 1, "First verse in the range."),
            _path_param("end", "integer", 6, "Last verse in the range."),
        ],
        **_success_examples(
            {
                "psalm_23": {
                    "summary": "Psalm 23",
                    "value": {
                        "book": "Psalms",
                        "chapter": 23,
                        "start": 1,
                        "end": 6,
                        "reference": "Psalms 23:1-6",
                        "verses": [
                            {
                                "verse": 1,
                                "text": "The LORD is my shepherd; I shall not want.",
                                "red_letter": None,
                            }
                        ],
                        "text": "The LORD is my shepherd; I shall not want...",
                    },
                }
            },
            "Verse range response.",
        ),
    },
    "/api/interlinear/{book}/{chapter}/{verse}": {
        "tags": ["Verses"],
        "summary": "Get interlinear word data",
        "description": "Return word-by-word interlinear data for a verse when it is available.",
        "parameters": [BOOK_PARAM, CHAPTER_PARAM, VERSE_PARAM],
        **_success_examples(
            {
                "john_3_16": {
                    "summary": "Interlinear lookup",
                    "value": {
                        "book": "John",
                        "chapter": 3,
                        "verse": 16,
                        "reference": "John 3:16",
                        "text": "For God so loved the world...",
                        "interlinear_available": True,
                        "words": [
                            {
                                "word": "loved",
                                "strongs": "G25",
                                "transliteration": "agapao",
                                "definition": "to love",
                            }
                        ],
                    },
                }
            },
            "Interlinear response.",
        ),
    },
    "/api/books": {
        "tags": ["Books"],
        "summary": "List Bible books",
        "description": "Return all 66 KJV books grouped by testament.",
        **_success_examples(
            {
                "books": {
                    "summary": "Book list",
                    "value": {
                        "total_books": 66,
                        "old_testament": [
                            {
                                "name": "Genesis",
                                "chapters": 50,
                                "testament": "Old Testament",
                            }
                        ],
                        "new_testament": [
                            {
                                "name": "Matthew",
                                "chapters": 28,
                                "testament": "New Testament",
                            }
                        ],
                    },
                }
            },
            "Book list.",
        ),
    },
    "/api/books/{book}": {
        "tags": ["Books"],
        "summary": "Get book metadata",
        "description": "Return chapter counts and available introduction metadata for a Bible book.",
        "parameters": [BOOK_PARAM],
        **_success_examples(
            {
                "john": {
                    "summary": "John",
                    "value": {
                        "name": "John",
                        "total_chapters": 21,
                        "chapters": [{"chapter": 1, "verses": 51}],
                        "links": {"pdf": "/api/books/John/pdf"},
                    },
                }
            },
            "Book metadata.",
        ),
    },
    "/api/books/{book}/chapters/{chapter}": {
        "tags": ["Books"],
        "summary": "Get a chapter",
        "description": "Return all verses in one Bible chapter.",
        "parameters": [BOOK_PARAM, CHAPTER_PARAM],
        **_success_examples(
            {
                "john_3": {
                    "summary": "John 3",
                    "value": {
                        "book": "John",
                        "chapter": 3,
                        "total_verses": 36,
                        "verses": [
                            {
                                "verse": 16,
                                "text": "For God so loved the world...",
                            }
                        ],
                        "links": {"pdf": "/api/books/John/chapters/3/pdf"},
                    },
                }
            },
            "Chapter response.",
        ),
    },
    "/api/cross-references/{book}/{chapter}/{verse}": {
        "tags": ["Verses"],
        "summary": "Get cross-references",
        "description": "Return cross-references for a verse when available.",
        "parameters": [BOOK_PARAM, CHAPTER_PARAM, VERSE_PARAM],
        **_success_examples(
            {
                "john_3_16": {
                    "summary": "Cross-references",
                    "value": {
                        "book": "John",
                        "chapter": 3,
                        "verse": 16,
                        "reference": "John 3:16",
                        "cross_references": ["John 3:15", "Romans 5:8"],
                    },
                }
            },
            "Cross-reference response.",
        ),
    },
    "/api/topics": {
        "tags": ["Study Resources"],
        "summary": "List topics",
        "description": "Return the topical index.",
        **_success_examples(
            {
                "topics": {
                    "summary": "Topic list",
                    "value": {
                        "total_topics": 36,
                        "topics": [
                            {
                                "name": "faith",
                                "slug": "faith",
                                "description": "Faith and trust in God",
                                "subtopics": ["saving_faith", "living_by_faith"],
                            }
                        ],
                    },
                }
            },
            "Topic list.",
        ),
    },
    "/api/topics/{topic_name}": {
        "tags": ["Study Resources"],
        "summary": "Get topic details",
        "description": "Return overview and subtopics for one topical study.",
        "parameters": [
            _path_param("topic_name", "string", "faith", "Topic slug.")
        ],
        **_success_examples(
            {
                "faith": {
                    "summary": "Faith topic",
                    "value": {
                        "name": "faith",
                        "description": "Faith and trust in God",
                        "overview": "Faith is central to Scripture...",
                        "subtopics": {},
                    },
                }
            },
            "Topic details.",
        ),
    },
    "/api/reading-plans": {
        "tags": ["Study Resources"],
        "summary": "List reading plans",
        "description": "Return available Bible reading plans.",
        **_success_examples(
            {
                "plans": {
                    "summary": "Reading plans",
                    "value": {
                        "total_plans": 12,
                        "plans": [
                            {
                                "id": "chronological",
                                "name": "Chronological Bible Reading",
                                "description": "Read Scripture in historical order.",
                            }
                        ],
                    },
                }
            },
            "Reading plan list.",
        ),
    },
    "/api/resources": {
        "tags": ["Study Resources"],
        "summary": "List resource categories",
        "description": "Return available biblical and theological resource categories.",
        **_success_examples(
            {
                "categories": {
                    "summary": "Resource categories",
                    "value": {
                        "total_categories": 39,
                        "categories": [
                            {
                                "name": "biblical_locations",
                                "title": "Biblical Locations",
                                "item_count": 15,
                                "url": "/api/resources/biblical_locations",
                                "html_url": "/biblical-locations",
                            }
                        ],
                    },
                }
            },
            "Resource category list.",
        ),
    },
    "/api/resources/{category}": {
        "tags": ["Study Resources"],
        "summary": "List resources in a category",
        "description": "Return all items in one resource category.",
        "parameters": [
            _path_param(
                "category",
                "string",
                "biblical_locations",
                "Resource category key.",
            )
        ],
        **_success_examples(
            {
                "biblical_locations": {
                    "summary": "Biblical locations",
                    "value": {
                        "category": "biblical_locations",
                        "title": "Biblical Locations",
                        "total_items": 15,
                        "items": [
                            {
                                "name": "Garden of Eden",
                                "slug": "garden-of-eden",
                                "description": "The original home of mankind",
                                "verse_count": 2,
                                "url": "/api/resources/biblical_locations/garden-of-eden",
                            }
                        ],
                    },
                }
            },
            "Resource category response.",
        ),
    },
    "/api/resources/{category}/{slug}": {
        "tags": ["Study Resources"],
        "summary": "Get resource details",
        "description": "Return one resource item with its Scripture references.",
        "parameters": [
            _path_param(
                "category",
                "string",
                "biblical_locations",
                "Resource category key.",
            ),
            _path_param("slug", "string", "garden-of-eden", "Resource item slug."),
        ],
        **_success_examples(
            {
                "garden_of_eden": {
                    "summary": "Garden of Eden",
                    "value": {
                        "name": "Garden of Eden",
                        "slug": "garden-of-eden",
                        "category": "biblical_locations",
                        "description": "The original home of mankind",
                        "verses": [
                            {
                                "reference": "Genesis 2:8",
                                "text": "And the LORD God planted a garden eastward in Eden...",
                            }
                        ],
                    },
                }
            },
            "Resource item response.",
        ),
    },
    "/api/red-letter": {
        "tags": ["Verses"],
        "summary": "List red-letter verses",
        "description": "Return verses containing words of Christ, optionally filtered by book.",
        "parameters": [
            _query_param(
                "book",
                {"type": "string", "nullable": True},
                "John",
                "Optional canonical book name or abbreviation.",
            ),
            _query_param(
                "limit",
                {"type": "integer", "minimum": 1, "maximum": 500, "default": 50},
                25,
                "Maximum number of verses to return.",
            ),
            _query_param(
                "offset",
                {"type": "integer", "minimum": 0, "default": 0},
                0,
                "Pagination offset.",
            ),
        ],
        **_success_examples(
            {
                "john": {
                    "summary": "Red-letter verses in John",
                    "value": {
                        "total": 419,
                        "verses": [
                            {
                                "reference": "John 3:16",
                                "book": "John",
                                "chapter": 3,
                                "verse": 16,
                                "text": "For God so loved the world...",
                                "christ_words": "full",
                                "is_full_verse": True,
                            }
                        ],
                        "limit": 25,
                        "offset": 0,
                    },
                }
            },
            "Red-letter verse list.",
        ),
    },
    "/api/verse/random": {
        "tags": ["Verses"],
        "summary": "Get a random verse",
        "description": "Return a random KJV verse, optionally filtered by testament or book.",
        "parameters": [
            _query_param(
                "testament",
                {"type": "string", "nullable": True, "enum": ["ot", "nt"]},
                "nt",
                "Optional testament filter.",
            ),
            _query_param(
                "book",
                {"type": "string", "nullable": True},
                "Romans",
                "Optional book filter.",
            ),
        ],
        **_success_examples(
            {
                "random_nt": {
                    "summary": "Random New Testament verse",
                    "value": {
                        "book": "Romans",
                        "chapter": 8,
                        "verse": 28,
                        "reference": "Romans 8:28",
                        "text": "And we know that all things work together for good...",
                        "red_letter": None,
                    },
                }
            },
            "Random verse response.",
        ),
    },
    "/api/commentary/{book}/{chapter}/{verse}": {
        "tags": ["Commentary"],
        "summary": "Get verse commentary",
        "description": "Return study commentary for a specific verse.",
        "parameters": [BOOK_PARAM, CHAPTER_PARAM, VERSE_PARAM],
        **_success_examples(
            {
                "john_3_16": {
                    "summary": "John 3:16 commentary",
                    "value": {
                        "book": "John",
                        "chapter": 3,
                        "verse": 16,
                        "reference": "John 3:16",
                        "text": "For God so loved the world...",
                        "analysis": "<strong>For God so loved...</strong>",
                        "historical": "Jesus speaks to Nicodemus...",
                        "questions": ["What does this reveal about God's love?"],
                    },
                }
            },
            "Verse commentary response.",
        ),
    },
    "/api/verses/bulk": {
        "tags": ["Verses"],
        "summary": "Look up verses in bulk",
        "description": "Resolve multiple verse references in one request. Invalid references are skipped.",
        "requestBody": {
            "required": True,
            "content": {
                JSON: {
                    "schema": {"$ref": "#/components/schemas/BulkVerseRequest"},
                    "examples": {
                        "common_verses": {
                            "summary": "Three common verses",
                            "value": {
                                "references": [
                                    "John 3:16",
                                    "Romans 8:28",
                                    "Psalm 23:1",
                                ]
                            },
                        }
                    },
                }
            },
        },
        "responses": {
            "200": {
                "description": "Bulk verse response.",
                "content": {
                    JSON: {
                        "schema": {"$ref": "#/components/schemas/BulkVerseResponse"},
                        "examples": {
                            "common_verses": {
                                "summary": "Bulk lookup response",
                                "value": {
                                    "total": 3,
                                    "verses": [
                                        {
                                            "book": "John",
                                            "chapter": 3,
                                            "verse": 16,
                                            "reference": "John 3:16",
                                            "text": "For God so loved the world...",
                                            "red_letter": "full",
                                        }
                                    ],
                                },
                            }
                        },
                    }
                },
            }
        },
    },
    "/api/family-tree/{name}": {
        "tags": ["Family Tree"],
        "summary": "Get biblical biography",
        "description": "Return a short biography and key events for a biblical figure.",
        "parameters": [
            _path_param("name", "string", "Abraham", "Biblical figure name or alias.")
        ],
        **_success_examples(
            {
                "abraham": {
                    "summary": "Abraham",
                    "value": {
                        "name": "Abraham",
                        "summary": "Originally named Abram...",
                        "significance": "Abraham is the father of the Hebrew nation...",
                        "key_events": [
                            {
                                "age": 100,
                                "event": "Birth of Isaac",
                                "verse": "Genesis 21:5",
                            }
                        ],
                    },
                }
            },
            "Biography response.",
        ),
    },
    "/api/strongs": {
        "tags": ["Strong's"],
        "summary": "Search Strong's concordance",
        "description": "Search Strong's entries by definition or KJV usage.",
        "parameters": [
            _query_param("q", {"type": "string", "nullable": True}, "love", "Search text."),
            _query_param(
                "language",
                {"type": "string", "default": "both", "enum": ["both", "hebrew", "greek"]},
                "greek",
                "Language filter.",
            ),
            _query_param(
                "limit",
                {"type": "integer", "default": 50},
                10,
                "Maximum number of results.",
            ),
        ],
        **_success_examples(
            {
                "love": {
                    "summary": "Search for love",
                    "value": {
                        "query": "love",
                        "language": "greek",
                        "total": 1,
                        "results": [
                            {
                                "strongs": "G25",
                                "word": "agapao",
                                "definition": "to love",
                            }
                        ],
                    },
                }
            },
            "Strong's search results.",
        ),
    },
    "/api/strongs/{strongs_number}": {
        "tags": ["Strong's"],
        "summary": "Get Strong's entry",
        "description": "Return a Hebrew or Greek Strong's concordance entry.",
        "parameters": [
            _path_param(
                "strongs_number",
                "string",
                "G25",
                "Strong's number, such as H7225 or G25.",
            )
        ],
        **_success_examples(
            {
                "g25": {
                    "summary": "G25",
                    "value": {
                        "strongs": "G25",
                        "word": "agapao",
                        "language": "greek",
                        "definition": "to love",
                    },
                }
            },
            "Strong's entry.",
        ),
    },
}


def install_openapi_examples(api) -> None:
    """Attach hand-curated examples to generated OpenAPI operations."""
    if not hasattr(api, "openapi"):
        return

    api.openapi.add_schema("BulkVerseRequest", BulkVerseRequest, check_existing=False)
    api.openapi.add_schema("BulkVerseResponse", BulkVerseResponse, check_existing=False)

    for route in api.router.routes:
        path = str(getattr(route, "path_template", getattr(route, "route", "")) or "")
        meta = OPENAPI_OPERATION_EXAMPLES.get(path)
        if not meta:
            continue
        endpoint = getattr(route, "endpoint", None)
        if endpoint is None:
            continue
        existing = getattr(endpoint, "_openapi_meta", {})
        endpoint._openapi_meta = _deep_merge(existing, meta)

    _install_parameter_example_hook(api)
    api.openapi._spec_cache = None


def _install_parameter_example_hook(api) -> None:
    """Merge parameter examples after Responder generates operation params."""
    if getattr(api.openapi, "_kjvstudy_examples_hooked", False):
        return

    original_build = api.openapi._build_apispec

    def build_with_parameter_examples():
        spec = original_build()
        _apply_parameter_examples(spec._paths)
        return spec

    api.openapi._build_apispec = build_with_parameter_examples
    api.openapi._kjvstudy_examples_hooked = True


def _apply_parameter_examples(paths: dict[str, Any]) -> None:
    """Apply documented parameter descriptions/examples to generated paths."""
    for path, meta in OPENAPI_OPERATION_EXAMPLES.items():
        documented_params = meta.get("parameters")
        if not documented_params or path not in paths:
            continue

        for operation in paths[path].values():
            if not isinstance(operation, dict):
                continue

            existing_params = list(operation.get("parameters", []))
            merged_params: list[dict[str, Any]] = []
            seen = set()

            for parameter in existing_params:
                key = (parameter.get("in"), parameter.get("name"))
                documented = _find_parameter(documented_params, *key)
                if documented:
                    parameter = _deep_merge(parameter, documented)
                merged_params.append(parameter)
                seen.add(key)

            for parameter in documented_params:
                key = (parameter.get("in"), parameter.get("name"))
                if key not in seen:
                    merged_params.append(deepcopy(parameter))

            operation["parameters"] = merged_params


def _find_parameter(
    parameters: list[dict[str, Any]],
    location: str | None,
    name: str | None,
) -> dict[str, Any] | None:
    for parameter in parameters:
        if parameter.get("in") == location and parameter.get("name") == name:
            return parameter
    return None
