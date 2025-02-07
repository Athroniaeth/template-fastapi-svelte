import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig({
    plugins: [svelte()],

    build: {
        manifest: true,
        rollupOptions: {
            input: {
                main: 'src/main.ts'
            }
        }
    },

    server: {
        cors: { origin: 'http://localhost:8000' },
    }
})