export function removeBaseUrl(text) {
  return text.replace(/https:\/\/raw\.githubusercontent\.com\/\S*\/\S*\/[a-z0-9]{40}\//g, '')
}
