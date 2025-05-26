from text_blind_watermark import TextBlindWatermark

# 文本加水印函数
def add_text_watermark(text, wm_text, password):
    try:
        twm = TextBlindWatermark(pwd=password.encode())
        watermarked_text = twm.add_wm_rnd(text=text, wm=wm_text.encode())
        return watermarked_text
    except Exception as e:
        return f"加水印失败: {str(e)}"

    # 文本消除水印函数


def remove_text_watermark(text, password):
    try:
        twm = TextBlindWatermark(pwd=password.encode())
        extracted_wm = twm.extract(text)
        # 这里只提取水印返回，消除文本中的水印恢复原文，若有对应api请替换
        # 如果不可逆，至少告诉水印内容
        return f"提取水印内容: {extracted_wm.decode(errors='ignore')}"
    except Exception as e:
        return f"消除水印失败: {str(e)}"

    # 文本处理总入口，根据用户选择调用