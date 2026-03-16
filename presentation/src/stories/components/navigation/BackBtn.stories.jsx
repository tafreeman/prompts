import React, { useState } from "react";
import { BackBtn } from "../../../components/navigation/BackBtn.tsx";

export default {
  title: "Navigation/BackBtn",
  component: BackBtn,
  parameters: {
    layout: "padded",
  },
};

export const Default = {
  args: {
    onClick: () => {},
  },
};

export const WithClickFeedback = {
  render: () => {
    const [clickCount, setClickCount] = useState(0);

    return (
      <div>
        <BackBtn onClick={() => setClickCount((n) => n + 1)} />
        <div style={{ fontSize: 13, color: "#888", marginTop: 8 }}>
          {clickCount === 0
            ? "Click the button to navigate back"
            : `Navigated back ${clickCount} time${clickCount === 1 ? "" : "s"}`}
        </div>
      </div>
    );
  },
};

export const InContext = {
  render: () => {
    const [view, setView] = useState("detail");

    return (
      <div
        style={{
          border: "1px solid #333",
          borderRadius: 8,
          padding: 24,
          maxWidth: 480,
          background: "#0f1117",
        }}
      >
        {view === "detail" ? (
          <div>
            <BackBtn onClick={() => setView("list")} />
            <div style={{ fontSize: 18, fontWeight: 700, color: "#fff", marginBottom: 8 }}>
              AI Governance Review
            </div>
            <div style={{ fontSize: 14, color: "#aaa", lineHeight: 1.6 }}>
              Detailed findings from the onboarding sprint code review cycle. All critical issues
              resolved before integration branch promotion.
            </div>
          </div>
        ) : (
          <div>
            <div style={{ fontSize: 14, color: "#aaa", marginBottom: 16 }}>
              Navigated back to list view. Click "Go to detail" to return.
            </div>
            <button
              onClick={() => setView("detail")}
              style={{
                background: "#22D3EE18",
                border: "none",
                color: "#22D3EE",
                fontSize: 13,
                padding: "6px 14px",
                borderRadius: 6,
                cursor: "pointer",
              }}
            >
              Go to detail
            </button>
          </div>
        )}
      </div>
    );
  },
};
