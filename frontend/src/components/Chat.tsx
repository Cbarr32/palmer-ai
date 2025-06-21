'use client';
import { useState, useEffect, useRef } from 'react';
import { Send, Upload, MessageCircle, Bot, CheckCircle, AlertCircle, FileText, Zap } from 'lucide-react';
import { chat, uploadAndChat, health } from '@/services/palmer-api';

interface Message {
  role: 'user' | 'assistant' | 'error' | 'system';
  content: string;
  suggestions?: string[];
  fileInfo?: any;
  timestamp: Date;
  id: string;
}

interface SystemStatus {
  backend: 'connected' | 'disconnected' | 'checking';
  ai: 'active' | 'inactive';
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<SystemStatus>({ backend: 'checking', ai: 'inactive' });
  const [isDragging, setIsDragging] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    checkSystemHealth();
    const interval = setInterval(checkSystemHealth, 30000); // Check every 30s
    return () => clearInterval(interval);
  }, []);

  const checkSystemHealth = async () => {
    try {
      await health();
      setStatus({ backend: 'connected', ai: 'active' });
    } catch (error) {
      setStatus({ backend: 'disconnected', ai: 'inactive' });
    }
  };

  const addMessage = (role: Message['role'], content: string, extra?: Partial<Message>) => {
    const message: Message = {
      role,
      content,
      timestamp: new Date(),
      id: Date.now().toString(),
      ...extra
    };
    setMessages(prev => [...prev, message]);
    return message;
  };

  const sendMessage = async () => {
    if (!input.trim() || loading) return;
    
    const userMessage = input;
    setInput('');
    addMessage('user', userMessage);
    setLoading(true);

    try {
      const response = await chat(userMessage);
      addMessage('assistant', response.palmer_response || 'Response received', {
        suggestions: response.suggestions || response.suggested_actions
      });
      setStatus(prev => ({ ...prev, backend: 'connected', ai: 'active' }));
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || error.message || 'Connection failed';
      addMessage('error', `Connection error: ${errorMsg}`);
      setStatus(prev => ({ ...prev, backend: 'disconnected' }));
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (file: File) => {
    if (!file || loading) return;

    const fileSize = (file.size / 1024).toFixed(1);
    addMessage('user', `📁 Uploaded: ${file.name} (${fileSize}KB)`, {
      fileInfo: { name: file.name, size: fileSize }
    });
    setLoading(true);

    try {
      const response = await uploadAndChat(file, `Please analyze this file: ${file.name}`);
      addMessage('assistant', response.palmer_response || 'File processed successfully', {
        fileInfo: response.file_info
      });
      setStatus(prev => ({ ...prev, backend: 'connected', ai: 'active' }));
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || error.message || 'Upload failed';
      addMessage('error', `Upload failed: ${errorMsg}`);
      setStatus(prev => ({ ...prev, backend: 'disconnected' }));
    } finally {
      setLoading(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const files = Array.from(e.dataTransfer.files);
    const file = files.find(f => f.name.match(/\.(xlsx?|csv)$/i));
    if (file) handleFileUpload(file);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const StatusIndicator = () => (
    <div className="flex items-center gap-2 text-sm">
      {status.backend === 'connected' ? (
        <CheckCircle className="w-4 h-4 text-green-500" />
      ) : status.backend === 'disconnected' ? (
        <AlertCircle className="w-4 h-4 text-red-500" />
      ) : (
        <div className="w-4 h-4 border-2 border-gray-300 border-t-blue-500 rounded-full animate-spin" />
      )}
      <span className="text-white/90">
        {status.backend === 'connected' ? 'AI Ready' : 
         status.backend === 'disconnected' ? 'Offline' : 'Connecting...'}
      </span>
    </div>
  );

  return (
    <div 
      className={`flex flex-col h-screen max-w-6xl mx-auto bg-white shadow-2xl transition-all duration-300 ${
        isDragging ? 'ring-4 ring-blue-400 ring-opacity-50' : ''
      }`}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
    >
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white p-6 shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="relative">
              <MessageCircle className="w-10 h-10" />
              {status.ai === 'active' && (
                <Zap className="w-4 h-4 absolute -top-1 -right-1 text-yellow-300" />
              )}
            </div>
            <div>
              <h1 className="text-2xl font-bold">Palmer AI</h1>
              <p className="text-blue-100">Conversational B2B Intelligence Platform</p>
            </div>
          </div>
          <StatusIndicator />
        </div>
      </header>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 bg-gradient-to-b from-gray-50 to-white">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-20">
            <Bot className="w-20 h-20 mx-auto mb-6 text-gray-300" />
            <h2 className="text-2xl font-bold mb-4 text-gray-700">Welcome to Palmer AI</h2>
            <div className="max-w-2xl mx-auto space-y-3">
              <p className="text-lg">Your AI-powered B2B intelligence assistant</p>
              <div className="grid md:grid-cols-2 gap-4 mt-8">
                <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                  <h3 className="font-semibold text-blue-800 mb-2">💬 Ask Palmer</h3>
                  <p className="text-sm text-blue-700">"I have 500 HVAC products with terrible descriptions"</p>
                </div>
                <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                  <h3 className="font-semibold text-green-800 mb-2">📊 Upload Files</h3>
                  <p className="text-sm text-green-700">Drop Excel/CSV files for AI enhancement</p>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="space-y-6">
          {messages.map((msg) => (
            <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-3xl rounded-2xl px-6 py-4 shadow-sm ${
                msg.role === 'user' 
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white' 
                  : msg.role === 'error'
                  ? 'bg-red-50 text-red-800 border border-red-200'
                  : 'bg-white text-gray-800 border border-gray-200'
              }`}>
                <div className="flex items-start gap-3">
                  {msg.role === 'assistant' && (
                    <Bot className="w-6 h-6 text-blue-600 mt-1 flex-shrink-0" />
                  )}
                  {msg.role === 'user' && msg.fileInfo && (
                    <FileText className="w-6 h-6 text-white/80 mt-1 flex-shrink-0" />
                  )}
                  <div className="flex-1">
                    <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                    
                    {msg.suggestions && msg.suggestions.length > 0 && (
                      <div className="mt-4 pt-3 border-t border-gray-200">
                        <p className="text-xs text-gray-600 mb-2 font-medium">Quick actions:</p>
                        <div className="flex flex-wrap gap-2">
                          {msg.suggestions.map((suggestion, i) => (
                            <button
                              key={i}
                              onClick={() => setInput(suggestion)}
                              className="bg-blue-50 hover:bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm transition-colors border border-blue-200"
                            >
                              {suggestion}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
                <p className="text-xs opacity-60 mt-2 text-right">
                  {msg.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))}
        </div>

        {loading && (
          <div className="flex justify-start mt-6">
            <div className="bg-white rounded-2xl px-6 py-4 shadow-sm border border-gray-200">
              <div className="flex items-center gap-3">
                <Bot className="w-6 h-6 text-blue-600" />
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                </div>
                <span className="text-gray-600">Palmer is analyzing...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <footer className="border-t bg-white p-6">
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
              placeholder="Ask Palmer about your business, products, or upload files..."
              className="w-full border border-gray-300 rounded-xl px-6 py-4 pr-32 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg"
              disabled={loading}
            />
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2 flex gap-2">
              <button
                onClick={() => fileInputRef.current?.click()}
                disabled={loading}
                className="p-2 text-green-600 hover:text-green-700 hover:bg-green-50 rounded-lg transition-colors"
                title="Upload file"
              >
                <Upload className="w-5 h-5" />
              </button>
              <button
                onClick={sendMessage}
                disabled={loading || !input.trim()}
                className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                title="Send message"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
        
        <div className="flex items-center justify-between mt-3 text-sm text-gray-500">
          <div className="flex items-center gap-4">
            <span>Powered by Claude Sonnet 4</span>
            <span>•</span>
            <span>Backend: localhost:8000</span>
          </div>
          <button
            onClick={checkSystemHealth}
            className="text-blue-600 hover:text-blue-800 font-medium"
          >
            Refresh Status
          </button>
        </div>

        <input
          ref={fileInputRef}
          type="file"
          accept=".xlsx,.xls,.csv"
          onChange={(e) => e.target.files?.[0] && handleFileUpload(e.target.files[0])}
          className="hidden"
        />
      </footer>

      {/* Drag and Drop Overlay */}
      {isDragging && (
        <div className="absolute inset-0 bg-blue-500 bg-opacity-20 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-8 shadow-lg text-center">
            <Upload className="w-12 h-12 mx-auto mb-4 text-blue-600" />
            <p className="text-lg font-semibold text-gray-800">Drop your Excel or CSV file here</p>
            <p className="text-gray-600">Palmer AI will analyze it instantly</p>
          </div>
        </div>
      )}
    </div>
  );
}
