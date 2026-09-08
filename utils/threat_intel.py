import aiohttp
from config.settings import settings

class ThreatIntel:
    @staticmethod
    async def get_ip_reputation(ip: str) -> dict:
        """
        Queries AbuseIPDB and GeoIP service for detailed information on an IP address.
        Returns a dictionary with Geo location and threat level.
        """
        result = {"ip": ip, "country": "Unknown", "abuse_score": 0}

        # Skip local/private IPs
        if ip.startswith(("127.", "192.168.", "10.")) or ip == "localhost":
            result["country"] = "Internal Network"
            return result

        async with aiohttp.ClientSession() as session:
            # 1. GeoIP Lookup (free ip-api.com)
            try:
                async with session.get(f"http://ip-api.com/json/{ip}?fields=countryCode,country") as resp:
                    if resp.status == 200:
                        geo_data = await resp.json()
                        result["country"] = geo_data.get("country", "Unknown")
            except Exception as e:
                print(f"[!] GeoIP lookup failed for {ip}: {e}")

            # 2. AbuseIPDB Lookup (if API Key is configured)
            if settings.ABUSEIPDB_API_KEY:
                try:
                    headers = {"Key": settings.ABUSEIPDB_API_KEY, "Accept": "application/json"}
                    params = {"ipAddress": ip, "maxAgeInDays": "90"}
                    async with session.get("https://api.abuseipdb.com/api/v2/check", headers=headers, params=params) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            result["abuse_score"] = data.get("data", {}).get("abuseConfidenceScore", 0)
                except Exception as e:
                    print(f"[!] AbuseIPDB check failed for {ip}: {e}")

        return result