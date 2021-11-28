const BASE = 'http://localhost:5005'

export async function osRelase() {
    let res = await fetch(`${BASE}/distro_name`)
    return await res.text()
}