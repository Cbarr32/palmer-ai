'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, Zap, TrendingUp, Users, BarChart3, Sparkles } from 'lucide-react'

interface ConversionHookProps {
  hookData: any
  onUpgrade: () => void
  onDismiss: () => void
}

export function ConversionHook({ hookData, onUpgrade, onDismiss }: ConversionHookProps) {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    if (hookData?.hook_data?.upgrade_prompt || hookData?.hook_data?.stage === 'conversion') {
      setIsVisible(true)
    }
  }, [hookData])

  if (!hookData) return null

  const { message_count = 0, max_free_messages = 3, hook_data: hook } = hookData

  return (
    <AnimatePresence>
      {message_count > 0 && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
          className="fixed top-20 right-4 bg-purple-900/90 backdrop-blur-sm rounded-full px-4 py-2 flex items-center gap-2 z-40 shadow-lg"
        >
          <Sparkles className="w-4 h-4 text-purple-300" />
          <span className="text-white text-sm font-medium">
            {message_count}/{max_free_messages} Free Analyses Used
          </span>
        </motion.div>
      )}

      {isVisible && hook?.upgrade_prompt && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={onDismiss}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="bg-gradient-to-br from-purple-900 to-black border border-purple-500/20 rounded-2xl p-8 max-w-lg w-full shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={onDismiss}
              className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors"
            >
              <X className="w-6 h-6" />
            </button>

            <div className="text-center mb-6">
              <Zap className="w-16 h-16 text-purple-400 mx-auto mb-4" />
              <h2 className="text-3xl font-bold text-white mb-2">
                {hook.upgrade_prompt.title || 'Unlock Unlimited Intelligence'}
              </h2>
              <p className="text-gray-300">
                {hook.upgrade_prompt.message || 'Get unlimited access to Palmer AI'}
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-6">
              {(hook.upgrade_prompt.benefits || [
                "Unlimited Analyses",
                "Decision Maker Contacts", 
                "Real-time Monitoring",
                "API Access"
              ]).slice(0, 4).map((benefit: string, i: number) => {
                const icons = [TrendingUp, Users, BarChart3, Sparkles]
                const Icon = icons[i]
                return (
                  <div key={i} className="flex items-center gap-2 text-gray-300">
                    <Icon className="w-5 h-5 text-purple-400 flex-shrink-0" />
                    <span className="text-sm">{benefit}</span>
                  </div>
                )
              })}
            </div>

            {hook.upgrade_prompt.urgency && (
              <div className="bg-purple-800/50 rounded-lg p-3 mb-6 text-center">
                <p className="text-purple-200 text-sm font-medium">{hook.upgrade_prompt.urgency}</p>
              </div>
            )}

            <button
              onClick={onUpgrade}
              className="w-full bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white font-bold py-4 rounded-lg transition-all transform hover:scale-105 shadow-lg"
            >
              {hook.upgrade_prompt.cta || 'Upgrade Now - $97/month'}
            </button>

            <p className="text-center text-gray-400 text-xs mt-4">
              No credit card required • Cancel anytime • 7-day free trial
            </p>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
