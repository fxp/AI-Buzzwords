#!/usr/bin/env bash
# migrate-vault.sh - 把 vault 里所有 [TAG] topic 目录的内容文件
# 按 lowercase-hyphen slug 复制到 ~/Code/AI-Buzzwords/deepdive/
#
# 复制规则：
# - 排除 _tracker / CLAUDE.md / AI Buzzwords Design System / README / .DS_Store / raw 目录
# - 仅 .md 和 .html 文件
# - 保留原文件名（包括中文）
# - 不修复内部链接（archive 化，待正式发布时再做完整 4 资产工作流）
# - 已存在的目标目录跳过（不覆盖已发布的文章）
#
# 用法：bash scripts/migrate-vault.sh

set -euo pipefail

VAULT="/Users/xiaopingfeng/Library/Mobile Documents/iCloud~md~obsidian/Documents/AI Buzzwords/DeepDive"
REPO="$HOME/Code/AI-Buzzwords"
DEEPDIVE="$REPO/deepdive"

# vault topic dir → repo slug
# 已发布的（保留原 repo slug，不重新覆盖内容）：
#   neolab / claude-desktop-buddy / labor-day-2026
#   claude-code-leak / ai-military / palantir-aip / cybertonia / emotion-vectors (历史发布，保留)
#   anthropic-enterprise-ai / china-llm-enterprise-ai / china-software-vs-west (历史)
declare -a MAPPINGS=(
  "[AGENT] Agent Economy|agent-economy"
  "[AGENT] Agent基础设施战|agent-infrastructure-war"
  "[AGENT] Agent工程与进化|agent-engineering-evolution"
  "[AGENT] Claude Code 源码泄露|claude-code-leak"
  "[ECONOMY] ME&E 435|mse435"
  "[ENTERPRISE] AI企业服务战|ai-enterprise-service-war"
  "[ENTERPRISE] Palantir AIP|palantir-aip"
  "[GOV] AI Military|ai-military"
  "[GOV] AI合规危机|ai-governance-failure"
  "[GOV] AI政治经济学|ai-energy-tax"
  "[GOV] AI模型意识形态|ai-model-ideology"
  "[GOV] ToS|llm-tos"
  "[Governance] AI Governance|ai-governance-compass"
  "[INFRA] AI推理民主化|ai-inference-democratization"
  "[INFRA] Cloudflare Agents Week|cloudflare-agents-week"
  "[INFRA] Google Cloud Next 2026|google-cloud-next-2026"
  "[MODELS] AI Scientist|ai-scientist"
  "[MODELS] AI黑盒与测量危机|ai-blackbox-measurement"
  "[MODELS] 训练数据危机|training-data-crisis"
  "[NEOLAB] AndonLab|neolab"
  "[NEWJOB] RentAHuman|newjob-rentahuman"
  "[OPENAI] DeployCo|openai-deployco"
  "[POLITICAL] 硅谷的政治家们|silicon-valley-politicians"
  "[SECURITY] AI攻防双螺旋|ai-security-double-helix"
  "[SECURITY] Mythos报告|mythos"
  "[TRENDS] AI商业模式重构|seat-to-compute"
  "[TRENDS] Cybertonia|cybertonia"
  "[TRENDS] 开源包围战|open-source-encirclement"
  "[TRENDS] 能力下沉与算力集中|capability-vs-compute"
)

# [LAB] ANTHROPIC 是伞型，子 topic 拆开
declare -a LAB_ANTHROPIC=(
  "[LAB] ANTHROPIC/Anthropic公司全景|anthropic/overview"
  "[LAB] ANTHROPIC/[ANALYSIS] Buddy BLE 协议深潜|claude-desktop-buddy"
  "[LAB] ANTHROPIC/[ANALYSIS] 中国大模型企业的Anthropic时刻|anthropic-china-moment"
  "[LAB] ANTHROPIC/[EVENT] Anthropic企业AI服务公司|anthropic-enterprise-ai"
  "[LAB] ANTHROPIC/[PRD] Claude Desktop Buddy|claude-desktop-buddy"
  "[LAB] ANTHROPIC/[PRD] Claude 桌面版开发者模式|anthropic-desktop-developer-mode"
)

# [TOPIC] AI×就业 全景：5 维 × 3 列 + [全景] 主篇 = labor-day-2026
declare -a LABOR_TOPIC=(
  "[TOPIC] AI×就业/[全景] 劳动的终局，还是转型的前夜？|labor-day-2026"
  "[TOPIC] AI×就业/[L1个体·心理] 认知外包与技能萎缩|labor-day-2026/l1-cognitive-outsourcing"
  "[TOPIC] AI×就业/[L1分配·制度] 意义的失落|labor-day-2026/l1-meaning-loss"
  "[TOPIC] AI×就业/[L1结构·权力] AI焦虑与生产力悖论|labor-day-2026/l1-anxiety-paradox"
  "[TOPIC] AI×就业/[L2个体·心理] 白领技能去熟练化|labor-day-2026/l2-skill-deskilling"
  "[TOPIC] AI×就业/[L2分配·制度] AI薪酬重构|labor-day-2026/l2-pay-restructuring"
  "[TOPIC] AI×就业/[L2结构·权力] 算法老板|labor-day-2026/l2-algorithmic-boss"
  "[TOPIC] AI×就业/[L3个体·心理] 白领工作终局|labor-day-2026"
  "[TOPIC] AI×就业/[L3分配·制度] 职业路径断裂|labor-day-2026/l3-career-rupture"
  "[TOPIC] AI×就业/[L3结构·权力] 蓝领神话的破裂|labor-day-2026/l3-blue-collar-myth"
  "[TOPIC] AI×就业/[L4个体·心理] 技能再培训的虚假承诺|labor-day-2026/l4-reskilling-myth"
  "[TOPIC] AI×就业/[L4分配·制度] AI税与知识使用税|labor-day-2026/l4-ai-tax"
  "[TOPIC] AI×就业/[L4结构·权力] 超越UBI：分配制度重构|labor-day-2026/l4-beyond-ubi"
  "[TOPIC] AI×就业/[L5个体·心理] 幽灵劳工|labor-day-2026/l5-ghost-labor"
  "[TOPIC] AI×就业/[L5分配·制度] 数字主权与劳动数据权|labor-day-2026/l5-digital-sovereignty"
  "[TOPIC] AI×就业/[L5结构·权力] AI殖民主义|labor-day-2026/l5-ai-colonialism"
)

copy_topic() {
  local src_rel="$1"
  local dst_slug="$2"
  local src_dir="$VAULT/$src_rel"
  local dst_dir="$DEEPDIVE/$dst_slug"

  if [ ! -d "$src_dir" ]; then
    echo "  ⊘ skip (no source): $src_rel"
    return
  fi

  mkdir -p "$dst_dir"

  # find all .md and .html files (excluding _tracker, CLAUDE.md, raw, .DS_Store)
  local copied=0
  while IFS= read -r -d '' f; do
    local base="$(basename "$f")"
    case "$base" in
      _tracker*|CLAUDE.md|"AI Buzzwords Design System"*|README.md|.DS_Store) continue ;;
    esac
    local dst="$dst_dir/$base"
    # don't overwrite if target already exists (preserve published files)
    if [ -e "$dst" ]; then
      continue
    fi
    cp "$f" "$dst"
    copied=$((copied + 1))
  done < <(find "$src_dir" -maxdepth 4 -type f \( -iname "*.md" -o -iname "*.html" \) \
           -not -path "*/raw/*" -not -path "*/_assets/*" -print0)

  if [ "$copied" -gt 0 ]; then
    echo "  ✓ $src_rel → $dst_slug ($copied files)"
  else
    echo "  ⊙ $src_rel → $dst_slug (no new)"
  fi
}

echo "=== Migrating top-level [TAG] topics ==="
for entry in "${MAPPINGS[@]}"; do
  src="${entry%%|*}"
  slug="${entry##*|}"
  copy_topic "$src" "$slug"
done

echo
echo "=== Migrating [LAB] ANTHROPIC sub-topics ==="
for entry in "${LAB_ANTHROPIC[@]}"; do
  src="${entry%%|*}"
  slug="${entry##*|}"
  copy_topic "$src" "$slug"
done

echo
echo "=== Migrating [TOPIC] AI×就业 sub-topics ==="
for entry in "${LABOR_TOPIC[@]}"; do
  src="${entry%%|*}"
  slug="${entry##*|}"
  copy_topic "$src" "$slug"
done

echo
echo "=== Done. Summary: ==="
total=$(find "$DEEPDIVE" -type f \( -iname "*.md" -o -iname "*.html" \) | wc -l | tr -d ' ')
echo "  Total .md/.html under deepdive/: $total"
echo "  Topic dirs: $(ls -1d "$DEEPDIVE"/*/ | wc -l | tr -d ' ')"
