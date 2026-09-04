import { ArrowRight, AlertTriangle, CircleDollarSign, CalendarClock } from 'lucide-react'
import { ChartCard, Badge } from '../components/UI'
import { localize } from '../i18n/labels'
import { percent, number } from '../utils/formatters'

const alertConfig = {
  critical: {
    title: 'Critical schedule exposure',
    description: 'Projects with critical health require an immediate recovery plan and executive review.',
    icon: AlertTriangle,
    tone: 'critical',
    filter: project => project.Health_Status === 'Critical',
    issue: project => `Critical health score ${percent(project.Project_Health_Score)} with ${number(project.Delay_Days)} delay days.`,
  },
  financial: {
    title: 'Financial watch list',
    description: 'Projects where spending has exceeded the expected delivery position or approved budget.',
    icon: CircleDollarSign,
    tone: 'financial',
    filter: project => project.Budget_Status === 'Watch' || project.Budget_Status === 'Over Budget',
    issue: project => `${localize(project.Budget_Status)} with a ${percent(project.Budget_Variance)} budget variance.`,
  },
  hold: {
    title: 'Projects on hold',
    description: 'Projects awaiting approval, coordination, or resolution of a delivery blocker.',
    icon: CalendarClock,
    tone: 'hold',
    filter: project => project.Status === 'On Hold',
    issue: project => project.Notes || 'Delivery is paused pending a project decision or coordination action.',
  },
}

export default function AlertDetails({ projects, alertType = 'critical', onProject, onBack }) {
  const config = alertConfig[alertType] || alertConfig.critical
  const Icon = config.icon
  const selected = projects.filter(config.filter).sort((a, b) => b.Delay_Days - a.Delay_Days)

  return <div className="alert-detail-page">
    <button className="back-link" onClick={onBack}><ArrowRight size={16}/>{localize('Back to notifications')}</button>
    <div className="page-intro"><span className="eyebrow">{localize('Risk command center')}</span><h1>{localize(config.title)}</h1><p>{localize(config.description)}</p></div>
    <ChartCard className={`alert-summary ${config.tone}`}><Icon size={25}/><div><b>{selected.length}</b><span>{localize('Projects requiring immediate action')}</span></div><p>{localize('Review each project below, understand its issue, and open its complete details.')}</p></ChartCard>
    <ChartCard title="Project alerts"><div className="alert-project-list">{selected.map(project => <article key={project.Project_ID} className="alert-project">
      <div className="alert-project-main"><span className="eyebrow">{project.Project_ID}</span><h3>{localize(project.Project_Name)}</h3><p>{localize(project.Contractor_Name)} · {localize(project.District)}</p></div>
      <div className="alert-project-issue"><span>{localize('Reason for review')}</span><p>{localize(config.issue(project))}</p></div>
      <div className="alert-project-metrics"><span>{localize('Actual progress')}</span><b>{percent(project.Actual_Progress)}</b><Badge value={project.Health_Status}/></div>
      <button onClick={() => onProject(project)}>{localize('Open project details')}<ArrowRight size={15}/></button>
    </article>)}</div></ChartCard>
  </div>
}
