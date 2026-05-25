# AIHubMix Gemini 生图配置说明

## 1. 用 AIHubMix 替代官方 Gemini 配额

- 生图由 **nano-banana-pro** skill 完成，内部调用 `generate_image.py`，原先只支持 `GEMINI_API_KEY`（官方）或 `openclaw.json` 里 `skills.entries["nano-banana-pro"].apiKey`。
- [AIHubMix Gemini 指南](https://docs.aihubmix.com/cn/api/Gemini-Guides) 支持同一套 Gemini 能力（含 Gemini 3 Pro Image Preview），需使用：
  - **base_url**: `https://aihubmix.com/gemini`
  - **api_key**: 你在 AIHubMix 的密钥（形如 `sk-***`）

## 2. 已做修改

- **脚本**：`openclaw` 自带的 `nano-banana-pro` 脚本已打补丁：当 `apiKey` 以 `sk-` 开头时，自动使用 `https://aihubmix.com/gemini` 作为 base_url，无需改环境变量或脚本参数。
- **配置**：你只需在 `~/.openclaw/openclaw.json` 里，把生图用的 key 改成 AIHubMix 的 key。

## 3. 你需要做的

在 `~/.openclaw/openclaw.json` 的 `skills.entries["nano-banana-pro"]` 中，将 `apiKey` 设为你在 AIHubMix 的 API Key（与你在 Cursor/OpenClaw 里用的 aihubmix 密钥一致即可，格式通常为 `sk-***`）：

```json
"skills": {
  "entries": {
    "nano-banana-pro": {
      "apiKey": "sk-你的AIHubMix密钥"
    }
  }
}
```

保存后重启网关（如 `systemctl --user restart openclaw-gateway`），再在飞书里向爪爪提生图需求即可走 AIHubMix 配额。

## 4. 注意

- `npm update openclaw` 或重装 openclaw 后，上述脚本补丁可能被覆盖，若生图再次报「配额用完」，需重新打补丁或等 openclaw 官方支持 AIHubMix base_url 配置。
- AIHubMix 计费与配额以他们文档为准：<https://docs.aihubmix.com/cn>.
