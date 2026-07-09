import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/')({
  component: () => (
    <div>
      <h2>Home Page</h2>
      <p>Welcome to the Home page.</p>
    </div>
  ),
})

