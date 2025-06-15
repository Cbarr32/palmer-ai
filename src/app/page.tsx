import ParticleBackground from '@/components/ParticleBackground'
import ResponsiveHero from '@/components/ResponsiveHero'

export default function Home() {
  return (
    <main className="relative min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      <ParticleBackground />
      <ResponsiveHero />
    </main>
  )
}
