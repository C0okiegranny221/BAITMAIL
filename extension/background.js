chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "new_email") {
    console.log("📩 Background received new email:", request.data);

    fetch("http://localhost:5000/new-email", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request.data),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("✅ Python response:", data);
        sendResponse({ status: "ok", data: data });
      })
      .catch((err) => {
        console.error("❌ Error sending to Python:", err);
        sendResponse({ status: "error", error: err.toString() });
      });

    return true; // Keep channel open for async response
  }
});
