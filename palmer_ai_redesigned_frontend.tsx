import React, { useState, useEffect, useRef } from 'react';
import { 
  Send, Upload, Users, BarChart3, Settings, Zap, 
  FileText, MessageCircle, Sparkles, ChevronRight,
  Clock, CheckCircle, ArrowRight, Plus, Share2,
  Lightbulb, TrendingUp, Search, Filter
} from 'lucide-react';

// Sophisticated Palmer Dark Theme System (Jobs-inspired)
const theme = {
  colors: {
    // Base surfaces (following Linear's approach)
    base: '#0a0a0a',
    surface: '#121212', 
    elevated: '#1a1a1a',
    border: '#2a2a2a',
    
    // Text hierarchy (87% / 60% / 38% opacity on white)
    textPrimary: '#ffffff',
    textSecondary: 'rgba(255, 255, 255, 0.87)',
    textMuted: 'rgba(255, 255, 255, 0.60)',
    textDisabled: 'rgba(255, 255, 255, 0.38)',
    
    // Palmer brand colors
    primary: '#10B981', // Emerald - for CTAs and success
    secondary: '#6366F1', // Indigo - for accents
    accent: '#F59E0B', // Amber - for highlights
    
    // Semantic colors
    success: '#22C55E',
    warning: '#F59E0B',
    error: '#EF4444',
    info: '#3B82F6'
  }
};

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  type?: 'insight' | 'template' | 'collaboration';
  confidence?: number;
}

interface WorkflowTemplate {
  id: string;
  title: string;
  description: string;
  industry: string;
  estimatedTime: string;
  icon: React.ReactNode;
}

export default function PalmerAIRedesigned() {
  const [currentView, setCurrentView] = useState<'welcome' | 'chat' | 'insights' | 'team'>('welcome');
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Industry-specific templates (Jobs' approach: smart defaults)
  const templates: WorkflowTemplate[] = [
    {
      id: 'hvac-analysis',
      title: 'HVAC Catalog Analysis',
      description: 'Optimize heating and cooling product descriptions for contractors',
      industry: 'HVAC',
      estimatedTime: '3 min',
      icon: <Zap className="w-5 h-5" />
    },
    {
      id: 'plumbing-competitive',
      title: 'Plumbing Competitive Intel',
      description: 'Compare your products against manufacturer catalogs',
      industry: 'Plumbing',
      estimatedTime: '5 min',
      icon: <TrendingUp className="w-5 h-5" />
    },
    {
      id: 'industrial-inventory',
      title: 'Industrial Inventory Insights',
      description: 'Identify top-selling products and market opportunities',
      industry: 'Industrial',
      estimatedTime: '4 min',
      icon: <BarChart3 className="w-5 h-5" />
    }
  ];

  const quickActions = [
    "Upload my product catalog",
    "Compare pricing with competitors", 
    "Generate contractor-friendly descriptions",
    "Find product substitutions",
    "Analyze sales patterns"
  ];

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim()) return;
    
    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsProcessing(true);

    // Simulate AI processing (replace with actual API call)
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: "I'll help you with that! Based on your request, I can analyze your catalog and provide insights tailored for your distributor business. Would you like to upload a file or shall I guide you through specific product intelligence workflows?",
        role: 'assistant',
        timestamp: new Date(),
        confidence: 0.94,
        type: 'insight'
      };
      setMessages(prev => [...prev, aiResponse]);
      setIsProcessing(false);
    }, 1500);
  };

  const handleTemplateSelect = (templateId: string) => {
    setSelectedTemplate(templateId);
    setCurrentView('chat');
    
    const template = templates.find(t => t.id === templateId);
    if (template) {
      setMessages([{
        id: '1',
        content: `I've prepared the ${template.title} workflow for you. This typically takes about ${template.estimatedTime} and will help you ${template.description.toLowerCase()}. Ready to start?`,
        role: 'assistant',
        timestamp: new Date(),
        type: 'template'
      }]);
    }
  };

  // Progressive Disclosure: Welcome Screen (Primary Layer)
  if (currentView === 'welcome') {
    return (
      <div className="min-h-screen" style={{ backgroundColor: theme.colors.base, color: theme.colors.textPrimary }}>
        {/* Navigation */}
        <nav className="border-b" style={{ backgroundColor: theme.colors.surface, borderColor: theme.colors.border }}>
          <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="relative">
                <Sparkles className="w-8 h-8" style={{ color: theme.colors.primary }} />
                <div className="absolute -top-1 -right-1 w-3 h-3 rounded-full animate-pulse" style={{ backgroundColor: theme.colors.accent }}></div>
              </div>
              <div>
                <h1 className="text-xl font-bold">Palmer AI</h1>
                <p className="text-xs" style={{ color: theme.colors.textMuted }}>Product Intelligence Platform</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <button className="p-2 rounded-lg hover:opacity-80 transition-opacity" style={{ backgroundColor: theme.colors.elevated }}>
                <Users className="w-5 h-5" />
              </button>
              <button className="p-2 rounded-lg hover:opacity-80 transition-opacity" style={{ backgroundColor: theme.colors.elevated }}>
                <Settings className="w-5 h-5" />
              </button>
            </div>
          </div>
        </nav>

        <div className="max-w-6xl mx-auto px-6 py-12">
          {/* Hero Section - Jobs' approach: Clarity of purpose */}
          <div className="text-center mb-16">
            <h1 className="text-5xl font-bold mb-6 leading-tight">
              Transform product descriptions into
              <span className="block bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                contractor gold
              </span>
            </h1>
            <p className="text-xl mb-8 max-w-3xl mx-auto leading-relaxed" style={{ color: theme.colors.textMuted }}>
              AI-powered product intelligence for HVAC, plumbing, and industrial distributors. 
              Turn boring catalogs into compelling sales tools in minutes, not hours.
            </p>
            
            <div className="flex items-center justify-center gap-4">
              <button 
                onClick={() => setCurrentView('chat')}
                className="px-8 py-4 rounded-xl font-semibold text-lg transition-all transform hover:scale-105 flex items-center gap-2"
                style={{ backgroundColor: theme.colors.primary, color: theme.colors.base }}
              >
                <MessageCircle className="w-5 h-5" />
                Start Conversation
              </button>
              <button className="px-8 py-4 rounded-xl font-semibold text-lg border-2 transition-all hover:opacity-80 flex items-center gap-2" 
                style={{ borderColor: theme.colors.border, color: theme.colors.textSecondary }}>
                <Upload className="w-5 h-5" />
                Upload Catalog
              </button>
            </div>
          </div>

          {/* Industry Templates - Progressive Disclosure Layer 1 */}
          <div className="mb-16">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold mb-4">Industry-Specific Workflows</h2>
              <p style={{ color: theme.colors.textMuted }}>Pre-built templates designed for your industry</p>
            </div>
            
            <div className="grid md:grid-cols-3 gap-6">
              {templates.map((template) => (
                <button
                  key={template.id}
                  onClick={() => handleTemplateSelect(template.id)}
                  className="p-6 rounded-2xl border text-left transition-all hover:scale-105 group"
                  style={{ backgroundColor: theme.colors.surface, borderColor: theme.colors.border }}
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-2 rounded-lg" style={{ backgroundColor: theme.colors.elevated, color: theme.colors.primary }}>
                      {template.icon}
                    </div>
                    <span className="text-xs px-2 py-1 rounded-full" style={{ backgroundColor: theme.colors.accent, color: theme.colors.base }}>
                      {template.estimatedTime}
                    </span>
                  </div>
                  <h3 className="font-semibold mb-2">{template.title}</h3>
                  <p className="text-sm mb-4" style={{ color: theme.colors.textMuted }}>{template.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs" style={{ color: theme.colors.textMuted }}>{template.industry}</span>
                    <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" style={{ color: theme.colors.primary }} />
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Social Proof - Following Jobs' approach */}
          <div className="text-center">
            <div className="grid md:grid-cols-3 gap-8 mb-8">
              <div className="p-6 rounded-2xl" style={{ backgroundColor: theme.colors.surface }}>
                <div className="text-3xl font-bold mb-2" style={{ color: theme.colors.primary }}>2.3M+</div>
                <p style={{ color: theme.colors.textMuted }}>Products Enhanced</p>
              </div>
              <div className="p-6 rounded-2xl" style={{ backgroundColor: theme.colors.surface }}>
                <div className="text-3xl font-bold mb-2" style={{ color: theme.colors.primary }}>89%</div>
                <p style={{ color: theme.colors.textMuted }}>Time Savings</p>
              </div>
              <div className="p-6 rounded-2xl" style={{ backgroundColor: theme.colors.surface }}>
                <div className="text-3xl font-bold mb-2" style={{ color: theme.colors.primary }}>500+</div>
                <p style={{ color: theme.colors.textMuted }}>Distributors Trust Us</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Progressive Disclosure: Chat Interface (Secondary Layer)
  return (
    <div className="h-screen flex" style={{ backgroundColor: theme.colors.base, color: theme.colors.textPrimary }}>
      {/* Sidebar - Tertiary Layer */}
      <div className="w-64 border-r flex flex-col" style={{ backgroundColor: theme.colors.surface, borderColor: theme.colors.border }}>
        <div className="p-4 border-b" style={{ borderColor: theme.colors.border }}>
          <button 
            onClick={() => setCurrentView('welcome')}
            className="flex items-center gap-2 text-sm hover:opacity-80"
            style={{ color: theme.colors.textMuted }}
          >
            <ArrowRight className="w-4 h-4 rotate-180" />
            Back to Home
          </button>
        </div>
        
        <div className="p-4">
          <h3 className="font-semibold mb-3">Quick Actions</h3>
          <div className="space-y-2">
            {quickActions.map((action, i) => (
              <button
                key={i}
                onClick={() => setInput(action)}
                className="w-full text-left p-2 rounded-lg text-sm transition-all hover:scale-105"
                style={{ backgroundColor: theme.colors.elevated, color: theme.colors.textMuted }}
              >
                {action}
              </button>
            ))}
          </div>
        </div>
        
        <div className="mt-auto p-4 border-t" style={{ borderColor: theme.colors.border }}>
          <button className="w-full flex items-center gap-2 p-3 rounded-lg transition-all hover:scale-105" 
            style={{ backgroundColor: theme.colors.primary, color: theme.colors.base }}>
            <Share2 className="w-4 h-4" />
            <span className="font-semibold">Invite Team</span>
          </button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <div className="border-b p-4 flex items-center justify-between" style={{ backgroundColor: theme.colors.surface, borderColor: theme.colors.border }}>
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full flex items-center justify-center" style={{ backgroundColor: theme.colors.primary }}>
              <Sparkles className="w-4 h-4" style={{ color: theme.colors.base }} />
            </div>
            <div>
              <h2 className="font-semibold">Palmer AI Assistant</h2>
              <p className="text-xs" style={{ color: theme.colors.textMuted }}>
                {selectedTemplate ? `${templates.find(t => t.id === selectedTemplate)?.title} Workflow` : 'Product Intelligence Chat'}
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: theme.colors.success }}></div>
            <span className="text-xs" style={{ color: theme.colors.textMuted }}>Claude Sonnet 4</span>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.length === 0 ? (
            <div className="text-center py-12">
              <Lightbulb className="w-12 h-12 mx-auto mb-4" style={{ color: theme.colors.accent }} />
              <h3 className="text-lg font-semibold mb-2">Ready to transform your product intelligence?</h3>
              <p style={{ color: theme.colors.textMuted }}>Ask me anything about your products, catalogs, or industry insights.</p>
            </div>
          ) : (
            messages.map((message) => (
              <div key={message.id} className={`flex gap-4 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                {message.role === 'assistant' && (
                  <div className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0" style={{ backgroundColor: theme.colors.primary }}>
                    <Sparkles className="w-4 h-4" style={{ color: theme.colors.base }} />
                  </div>
                )}
                
                <div className={`max-w-2xl rounded-2xl px-6 py-4 ${
                  message.role === 'user' 
                    ? 'ml-12' 
                    : 'mr-12'
                }`} style={{ 
                  backgroundColor: message.role === 'user' ? theme.colors.primary : theme.colors.surface,
                  color: message.role === 'user' ? theme.colors.base : theme.colors.textPrimary
                }}>
                  <p className="leading-relaxed">{message.content}</p>
                  
                  {message.confidence && (
                    <div className="mt-3 pt-3 border-t" style={{ borderColor: theme.colors.border }}>
                      <div className="flex items-center justify-between text-xs" style={{ color: theme.colors.textMuted }}>
                        <span>Confidence: {Math.round(message.confidence * 100)}%</span>
                        <span>Claude Sonnet 4</span>
                      </div>
                    </div>
                  )}
                </div>
                
                {message.role === 'user' && (
                  <div className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0" style={{ backgroundColor: theme.colors.secondary }}>
                    <span className="text-sm font-bold" style={{ color: theme.colors.textPrimary }}>U</span>
                  </div>
                )}
              </div>
            ))
          )}
          
          {isProcessing && (
            <div className="flex gap-4">
              <div className="w-8 h-8 rounded-full flex items-center justify-center" style={{ backgroundColor: theme.colors.primary }}>
                <Sparkles className="w-4 h-4" style={{ color: theme.colors.base }} />
              </div>
              <div className="flex items-center gap-2 px-6 py-4 rounded-2xl" style={{ backgroundColor: theme.colors.surface }}>
                <div className="flex gap-1">
                  <div className="w-2 h-2 rounded-full animate-bounce" style={{ backgroundColor: theme.colors.primary }}></div>
                  <div className="w-2 h-2 rounded-full animate-bounce [animation-delay:0.1s]" style={{ backgroundColor: theme.colors.primary }}></div>
                  <div className="w-2 h-2 rounded-full animate-bounce [animation-delay:0.2s]" style={{ backgroundColor: theme.colors.primary }}></div>
                </div>
                <span className="text-sm ml-2" style={{ color: theme.colors.textMuted }}>Palmer is thinking...</span>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t p-6" style={{ backgroundColor: theme.colors.surface, borderColor: theme.colors.border }}>
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
                placeholder="Ask Palmer about your products, pricing, or market insights..."
                className="w-full rounded-xl px-6 py-4 pr-12 focus:outline-none focus:ring-2 transition-all"
                style={{ 
                  backgroundColor: theme.colors.elevated, 
                  color: theme.colors.textPrimary,
                  border: `1px solid ${theme.colors.border}`,
                  focusRingColor: theme.colors.primary
                }}
                disabled={isProcessing}
              />
              <button
                onClick={handleSendMessage}
                disabled={!input.trim() || isProcessing}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 p-2 rounded-lg transition-all disabled:opacity-50"
                style={{ backgroundColor: theme.colors.primary, color: theme.colors.base }}
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
            
            <button className="p-4 rounded-xl transition-all hover:scale-105" style={{ backgroundColor: theme.colors.elevated, color: theme.colors.textMuted }}>
              <Upload className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}