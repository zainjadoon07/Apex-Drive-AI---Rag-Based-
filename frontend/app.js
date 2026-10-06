// app.js - WebSocket Streaming Client with Grounded Citations & Real-Time Metrics

let sessionId = "user_sess_" + Math.random().toString(36).substring(2, 9);
let socket = null;
let currentBotBubble = null;
let currentBotText = "";
let currentCitations = [];
let isStreaming = false;

const messagesContainer = document.getElementById("messages-container");
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const welcomeBox = document.getElementById("welcome-box");
const newChatBtn = document.getElementById("new-chat-btn");
const headerMetrics = document.getElementById("header-metrics");

// Fetch initial health & RAG corpus status
async function loadHealthStatus() {
  try {
    const res = await fetch("/api/health");
    if (res.ok) {
      const data = await res.json();
      const docCountEl = document.getElementById("rag-doc-count");
      const chunkCountEl = document.getElementById("rag-chunk-count");
      if (docCountEl && data.indexed_documents) {
        docCountEl.innerText = `${data.indexed_documents} Verified`;
      }
      if (chunkCountEl && data.indexed_chunks) {
        chunkCountEl.innerText = `${data.indexed_chunks} Chunks`;
      }
    }
  } catch (e) {
    console.warn("Health status check failed:", e);
  }
}

// Connect to WebSocket endpoint
function connectWebSocket() {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${window.location.host}/ws/chat`;

  socket = new WebSocket(wsUrl);

  socket.onopen = () => {
    console.log("WebSocket connected to Apex RAG backend");
    const metricsText = document.getElementById("metrics-text");
    if (metricsText) metricsText.innerText = "Connected (RAG Ready)";
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);

      // 1. Citations packet received (Bonus Feature: Visible Citations)
      if (data.type === "citations") {
        currentCitations = data.citations || [];
        renderCitations(currentBotBubble, currentCitations, data.retrieval_ms, data.is_cached);
      }

      // 2. Token chunk received
      else if (data.type === "token") {
        currentBotText += data.content;
        if (currentBotBubble) {
          const contentEl = currentBotBubble.querySelector(".content");
          if (contentEl) {
            const parsed = window.marked ? marked.parse(currentBotText) : currentBotText;
            contentEl.innerHTML = parsed + '<span class="streaming-cursor"></span>';
          }
        }
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
      }

      // 3. Final completion packet received
      else if (data.type === "end") {
        isStreaming = false;

        if (currentBotBubble) {
          const contentEl = currentBotBubble.querySelector(".content");
          if (contentEl) {
            contentEl.innerHTML = window.marked ? marked.parse(currentBotText) : currentBotText;
          }

          const metricsEl = currentBotBubble.querySelector(".metrics-tag");
          if (metricsEl && data.metrics) {
            const m = data.metrics;
            const cacheBadge = m.is_cached ? '<span class="metric-pill cache-hit">⚡ Cache Hit</span>' : '';
            metricsEl.innerHTML = `
              <span class="rag-latency">⚡ RAG: ${m.retrieval_ms || 0}ms</span>
              <span class="ttft">TTFT: ${m.ttft_ms || 0}ms</span>
              <span>Speed: ${m.tps || 0} tok/s</span>
              <span>Total: ${m.total_time_s || 0}s</span>
              ${cacheBadge}
            `;

            const metricsText = document.getElementById("metrics-text");
            if (metricsText) {
              metricsText.innerText = `RAG ${m.retrieval_ms || 0}ms | ${m.tps || 0} tok/s`;
            }
          }
        }

        currentBotBubble = null;
        currentBotText = "";
        currentCitations = [];
        messageInput.focus();
        if (window.lucide) lucide.createIcons();
      }

      // 4. Error packet
      else if (data.type === "error") {
        console.error("Backend error:", data.message);
        if (currentBotBubble) {
          const contentEl = currentBotBubble.querySelector(".content");
          if (contentEl) {
            contentEl.innerHTML = `<span style="color:#ff6b6b;">⚠️ ${data.message}</span>`;
          }
        }
        isStreaming = false;
      }
    } catch (err) {
      console.error("Error parsing WebSocket packet:", err);
    }
  };

  socket.onclose = () => {
    console.log("WebSocket connection closed. Retrying in 2s...");
    const metricsText = document.getElementById("metrics-text");
    if (metricsText) metricsText.innerText = "Reconnecting...";
    setTimeout(connectWebSocket, 2000);
  };
}

const citationStore = {};
let nextCitationId = 1;

// Render visible citation pills
function renderCitations(bubbleEl, citations, retrievalMs, isCached) {
  if (!bubbleEl || !citations || citations.length === 0) return;

  const bubbleWrap = bubbleEl.querySelector(".bubble-wrap");
  if (!bubbleWrap) return;

  let shelfEl = bubbleWrap.querySelector(".citations-shelf");
  if (!shelfEl) {
    shelfEl = document.createElement("div");
    shelfEl.className = "citations-shelf";
    const bubble = bubbleWrap.querySelector(".bubble");
    bubbleWrap.insertBefore(shelfEl, bubble);
  }

  const cacheNote = isCached ? " (Cached)" : "";
  const headerHTML = `
    <div class="citations-header">
      <span><i data-lucide="book-open" class="icon-xxs"></i> Grounded in ${citations.length} verified documents &middot; <strong>${retrievalMs || 0}ms</strong>${cacheNote}</span>
    </div>
  `;

  let pillsHTML = '<div class="citation-pills-list">';
  citations.forEach((cit) => {
    const citId = "cit_" + (nextCitationId++);
    citationStore[citId] = cit;

    const safeTitle = escapeHTML(cit.title || cit.doc_id || "Document");
    const safeCat = escapeHTML(cit.category || "Policy");
    const safeSec = cit.section ? escapeHTML(cit.section) : "";
    const displayLabel = safeSec && safeSec !== safeTitle ? `${safeTitle} &middot; <em style="opacity:0.8;font-style:normal;">${safeSec}</em>` : safeTitle;

    pillsHTML += `
      <button type="button" class="citation-pill" data-cit-id="${citId}" onclick="openCitationModal('${citId}')" title="Click to view verified excerpt">
        <span class="citation-pill-cat">${safeCat}</span>
        <span class="citation-pill-title">${displayLabel}</span>
        <i data-lucide="chevron-right" class="icon-xxs"></i>
      </button>
    `;
  });
  pillsHTML += '</div>';

  shelfEl.innerHTML = headerHTML + pillsHTML;
  if (window.lucide) lucide.createIcons();
}

// Citation Modal Viewer (Interactive Excerpt Drawer)
window.openCitationModal = function(citId) {
  const cit = citationStore[citId];
  if (!cit) {
    console.warn("No citation data found for ID:", citId);
    return;
  }

  const modal = document.getElementById("citation-modal");
  const titleEl = document.getElementById("modal-doc-title");
  const metaEl = document.getElementById("modal-doc-meta");
  const fileEl = document.getElementById("modal-source-file");
  const excerptEl = document.getElementById("modal-doc-excerpt");

  if (titleEl) titleEl.innerText = cit.title || "Document Excerpt";
  if (metaEl) metaEl.innerText = `${cit.category || 'General'} · Section: ${cit.section || 'General Policy'}`;
  if (fileEl) fileEl.innerText = cit.source_file || "Internal Database";
  if (excerptEl) excerptEl.innerText = cit.excerpt || "No excerpt text available.";

  if (modal) modal.style.display = "flex";
  if (window.lucide) lucide.createIcons();
};

window.closeCitationModal = function(event) {
  if (event && event.target && event.target.id !== "citation-modal" && !event.target.classList.contains("modal-close-btn")) {
    return;
  }
  const modal = document.getElementById("citation-modal");
  if (modal) modal.style.display = "none";
};

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    const modal = document.getElementById("citation-modal");
    if (modal) modal.style.display = "none";
  }
});


// Send user message
function sendMessage(text) {
  const msg = text || messageInput.value.trim();
  if (!msg || isStreaming) return;

  if (welcomeBox && welcomeBox.style.display !== "none") {
    welcomeBox.style.display = "none";
  }

  // 1. Render User Message
  appendMessageDOM("user", "U", escapeHTML(msg));

  // 2. Render Bot Placeholder for streaming
  currentBotBubble = appendMessageDOM("bot", "A", '<span class="streaming-cursor"></span>');
  currentBotText = "";
  currentCitations = [];
  isStreaming = true;

  // 3. Clear Input
  messageInput.value = "";

  // 4. Send via WebSocket
  socket.send(JSON.stringify({
    session_id: sessionId,
    message: msg
  }));

  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function appendMessageDOM(role, avatarText, initialHTML) {
  const row = document.createElement("div");
  row.className = `message-row ${role}`;

  const userIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>`;

  const botIcon = `<svg width="16" height="16" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg"><polygon points="18,3 33,30 3,30" stroke="currentColor" stroke-width="2.2" fill="none" stroke-linejoin="round"/><circle cx="18" cy="18" r="3" fill="currentColor"/></svg>`;

  const avatarHTML = role === "user" ? userIcon : botIcon;

  row.innerHTML = `
    <div class="avatar">${avatarHTML}</div>
    <div class="bubble-wrap">
      <div class="bubble"><div class="content">${initialHTML}</div></div>
      <div class="metrics-tag"></div>
    </div>
  `;
  messagesContainer.appendChild(row);
  return row;
}

function escapeHTML(str) {
  return str.replace(/[&<>'"]/g, 
    tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
  );
}

function sendQuickPrompt(promptText) {
  sendMessage(promptText);
}

// Event Listeners
chatForm.addEventListener("submit", (e) => {
  e.preventDefault();
  sendMessage();
});

messageInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

newChatBtn.addEventListener("click", async () => {
  try {
    await fetch("/api/reset", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId })
    });
  } catch (e) {
    console.warn("Reset failed:", e);
  }

  sessionId = "user_sess_" + Math.random().toString(36).substring(2, 9);
  messagesContainer.innerHTML = "";
  if (welcomeBox) {
    welcomeBox.style.display = "flex";
    messagesContainer.appendChild(welcomeBox);
  }
  const metricsText = document.getElementById("metrics-text");
  if (metricsText) metricsText.innerText = "Ready";
});

// Close modal on Escape
window.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeCitationModal();
});

// Initialize on page load
connectWebSocket();
loadHealthStatus();
