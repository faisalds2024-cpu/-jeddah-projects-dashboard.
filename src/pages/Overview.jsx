import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts'
import { BriefcaseBusiness, Landmark, WalletCards, ChartNoAxesCombined, CheckCircle2, Clock3, ShieldAlert } from 'lucide-react'
import { ChartCard, KPICard, ProjectTable, RankedBars } from '../components/UI'
import { currency, percent } from '../utils/formatters'
import { completionBuckets, group, summary } from '../data/service'
import { localize, projectCount } from '../i18n/labels'
import { chartStatusColor } from '../utils/chartColors'

const healthColor = { Healthy:'#1ca98a', Monitor:'#e4a62b', 'At Risk':'#e8786c', Critical:'#ca5650' }

export default function Overview({ projects, onProject, t }) {
  const s = summary(projects), status = group(projects, 'Status'), sector = group(projects, 'Sector'), health = group(projects, 'Health_Status')
  const maxHealth = Math.max(...health.map(d => d.value), 1)
  const attention = [...projects].filter(p => p.Health_Status === 'Critical' || p.Delay_Days > 90).sort((a, b) => b.Delay_Days - a.Delay_Days).slice(0, 7)
  const cards = [[t('totalProjects'),s.total,BriefcaseBusiness,'blue'],[t('totalValue'),currency(s.contract),Landmark,'cyan'],[t('approvedBudget'),currency(s.budget),WalletCards,'blue'],[t('actualProgress'),percent(s.actual),ChartNoAxesCombined,'cyan'],[t('completed'),s.completed,CheckCircle2,'green'],[t('delayed'),s.delayed,Clock3,'amber'],[t('critical'),s.critical,ShieldAlert,'red']]
  return <>
    <div className="page-intro"><span className="eyebrow">{localize('Jeddah Construction Portfolio')}</span><h1>{t('overview')}</h1><p>{localize('A real-time executive view of portfolio delivery, financial exposure and project health.')}</p></div>
    <div className="kpi-grid">{cards.map(([label,value,icon,tone], index) => <KPICard key={label} label={label} value={value} icon={icon} tone={tone} index={index}/>)}</div>
    <div className="chart-grid overview-grid">
      <ChartCard title="Projects by status"><ResponsiveContainer width="100%" height={250}><PieChart><Pie data={status} dataKey="value" nameKey="name" innerRadius={68} outerRadius={94} paddingAngle={3}>{status.map(item => <Cell key={item.name} fill={chartStatusColor(item.name)}/>)}</Pie><Tooltip formatter={(value, name) => [value, localize(name)]}/></PieChart></ResponsiveContainer><div className="legend">{status.map(item => <span key={item.name}><i style={{background:chartStatusColor(item.name)}}/><b>{item.value}</b><em>{localize(item.name)}</em></span>)}</div></ChartCard>
      <ChartCard title="Project health distribution"><div className="health-pulse">{health.map(item => <div className="health-row" key={item.name}><span>{localize(item.name)}</span><div className="health-track"><i className={`health-${item.name.toLowerCase().replaceAll(' ','-')}`} style={{width:`${item.value / maxHealth * 100}%`,background:healthColor[item.name]}}/></div><b>{item.value}</b></div>)}</div></ChartCard>
      <ChartCard title="Projects by sector" className="wide"><RankedBars items={sector} valueFormatter={projectCount}/></ChartCard>
      <ChartCard title="Completion distribution"><div className="axis-safe-chart"><ResponsiveContainer width="100%" height={220}><BarChart data={completionBuckets(projects)} margin={{top:14,right:18,bottom:0,left:18}}><XAxis dataKey="name" tickMargin={10}/><YAxis allowDecimals={false} width={42} tickMargin={10}/><Tooltip/><Bar dataKey="value" fill="#6ec2d6" radius={[5,5,0,0]}/></BarChart></ResponsiveContainer></div></ChartCard>
      <ChartCard title="Budget by sector"><RankedBars items={group(projects, 'Sector', 'Approved_Budget')} valueFormatter={currency} color="#376fa8"/></ChartCard>
    </div>
    <ChartCard title="Top projects requiring attention"><ProjectTable projects={attention} onProject={onProject}/></ChartCard>
  </>
}
