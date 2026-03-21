export default function RaceLabPage() {
  return (
    <div className="flex flex-col h-full p-8 animate-fade-in">
      <div className="mb-8">
        <h1 className="text-3xl font-semibold text-text-primary mb-1">
          Race Lab
        </h1>
        <p className="text-text-secondary text-base">
          Explore telemetry, tyre strategy, and session analysis.
        </p>
      </div>
      <div className="card p-8 flex-1 flex items-center justify-center">
        <p className="text-text-tertiary text-sm">
          Telemetry charts coming in Phase 3
        </p>
      </div>
    </div>
  )
}
