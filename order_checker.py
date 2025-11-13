import requests
from dotenv import load_dotenv
import os
import httpx


# ============ 1. Настройки ============
load_dotenv()
SITE_API_URL = "https://seller.ozon.ru/api/site/fbo-posting-service/posting/list"  # URL для парсинга заказов
API_URL = "https://api-seller.ozon.ru/v2/posting/fbo/get"
OUTPUT_FILE = "ozon_clusters.xlsx"

def data_from_site(posting_number):
    """
    Получает данные о времени доставки через неофициальное API
    """

    client = httpx.Client()
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ru",
        "Content-Type": "application/json",
        "Cookie": "__Secure-ext_xcid=27faf522100f77d2b130d016cfc1b9a7; __Secure-ab-group=38; __Secure-ETC=bc0825e8423099a1cb9076432fb3f7f1; ADDRESSBOOKBAR_WEB_CLARIFICATION=1762859777; __Secure-user-id=142345068; bacntid=6248116; sc_company_id=290929; x-o3-language=ru; abt_data=7.m1MvWyNUHGd8Y96nZKoBJVJ7-GOTXw8nZqFDLhssPNnDHSFm0fb3qJInkCG1fNafBVVPhbI3XdC45DZ3UrUSSOzDQG6GElxIcRXtJ4J2ri3obeB3JPjNl2sBq7Pw1rj_Rpq-tsh5H7foB0F4wOpxDupAov-JJUtyNyOZEarUSbAnP1aNza7ZriOcWbFuQQ1U-6qAUuSH2_FPERRBJlNpVUkBYdHkeptSSsTLzIdzxGjfFP-jXI2EZjVa-7Zx68OY6dBl4I_Spr1qb0Y62d7To56TD11nFAHNGOloao7dc8uyLyrba9kkHXpKfhBsW5K4Ty7ZqiC1xvT5cHv7olJlnIpcB0MDnlamrIkqFiHHqZZSgDEwIlepPRQhGddDh6wXEogCWRv4V0Ejuunqnxn3mSq0MK0OV5-0shcCWPocNXNNr4gOGlyoKMsyTufJJ4JPkETNWs8pGVEUq3kYRRnDjhVAis1DzeV7lyN0RGDzVwmZMaaH97Tt1xBzxtxEunEuyGatOJ8U9ktPbqhsAXUR5amTEq1HDTmuCEhVkCi2OLD4SZ9KKgnNdvj00Kh5EVwZ74ud39N3FMNOob6xKC_14mCzNm_6DrVhvYnP0TE0OJNrPRlAumzwJfm1T3b2f5FevFyjXso1NDpST1I; __Secure-refresh-token=9.142345068.VbGj-Qd2SeOQJIO8YLXtXA.38.AUCdFbPi2a1F3PmVoH7kI3arqE4n5PnS4DY4PD3U62nP7LmLvIEzORk9i0t0D8xsCDvqbpXQyo5-G1iOt8dcOk8BAuIe_GAWTXXTjay3ZFt3DAAs6VfHw9P0Sx1lmV6fOA.20230917093549.20251112113145.LHWp50chgOz1rz8e6j4jB2vRt98SOSuusKF58izRpaM.1fb9d0a13a6ef9250; __Secure-access-token=9.142345068.VbGj-Qd2SeOQJIO8YLXtXA.38.AUCdFbPi2a1F3PmVoH7kI3arqE4n5PnS4DY4PD3U62nP7LmLvIEzORk9i0t0D8xsCDvqbpXQyo5-G1iOt8dcOk8BAuIe_GAWTXXTjay3ZFt3DAAs6VfHw9P0Sx1lmV6fOA.20230917093549.20251112113145.rmT1OgACAx9Epy7cPuKgrwhbIdUrGU2oSGJa5vsAJrI.12e51e3635b58e9fd",
        "Origin": "https://seller.ozon.ru",
        "Priority": "u=1, i",
        "Referer": "https://seller.ozon.ru/app/postings/fbo?statusAlias=all&processedAtFrom=2025-11-10T20%3A00%3A00.000Z&processedAtTo=2025-11-11T19%3A59%3A59.999Z",
        "Sec-Ch-Ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "X-O3-App-Name": "seller-ui",
        "x-O3-Company-Id": "290929",
        "x-O3-Language": "ru",
        "x-O3-Page-Type": "PostingsFbo",
    }
    json_payload = {
        "filter": {"company_id": "290929", "posting_number": [posting_number]},
        "limit": "30",
        "sort_dir": "desc",
    }
    response = client.post(
        url=SITE_API_URL, headers=headers, json=json_payload, follow_redirects=True
    )
    data = response.json()
    result = data.get("result")
    posting = result.get("postings")[0]
    return {"estimated_delivery_time_hours": posting.get("estimated_delivery_time_hours"),}
def api_data(posting_number):
    """
    Получает данные о номере заказаб городе получателя, id склада, названии, кластере отправления и кластере получения
    """
    headers = {
        "Host": "api-seller.ozon.ru",
        "Client-Id": os.environ.get("CLIENT_ID"),
        "Api-Key": os.environ.get("API_KEY"),
        "Content-Type": "application/json",
    }
    json_payload = {
        "posting_number": posting_number,
        "translit": True,
        "with": {
            "analytics_data": True,
            "financial_data": True,
        },
    }
    response = requests.post(url=API_URL, headers=headers, json=json_payload)
    data = response.json()
    result = data.get("result", {})
    analytics = result.get("analytics_data", {})
    finances = result.get("financial_data", {})
    return    {
            "posting_number": posting_number,
            "order_id": result.get("order_id"),
            "city": analytics.get("city"),
            "warehouse_id": analytics.get("warehouse_id"),
            "warehouse_name": analytics.get("warehouse_name"),
            "cluster_from": finances.get("cluster_from"),
            "cluster_to": finances.get("cluster_to"),
        }

def main():
    posting_number = input()
    print(api_data(posting_number) | data_from_site(posting_number))

if __name__ == "__main__":
    main()