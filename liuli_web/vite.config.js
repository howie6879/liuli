import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue({
            template: {
                compilerOptions: {
                    isCustomElement: (tag) => tag === 'hgroup'
                }
            }
        })
    ],
    server: {
        host: '0.0.0.0',
        port: 3000,
        open: false,
        https: false,
        proxy: {
            '/v1': {
                target: 'http://0.0.0.0:8765/',
                changeOrigin: true
            }
        }
    }
});
