"""Generate isolated Xano moderation fixtures; never contact a service.

The emitted functions reuse the production GET/PUT stacks and responses. Only
table names and authenticated actor injection change. The session-version guard
is deliberately omitted: this fixture cannot validate authentication, HTTP
authorization, concurrency, production data, or report creation.

Run each case in a fresh Xano interpreter, never publish this document. The
result checker accepts explicit synthetic results; passing offline tests of the
checker does not mean the Xano functions have executed successfully.
"""
import argparse
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PREFIX = "moderation_fixture_"
TARGET = {"id": 1, "user_id": 2, "body": "Synthetic unchanged target"}
ROWS = (
    ("pending", "post", "spam"),
    ("reviewing", "comment", "harassment"),
    ("resolved", "profile", "inappropriate"),
    ("rejected", "media", "other"),
    ("pending", "message", "spam"),
    ("reviewing", "post", "other"),
    ("resolved", "media", "harassment"),
    ("pending", "comment", "inappropriate"),
)
LIST_FIELDS = {"id", "created_at", "reporter_user_id", "target_type", "target_id",
               "reason", "description", "target_snapshot", "status",
               "reviewer_user_id", "decision", "reviewed_at"}
LIST_REQUIRED_FIELDS = LIST_FIELDS - {"reviewer_user_id", "decision", "reviewed_at"}


def cases():
    """Explicit expected IDs, independent of the production filter expression."""
    rows = [("all", {}, [8, 7, 6, 5, 4, 3, 2, 1]),
            ("pending", {"status": "pending"}, [8, 5, 1]),
            ("reviewing", {"status": "reviewing"}, [6, 2]),
            ("resolved", {"status": "resolved"}, [7, 3]),
            ("rejected", {"status": "rejected"}, [4]),
            ("post", {"target_type": "post"}, [6, 1]),
            ("comment", {"target_type": "comment"}, [8, 2]),
            ("profile", {"target_type": "profile"}, [3]),
            ("media", {"target_type": "media"}, [7, 4]),
            ("message", {"target_type": "message"}, [5]),
            ("spam", {"reason": "spam"}, [5, 1]),
            ("harassment", {"reason": "harassment"}, [7, 2]),
            ("inappropriate", {"reason": "inappropriate"}, [8, 3]),
            ("other", {"reason": "other"}, [6, 4]),
            ("combined", {"status": "pending", "target_type": "post", "reason": "spam"}, [1]),
            ("empty_combined", {"status": "pending", "target_type": "media"}, []),
            ("first_page", {"per_page": 3}, [8, 7, 6]),
            ("second_page", {"per_page": 3, "page": 2}, [5, 4, 3]),
            ("last_page", {"per_page": 3, "page": 3}, [2, 1])]
    result = [dict(name=name, inputs=inputs, ids=ids,
                   total=8 if "page" in name else len(ids)) for name, inputs, ids in rows]
    for status in ("reviewing", "resolved", "rejected"):
        result.append(dict(name="decision_"+status,
                           inputs=dict(action="review", status=status), review=True))
    return result


def _production_function(filename, function_name):
    source = (ROOT/"xano/api/codeboxd"/filename).read_text(encoding="utf-8")
    inputs = re.search(r"  input \{(.*?)\n  \}", source, re.S)
    if not inputs or "  stack {\n" not in source or "\n  }\n\n  response" not in source:
        raise ValueError("Production contract layout changed; review extraction")
    stack = source.split("  stack {\n", 1)[1].rsplit("\n  }\n\n  response", 1)[0]
    guard = r'    function\.run "Security/require_current_session" \{\n.*?\n    \}\n'
    stack, removed = re.subn(guard, "", stack, flags=re.S)
    if removed != 1 or "function.run" in stack:
        raise ValueError("Unexpected function dependency; fixture must remain isolated")
    response = "  response"+source.rsplit("\n  }\n\n  response", 1)[1].split("\n  guid =", 1)[0]
    body = stack+"\n  }\n\n"+response
    body = body.replace("$auth.id", "$input.fixture_actor_id")
    referenced = set(re.findall(r"\bdb\.(?:get|query|add|edit|del)\s+(\w+)", body))
    if not referenced <= {"user", "report", "event_log", "post"} or "$auth" in body:
        raise ValueError("Unexpected production dependency; do not emit unsafe script")
    for table in ("user", "report", "event_log", "post"):
        body = re.sub(r"(\bdb\.(?:get|query|add|edit|del)\s+)"+table+r"\b",
                      lambda match: match[1]+PREFIX+table, body)
        body = re.sub(r"\b"+table+r"\.", PREFIX+table+".", body)
    return ('function "'+function_name+'" {\n  input {'+inputs[1]+
            '\n    int fixture_actor_id?=1\n  }\n  stack {\n'+body+'\n}')


def script():
    definitions = {
        "user": "int id\n text account_status\n text role",
        "post": "int id\n int user_id\n text body",
        "report": "int id\n timestamp created_at?=now\n int reporter_user_id\n text target_type\n text target_id\n text reason\n text description\n json target_snapshot?\n text status\n int reviewer_user_id?\n text decision?\n timestamp reviewed_at?",
        "event_log": "int id\n timestamp created_at?=now\n int user_id\n text action\n json metadata?",
    }
    documents = ['table '+PREFIX+name+' {\n schema {\n '+fields+
                  '\n }\n index = [{type: "primary", field: [{name: "id"}]}]\n}'
                 for name, fields in definitions.items()]
    documents += [_production_function("admin_reports_GET.xs", "moderation_list"),
                  _production_function("admin_reports_id_PUT.xs", "moderation_review")]
    seed = []
    for role, status in (("admin", "active"), ("member", "active"), ("admin", "disabled")):
        seed.append('    db.add '+PREFIX+'user { data = '+json.dumps(dict(role=role, account_status=status))+' }')
    seed.append('    db.add '+PREFIX+'post { data = '+json.dumps({k: v for k, v in TARGET.items() if k != "id"})+' }')
    for index, (status, target, reason) in enumerate(ROWS, 1):
        values = dict(created_at=1000+index, reporter_user_id=2, target_type=target,
                      target_id="1", reason=reason, description="Synthetic report "+str(index),
                      target_snapshot={"body": TARGET["body"]}, status=status)
        seed.append('    db.add '+PREFIX+'report { data = '+json.dumps(values)+' }')
    wrapper = '''function "moderation_fixture" {
  input {
    enum action?="list" { values = ["list", "review"] }
    text status?=""
    text target_type?=""
    text reason?=""
    int page?=1 filters=min:1
    int per_page?=25 filters=min:1|max:100
    int fixture_actor_id?=1
    int id?=1
    text decision?="Synthetic review"
  }
  stack {
SEED
    var $result { value = null }
    conditional {
      if ($input.action == "review") {
        function.run "moderation_review" { input = {id: $input.id, status: $input.status, decision: $input.decision, fixture_actor_id: $input.fixture_actor_id} } as $result
      }
      else {
        function.run "moderation_list" { input = {status: $input.status, target_type: $input.target_type, reason: $input.reason, page: $input.page, per_page: $input.per_page, fixture_actor_id: $input.fixture_actor_id} } as $result
      }
    }
    db.query moderation_fixture_report { sort = {moderation_fixture_report.id: "asc"} return = {type: "list"} } as $reports_after
    db.query moderation_fixture_event_log { return = {type: "list"} } as $audit
    db.query moderation_fixture_post { return = {type: "list"} } as $targets
  }
  response = {result: $result, reports_after: $reports_after, audit: $audit, targets: $targets}
}'''
    documents.append(wrapper.replace("SEED", "\n".join(seed)))
    return "\n---\n".join(documents)+"\n"


def _same(actual, expected):
    """JSON equality without Python's True == 1 coercion."""
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return set(actual) == set(expected) and all(_same(actual[key], value) for key, value in expected.items())
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(_same(a, b) for a, b in zip(actual, expected))
    return actual == expected


def check_result(data, case):
    """Check an interpreter result, never simulate execution of a contract."""
    if not isinstance(data, dict):
        return {"result_object": False}
    result = data.get("result")
    if not isinstance(result, dict):
        return {"result_object": False}
    targets = data.get("targets")
    checks = {"target_unchanged": _same(targets, [TARGET])}
    reports = data.get("reports_after")
    checks["reports_preserved"] = (isinstance(reports, list) and len(reports) == len(ROWS)
                                   and _same([row.get("id") for row in reports if isinstance(row, dict)], list(range(1, 9))))
    checks["report_content_preserved"] = checks["reports_preserved"] and all(
        row.get("created_at") == 1000+index and row.get("reporter_user_id") == 2
        and row.get("target_type") == target and row.get("target_id") == "1"
        and row.get("reason") == reason and row.get("description") == "Synthetic report "+str(index)
        and row.get("target_snapshot") == {"body": TARGET["body"]}
        and row.get("status") == (case["inputs"]["status"] if case.get("review") and index == 1 else status)
        for index, (row, (status, target, reason)) in enumerate(zip(reports, ROWS), 1))
    if case.get("review"):
        desired = case["inputs"]["status"]
        checks["response"] = (result.get("success") is True and _same(result.get("report_id"), 1)
                              and result.get("previous_status") == "pending" and result.get("status") == desired
                              and _same(result.get("reviewer_user_id"), 1) and result.get("decision") == "Synthetic review")
        current = reports[0] if checks["reports_preserved"] else {}
        checks["stored_decision"] = (current.get("status") == desired and _same(current.get("reviewer_user_id"), 1)
                                     and current.get("decision") == "Synthetic review" and bool(current.get("reviewed_at")))
        audit = data.get("audit")
        event = audit[0] if isinstance(audit, list) and len(audit) == 1 and isinstance(audit[0], dict) else {}
        checks["audit"] = (_same(event.get("user_id"), 1) and event.get("action") == "admin_report_status_changed"
                           and bool(event.get("created_at")) and _same(event.get("metadata"), dict(
                               report_id=1, target_type="post", target_id="1", previous_status="pending",
                               new_status=desired, decision="Synthetic review")))
    else:
        inputs, total = case["inputs"], case["total"]
        page, size = inputs.get("page", 1), inputs.get("per_page", 25)
        items = result.get("items")
        checks["page"] = (isinstance(items, list) and all(isinstance(row, dict) for row in items)
                          and _same([row.get("id") for row in items], case["ids"])
                          and _same(result.get("total"), total) and _same(result.get("page"), page)
                          and _same(result.get("per_page"), size)
                          and _same(result.get("next_page"), page+1 if page*size < total else None))
        checks["payload_fields"] = isinstance(items, list) and all(
            isinstance(row, dict) and LIST_REQUIRED_FIELDS <= set(row) <= LIST_FIELDS for row in items)
        checks["read_only_audit"] = data.get("audit") == []
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="New directory for script and cases; no network")
    args = parser.parse_args()
    generated = script()  # Validate dependencies before creating any output.
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output/"fixture.xs").write_text(generated, encoding="utf-8")
    (args.output/"cases.json").write_text(json.dumps(cases(), indent=2)+"\n", encoding="utf-8")
    print(json.dumps(dict(layer="offline_fixture_generation", cases=len(cases()),
                          interpreter_executed=False, published=False)))


if __name__ == "__main__":
    main()
