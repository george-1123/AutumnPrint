import { app, BrowserWindow, ipcMain, net, protocol, session } from 'electron';
import { readFileSync } from 'node:fs';
import { dirname, join, resolve, sep } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { AutumnClient } from '@autumn/sdk';

const here = dirname(fileURLToPath(import.meta.url));
protocol.registerSchemesAsPrivileged([{ scheme: 'app', privileges: { standard: true, secure: true, supportFetchAPI: true } }]);
if (!app.requestSingleInstanceLock()) app.quit();
else app.whenReady().then(async () => {
  const configPath = process.env.AUTUMN_SESSION;
  if (!configPath) throw new Error('Start the development backend and set AUTUMN_SESSION');
  const config = JSON.parse(readFileSync(configPath, 'utf8'));
  const endpoint = new URL(config.url);
  if (config.mode === 'personal' && !['127.0.0.1', 'localhost'].includes(endpoint.hostname)) throw new Error('Personal API must be loopback');
  if (config.mode === 'enterprise' && endpoint.protocol !== 'https:') throw new Error('Enterprise API requires HTTPS');
  const api = new AutumnClient(config.url, config.desktop_token);
  const rendererRoot = resolve(here, '../renderer');
  protocol.handle('app', (request) => {
    const url = new URL(request.url);
    const target = resolve(rendererRoot, '.' + decodeURIComponent(url.pathname));
    if (url.hostname !== 'autumn' || !target.startsWith(rendererRoot + sep)) return new Response('Forbidden', {status: 403});
    return net.fetch(pathToFileURL(target).href);
  });
  session.defaultSession.setPermissionRequestHandler((_wc, _permission, callback) => callback(false));
  let window: BrowserWindow;
  const devUrl = process.env.ELECTRON_RENDERER_URL;
  function trusted(url: string) {
    return devUrl ? new URL(url).origin === new URL(devUrl).origin : url.startsWith('app://autumn/');
  }
  function handle(channel: string, callback: (...args: any[]) => unknown) {
    ipcMain.handle(channel, (event, ...args) => {
      if (event.sender !== window.webContents || event.senderFrame !== window.webContents.mainFrame || !trusted(event.senderFrame.url)) throw new Error('Untrusted IPC sender');
      return callback(...args);
    });
  }
  handle('connection', () => ({mode: config.mode, workspace: config.workspace}));
  handle('tasks:list', () => api.list());
  handle('tasks:submit', (key: unknown) => {
    if (typeof key !== 'string' || !/^[\w-]{1,128}$/.test(key)) throw new Error('Invalid request key');
    return api.submit(key);
  });
  handle('tasks:events', (id: unknown, after: unknown) => {
    if (typeof id !== 'string' || !/^[\da-f-]{36}$/.test(id) || !Number.isSafeInteger(after) || Number(after) < 0) throw new Error('Invalid event cursor');
    return api.events(id, Number(after));
  });
  function createWindow() {
    window = new BrowserWindow({ width: 1120, height: 760, title: 'Autumn Print',
      webPreferences: { preload: join(here, '../preload/index.cjs'), nodeIntegration: false, contextIsolation: true, sandbox: true } });
    window.webContents.setWindowOpenHandler(() => ({action: 'deny'}));
    window.webContents.on('will-navigate', event => event.preventDefault());
    if (devUrl) void window.loadURL(devUrl);
    else void window.loadURL('app://autumn/index.html');
  }
  createWindow();
  app.on('second-instance', () => { if (window.isDestroyed()) createWindow(); else window.focus(); });
  app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });
});
// The independently launched Python host owns all background processes.
app.on('window-all-closed', () => app.quit());
