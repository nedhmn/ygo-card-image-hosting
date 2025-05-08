// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

// https://astro.build/config
export default defineConfig({
  site: "https://nedhmn.github.io",
  base: "/ygo-card-image-hosting/",
  integrations: [
    starlight({
      title: "YGO Card Image Hosting",
      social: [
        {
          icon: "github",
          label: "GitHub",
          href: "https://github.com/nedhmn/ygo-card-image-hosting",
        },
      ],
      sidebar: [
        {
          label: "Getting Started",
          items: [
            { label: "Introduction", slug: "getting-started/introduction" },
            { label: "Installation", slug: "getting-started/installation" },
            { label: "Configuration", slug: "getting-started/configuration" },
            {
              label: "Running the Project",
              slug: "getting-started/running-the-project",
            },
          ],
        },
        {
          label: "Guides",
          items: [
            {
              label: "Serving GOAT Format Cards",
              slug: "guides/serving-goat-format-cards",
            },
            {
              label: "Serving HAT Format Cards",
              slug: "guides/serving-hat-format-cards",
            },
          ],
        },
      ],
    }),
  ],
});
