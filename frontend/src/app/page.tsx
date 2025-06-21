'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ResponsiveHero } from '@/components/ResponsiveHero'
import { ParticleBackground } from '@/components/ParticleBackground'
import { AnalysisModal } from '@/components/AnalysisModal'
import { ConversionHook } from '@/components/ConversionHook'
import { Search, TrendingUp, Shield, Zap, ArrowRight, CheckCircle } from 'lucide-react'

export default function Home() {
  const [companyUrl, setCompanyUrl] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [conversionHookData, setConversionHookData] = useState(null)
  const [showModal, setShowModal] = useState(false)

  const handleAnalyze = async () => {
    if (!companyUrl.trim()) return
    
    setIsAnalyzing(true)
    try {
      const response = await fetch('http://localhost:8000/palmer/analyze-with-hook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          company_name: companyUrl,
          url: companyUrl.includes('.') ? companyUrl : `${companyUrl}.com`
        })
      })
      
      const data = await response.json()
      
      if (response.status === 403) {
        setConversionHookData({
          message_count: 3,
          max_free_messages: 3,
          hook_data: {
            stage: 'conversion',
            upgrade_prompt: data.detail
          }
        })
      } else {
        setAnalysisResult(data.analysis)
        setConversionHookData(data.conversion_hook)
        setShowModal(true)
      }
    } catch (error) {
      console.error('Analysis error:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-900 via-purple-900/20 to-black text-white overflow-hidden">
      <ParticleBackground />
      
      {/* Navigation */}
      <nav className="relative z-10 flex justify-between items-center p-6 lg:px-12">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center gap-2"
        >
          <Zap className="w-8 h-8 text-purple-400" />
          <span className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            Palmer AI
          </span>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center gap-6"
        >
          <a href="#features" className="hover:text-purple-400 transition-colors">Features</a>
          <a href="#pricing" className="hover:text-purple-400 transition-colors">Pricing</a>
          <button className="bg-purple-600 hover:bg-purple-700 px-6 py-2 rounded-lg font-medium transition-all transform hover:scale-105">
            Get Started
          </button>
        </motion.div>
      </nav>

      {/* Hero Section */}
      <section className="relative z-10 px-6 lg:px-12 py-20 max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl lg:text-7xl font-bold mb-6 bg-gradient-to-r from-white via-purple-200 to-purple-400 bg-clip-text text-transparent leading-tight">
            B2B Intelligence
            <br />
            <span className="text-3xl lg:text-5xl">In Seconds, Not Weeks</span>
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-2">
            Transform any company URL into comprehensive competitive intelligence.
            What takes consultants weeks, Palmer AI delivers in seconds.
          </p>
          <p className="text-sm text-purple-400 font-medium">
            Trusted by 500+ industrial distributors • No integration required
          </p>
        </motion.div>

        {/* Search Box */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="max-w-2xl mx-auto mb-16"
        >
          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl blur-xl opacity-50 group-hover:opacity-75 transition-opacity"></div>
            <div className="relative bg-gray-900/90 backdrop-blur-sm rounded-2xl p-2 border border-purple-500/20">
              <div className="flex items-center">
                <Search className="w-6 h-6 text-gray-400 ml-4" />
                <input
                  type="text"
                  value={companyUrl}
                  onChange={(e) => setCompanyUrl(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
                  placeholder="Enter any company URL or name..."
                  className="flex-1 bg-transparent px-4 py-4 text-lg focus:outline-none placeholder-gray-500"
                />
                <button
                  onClick={handleAnalyze}
                  disabled={isAnalyzing}
                  className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 px-8 py-4 rounded-xl font-semibold transition-all transform hover:scale-105 disabled:hover:scale-100 flex items-center gap-2"
                >
                  {isAnalyzing ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                      Analyzing...
                    </>
                  ) : (
                    <>
                      Analyze Now
                      <ArrowRight className="w-5 h-5" />
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
          <p className="text-center text-sm text-gray-400 mt-4">
            Try: "ibm.com", "acme-hvac.com", or any B2B company
          </p>
        </motion.div>

        {/* Value Props */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="grid md:grid-cols-3 gap-8 mb-20"
        >
          {[
            {
              icon: TrendingUp,
              title: "Instant Intelligence",
              description: "Complete competitive analysis in seconds. No consultants, no waiting.",
              color: "from-purple-500 to-pink-500"
            },
            {
              icon: Shield,
              title: "Zero Integration",
              description: "Just enter a URL. No setup, no IT involvement, no training needed.",
              color: "from-blue-500 to-purple-500"
            },
            {
              icon: Zap,
              title: "$30K → $97",
              description: "Replace enterprise tools costing $30K/year with our $97/month solution.",
              color: "from-pink-500 to-orange-500"
            }
          ].map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 + index * 0.1 }}
              className="relative group"
            >
              <div className={`absolute inset-0 bg-gradient-to-r ${feature.color} rounded-2xl blur-xl opacity-20 group-hover:opacity-40 transition-opacity`}></div>
              <div className="relative bg-gray-900/50 backdrop-blur-sm rounded-2xl p-8 border border-purple-500/20 hover:border-purple-500/40 transition-colors">
                <feature.icon className="w-12 h-12 text-purple-400 mb-4" />
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-400">{feature.description}</p>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Social Proof */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="text-center"
        >
          <p className="text-sm text-gray-400 mb-4">TRUSTED BY INDUSTRY LEADERS</p>
          <div className="flex flex-wrap justify-center items-center gap-8 opacity-50">
            {['HVAC Masters', 'Industrial Supply Co', 'TechFlow Systems', 'Global Machinery', 'ProBuild Solutions'].map((company, i) => (
              <div key={i} className="text-gray-500 font-semibold">{company}</div>
            ))}
          </div>
        </motion.div>
      </section>

      {/* Features Section */}
      <section id="features" className="relative z-10 py-20 px-6 lg:px-12 bg-black/50">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">Intelligence That Drives Revenue</h2>
            <p className="text-xl text-gray-400">Every feature designed to help you win more deals</p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-12">
            {[
              {
                title: "Company Deep Dive",
                description: "Instant analysis of any B2B company including size, growth, technology stack, and market position.",
                features: ["Financial indicators", "Employee insights", "Tech stack detection", "Growth signals"]
              },
              {
                title: "Competitive Intelligence", 
                description: "Know your competition better than they know themselves. Track pricing, positioning, and strategies.",
                features: ["Pricing analysis", "Product comparison", "Market positioning", "Win/loss patterns"]
              },
              {
                title: "Decision Maker Identification",
                description: "Find the right contacts with buying power. Direct paths to decision makers.",
                features: ["Contact discovery", "Org structure mapping", "Buying committee ID", "Engagement insights"]
              },
              {
                title: "Real-Time Monitoring",
                description: "Stay ahead with alerts on competitor moves, market changes, and opportunities.",
                features: ["Change detection", "New product alerts", "Personnel updates", "Market shifts"]
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: index % 2 === 0 ? -20 : 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                className="bg-gray-900/50 backdrop-blur-sm rounded-2xl p-8 border border-purple-500/20"
              >
                <h3 className="text-2xl font-semibold mb-4">{feature.title}</h3>
                <p className="text-gray-400 mb-6">{feature.description}</p>
                <ul className="space-y-2">
                  {feature.features.map((item, i) => (
                    <li key={i} className="flex items-center gap-2 text-gray-300">
                      <CheckCircle className="w-5 h-5 text-purple-400" />
                      {item}
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Modals */}
      <AnimatePresence>
        {showModal && analysisResult && (
          <AnalysisModal
            isOpen={showModal}
            onClose={() => setShowModal(false)}
            result={analysisResult}
          />
        )}
      </AnimatePresence>

      <ConversionHook
        hookData={conversionHookData}
        onUpgrade={() => window.location.href = '/pricing'}
        onDismiss={() => setConversionHookData(null)}
      />
    </main>
  )
}
