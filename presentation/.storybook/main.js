/** @type {import('@storybook/react-vite').StorybookConfig} */
const config = {
  stories: [
    "../src/**/*.stories.@(js|jsx)",
  ],
  addons: [
    "@storybook/addon-docs",
    "@storybook/addon-a11y",
    "@storybook/addon-onboarding",
  ],
  framework: "@storybook/react-vite",
};

export default config;
