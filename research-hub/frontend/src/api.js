async function getJson(url) {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} for ${url}`)
  return res.json()
}

export const fetchDatasets = () => getJson('/api/datasets')
export const fetchDataset = (slug) => getJson(`/api/datasets/${slug}`)
