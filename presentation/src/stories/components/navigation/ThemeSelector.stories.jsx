import React from "react";
import { ThemeSelector } from "../../../components/navigation/ThemeSelector.jsx";
import { action } from "@storybook/addon-actions";

export default {
  title: "Navigation/ThemeSelector",
  component: ThemeSelector,
  parameters: {
    layout: "fullscreen",
  },
};

export const Default = {
  args: {
    onSelect: action("theme-selected"),
  },
};

export const WithLoggedSelection = {
  render: () => {
    const handleSelect = (theme) => {
      action("theme-selected")(theme);
      // eslint-disable-next-line no-console
      console.log("Selected theme:", theme.id, theme.name);
    };

    return <ThemeSelector onSelect={handleSelect} />;
  },
};
