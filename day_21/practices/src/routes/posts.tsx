// import { createFileRoute } from '@tanstack/react-router'

// type SearchParams = {
//   page: number
//   sort: 'asc' | 'desc'
// }

// export const Route = createFileRoute('/posts')({
//   validateSearch: (search): SearchParams => ({
//     page: Number(search.page ?? 1),
//     sort: search.sort === 'desc' ? 'desc' : 'asc',
//   }),
//   component: Posts,
// })

// function Posts() {
//   const search = Route.useSearch()

//   return (
//     <div>
//       <h2>Posts</h2>

//       <p>Page: {search.page}</p>
//       <p>Sort: {search.sort}</p>
//     </div>
//   )
// }

import { createFileRoute } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'

export const Route = createFileRoute('/posts')({
  component: Posts,
})

type Post = {
  id: number
  title: string
  body: string
}

function Posts() {
  const {
    data,
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ['posts'],
    queryFn: async () => {
      const response = await fetch(
        'https://jsonplaceholder.typicode.com/posts'
      )

      if (!response.ok) {
        throw new Error('Failed to fetch posts')
      }

      return response.json() as Promise<Post[]>
    },
  })

  if (isLoading) {
    return <h2>Loading...</h2>
  }

  if (isError) {
    return <h2>{error.message}</h2>
  }

  return (
    <div>
      <h2>Posts</h2>

      <ul>
        {data.map((post) => (
          <li key={post.id}>
            {post.title}
          </li>
        ))}
      </ul>
    </div>
  )
}