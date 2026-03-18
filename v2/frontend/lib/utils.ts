import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

/** Merge Tailwind classes cleanly without conflicts. */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/** Format lap time from seconds → MM:SS.mmm */
export function formatLapTime(seconds: number): string {
  if (!seconds || isNaN(seconds)) return '--:--.---'
  const mins = Math.floor(seconds / 60)
  const secs = (seconds % 60).toFixed(3).padStart(6, '0')
  return `${mins}:${secs}`
}

/** Format gap to leader, e.g. "+1.234s" */
export function formatGap(seconds: number): string {
  if (!seconds || isNaN(seconds)) return '--'
  if (seconds < 60) return `+${seconds.toFixed(3)}s`
  return `+${formatLapTime(seconds)}`
}

/** Map tyre compound name → hex colour. */
export function getTyreColor(compound: string): string {
  const colors: Record<string, string> = {
    SOFT:         '#E8394D',
    MEDIUM:       '#FFD60A',
    HARD:         '#F2F2F7',
    INTERMEDIATE: '#30D158',
    WET:          '#0A84FF',
  }
  return colors[compound?.toUpperCase()] ?? '#AEAEB2'
}

/** Map FastF1 team name → hex colour. */
export function getTeamColor(team: string): string {
  const colors: Record<string, string> = {
    'Red Bull Racing': '#3671C6',
    'Mercedes':        '#27F4D2',
    'Ferrari':         '#E8002D',
    'McLaren':         '#FF8000',
    'Aston Martin':    '#229971',
    'Alpine':          '#FF87BC',
    'Williams':        '#64C4FF',
    'AlphaTauri':      '#6692FF',
    'RB':              '#6692FF',
    'Alfa Romeo':      '#C92D4B',
    'Haas F1 Team':    '#B6BABD',
    'Sauber':          '#52E252',
  }
  return colors[team] ?? '#AEAEB2'
}
