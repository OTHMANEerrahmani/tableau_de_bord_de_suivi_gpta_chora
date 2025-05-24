import { useEffect } from 'react'

export default function Home() {
  useEffect(() => {
    // Rediriger vers l'application Reflex
    window.location.href = '/'
  }, [])

  return null
} 