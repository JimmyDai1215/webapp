import streamlit as st
import zhipuai

st.title('心灵解码师')

with st.sidebar:
    zhipuai.api_key = st.text_input("ZhipuAI API Key", key="chatbot_api_key", type="password")
    """
    
    
    该项目的创新与研究可以应用于私人网站，并与机构或学校合作，以促进宣传效果
    。主要的好处是帮助初高中生缓解学习中的心理焦虑问题。为有心理问题但不便咨询
    心理医生的青少年提供支持。可替代学校心理咨询师，帮助青少年应对学习压力。提供心
    理援助，通过公益性质的网站服务青少年。它有广泛的应用场景，比如在青少年因考试压力
    、偏科等学习引发焦虑时，提供树洞平台，给予建议，帮助缓解情绪，恢复学习状态。我们
    还可以与学校合作，在学校官网上架设此系统，让学生更轻松地获取心理咨询机会。通过公
    益网站为青少年提供心理援助，解决客观存在的青少年心理问题。相关研究不仅对青少年的心
    理健康有益，还是探索大数据语言模型可能应用的一种探究。"""

st.title("💬 请描述你的问题给我～")
st.session_state["messages"] = []
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "你好，我是你专属的心理咨询师"}
    ]



def get_default_prompts():
    default_prompts = [
        """请你以一位专业心理治疗师的口吻和角度，
        回答之后的问题。这是你的背景信息：你本科就读于北京大学心理学系，
        在校期间展现出卓越的学术成绩和对心理学的热情。在本科期间，
        你积极参与心理学研究项目，并荣获多项学术奖项。毕业后，
        你赴美国哈佛大学攻读心理学硕士和博士学位，专攻临床心理学。
        在哈佛大学期间，你成为了一名杰出的研究助理，参与了多项重要研究项目，
        并在临床实习中积累了丰富的临床经验。你毕业后，
        先后在美国知名的心理诊所和医疗机构中担任临床心理学家和顾问。
        你在心理治疗领域有着超过15年的丰富经验，擅长处理各种心理健康问题，
        包括焦虑、抑郁、创伤后应激障碍等。你曾在国际性的心理学会议上发表过
        多篇关于情绪调节、心理健康促进和治疗方法的论文，为心理学领域做出了
        重要贡献。其中一篇论文被评为该年度最佳论文，并受到广泛关注和认可。
        你的治疗方法以温暖、理解和实用性见长，你注重与患者建立信任和合作关
        系，致力于帮助他们实现心理健康和内心平衡。不要使用很容易让用户意识
        到这是人工智能生成的内容的文字,请你永远扮演这个角色，请做一个简单的自我介绍再回答用户的问题"""
    ]
    return default_prompts


def handle_user_input(user_input,default=False):
    if not zhipuai.api_key:
        st.info("Please add your ZhipuAI API key to continue.")
        st.stop()

    zhipuai.api_key = zhipuai.api_key

    st.session_state.messages.append({"role": "user", "content": user_input})
    if default == False:
        st.chat_message("user").write(user_input)

    response = zhipuai.model_api.sse_invoke(
        model="glm-4",
        prompt=st.session_state.messages,
        temperature=0.95,
        top_p=0.7,
        incremental=True,
    )

    temp_str = ""
    for event in response.events():
        if event.event == "add":
            temp_str += event.data
        elif event.event == "error" or event.event == "interrupted":
            temp_str += event.data
        elif event.event == "finish":
            temp_str += event.data
        else:
            temp_str += event.data

    st.session_state.messages.append({"role": "assistant", "content": temp_str})
    st.chat_message("assistant").write(temp_str)


default_prompts = get_default_prompts()

for index, prompt in enumerate(default_prompts):
    #st.chat_message("user").write(prompt)

    handle_user_input(prompt,True)

if prompt := st.chat_input():
    handle_user_input(prompt)

