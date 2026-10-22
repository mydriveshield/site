# MyDriveShield site

Source for https://mydriveshield.com.au (static HTML, hosted on Netlify project `driveshield-au`) and the code that lives inside the n8n workflows.

## Layout
- `index.html`, `partners.html`, `confirmation.html`, images, `docs/` are the site as deployed. Publish directory is the repo root (see `netlify.toml`).
- `n8n/` holds exports of the n8n workflows on layden.app.n8n.cloud. n8n is the runtime; these files are the versioned record. When a node is edited in n8n, export the workflow again and commit it in the same change.

## Deploy
Netlify builds from the `main` branch on every push. There is no build step; the files are served as they are. To roll back, re-deploy an earlier commit from the Netlify deploys list.

## Conventions
- Commit messages carry the date and what changed, e.g. `22/10/2026: PDS acceptance tick box`.
- Record every shipped change as a dated note in the Claude project as well.
