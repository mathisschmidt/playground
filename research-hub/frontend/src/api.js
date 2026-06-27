async function getJson(url) {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} for ${url}`)
  return res.json()
}

export const fetchDatasets = () => getJson('/api/datasets')
export const fetchDataset = (slug) => getJson(`/api/datasets/${slug}`)

export async function uploadDataset(file) {
  const body = new FormData()
  body.append('file', file)
  const res = await fetch('/api/datasets/upload', { method: 'POST', body })
  if (!res.ok) {
    let detail = `${res.status} ${res.statusText}`
    try {
      detail = (await res.json()).detail || detail
    } catch {}
    throw new Error(detail)
  }
  return res.json()
}
