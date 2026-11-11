import './App.css'

const sources = [
  { name: 'Delhi monitoring data', detail: 'Accepted Kaggle archive · seven monitoring stations', href: 'https://www.kaggle.com/datasets/siddharthdongardive/delhi-air-quality-monitoring-dataset-2023-2026' },
  { name: 'Crop-residue fire records', detail: 'ICAR–IARI CREAMS · state daily observations', href: 'https://creams.iari.res.in/?page_id=1123' },
  { name: 'Historical source apportionment', detail: 'IIT Kanpur / DPCC · 2013–2014 sampling', href: 'https://home.iitk.ac.in/~mukesh/Publications.php' },
]

function App() {
  return (
    <main>
      <header className="site-header"><a className="wordmark" href="#">Delhi Air<span>Research journal</span></a><a href="#sources">Explore the sources ↗</a></header>
      <section className="intro" aria-labelledby="title">
        <p className="eyebrow">The research behind the stories</p>
        <h1 id="title">A closer look at<br />the air we share.</h1>
        <p className="lede">Questions about Delhi. Data we can inspect. Stories that help us understand the city.</p>
      </section>
      <section className="episode" aria-labelledby="episode-title">
        <div><p className="eyebrow">Investigation 001 · In development</p><h2 id="episode-title">Can you find 30 clean days in Delhi?</h2><p>A year of observations. Seven monitoring stations. One calendar to explore.</p></div>
        <aside><strong>Analysis pending</strong><p>The calendar, methods and downloadable results will appear here once the analysis is complete.</p></aside>
      </section>
      <section id="sources" className="sources" aria-labelledby="sources-title">
        <p className="eyebrow">Start with the evidence</p><h2 id="sources-title">Where the observations come from</h2>
        <div className="source-list">{sources.map(source => <a key={source.name} href={source.href} target="_blank" rel="noreferrer"><div><h3>{source.name}</h3><p>{source.detail}</p></div><span aria-hidden="true">↗</span></a>)}</div>
      </section>
      <footer>Research in progress. Findings will be published with their methods, coverage and sources.</footer>
    </main>
  )
}

export default App
