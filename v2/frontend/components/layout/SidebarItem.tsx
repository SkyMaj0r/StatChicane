'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

interface SidebarItemProps {
  href: string
  icon: React.ReactNode
  label: string
  collapsed: boolean
}

export default function SidebarItem({
  href,
  icon,
  label,
  collapsed,
}: SidebarItemProps) {
  const pathname = usePathname()
  const isActive = pathname.startsWith(href)

  return (
    <Link
      href={href}
      className={`
        flex items-center gap-3 px-3 py-2.5 rounded-lg
        transition-all duration-250 group relative
        ${isActive
          ? 'bg-accent-muted text-accent'
          : 'text-text-secondary hover:bg-surface-high hover:text-text-primary'
        }
      `}
    >
      {/* Active indicator bar */}
      {isActive && (
        <div
          className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5
                     h-5 rounded-full"
          style={{ backgroundColor: '#FF4500' }}
        />
      )}

      {/* Icon */}
      <span className={`flex-shrink-0 w-5 h-5 ${
        isActive ? 'text-accent' : 'text-text-secondary group-hover:text-text-primary'
      }`}>
        {icon}
      </span>

      {/* Label */}
      {!collapsed && (
        <span className="text-sm font-medium whitespace-nowrap
                         overflow-hidden">
          {label}
        </span>
      )}

      {/* Tooltip when collapsed */}
      {collapsed && (
        <div className="
          absolute left-full ml-3 px-2.5 py-1.5 rounded-md
          bg-surface-high text-text-primary text-sm font-medium
          opacity-0 group-hover:opacity-100 pointer-events-none
          transition-opacity duration-200 whitespace-nowrap z-50
          border border-surface-border
        ">
          {label}
        </div>
      )}
    </Link>
  )
}
