# 该程序可读取多个国家/行业标准文件，利用kimi模型能力对内容进行提炼，并将内容按照一定框架组织起来，输出到一个excel表中
from openai import OpenAI
from pathlib import Path
import util

# 文件内容分类，以map的形式分层映射
## 例如数据安全生命周期
role_data_std={
    '数据采集':['数据分类分级','数据采集安全管理','数据源鉴别与记录','数据质量管理'],
    '数据传输':['数据传输加密','网络可用性管理'],
    '数据存储':['存储媒体安全','逻辑存储安全','数据备份与恢复'],
    '数据处理':['数据脱敏','数据分析安全','数据正当使用','数据处理环境安全','数据导入导出安全'],
    '数据交换':['数据共享安全','数据发布安全','数据接口安全'],
    '数据销毁':['数据销毁处置','存储媒体销毁处置']
}

# 成熟度评估维度
role_DSMM_std=['人员能力','组织建设','技术工具','制度流程']

# 定义客户端
client=OpenAI(
    api_key = "sk-VSfZrkcMEInJG8FnLPWCxwHP1LpGZRAMHvdkB8zkR5bhZ3nE",
    base_url = "https://api.moonshot.cn/v1",
)

# 文件名称列表
file_list=["GB∕T 37988-2019 信息安全技术 数据安全能力成熟度模型.pdf"]
# 利用文件上传接口，循环上传文件
for f in file_list:
    # 获取已上传文件列表
    ai_file_list = client.files.list()
    isOnline,file_id=util.isInList(ai_file_list,f)
    # 文件未曾上传
    if not isOnline:
        # 文件上传
        file_object = client.files.create(file=Path(f), purpose="file-extract")
    else:
        # 读取文件对象
        file_object = client.files.retrieve(file_id)
    # 获取结果
    file_content = client.files.content(file_id=file_object.id).text
    for rd_key,rd_value in role_data_std.items():
        completion = client.chat.completions.create(
            model="moonshot-v1-128k",
            messages=[
                {
                    "role": "system",
                    "content": "下面你扮演一个数据安全专家，请以一个数据安全专家的角色和我对话",
                },
                {
                    "role": "system",
                    "content": file_content,
                },
                {
                    "role": "user",
                    "content": f"请根据{f}文件内容，按照{'、'.join(role_DSMM_std)}{len(role_DSMM_std)}个方面，总结数据生命周期中{rd_key}中的{rd_value}的安全风险评估指标",
                },
                {
                    "role": "assistant",
                    "name": "数据安全专家",
                    "content": "",
                    "partial": True,
                },
            ],
            temperature=0.3,
            max_tokens=65536,
        )

        print(completion.choices[0].message.content)
# TODO:EXCEL文件生成

# TODO:根据指标描述语义对EXCEL文件中相同标签进行去重

# TODO:根据去重后的数据结合特定领域进行特异化