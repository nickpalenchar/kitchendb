import type { Component } from 'solid-js';

const Another: Component = () => {
  return (
    <div>
      hello from solid AGAIN!
    </div>
  );
};

// @ts-expect-error
window._componentAnother = Another;
