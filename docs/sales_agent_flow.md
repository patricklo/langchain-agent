# Sales Agent 流程图

基于 [agent/agent_sales_agent.py](../agent/agent_sales_agent.py) 梳理 Sales Agent 的组件架构、初始化流程、对话主循环，以及「带工具 / 不带工具」两种响应生成路径。

## 1. 整体架构

Sales Agent 以 `SalesGPT` 为核心控制器，串联「阶段分析」「话术生成」「知识库检索」三条链路。

```mermaid
flowchart TB
    subgraph controller [SalesGPT 控制器]
        seedAgent[seed_agent]
        determineStage[determine_conversation_stage]
        humanStep[human_step]
        step[step / _call]
    end

    subgraph chains [LLM 链路]
        stageAnalyzer[StageAnalyzerChain]
        salesConvo[SalesConversationChain]
    end

    subgraph toolsPath [工具增强路径 use_tools=True]
        customPrompt[CustomPromptTemplateForTools]
        llmChain[LLMChain]
        outputParser[SalesConvoOutputParser]
        singleAction[LLMSingleActionAgent]
        executor[AgentExecutor]
    end

    subgraph kb [知识库]
        catalog[sample_product_catalog.txt]
        splitter[CharacterTextSplitter]
        chroma[Chroma 向量库]
        retrievalQA[RetrievalQA]
        productSearch[ProductSearch Tool]
    end

    llm[ChatOpenAI gpt-4o]

    seedAgent --> determineStage
    determineStage --> stageAnalyzer
    stageAnalyzer --> llm

    humanStep --> determineStage
    determineStage --> step

    step -->|use_tools=False| salesConvo
    step -->|use_tools=True| executor

    salesConvo --> llm

    executor --> customPrompt --> llmChain --> llm
    llmChain --> outputParser
    outputParser --> singleAction
    singleAction --> executor
    executor --> productSearch
    productSearch --> retrievalQA --> chroma

    catalog --> splitter --> chroma
```

---

## 2. 初始化流程 (`SalesGPT.from_llm`)

```mermaid
flowchart TD
    start([from_llm 开始]) --> createStage[创建 StageAnalyzerChain]
    createStage --> createConvo[创建 SalesConversationChain]
    createConvo --> checkTools{use_tools?}

    checkTools -->|False| setExecutorNull[sales_agent_executor = None]
    checkTools -->|True| setupKB[setup_knowledge_base]

    setupKB --> readFile[读取 product_catalog 文本]
    readFile --> splitText[CharacterTextSplitter 分块]
    splitText --> buildChroma[Chroma.from_texts 建向量库]
    buildChroma --> buildQA[RetrievalQA 封装检索问答]
    buildQA --> getTools[get_tools 注册 ProductSearch]

    getTools --> buildPrompt[CustomPromptTemplateForTools]
    buildPrompt --> buildLLMChain[LLMChain + SALES_AGENT_TOOLS_PROMPT]
    buildLLMChain --> buildParser[SalesConvoOutputParser]
    buildParser --> buildAgent[LLMSingleActionAgent]
    buildAgent --> buildExecutor[AgentExecutor.from_agent_and_tools]

    setExecutorNull --> returnObj[返回 SalesGPT 实例]
    buildExecutor --> returnObj
    returnObj --> endInit([初始化完成])
```

关键代码入口：

- 工厂方法：`SalesGPT.from_llm`（[agent_sales_agent.py](../agent/agent_sales_agent.py) 约 420–480 行）
- 知识库：`setup_knowledge_base`（约 145–156 行）
- 工具注册：`get_tools`（约 158–172 行）

---

## 3. 对话主循环（脚本底部示例）

脚本末尾演示了一轮完整交互：

```mermaid
flowchart TD
    init([sales_agent = SalesGPT.from_llm]) --> seed[seed_agent]
    seed --> resetStage[阶段重置为 1 介绍]
    resetStage --> clearHistory[conversation_history 清空]

    clearHistory --> loopStart{继续对话?}

    loopStart -->|是| analyze[determine_conversation_stage]
    analyze --> stageLLM[StageAnalyzerChain 分析历史]
    stageLLM --> stageNum[输出阶段编号 1-7]
    stageNum --> updateStage[更新 current_conversation_stage]

    updateStage --> agentStep[step 生成销售回复]
    agentStep --> printReply[打印并写入 conversation_history]

    printReply --> waitUser[等待用户输入]
    waitUser --> humanStep[human_step 追加 User 消息]
    humanStep --> loopStart

    loopStart -->|否| endCall([对话结束])
```

对应执行序列（517–528 行）：

1. `seed_agent()` — 初始化
2. `determine_conversation_stage()` — 分析阶段
3. `step()` — AI 首轮回复
4. `human_step("好的。能否介绍一下问界M7")` — 用户输入
5. `determine_conversation_stage()` — 再次分析阶段
6. `step()` — AI 第二轮回复

---

## 4. 阶段判定流程 (`determine_conversation_stage`)

```mermaid
flowchart TD
    start([determine_conversation_stage]) --> checkHist{conversation_history 非空?}

    checkHist -->|是| joinHist["拼接历史: '\n'.join(...)"]
    checkHist -->|否| noHist[使用 '暂无历史对话']

    joinHist --> invoke[stage_analyzer_chain.invoke]
    noHist --> invoke

    invoke --> parseResult[解析 LLM 返回的阶段编号 text]
    parseResult --> lookup[conversation_stage_dict 查阶段描述]
    lookup --> update[current_conversation_stage 更新]
    update --> printStage[打印 Current Conversation Stage]
```

**7 个销售阶段**（`conversation_stage_dict`）：

| 编号 | 阶段 | 目标 |
|------|------|------|
| 1 | 介绍 | 自我介绍、说明来电原因 |
| 2 | 资格 | 确认对方是否为合适决策者 |
| 3 | 价值主张 | 说明产品独特卖点 |
| 4 | 需求分析 | 开放式提问挖掘痛点 |
| 5 | 解决方案展示 | 针对需求展示方案 |
| 6 | 异议处理 | 回应客户疑虑 |
| 7 | 结束/成交 | 提出下一步行动 |

> 工具模式 prompt 中还定义了第 8 阶段「结束对话」（客户离开、不感兴趣等），但 `conversation_stage_dict` 仅映射 1–7。

---

## 5. 单步响应生成 (`step` → `_call`)

这是核心分支：根据 `use_tools` 选择不同生成路径。

```mermaid
flowchart TD
    start([_call 开始]) --> branch{use_tools?}

    branch -->|False| convoChain[sales_conversation_utterance_chain.invoke]
    convoChain --> convoPrompt[注入: 销售身份/公司/阶段/历史]
    convoPrompt --> convoLLM[LLM 直接生成话术]
    convoLLM --> convoOut[ai_message]

    branch -->|True| executorInvoke[sales_agent_executor.invoke]
    executorInvoke --> toolPrompt[CustomPromptTemplateForTools 组装 prompt]
    toolPrompt --> addScratchpad[写入 intermediate_steps 到 agent_scratchpad]
    addScratchpad --> injectTools[注入 ProductSearch 工具描述]
    injectTools --> agentLLM[LLM 输出 JSON]

    agentLLM --> parser{SalesConvoOutputParser.parse}

    parser -->|isNeedTools=False| finish[AgentFinish]
    finish --> directReply[output 字段作为最终回复]

    parser -->|isNeedTools=True| action[AgentAction]
    action --> runTool[执行 ProductSearch]
    runTool --> retrieval[RetrievalQA 检索产品目录]
    retrieval --> observation[Observation 回传 LLM]
    observation --> agentLLM

    directReply --> convoOut
    convoOut --> formatMsg["格式化: {salesperson_name}: {message}"]
    formatMsg --> appendEND[若无则追加 END_OF_TURN]
    appendEND --> saveHist[追加到 conversation_history]
    saveHist --> endStep([返回])
```

### 工具模式 JSON 协议

LLM 必须返回以下 JSON 之一（`SalesConvoOutputParser`，约 222–237 行）：

- **不需要工具**：`{"isNeedTools": "False", "output": "..."}`
- **需要工具**：`{"isNeedTools": "True", "action": "ProductSearch", "action_input": "..."}`

`AgentExecutor` 在 `isNeedTools=True` 时循环：调用 `ProductSearch` → 将检索结果作为 `Observation` → 再次请求 LLM，直到返回 `AgentFinish`。

---

## 6. 知识库检索子流程

```mermaid
flowchart LR
    query[用户问题 / action_input] --> productSearch[ProductSearch.run]
    productSearch --> retrievalQA[RetrievalQA]
    retrievalQA --> retriever[Chroma retriever 相似检索]
    retriever --> chunks[相关文本块]
    chunks --> stuffChain[stuff chain 拼接上下文]
    stuffChain --> llmAnswer[LLM 生成答案]
    llmAnswer --> returnObs[作为 Observation 返回 Agent]
```

- Embedding 模型：`HuggingFaceEmbeddings`（`bge-large-zh-v1.5`）
- 数据源：[sample_product_catalog.txt](../agent/sample_product_catalog.txt)
- 分块参数：`chunk_size=10, chunk_overlap=0`

---

## 7. 数据流总览

```mermaid
sequenceDiagram
    participant User as 用户
    participant SG as SalesGPT
    participant SA as StageAnalyzerChain
    participant SC as SalesConversationChain
    participant AE as AgentExecutor
    participant PS as ProductSearch
    participant KB as RetrievalQA/Chroma

    User->>SG: human_step 输入
    SG->>SA: conversation_history
    SA-->>SG: 阶段编号 1-7
    alt use_tools=False
        SG->>SC: 阶段 + 历史 + 销售身份
        SC-->>SG: AI 话术
    else use_tools=True
        SG->>AE: 阶段 + 历史 + 销售身份
        loop 直到 AgentFinish
            AE->>AE: LLM 输出 JSON
            alt isNeedTools=True
                AE->>PS: action_input
                PS->>KB: 检索产品目录
                KB-->>PS: 答案
                PS-->>AE: Observation
            else isNeedTools=False
                AE-->>SG: output
            end
        end
    end
    SG-->>User: 打印销售回复
```

---

## 8. 关键类与职责

| 类/函数 | 职责 |
|---------|------|
| `StageAnalyzerChain` | 根据对话历史判断当前应处于哪个销售阶段 |
| `SalesConversationChain` | 无工具模式下生成下一句销售话术 |
| `SalesGPT` | 状态管理（历史、阶段）+ 编排各链路 |
| `CustomPromptTemplateForTools` | 动态注入工具列表与 ReAct scratchpad |
| `SalesConvoOutputParser` | 解析 JSON，区分直接回复 vs 工具调用 |
| `setup_knowledge_base` | 构建 Chroma + RetrievalQA 产品知识库 |
| `AgentExecutor` | 工具模式下驱动 LLM ↔ 工具 多轮循环 |
