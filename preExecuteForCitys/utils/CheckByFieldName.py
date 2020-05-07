# _*_ coding=utf-8 _*_

"""
根据名字判断需要执行哪些验证
"""
from preExecuteForCitys.check.CheckFuncs import checkIsNone, checkInDic, checkChar, checkId, checkDate, checkcisrea, \
    checkDateVail, checkDateVailEm

biRole = {"POOLAREA": [checkIsNone, checkInDic],
          "PSN_NO": [checkIsNone],
          "NAME": [checkIsNone, checkChar],
          "GEND": [checkIsNone, checkInDic],
          "CERT_TYPE": [checkIsNone, checkInDic],
          "CERT_NO": [checkIsNone, checkId],
          "BRDY": [checkIsNone, checkDate],
          "NATY": [checkIsNone, checkInDic],
          "NAT_REGN_CODE": [checkIsNone, checkInDic],
          "SURV_STAS": [checkIsNone, checkInDic],
          }

cbRole = {"ADMDVS": [checkIsNone, checkInDic],
          "INSU_POOLAREA": [checkIsNone, checkInDic],
          "POOLAREA": [checkIsNone, checkInDic],
          "PSN_NO": [checkIsNone],
          "CERT_TYPE": [checkIsNone, checkInDic],
          "CERT_NO": [checkIsNone, checkId],
          "NAME": [checkIsNone, checkChar],
          "PSN_CLCT_STAS": [checkIsNone, checkInDic],
          "INSU_STAS": [checkIsNone, checkInDic],
          "PSN_TYPE": [checkIsNone, checkInDic],
          "INSU_TYPE": [checkIsNone, checkInDic],
          "BEGN_YM": [checkIsNone, checkDateVail],
          "EXPI_YM": [checkDateVailEm],
          "EMP_NO": [checkIsNone],
          "EMP_NAME": [checkIsNone],
          "CIS_REA": [checkcisrea]
          }
