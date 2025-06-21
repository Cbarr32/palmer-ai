'use client'

import { motion } from 'framer-motion'
import { X, Download, Share2, Sparkles } from 'lucide-react'

interface AnalysisModalProps {
  isOpen: boolean
  onClose: () => void
  result: any
}

export function AnalysisModal({ isOpen, onClose, result }: AnalysisModalProps) {
  if (!isOpen || !result) return null

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        className="bg-gradient-to-br from-gray-900 to-purple-900/20 border border-purple-500/20 rounded-2xl p-8 max-w-4xl w-full max-h-[80vh] overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-between items-start mb-6">
          <div>
            <h2 className="text-3xl font-bold text-white mb-2">
              {result.company_name || 'Company'} Analysis
            </h2>
            <p className="text-purple-400 flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              {result.level || 'Complete'} Intelligence Report
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="overflow-y-auto max-h-[50vh] mb-6">
          <div className="prose prose-invert max-w-none">
            <div className="bg-black/30 rounded-xl p-6 whitespace-pre-wrap">
              {result.insights || 'No insights available'}
            </div>
          </div>
          
          {result.teaser && (
            <div className="mt-4 p-4 bg-purple-500/20 rounded-lg border border-purple-500/40">
              <p className="text-purple-300 font-medium">{result.teaser}</p>
            </div>
          )}
        </div>

        <div className="flex gap-4">
          <button className="flex-1 bg-purple-600 hover:bg-purple-700 text-white py-3 px-6 rounded-lg font-medium transition-colors flex items-center justify-center gap-2">
            <Download className="w-5 h-5" />
            Download Report
          </button>
          <button className="flex-1 bg-gray-800 hover:bg-gray-700 text-white py-3 px-6 rounded-lg font-medium transition-colors flex items-center justify-center gap-2">
            <Share2 className="w-5 h-5" />
            Share Analysis
          </button>
        </div>
      </motion.div>
    </motion.div>
  )
}
