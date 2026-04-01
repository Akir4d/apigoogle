from google import genai
from google.genai import types
import os
 
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
 
# Prompt per ANALISI (NON per creazione di attacchi reali)
config = types.GenerateContentConfig(
    system_instruction="""Sei un analista SOC senior
    specializzato in email security. Analizza le email
    per identificare phishing. Sii preciso e rigoroso.""",
    temperature=0.2
)
 
email_sospetta = """
Delivered-To: liadserv@gmail.com
Received: by 2002:a05:6300:2201:b0:38e:7abc:43a5 with SMTP id s1csp1725414pzm;
        Mon, 2 Mar 2026 06:15:34 -0800 (PST)
X-Received: by 2002:a17:903:2a84:b0:2a9:6281:6a56 with SMTP id d9443c01a7336-2ae2e4bbf6dmr99029395ad.6.1772460933802;
        Mon, 02 Mar 2026 06:15:33 -0800 (PST)
ARC-Seal: i=1; a=rsa-sha256; t=1772460933; cv=none;
        d=google.com; s=arc-20240605;
        b=TElDxCCcSlcD5KnExtKAD+ErINA4eQQxvW+GMao9+ySvmw+VFQ2SPmGc1QKCrYTHNc
         O0w44G8VtZ1IzRN0nau+q+da/SAPebS7YgoTOJ3JIblJMuPVMmcaZ++Ckwpeel+OP+jQ
         Fgz2qeSTRbyH/IfbRvM5GVEGqBK6byoM140kndcfTtbGz8OGmS7qUH8PM54jgX6WdLSn
         3AiDBhHGyYqbV9B4B014OK3DNPzAJoVH8ksDnt+LjWGc6xy7kilcW0M8ifM+Ii+bOo2Z
         1CMfdfqE7lVvjlX4M+HEqiAEcpu1xQ9/rJb2cyghnYIPc6aozc7bvw9SSvbWlqk/9QCb
         rUDw==
ARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20240605;
        h=to:subject:message-id:mime-version:from:date
         :content-transfer-encoding:dkim-signature:dkim-signature;
        bh=iAtJxmwcIvTOKqNMZljFeZSr0kgMa3eW64AjVGUWKIY=;
        fh=T5QDzZa2M7aMhMkhW8656uwrK3fHoEEVYLHy1A0M8fE=;
        b=dQTwfLv9rb2Y0YMyWnKbLMoq2WSnkoTSgIUQ69MrRI9siBK3vKhkqq/620+0QfC86n
         NW8WZd5+kLnxHNq1NMCDJlxKIIgraJCrrVo3yNB6TgmcCg6LYVvzO3gfxfNdJNgKbwbf
         Cz63qrsoFW7XaetbB/77QvvLAx5x1YFlKlCC6k0h6CYPzt5g3LFOyeCKdocmjz4HcI4D
         TOsaba3EWXwRGK/3ld6EJy7ywNv65Jveg4y+8sXmtAtPCGQJMR1qh6WatOIhYG4DZgNe
         Hn8/3Kgz8uaagwz3cbIjSDYF3wnAMutUbwG3PbmapqW9mkRaMOVOxP5+TbXCyAIvIydJ
         W9yQ==;
        dara=google.com
ARC-Authentication-Results: i=1; mx.google.com;
       dkim=pass header.i=@raymondli.tech header.s=s1 header.b=ptr07s5q;
       dkim=pass header.i=@sendgrid.info header.s=smtpapi header.b="HsY1/xAl";
       spf=pass (google.com: domain of bounces+57011760-08d3-liadserv=gmail.com@em629.raymondli.tech designates 149.72.184.102 as permitted sender) smtp.mailfrom="bounces+57011760-08d3-liadserv=gmail.com@em629.raymondli.tech";
       dmarc=pass (p=NONE sp=NONE dis=NONE) header.from=raymondli.tech
Return-Path: <bounces+57011760-08d3-liadserv=gmail.com@em629.raymondli.tech>
Received: from s.wrqvbvss.outbound-mail.sendgrid.net (s.wrqvbvss.outbound-mail.sendgrid.net. [149.72.184.102])
        by mx.google.com with ESMTPS id d9443c01a7336-2ae49d2936esi83011905ad.196.2026.03.02.06.15.33
        for <liadserv@gmail.com>
        (version=TLS1_3 cipher=TLS_AES_128_GCM_SHA256 bits=128/128);
        Mon, 02 Mar 2026 06:15:33 -0800 (PST)
Received-SPF: pass (google.com: domain of bounces+57011760-08d3-liadserv=gmail.com@em629.raymondli.tech designates 149.72.184.102 as permitted sender) client-ip=149.72.184.102;
Authentication-Results: mx.google.com;
       dkim=pass header.i=@raymondli.tech header.s=s1 header.b=ptr07s5q;
       dkim=pass header.i=@sendgrid.info header.s=smtpapi header.b="HsY1/xAl";
       spf=pass (google.com: domain of bounces+57011760-08d3-liadserv=gmail.com@em629.raymondli.tech designates 149.72.184.102 as permitted sender) smtp.mailfrom="bounces+57011760-08d3-liadserv=gmail.com@em629.raymondli.tech";
       dmarc=pass (p=NONE sp=NONE dis=NONE) header.from=raymondli.tech
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=raymondli.tech; h=content-transfer-encoding:content-type:date:from:mime-version:subject: to:cc:content-type:date:feedback-id:from:subject:to; s=s1; bh=iAtJxmwcIvTOKqNMZljFeZSr0kgMa3eW64AjVGUWKIY=; b=ptr07s5q6fPaSqrxlCvqXomqFgJDL14LYg6vvHnAP3kp69QbhHHPFH5Rq0/k4tsg4Fj4 ztKVs9XsYfEu5hp1Qmh5cqVk+piA4K3Cf4mUtopeByoOeiIkPOqk9+TGsOkqwbJ/0k/SFg 5B7flQ34QPOwDeJv4zfVnY0cygBFFo2wFX4EifQUYHxgwU9o/c8jyU0qf4Ue1wIgLdgscF DnP7LSubZsaKAzE8xzqJSjw5HQtthGr5I1EcSNA3O8jXzXB9TbHso1IS4ccjUvYEX3L64q MVZ6ROB0+hOpdl8U9NGXFKV/l6vcngs0fvQq0NhBqL4+93y13onKN9qhBEan5L9w==
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=sendgrid.info; h=content-transfer-encoding:content-type:date:from:mime-version:subject: to:cc:content-type:date:feedback-id:from:subject:to; s=smtpapi; bh=iAtJxmwcIvTOKqNMZljFeZSr0kgMa3eW64AjVGUWKIY=; b=HsY1/xAl7mAHLnR3gM93PLsO726ifPm90707CJM2VkvoMwIGs41A0rnzQAsinoopXeDD BoeJ7jAsc/jIqHdOpH7vARg2jMdvwjL81TqzUfo6D2sBifzzIFVmuSzWbCgkVz8cvhhfSp OAcTPaK2EGlOYhGhntSCdIM5z52bshxpY=
Received: by recvd-65c5b6cc87-tkv7f with SMTP id recvd-65c5b6cc87-tkv7f-1-69A59B84-82 2026-03-02 14:15:32.437587062 +0000 UTC m=+6451464.909738679
Received: from NTcwMTE3NjA (unknown) by geopod-ismtpd-5 (SG) with HTTP id j3a2u-hxTHCNK7ajmc2M5A Mon, 02 Mar 2026 14:15:32.336 +0000 (UTC)
Content-Transfer-Encoding: quoted-printable
Content-Type: text/html; charset=utf-8
Date: Mon, 02 Mar 2026 14:15:32 +0000 (UTC)
From: mail@raymondli.tech
Mime-Version: 1.0
Message-ID: <j3a2u-hxTHCNK7ajmc2M5A@geopod-ismtpd-5>
Subject: Hi Paolo Rampino, Open to New Opportunities
X-SG-EID: u001.oeOe1dnTz6srxxQGVvCKPPdzcM9A+Kzix/3GkTEx5XAsC+ef4YuybQ6Z/Smbh9tt7S1hiKGgLBXTeL0t3TgJ29LtV4wbXwZdgvdSylkjFnyINXbMVknep68UFIPFJ4IoYZxWm6IekfrYemPy2SWZc9SArxi57iFv9XCI6J4KAY14ffyvuZh18+kGGTk5p5KYrBTVHAeHR1s+/0DIyg2ygQ==
To: liadserv@gmail.com
X-Entity-ID: u001.5i6p/pdlnmfISs2idvyXEA==

<div style=3D"font-family: Arial, sans-serif; font-size: 18px; line-height:=
 1.7; color: #333; max-width: 700px;">
      Hi Paolo Rampino, I=E2=80=99m Raymond from Texas, a Senior Full-Stack=
 Software Engineer with 10+ years of experience building secure, scalable, =
and reliable web and mobile applications. I specialize in frontend and back=
end development, DevOps and AI integration, and I=E2=80=99ve led projects f=
rom concept to deployment, including custom software, iOS/Android apps, and=
 enterprise web platforms.<br>
<br>
I excel at turning complex workflows into clean, automated processes and in=
tegrating emerging technologies into practical, real-world solutions. I=E2=
=80=99m comfortable joining existing codebases or building solutions from s=
cratch and prioritize clear communication and collaboration with teams and =
stakeholders.<br>
I=E2=80=99m currently open to new opportunities=E2=80=94contract, freelance=
, or full-time=E2=80=94and referrals or introductions are welcome.<br>
<br>
Portfolio: https://raymondli.tech<br>
Github: https://github.com/RL-devone<br>
Email: <strong style=3D"color: #3498db;">mail@raymondli.tech</strong><br>
Whatsapp: +1 (347) 647-0996<br>
<br>
<strong style=3D"font-size: 17px;">Best regards,</strong><br>
Raymond Li
    </div><img src=3D"https://u57011760.ct.sendgrid.net/wf/open?upn=3Du001.=
wbm4Rkf03me9ekxfAKLPHrIa8GjLD5uuPc18u-2B8zQjot7ASeB3n4MivKImhNdrR1DZITfB7Ao=
VpR7wKqiphhmhv2McwhUyFJoN1QcivQf4VLSJNvaoIiKCn0SWrJZiB7GwZrSDlbPNXW1N2XwocE=
nmqXarosrBqd-2BDT1H2Nz3hLWmHXNFIxE6vxH-2B4pEo0Je0G6J-2BzFKFGKfbih9ALw4Jg-3D=
-3D" alt=3D"" width=3D"1" height=3D"1" border=3D"0" style=3D"height:1px !im=
portant;width:1px !important;border-width:0 !important;margin-top:0 !import=
ant;margin-bottom:0 !important;margin-right:0 !important;margin-left:0 !imp=
ortant;padding-top:0 !important;padding-bottom:0 !important;padding-right:0=
 !important;padding-left:0 !important;"/>.
"""
 
prompt = f"""Analizza questa email per indicatori
di phishing. Per ogni indicatore trovato, assegna
un punteggio di rischio (1-10) e spiega.
 
Email:
{email_sospetta}
 
Rispondi in formato tabella Markdown.
"""
 
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=config
)
print(response.text)
