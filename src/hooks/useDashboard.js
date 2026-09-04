import { useEffect, useMemo, useState } from 'react'
import { filtersFor, getFilteredProjects, loadData } from '../data/service'
export function useDashboard() { const [data,setData]=useState(null); const [filters,setFilters]=useState({}); useEffect(()=>{loadData().then(setData)},[]); const projects=useMemo(()=>data?getFilteredProjects(data.projects,filters):[],[data,filters]); return { data, projects, filters, setFilters, options:data?filtersFor(data.projects):null, reset:()=>setFilters({}) } }
