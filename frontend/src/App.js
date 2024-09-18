import React, { useState } from 'react';

function App() {
  const [message, setMessage] = useState('');
  const [reply, setReply] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://localhost:8000/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ content: message })
    });
    const data = await response.json();
    setReply(data.reply);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>ChatGPT Assistant</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          rows="4"
          cols="50"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message here..."
          required
        />
        <br />
        <button type="submit">Send</button>
      </form>
      {reply && (
        <div style={{ marginTop: '20px' }}>
          <h2>Assistant's Reply:</h2>
          <p>{reply}</p>
        </div>
      )}
    </div>
  );
}

export default App;
