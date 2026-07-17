import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: '歷史分享網',
      defaultLocale: 'root',
      locales: {
        root: {
          label: '繁體中文',
          lang: 'zh-TW',
        },
      },
      social: [],
      tableOfContents: false,
      sidebar: [
        {
          label: '文明的平行與岔路',
          items: [
            { autogenerate: { directory: '文明的平行與岔路' } },
          ],
        },
        {
          label: '中美洲文明的起源與演化',
          items: [
            { autogenerate: { directory: '中美洲文明的起源與演化' } },
          ],
        },
        {
          label: '美洲給世界的禮物',
          items: [
            { autogenerate: { directory: '美洲給世界的禮物' } },
          ],
        },
        {
          label: '馬雅文化',
          items: [
            { autogenerate: { directory: '馬雅文化' } },
          ],
        },
        {
          label: '墨西哥歷史',
          items: [
            { autogenerate: { directory: '墨西哥歷史' } },
          ],
        },
        {
          label: '中美洲歷史',
          items: [
            { autogenerate: { directory: '中美洲歷史' } },
          ],
        },
      ],
    }),
  ],
});
