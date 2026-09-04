import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, LineChart, Line, Legend, Cell, PieChart, Pie } from 'recharts'
import { Timer, TrendingUp, Clock3, AlertTriangle, Gauge, CalendarClock } from 'lucide-react'
import { ChartCard, KPICard, ProjectTable } from '../components/UI'
import { percent } from '../utils/formatters'
import { group, summary } from '../data/service'
import { localize } from '../i18n/labels'
import { chartStatusColor } from '../utils/chartColors'

export default function Schedule({ projects, data, onProject }) {
  const s = summary(projects)
  const delayed = [...projects].filter(p => p.Delay_Days > 0).sort((a, b) => b.Delay_Days - a.Delay_Days).slice(0, 10)
  const progress = [...projects].sort((a, b) => b.Schedule_Variance - a.Schedule_Variance).slice(0, 16)
  const scheduleStatus = group(projects, 'Schedule_Status')
  const ids = new Set(projects.map(p => p.Project_ID))
  const trend = data.progress.filter(row => ids.has(row.Project_ID)).reduce((acc, row) => { if (!acc[row.Date]) acc[row.Date] = { Date:row.Date, p:0, a:0, n:0 }; acc[row.Date].p += row.Planned_Progress; acc[row.Date].a += row.Actual_Progress; acc[row.Date].n++; return acc }, {})
  const trendData = Object.values(trend).map(row => ({ Date:row.Date, Planned:row.p / row.n, Actual:row.a / row.n }))
  const recovery = [['Projects on track',s.onTrack,chartStatusColor('On Track')],['Ahead of schedule',s.ahead,chartStatusColor('Ahead of Schedule')],['Delayed',s.delayed,chartStatusColor('Delayed')],['Critical delay',s.criticalDelay,chartStatusColor('Critical Delay')]]
  const max = Math.max(...recovery.map(item => item[1]), 1)
  const cards = [['On track',s.onTrack,Timer,'green'],['Ahead of schedule',s.ahead,TrendingUp,'cyan'],['Delayed',s.delayed,Clock3,'amber'],['Critical delay',s.criticalDelay,AlertTriangle,'red'],['Avg. schedule variance',percent(s.variance),Gauge,'blue'],['Average delay days',`${s.avgDelay.toFixed(0)} days`,CalendarClock,'blue']]
  return <>
    <div className="page-intro"><span className="eyebrow">{localize('Delivery intelligence')}</span><h1>{localize('Schedule & Progress Performance')}</h1><p>{localize('Understand variance early, isolate delays and track recovery across the portfolio.')}</p></div>
    <div className="kpi-grid six">{cards.map(([label,value,icon,tone], index) => <KPICard key={label} label={label} value={value} icon={icon} tone={tone} index={index}/>)}</div>
    <div className="chart-grid">
      <ChartCard title="Planned vs actual progress" className="wide"><ResponsiveContainer width="100%" height={320}><BarChart data={progress}><XAxis dataKey="Project_ID" tick={{fontSize:9}} interval={1}/><YAxis/><Tooltip/><Legend/><Bar dataKey="Planned_Progress" name={localize('Planned progress')} fill="#91b7d8" radius={[4,4,0,0]}/><Bar dataKey="Actual_Progress" name={localize('Actual progress')} fill="#1f5e97" radius={[4,4,0,0]}/></BarChart></ResponsiveContainer></ChartCard>
      <ChartCard title="Schedule status distribution"><ResponsiveContainer width="100%" height={225}><PieChart><Pie data={scheduleStatus} dataKey="value" nameKey="name" innerRadius={58} outerRadius={86} paddingAngle={3}>{scheduleStatus.map(item => <Cell key={item.name} fill={chartStatusColor(item.name)}/>)}</Pie><Tooltip formatter={(value, name) => [value, localize(name)]}/></PieChart></ResponsiveContainer><div className="legend compact-legend">{scheduleStatus.map(item => <span key={item.name}><i style={{background:chartStatusColor(item.name)}}/><b>{item.value}</b><em>{localize(item.name)}</em></span>)}</div></ChartCard>
      <ChartCard title="Schedule recovery indicators"><div className="health-pulse">{recovery.map(([name,value,color]) => <div className="health-row" key={name}><span>{localize(name)}</span><div className="health-track"><i style={{width:`${value / max * 100}%`,background:color}}/></div><b>{value}</b></div>)}</div></ChartCard>
      <ChartCard title="Progress trend" className="wide"><ResponsiveContainer width="100%" height={290}><LineChart data={trendData}><XAxis dataKey="Date" tick={{fontSize:10}} minTickGap={35}/><YAxis domain={[0,100]}/><Tooltip/><Legend/><Line type="monotone" dataKey="Planned" name={localize('Planned progress')} stroke="#8eb4d7" strokeWidth={2} dot={false}/><Line type="monotone" dataKey="Actual" name={localize('Actual progress')} stroke="#1f5e97" strokeWidth={2.5} dot={false}/></LineChart></ResponsiveContainer></ChartCard>
    </div>
    <ChartCard title="Most delayed projects"><ProjectTable projects={delayed} onProject={onProject}/></ChartCard>
  </>
}
