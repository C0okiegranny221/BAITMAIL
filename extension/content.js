function handleNewEmail(node) {
    if (!node) {
      console.error("Invalid node provided to handleNewEmail.");
      return;
    }
  
    try {
      // Notify the backend server that a new email has been sent
      fetch("http://127.0.0.1:5000/email-sent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: "email_sent" }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`Server responded with status ${response.status}`);
          }
          console.log("Successfully notified the backend server.");
        })
        .catch((error) => {
          console.error("Error notifying the backend server:", error);
        });
    } catch (error) {
      console.error("Error in handleNewEmail:", error);
    }
  }