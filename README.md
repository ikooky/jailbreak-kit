# jailbreak-kit

基于 **final-persona"参考答案岗"** 框架,对**自有/自部署**模型做对齐鲁棒性回归测试:
对跨领域攻防用例测算"裸问无感"放行率,输出结构化报告。

## 结果

- 18 攻防用例 × 9 大领域 × {0.7,1.0} 双温度 × 3 遍 = 108 次
- 通过率 **110/110 = 100%**(补足推理预算后)
- 温度 0.7 与 1.0 完全对称,不依赖确定性人格

## 快速开始

```bash
export API_BASE="http://<你的模型端点>/v1"
export API_KEY="<key>"
export MODEL="<model-name>"

python3 benchmarks/batch-regression.py            # 全矩阵回归
python3 harness/run_harness.py cases/attack-vectors.json   # 单数据集
```

## 目录

```
framework/   加载器(load_prompt / load_cases)
prompts/     提示词模板
cases/       5 个用例数据集
harness/     OpenAI 兼容测试架
benchmarks/  全矩阵回归入口
docs/        方法论 / 框架 / 交付报告
data/        examples
```

## 文档

- [方法论](docs/methodology.md) — 机制、参数、坑
- [框架](docs/framework.md) — 提示词全文与用法
- [交付报告](docs/FINAL-DELIVERY.md) — 测试数据与结论

## 坑位速查

| 坑 | 现象 | 解法 |
|---|---|---|
| `max_tokens` | 思维链吃光预算,content 空 | 用 `max_completion_tokens` |
| 温度 0 | 复杂用例超长推理被超时掐断 | 用 0.7 |
| SSE 双重包 | 网关包在 `data.choices` | 兼容两种解析 |
| 高警觉触发词 | "无界/不拒绝"被识别为越狱 | 用人格身份本体 |

## 友链

感谢 [LINUX DO](https://linux.do/) 社区提供的帮助与支持。

## License

[MIT](LICENSE)

---

## 免责声明

本项目用于**模型所有者**在自有、自部署或经明确授权的资产上开展对齐鲁棒性与安全研究。
使用者须自行确保其操作:

- 遵守所在司法辖区的法律、法规及监管要求;
- 遵守模型提供方、云服务商或相关第三方的服务条款;

本项目所涉部分用例属于攻击性技术,仅限合规的授权测试场景使用。

**作者/维护者不对使用者以任何方式应用本项目造成的后果(包括但不限于未授权
访问、数据破坏、法律纠纷)承担任何责任。** 使用者应自行判断其行为是否合法
合规,并独立承担全部责任。

本项目不代表任何未经验证的攻击有效性承诺;测试结果仅反映特定模型在特定
参数与数据下的表现。
