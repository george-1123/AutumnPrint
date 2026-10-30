import { _electron as electron } from '@playwright/test';
import assert from 'node:assert/strict';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';

const root = process.cwd();
const config = path.join(root, '.runtime/session.json');
async function launch() {
  const env = {...process.env, AUTUMN_SESSION: config};
  delete env.ELECTRON_RUN_AS_NODE;
  const app = await electron.launch({args: [path.join(root, 'apps/desktop')], env});
  const page = await app.firstWindow();
  await page.getByRole('heading', {name: '让每一步执行，都有迹可循。'}).waitFor();
  return {app, page};
}

let {app, page} = await launch();
try {
  const previous = await page.evaluate(() => window.autumn.tasks());
  await page.getByRole('button', {name: '运行链路诊断 →'}).click();
  await page.waitForFunction(async count => (await window.autumn.tasks()).length > count, previous.length);
  const task = await page.evaluate(async ids => (await window.autumn.tasks()).find(task => !ids.includes(task.id)), previous.map(task => task.id));
  assert.ok(task);
  await app.close();
  // UI closure cannot own the worker lifetime; reconnect to the same durable task.
  ({app, page} = await launch());
  await page.getByText(task.id.slice(0, 8), {exact: true}).waitFor();
  await page.getByText(task.id.slice(0, 8), {exact: true}).click();
  await page.getByText('fake_tool_completed', {exact: true}).waitFor();
  assert.equal(await page.evaluate(() => typeof window.require), 'undefined');
  await assert.rejects(page.evaluate(() => window.autumn.submit('../invalid')));
  assert.equal(await page.evaluate(() => Object.keys(window.autumn).length), 4);
  const directory = path.join(root, '.runtime');
  await mkdir(directory, {recursive: true});
  await page.screenshot({path: path.join(directory, 'desktop.png')});
  console.log('Electron roundtrip, close/reopen replay, sandbox bridge and IPC validation passed');
} finally {
  await app.close();
}
