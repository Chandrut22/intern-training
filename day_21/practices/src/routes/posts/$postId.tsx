import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/posts/$postId')({
  component: PostDetails,
})

function PostDetails() {
  const { postId } = Route.useParams()

  return (
    <div>
      <h2>Post Details</h2>
      <p>Post ID: {postId}</p>
    </div>
  )
}