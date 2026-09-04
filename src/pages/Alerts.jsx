import { AlertTriangle, CircleDollarSign, CalendarClock, ArrowRight } from 'lucide-react'
import { ChartCard, ProjectTable } from '../components/UI'
import { localize } from '../i18n/labels'

export default function Alerts({ projects, onProject, onAlertFilter }) {
  const critical = projects.filter(project => project.Health_Status === 'Critical').sort((a, b) => b.Delay_Days - a.Delay_Days)
  const financial = projects.filter(project => project.Budget_Status === 'Watch' || project.Budget_Status === 'Over Budget').sort((a, b) => b.Budget_Variance - a.Budget_Variance)
  const held = projects.filter(project => project.Status === 'On Hold')
  const cards = [
    ['critical','Critical schedule exposure',AlertTriangle,'#ca5650',critical.length,'Critical projects','High delays or declining project health require a clear recovery plan.','Open critical projects'],
    ['financial','Financial watch list',CircleDollarSign,'#df7a43',financial.length,'Financial risks','Spending is ahead of physical progress or exceeds the approved budget.','Open financial risks'],
    ['hold','Projects on hold',CalendarClock,'#e4a62b',held.length,'Projects on hold','Projects are awaiting approval, coordination, or resolution of a delivery blocker.','Open projects on hold'],
  ]
  return <div className="alert-page">
    <div className="page-intro"><span className="eyebrow">{localize('Risk command center')}</span><h1>{localize('Notifications')}</h1><p>{localize('Decisions and risks requiring immediate follow-up across the project portfolio.')}</p></div>
    <div className="alert-grid">{cards.map(([type,title,Icon,color,count,label,description,action]) => <ChartCard className="alert-card" title={title} key={type}><Icon color={color}/><h3>{count} {localize(label)}</h3><p>{localize(description)}</p><button onClick={() => onAlertFilter(type)}>{localize(action)} <ArrowRight size={14}/></button></ChartCard>)}</div>
    <ChartCard title="Critical schedule exposure"><ProjectTable projects={critical.slice(0,12)} onProject={onProject}/></ChartCard>
  </div>
}
