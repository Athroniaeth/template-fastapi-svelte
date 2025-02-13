import { mount } from 'svelte'
import './app.css'
import App from './components/App.svelte'

// Import all images in the assets folder to manifest / dist
import.meta.glob("../assets/**/*.{png,jpg,jpeg,svg,avif}")

const app = mount(App, {
  target: document.getElementById('app')!,
})

export default app
