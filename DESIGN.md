# 设计系统 — AIDigestCN

## 产品背景

- **是什么：** 每日自动抓取顶级 AI 领袖的推文，翻译成中文，发布到 GitHub Pages 的资讯站点
- **目标读者：** 中国 AI/科技从业者（工程师、产品经理、研究者），信息密度偏高
- **所属领域：** AI 资讯、内容聚合、专业媒体
- **项目类型：** 编辑型资讯站点（Editorial News Site）

## 美学方向

- **方向：** 专业编辑 / 财经媒体感（Professional Editorial）
- **装饰程度：** 克制（Intentional）——版式做所有重活，只用极少量装饰点缀
- **气质：** Financial Times 遇上中文科技出版物——权威、克制、有分量。信息密度高但不压迫，白天阅读舒适
- **核心差异化：** 以"人"为主角，而非以"内容"为主角。头像 + 姓名是每张卡片的视觉焦点，推文内容在其下方展开——这与 The Batch、TLDR 等纯内容卡片完全不同

## 字体

- **展示/刊头：** Clash Grotesk 700 — 几何感粗体 grotesque，现代力量感，与衬线类编辑体完全不同，行业里没有 AI 资讯站用几何粗体做刊头
- **正文/UI：** Source Sans 3 400/500/600 — 拉丁字符可读性极佳，与中文系统字体（PingFang SC、Noto Sans CJK SC）搭配自然
- **中文回退：** PingFang SC → Hiragino Sans GB → Noto Sans CJK SC → sans-serif
- **数据/时间戳：** Geist Mono — tabular-nums，用于所有数字等宽场景（时间、期号、统计数据）
- **字体加载：**
  ```
  https://api.fontshare.com/v2/css?f[]=clash-grotesk@700,600,500,400&display=swap
  https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,300;0,400;0,500;0,600;1,400&family=Geist+Mono:wght@400;500&display=swap
  ```
- **字阶：**

  | 用途 | 字体 | 字号 | 字重 |
  |------|------|------|------|
  | 刊头/大标题 | Clash Grotesk | clamp(32px, 5vw, 48px) | 700 |
  | 二级标题 | Clash Grotesk | 24–28px | 600 |
  | 姓名/卡片标题 | Clash Grotesk | 15px | 600 |
  | 正文段落 | Source Sans 3 | 16px | 400 · 行高 1.75 |
  | UI 标签/按钮 | Source Sans 3 | 14px | 600 |
  | 元数据/时间戳 | Geist Mono | 11–13px | 400 · tabular-nums |

## 配色

- **方案：** 克制（Restrained）——1 个强调色 + 冷色中性调，颜色稀少而有分量

### 浅色模式

```css
:root {
  --bg:           #FFFFFF;
  --bg-2:         #F8F9FA;  /* 页面浅层 */
  --surface:      #FFFFFF;
  --surface-2:    #F3F4F6;
  --border:       #E5E7EB;
  --border-2:     #D1D5DB;
  --text:         #111827;  /* 冷炭黑，比暖黑更现代 */
  --text-2:       #6B7280;  /* 钢灰 */
  --text-3:       #9CA3AF;  /* 辅助文字 */
  --accent:       #15803D;  /* 森林绿 — 行业唯一，区别于所有 AI 产品蓝色 */
  --accent-hover: #166534;
  --accent-bg:    #DCFCE7;
  --accent-light: #F0FDF4;
  --shadow-sm:    0 1px 3px rgba(17,24,39,.06), 0 1px 2px rgba(17,24,39,.04);
  --shadow-md:    0 4px 20px rgba(17,24,39,.09), 0 2px 6px rgba(17,24,39,.05);
  --shadow-hover: 0 8px 30px rgba(17,24,39,.12), 0 3px 8px rgba(17,24,39,.07);
}
```

### 深色模式

```css
[data-theme="dark"] {
  --bg:           #0A0F0D;  /* 带微绿的近黑，与 generic 深灰不同 */
  --bg-2:         #111810;
  --surface:      #141A12;
  --surface-2:    #1C2419;
  --border:       #2A3325;
  --border-2:     #3A4A33;
  --text:         #D1FAE5;
  --text-2:       #86EFAC;
  --text-3:       #4ADE80;
  --accent:       #22C55E;  /* 深色模式略亮，保持对比度 */
  --accent-hover: #16A34A;
  --accent-bg:    #14532D;
  --accent-light: #052E16;
}
```

**强调色选择理由：** 全球 AI 资讯产品（OpenAI、Anthropic、The Batch、TLDR、量子位、机器之心）均使用蓝色调。森林绿传递"权威出版物/专业媒体"的感知，而非"科技产品"，建立即时的视觉辨识度。深色模式的微绿底色 #0A0F0D 也与系统默认深灰完全不同。

## 间距

- **基础单位：** 8px
- **密度：** 舒适（comfortable）——面向从业者，不是大众媒体
- **间距阶梯：**

  | Token | 值 |
  |-------|-----|
  | 2xs | 2px |
  | xs  | 4px |
  | sm  | 8px |
  | md  | 16px |
  | lg  | 24px |
  | xl  | 32px |
  | 2xl | 48px |
  | 3xl | 64px |

## 布局

- **方案：** 以内容为中心的单列流（Content-centered single column）
- **最大内容宽度：** 720px（深度阅读体验，不分散注意力）
- **断点：** 移动优先，≥640px 展示完整导航
- **圆角层级：**
  - `--radius-sm: 4px`（标签、徽章、小按钮）
  - `--radius-md: 8px`（按钮、输入框、小卡片）
  - `--radius-lg: 12px`（主卡片、模块容器）
  - `--radius-full: 9999px`（头像、人物芯片、药片形标签）

## 动效

- **方案：** 有意最小化（Intentional-minimal）——只有辅助理解的过渡，不干扰阅读
- **缓动函数：** 进入 ease-out · 退出 ease-in · 位移 ease-in-out
- **时长：**
  - micro: 50–100ms（状态切换）
  - short: 150–250ms（卡片悬停、按钮）
  - medium: 250–400ms（主题切换）
  - long: 400–700ms（页面过渡）
- **典型用法：** 卡片悬停轻微提升（translateY -1px + shadow 加深）；内容加载淡入；主题切换 background/color 平滑过渡

## 组件规范

### 人物卡片（核心组件）

信息层级：
1. **头像** + **姓名**（最突出）—— Who said it
2. **Twitter handle** + **时间戳**（元数据，Geist Mono）
3. **中文翻译**（主要阅读内容，Source Sans 3 16px）
4. **英文原文**（左侧 2px 边框，斜体，辅助色）
5. **来源链接** + **话题标签**（卡片底部）

### 字体加载策略

`display=swap` + 合理的系统字体回退栈，确保中文用户在字体加载前有可读体验。

## 决策日志

| 日期 | 决策 | 理由 |
|------|------|------|
| 2026-03-26 | 全新设计系统（替换旧版琥珀金方案） | 用户要求完全重做，方向改为专业媒体感 |
| 2026-03-26 | 选用 Clash Grotesk 几何粗体 | 区别于旧版 Fraunces 衬线，更有力量感；行业内无 AI 资讯站用几何粗体做刊头 |
| 2026-03-26 | 选用森林绿 #15803D 作为强调色 | 全球 AI 资讯竞品清一色蓝色；绿色传递"专业出版物"而非"科技产品"，建立即时辨识度 |
| 2026-03-26 | 深色模式用微绿近黑 #0A0F0D | 与 generic 深灰完全不同，延续绿色品牌调性到深色模式 |
| 2026-03-26 | 以人物为主角的信息架构 | EUREKA：AI digest 类站点把内容当等价卡片，但本站本质是特定人物的声音合集，"谁说的"比"说了什么"更重要 |
| 2026-03-26 | 最大宽度 720px 单列布局 | 深度阅读体验优先，避免多列分散注意力 |
