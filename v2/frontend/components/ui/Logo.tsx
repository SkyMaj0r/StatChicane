export default function Logo({ collapsed }: { collapsed: boolean }) {
  return (
    <div className="flex items-center gap-2 px-2">
      <div
        className="w-8 h-8 rounded-lg flex items-center justify-center
                   font-bold text-sm flex-shrink-0"
        style={{ backgroundColor: '#FF4500', color: '#DDD8C4' }}
      >
        SC
      </div>
      {!collapsed && (
        <span className="font-semibold text-lg text-text-primary
                         whitespace-nowrap overflow-hidden">
          Stat<span style={{ color: '#FF4500' }}>Chicane</span>
        </span>
      )}
    </div>
  )
}
