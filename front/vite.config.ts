import type {Plugin, ViteDevServer} from 'vite'
import {defineConfig} from 'vite'
import fs from 'fs'
import path from 'path'
import {svelte} from '@sveltejs/vite-plugin-svelte'
import {viteStaticCopy} from "vite-plugin-static-copy";


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
                    src: 'src/assets/**/*.{png,jpg,jpeg,svg,avif}', // chemin relatif à la racine du projet
                    dest: 'assets' // sera copié dans dist/assets
                }
            ]
        })

    ],

    build: {
        outDir: './dist',
        assetsDir: 'assets',
        emptyOutDir: true,
        manifest: true,
        rollupOptions: {
            input: {
                index: 'src/main.ts',
                //...glob.sync(resolve(__dirname, "src/**/*.svg")),
            }
        }
    },

    server: {
        cors: {origin: 'http://localhost:8000'},
    }
})
