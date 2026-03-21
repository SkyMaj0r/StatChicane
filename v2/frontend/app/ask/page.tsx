export default function AskPage() {
  return (
    <div className="flex flex-col h-full p-8 animate-fade-in">
      <div className="mb-8">
        <h1 className="text-3xl font-semibold text-text-primary mb-1">
          Ask F1
        </h1>
        <p className="text-text-secondary text-base">
          Ask anything about Formula 1 history and statistics.
        </p>
      </div>
      <div className="card p-8 flex-1 flex items-center justify-center">
        <p className="text-text-tertiary text-sm">
          Chat interface coming in Phase 2
        </p>
      </div>
    </div>
  )
}
