"use client";

import { useState } from "react";
import { Upload, FileText, Brain, Sparkles, Play, CheckCircle } from "lucide-react";

export default function Home() {
  const [activeTab, setActiveTab] = useState("upload");
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileUpload = () => {
    setIsProcessing(true);
    setTimeout(() => {
      setIsProcessing(false);
      setActiveTab("analyze");
    }, 2000);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
            RFP Intelligence Platform
          </h1>
          <p className="text-xl text-gray-300">
            LOCAL DEVELOPMENT - AI-powered RFP completion
          </p>
        </header>

        <div className="max-w-6xl mx-auto">
          <div className="bg-slate-800/50 backdrop-blur rounded-2xl shadow-2xl overflow-hidden border border-slate-700">
            <div className="flex border-b border-slate-700">
              {["upload", "analyze", "respond", "demo"].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`flex-1 px-6 py-4 flex items-center justify-center gap-2 transition-all ${
                    activeTab === tab
                      ? "bg-blue-600/20 text-blue-400 border-b-2 border-blue-500"
                      : "text-gray-400 hover:bg-slate-700/50"
                  }`}
                >
                  {tab === "upload" && <Upload className="w-5 h-5" />}
                  {tab === "analyze" && <Brain className="w-5 h-5" />}
                  {tab === "respond" && <FileText className="w-5 h-5" />}
                  {tab === "demo" && <Sparkles className="w-5 h-5" />}
                  <span className="capitalize">{tab}</span>
                </button>
              ))}
            </div>

            <div className="p-8">
              {activeTab === "upload" && (
                <div className="text-center py-16">
                  <div className="mb-8">
                    <Upload className="w-20 h-20 mx-auto text-blue-400 mb-4" />
                    <h2 className="text-3xl font-semibold mb-2">Upload RFP Document</h2>
                    <p className="text-gray-400 mb-6">
                      Drag and drop your RFP file or click to browse
                    </p>
                  </div>
                  
                  <div className="border-2 border-dashed border-slate-600 rounded-xl p-8 mb-6 hover:border-blue-500 transition-colors cursor-pointer">
                    <p className="text-gray-500 mb-4">Supported formats: PDF, DOCX, TXT</p>
                    <button 
                      onClick={handleFileUpload}
                      className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2 mx-auto"
                    >
                      {isProcessing ? (
                        <>Processing...</>
                      ) : (
                        <>
                          <Upload className="w-4 h-4" />
                          Select File
                        </>
                      )}
                    </button>
                  </div>
                </div>
              )}

              {activeTab === "analyze" && (
                <div className="space-y-6">
                  <h2 className="text-3xl font-semibold flex items-center gap-3">
                    <Brain className="w-8 h-8 text-blue-400" />
                    AI-Powered Analysis
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-slate-700/50 p-6 rounded-lg">
                      <h3 className="text-xl font-semibold mb-3 text-blue-400">Requirements Extracted</h3>
                      <p className="text-gray-300">47 technical requirements identified</p>
                    </div>
                    <div className="bg-slate-700/50 p-6 rounded-lg">
                      <h3 className="text-xl font-semibold mb-3 text-purple-400">Gap Analysis</h3>
                      <p className="text-gray-300">12 areas need attention</p>
                    </div>
                  </div>
                  <button className="px-6 py-3 bg-green-600 rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2">
                    <Play className="w-4 h-4" />
                    Start Deep Analysis
                  </button>
                </div>
              )}

              {activeTab === "respond" && (
                <div className="space-y-6">
                  <h2 className="text-3xl font-semibold flex items-center gap-3">
                    <FileText className="w-8 h-8 text-green-400" />
                    Generate Response
                  </h2>
                  <div className="bg-slate-700/50 p-6 rounded-lg">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-xl font-semibold">Response Progress</h3>
                      <span className="text-green-400">75% Complete</span>
                    </div>
                    <div className="w-full bg-slate-600 rounded-full h-3">
                      <div className="bg-green-500 h-3 rounded-full" style={{width: '75%'}}></div>
                    </div>
                  </div>
                  <button className="px-6 py-3 bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors">
                    Generate Full Response
                  </button>
                </div>
              )}

              {activeTab === "demo" && (
                <div className="space-y-6">
                  <h2 className="text-3xl font-semibold flex items-center gap-3">
                    <Sparkles className="w-8 h-8 text-yellow-400" />
                    Interactive Demo Builder
                  </h2>
                  <p className="text-gray-300">
                    Generate working prototypes based on RFP requirements
                  </p>
                  <div className="bg-slate-700/50 p-6 rounded-lg">
                    <h3 className="text-xl font-semibold mb-3">Demo Features</h3>
                    <ul className="space-y-2">
                      <li className="flex items-center gap-2 text-gray-300">
                        <CheckCircle className="w-4 h-4 text-green-400" />
                        Live website preview
                      </li>
                      <li className="flex items-center gap-2 text-gray-300">
                        <CheckCircle className="w-4 h-4 text-green-400" />
                        Interactive components
                      </li>
                      <li className="flex items-center gap-2 text-gray-300">
                        <CheckCircle className="w-4 h-4 text-green-400" />
                        Mobile responsive
                      </li>
                    </ul>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        <footer className="text-center mt-12 text-gray-500">
          <p>Running on localhost:3000 | Development Mode</p>
        </footer>
      </div>
    </main>
  );
}
