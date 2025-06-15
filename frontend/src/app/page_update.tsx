// Add these imports to your page.tsx
import { ConversionHook } from '@/components/ConversionHook'

// Add to your state
const [conversionHookData, setConversionHookData] = useState(null)

// Update your API call to use the hook endpoint
const response = await fetch('http://localhost:8000/palmer/analyze-with-hook', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ company_name, url })
})

const data = await response.json()
setAnalysisResult(data.analysis)
setConversionHookData(data.conversion_hook)

// Add the component to your JSX
<ConversionHook 
  hookData={conversionHookData}
  onUpgrade={() => window.location.href = '/pricing'}
  onDismiss={() => setConversionHookData(null)}
/>
