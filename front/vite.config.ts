import type {Plugin, ViteDevServer} from 'vite'
import {defineConfig} from 'vite'
import {svelte} from '@sveltejs/vite-plugin-svelte'

import fs from 'fs'
import path from 'path'

function watchJinja2(): Plugin {
    return {
        name: 'watch-jinja2',
        configureServer(server: ViteDevServer) {
            const edgeDir = path.resolve(__dirname, '..', 'templates')
            fs.watch(edgeDir, {recursive: true}, (_, filename) => {
                // @ts-ignore
                if (filename.endsWith('.jinja2')) {
                    server.ws.send({type: 'full-reload'})
                }
            })
        },
    }
}

export default defineConfig({
    plugins: [
        svelte(),
        watchJinja2(),
    ],
    build: {
        manifest: true,
        rollupOptions: {
            input: {
                main: 'src/main.ts',
            },
        },
    },

    server: {
        cors: {
            origin: 'http://localhost:8000',
        },
    },
})
