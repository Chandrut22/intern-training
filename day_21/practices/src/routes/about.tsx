import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/about')({
  component: () => {
      return <div>Hello "/about"!</div>

  },
})

