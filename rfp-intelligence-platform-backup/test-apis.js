require('dotenv').config({ path: '.env.local' });

console.log('Testing API Keys...\n');

// Check if keys exist
const openaiKey = process.env.OPENAI_API_KEY;
const anthropicKey = process.env.ANTHROPIC_API_KEY;

if (openaiKey) {
  console.log('✅ OpenAI Key found:', openaiKey.substring(0, 20) + '...');
} else {
  console.log('❌ OpenAI Key missing');
}

if (anthropicKey) {
  console.log('✅ Anthropic Key found:', anthropicKey.substring(0, 20) + '...');
} else {
  console.log('❌ Anthropic Key missing');
}

// Test OpenAI
async function testOpenAI() {
  try {
    const response = await fetch('https://api.openai.com/v1/models', {
      headers: { 'Authorization': `Bearer ${openaiKey}` }
    });
    if (response.ok) {
      console.log('✅ OpenAI API connection successful');
    } else {
      console.log('❌ OpenAI API error:', response.status);
    }
  } catch (error) {
    console.log('❌ OpenAI connection failed:', error.message);
  }
}

testOpenAI();
