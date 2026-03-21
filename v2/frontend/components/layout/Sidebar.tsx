'use client'

import { useState } from 'react'
import Logo from '@/components/ui/Logo'
import SidebarItem from '@/components/layout/SidebarItem'

// SVG icons inline — no icon library needed
const AskIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
       strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
  </svg>
)

const RaceLabIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
       strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
  </svg>
)

const CollapseIcon = ({ collapsed }: { collapsed: boolean }) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
       strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round"
       className={`transition-transform duration-300 ${
         collapsed ? 'rotate-180' : ''
       }`}>
    <polyline points="15 18 9 12 15 6"/>
  </svg>
)

const navItems = [
  { href: '/ask', icon: <AskIcon />, label: 'Ask F1' },
  { href: '/racelab', icon: <RaceLabIcon />, label: 'Race Lab' },
]

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <aside
      className={`
        flex flex-col h-screen sticky top-0
        glass-heavy border-r border-surface-border
        transition-all duration-350 ease-apple flex-shrink-0
        ${collapsed ? 'w-16' : 'w-56'}
      `}
    >
      {/* Logo area */}
      <div className="flex items-center justify-between px-3 py-5
                      border-b border-surface-border">
        <Logo collapsed={collapsed} />
      </div>

      {/* Navigation items */}
      <nav className="flex-1 px-2 py-4 flex flex-col gap-1">
        {navItems.map((item) => (
          <SidebarItem
            key={item.href}
            href={item.href}
            icon={item.icon}
            label={item.label}
            collapsed={collapsed}
          />
        ))}
      </nav>

      {/* Bottom — collapse toggle + version */}
      <div className="px-2 py-4 border-t border-surface-border
                      flex flex-col gap-2">
        {/* F1 red easter egg — subtle version badge */}
        {!collapsed && (
          <div className="px-3 py-1">
            <span className="text-xs" style={{ color: '#FF1E00' }}>
              v2.0
            </span>
          </div>
        )}

        {/* Collapse button */}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="flex items-center gap-3 px-3 py-2.5 rounded-lg
                     text-text-tertiary hover:text-text-secondary
                     hover:bg-surface-high transition-all duration-250
                     w-full"
        >
          <span className="w-5 h-5 flex-shrink-0">
            <CollapseIcon collapsed={collapsed} />
          </span>
          {!collapsed && (
            <span className="text-sm font-medium">Collapse</span>
          )}
        </button>
      </div>
    </aside>
  )
}
