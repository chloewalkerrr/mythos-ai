export function validateQuestion(value) {
  const question = value.trim();
  if (!question || !/\p{L}/u.test(question)) return "Enter a question containing words.";
  if (question.length > 2000) return "Keep your question within 2,000 characters.";
  return "";
}

export function fieldLabel(field) {
  if (field.startsWith("power:")) return "Power";
  return field.replaceAll("_", " ").replace(/^./, (letter) => letter.toUpperCase());
}

// Enter asks; Shift+Enter keeps a newline; IME composition is never interrupted.
export function submitsOnEnter(event) {
  return event.key === "Enter" && !event.shiftKey && !event.isComposing;
}

export function groupFacts(facts) {
  const groups = new Map();
  for (const fact of facts) {
    const key = `${fact.entity_type}:${fact.entity_id}`;
    if (!groups.has(key)) groups.set(key, { name: fact.name, facts: [] });
    groups.get(key).facts.push(fact);
  }
  return [...groups.values()];
}

function validSourceUrl(value) {
  if (typeof value !== "string") return false;
  try {
    const url = new URL(value);
    return ["http:", "https:"].includes(url.protocol) && !url.username && !url.password;
  } catch {
    return false;
  }
}

function validAnswer(data) {
  const strings = (item, keys) => item && keys.every((key) => typeof item[key] === "string");
  return strings(data, ["question", "answer"]) && data.answer.trim() &&
    typeof data.insufficient_context === "boolean" &&
    Array.isArray(data.facts) && data.facts.every((fact) =>
      strings(fact, ["entity_type", "name", "field", "value"]) &&
      ["character", "god"].includes(fact.entity_type) && Number.isInteger(fact.entity_id)) &&
    Array.isArray(data.evidence) && data.evidence.every((item) =>
      strings(item, ["source_id", "title", "reference", "text"]) &&
      item.provenance === "attributed_summary" && validSourceUrl(item.source_url) &&
      Array.isArray(item.tags) &&
      item.tags.every((tag) => typeof tag === "string") && Number.isFinite(item.score));
}

export async function requestAnswer(question, fetchImpl = globalThis.fetch) {
  let response;
  try {
    // Let the server own its inference timeout; local generation can take two minutes.
    response = await fetchImpl("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: question.trim() }),
    });
  } catch {
    throw new Error("Couldn’t reach MythosAI. Check that the app is running, then try Ask again.");
  }
  if (!response.ok) {
    const messages = {
      422: "Check your question: use words and no more than 2,000 characters, then try Ask again.",
      502: "The local model couldn’t produce a valid answer. Try Ask again.",
      503: "The local model server is unavailable. Start the LM Studio server, then try Ask again.",
      504: "The local model is taking longer than expected. Try Ask again.",
    };
    throw new Error(messages[response.status] || "MythosAI couldn’t complete the request. Try Ask again.");
  }
  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error("MythosAI returned an unreadable response. Try Ask again.");
  }
  if (!validAnswer(data)) throw new Error("MythosAI returned an incomplete response. Try Ask again.");
  return data;
}

export function initializeAsk(doc = document) {
  const get = (id) => doc.getElementById(id);
  const form = get("ask-form");
  const input = get("question");
  const button = get("ask-button");
  const status = get("status");
  let pending = false;

  // API text is always inserted as text, never interpreted as HTML or Markdown.
  function element(tag, className, text) {
    const node = doc.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function clearValidation() {
    get("form-error").hidden = true;
    input.removeAttribute("aria-invalid");
    input.setAttribute("aria-describedby", "question-help");
  }

  function renderAnswer(data) {
    get("result-question").textContent = data.question;
    get("answer-text").textContent = data.answer;
    get("context-note").hidden = !data.insufficient_context;
    get("context-help").hidden = !data.insufficient_context;
    const facts = get("facts");
    facts.replaceChildren();
    for (const group of groupFacts(data.facts)) {
      const section = element("section", "fact-group");
      section.append(element("h4", "", group.name));
      const list = element("dl");
      for (const fact of group.facts) {
        const row = element("div", "fact-row");
        row.append(element("dt", "", fieldLabel(fact.field)), element("dd", "", fact.value));
        list.append(row);
      }
      section.append(list);
      facts.append(section);
    }
    if (!data.facts.length) facts.append(element("p", "empty-note", "No matching database facts were found."));

    const evidence = get("evidence");
    evidence.replaceChildren();
    data.evidence.forEach((passage, index) => {
      const item = element("li", "evidence-item");
      const title = element("h4", "evidence-title");
      title.append(element("span", "reference-number", `[${String(index + 1).padStart(2, "0")}]`));
      title.append(doc.createTextNode(passage.title));
      const reference = element("p", "source-reference");
      const link = element("a", "", passage.reference);
      link.href = passage.source_url;
      reference.append(link);
      item.append(title, element("p", "evidence-text", passage.text),
        reference,
        element("p", "source-id", `Source: ${passage.source_id}`));
      evidence.append(item);
    });
    get("no-evidence").hidden = data.evidence.length > 0;
    get("result").hidden = false;
  }

  input.addEventListener("input", clearValidation);
  input.addEventListener("keydown", (event) => {
    if (!submitsOnEnter(event)) return;
    event.preventDefault();
    form.requestSubmit();
  });
  get("examples").querySelectorAll("button").forEach((example) => {
    example.addEventListener("click", () => {
      input.value = example.textContent;
      clearValidation();
      input.focus();
    });
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (pending) return;
    const validation = validateQuestion(input.value);
    if (validation) {
      get("form-error").textContent = validation;
      get("form-error").hidden = false;
      input.setAttribute("aria-invalid", "true");
      input.setAttribute("aria-describedby", "question-help form-error");
      input.focus();
      return;
    }
    clearValidation();
    pending = true;
    button.disabled = true;
    input.readOnly = true;
    button.textContent = "Asking…";
    form.setAttribute("aria-busy", "true");
    get("error").hidden = true;
    get("result").hidden = true;
    get("examples").hidden = true;
    status.classList.remove("visually-hidden");
    status.replaceChildren(element("strong", "", "Preparing your answer…"),
      element("p", "", "Local generation may take a minute or two. Your question is being processed."));
    let focusTarget;
    try {
      const data = await requestAnswer(input.value);
      renderAnswer(data);
      get("introduction").classList.add("visually-hidden");
      status.textContent = data.insufficient_context ? "The available context is insufficient." : "Answer ready.";
      focusTarget = get("result-question");
    } catch (error) {
      get("error-detail").textContent = error.message;
      get("error").hidden = false;
      status.textContent = "Request unsuccessful.";
      focusTarget = get("error-title");
    } finally {
      pending = false;
      button.disabled = false;
      input.readOnly = false;
      button.textContent = "Ask";
      form.removeAttribute("aria-busy");
      // Announce completion without leaving a second visible result heading.
      status.classList.add("visually-hidden");
      focusTarget.focus();
    }
  });
}

if (typeof document !== "undefined") initializeAsk();
