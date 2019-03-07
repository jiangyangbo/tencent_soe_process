# -*- coding: utf-8 -*-
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入对应产品模块的client models。

from tencentcloud.soe.v20180724 import soe_client, models

from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

# Id 和　key ,需要注册腾讯帐号，开通智聆业务，才可以使用,此处的不可用
secretId = "AKIDEQKxx0Y4TbnH0YsxMa0GJG1iLxCT"
secretKey = "EbopcAxx0ECESSDzExSmrNVMFCIe"

def init_oral_process(text, sessionId): #  语音段唯一标识，一个完整语音一个SessionId。
    try:
	    # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey
	    cred = credential.Credential(secretId, secretKey)

	    # 实例化一个http选项，可选的，没有特殊需求可以跳过。
	    httpProfile = HttpProfile()
	    httpProfile.reqMethod = "POST"  # post请求(默认为post请求)
	    httpProfile.reqTimeout = 30  # 请求超时时间，单位为秒(默认60秒)
	    httpProfile.endpoint = "soe.tencentcloudapi.com"  # 指定接入地域域名(默认就近接入)

	    # 实例化一个client选项，可选的，没有特殊需求可以跳过。
	    clientProfile = ClientProfile()
	    clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法(默认为HmacSHA256)
	    clientProfile.unsignedPayload = True
	    clientProfile.httpProfile = httpProfile

	    client = soe_client.SoeClient(cred, "", clientProfile)
	    req = models.InitOralProcessRequest()
	    #req.SessionId = "stress_test_956938"
	    req.SessionId = sessionId
	    req.RefText = text  # refer 的文本
	    req.WorkMode = 1   # workMode  语音输入模式，0：流式分片，1：非流式一次性评估
	    req.EvalMode = 1   # EvalMode 评估模式，0：词模式，,1：:句子模式，2：段落模式，3：自由说模式，当为词模式
        #评估时，能够提供每个音节的评估信息，当为句子模式时，能够提供完整度和流利度信息。
	    req.ScoreCoeff = 3.5;  # ScoreCoeff 评价苛刻指数，取值为[1.0 - 4.0]范围内的浮点数，用于平滑不同年龄段的分数，1.0
        #为小年龄段，4.0为最高年龄段

	    resp = client.InitOralProcess(req)

	    # 输出json格式的字符串回包
	    print("%s" % resp.to_json_string())

    except TencentCloudSDKException as err:
	    print("%s" % err)
	    
def transmit_oral_process(sessionId, userVoiceData):  #  语音段唯一标识，一个完整语音一个SessionId。
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey
	    cred = credential.Credential(secretId, secretKey)

	    # 实例化一个http选项，可选的，没有特殊需求可以跳过。
	    httpProfile = HttpProfile()
	    httpProfile.reqMethod = "POST"  # post请求(默认为post请求)
	    httpProfile.reqTimeout = 30  # 请求超时时间，单位为秒(默认60秒)
	    httpProfile.endpoint = "soe.tencentcloudapi.com"  # 指定接入地域域名(默认就近接入)
	    
	    clientProfile = ClientProfile()
	    clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法(默认为HmacSHA256)
	    clientProfile.unsignedPayload = True
	    clientProfile.httpProfile = httpProfile

	    client = soe_client.SoeClient(cred, "", clientProfile)
	    req = models.TransmitOralProcessRequest()
	    req.SessionId = sessionId
	    req.VoiceFileType = 2  # 语音文件类型 1:raw, 2:wav, 3:mp3(三种格式目前仅支持16k采样率16bit编码单声道
	    req.SeqId = 1           # 流式数据包的序号，从1开始，当IsEnd字段为1后后续序号无意义，当
        #IsLongLifeSession不为1且为非流式模式时无意义。
	    req.VoiceEncodeType = 1  # 语音编码类型 1:pcm。
	    req.IsEnd = 1            #  是否传输完毕标志，若为0表示未完毕，若为1则传输完毕开始评估，非流式模式下无意义
	
	    req.UserVoiceData = userVoiceData  # 当前数据包数据, 流式模式下数据包大小可以按需设置，数据包大小必须 >= 4K，且必
        #须保证分片帧完整（16bit的数据必须保证音频长度为偶数），编码格式要求为BASE64。

	    # process
	    resp = client.TransmitOralProcess(req)

	    # 输出json格式的字符串回包
	    print("%s" % resp.to_json_string())

    except TencentCloudSDKException as err:
	    print("%s" % err)

def process(text, audiofile):
   import librosa
   import base64 
   
   with open(audiofile,'rb') as f: #读入二进制数据
        y = f.read()
     
   sessionId = "test_956938"
   userVoiceData = base64.b64encode(y)  # base64 编码
   userVoiceData = str(userVoiceData, encoding = "utf-8") # 把　b'' 格式　转化为 ""格式
   # init
   init_oral_process(text, sessionId)
   # transmit 
   transmit_oral_process(sessionId, userVoiceData)
   
if __name__=="__main__":
    text = "bussiness"
    audiofile = 'word_test.wav'
    process(text, audiofile)
    
