'use client'

import { motion } from 'framer-motion'
import { TrendingUp, Shield, Zap } from 'lucide-react'

export function ResponsiveHero() {
  const features = [
    {
      icon: TrendingUp,
      title: "Instant Analysis",
      description: "Get comprehensive insights in seconds, not weeks"
    },
    {
      icon: Shield,
      title: "Enterprise Grade",
      description: "Bank-level security with startup pricing"
    },
    {
      icon: Zap,
      title: "Zero Setup",
      description: "No integration needed - just enter a URL"
    }
  ]

  return (
    <div className="grid md:grid-cols-3 gap-8 mt-16 px-6">
      {features.map((feature, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 + index * 0.1 }}
          className="text-center"
        >
          <div className="inline-flex items-center justify-center w-16 h-16 bg-purple-500/20 rounded-2xl mb-4">
            <feature.icon className="w-8 h-8 text-purple-400" />
          </div>
          <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
          <p className="text-gray-400">{feature.description}</p>
        </motion.div>
      ))}
    </div>
  )
}
