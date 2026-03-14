import { useEffect, useState } from "react";

function readViewport() {
  if (typeof window === "undefined") {
    return {
      width: 1440,
      height: 900,
      isPhone: false,
      isCompact: false,
      pagePaddingX: 48,
      pagePaddingTop: 36,
      pagePaddingBottom: 48,
      titleSize: 42,
      heroTitleSize: 44,
      sectionTitleSize: 32,
      bodySize: 15,
      subtitleSize: 16,
      cardGap: 20,
      tileMinHeight: 300,
      overlayScroll: "hidden",
    };
  }

  const width = window.innerWidth;
  const height = window.innerHeight;
  const isPhone = width < 720;
  const isCompact = isPhone || width < 1100 || height < 820;

  return {
    width,
    height,
    isPhone,
    isCompact,
    pagePaddingX: isPhone ? 16 : isCompact ? 24 : 48,
    pagePaddingTop: isPhone ? 20 : isCompact ? 28 : 36,
    pagePaddingBottom: isPhone ? 28 : isCompact ? 36 : 48,
    titleSize: isPhone ? 30 : isCompact ? 36 : 42,
    heroTitleSize: isPhone ? 32 : isCompact ? 38 : 44,
    sectionTitleSize: isPhone ? 26 : isCompact ? 30 : 32,
    bodySize: isPhone ? 13 : isCompact ? 14 : 15,
    subtitleSize: isPhone ? 14 : 16,
    cardGap: isPhone ? 12 : isCompact ? 16 : 20,
    tileMinHeight: isPhone ? 220 : isCompact ? 260 : 300,
    overlayScroll: isCompact ? "auto" : "hidden",
  };
}

export function usePresentationViewport() {
  const [viewport, setViewport] = useState(readViewport);

  useEffect(() => {
    let frame = null;

    const handleResize = () => {
      if (frame != null) {
        window.cancelAnimationFrame(frame);
      }
      frame = window.requestAnimationFrame(() => {
        setViewport(readViewport());
      });
    };

    window.addEventListener("resize", handleResize);
    return () => {
      if (frame != null) {
        window.cancelAnimationFrame(frame);
      }
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return viewport;
}

export default usePresentationViewport;
