import gradio as gr

from utils.image_util import *
from utils.watermark_for_text import add_text_watermark, remove_text_watermark

def process_text_module(mode, input_text, wm_text, password):
    if not input_text:
        return ""
    if not password:
        return "请输入密码"
    if mode == "文本加上水印":
        if not wm_text:
            return "请输入水印内容"
        return add_text_watermark(input_text, wm_text, password)
    else:  # 消除水印
        return remove_text_watermark(input_text, password)

    # 清空输入文本


def clear_text():
    return ""

def process_image_module(option, image, wm_text="", password=""):
    if image is None:
        return None

    pil_img = Image.fromarray(image)

    try:
        if option == "ASCII码图":
            ascii_result = ascii_art(pil_img)
            # ASCII码图这里返回字符串，Gradio直接显示文本比较好
            # 若在图像输出框，可提前绘制文字成图返回
            # 下面演示返回ASCII文本，配合你UI里自行调整
            return ascii_result

        elif option == "灰度图":
            gray_img = pil_img.convert("L")
            return np.array(gray_img)

        elif option == "素描图":
            sketch_np = sketch_image(pil_img)
            return sketch_np

        elif option == "添加明水印":
            watermarked_img = embed_visible_watermark(pil_img, wm_text)
            return np.array(watermarked_img)

        elif option == "消除明水印":
            # 明水印简单示范，没有去水印算法时直接返回原图
            return np.array(pil_img)

        elif option == "添加隐水印":
            if not password:
                password = "1"
            out_path = "output_hidden_embed.png"
            wm_img = embed_blind_watermark(pil_img, wm_text, pw_img=int(password), pw_wm=int(password),
                                           out_path=out_path)
            return np.array(wm_img)

        elif option == "消除隐水印":
            # 这个示范直接提取隐水印内容，不能真正去除隐水印
            if not password:
                password = "1"
            tmp_path = 'output_hidden_embed.png'
            # 如果你有隐水印解码图实现，可替换这里，否则返回原图
            return np.array(pil_img)

        elif option == "分析隐水印":
            # 简单示范，返回图片直方图
            hist = pil_img.histogram()
            # 这里直接返回原图，你可以写详细分析逻辑
            return np.array(pil_img)

        else:
            return np.array(pil_img)

    except Exception as e:
        print("图像处理异常：", str(e))
        return np.array(pil_img)


with gr.Blocks() as demo:
    gr.Markdown("# 妙染汗青")

    with gr.Tabs():
        # 文本处理模块
        with gr.Tab("文本水印"):
            mode_select = gr.Radio(["文本加上水印", "文本消除水印"], label="请选择操作类型")
            password_input = gr.Textbox(label="密码", placeholder="请输入密码", type="password")
            wm_text_input = gr.Textbox(label="水印内容", placeholder="自定义水印，消除水印时可空", visible=True)
            text_input = gr.Textbox(label="输入文本", lines=6)
            btn_clear = gr.Button("清空输入")
            text_output = gr.Textbox(label="输出文本", lines=6)
            btn_copy = gr.Button("复制输出")


            # 根据模式切换显示水印内容输入框
            def change_wm_visibility(choice):
                return gr.update(visible=(choice == "文本加上水印"))


            mode_select.change(change_wm_visibility, inputs=mode_select, outputs=wm_text_input)

            # 绑定清空按钮
            btn_clear.click(fn=clear_text, inputs=None, outputs=text_input)
            # 绑定复制按钮 (前端实现良好，略)
            btn_copy.click(fn=lambda x: x, inputs=text_output, outputs=None)

            submit_button = gr.Button("提交")
            submit_button.click(process_text_module,
                                inputs=[mode_select, text_input, wm_text_input, password_input],
                                outputs=text_output)

            # 图像处理模块
        with gr.Tab("图像水印"):
            img_option = gr.Dropdown([
                "添加明水印", "消除明水印",
                "添加隐水印", "消除隐水印", "分析隐水印"
            ], label="选择图像处理功能")
            image_input = gr.Image(label="上传图片", type="numpy")
            image_output = gr.Image(label="处理后的图片")
            image_wm_text = gr.Textbox(label="水印内容（加水印时填写）", visible=True)
            image_password = gr.Textbox(label="密码（加/消隐水印时填写）", placeholder="可不填")
            image_submit = gr.Button("提交")


            # 动态显示水印内容和密码框（仅加/消水印时显示）
            def toggle_img_inputs(choice):
                visible = choice in ["添加明水印", "添加隐水印", "消除明水印", "消除隐水印"]
                return gr.update(visible=visible), gr.update(visible=visible)


            img_option.change(toggle_img_inputs, inputs=img_option, outputs=[image_wm_text, image_password])

            image_submit.click(process_image_module,
                               inputs=[img_option, image_input, image_wm_text, image_password],
                               outputs=image_output)

        with gr.Tab("图像新风格"):
            img_option = gr.Dropdown([
                "ASCII码图",
                "灰度图",
                "素描图"
            ], label="选择图像处理功能")
            image_input = gr.Image(label="上传图片", type="numpy")
            image_output = gr.Image(label="处理后的图片")
            image_submit = gr.Button("提交")

            image_submit.click(process_image_module,
                               inputs=[img_option, image_input],
                               outputs=image_output)

demo.launch()