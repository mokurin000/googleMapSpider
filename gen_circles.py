import math
from decimal import Decimal, getcontext

# 设置Decimal的精度
getcontext().prec = 10

# 地球半径（单位：公里）
EARTH_RADIUS = Decimal("6371.0")


# 将角度转换为弧度
def deg_to_rad(deg):
    return Decimal(deg) * Decimal(math.pi) / Decimal("180")


# 将弧度转换为角度
def rad_to_deg(rad):
    return Decimal(rad) * Decimal("180") / Decimal(math.pi)


# 计算新经纬度
def calculate_new_lat_lon(lat, lon, distance_km, bearing_deg):
    # 将输入参数转换为 Decimal 类型
    lat = Decimal(lat)
    lon = Decimal(lon)
    distance_km = Decimal(distance_km)
    bearing_deg = Decimal(bearing_deg)

    lat_rad = deg_to_rad(lat)
    lon_rad = deg_to_rad(lon)
    bearing_rad = deg_to_rad(bearing_deg)

    new_lat_rad = Decimal(
        math.asin(
            Decimal(math.sin(lat_rad)) * Decimal(math.cos(distance_km / EARTH_RADIUS))
            + Decimal(math.cos(lat_rad))
            * Decimal(math.sin(distance_km / EARTH_RADIUS))
            * Decimal(math.cos(bearing_rad))
        )
    )
    new_lon_rad = lon_rad + Decimal(
        math.atan2(
            Decimal(math.sin(bearing_rad))
            * Decimal(math.sin(distance_km / EARTH_RADIUS))
            * Decimal(math.cos(lat_rad)),
            Decimal(math.cos(distance_km / EARTH_RADIUS))
            - Decimal(math.sin(lat_rad)) * Decimal(math.sin(new_lat_rad)),
        )
    )

    new_lat = rad_to_deg(new_lat_rad)
    new_lon = rad_to_deg(new_lon_rad)
    return new_lat, new_lon


# 生成圆的中心点
def generate_circle_centers(lat, lon, radius_km, min_radius_km, depth, max_depth):
    # 将输入参数转换为 Decimal 类型
    lat = Decimal(lat)
    lon = Decimal(lon)
    radius_km = Decimal(radius_km)
    min_radius_km = Decimal(min_radius_km)

    if radius_km < min_radius_km or depth > max_depth:
        return []

    centers = [(lat, lon)]
    small_radius_km = radius_km / 2

    # 6个小圆的中心点
    for i in range(6):
        angle_deg = i * 60
        new_lat, new_lon = calculate_new_lat_lon(lat, lon, small_radius_km, angle_deg)
        centers.append((new_lat, new_lon))

    # 递归生成更小的圆
    for i in range(1, 7):  # 从1开始，跳过中心点
        centers.extend(
            generate_circle_centers(
                centers[i][0],
                centers[i][1],
                small_radius_km,
                min_radius_km,
                depth + 1,
                max_depth,
            )
        )

    return centers


def main():
    # 初始经纬度
    initial_lat = Decimal("35.6999418")
    initial_lon = Decimal("139.7723058")

    # 最小半径（单位：公里）
    min_radius_km = Decimal("16")

    # 最大递归深度
    max_depth = 3

    # 初始半径（单位：公里）
    initial_radius_km = Decimal("8") * (2**max_depth)  # 16公里

    # 生成中心点
    circle_centers = generate_circle_centers(
        initial_lat, initial_lon, initial_radius_km, min_radius_km, 0, max_depth
    )

    print(len(circle_centers))


if __name__ == "__main__":
    main()
