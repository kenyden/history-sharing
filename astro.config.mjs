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
      sidebar: [
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
