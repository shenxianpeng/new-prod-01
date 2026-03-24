# 设计系统 — AIDigestCN

## 产品背景

- **是什么：** 每日自动抓取顶级 AI 领袖的推文，翻译成中文，发布到 GitHub Pages 的资讯站点
- **目标读者：** 中国 AI/科技从业者（工程师、产品经理、研究者），信息密度偏高
- **所属领域：** AI 资讯、内容聚合、技术媒体
- **项目类型：** 编辑型资讯站点（Editorial News Site）

## 美学方向

- **方向：** 精致编辑风（Editorial/Refined）
- **装饰程度：** 有意克制（Intentional）——版式做所有重活，只用极少量装饰点缀
- **气质：** 像《经济学人》遇上现代中文科技出版物——有权威感、有温度、信息密度高但不拥挤
- **核心差异化：** 以"人"为主角，而非以"内容"为主角。头像 + 姓名是每张卡片的视觉焦点，推文内容在其下方展开——这与 The Batch、TLDR 等纯内容卡片完全不同

## 字体

- **展示/刊头：** Fraunces — 有机感的现代衬线体，有出版物质感，完全区别于所有 AI 产品惯用的无衬线字体
- **正文/UI：** Plus Jakarta Sans — Latin 字符可读性优秀，与中文系统字体（PingFang SC、Noto Sans CJK SC）搭配自然
- **中文回退：** PingFang SC → Hiragino Sans GB → Noto Sans CJK SC → sans-serif（系统字体，确保渲染速度）
- **数据/时间戳：** Geist Mono — tabular-nums，用于所有数字等宽场景（时间、期号、统计数据）
- **字体加载：** Google Fonts CDN
  ```
  https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,300;1,9..144,400&family=Plus+Jakarta+Sans:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap
  ```
- **字阶：**

  | 用途 | 字体 | 字号 | 字重 |
  |------|------|------|------|
  | 刊头/大标题 | Fraunces | clamp(36px, 5vw, 56px) | 700 |
  | 大标题斜体 | Fraunces Italic | clamp(24px, 3.5vw, 36px) | 300 |
  | 二级标题 | Fraunces | 22px | 600 |
  | 正文段落 | Plus Jakarta Sans | 16px | 400 · 行高 1.7 |
  | UI 标签/导航 | Plus Jakarta Sans | 14px | 500 |
  | 元数据/时间戳 | Geist Mono | 11–13px | 400 · tabular-nums |

## 配色

- **方案：** 有意克制（Restrained）——1个强调色 + 暖色中性调，颜色稀少而有分量

### 浅色模式

```css
:root {
  --bg:           #FAF9F6;  /* 暖米白，像高质量纸张 */
  --surface:      #FFFFFF;
  --surface-2:    #F5F3EF;
  --border:       #E8E5DF;
  --text:         #1C1917;  /* 近黑，带一丝暖意 */
  --text-2:       #78716C;  /* 暖灰 */
  --text-3:       #A8A29E;  /* 辅助文字 */
  --accent:       #B8730A;  /* 琥珀金 — 区别于所有 AI 产品的蓝色 */
  --accent-bg:    #FEF3E2;
  --accent-hover: #9A6009;
  --success:      #166534;  --success-bg: #DCFCE7;
  --warning:      #92400E;  --warning-bg: #FEF3C7;
  --error:        #991B1B;  --error-bg:   #FEE2E2;
  --info:         #1E40AF;  --info-bg:    #DBEAFE;
  --shadow:       0 1px 3px rgba(28,25,23,.06), 0 1px 2px rgba(28,25,23,.04);
  --shadow-hover: 0 4px 20px rgba(28,25,23,.10), 0 2px 6px rgba(28,25,23,.06);
}
```

### 深色模式

```css
[data-theme="dark"] {
  --bg:           #171410;
  --surface:      #1F1C18;
  --surface-2:    #2A2520;
  --border:       #3A3530;
  --text:         #F5F0E8;
  --text-2:       #A8A29E;
  --text-3:       #6B6560;
  --accent:       #D4880F;  /* 深色模式下略亮，保持对比度 */
  --accent-bg:    #2C1F08;
  --accent-hover: #E8970F;
}
```

**强调色选择理由：** 所有主流 AI 产品（OpenAI、Anthropic、The Batch、TLDR）均使用蓝色调。琥珀金传递"权威出版物/精选刊物"的感知，而非"科技产品"，建立即时的视觉辨识度。

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
  - `--radius-full: 9999px`（头像、药片形标签）

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
1. **头像** + **姓名**（最突出）——Who said it
2. **Twitter handle** + **时间戳**（元数据，Geist Mono）
3. **中文翻译**（主要阅读内容，Plus Jakarta Sans 16px）
4. **英文原文**（左侧 2px 边框，斜体，辅助色）——On hover / 始终展示
5. **来源链接** + **话题标签**（卡片底部）

### 字体加载策略

`display=swap` + 合理的系统字体回退栈，确保中文用户在字体加载前有可读体验。

## 决策日志

| 日期 | 决策 | 理由 |
|------|------|------|
| 2025-03-24 | 初始设计系统创建 | 由 `/design-consultation` 根据产品调研生成 |
| 2025-03-24 | 选用 Fraunces 衬线体 | 区别于所有 AI 产品的无衬线惯例，建立出版物权威感 |
| 2025-03-24 | 选用琥珀金 #B8730A 作为强调色 | 所有竞品用蓝色；琥珀金传递"精选刊物"而非"科技产品" |
| 2025-03-24 | 以人物为主角的信息架构 | EUREKA：AI digest 类站点把内容当等价卡片，但本站本质是特定人物的声音合集，"谁说的"比"说了什么"更重要 |
| 2025-03-24 | 最大宽度 720px 单列布局 | 深度阅读体验优先，避免多列分散注意力 |
