import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './ChatBot.css';
import { FaChevronRight } from "react-icons/fa";

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const inputRef = useRef(null);

    const handleInputChange = (event) => {
        setInputMessage(event.target.value);
    };

    const handleSubmit = async () => {
        if (inputMessage.trim() !== '') {
            const newMessage = { text: inputMessage, sender: 'user' };
            setMessages([...messages, newMessage]);
            setInputMessage('');

            try {
                const response = await axios.post('http://localhost:5000/chatbot', { message: inputMessage });
                const botMessage = { text: response.data.response, sender: 'bot' };
                setMessages([...messages, newMessage, botMessage]);
            } catch (error) {
                console.error('Error al enviar mensaje al chatbot', error);
            }
        }
    };

    return (
<div className="chatbot">
            <h2>Chatbot</h2>
            <div className="chat-container">
                {messages.map((message, index) => (
                    <div 
                        key={index} 
                        className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
                    >
                        {message.text}
                    </div>
                ))}
            </div>
            <div className="input-container">
                <input 
                    type="text" 
                    value={inputMessage} 
                    onChange={handleInputChange} 
                    ref={inputRef}
                    placeholder="Escribe tu mensaje..."
                />
                <button onClick={handleSubmit} className="send-button">
                <FaChevronRight />
                </button>
            </div>
        </div>
    );
};

export default Chatbot;