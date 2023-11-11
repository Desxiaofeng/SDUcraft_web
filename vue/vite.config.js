import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite';
import { VantResolver } from '@vant/auto-import-resolver';
import NutUIResolver from '@nutui/nutui/dist/resolver'
import AutoImport from 'unplugin-auto-import/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import IconsResolver  from 'unplugin-icons/resolver'
import Icons from 'unplugin-icons/vite'
import { NaiveUiResolver } from 'unplugin-vue-components/resolvers'

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    outDir:'../www/vue-dist/'
  },
  plugins: [
    vue(),
    AutoImport({
        resolvers: [ElementPlusResolver(),IconsResolver({prefix: 'Icon',})],
        imports: [
            'vue',
            {
              'naive-ui': [
                'useDialog',
                'useMessage',
                'useNotification',
                'useLoadingBar'
              ]
            }
          ]
    }),
    Components({
        resolvers: [VantResolver(),NutUIResolver(),ElementPlusResolver(),IconsResolver({enabledCollections: ['ep'],}),NaiveUiResolver()],
    }),
    Icons({
        autoInstall: true,
    }),
  ],
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@nutui/nutui/dist/styles/variables.scss";`
      }
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
