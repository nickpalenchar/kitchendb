import type { Component } from 'solid-js';

const App: Component = () => {
  console.log('hello????')
  return (
    <div>
      hello from solid!
    </div>
  );
};

window._componentApp = App;
export default App;