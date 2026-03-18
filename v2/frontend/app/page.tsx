export default function Home() {
  return (
    <main className="min-h-screen bg-background flex items-center justify-center p-6">
      <div className="card p-10 max-w-md w-full text-center animate-fade-in">
        <h1 className="text-4xl font-bold text-text-primary mb-2">
          Stat<span className="text-accent">Chicane</span>
        </h1>
        <p className="text-text-secondary text-base mb-8">
          F1 Intelligence Platform
        </p>
        <div className="divider mb-8" />
        <div className="flex gap-3 justify-center">
          <button className="btn-accent">Ask F1</button>
          <button className="btn-ghost">Race Lab</button>
        </div>
      </div>
    </main>
  )
}
