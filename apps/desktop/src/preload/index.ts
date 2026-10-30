import { contextBridge, ipcRenderer } from 'electron';
import type { Bridge } from '../shared/bridge';

const bridge: Bridge = {
  connection: () => ipcRenderer.invoke('connection'),
  tasks: () => ipcRenderer.invoke('tasks:list'),
  submit: (key) => ipcRenderer.invoke('tasks:submit', key),
  events: (id, after) => ipcRenderer.invoke('tasks:events', id, after)
};
contextBridge.exposeInMainWorld('autumn', bridge);
