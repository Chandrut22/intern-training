import { createRouter } from '@tanstack/react-router'
import { routeTree } from './routeTree.gen'

export const router = createRouter({
    routeTree,
})

// Correct way to track navigation events in TanStack Router
router.subscribe('onBeforeNavigate', (event) => {
    console.log("Moving to target URL:", event.toLocation.pathname);
})

declare module '@tanstack/react-router' {
    interface Register {
        router: typeof router
    }
}
