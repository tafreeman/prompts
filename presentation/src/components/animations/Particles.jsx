/**
 * Particles — canvas-based particle system.
 *
 * Extracted from the monolith (genai_advocacy_hub_13.jsx lines 464-553).
 * Supports three particle behaviours: 'hurdles' (upward burst),
 * 'human' (gentle drift with connecting lines), and 'sprint' (orbital).
 *
 * @example
 *   <Particles color="#F59E0B" type="hurdles" active={true} />
 */

import React, { useRef, useEffect } from "react";
import PropTypes from "prop-types";

import { TIMING } from "../../tokens/timing.ts";

/* ── entropy helpers (copied from monolith) ── */

let fallbackEntropyCursor = 0;
const FALLBACK_ENTROPY_DIVISOR = 997;

function getRandomUnit() {
  const cryptoApi = globalThis.crypto;

  if (cryptoApi && typeof cryptoApi.getRandomValues === "function") {
    return cryptoApi.getRandomValues(new Uint32Array(1))[0] / 0x100000000;
  }

  fallbackEntropyCursor = (fallbackEntropyCursor + 619) % FALLBACK_ENTROPY_DIVISOR;
  return fallbackEntropyCursor / FALLBACK_ENTROPY_DIVISOR;
}

/* ── component ── */

/**
 * @param {object} props
 * @param {string} props.color — base colour for particles (hex, e.g. "#F59E0B")
 * @param {'hurdles'|'human'|'sprint'} props.type — particle behaviour preset
 * @param {boolean} props.active — whether the animation is running
 */
function Particles({ color, type, active }) {
  const canvasRef = useRef(null);
  const pRef = useRef([]);
  const animRef = useRef(null);

  useEffect(() => {
    const c = canvasRef.current;
    if (!c) return;
    const ctx = c.getContext("2d");
    c.width = c.offsetWidth * 2;
    c.height = c.offsetHeight * 2;
    ctx.scale(2, 2);
    const W = c.offsetWidth;
    const H = c.offsetHeight;
    pRef.current = [];

    let n;
    if (type === "hurdles") {
      n = 60;
    } else if (type === "sprint") {
      n = 40;
    } else {
      n = 30;
    }

    for (let i = 0; i < n; i++) {
      const hurdleParticle = type === "hurdles";
      pRef.current.push({
        x: getRandomUnit() * W,
        y: getRandomUnit() * H,
        vx: hurdleParticle ? (getRandomUnit() - 0.3) * 3 : (getRandomUnit() - 0.5) * 0.5,
        vy: hurdleParticle ? -getRandomUnit() * 4 - 1 : (getRandomUnit() - 0.5) * 0.5,
        r: hurdleParticle ? getRandomUnit() * 3 + 1 : getRandomUnit() * 2 + 1,
        o: getRandomUnit() * 0.5 + 0.15,
        life: getRandomUnit() * 100,
      });
    }

    function draw() {
      ctx.clearRect(0, 0, W, H);
      pRef.current.forEach((p) => {
        p.life++;
        if (type === "hurdles") {
          p.x += p.vx;
          p.y += p.vy;
          p.vy -= 0.02;
          if (p.y < -10 || p.x < -10 || p.x > W + 10) {
            p.x = getRandomUnit() * W;
            p.y = H + 10;
            p.vy = -getRandomUnit() * 4 - 1;
            p.vx = (getRandomUnit() - 0.3) * 3;
          }
        } else if (type === "human") {
          p.x += Math.sin(p.life * 0.015) * 0.3;
          p.y += Math.cos(p.life * 0.012) * 0.3;
        } else if (type === "sprint") {
          const cx = W / 2;
          const cy = H / 2;
          const a = Math.atan2(p.y - cy, p.x - cx);
          p.x += Math.cos(a + Math.PI / 2) * 0.35;
          p.y += Math.sin(a + Math.PI / 2) * 0.35;
          const d = Math.sqrt((p.x - cx) ** 2 + (p.y - cy) ** 2);
          if (d > Math.max(W, H) * 0.55) {
            p.x = cx + (getRandomUnit() - 0.5) * W * 0.4;
            p.y = cy + (getRandomUnit() - 0.5) * H * 0.4;
          }
        } else {
          p.x += p.vx;
          p.y += p.vy;
          if (p.x < 0 || p.x > W) {
            p.vx *= -1;
          }
          if (p.y < 0 || p.y > H) {
            p.vy *= -1;
          }
        }
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle =
          color + Math.round(p.o * 255).toString(16).padStart(2, "0");
        ctx.fill();
      });

      if (type === "human") {
        const pts = pRef.current;
        for (let i = 0; i < pts.length; i++) {
          for (let j = i + 1; j < pts.length; j++) {
            const dx = pts[i].x - pts[j].x;
            const dy = pts[i].y - pts[j].y;
            const d = Math.sqrt(dx * dx + dy * dy);
            if (d < 120) {
              ctx.beginPath();
              ctx.moveTo(pts[i].x, pts[i].y);
              ctx.lineTo(pts[j].x, pts[j].y);
              ctx.strokeStyle =
                color +
                Math.round((1 - d / 120) * 40)
                  .toString(16)
                  .padStart(2, "0");
              ctx.lineWidth = 0.5;
              ctx.stroke();
            }
          }
        }
      }

      animRef.current = requestAnimationFrame(draw);
    }

    if (active) draw();
    return () => cancelAnimationFrame(animRef.current);
  }, [color, type, active]);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: "absolute",
        inset: 0,
        width: "100%",
        height: "100%",
        pointerEvents: "none",
        opacity: active ? 1 : 0,
        transition: `opacity ${TIMING.slow}s`,
      }}
    />
  );
}

Particles.propTypes = {
  color: PropTypes.string.isRequired,
  type: PropTypes.oneOf(["hurdles", "human", "sprint"]).isRequired,
  active: PropTypes.bool.isRequired,
};

export default Particles;
