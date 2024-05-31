"""
Creation date: 2023/9/14
Creation Time: 11:14
DIR PATH: 
Project Name: GoogleMap
FILE NAME: browser.py
Editor: cuckoo
"""

import csv
import os
from typing import Union

import googlemaps


class WebScraper:
    def __init__(self, port=None):
        self.__port = port
        if self.__port:
            print(f"正在使用代理端口 [{self.__port}]")
            os.environ["http_proxy"] = f"socks5://127.0.0.1:{self.__port}"
            os.environ["https_proxy"] = f"socks5://127.0.0.1:{self.__port}"
        else:
            print("未使用代理端口")

        self.__language = "zh-CN"
        self.__map: googlemaps.Client = googlemaps.Client(
            key="AIzaSyDDGZHV6WOtXA3GpoFvEFEO07sZf-q3onk"
        )

    def get_session(
        self,
        search_word: str,
        wx: str = "",
        jx: str = "",
        sf_meter: Union[int, str] = "10000",
    ):
        filename = search_word.replace(" ", "_") + f"_{wx}_{jx}_{sf_meter}".replace(
            ".", "-"
        )
        # skip existing data
        if os.path.isfile(f"output/{filename}"):
            return True
        info_list = self.__start_session(search_word, wx, jx, sf_meter)
        if info_list:
            self.csv_writer(filename, info_list)
        return False

    def __start_session(self, search_word, wx, jx, sf_meter):
        args = {}
        if wx and jx:
            args["location"] = list(map(float, (jx, wx)))
        args["radius"] = int(sf_meter)
        args["language"] = self.__language

        shops = self.__map.places(
            search_word,
            **args,
        )

        if not shops or shops["status"] != "OK":
            return None

        results = []
        while True:
            origin_results = shops["results"]
            for place in origin_results:
                place_id = place["place_id"]
                place_detail = self.__map.place(
                    place_id,
                    language=self.__language,
                    fields=["name", "international_phone_number", "url"],
                )["result"]
                name = place_detail["name"]
                phone = place_detail.get("international_phone_number") or ""
                url = place_detail["url"]
                results.append((name, phone, url))

            if "next_page_token" not in shops:
                break
            next_page_token = shops["next_page_token"]
            args["page_token"] = next_page_token
            shops = self.__map.places(search_word, **args)
        return results

    @staticmethod
    def csv_writer(filename: str, data: list):
        # 创建输出文件夹，允许已存在
        os.makedirs("output", exist_ok=True)

        print(f"正在写入{filename}.csv")
        title = ["店铺名称", "联系电话", "网址"]
        with open(f"output/{filename}.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(title)
            writer.writerows(data)
        print("写入完毕")


if __name__ == "__main__":
    keyword_ = "重庆小面"
    scraper = WebScraper(port="7890")
    scraper.get_session(keyword_)
