# 黑龙江省交易集团数智化大屏

参照设计图制作的静态数据大屏，包含人才服务、招标采购、产权交易、中国地图热力分布和分中心数据面板。

## 打开页面

下载或克隆仓库后，使用浏览器直接打开 `index.html`。CSS、JavaScript 和 SVG 均已内嵌，无需安装依赖或连接网络。

也可以在仓库目录运行：

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

然后在本机浏览器打开 `http://127.0.0.1:8080`。这只是本地预览，不会将网站部署到公网。

页面按窗口大小保持超宽大屏比例，建议使用桌面浏览器。支持市场开拓/财务指标切换、数据悬停提示、全屏和北京时间时钟。业务指标和天气均为演示数据。

## 修改与重新生成

`index.html` 是可独立使用的最终页面；修改以下源文件后，可用 Python 3 重新生成：

```sh
python3 build_dashboard.py
```

- `build_dashboard.py`：页面布局、左侧面板、样式及交互逻辑。
- `right-panels.html`、`right-panels.css`：右侧数据面板。
- `china-map.svg`：内嵌中国省级地图和热力效果。

生成脚本仅使用 Python 标准库。当前交付是原生 HTML/CSS/JavaScript 静态页面，没有 Vue 构建依赖。

## 浏览器验证

```sh
python3 verify_dashboard.py
```

验证脚本需要 Python Playwright 包和 `/usr/bin/chromium`；当前云环境已提供。截图写入 `/workspace/dashboard-wide.png` 和 `/workspace/dashboard-preview.png`，在其他机器执行前应按本机路径调整。

检查覆盖十个数据面板、内嵌地图、页签切换、悬停提示、多个窗口尺寸，以及浏览器运行错误和外部网络请求。

## 地图来源

省级边界坐标来源：[longwosion/geojson-map-china](https://github.com/longwosion/geojson-map-china)。页面通过内嵌 SVG 展示，不会在运行时请求该仓库。
