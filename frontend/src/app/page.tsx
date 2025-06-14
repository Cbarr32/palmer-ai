// src/app/page.tsx - Palmer AI Landing Page
'use client'

import { motion } from 'framer-motion'
import { ArrowRight, Zap, Users, TrendingUp, CheckCircle, Play } from 'lucide-react'
import Link from 'next/link'
import { useState, useEffect } from 'react'

export default function LandingPage() {
  const [isVisible, setIsVisible] = useState(false)
  const [liveStats, setLiveStats] = useState({
    productsEnhanced: 1247,
    hoursaved: 89,
    revenueGenerated: 2300000
  })

  useEffect(() => {
    setIsVisible(true)
    // Animate live stats
    const interval = setInterval(() => {
      setLiveStats(prev => ({
        productsEnhanced: prev.productsEnhanced + Math.floor(Math.random() * 3),
        hoursaved: prev.hoursaved + Math.floor(Math.random() * 2),
        revenueGenerated: prev.revenueGenerated + Math.floor(Math.random() * 10000)
      }))
    }, 5000)
    return () => clearInterval(interval)
  }, [])

  const fadeInUp = {
    initial: { opacity: 0, y: 50 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6 }
  }

  return (
    <div className="min-h-screen bg-slate-900 text-slate-50">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-slate-900/90 backdrop-blur-sm border-b border-slate-800 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                Palmer AI
              </div>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <Link href="/demo" className="text-slate-300 hover:text-emerald-400 px-3 py-2 text-sm font-medium">
                  Demo
                </Link>
                <Link href="/pricing" className="text-slate-300 hover:text-emerald-400 px-3 py-2 text-sm font-medium">
                  Pricing
                </Link>
                <Link href="/trial" className="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                  Start Free Trial
                </Link>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div {...fadeInUp} className="mb-8">
            <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
              Transform{' '}
              <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                500 boring
              </span>
              <br />
              product descriptions into{' '}
              <span className="bg-gradient-to-r from-amber-400 to-orange-400 bg-clip-text text-transparent">
                contractor gold
              </span>
              <br />
              <span className="text-slate-400 text-4xl md:text-5xl">in 10 minutes</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-slate-300 mb-8 max-w-4xl mx-auto leading-relaxed">
              Palmer AI uses Claude Sonnet 4 to turn your bland product catalogs into compelling, 
              technical descriptions that make contractors call YOU instead of your competition.
            </p>
          </motion.div>

          {/* Live Stats */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3, duration: 0.6 }}
            className="flex flex-wrap justify-center gap-8 mb-12 text-center"
          >
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
              <div className="text-3xl font-bold text-emerald-400">{liveStats.productsEnhanced.toLocaleString()}</div>
              <div className="text-slate-400">Products Enhanced Today</div>
            </div>
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
              <div className="text-3xl font-bold text-amber-400">{liveStats.hoursaved}%</div>
              <div className="text-slate-400">Time Saved on Descriptions</div>
            </div>
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
              <div className="text-3xl font-bold text-cyan-400">${(liveStats.revenueGenerated/1000000).toFixed(1)}M</div>
              <div className="text-slate-400">Distributor Revenue Optimized</div>
            </div>
          </motion.div>

          {/* Primary CTA */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.6 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          >
            <Link 
              href="/demo"
              className="group bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-700 hover:to-emerald-800 text-white px-8 py-4 rounded-xl text-lg font-semibold flex items-center gap-2 transition-all duration-300 transform hover:scale-105 shadow-2xl shadow-emerald-900/50"
            >
              <Play size={20} />
              See Palmer AI in Action
              <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
            </Link>
            
            <Link 
              href="/trial"
              className="border-2 border-slate-600 hover:border-emerald-400 text-slate-300 hover:text-emerald-400 px-8 py-4 rounded-xl text-lg font-semibold transition-all duration-300"
            >
              Start Free Trial
            </Link>
          </motion.div>

          {/* Social Proof */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.9, duration: 0.6 }}
            className="mt-12 text-slate-400"
          >
            <p className="mb-4">Trusted by leading B2B distributors</p>
            <div className="flex justify-center items-center gap-8 opacity-60">
              <div className="text-2xl font-bold">Ferguson</div>
              <div className="text-2xl font-bold">Grainger</div>
              <div className="text-2xl font-bold">HD Supply</div>
              <div className="text-2xl font-bold">Winsupply</div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="py-20 px-4 bg-slate-800/50">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              HVAC contractors are calling you{' '}
              <span className="text-red-400">40 times a day</span>
              <br />
              asking "What's the part number for..."
            </h2>
            <p className="text-xl text-slate-300 max-w-4xl mx-auto">
              Your counter staff spends 60% of their time doing SKU lookups instead of selling. 
              Meanwhile, contractors are buying from whoever has the clearest product information.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: <Users className="text-red-400" size={48} />,
                title: "Counter Staff Overwhelmed",
                description: "40+ calls per day for basic product information kills productivity"
              },
              {
                icon: <TrendingUp className="text-amber-400" size={48} />,
                title: "Lost Sales Opportunities", 
                description: "Contractors buy from competitors with better product descriptions"
              },
              {
                icon: <Zap className="text-cyan-400" size={48} />,
                title: "Manual Catalog Updates",
                description: "Updating 500+ product descriptions takes weeks of manual work"
              }
            ].map((problem, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2, duration: 0.6 }}
                className="bg-slate-900/50 p-8 rounded-2xl border border-slate-700"
              >
                <div className="mb-4">{problem.icon}</div>
                <h3 className="text-xl font-semibold mb-3">{problem.title}</h3>
                <p className="text-slate-400">{problem.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Solution Preview */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Palmer AI turns this mess into magic
            </h2>
            <p className="text-xl text-slate-300 max-w-4xl mx-auto">
              Watch Palmer transform boring manufacturer specs into compelling, 
              contractor-focused descriptions that sell themselves.
            </p>
          </motion.div>

          {/* Before/After Example */}
          <div className="grid md:grid-cols-2 gap-8 mb-12">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="bg-red-900/20 border border-red-800 rounded-2xl p-6"
            >
              <h3 className="text-xl font-semibold mb-4 text-red-400">❌ Before (Generic)</h3>
              <div className="bg-slate-900 p-4 rounded-lg font-mono text-sm text-slate-400">
                <p><strong>Product:</strong> Model AC-2000 Unit</p>
                <p><strong>Description:</strong> Air conditioning unit. 2000 BTU capacity. Standard efficiency.</p>
                <p><strong>Specifications:</strong> See manual for details.</p>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="bg-emerald-900/20 border border-emerald-800 rounded-2xl p-6"
            >
              <h3 className="text-xl font-semibold mb-4 text-emerald-400">✅ After (Palmer AI)</h3>
              <div className="bg-slate-900 p-4 rounded-lg font-mono text-sm text-slate-300">
                <p><strong>AC-2000:</strong> Contractor-Grade Split System</p>
                <p><strong>Perfect for:</strong> 800-1200 sq ft residential installations. Ideal for retrofit jobs where efficiency matters.</p>
                <p><strong>Contractor Benefits:</strong> Quick-connect refrigerant lines, pre-charged system saves 2 hours install time. SEER 16 rating qualifies for utility rebates up to $500.</p>
                <p><strong>Stock Status:</strong> Ready to ship same-day. Compatible with Honeywell smart thermostats.</p>
              </div>
            </motion.div>
          </div>

          {/* Feature Benefits */}
          <div className="grid md:grid-cols-4 gap-6">
            {[
              "10x faster than manual writing",
              "Contractor-focused language", 
              "Technical accuracy guaranteed",
              "Works with any manufacturer"
            ].map((benefit, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1, duration: 0.6 }}
                className="flex items-center gap-3 bg-slate-800/50 p-4 rounded-xl"
              >
                <CheckCircle className="text-emerald-400 flex-shrink-0" size={24} />
                <span className="text-slate-300">{benefit}</span>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-20 px-4 bg-gradient-to-r from-emerald-900/20 to-cyan-900/20">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Ready to give your counter staff their life back?
            </h2>
            <p className="text-xl text-slate-300 mb-8">
              See Palmer AI enhance your first 50 products in under 5 minutes. 
              No setup fees, no long-term contracts.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                href="/demo"
                className="bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-700 hover:to-emerald-800 text-white px-8 py-4 rounded-xl text-lg font-semibold flex items-center justify-center gap-2 transition-all duration-300 transform hover:scale-105"
              >
                <Play size={20} />
                Watch 2-Minute Demo
              </Link>
              
              <Link 
                href="/trial"
                className="bg-white text-slate-900 hover:bg-slate-100 px-8 py-4 rounded-xl text-lg font-semibold transition-all duration-300"
              >
                Start Free Trial
              </Link>
            </div>

            <p className="text-sm text-slate-400 mt-6">
              💜 Built with love in memory of Mia Palmer Barreto
            </p>
          </motion.div>
        </div>
      </section>
    </div>
  )
}