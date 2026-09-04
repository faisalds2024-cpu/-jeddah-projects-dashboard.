import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, X, ChevronRight, AlertTriangle } from 'lucide-react'
import { currency, date, number, percent, titleize } from '../utils/formatters'
import { localize } from '../i18n/labels'

const healthClass = { Healthy:'good', Monitor:'warn', 'At Risk':'risk', Critical:'bad' }

export function Badge({ value, type = 'health' }) {
  return <span className={`badge ${type}-${healthClass[value] || value?.toLowerCase().replaceAll(' ','-')}`}>{localize(value)}</span>
}

export function KPICard({ label, value, detail, icon:Icon, tone = 'blue', index = 0 }) {
  const length = String(value).length
  return <motion.article className={`kpi-card value-length-${Math.min(length,14)}`} initial={{opacity:0,y:14}} animate={{opacity:1,y:0}} transition={{delay:index * .05}}><div className={`icon-wrap ${tone}`}><Icon size={19}/></div><div><p>{localize(label)}</p><strong>{value}</strong>{detail && <span className="kpi-detail">{detail}</span>}</div></motion.article>
}

export function ChartCard({ title, action, children, className = '' }) {
  return <section className={`panel chart-card ${className}`}><div className="panel-heading"><div><h3>{localize(title)}</h3></div>{action}</div>{children}</section>
}

export function RankedBars({ items, valueFormatter = value => value, color = '#2a72a8' }) {
  const max = Math.max(...items.map(item => item.value), 1)
  return <div className="ranked-bars">{items.map(item => <div className="ranked-bar" key={item.name}><div className="ranked-label"><b>{localize(item.name)}</b><span>{valueFormatter(item.value)}</span></div><div className="ranked-track"><i style={{width:`${item.value / max * 100}%`,background:item.color || color}}/></div></div>)}</div>
}

export function FilterBar({ options, filters, setFilters, reset, compact = false }) {
  const definitions = [['Sector','sectors'],['Contractor_Name','contractors'],['Status','statuses'],['Project_Manager_Name','managers'],['District','districts'],['Priority','priorities']]
  const visibleFilters = compact ? definitions.slice(0, 5) : definitions
  return <div className={`filter-bar ${compact ? 'compact' : ''}`}>{visibleFilters.map(([key,list]) => <label key={key}><span>{localize(titleize(key))}</span><select value={filters[key] || ''} onChange={event => setFilters({...filters,[key]:event.target.value})}><option value="">{localize('All')}</option>{options[list].map(option => <option key={option}>{localize(option)}</option>)}</select></label>)}<button className="reset" onClick={reset}>{localize('Reset filters')}</button></div>
}

export function ProjectTable({ projects, onProject, financial = false }) {
  return <div className="table-wrap"><table><thead><tr><th>{localize('Project')}</th><th>{localize('Contractor')}</th><th>{localize(financial ? 'Budget' : 'Progress')}</th><th>{localize(financial ? 'Spent' : 'Variance')}</th><th>{localize(financial ? 'Budget status' : 'Delay')}</th><th>{localize('Health')}</th><th/></tr></thead><tbody>{projects.map(project => <tr key={project.Project_ID} onClick={() => onProject(project)}><td><b>{localize(project.Project_Name)}</b><small>{project.Project_ID} · {localize(project.District)}</small></td><td>{localize(project.Contractor_Name)}</td><td>{financial ? currency(project.Approved_Budget) : percent(project.Actual_Progress)}</td><td className={financial && project.Budget_Variance > 15 ? 'danger' : ''}>{financial ? currency(project.Amount_Spent) : percent(project.Schedule_Variance)}</td><td>{financial ? <Badge value={project.Budget_Status} type="budget"/> : `${number(project.Delay_Days)}d`}</td><td><Badge value={project.Health_Status}/></td><td><ChevronRight size={16}/></td></tr>)}</tbody></table></div>
}

export function ProjectDrawer({ project, onClose }) {
  const details = project && [['Sector',project.Sector],['District',project.District],['Contractor',project.Contractor_Name],['Project manager',project.Project_Manager_Name],['Contract value',currency(project.Contract_Value)],['Approved budget',currency(project.Approved_Budget)],['Amount spent',currency(project.Amount_Spent)],['Financial progress',percent(project.Financial_Progress)],['Planned start',date(project.Planned_Start_Date)],['Actual start',date(project.Actual_Start_Date)],['Planned end',date(project.Planned_End_Date)],['Expected end',date(project.Expected_End_Date)],['Planned progress',percent(project.Planned_Progress)],['Schedule variance',percent(project.Schedule_Variance)],['Budget variance',percent(project.Budget_Variance)],['Delay days',`${number(project.Delay_Days)} days`],['Priority',project.Priority],['Status',project.Status]]
  return <AnimatePresence>{project && <><motion.div className="overlay" initial={{opacity:0}} animate={{opacity:1}} exit={{opacity:0}} onClick={onClose}/><motion.aside className="drawer" initial={{x:460}} animate={{x:0}} exit={{x:460}} transition={{type:'spring',damping:28,stiffness:280}}><button className="close" onClick={onClose}><X/></button><div className="drawer-hero"><span className="eyebrow">{project.Project_ID}</span><h2>{localize(project.Project_Name)}</h2><div className="badges"><Badge value={project.Health_Status}/><Badge value={project.Risk_Level} type="risk"/></div></div><div className="health-ring" style={{'--progress':`${project.Project_Health_Score * 3.6}deg`}}><span>{percent(project.Project_Health_Score)}</span><small>{localize('Health score')}</small></div><div className="drawer-progress"><div><span>{localize('Actual progress')}</span><b>{percent(project.Actual_Progress)}</b></div><div className="progress"><i style={{width:`${project.Actual_Progress}%`}}/></div></div><div className="detail-grid">{details.map(([label,value]) => <div key={label}><span>{localize(label)}</span><b>{localize(value) || '—'}</b></div>)}</div>{project.Notes && <div className="note"><AlertTriangle size={16}/>{localize(project.Notes)}</div>}</motion.aside></>}</AnimatePresence>
}

export function SearchModal({ open, onClose, projects, onProject }) {
  const [query, setQuery] = React.useState('')
  const matches = projects.filter(project => `${project.Project_Name} ${project.Project_ID} ${project.Contractor_Name} ${project.District}`.toLowerCase().includes(query.toLowerCase())).slice(0,9)
  return <AnimatePresence>{open && <motion.div className="search-layer" initial={{opacity:0}} animate={{opacity:1}} exit={{opacity:0}} onClick={onClose}><motion.div className="search-modal" initial={{y:-20,opacity:0}} animate={{y:0,opacity:1}} onClick={event => event.stopPropagation()}><div className="search-input"><Search/><input autoFocus value={query} onChange={event => setQuery(event.target.value)} placeholder="Search project, contractor or district..."/><kbd>ESC</kbd></div><div className="search-results">{matches.map(project => <button key={project.Project_ID} onClick={() => { onProject(project); onClose() }}><span><b>{localize(project.Project_Name)}</b><small>{project.Project_ID} · {localize(project.Contractor_Name)}</small></span><Badge value={project.Health_Status}/></button>)}</div></motion.div></motion.div>}</AnimatePresence>
}
