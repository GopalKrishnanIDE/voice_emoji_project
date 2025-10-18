import React, { useState, useRef } from 'react';
import axios from 'axios';

function VoiceRecorder() {
  const [recordings, setRecordings] = useState([]);
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    setIsRecording(true);
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);
    audioChunksRef.current = [];

    mediaRecorderRef.current.ondataavailable = e => {
      audioChunksRef.current.push(e.data);
    };

    mediaRecorderRef.current.onstop = async () => {
      const blob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
      const formData = new FormData();
      formData.append('audio_file', blob, 'voice.wav');

      try {
        const res = await axios.post('http://127.0.0.1:8000/api/recordings/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        setRecordings(prev => [res.data, ...prev]);
      } catch (err) {
        console.error(err);
      }
    };

    mediaRecorderRef.current.start();
  };

  const stopRecording = () => {
    setIsRecording(false);
    mediaRecorderRef.current.stop();
  };

  return (
    <div>
      <h2>Voice to Emoji</h2>
      <button onClick={isRecording ? stopRecording : startRecording}>
        {isRecording ? 'Stop Recording' : 'Start Recording'}
      </button>

      <h3>Recorded Emojis:</h3>
      <ul>
        {recordings.map((r, index) => (
          <li key={index}>
            {r.emoji} — {new Date(r.timestamp).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default VoiceRecorder;
