import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/contact')({
  component: () => {
    return <div>Hello "/contact"!</div>

  },
})

