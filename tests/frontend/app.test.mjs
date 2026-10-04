import assert from "node:assert/strict";
import test from "node:test";
import {
  fieldLabel, groupFacts, requestAnswer, submitsOnEnter, validateQuestion,
} from "../../frontend/app.js";

const answer = {
  question: "Who is Athena?", answer: "Athena is the goddess of wisdom.",
  insufficient_context: false,
  facts: [{ entity_type: "god", entity_id: 2, name: "Athena", field: "domain", value: "Wisdom" }],
  evidence: [{ source_id: "athena-wisdom", title: "Athena", reference: "Rick Riordan — Athena",
    source_url: "https://rickriordan.com/character/athena-2/",
    text: "Athena is the goddess of wisdom.", tags: ["Athena"], score: 0.6,
    provenance: "attributed_summary" }],
};

test("question validation matches word, whitespace, and length constraints", () => {
  for (const question of ["", " \n ", "?!", "123", "a".repeat(2001)]) {
    assert.ok(validateQuestion(question));
  }
  for (const question of ["Who is Athena?", "  Who is Percy?  ", "Αθηνά", "a".repeat(2000)]) {
    assert.equal(validateQuestion(question), "");
  }
});

test("Enter submits, while Shift+Enter and IME composition do not", () => {
  assert.equal(submitsOnEnter({ key: "Enter", shiftKey: false, isComposing: false }), true);
  assert.equal(submitsOnEnter({ key: "Enter", shiftKey: true, isComposing: false }), false);
  assert.equal(submitsOnEnter({ key: "Enter", shiftKey: false, isComposing: true }), false);
  assert.equal(submitsOnEnter({ key: "a", shiftKey: false, isComposing: false }), false);
});

test("posts only the trimmed question to the same-origin API", async () => {
  const data = await requestAnswer("  Who is Athena?  ", async (url, options) => {
    assert.equal(url, "/ask");
    assert.equal(options.method, "POST");
    assert.equal(options.headers["Content-Type"], "application/json");
    assert.deepEqual(JSON.parse(options.body), { question: "Who is Athena?" });
    return { ok: true, json: async () => answer };
  });
  assert.deepEqual(data, answer);
});

test("insufficient context is a successful result, including empty supporting context", async () => {
  const insufficient = { ...answer, insufficient_context: true, facts: [], evidence: [] };
  assert.deepEqual(await requestAnswer("Unknown subject", async () => ({
    ok: true, json: async () => insufficient,
  })), insufficient);
});

for (const [status, expected] of [
  [422, /Check your question/], [502, /valid answer/], [503, /LM Studio/],
  [504, /longer than expected/], [500, /couldn’t complete/],
]) {
  test(`HTTP ${status} provides a safe, actionable error`, async () => {
    await assert.rejects(requestAnswer("Athena", async () => ({
      ok: false, status, json: async () => ({ detail: "private internals" }),
    })), expected);
  });
}

test("network failure gives recovery guidance", async () => {
  await assert.rejects(requestAnswer("Athena", async () => { throw new Error("private"); }),
    /Check that the app is running/);
});

test("malformed JSON and incomplete contract are rejected", async () => {
  await assert.rejects(requestAnswer("Athena", async () => ({
    ok: true, json: async () => { throw new SyntaxError(); },
  })), /unreadable/);
  for (const data of [null, {}, { ...answer, answer: " " }, { ...answer, facts: null },
    { ...answer, insufficient_context: "false" },
    { ...answer, evidence: [{ ...answer.evidence[0], provenance: "authoritative" }] }]) {
    await assert.rejects(requestAnswer("Athena", async () => ({ ok: true, json: async () => data })),
      /incomplete/);
  }
});

test("facts group by entity identity, preserving supplied facts and their order", () => {
  const facts = [...answer.facts,
    { ...answer.facts[0], field: "symbol", value: "Owl" },
    { ...answer.facts[0], entity_type: "character", name: "Different entity" }];
  const groups = groupFacts(facts);
  assert.equal(groups.length, 2);
  assert.deepEqual(groups[0].facts, facts.slice(0, 2));
  assert.equal(groups[1].name, "Different entity");
  assert.equal(fieldLabel("parent_god"), "Parent god");
  assert.equal(fieldLabel("power:12"), "Power");
});

test("evidence requires an attributed summary and safe source URL", async () => {
  for (const source_url of [undefined, "", "not a URL", "javascript:alert(1)",
    "file:///tmp/source", "ftp://example.com/file", "https://user:pass@example.com/"]) {
    const data = { ...answer, evidence: [{ ...answer.evidence[0], source_url }] };
    await assert.rejects(requestAnswer("Athena", async () => ({ ok: true, json: async () => data })),
      /incomplete/);
  }
  const data = { ...answer, evidence: [{ ...answer.evidence[0], provenance: "development_summary" }] };
  await assert.rejects(requestAnswer("Athena", async () => ({ ok: true, json: async () => data })),
    /incomplete/);
});
