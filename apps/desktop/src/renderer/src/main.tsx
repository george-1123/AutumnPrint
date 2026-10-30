import { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import type { Task, TaskEvent } from '@autumn/sdk';
import type { Bridge } from '../../shared/bridge';
import './style.css';

declare global { interface Window { autumn: Bridge } }
const status: Record<string, string> = {queued: '排队中', waiting_edge: '等待现场执行', succeeded: '诊断完成'};
function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [events, setEvents] = useState<TaskEvent[]>([]);
  const [selected, select] = useState('');
  const [connection, setConnection] = useState({mode: '', workspace: ''});
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  useEffect(() => {
    window.autumn.connection().then(setConnection).catch(() => setError('无法读取工作区连接'));
    let stopped = false;
    async function refresh() {
      try {
        const list = await window.autumn.tasks();
        if (!stopped) {setTasks(list); setError('');}
      } catch { if (!stopped) setError('后台连接中断，任务将保留。请检查后台状态。'); }
    }
    void refresh();
    const timer = setInterval(refresh, 750);
    return () => {stopped = true; clearInterval(timer);};
  }, []);
  useEffect(() => {
    if (!selected) return;
    let stopped = false;
    let cursor = 0;
    setEvents([]);
    let pending = false;
    async function refresh() {
      if (pending) return;
      pending = true;
      try {
        const batch = await window.autumn.events(selected, cursor);
        if (!stopped && batch.length) {
          cursor = batch[batch.length - 1].sequence;
          setEvents(previous => [...previous, ...batch]);
        }
      } catch { /* Task list reports connectivity errors. */ }
      finally {pending = false;}
    }
    void refresh();
    const timer = setInterval(refresh, 750);
    return () => {stopped = true; clearInterval(timer);};
  }, [selected]);
  async function submit() {
    setBusy(true);
    try { const task = await window.autumn.submit(crypto.randomUUID()); select(task.id); }
    catch {setError('提交失败，请检查后台连接。');}
    finally {setBusy(false);}
  }
  return <div className="shell">
    <aside><div className="brand">a<span>Autumn Print</span></div><small>工艺与生产工作台</small><nav>◈ 工程诊断</nav><footer>工作区<br/><strong>{connection.workspace || '连接中…'}</strong><p>{connection.mode === 'personal' ? '个人本地模式' : '企业模式'}</p></footer></aside>
    <main><header><span>工作台 / 工程诊断</span><span className="badge">开发预览 · Fake</span></header>
    <section className="intro"><p className="eyebrow">WORKSPACE DIAGNOSTICS</p><h1>让每一步执行，都有迹可循。</h1><p>检查 API、持久队列、worker 与现场端的完整协作链路。</p><button onClick={submit} disabled={busy}>{busy ? '正在提交…' : '运行链路诊断 →'}</button></section>
    {error && <p role="alert" className="error">{error}</p>}
    <div className="grid"><section className="card"><h2>诊断任务 <span>{tasks.length}</span></h2>{!tasks.length && <p className="muted">还没有任务。运行一次诊断，开始检查工程连接。</p>}
    {tasks.map(task => <button className={'task ' + (selected === task.id ? 'selected' : '')} key={task.id} onClick={() => select(task.id)}><strong>{status[task.status]}</strong><small>{task.id.slice(0, 8)}</small>{task.result && <p>{task.result.message}</p>}</button>)}</section>
    <section className="card"><h2>执行记录</h2><p className="muted">关闭窗口后后台继续运行，重新打开可补读记录。</p>{events.map(event => <div className="event" key={event.sequence}><span>#{event.sequence}</span><code>{event.kind}</code></div>)}</section></div>
    <p className="note">当前仅执行模拟模型与工具，不连接真实打印机或模型服务。</p></main></div>;
}
createRoot(document.getElementById('root')!).render(<App/>);
