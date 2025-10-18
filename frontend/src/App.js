import React, { useState, useRef } from "react";

function App() {
  const [emojis, setEmojis] = useState([]);
  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    setRecording(true);
    audioChunksRef.current = [];
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);
    mediaRecorderRef.current.ondataavailable = (e) => audioChunksRef.current.push(e.data);
    mediaRecorderRef.current.start();
  };

  const stopRecording = () => {
    setRecording(false);
    mediaRecorderRef.current.stop();

    mediaRecorderRef.current.onstop = async () => {
      const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
      const formData = new FormData();
      formData.append("audio_file", audioBlob);

      try {
        const res = await fetch("http://127.0.0.1:8000/api/recordings/", {
          method: "POST",
          body: formData,
        });

        const data = await res.json();
        if (data.emoji && data.audio_file) {
          console.log('Sending the data from UI')
          setEmojis((prev) => [...prev, { emoji: data.emoji, audio_file: data.audio_file }]);
        }
      } catch (err) {
        console.error("Error sending audio:", err);
      }
    };
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Voice to Emoji</h1>
      <button onClick={recording ? stopRecording : startRecording}>
        {recording ? "Stop Recording" : "Start Recording"}
      </button>

      <h3>Recorded Emojis & Audio:</h3>
      {emojis.map((item, i) => (
        <div key={i} style={{ marginTop: "1rem" }}>
          <span style={{ fontSize: "2rem" }}>{item.emoji}</span>
          <audio controls src={`http://127.0.0.1:8000${item.audio_file}`}></audio>
        </div>
      ))}
    </div>
  );
}

export default App;
