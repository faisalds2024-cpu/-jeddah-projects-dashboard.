import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { AnimatePresence, motion } from 'framer-motion'
import { LayoutDashboard, CalendarRange, WalletCards, Building2, Map, Search, Bell, Maximize, Presentation, Moon, Sun, Menu, X, CheckCheck, AlertTriangle, Clock3, ChevronLeft, ChevronRight } from 'lucide-react'
import { useDashboard } from './hooks/useDashboard'
import { FilterBar, ProjectDrawer, SearchModal } from './components/UI'
import { localize } from './i18n/labels'
import Overview from './pages/Overview'
import Schedule from './pages/Schedule'
import Budget from './pages/Budget'
import Contractors from './pages/Contractors'
import ProjectMap from './pages/Map'
import Alerts from './pages/Alerts'
import AlertDetails from './pages/AlertDetails'

const nav = [['overview',LayoutDashboard],['schedule',CalendarRange],['budget',WalletCards],['contractors',Building2],['map',Map]]

function Intro() {
  return <motion.div className="intro" initial={{opacity:1}} exit={{opacity:0}} transition={{delay:1.05,duration:.35}}><div className="blueprint"><i/><i/><i/></div><span>JEDDAH</span><h1>Construction Projects<br/>Control Center</h1><p>PMO portfolio intelligence</p></motion.div>
}

function NotificationMenu({ alerts, onOpen }) {
  return <motion.div className="notification-menu" initial={{opacity:0,y:-8}} animate={{opacity:1,y:0}} exit={{opacity:0,y:-8}}><button className="notification-title" onClick={onOpen}><b>{localize('Notifications')}</b><span>{alerts.length} {localize('new')}</span></button>{alerts.map(([title,copy,Icon,tone]) => <button className="notification-item" onClick={onOpen} key={title}><div className={tone}><Icon size={15}/></div><span><b>{localize(title)}</b><small>{localize(copy)}</small></span></button>)}</motion.div>
}

export default function App() {
  const { t, i18n } = useTranslation()
  const { data, projects, filters, setFilters, options, reset } = useDashboard()
  const [page, setPage] = useState('overview')
  const [drawer, setDrawer] = useState(null)
  const [search, setSearch] = useState(false)
  const [dark, setDark] = useState(localStorage.getItem('jpc-theme') === 'dark')
  const [intro, setIntro] = useState(sessionStorage.getItem('jpc-intro') !== 'seen')
  const [present, setPresent] = useState(false)
  const [mobile, setMobile] = useState(false)
  const [notifications, setNotifications] = useState(false)
  const [alertType, setAlertType] = useState('critical')

  useEffect(() => { document.documentElement.classList.toggle('dark', dark); localStorage.setItem('jpc-theme', dark ? 'dark' : 'light') }, [dark])
  useEffect(() => { document.documentElement.dir = i18n.language === 'ar' ? 'rtl' : 'ltr'; document.documentElement.lang = i18n.language }, [i18n.language])
  useEffect(() => { window.scrollTo(0, 0) }, [page])
  useEffect(() => {
    if (!notifications) return undefined
    const dismissNotifications = () => setNotifications(false)
    window.addEventListener('pointerdown', dismissNotifications)
    return () => window.removeEventListener('pointerdown', dismissNotifications)
  }, [notifications])
  useEffect(() => {
    const handleKey = event => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); setSearch(true) }
      if (event.key === 'Escape') { setSearch(false); setNotifications(false) }
      if (present && event.key === 'ArrowRight') setPage(current => nav[(nav.findIndex(item => item[0] === current) + 1) % nav.length][0])
      if (present && event.key === 'ArrowLeft') setPage(current => nav[(nav.findIndex(item => item[0] === current) - 1 + nav.length) % nav.length][0])
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [present])
  useEffect(() => {
    if (!intro) return undefined
    const timer = setTimeout(() => { setIntro(false); sessionStorage.setItem('jpc-intro', 'seen') }, 1450)
    return () => clearTimeout(timer)
  }, [intro])

  if (!data) return <div className="skeleton-screen"><div/><div/><div/></div>

  const pages = { overview:Overview, schedule:Schedule, budget:Budget, contractors:Contractors, map:ProjectMap, alerts:Alerts, 'alert-details':AlertDetails }
  const Page = pages[page]
  const current = Math.max(0, nav.findIndex(item => item[0] === page))
  const go = offset => setPage(nav[(current + offset + nav.length) % nav.length][0])
  const toggleLanguage = () => { const next = i18n.language === 'en' ? 'ar' : 'en'; i18n.changeLanguage(next); localStorage.setItem('jpc-language', next) }
  const full = () => document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen()
  const alerts = [['Critical schedule exposure',`${projects.filter(p => p.Health_Status === 'Critical').length} critical projects require review`,AlertTriangle,'critical'],['Financial watch list',`${projects.filter(p => p.Budget_Status === 'Watch' || p.Budget_Status === 'Over Budget').length} projects are above expected spend`,Clock3,'warning'],['Portfolio refresh complete','Local PMO dataset updated 03 Sep 2026',CheckCheck,'success']]
  const openAlerts = () => { setNotifications(false); setPage('alerts') }
  const openAlertDetails = type => { setAlertType(type); setPage('alert-details') }

  return <>
    <AnimatePresence>{intro && <Intro/>}</AnimatePresence>
    <div className={`app-shell ${present ? 'presentation' : ''}`}>
      <aside className={`sidebar ${mobile ? 'open' : ''}`}>
        <div className="brand"><div className="brand-mark"><i/><i/><i/></div><div><b>Jeddah Projects</b><small>Control Center</small></div><button className="mobile-x" onClick={() => setMobile(false)}><X/></button></div>
        <nav>{nav.map(([id, Icon]) => <button key={id} className={page === id ? 'active' : ''} onClick={() => { setPage(id); setMobile(false) }}><Icon size={19}/><span>{t(id)}</span>{page === id && <motion.i layoutId="active"/>}</button>)}</nav>
        <div className="sidebar-foot"><span>{t('lastUpdated')}</span><b>03 Sep 2026</b><small>{i18n.language === 'ar' ? 'تم التحديث من مصدر PMO المحلي' : 'Data refreshed from local PMO source'}</small></div>
      </aside>
      <main>
        <header className="top-header"><button className="menu-btn" onClick={() => setMobile(true)}><Menu/></button><div className="crumb"><span>{i18n.language === 'ar' ? 'إدارة المحفظة' : 'Portfolio Management'}</span><b>{page === 'alerts' ? localize('Notifications') : page === 'alert-details' ? localize('Project alerts') : t(page)}</b></div><button className="global-search" onClick={() => setSearch(true)}><Search size={17}/><span>{t('search')}</span><kbd>Ctrl K</kbd></button><div className="header-actions"><button onClick={toggleLanguage}>{i18n.language === 'en' ? 'AR' : 'EN'}</button><button onClick={() => setDark(!dark)} aria-label="theme">{dark ? <Sun size={18}/> : <Moon size={18}/>}</button><button onClick={full}><Maximize size={18}/></button><button className={present ? 'selected' : ''} onClick={() => setPresent(!present)}><Presentation size={18}/><span>{t('presentation')}</span></button><div className="notification-wrap"><button className="notification" aria-label="notifications" onClick={() => setNotifications(!notifications)}><Bell size={18}/><i/></button><AnimatePresence>{notifications && <NotificationMenu alerts={alerts} onOpen={openAlerts}/>}</AnimatePresence></div></div></header>
        <div className="content">{page !== 'alerts' && page !== 'alert-details' && <FilterBar options={options} filters={filters} setFilters={setFilters} reset={reset} compact={page === 'map'}/>}<AnimatePresence mode="wait"><motion.div className="page-transition-enter" key={page} initial={{opacity:0,y:13,scale:.992}} animate={{opacity:1,y:0,scale:1}} exit={{opacity:0,y:-7,scale:.997}} transition={{duration:.32,ease:[.2,.8,.2,1]}}><Page projects={projects} data={data} contractors={data.contractors} onProject={setDrawer} onAlertFilter={openAlertDetails} alertType={alertType} onBack={openAlerts} t={t}/></motion.div></AnimatePresence></div>
      </main>
    </div>
    {present && <div className="presentation-controls"><button onClick={() => go(-1)}><ChevronLeft/></button><button onClick={() => go(1)}><ChevronRight/></button></div>}
    <ProjectDrawer project={drawer} onClose={() => setDrawer(null)}/>
    <SearchModal open={search} onClose={() => setSearch(false)} projects={data.projects} onProject={setDrawer}/>
  </>
}
