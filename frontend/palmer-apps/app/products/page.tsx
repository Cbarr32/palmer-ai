'use client'
import { useState } from 'react'

export default function ProductOptimizer() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string>('')
  const [formData, setFormData] = useState({
    name: '',
    sku: '',
    manufacturer: '',
    description: '',
    specifications: '',
    industry: 'industrial'
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/products/optimize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setResult(data)
    } catch (error) {
      console.error('Error:', error)
      setError('Failed to optimize. Make sure the backend is running on port 8000.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-2">
          🤖 Palmer AI
        </h1>
        <p className="text-center text-gray-400 mb-8">
          Product Description Optimizer
        </p>
        
        <div className="bg-yellow-900/20 border border-yellow-600 rounded-lg p-6 mb-8">
          <h2 className="text-2xl font-bold text-yellow-400 mb-2">
            💰 Save 95% on Product Description Costs
          </h2>
          <p className="text-yellow-200">
            Manual Writing: $2-5 per description | Palmer AI: $0.10 per description
          </p>
        </div>

        <div className="bg-gray-800 rounded-lg shadow-lg p-8">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Product Name *</label>
              <input
                type="text"
                required
                className="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-white"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                placeholder="e.g., Heavy Duty Ball Valve 1 inch"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">SKU</label>
                <input
                  type="text"
                  className="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-white"
                  value={formData.sku}
                  onChange={(e) => setFormData({...formData, sku: e.target.value})}
                  placeholder="e.g., BV-1000-HD"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">Manufacturer</label>
                <input
                  type="text"
                  className="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-white"
                  value={formData.manufacturer}
                  onChange={(e) => setFormData({...formData, manufacturer: e.target.value})}
                  placeholder="e.g., FlowTech"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Industry</label>
              <select
                className="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-white"
                value={formData.industry}
                onChange={(e) => setFormData({...formData, industry: e.target.value})}
              >
                <option value="industrial">Industrial</option>
                <option value="electrical">Electrical</option>
                <option value="hvac">HVAC</option>
                <option value="plumbing">Plumbing</option>
                <option value="safety">Safety</option>
                <option value="tools">Tools</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-purple-600 text-white py-3 rounded-lg font-semibold hover:bg-purple-700 disabled:bg-gray-600"
            >
              {loading ? 'Optimizing...' : 'Optimize Description'}
            </button>
          </form>

          {error && (
            <div className="mt-4 bg-red-900/20 border border-red-600 p-4 rounded-lg">
              <p className="text-red-400">{error}</p>
            </div>
          )}

          {result && result.success && (
            <div className="mt-8 bg-green-900/20 border border-green-600 p-6 rounded-lg">
              <h3 className="text-xl font-bold mb-4 text-green-400">✨ Optimized Description:</h3>
              <p className="mb-4 text-gray-300">{result.optimized_product.optimized.description}</p>
              
              <h4 className="font-bold mb-2 text-green-400">Key Features:</h4>
              <ul className="list-disc list-inside mb-4 text-gray-300">
                {result.optimized_product.optimized.key_features.map((feature: string, i: number) => (
                  <li key={i}>{feature}</li>
                ))}
              </ul>
              
              <div className="bg-green-900/40 p-3 rounded">
                <p className="text-sm text-green-300">
                  <strong>Cost:</strong> {result.actual_cost} | 
                  <strong> Savings:</strong> {result.savings}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
