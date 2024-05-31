import argparse
from time import sleep

from browser import WebScraper
from gen_circles import generate_circle_centers


RADIUS = 16


def main():
    parser = argparse.ArgumentParser(
        prog="GoogleMapSpider",
        description="Craw Shop/Number from Google Map",
    )
    parser.add_argument("-n", "--name", required=True, type=str, help="搜索关键词")
    parser.add_argument(
        "-p", "--proxy-port", required=False, type=int, help="socks5代理端口"
    )
    parser.add_argument("--lat", required=True, help="经度", type=str, default="0")
    parser.add_argument("--lon", required=True, help="纬度", type=str, default="0")

    args = parser.parse_args()
    kw = args.name
    if not kw:
        print("搜索关键词不能为空！")
        return
    proxy_port = args.proxy_port
    center_lat = args.lat or ""
    center_lon = args.lon or ""
    map_scrapper = WebScraper(port=proxy_port)

    max_depth = 3
    split_circles = generate_circle_centers(
        center_lat,
        center_lon,
        RADIUS * (2**max_depth),
        RADIUS,
        0,
        max_depth=max_depth,
    )
    print(len(split_circles))

    for lat, lon in split_circles:
        if map_scrapper.get_session(
            # 关键词
            search_word=kw,
            # 纬度
            wx=lon,
            # 经度
            jx=lat,
            # 小圆半径
            sf_meter=1000,
        ):
            continue
        sleep(5)


if __name__ == "__main__":
    main()
