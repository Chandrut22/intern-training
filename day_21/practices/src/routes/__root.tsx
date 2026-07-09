import { Outlet, Link, createRootRoute } from '@tanstack/react-router'

export const Route = createRootRoute({
  component: () => (
    <>
        <header>
        <h1>TanStack Router Demo</h1>

        <nav>
            <Link to="/">Home</Link>{" | "}
            <Link to="/about">About</Link>{" | "}
            <Link to="/contact">Contact</Link>{" | "}
            <Link to="/posts" search={{page: 1,sort: "asc",}}>Posts</Link>
        </nav>

        <hr />
      </header>

      <main>
        <Outlet />
      </main>
    </>
  ),
})


