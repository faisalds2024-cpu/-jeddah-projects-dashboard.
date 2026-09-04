export const number = (value) => new Intl.NumberFormat('en-US').format(Math.round(Number(value) || 0))
export const percent = (value) => `${(Number(value) || 0).toFixed(1)}%`
export const currency = (value) => { const n = Number(value) || 0; return `SAR ${n >= 1e9 ? `${(n / 1e9).toFixed(2)}B` : `${(n / 1e6).toFixed(1)}M`}` }
export const date = (value) => value ? new Intl.DateTimeFormat('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }).format(new Date(`${value}T00:00:00`)) : '—'
export const titleize = (value) => String(value || '').replaceAll('_', ' ')
