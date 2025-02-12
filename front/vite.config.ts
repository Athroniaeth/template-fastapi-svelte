import type {Plugin, ViteDevServer} from 'vite'
import {defineConfig} from 'vite'
import {svelte} from '@sveltejs/vite-plugin-svelte'
import {glob} from 'glob'
import fs from 'fs'
import path, {resolve} from 'path'
import {viteStaticCopy} from 'vite-plugin-static-copy'

function watchJinja2(): Plugin {
    return {
        name: 'watch-jinja2',
        configureServer(server: ViteDevServer) {
            const edgeDir = path.resolve(__dirname, '..', 'templates')

            // @ts-ignore
            fs.watch(edgeDir, {recursive: true}, (_: any, filename: string) => {
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
        viteStaticCopy({
            targets: [
                {
                    src: 'src/assets/**/*.{png,jpg,jpeg,svg,avif}', // relative to project root
                    dest: 'assets' // will be copied to `dist/assets`
                }
            ]
        })
    ],

    build: {
        manifest: true,
        rollupOptions: {
            input: {
                main: 'src/main.ts',
            }
        }
    },

    server: {
        cors: {origin: 'http://localhost:8000'},
    }
})
