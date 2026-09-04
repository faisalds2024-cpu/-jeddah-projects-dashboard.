const statusColors = {
  Completed: '#1ca98a',
  Healthy: '#1ca98a',
  'Ahead of Schedule': '#50b89a',
  'On Track': '#70b9d5',
  'In Progress': '#4f82c9',
  Monitor: '#e4a62b',
  'Slightly Delayed': '#e4a62b',
  Delayed: '#df7a43',
  'At Risk': '#e8786c',
  Critical: '#ca5650',
  'Critical Delay': '#ca5650',
  'On Hold': '#8b97a8',
  'Not Started': '#a3b1c2',
  Excellent: '#1ca98a',
  Good: '#50b89a',
  'Needs Attention': '#e4a62b',
  Poor: '#ca5650',
}

export const chartStatusColor = (status) => statusColors[status] || '#4f82c9'
