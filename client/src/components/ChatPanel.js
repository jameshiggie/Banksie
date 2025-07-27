import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, Bot, User, Loader } from 'lucide-react';
import './ChatPanel.css';

const ChatPanel = ({ user }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);
  const [streamingMessage, setStreamingMessage] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    fetchChatHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingMessage]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchChatHistory = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/api/chat/history', {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      const formattedMessages = response.data.flatMap(chat => [
        {
          id: `${chat.id}-user`,
          text: chat.message,
          sender: 'user',
          timestamp: chat.created_at
        },
        {
          id: `${chat.id}-ai`,
          text: chat.response,
          sender: 'ai',
          timestamp: chat.created_at
        }
      ]);
      
      setMessages(formattedMessages);
    } catch (error) {
      console.error('Error fetching chat history:', error);
    } finally {
      setIsLoadingHistory(false);
    }
  };

  const startNewChat = () => {
    setMessages([]);
    setStreamingMessage('');
    setInputMessage('');
    setIsLoading(false);
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    const messageText = inputMessage;
    setInputMessage('');
    setIsLoading(true);
    setStreamingMessage('');

    // Set a timeout to prevent infinite loading
    const timeoutId = setTimeout(() => {
      console.log('Request timeout - stopping loading state');
      setIsLoading(false);
      setStreamingMessage('');
      const timeoutMessage = {
        id: Date.now() + 1,
        text: 'Sorry, the request timed out. Please check your connection and try again.',
        sender: 'ai',
        timestamp: new Date().toISOString(),
        isError: true
      };
      setMessages(prev => [...prev, timeoutMessage]);
    }, 30000); // 30 second timeout

    try {
      const token = localStorage.getItem('token');
      
      console.log('Starting streaming request...');
      
      // Use Server-Sent Events for streaming
      const response = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
          'Accept': 'text/event-stream',
        },
        body: JSON.stringify({ message: messageText }),
        // Add timeout to the fetch request
        signal: AbortSignal.timeout(25000) // 25 second fetch timeout
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      console.log('Response received, starting to read stream...');
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulatedResponse = '';
      let buffer = '';
      let hasReceivedData = false;

      try {
        let loopCount = 0;
        const maxLoops = 1000; // Prevent infinite loops
        
        while (true) {
          loopCount++;
          if (loopCount > maxLoops) {
            console.warn('Stream processing exceeded maximum iterations');
            break;
          }

          const { done, value } = await reader.read();
          
          if (done) {
            console.log('Stream completed');
            break;
          }
          
          const chunk = decoder.decode(value, { stream: true });
          buffer += chunk;
          hasReceivedData = true;
          
          // Process complete lines
          const lines = buffer.split('\n');
          buffer = lines.pop() || ''; // Keep incomplete line in buffer
          
          for (const line of lines) {
            if (line.trim() && line.startsWith('data: ')) {
              try {
                const jsonStr = line.slice(6).trim();
                if (jsonStr) {
                  const data = JSON.parse(jsonStr);
                  console.log('Received chunk:', data);
                  
                  if (data.error) {
                    throw new Error('Server error during streaming');
                  }
                  
                  if (data.done) {
                    console.log('Stream finished, final message:', accumulatedResponse);
                    // Clear timeout since we completed successfully
                    clearTimeout(timeoutId);
                    
                    // Streaming complete, add final message
                    const aiMessage = {
                      id: data.message_id || Date.now() + 1,
                      text: accumulatedResponse || 'No response received',
                      sender: 'ai',
                      timestamp: data.created_at || new Date().toISOString()
                    };
                    
                    setMessages(prev => [...prev, aiMessage]);
                    setStreamingMessage('');
                    setIsLoading(false);
                    return; // Exit the function
                  } else if (data.chunk) {
                    // Update streaming message
                    accumulatedResponse += data.chunk;
                    console.log('Updating streaming message:', accumulatedResponse);
                    setStreamingMessage(accumulatedResponse);
                    
                    // Force a small delay to ensure React updates
                    await new Promise(resolve => setTimeout(resolve, 10));
                  }
                }
              } catch (parseError) {
                console.error('Error parsing SSE data:', parseError, 'Line:', line);
              }
            }
          }
        }
        
        // If we exit the loop without getting a done signal, handle it gracefully
        if (hasReceivedData && accumulatedResponse) {
          console.log('Stream ended without done signal, using accumulated response');
          clearTimeout(timeoutId);
          
          const aiMessage = {
            id: Date.now() + 1,
            text: accumulatedResponse,
            sender: 'ai',
            timestamp: new Date().toISOString()
          };
          
          setMessages(prev => [...prev, aiMessage]);
          setStreamingMessage('');
          setIsLoading(false);
        } else {
          // No data received at all
          throw new Error('No response data received from server');
        }
        
      } finally {
        reader.releaseLock();
      }
      
    } catch (error) {
      console.error('Error sending message:', error);
      clearTimeout(timeoutId); // Clear timeout on error
      
      let errorText = 'Sorry, I encountered an error processing your message. Please try again.';
      
      if (error.name === 'AbortError' || error.message.includes('timeout')) {
        errorText = 'Request timed out. Please check your connection and try again.';
      } else if (error.message.includes('Failed to fetch')) {
        errorText = 'Unable to connect to the server. Please check if the backend is running.';
      }
      
      const errorMessage = {
        id: Date.now() + 1,
        text: errorText,
        sender: 'ai',
        timestamp: new Date().toISOString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
      setStreamingMessage('');
      setIsLoading(false);
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (isLoadingHistory) {
    return (
      <div className="chat-panel">
        <div className="chat-header">
          <Bot size={20} />
          <h3>Banksie</h3>
        </div>
        <div className="chat-loading">
          <Loader className="loading-spinner" size={24} />
          <p>Loading chat history...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <Bot size={20} />
        <h3>Banksie</h3>
        <button onClick={startNewChat} className="new-chat-button">
          New Chat
        </button>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && !streamingMessage ? (
          <div className="empty-chat">
            <Bot size={48} className="empty-chat-icon" />
            <p>Start a conversation with Banksie!</p>
            <div className="chat-suggestions">
              <button 
                onClick={() => setInputMessage("Tell me about the data in the table")}
                className="suggestion-button"
              >
                Tell me about the data
              </button>
              <button 
                onClick={() => setInputMessage("What products are most valuable?")}
                className="suggestion-button"
              >
                Analyze products
              </button>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.sender} ${message.isError ? 'error' : ''}`}
              >
                <div className="message-avatar">
                  {message.sender === 'user' ? (
                    <User size={18} />
                  ) : (
                    <Bot size={18} />
                  )}
                </div>
                <div className="message-content">
                  <div className="message-text">{message.text}</div>
                  <div className="message-time">
                    {formatTime(message.timestamp)}
                  </div>
                </div>
              </div>
            ))}
            
            {/* Streaming message */}
            {streamingMessage && (
              <div className="message ai streaming">
                <div className="message-avatar">
                  <Bot size={18} />
                </div>
                <div className="message-content">
                  <div className="message-text">
                    {streamingMessage}
                    <span className="streaming-cursor">|</span>
                  </div>
                </div>
              </div>
            )}
            
            {/* Typing indicator when loading but no streaming content yet */}
            {isLoading && !streamingMessage && (
              <div className="message ai typing">
                <div className="message-avatar">
                  <Bot size={18} />
                </div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={sendMessage} className="chat-input-form">
        <div className="chat-input-container">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Ask me anything about your data..."
            disabled={isLoading}
            className="chat-input"
          />
          <button
            type="submit"
            disabled={!inputMessage.trim() || isLoading}
            className="send-button"
          >
            {isLoading ? <Loader size={20} className="loading-spinner" /> : <Send size={20} />}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatPanel; 