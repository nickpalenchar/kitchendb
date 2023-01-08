import { render } from 'solid-js/web';

window._loadComponent = async (_component: string) => {
  const module = await import('./App.js');
  console.log("got the module", module);
  render(() => <module.default/>, document.getElementById('my-root') as HTMLElement);
}
