import React, { useEffect, useState } from 'react';

const API_URL = 'http://localhost:5000';

export default function MessageManager() {
  const [messages, setMessages] = useState([]);
  const [form, setForm] = useState({ template_name: '', body_template: '' });
  const [editingId, setEditingId] = useState(null);

  const loadMessages = () => {
    fetch(`${API_URL}/messages`)
      .then(r => r.json())
      .then(setMessages);
  };

  useEffect(() => {
    loadMessages();
  }, []);

  const submit = e => {
    e.preventDefault();
    const method = editingId ? 'PUT' : 'POST';
    const url = editingId ? `${API_URL}/messages/${editingId}` : `${API_URL}/messages`;
    fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    }).then(() => {
      setForm({ template_name: '', body_template: '' });
      setEditingId(null);
      loadMessages();
    });
  };

  const edit = msg => {
    setEditingId(msg.id);
    setForm({ template_name: msg.template_name, body_template: msg.body_template });
  };

  const remove = id => {
    fetch(`${API_URL}/messages/${id}`, { method: 'DELETE' })
      .then(loadMessages);
  };

  return (
    <div>
      <form onSubmit={submit} style={{ marginBottom: '1rem' }}>
        <input
          placeholder="Template Name"
          value={form.template_name}
          onChange={e => setForm({ ...form, template_name: e.target.value })}
        />
        <input
          placeholder="Body Template"
          value={form.body_template}
          onChange={e => setForm({ ...form, body_template: e.target.value })}
          style={{ width: '300px', marginLeft: '0.5rem' }}
        />
        <button type="submit" style={{ marginLeft: '0.5rem' }}>
          {editingId ? 'Update' : 'Create'}
        </button>
      </form>
      <ul>
        {messages.map(m => (
          <li key={m.id} style={{ marginBottom: '0.5rem' }}>
            <strong>{m.template_name}</strong>: {m.body_template}{' '}
            <button onClick={() => edit(m)}>Edit</button>
            <button onClick={() => remove(m.id)} style={{ marginLeft: '0.5rem' }}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
