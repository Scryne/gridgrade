# GridGrade

US electricity prices and utility report cards for every state, utility and county, rebuilt automatically from public
U.S. Energy Information Administration (EIA) data.

- **Data:** EIA-861M (monthly sales and revenue by state) and EIA-861 (annual utility sales, reliability and service
  territory), downloaded without an API key.
- **Grades:** each utility is scored against all US utilities on residential price and outage minutes (SAIDI, excluding
  major event days); see `templates/methodology.html` or the live methodology page.
- **Build:** Python + Jinja2 generate a static site; charts are server-rendered SVG. GitHub Actions rebuilds daily and
  deploys to GitHub Pages.

```bash
uv sync --group dev
uv run gridgrade hepsi      # download (cek), model (isle), generate (uret), check (kontrol)
uv run pytest -q
```

Environment: `GRIDGRADE_URL` (site base URL), `GRIDGRADE_ADSENSE` (optional ad client id).

## Deployment

- Source lives in the private `Scryne/gridgrade`; the generated HTML is pushed to the public `Scryne/gridgrade-site`
  (GitHub Pages, live at https://scryne.github.io/gridgrade-site/) with a deploy key (`SITE_DEPLOY_KEY` secret).
- `.github/workflows/yayin.yml` rebuilds on every push to `main` and daily at 14:17 UTC (GitHub may start scheduled runs
  a few hours late). An unchanged build pushes nothing; a changed one pings IndexNow (`gridgrade bildir`).
- Repository variables: `SITE_URL` (switch to a custom domain once a CNAME is set up) and `ADSENSE_CLIENT` (ads are
  rendered only when it is set). Steps for the domain, Search Console and AdSense: `docs/alan-adi-ve-reklam.md`.

Data are U.S. government works (public domain); source attribution: U.S. Energy Information Administration.
GridGrade is independent and not affiliated with EIA or any utility.
